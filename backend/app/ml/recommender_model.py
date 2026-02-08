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
                'email': person.email,  # Agregar email para coincidir con el select del frontend
                'name': person.full_name or 'Sin nombre',
                'score': score,
                'score_percentage': round(score * 100, 2),
                'area': person.area or 'Sin área',
                'role': 'Colaborador',
                'experience_years': person.experience_years or 0,
                'performance_index': person.performance_index or 0,
                'satisfaction_score': person.satisfaction_score or 0,
                'current_workload': workload,
                'skills': person.skills.split(',') if person.skills else [],  # Habilidades reales del usuario
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
            'criteria_used': ['performance_index', 'experience', 'area_match', 'workload', 'skill_match', 'ml_prediction'],
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
    person_area = str(person.area or 'IT')
    role = 'Colaborador'  # Todos los web_users con role_id=7 son colaboradores
    
    # Features numéricas de la persona (ahora con campos reales)
    experience_years_imputed = float(person.experience_years or 2)
    availability_hours_week_imputed = float(person.availability_hours_week or 40.0)
    current_load_imputed = float(person.current_load or 0)
    performance_index_imputed = float(person.performance_index or 50.0)
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
    
    # skill_match_score: coincidencia de habilidades (0-1)
    skill_match_score = calculate_skill_match(person, task_data)
    print(f"  - Skill match: {skill_match_score:.2f}")
    
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


def calculate_skill_match(person, task_data):
    """
    Calcular coincidencia de habilidades entre persona y tarea (0-1)
    
    Args:
        person: WebUser con campo skills
        task_data: dict con skills_required (opcional)
    
    Returns:
        float: Score de 0 a 1 (1 = match perfecto)
    """
    # Obtener habilidades requeridas por la tarea
    required_skills = task_data.get('skills_required', [])
    
    # Si no hay skills requeridas, score neutro
    if not required_skills:
        return 0.5
    
    # Obtener habilidades de la persona
    person_skills_str = person.skills or ''
    if not person_skills_str.strip():
        return 0.2  # Penalización si no tiene habilidades definidas
    
    # Convertir a listas en minúsculas
    person_skills = [s.strip().lower() for s in person_skills_str.split(',')]
    required_skills_lower = [s.strip().lower() for s in required_skills]
    
    # Contar coincidencias
    matches = 0
    for req_skill in required_skills_lower:
        # Match exacto o parcial (ej: "python" en "python avanzado")
        if any(req_skill in p_skill or p_skill in req_skill for p_skill in person_skills):
            matches += 1
    
    # Calcular porcentaje de match
    match_ratio = matches / len(required_skills_lower) if required_skills_lower else 0.5
    
    return match_ratio


def get_candidates(task_data):
    """
    Obtener candidatos de la base de datos
    """
    area = task_data.get('area')
    exclude_ids = task_data.get('exclude_person_ids', [])
    
    # Consulta base: usuarios con role_id = 4 (colaboradores) y activos
    query = WebUser.query.filter(
        WebUser.role_id == 4,  # Solo colaboradores (role_id=4)
        WebUser.status == 'active'  # Solo activos
    )
    
    # Filtrar por área si se especifica (opcional)
    # if area:
    #     query = query.filter(WebUser.area == area)
    
    # Excluir personas específicas
    if exclude_ids:
        query = query.filter(~WebUser.id.in_(exclude_ids))
    
    # Ordenar por nombre
    query = query.order_by(WebUser.full_name)
    
    candidates = query.all()
    print(f"✓ Candidatos encontrados: {len(candidates)}")
    for c in candidates:
        print(f"  - {c.full_name} (ID: {c.id}, Área: {c.area}, Role: {c.role_id})")
    
    return candidates


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
    
    # Habilidades
    skill_match = calculate_skill_match(person, task_data)
    if skill_match >= 0.8:
        reasons.append(f'✅ Habilidades altamente compatibles ({skill_match*100:.0f}%)')
    elif skill_match >= 0.5:
        reasons.append(f'Habilidades compatibles ({skill_match*100:.0f}%)')
    elif skill_match < 0.3 and task_data.get('skills_required'):
        reasons.append(f'⚠️ Habilidades parciales ({skill_match*100:.0f}%)')
    
    # Área
    if person.area == task_data.get('area'):
        reasons.append(f'Experiencia en {person.area}')
    
    # Performance
    if person.performance_index and person.performance_index >= 85:
        reasons.append(f'Rendimiento excelente ({person.performance_index:.0f}%)')
    elif person.performance_index and person.performance_index >= 70:
        reasons.append(f'Buen rendimiento ({person.performance_index:.0f}%)')
    
    # Experiencia
    if person.experience_years and person.experience_years >= 8:
        reasons.append(f'Altamente experimentado ({person.experience_years} años)')
    elif person.experience_years and person.experience_years >= 3:
        reasons.append(f'{person.experience_years} años de experiencia')
    
    # Workload
    workload = person.current_load or 0
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
                'email': person.email,  # Agregar email para coincidir con el select del frontend
                'name': person.full_name or 'Sin nombre',
                'score': score / 100,  # Normalizar a 0-1
                'score_percentage': round(score, 2),
                'area': person.area or 'Sin área',
                'role': 'Colaborador',
                'experience_years': person.experience_years or 0,
                'performance_index': person.performance_index or 0,
                'satisfaction_score': person.satisfaction_score or 0,
                'current_workload': workload,
                'skills': person.skills.split(',') if person.skills else [],  # Habilidades reales del usuario
                'availability': 'Alta' if workload <= 2 else ('Media' if workload <= 4 else 'Baja'),
                'reasons': generate_recommendation_reasons(person, task_data, score / 100)
            })
        
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        top_n = task_data.get('top_n', 5)
        
        return {
            'recommendations': scored_candidates[:top_n],
            'total_candidates': len(candidates),
            'criteria_used': ['area_match', 'workload', 'skill_match', 'performance', 'experience'],
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
    Incluye matching de habilidades
    """
    score = 0
    
    # Performance index (0-30 puntos)
    if person.performance_index:
        score += min(person.performance_index * 30 / 100, 30)
    else:
        score += 15
    
    # Experiencia (0-20 puntos)
    years = person.experience_years or 0
    if years >= 10:
        score += 20
    elif years >= 5:
        score += 15
    elif years >= 2:
        score += 10
    else:
        score += 5
    
    # Workload actual (0-15 puntos)
    workload = person.current_load or 0
    if workload == 0:
        score += 15
    elif workload <= 2:
        score += 12
    elif workload <= 4:
        score += 8
    else:
        score += 3
    
    # Coincidencia de área (0-15 puntos)
    if task_data.get('area') == person.area:
        score += 15
    
    # Coincidencia de habilidades (0-20 puntos) - NUEVO
    skill_match = calculate_skill_match(person, task_data)
    score += skill_match * 20
    
    # Asegurar que el score esté entre 0-100
    return max(0, min(score, 100))
