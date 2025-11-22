"""
Modelo de Predicción de Desempeño
Predice el desempeño esperado de una persona en una tarea específica
"""
import os
import joblib
import numpy as np
from flask import current_app

from app.extensions import db
from app.models.person import Person
from app.models.task import Task, Assignee


_model = None


def load_model():
    """
    Cargar modelo de predicción de desempeño
    """
    global _model
    
    if _model is not None:
        return _model
    
    try:
        # Cargar desde la misma carpeta app/ml/
        ml_path = os.path.dirname(os.path.abspath(__file__))
        model_file = os.path.join(ml_path, 'performance_model.pkl')
        
        if os.path.exists(model_file):
            _model = joblib.load(model_file)
            print(f"✓ Modelo de desempeño cargado: {model_file}")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo de desempeño: {str(e)}")
        return None


def predict_performance(data):
    """
    Predecir el desempeño de una persona en una tarea
    
    Args:
        data (dict):
            - person_id: str (requerido)
            - task_id: str (opcional)
            - task_type: str
            - complexity_level: str
            - area: str
    
    Returns:
        dict:
            - score: float (0-100)
            - level: str (bajo/medio/alto/excelente)
            - strengths: list[str]
            - weaknesses: list[str]
            - confidence: float (0-1)
    """
    model = load_model()
    
    # Obtener persona de la BD
    person = Person.query.get(data.get('person_id'))
    
    if not person:
        return {
            'score': 0,
            'level': 'desconocido',
            'strengths': [],
            'weaknesses': ['Persona no encontrada'],
            'confidence': 0
        }
    
    if model is None:
        return predict_performance_heuristic(person, data)
    
    try:
        features = prepare_features(person, data)
        
        # Predicción
        performance_score = model.predict([features])[0]
        confidence = model.predict_proba([features])[0].max()
        
        # Clasificar nivel
        level = classify_performance_level(performance_score)
        
        # Analizar fortalezas y debilidades
        strengths = identify_strengths(person, data)
        weaknesses = identify_weaknesses(person, data)
        
        return {
            'score': float(performance_score),
            'level': level,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'confidence': float(confidence)
        }
        
    except Exception as e:
        print(f"Error en predicción de desempeño: {str(e)}")
        return predict_performance_heuristic(person, data)


def predict_performance_heuristic(person, data):
    """
    Predicción heurística de desempeño
    """
    score = 50  # Base
    
    # Performance index histórico (peso 40%)
    if person.performance_index:
        score = person.performance_index * 0.4 + score * 0.6
    
    # Experiencia (peso 20%)
    years = person.experience_years or 0
    if years >= 10:
        score += 10
    elif years >= 5:
        score += 7
    elif years >= 2:
        score += 4
    
    # Coincidencia de área (peso 15%)
    if person.area == data.get('area'):
        score += 15
    else:
        score -= 5
    
    # Complejidad vs experiencia (peso 15%)
    complexity = data.get('complexity_level', '').lower()
    if 'high' in complexity or 'alta' in complexity:
        if years >= 5:
            score += 10
        else:
            score -= 10
    elif 'medium' in complexity or 'media' in complexity:
        if years >= 2:
            score += 5
    
    # Satisfacción laboral (peso 10%)
    if person.satisfaction_score:
        score += (person.satisfaction_score - 50) * 0.2
    
    # Workload actual
    from app.ml.recommender_model import get_current_workload
    workload = get_current_workload(person.person_id)
    if workload > 5:
        score -= 10  # Sobrecarga reduce desempeño
    
    score = max(0, min(100, score))
    
    level = classify_performance_level(score)
    strengths = identify_strengths(person, data)
    weaknesses = identify_weaknesses(person, data)
    
    return {
        'score': round(score, 1),
        'level': level,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'confidence': 0.75
    }


def classify_performance_level(score):
    """
    Clasificar el score en un nivel descriptivo
    """
    if score >= 85:
        return 'excelente'
    elif score >= 70:
        return 'alto'
    elif score >= 50:
        return 'medio'
    elif score >= 30:
        return 'bajo'
    else:
        return 'muy bajo'


def identify_strengths(person, data):
    """
    Identificar fortalezas de la persona para esta tarea
    """
    strengths = []
    
    # Performance histórico
    if person.performance_index and person.performance_index >= 80:
        strengths.append(f'Historial de alto rendimiento ({person.performance_index}%)')
    
    # Experiencia
    years = person.experience_years or 0
    if years >= 10:
        strengths.append(f'Amplia experiencia ({years} años)')
    elif years >= 5:
        strengths.append(f'Experiencia sólida ({years} años)')
    
    # Área de especialización
    if person.area == data.get('area'):
        strengths.append(f'Especialista en {person.area}')
    
    # Satisfacción
    if person.satisfaction_score and person.satisfaction_score >= 80:
        strengths.append('Alta motivación y satisfacción laboral')
    
    # Educación
    if person.education_level:
        education = person.education_level.lower()
        if 'master' in education or 'phd' in education or 'doctorado' in education:
            strengths.append('Formación académica avanzada')
    
    # Skills técnicas
    if person.technical_skills:
        strengths.append('Habilidades técnicas documentadas')
    
    return strengths if strengths else ['Perfil profesional estándar']


def identify_weaknesses(person, data):
    """
    Identificar posibles debilidades o riesgos
    """
    weaknesses = []
    
    # Workload
    from app.ml.recommender_model import get_current_workload
    workload = get_current_workload(person.person_id)
    if workload > 5:
        weaknesses.append(f'Alta carga de trabajo actual ({workload} tareas activas)')
    
    # Experiencia limitada
    years = person.experience_years or 0
    complexity = data.get('complexity_level', '').lower()
    if ('high' in complexity or 'alta' in complexity) and years < 3:
        weaknesses.append('Experiencia limitada para tareas de alta complejidad')
    
    # Área diferente
    if data.get('area') and person.area != data.get('area'):
        weaknesses.append(f'Área de especialización diferente ({person.area} vs {data.get("area")})')
    
    # Performance bajo
    if person.performance_index and person.performance_index < 60:
        weaknesses.append('Desempeño histórico por debajo del promedio')
    
    # Satisfacción baja
    if person.satisfaction_score and person.satisfaction_score < 50:
        weaknesses.append('Baja satisfacción laboral puede afectar rendimiento')
    
    # Riesgo de renuncia
    if person.attrition_risk and person.attrition_risk > 0.7:
        weaknesses.append('⚠️ Alto riesgo de deserción')
    
    return weaknesses if weaknesses else []


def prepare_features(person, data):
    """
    Preparar features para el modelo ML
    """
    features = []
    
    # Features de la persona
    features.append(person.performance_index or 50)
    features.append(person.experience_years or 0)
    features.append(person.satisfaction_score or 50)
    features.append(person.attrition_risk or 0.5)
    
    # Workload
    from app.ml.recommender_model import get_current_workload
    features.append(get_current_workload(person.person_id))
    
    # Match de área
    area_match = 1 if person.area == data.get('area') else 0
    features.append(area_match)
    
    # Complejidad de la tarea
    complexity_map = {'low': 1, 'baja': 1, 'medium': 2, 'media': 2, 'high': 3, 'alta': 3}
    complexity = data.get('complexity_level', 'medium').lower()
    features.append(complexity_map.get(complexity, 2))
    
    # Tipo de tarea (hash)
    task_type_hash = hash(data.get('task_type', 'general')) % 5
    features.append(task_type_hash)
    
    return np.array(features)


def get_historical_performance(person_id):
    """
    Obtener desempeño histórico en tareas completadas
    """
    try:
        # Tareas completadas por esta persona
        completed_tasks = Task.query.join(Assignee).filter(
            Assignee.person_id == person_id,
            Task.status == 'Completed'
        ).all()
        
        if not completed_tasks:
            return None
        
        # Calcular métricas
        on_time_count = 0
        total_with_dates = 0
        
        for task in completed_tasks:
            if task.end_date_real and task.end_date_est:
                total_with_dates += 1
                if task.end_date_real <= task.end_date_est:
                    on_time_count += 1
        
        if total_with_dates > 0:
            on_time_rate = (on_time_count / total_with_dates) * 100
            return {
                'total_completed': len(completed_tasks),
                'on_time_rate': round(on_time_rate, 1),
                'tasks_analyzed': total_with_dates
            }
        
        return None
        
    except Exception as e:
        print(f"Error al obtener historial: {str(e)}")
        return None
