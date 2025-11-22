"""
Modelo de Predicción de Riesgo
Predice el nivel de riesgo de una tarea basado en sus características
"""
import os
import joblib
import numpy as np
from flask import current_app


# Variable global para el modelo cargado
_model = None
_label_encoders = None


def load_model():
    """
    Cargar el modelo de predicción de riesgo desde archivo .pkl
    """
    global _model, _label_encoders
    
    if _model is not None:
        return _model
    
    try:
        # Cargar desde la misma carpeta app/ml/
        ml_path = os.path.dirname(os.path.abspath(__file__))
        model_file = os.path.join(ml_path, 'risk_model.pkl')
        encoders_file = os.path.join(ml_path, 'risk_encoders.pkl')
        
        if os.path.exists(model_file):
            _model = joblib.load(model_file)
            print(f"✓ Modelo de riesgo cargado: {model_file}")
        
        if os.path.exists(encoders_file):
            _label_encoders = joblib.load(encoders_file)
            print(f"✓ Encoders de riesgo cargados: {encoders_file}")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo de riesgo: {str(e)}")
        return None


def predict_risk(task_data):
    """
    Predecir el riesgo de una tarea
    
    Args:
        task_data (dict): Datos de la tarea
            - complexity_level: str
            - priority: str
            - area: str
            - task_type: str
            - duration_est: int (opcional)
            - assignees_count: int (opcional)
            - dependencies: int (opcional)
    
    Returns:
        dict: Predicción de riesgo
            - risk_level: str (bajo/medio/alto)
            - probability: float (0-1)
            - factors: list[str]
            - recommendations: list[str]
    """
    model = load_model()
    
    # Si no hay modelo, usar reglas heurísticas
    if model is None:
        return predict_risk_heuristic(task_data)
    
    try:
        # Preparar features
        features = prepare_features(task_data)
        
        # Hacer predicción
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]
        
        # Mapear predicción a nivel de riesgo
        risk_levels = ['bajo', 'medio', 'alto']
        risk_level = risk_levels[prediction] if prediction < len(risk_levels) else 'medio'
        
        # Identificar factores de riesgo
        factors = identify_risk_factors(task_data, risk_level)
        
        # Generar recomendaciones
        recommendations = generate_recommendations(task_data, risk_level)
        
        return {
            'risk_level': risk_level,
            'probability': float(max(probability)),
            'factors': factors,
            'recommendations': recommendations
        }
        
    except Exception as e:
        print(f"Error en predicción de riesgo: {str(e)}")
        return predict_risk_heuristic(task_data)


def predict_risk_heuristic(task_data):
    """
    Predicción de riesgo usando reglas heurísticas (fallback)
    """
    risk_score = 0
    factors = []
    
    # Factor: Complejidad
    complexity = task_data.get('complexity_level', '').lower()
    if 'high' in complexity or 'alta' in complexity:
        risk_score += 3
        factors.append('Complejidad alta')
    elif 'medium' in complexity or 'media' in complexity:
        risk_score += 2
        factors.append('Complejidad media')
    else:
        risk_score += 1
    
    # Factor: Prioridad
    priority = task_data.get('priority', '').lower()
    if 'high' in priority or 'alta' in priority:
        risk_score += 2
        factors.append('Prioridad alta')
    elif 'critical' in priority or 'crítica' in priority:
        risk_score += 3
        factors.append('Prioridad crítica')
    
    # Factor: Duración estimada
    duration = task_data.get('duration_est', 0)
    if duration > 30:
        risk_score += 2
        factors.append('Duración larga (>30 días)')
    elif duration > 14:
        risk_score += 1
        factors.append('Duración moderada (>14 días)')
    
    # Factor: Número de asignados
    assignees = task_data.get('assignees_count', 1)
    if assignees > 5:
        risk_score += 1
        factors.append('Múltiples asignados (>5)')
    elif assignees == 0:
        risk_score += 2
        factors.append('Sin asignados')
    
    # Factor: Dependencias
    dependencies = task_data.get('dependencies', 0)
    if dependencies > 3:
        risk_score += 2
        factors.append('Múltiples dependencias (>3)')
    
    # Determinar nivel de riesgo
    if risk_score >= 7:
        risk_level = 'alto'
    elif risk_score >= 4:
        risk_level = 'medio'
    else:
        risk_level = 'bajo'
    
    # Generar recomendaciones
    recommendations = generate_recommendations(task_data, risk_level)
    
    return {
        'risk_level': risk_level,
        'probability': min(risk_score / 10, 1.0),
        'factors': factors,
        'recommendations': recommendations
    }


def prepare_features(task_data):
    """
    Preparar features para el modelo ML
    """
    global _label_encoders
    
    features = []
    
    # Aquí se debe transformar task_data en el formato que espera el modelo
    # Ejemplo básico:
    
    categorical_fields = ['complexity_level', 'priority', 'area', 'task_type']
    
    for field in categorical_fields:
        value = task_data.get(field, 'unknown')
        
        if _label_encoders and field in _label_encoders:
            try:
                encoded = _label_encoders[field].transform([value])[0]
            except:
                encoded = 0
        else:
            # Encoding simple si no hay label encoder
            encoded = hash(value) % 100
        
        features.append(encoded)
    
    # Features numéricas
    features.append(task_data.get('duration_est', 0))
    features.append(task_data.get('assignees_count', 0))
    features.append(task_data.get('dependencies', 0))
    
    return np.array(features)


def identify_risk_factors(task_data, risk_level):
    """
    Identificar los factores que contribuyen al riesgo
    """
    factors = []
    
    if task_data.get('complexity_level', '').lower() in ['high', 'alta']:
        factors.append('Alta complejidad técnica')
    
    if task_data.get('priority', '').lower() in ['high', 'alta', 'critical', 'crítica']:
        factors.append('Prioridad elevada')
    
    if task_data.get('dependencies', 0) > 2:
        factors.append(f"Múltiples dependencias ({task_data.get('dependencies')})")
    
    if task_data.get('assignees_count', 1) == 0:
        factors.append('Sin recursos asignados')
    
    if task_data.get('duration_est', 0) > 21:
        factors.append('Duración prolongada')
    
    return factors if factors else ['Sin factores de riesgo identificados']


def generate_recommendations(task_data, risk_level):
    """
    Generar recomendaciones basadas en el nivel de riesgo
    """
    recommendations = []
    
    if risk_level == 'alto':
        recommendations.append('Realizar seguimiento diario del progreso')
        recommendations.append('Asignar recursos adicionales si es posible')
        recommendations.append('Establecer puntos de control frecuentes')
        
        if task_data.get('assignees_count', 1) == 0:
            recommendations.append('URGENTE: Asignar personal a la tarea')
    
    elif risk_level == 'medio':
        recommendations.append('Seguimiento semanal recomendado')
        recommendations.append('Revisar dependencias críticas')
        
        if task_data.get('dependencies', 0) > 2:
            recommendations.append('Validar que las dependencias estén en progreso')
    
    else:  # bajo
        recommendations.append('Continuar con el flujo normal de trabajo')
        recommendations.append('Revisión quincenal suficiente')
    
    # Recomendación por complejidad
    if task_data.get('complexity_level', '').lower() in ['high', 'alta']:
        recommendations.append('Considerar dividir en subtareas más pequeñas')
    
    return recommendations
