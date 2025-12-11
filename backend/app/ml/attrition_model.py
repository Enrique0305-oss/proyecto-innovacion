"""
Modelo de Predicción de Renuncia (Attrition)
Predice la probabilidad de que un empleado renuncie
"""
import os
import json
import joblib
import numpy as np
from flask import current_app

from app.extensions import db
from app.models.person import Person


_model = None
_columns = None


def load_attrition_model():
    """
    Cargar modelo de predicción de desempeño/renuncia
    """
    global _model, _columns
    
    if _model is not None:
        return _model
    
    try:
        # Ruta al modelo
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(base_path, 'ml', 'models', 'attrition')
        
        model_file = os.path.join(model_path, 'model_performance_predictor_best.pkl')
        columns_file = os.path.join(model_path, 'columns_performance.json')
        
        if os.path.exists(model_file):
            _model = joblib.load(model_file)
            print(f"✓ Modelo de performance cargado: {model_file}")
        
        if os.path.exists(columns_file):
            with open(columns_file, 'r') as f:
                _columns = json.load(f)
            print(f"✓ Columnas cargadas: {len(_columns.get('feature_columns', []))} features")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo de performance: {str(e)}")
        return None


def prepare_attrition_features(person):
    """
    Preparar features para predicción de performance/renuncia
    
    Features del modelo:
    - person_area (categorical)
    - role (categorical)
    - experience_years
    - availability_hours
    - current_load
    - performance_index
    - rework_rate
    - total_tasks
    - avg_delay_ratio
    - success_rate
    - avg_task_complexity
    - load_ratio
    
    Args:
        person (Person): Objeto Person de la BD
    
    Returns:
        dict: Features preparadas para el modelo
    """
    from app.models.task import Task, Assignee
    from sqlalchemy import func
    
    # Calcular métricas agregadas de tareas
    assignee_stats = db.session.query(
        func.count(Assignee.task_id).label('total_tasks'),
        func.avg(Task.delay_ratio).label('avg_delay_ratio'),
        func.avg(
            db.case(
                (Task.status == 'completed', 1),
                else_=0
            )
        ).label('success_rate'),
        func.avg(Task.complexity_numeric).label('avg_task_complexity')
    ).join(
        Task, Task.task_id == Assignee.task_id
    ).filter(
        Assignee.person_id == person.person_id
    ).first()
    
    total_tasks = assignee_stats.total_tasks or 0
    avg_delay_ratio = float(assignee_stats.avg_delay_ratio or 0)
    success_rate = float(assignee_stats.success_rate or 0)
    avg_task_complexity = float(assignee_stats.avg_task_complexity or 2)
    
    # Calcular load_ratio
    availability_hours = float(person.availability_hours_week or 40)
    current_load = float(person.current_load or 0)
    load_ratio = current_load if availability_hours > 0 else 0
    
    features = {
        'person_area': person.area or 'Unknown',
        'role': person.role or 'Unknown',
        'experience_years': float(person.experience_years or 2),
        'availability_hours': availability_hours,
        'current_load': current_load,
        'performance_index': float(person.performance_index or 75),
        'rework_rate': float(person.rework_rate or 0.05),
        'total_tasks': int(total_tasks),
        'avg_delay_ratio': avg_delay_ratio,
        'success_rate': success_rate,
        'avg_task_complexity': avg_task_complexity,
        'load_ratio': load_ratio
    }
    
    return features


def predict_attrition(data):
    """
    Predecir clase de performance (at_risk, high_performer, resignation_risk)
    
    Args:
        data (dict):
            - person_id: str (requerido)
    
    Returns:
        dict:
            - performance_class: str (at_risk/high_performer/resignation_risk)
            - probabilities: dict con probabilidades de cada clase
            - attrition_probability: float (prob de resignation_risk)
            - attrition_risk: str (bajo/medio/alto)
            - confidence: float (0-1)
            - factors: list[dict] con factores contribuyentes
    """
    model = load_attrition_model()
    
    # Obtener persona de la BD
    person_id = data.get('person_id')
    person = Person.query.get(person_id)
    
    if not person:
        return {
            'performance_class': 'unknown',
            'probabilities': {},
            'attrition_probability': 0.5,
            'attrition_risk': 'desconocido',
            'confidence': 0,
            'factors': [{'factor': 'Persona no encontrada', 'impact': 'N/A'}]
        }
    
    # Si no hay modelo, usar heurística
    if model is None:
        return predict_attrition_heuristic(person)
    
    try:
        # Preparar features
        features_dict = prepare_attrition_features(person)
        
        # Convertir a DataFrame para CatBoost/XGBoost
        import pandas as pd
        features_df = pd.DataFrame([features_dict])
        
        # Predicción
        prediction = model.predict(features_df)[0]
        probas = model.predict_proba(features_df)[0]
        
        # Clases: ['at_risk', 'high_performer', 'resignation_risk']
        class_names = ['at_risk', 'high_performer', 'resignation_risk']
        
        probabilities = {
            class_names[i]: float(probas[i]) 
            for i in range(len(class_names))
        }
        
        performance_class = class_names[prediction]
        attrition_probability = probabilities['resignation_risk']
        
        # Clasificar riesgo de renuncia
        if attrition_probability < 0.15:
            risk = 'bajo'
        elif attrition_probability < 0.50:
            risk = 'medio'
        else:
            risk = 'alto'
        
        # Analizar factores
        factors = analyze_attrition_factors(person, performance_class, probabilities)
        
        return {
            'performance_class': performance_class,
            'probabilities': probabilities,
            'attrition_probability': round(attrition_probability, 4),
            'attrition_risk': risk,
            'confidence': round(float(max(probas)), 4),
            'factors': factors
        }
        
    except Exception as e:
        print(f"✗ Error en predicción de performance: {str(e)}")
        import traceback
        traceback.print_exc()
        return predict_attrition_heuristic(person)


def predict_attrition_heuristic(person):
    """
    Predicción heurística cuando no hay modelo
    """
    risk_score = 0
    factors = []
    
    # Factor: Bajo desempeño
    if person.performance_index and person.performance_index < 60:
        risk_score += 0.3
        factors.append({
            'factor': 'Desempeño bajo',
            'value': f'{person.performance_index}%',
            'impact': 'alto'
        })
    elif person.performance_index and person.performance_index > 90:
        # Alto desempeño
        performance_class = 'high_performer'
        probabilities = {
            'at_risk': 0.05,
            'high_performer': 0.90,
            'resignation_risk': 0.05
        }
        return {
            'performance_class': performance_class,
            'probabilities': probabilities,
            'attrition_probability': 0.05,
            'attrition_risk': 'bajo',
            'confidence': 0.6,
            'factors': [{
                'factor': 'Desempeño excelente',
                'value': f'{person.performance_index}%',
                'impact': 'positivo'
            }]
        }
    
    # Factor: Sobrecarga
    if person.current_load and person.current_load > 0.9:
        risk_score += 0.25
        factors.append({
            'factor': 'Sobrecarga de trabajo',
            'value': f'{person.current_load * 100:.0f}%',
            'impact': 'alto'
        })
    
    # Factor: Alta tasa de retrabajos
    if person.rework_rate and person.rework_rate > 0.2:
        risk_score += 0.2
        factors.append({
            'factor': 'Alta tasa de retrabajos',
            'value': f'{person.rework_rate * 100:.1f}%',
            'impact': 'medio'
        })
    
    # Clasificar
    attrition_probability = min(risk_score, 0.95)
    
    if attrition_probability > 0.5:
        performance_class = 'resignation_risk'
        risk = 'alto'
    elif attrition_probability > 0.3:
        performance_class = 'at_risk'
        risk = 'medio'
    else:
        performance_class = 'high_performer'
        risk = 'bajo'
    
    # Construir probabilities
    if performance_class == 'resignation_risk':
        probabilities = {
            'at_risk': 0.2,
            'high_performer': 0.1,
            'resignation_risk': attrition_probability
        }
    elif performance_class == 'at_risk':
        probabilities = {
            'at_risk': attrition_probability,
            'high_performer': 0.3,
            'resignation_risk': 0.2
        }
    else:
        probabilities = {
            'at_risk': 0.1,
            'high_performer': 1 - attrition_probability,
            'resignation_risk': attrition_probability
        }
    
    return {
        'performance_class': performance_class,
        'probabilities': probabilities,
        'attrition_probability': round(attrition_probability, 4),
        'attrition_risk': risk,
        'confidence': 0.6,
        'factors': factors
    }


def analyze_attrition_factors(person, performance_class, probabilities):
    """
    Analizar factores que contribuyen al performance/renuncia
    """
    factors = []
    
    # Análisis según la clase predicha
    if performance_class == 'resignation_risk':
        factors.append({
            'factor': '⚠️ Alto riesgo de renuncia',
            'value': f'{probabilities["resignation_risk"] * 100:.1f}%',
            'impact': 'crítico'
        })
    elif performance_class == 'high_performer':
        factors.append({
            'factor': '⭐ Alto desempeño',
            'value': f'{probabilities["high_performer"] * 100:.1f}%',
            'impact': 'positivo'
        })
    elif performance_class == 'at_risk':
        factors.append({
            'factor': '⚠️ En riesgo',
            'value': f'{probabilities["at_risk"] * 100:.1f}%',
            'impact': 'alto'
        })
    
    # Análisis de factores clave
    if person.performance_index:
        if person.performance_index < 70:
            factors.append({
                'factor': 'Desempeño bajo',
                'value': f'{person.performance_index}%',
                'impact': 'alto'
            })
        elif person.performance_index > 90:
            factors.append({
                'factor': 'Desempeño excelente',
                'value': f'{person.performance_index}%',
                'impact': 'positivo'
            })
    
    if person.current_load and person.current_load > 0.85:
        factors.append({
            'factor': 'Sobrecarga de trabajo',
            'value': f'{person.current_load * 100:.0f}%',
            'impact': 'alto'
        })
    
    if person.rework_rate and person.rework_rate > 0.15:
        factors.append({
            'factor': 'Alta tasa de retrabajos',
            'value': f'{person.rework_rate * 100:.1f}%',
            'impact': 'medio'
        })
    
    if person.experience_years and person.experience_years < 1:
        factors.append({
            'factor': 'Poca experiencia',
            'value': f'{person.experience_years} años',
            'impact': 'medio'
        })
    
    return factors[:5]  # Top 5 factores
