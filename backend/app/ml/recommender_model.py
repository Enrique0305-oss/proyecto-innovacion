"""
Modelo de Recomendación de Personas - CatBoost
Recomienda las mejores personas para una tarea específica usando ranking
"""
import os
import json
import numpy as np
import pandas as pd
from catboost import CatBoost
from sqlalchemy import and_

from app.extensions import db
from app.models.web_user import WebUser
from app.models.web_task import WebTask


# Variables globales para modelo y configuración
_model = None
_config = None
_metrics = None


def load_model():
    """
    Cargar el modelo CatBoost de recomendación (.pkl) y sus configuraciones
    """
    global _model, _config, _metrics
    
    if _model is not None:
        return _model
    
    try:
        # Ruta al modelo
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(base_path, 'ml', 'models', 'recommender')
        
        model_file = os.path.join(model_path, 'model_catboost_recommender.pkl')
        config_file = os.path.join(model_path, 'columns_recommender.json')
        metrics_file = os.path.join(model_path, 'recommender_metrics.json')
        
        # Cargar modelo CatBoost
        if os.path.exists(model_file):
            import joblib
            _model = joblib.load(model_file)
            print(f"✓ Modelo CatBoost Recommender cargado: {model_file}")
        else:
            print(f"⚠ Modelo no encontrado: {model_file}")
            return None
        
        # Cargar configuración de columnas
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                _config = json.load(f)
            print(f"✓ Configuración cargada: {config_file}")
            print(f"   Features: {len(_config.get('all_columns', []))}")
        
        # Cargar métricas
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r', encoding='utf-8') as f:
                _metrics = json.load(f)
            print(f"✓ Métricas cargadas")
            print(f"   ROC-AUC: {_metrics.get('classification_metrics', {}).get('roc_auc', 0):.4f}")
            print(f"   Accuracy: {_metrics.get('classification_metrics', {}).get('accuracy', 0):.4f}")
            print(f"   Accuracy@1: {_metrics.get('ranking_metrics', {}).get('accuracy_at_1', 0)/100:.4f}")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def recommend_person(task_data):
    """
    Recomendar las mejores personas para una tarea usando el modelo CatBoost
    
    Args:
        task_data (dict):
            - area: str (requerido)
            - task_type: str
            - complexity_level: str
            - duration_est: int (días)
            - priority: str
            - skills_required: list[str] (opcional)
            - exclude_person_ids: list[str] (opcional)
            - top_n: int (default: 5)
    
    Returns:
        dict:
            - recommendations: list[dict] con person_id, score, reasons
            - total_candidates: int
            - criteria_used: list[str]
    """
    model = load_model()
    
    if model is None:
        print("⚠ Modelo no disponible, usando heurística")
        return recommend_person_heuristic(task_data)
    
    try:
        # Obtener candidatos de la base de datos
        candidates = get_candidates(task_data)
        
        if not candidates:
            return {
                'recommendations': [],
                'total_candidates': 0,
                'criteria_used': [],
                'message': 'No se encontraron candidatos disponibles'
            }
        
        print(f"\n🔍 Evaluando {len(candidates)} candidatos...")
        
        # Calcular scores usando el modelo ML
        scored_candidates = []
        
        for person in candidates:
            # Preparar features para el modelo
            features_df = prepare_features(person, task_data)
            
            # Predicción: probabilidad de que sea una buena asignación
            prediction_proba = model.predict_proba(features_df)[0]
            
            # Tomamos la probabilidad de la clase positiva (buena asignación)
            score = float(prediction_proba[1]) if len(prediction_proba) > 1 else float(prediction_proba[0])
            
            # Calcular métricas adicionales
            workload = get_current_workload(person.id)
            
            scored_candidates.append({
                'person_id': person.id,
                'name': person.full_name or 'Sin nombre',
                'score': score,
                'score_percentage': round(score * 100, 2),
                'area': person.area or 'Sin área',
                'role': 'Colaborador',  # role_id = 1
                'experience_years': 0,  # WebUser no tiene este campo
                'performance_index': 0,  # WebUser no tiene este campo
                'satisfaction_score': 0,  # WebUser no tiene este campo
                'current_workload': workload,
                'skills': task_data.get('skills_required', [])[:4],  # Primeras 4 skills
                'availability': 'Alta' if workload <= 2 else ('Media' if workload <= 4 else 'Baja'),
                'reasons': generate_recommendation_reasons(person, task_data, score)
            })
        
        # Ordenar por score descendente
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # Retornar top N
        top_n = task_data.get('top_n', 5)
        
        print(f"✓ Top {min(top_n, len(scored_candidates))} recomendaciones generadas")
        
        return {
            'recommendations': scored_candidates[:top_n],
            'total_candidates': len(candidates),
            'criteria_used': ['performance_index', 'experience', 'area_match', 'workload', 'ml_prediction'],
            'model_used': 'catboost_recommender'
        }
        
    except Exception as e:
        print(f"✗ Error en recomendación: {str(e)}")
        import traceback
        traceback.print_exc()
        return recommend_person_heuristic(task_data)


def prepare_features(person, task_data):
    """
    Preparar features que el modelo espera según columns_recommender.json
    
    Features del modelo:
    - task_area, task_type, complexity_level (categóricas de la tarea)
    - person_area, role (categóricas de la persona)
    - duration_est_imputed, experience_years_imputed, availability_hours_week_imputed,
      current_load_imputed, performance_index_imputed, rework_rate_imputed (numéricas)
    - match_area, match_role_type (binarias)
    - experience_complexity_ratio, load_capacity_ratio (derivadas)
    """
    global _config
    
    print(f"\n🔧 Preparando features para: {person.full_name}")
    
    # Features de la tarea (categóricas)
    task_area = str(task_data.get('area', 'TI'))
    task_type = str(task_data.get('task_type', 'Desarrollo'))
    complexity_level = str(task_data.get('complexity_level', 'Media'))
    duration_est_imputed = float(task_data.get('duration_est', 10))
    
    # Features de la persona (categóricas)
    person_area = str(person.area or 'TI')
    role = 'Colaborador'  # Todos los web_users con role_id=1 son colaboradores
    
    # Features numéricas de la persona (WebUser no tiene estos campos, usamos defaults)
    experience_years_imputed = 2.0  # Default
    availability_hours_week_imputed = 40.0  # Default 40 horas/semana
    current_load_imputed = float(get_current_workload(person.id))
    performance_index_imputed = 50.0  # Default
    rework_rate_imputed = 0.1  # Default 10% de retrabajo
    
    # Features binarias
    match_area = 1.0 if person_area == task_area else 0.0
    match_role_type = 1.0 if _matches_role_type(role, task_type) else 0.0
    
    # Features derivadas
    # experience_complexity_ratio: experiencia ajustada por complejidad
    complexity_map = {'Baja': 1, 'Media': 2, 'Alta': 3, 'baja': 1, 'media': 2, 'alta': 3}
    complexity_numeric = complexity_map.get(complexity_level, 2)
    experience_complexity_ratio = experience_years_imputed / max(complexity_numeric, 1)
    
    # load_capacity_ratio: capacidad disponible vs carga actual
    max_capacity = 10.0  # Máximo de tareas simultáneas
    load_capacity_ratio = current_load_imputed / max_capacity if max_capacity > 0 else 0.0
    
    # Crear diccionario con TODAS las features en el orden correcto según all_features
    feature_dict = {
        'task_area': task_area,
        'task_type': task_type,
        'complexity_level': complexity_level,
        'duration_est_imputed': duration_est_imputed,
        'person_area': person_area,
        'role': role,
        'experience_years_imputed': experience_years_imputed,
        'availability_hours_week_imputed': availability_hours_week_imputed,
        'current_load_imputed': current_load_imputed,
        'performance_index_imputed': performance_index_imputed,
        'rework_rate_imputed': rework_rate_imputed,
        'match_area': match_area,
        'experience_complexity_ratio': experience_complexity_ratio,
        'load_capacity_ratio': load_capacity_ratio,
        'match_role_type': match_role_type
    }
    
    # Crear DataFrame
    df = pd.DataFrame([feature_dict])
    
    # Asegurar orden correcto según config
    if _config and 'all_features' in _config:
        df = df[_config['all_features']]
    
    print(f"✓ Features preparados: {df.shape}")
    print(f"  - Categóricas: {task_area}, {task_type}, {complexity_level}, {person_area}, {role}")
    print(f"  - Match área: {match_area}, Experience: {experience_years_imputed}, Load: {current_load_imputed}")
    
    return df


def _matches_role_type(role, task_type):
    """
    Determinar si el rol de la persona coincide con el tipo de tarea
    """
    role_lower = role.lower()
    task_lower = task_type.lower()
    
    # Mapeo simple de roles a tipos de tarea
    role_task_map = {
        'developer': ['desarrollo', 'development'],
        'designer': ['diseño', 'design'],
        'analyst': ['análisis', 'analysis'],
        'tester': ['testing', 'qa'],
        'devops': ['soporte', 'support', 'desarrollo'],
        'pm': ['documentación', 'documentation']
    }
    
    for role_key, task_types in role_task_map.items():
        if role_key in role_lower:
            return any(t in task_lower for t in task_types)
    
    return False  # Por defecto no hay match


def get_candidates(task_data):
    """
    Obtener candidatos de la base de datos
    """
    area = task_data.get('area')
    exclude_ids = task_data.get('exclude_person_ids', [])
    
    # Consulta base: usuarios con role_id = 7 (colaboradores) y activos
    query = WebUser.query.filter(
        WebUser.role_id == 7,  # Solo colaboradores
        WebUser.status == 'active'  # Solo activos
    )
    
    # Filtrar por área si se especifica
    if area:
        query = query.filter(WebUser.area == area)
    
    # Excluir personas específicas
    if exclude_ids:
        query = query.filter(~WebUser.id.in_(exclude_ids))
    
    # Ordenar por nombre
    query = query.order_by(WebUser.full_name)
    
    return query.all()


def get_current_workload(user_id):
    """
    Obtener carga de trabajo actual de un usuario
    """
    try:
        # Contar tareas activas asignadas en web_tasks
        active_tasks = WebTask.query.filter(
            and_(
                WebTask.assigned_to == user_id,
                WebTask.status.in_(['pending', 'in_progress'])
            )
        ).count()
        
        return active_tasks
        
    except Exception as e:
        print(f"Error al calcular workload: {str(e)}")
        return 0


def generate_recommendation_reasons(person, task_data, score):
    """
    Generar razones de la recomendación basadas en el score del modelo
    """
    reasons = []
    
    # Score del modelo
    if score >= 0.9:
        reasons.append(f'Coincidencia excepcional ({score*100:.1f}%)')
    elif score >= 0.8:
        reasons.append(f'Muy buena compatibilidad ({score*100:.1f}%)')
    elif score >= 0.7:
        reasons.append(f'Buena compatibilidad ({score*100:.1f}%)')
    
    # Área
    if person.area == task_data.get('area'):
        reasons.append(f'Experiencia en {person.area}')
    
    # Workload (usar person.id en lugar de person.person_id)
    workload = get_current_workload(person.id)
    if workload == 0:
        reasons.append('Disponibilidad completa')
    elif workload <= 2:
        reasons.append('Buena disponibilidad')
    elif workload >= 6:
        reasons.append(f'⚠️ Alta carga ({workload} tareas activas)')
    
    return reasons if reasons else ['Perfil compatible con la tarea']


def recommend_person_heuristic(task_data):
    """
    Recomendación basada en reglas heurísticas (fallback)
    """
    try:
        candidates = get_candidates(task_data)
        
        if not candidates:
            return {
                'recommendations': [],
                'total_candidates': 0,
                'criteria_used': []
            }
        
        scored_candidates = []
        
        for person in candidates:
            score = calculate_heuristic_score(person, task_data)
            workload = get_current_workload(person.id)
            
            scored_candidates.append({
                'person_id': person.id,
                'name': person.full_name or 'Sin nombre',
                'score': score / 100,  # Normalizar a 0-1
                'score_percentage': round(score, 2),
                'area': person.area or 'Sin área',
                'role': 'Colaborador',
                'experience_years': 0,  # WebUser no tiene este campo
                'performance_index': 0,  # WebUser no tiene este campo
                'satisfaction_score': 0,  # WebUser no tiene este campo
                'current_workload': workload,
                'skills': task_data.get('skills_required', [])[:4],
                'availability': 'Alta' if workload <= 2 else ('Media' if workload <= 4 else 'Baja'),
                'reasons': generate_recommendation_reasons(person, task_data, score / 100)
            })
        
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        top_n = task_data.get('top_n', 5)
        
        return {
            'recommendations': scored_candidates[:top_n],
            'total_candidates': len(candidates),
            'criteria_used': ['area_match', 'workload'],
            'model_used': 'heuristic_fallback'
        }
        
    except Exception as e:
        print(f"Error en heurística: {str(e)}")
        return {
            'recommendations': [],
            'total_candidates': 0,
            'criteria_used': [],
            'error': str(e)
        }


def calculate_heuristic_score(person, task_data):
    """
    Calcular score heurístico (0-100) para WebUser
    """
    score = 50  # Base score para colaboradores
    
    # Match de área (+30 puntos)
    if person.area == task_data.get('area'):
        score += 30
    
    # Workload (-10 puntos por tarea activa)
    workload = get_current_workload(person.id)
    score -= min(workload * 10, 30)
    
    # Asegurar que el score esté entre 0-100
    return max(0, min(score, 100))
    
    # Satisfacción (0-15 puntos)
    if person.satisfaction_score:
        score += min(person.satisfaction_score * 15 / 100, 15)
    else:
        score += 7
    
    # Asegurar que el score esté entre 0-100
    return max(0, min(score, 100))
