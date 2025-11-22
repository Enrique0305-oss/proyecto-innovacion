"""
Modelo de Predicción de Duración
Predice la duración real de una tarea
"""
import os
import joblib
import numpy as np
from flask import current_app


_model = None
_scaler = None


def load_model():
    """
    Cargar el modelo de predicción de duración
    """
    global _model, _scaler
    
    if _model is not None:
        return _model
    
    try:
        # Cargar desde la misma carpeta app/ml/
        ml_path = os.path.dirname(os.path.abspath(__file__))
        model_file = os.path.join(ml_path, 'duration_model.pkl')
        scaler_file = os.path.join(ml_path, 'duration_scaler.pkl')
        
        if os.path.exists(model_file):
            _model = joblib.load(model_file)
            print(f"✓ Modelo de duración cargado: {model_file}")
        
        if os.path.exists(scaler_file):
            _scaler = joblib.load(scaler_file)
            print(f"✓ Scaler de duración cargado: {scaler_file}")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo de duración: {str(e)}")
        return None


def predict_duration(task_data):
    """
    Predecir la duración real de una tarea
    
    Args:
        task_data (dict): Datos de la tarea
            - complexity_level: str
            - task_type: str
            - area: str
            - assignees_count: int
            - tools_used: str
            - dependencies: int
    
    Returns:
        dict: Predicción de duración
            - duration: float (días)
            - confidence_interval: dict
            - factors: list[str]
    """
    model = load_model()
    
    if model is None:
        return predict_duration_heuristic(task_data)
    
    try:
        features = prepare_features(task_data)
        
        # Predicción
        predicted_days = model.predict([features])[0]
        
        # Intervalo de confianza (estimación básica ±20%)
        confidence_interval = {
            'min': max(1, predicted_days * 0.8),
            'max': predicted_days * 1.2,
            'mean': predicted_days
        }
        
        # Factores que afectan la duración
        factors = identify_duration_factors(task_data)
        
        return {
            'duration': round(predicted_days, 1),
            'confidence_interval': confidence_interval,
            'factors': factors
        }
        
    except Exception as e:
        print(f"Error en predicción de duración: {str(e)}")
        return predict_duration_heuristic(task_data)


def predict_duration_heuristic(task_data):
    """
    Predicción heurística de duración
    """
    base_duration = 5  # días base
    
    factors = []
    
    # Factor: Complejidad
    complexity = task_data.get('complexity_level', '').lower()
    if 'high' in complexity or 'alta' in complexity:
        base_duration *= 3
        factors.append('Complejidad alta: x3 tiempo')
    elif 'medium' in complexity or 'media' in complexity:
        base_duration *= 2
        factors.append('Complejidad media: x2 tiempo')
    else:
        base_duration *= 1
        factors.append('Complejidad baja: tiempo estándar')
    
    # Factor: Tipo de tarea
    task_type = task_data.get('task_type', '').lower()
    if 'development' in task_type or 'desarrollo' in task_type:
        base_duration *= 1.5
        factors.append('Desarrollo: +50% tiempo')
    elif 'research' in task_type or 'investigación' in task_type:
        base_duration *= 1.3
        factors.append('Investigación: +30% tiempo')
    
    # Factor: Dependencias
    dependencies = task_data.get('dependencies', 0)
    if dependencies > 3:
        base_duration += dependencies * 1
        factors.append(f'Dependencias ({dependencies}): +{dependencies} días')
    
    # Factor: Asignados
    assignees = task_data.get('assignees_count', 1)
    if assignees > 1:
        # Más personas pueden reducir tiempo pero con overhead
        reduction_factor = 1 / (assignees * 0.7)
        base_duration *= reduction_factor
        factors.append(f'Equipo de {assignees}: reducción parcial')
    
    # Factor: Herramientas
    tools = task_data.get('tools_used', '')
    if tools and len(tools.split(',')) > 3:
        base_duration *= 1.1
        factors.append('Múltiples herramientas: +10% complejidad')
    
    predicted_days = max(1, base_duration)
    
    return {
        'duration': round(predicted_days, 1),
        'confidence_interval': {
            'min': round(predicted_days * 0.7, 1),
            'max': round(predicted_days * 1.3, 1),
            'mean': round(predicted_days, 1)
        },
        'factors': factors
    }


def prepare_features(task_data):
    """
    Preparar features para el modelo
    """
    features = []
    
    # Complejidad (codificada)
    complexity_map = {'low': 1, 'baja': 1, 'medium': 2, 'media': 2, 'high': 3, 'alta': 3}
    complexity = task_data.get('complexity_level', 'medium').lower()
    features.append(complexity_map.get(complexity, 2))
    
    # Tipo de tarea (hash simple)
    task_type_hash = hash(task_data.get('task_type', 'general')) % 10
    features.append(task_type_hash)
    
    # Área (hash)
    area_hash = hash(task_data.get('area', 'general')) % 10
    features.append(area_hash)
    
    # Numéricos
    features.append(task_data.get('assignees_count', 1))
    features.append(task_data.get('dependencies', 0))
    
    # Número de herramientas
    tools = task_data.get('tools_used', '')
    tools_count = len(tools.split(',')) if tools else 0
    features.append(tools_count)
    
    return np.array(features)


def identify_duration_factors(task_data):
    """
    Identificar factores que afectan la duración
    """
    factors = []
    
    complexity = task_data.get('complexity_level', '').lower()
    if 'high' in complexity or 'alta' in complexity:
        factors.append('Alta complejidad incrementa tiempo significativamente')
    
    if task_data.get('dependencies', 0) > 2:
        factors.append('Dependencias múltiples pueden causar esperas')
    
    assignees = task_data.get('assignees_count', 1)
    if assignees > 3:
        factors.append('Equipo grande: coordinación puede añadir overhead')
    elif assignees == 1:
        factors.append('Trabajo individual: sin overhead de coordinación')
    
    return factors if factors else ['Factores estándar de duración']
