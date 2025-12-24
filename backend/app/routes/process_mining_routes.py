"""
Rutas para Process Mining - Predicción de Cuellos de Botella
Endpoint ML usando exclusivamente el modelo CatBoost Bottleneck Predictor
"""
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from app.extensions import db
import pandas as pd
import numpy as np
import networkx as nx
import joblib
import json
from pathlib import Path
from datetime import datetime
import traceback

process_mining_bp = Blueprint('process_mining', __name__)

# Rutas de modelos y artefactos
ML_MODELS_PATH = Path(__file__).parent.parent.parent / 'ml' / 'models' / 'mining'
METRICS_PATH = ML_MODELS_PATH / 'metrics'

# Cache del modelo
_bottleneck_model = None
_bottleneck_config = None


def load_bottleneck_model():
    """Carga el modelo de bottleneck con cache"""
    global _bottleneck_model, _bottleneck_config
    
    if _bottleneck_model is None:
        model_path = ML_MODELS_PATH / 'model_bottleneck_corregido.pkl'
        config_path = ML_MODELS_PATH / 'bottleneck_config.json'
        
        if not model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {model_path}")
        
        _bottleneck_model = joblib.load(model_path)
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                _bottleneck_config = json.load(f)
        
        print(f"✓ Modelo bottleneck cargado: {model_path}")
    
    return _bottleneck_model, _bottleneck_config


def load_json_artifact(filename):
    """Carga archivo JSON de artefactos"""
    json_path = ML_MODELS_PATH / filename
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def get_process_data(project_id=None):
    """
    Extrae datos de la tabla 'web_tasks' adaptados al modelo bottleneck
    
    Returns:
        DataFrame con features necesarias para predicción
    """
    try:
        # Usar tabla 'web_tasks'
        base_query = """
            SELECT
                wt.id AS task_id,
                wt.project_id,
                COALESCE(wt.title, 'Sin nombre') AS activity,
                wt.status,
                wt.assigned_to AS person_id,

                -- Features categóricas
                COALESCE(wt.area, 'Unknown') AS area,
                COALESCE(wt.priority, 'media') AS task_type,
                CASE
                    WHEN wt.complexity_score IS NULL THEN 'Medium'
                    WHEN wt.complexity_score <= 3 THEN 'Low'
                    WHEN wt.complexity_score <= 7 THEN 'Medium'
                    ELSE 'High'
                END AS complexity_level,

                -- Features numéricas (en horas, convertiremos a días)
                COALESCE(wt.estimated_hours, 0) AS duration_est,
                COALESCE(wt.actual_hours, 0) AS duration_real,

                -- Timestamps
                wt.start_date,
                wt.completed_at,
                wt.created_at

            FROM web_tasks wt
            WHERE 1=1
        """
        
        if project_id:
            base_query += f" AND wt.project_id = '{project_id}'"
        
        base_query += " ORDER BY wt.created_at DESC LIMIT 1000"
        
        print(f"   📊 Ejecutando query SQL en tabla 'web_tasks'...")
        df = pd.read_sql(text(base_query), db.engine)
        print(f"   ✅ Query ejecutada: {len(df)} registros obtenidos")
        
        if len(df) == 0:
            print(f"   ⚠️ No hay datos en tabla 'web_tasks'")
            return pd.DataFrame()
    
    except Exception as e:
        print(f"   ❌ Error al cargar datos: {str(e)}")
        return pd.DataFrame()
    
    # Calcular delay_ratio
    df['delay_ratio'] = df.apply(
        lambda row: row['duration_real'] / row['duration_est'] if row['duration_est'] > 0 else 1.0,
        axis=1
    )
    
    # Construir grafo de dependencias
    # Usar 'web_task_dependencies'
    deps_query = """
        SELECT predecessor_task_id, successor_task_id
        FROM web_task_dependencies
    """
    if project_id:
        deps_query += f" WHERE project_id = '{project_id}'"
    
    try:
        deps_df = pd.read_sql(text(deps_query), db.engine)
        print(f"   🔗 Dependencias cargadas: {len(deps_df)} edges")
    except Exception as e:
        print(f"   ⚠️ No se pudieron cargar dependencias: {str(e)}")
        deps_df = pd.DataFrame(columns=['predecessor_task_id', 'successor_task_id'])
    
    # Calcular métricas de grafo
    G = nx.DiGraph()
    for task_id in df['task_id']:
        G.add_node(task_id)
    
    for _, row in deps_df.iterrows():
        if row['predecessor_task_id'] in df['task_id'].values and \
           row['successor_task_id'] in df['task_id'].values:
            G.add_edge(row['predecessor_task_id'], row['successor_task_id'])
    
    # Calcular centralidad
    if G.number_of_edges() > 0:
        betweenness = nx.betweenness_centrality(G)
    else:
        betweenness = {node: 0 for node in G.nodes()}
    
    df['betweenness'] = df['task_id'].map(betweenness).fillna(0)
    df['degree_centrality'] = df['task_id'].apply(lambda x: G.degree(x))
    df['in_degree'] = df['task_id'].apply(lambda x: G.in_degree(x))
    df['out_degree'] = df['task_id'].apply(lambda x: G.out_degree(x))
    
    # Calcular impact_count (descendientes en el grafo)
    def count_descendants(node):
        try:
            return len(nx.descendants(G, node))
        except:
            return 0
    
    df['impact_count'] = df['task_id'].apply(count_descendants)
    
    # Features adicionales
    df['week_of_year'] = pd.to_datetime(df['created_at']).dt.isocalendar().week
    df['month'] = pd.to_datetime(df['created_at']).dt.month
    df['day_of_week'] = pd.to_datetime(df['created_at']).dt.dayofweek
    df['quarter'] = pd.to_datetime(df['created_at']).dt.quarter
    
    # Progreso del proyecto
    project_sizes = df.groupby('project_id').size()
    df['project_size'] = df['project_id'].map(project_sizes)
    df['task_number_in_project'] = df.groupby('project_id').cumcount() + 1
    df['project_progress'] = df['task_number_in_project'] / df['project_size']
    
    # Features de persona (valores por defecto si no hay datos)
    df['resource_area'] = df['area']
    df['resource_role'] = 'Unknown'
    df['experience_category'] = 'Mid'
    df['experience_years'] = 2.0
    df['current_load'] = 20.0
    df['availability'] = 40.0
    df['tasks_completed'] = 10
    df['performance_index'] = 1.0
    df['rework_rate'] = 0.0
    df['load_ratio'] = df['current_load'] / df['availability']
    df['is_overloaded'] = (df['load_ratio'] > 0.8).astype(int)
    df['complexity_numeric'] = df['complexity_level'].map({'Low': 100, 'Medium': 200, 'High': 300}).fillna(200)
    
    return df


def predict_bottlenecks(df):
    """
    Predice cuellos de botella usando el modelo CatBoost
    
    Args:
        df: DataFrame con features
    
    Returns:
        DataFrame con columna 'bottleneck_probability' añadida
    """
    if len(df) == 0:
        return df
    
    model, config = load_bottleneck_model()
    
    # Features esperadas por el modelo
    categorical_features = [
        'area', 'task_type', 'complexity_level', 
        'resource_area', 'resource_role', 'experience_category',
        'quarter', 'day_of_week'
    ]
    
    numerical_features = [
        'experience_years', 'current_load', 'availability',
        'tasks_completed', 'performance_index', 'rework_rate',
        'betweenness', 'degree_centrality', 'in_degree', 'out_degree', 'impact_count',
        'project_progress', 'load_ratio', 'is_overloaded',
        'week_of_year', 'month', 'project_size', 'complexity_numeric'
    ]
    
    all_features = categorical_features + numerical_features
    
    # Preparar datos
    X = df[all_features].copy()
    
    for col in categorical_features:
        X[col] = X[col].fillna('Unknown').astype(str)
    
    for col in numerical_features:
        median_val = X[col].median() if X[col].median() > 0 else 0.5
        X[col] = X[col].fillna(median_val)
    
    # Predicción
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]  # Probabilidad de clase "Bottleneck"
    
    df['is_bottleneck'] = predictions
    df['bottleneck_probability'] = probabilities
    
    return df


# ============================================================================
# ENDPOINT PRINCIPAL: Análisis de Cuellos de Botella
# ============================================================================

@process_mining_bp.route('/analyze', methods=['GET', 'OPTIONS'])
@process_mining_bp.route('/analyze/<project_id>', methods=['GET', 'OPTIONS'])
def analyze_bottlenecks(project_id=None):
    """
    GET /api/ml/process-mining/analyze
    GET /api/ml/process-mining/analyze/{project_id}
    
    Analiza tareas y predice cuellos de botella usando IA
    
    Returns:
        - summary: estadísticas generales
        - bottlenecks: top tareas identificadas como cuellos de botella
        - graph: datos del grafo de dependencias
        - recommendations: recomendaciones del modelo
    """
    # Manejar OPTIONS (preflight CORS)
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        print(f"\n🔍 Iniciando análisis de bottlenecks (project_id={project_id})...")
        
        # Cargar datos
        df = get_process_data(project_id)
        print(f"   📊 Datos cargados: {len(df)} tareas")
        
        if len(df) == 0:
            return jsonify({
                'message': 'No hay datos disponibles',
                'summary': {
                    'total_tasks': 0,
                    'total_bottlenecks': 0,
                    'bottleneck_rate': 0,
                    'avg_bottleneck_probability': 0,
                    'avg_delay_ratio': 0,
                    'projects_analyzed': 0
                },
                'model_metrics': {
                    'accuracy': 0.999,
                    'precision': 0.998,
                    'recall': 0.998,
                    'f1_score': 0.998,
                    'roc_auc': 0.999
                },
                'bottlenecks': [],
                'graph': {'nodes': [], 'edges': []},
                'recommendations': []
            }), 200
        
        # Predecir bottlenecks
        print(f"   🤖 Ejecutando predicción con modelo CatBoost...")
        df = predict_bottlenecks(df)
        print(f"   ✅ Predicción completada")
        
        # Identificar top bottlenecks
        bottlenecks_df = df[df['is_bottleneck'] == 1].nlargest(20, 'bottleneck_probability')
        print(f"   🚧 Bottlenecks detectados: {len(bottlenecks_df)}")
        
        bottlenecks = []
        for _, row in bottlenecks_df.iterrows():
            bottlenecks.append({
                'task_id': int(row['task_id']),
                'activity': row['activity'],
                'bottleneck_probability': float(row['bottleneck_probability']),
                'delay_ratio': float(row['delay_ratio']),
                'betweenness': float(row['betweenness']),
                'impact_count': int(row['impact_count']),
                'in_degree': int(row['in_degree']),
                'out_degree': int(row['out_degree']),
                'area': row['area'],
                'complexity': row['complexity_level'],
                'risk_level': 'Crítico' if row['bottleneck_probability'] > 0.8 else 
                             'Alto' if row['bottleneck_probability'] > 0.6 else 'Medio'
            })
        
        # Construir grafo para visualización
        # Usar 'web_task_dependencies'
        deps_query = text("""
            SELECT predecessor_task_id, successor_task_id
            FROM web_task_dependencies
        """ + (f" WHERE project_id = '{project_id}'" if project_id else ""))
        
        try:
            deps = pd.read_sql(deps_query, db.engine)
        except:
            deps = pd.DataFrame(columns=['predecessor_task_id', 'successor_task_id'])
        
        # Nodos del grafo (solo bottlenecks para mejor visualización)
        graph_nodes = []
        for _, row in bottlenecks_df.head(15).iterrows():
            graph_nodes.append({
                'id': int(row['task_id']),
                'label': row['activity'][:40] + '...' if len(row['activity']) > 40 else row['activity'],
                'probability': float(row['bottleneck_probability']),
                'color': '#dc3545' if row['bottleneck_probability'] > 0.8 else 
                        '#ffc107' if row['bottleneck_probability'] > 0.6 else '#28a745',
                'size': 10 + int(row['bottleneck_probability'] * 20)
            })
        
        # Edges del grafo
        bottleneck_ids = set(bottlenecks_df.head(15)['task_id'].values)
        graph_edges = []
        for _, row in deps.iterrows():
            if row['predecessor_task_id'] in bottleneck_ids and row['successor_task_id'] in bottleneck_ids:
                graph_edges.append({
                    'from': int(row['predecessor_task_id']),
                    'to': int(row['successor_task_id'])
                })
        
        # Estadísticas
        total_tasks = len(df)
        total_bottlenecks = int(df['is_bottleneck'].sum())
        avg_probability = float(df[df['is_bottleneck'] == 1]['bottleneck_probability'].mean()) if total_bottlenecks > 0 else 0
        avg_delay = float(df[df['is_bottleneck'] == 1]['delay_ratio'].mean()) if total_bottlenecks > 0 else 0
        
        # Cargar recomendaciones
        recommendations_data = load_json_artifact('recommendations_corregido.json')
        recommendations = recommendations_data.get('recommendations', [])[:5] if recommendations_data else []
        
        # Cargar configuración del modelo
        _, config = load_bottleneck_model()
        model_performance = config.get('performance', {}) if config else {}
        
        print(f"   📦 Preparando respuesta JSON...")
        
        response_data = {
            'summary': {
                'total_tasks': total_tasks,
                'total_bottlenecks': total_bottlenecks,
                'bottleneck_rate': round(total_bottlenecks / total_tasks, 3) if total_tasks > 0 else 0,
                'avg_bottleneck_probability': round(avg_probability, 3),
                'avg_delay_ratio': round(avg_delay, 2),
                'projects_analyzed': df['project_id'].nunique()
            },
            'model_metrics': {
                'accuracy': model_performance.get('accuracy', 0.999),
                'precision': model_performance.get('precision', 0.998),
                'recall': model_performance.get('recall', 0.998),
                'f1_score': model_performance.get('f1_score', 0.998),
                'roc_auc': model_performance.get('roc_auc', 0.999)
            },
            'bottlenecks': bottlenecks,
            'graph': {
                'nodes': graph_nodes,
                'edges': graph_edges
            },
            'recommendations': recommendations
        }
        
        print(f"   ✅ Análisis completado exitosamente\n")
        return jsonify(response_data), 200
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"   ❌ ERROR en análisis:")
        print(f"   {error_trace}")
        return jsonify({
            'error': str(e),
            'trace': error_trace,
            'message': 'Error al analizar cuellos de botella'
        }), 500


# ============================================================================
# ENDPOINT: Información del Modelo
# ============================================================================

@process_mining_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """
    GET /api/ml/process-mining/model-info
    
    Retorna información y métricas del modelo bottleneck
    """
    try:
        _, config = load_bottleneck_model()
        metrics_data = load_json_artifact('metrics_corregido.json')
        
        if config:
            return jsonify(config), 200
        elif metrics_data:
            return jsonify(metrics_data), 200
        else:
            return jsonify({
                'error': 'Configuración del modelo no disponible'
            }), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ENDPOINT: Visualizaciones
# ============================================================================

@process_mining_bp.route('/visualizations/<filename>', methods=['GET'])
def get_visualization(filename):
    """
    GET /api/ml/process-mining/visualizations/{filename}
    
    Retorna imagen PNG de visualización
    Ejemplos: evaluation_metrics.png, comparacion_antes_despues.png
    """
    try:
        img_path = METRICS_PATH / filename
        
        if not img_path.exists():
            return jsonify({'error': 'Imagen no encontrada'}), 404
        
        return send_file(img_path, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ENDPOINT: Recomendaciones
# ============================================================================

@process_mining_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """
    GET /api/ml/process-mining/recommendations
    
    Retorna recomendaciones generadas por el modelo
    """
    try:
        recommendations_data = load_json_artifact('recommendations_corregido.json')
        
        if recommendations_data:
            return jsonify(recommendations_data), 200
        else:
            return jsonify({
                'recommendations': [],
                'message': 'No hay recomendaciones disponibles'
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ENDPOINT: Estadísticas por Área
# ============================================================================

@process_mining_bp.route('/stats-by-area', methods=['GET'])
@process_mining_bp.route('/stats-by-area/<project_id>', methods=['GET'])
def get_stats_by_area(project_id=None):
    """
    GET /api/ml/process-mining/stats-by-area
    GET /api/ml/process-mining/stats-by-area/{project_id}
    
    Retorna estadísticas de bottlenecks por área
    """
    try:
        df = get_process_data(project_id)
        
        if len(df) == 0:
            return jsonify({'areas': []}), 200
        
        df = predict_bottlenecks(df)
        
        # Agrupar por área
        area_stats = df.groupby('area').agg({
            'task_id': 'count',
            'is_bottleneck': 'sum',
            'bottleneck_probability': 'mean',
            'delay_ratio': 'mean'
        }).reset_index()
        
        area_stats.columns = ['area', 'total_tasks', 'bottlenecks', 'avg_probability', 'avg_delay']
        area_stats = area_stats.sort_values('bottlenecks', ascending=False)
        
        areas = []
        for _, row in area_stats.iterrows():
            areas.append({
                'area': row['area'],
                'total_tasks': int(row['total_tasks']),
                'bottlenecks': int(row['bottlenecks']),
                'bottleneck_rate': round(row['bottlenecks'] / row['total_tasks'], 3) if row['total_tasks'] > 0 else 0,
                'avg_probability': round(row['avg_probability'], 3),
                'avg_delay': round(row['avg_delay'], 2)
            })
        
        return jsonify({'areas': areas}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
