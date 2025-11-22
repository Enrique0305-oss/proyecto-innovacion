"""
Modelo de Recomendación de Personas
Recomienda las mejores personas para una tarea específica
"""
import os
import joblib
import numpy as np
from flask import current_app
from sqlalchemy import and_, or_

from app.extensions import db
from app.models.person import Person
from app.models.task import Task, Assignee


_model = None


def load_model():
    """
    Cargar modelo de recomendación
    """
    global _model
    
    if _model is not None:
        return _model
    
    try:
        # Cargar desde la misma carpeta app/ml/
        ml_path = os.path.dirname(os.path.abspath(__file__))
        model_file = os.path.join(ml_path, 'recommender_model.pkl')
        
        if os.path.exists(model_file):
            _model = joblib.load(model_file)
            print(f"✓ Modelo de recomendación cargado: {model_file}")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo de recomendación: {str(e)}")
        return None


def recommend_person(task_data):
    """
    Recomendar las mejores personas para una tarea
    
    Args:
        task_data (dict):
            - area: str (requerido)
            - task_type: str
            - complexity_level: str
            - skills_required: list[str]
            - exclude_person_ids: list[str]
            - top_n: int (default: 5)
    
    Returns:
        dict:
            - recommendations: list[dict] con person_id, score, reasons
            - total_candidates: int
            - criteria_used: list[str]
    """
    model = load_model()
    
    if model is None:
        return recommend_person_heuristic(task_data)
    
    try:
        # Obtener candidatos de la base de datos
        candidates = get_candidates(task_data)
        
        # Calcular scores usando el modelo ML
        scored_candidates = []
        for person in candidates:
            features = prepare_person_features(person, task_data)
            score = model.predict_proba([features])[0][1]  # Probabilidad de éxito
            
            scored_candidates.append({
                'person_id': person.person_id,
                'name': f"{person.first_name} {person.last_name}",
                'score': float(score),
                'area': person.area,
                'role': person.role,
                'experience_years': person.experience_years,
                'performance_index': person.performance_index,
                'reasons': generate_recommendation_reasons(person, task_data)
            })
        
        # Ordenar por score descendente
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # Retornar top N
        top_n = task_data.get('top_n', 5)
        
        return {
            'recommendations': scored_candidates[:top_n],
            'total_candidates': len(candidates),
            'criteria_used': ['performance_index', 'experience', 'area_match', 'workload']
        }
        
    except Exception as e:
        print(f"Error en recomendación: {str(e)}")
        return recommend_person_heuristic(task_data)


def recommend_person_heuristic(task_data):
    """
    Recomendación basada en reglas heurísticas
    """
    try:
        # Obtener candidatos
        candidates = get_candidates(task_data)
        
        # Calcular score heurístico
        scored_candidates = []
        
        for person in candidates:
            score = calculate_heuristic_score(person, task_data)
            
            scored_candidates.append({
                'person_id': person.person_id,
                'name': f"{person.first_name} {person.last_name}",
                'score': score,
                'area': person.area,
                'role': person.role,
                'experience_years': person.experience_years,
                'performance_index': person.performance_index,
                'satisfaction_score': person.satisfaction_score,
                'current_workload': get_current_workload(person.person_id),
                'reasons': generate_recommendation_reasons(person, task_data)
            })
        
        # Ordenar por score
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        top_n = task_data.get('top_n', 5)
        
        return {
            'recommendations': scored_candidates[:top_n],
            'total_candidates': len(candidates),
            'criteria_used': ['area_match', 'performance', 'experience', 'workload', 'satisfaction']
        }
        
    except Exception as e:
        return {
            'recommendations': [],
            'total_candidates': 0,
            'criteria_used': [],
            'error': str(e)
        }


def get_candidates(task_data):
    """
    Obtener candidatos de la base de datos
    """
    area = task_data.get('area')
    exclude_ids = task_data.get('exclude_person_ids', [])
    
    # Consulta base
    query = Person.query.filter(
        Person.resigned == False  # Solo personas activas
    )
    
    # Filtrar por área si se especifica
    if area:
        query = query.filter(Person.area == area)
    
    # Excluir personas específicas
    if exclude_ids:
        query = query.filter(~Person.person_id.in_(exclude_ids))
    
    # Ordenar por performance
    query = query.order_by(Person.performance_index.desc())
    
    return query.all()


def calculate_heuristic_score(person, task_data):
    """
    Calcular score heurístico (0-100)
    """
    score = 0
    
    # Performance index (0-40 puntos)
    if person.performance_index:
        score += min(person.performance_index * 40 / 100, 40)
    else:
        score += 20  # Default
    
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
    
    # Satisfacción (0-15 puntos)
    if person.satisfaction_score:
        score += min(person.satisfaction_score * 15 / 100, 15)
    else:
        score += 7
    
    # Workload actual (0-15 puntos)
    workload = get_current_workload(person.person_id)
    if workload == 0:
        score += 15  # Sin carga
    elif workload <= 2:
        score += 12  # Carga baja
    elif workload <= 4:
        score += 8   # Carga media
    else:
        score += 3   # Carga alta
    
    # Coincidencia de área (0-10 puntos)
    if task_data.get('area') == person.area:
        score += 10
    
    return min(score, 100)


def get_current_workload(person_id):
    """
    Obtener carga de trabajo actual de una persona
    """
    try:
        # Contar tareas activas asignadas
        active_tasks = Assignee.query.join(Task).filter(
            and_(
                Assignee.person_id == person_id,
                Task.status.in_(['Pending', 'In - Progress'])
            )
        ).count()
        
        return active_tasks
        
    except Exception as e:
        print(f"Error al calcular workload: {str(e)}")
        return 0


def generate_recommendation_reasons(person, task_data):
    """
    Generar razones de la recomendación
    """
    reasons = []
    
    # Área
    if person.area == task_data.get('area'):
        reasons.append(f'Experiencia en {person.area}')
    
    # Performance
    if person.performance_index and person.performance_index >= 80:
        reasons.append(f'Alto rendimiento ({person.performance_index}%)')
    
    # Experiencia
    if person.experience_years and person.experience_years >= 5:
        reasons.append(f'{person.experience_years} años de experiencia')
    
    # Workload
    workload = get_current_workload(person.person_id)
    if workload <= 2:
        reasons.append('Baja carga de trabajo actual')
    elif workload > 5:
        reasons.append(f'⚠️ Alta carga actual ({workload} tareas)')
    
    # Satisfacción
    if person.satisfaction_score and person.satisfaction_score >= 80:
        reasons.append('Alta satisfacción laboral')
    
    return reasons if reasons else ['Perfil compatible con la tarea']


def prepare_person_features(person, task_data):
    """
    Preparar features para el modelo ML
    """
    features = []
    
    # Features de la persona
    features.append(person.performance_index or 50)
    features.append(person.experience_years or 0)
    features.append(person.satisfaction_score or 50)
    features.append(get_current_workload(person.person_id))
    
    # Match de área (0 o 1)
    area_match = 1 if person.area == task_data.get('area') else 0
    features.append(area_match)
    
    # Complejidad de la tarea
    complexity_map = {'low': 1, 'baja': 1, 'medium': 2, 'media': 2, 'high': 3, 'alta': 3}
    complexity = task_data.get('complexity_level', 'medium').lower()
    features.append(complexity_map.get(complexity, 2))
    
    return np.array(features)
