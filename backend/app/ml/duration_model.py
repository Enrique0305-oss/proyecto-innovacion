"""
Modelo de Predicción de Duración
Predice la duración real de una tarea en horas
"""
import os
import json
import joblib
import numpy as np
import pandas as pd
from flask import current_app


_model = None
_config = None
_metrics = None


def load_model():
    """
    Cargar el modelo de predicción de duración
    """
    global _model, _config, _metrics
    
    if _model is not None:
        return _model
    
    try:
        # Ruta al modelo NUMERIC_ONLY (sin dependencias categóricas)
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(base_path, 'ml', 'models', 'duration')
        
        model_file = os.path.join(model_path, 'model_catboost_rmse_numeric.pkl')
        config_file = os.path.join(model_path, 'columns_regression_numeric.json')
        
        # Cargar modelo CatBoost (guardado con joblib)
        if os.path.exists(model_file):
            _model = joblib.load(model_file)
            print(f"✓ Modelo CatBoost Duration cargado: {model_file}")
        else:
            print(f"⚠ Modelo no encontrado: {model_file}")
            return None
        
        # Cargar configuración de columnas
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                _config = json.load(f)
            print(f"✓ Configuración cargada: {config_file}")
            print(f"   Features: {len(_config.get('numeric', [])) + len(_config.get('categorical', []))}")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo de duración: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def predict_duration(task_data):
    """
    Predecir la duración real de una tarea usando modelo NUMERIC_ONLY
    
    MODELO: CatBoost entrenado solo con features numéricas (sin categorías de dominio)
    
    MODO DUAL:
    - Si task_data incluye 'person_id' → Predicción personalizada
    - Si NO incluye 'person_id' → Predicción genérica (promedios)
    
    Args:
        task_data (dict): Datos de la tarea
            - complexity_level: str ('Baja', 'Media', 'Alta')
            - duration_est_days: float (estimación inicial en días)
            - assignees_count: int (opcional)
            - dependencies: int (opcional)
            - person_id: int (OPCIONAL - para modo personalizado)
    
    Returns:
        dict: Predicción de duración
            - duration_days: float (días)
            - confidence_interval: dict {min, max, mean}
            - factors: list[str]
            - mode: str ('personalized' o 'generic')
    """
    model = load_model()
    
    if model is None:
        return predict_duration_heuristic(task_data)
    
    try:
        # Detectar modo (personalizado vs genérico)
        person_id = task_data.get('person_id')
        mode = 'personalized' if person_id else 'generic'
        
        features = prepare_features(task_data, person_id)
        
        # Predicción: el modelo predice log1p(duration_days), debemos revertir
        predicted_log = model.predict(features)[0]
        predicted_days_raw = np.expm1(predicted_log)  # Revertir transformación log1p
        
        # CALIBRACIÓN: El modelo fue entrenado con datos rurales (~834 días promedio)
        # Factor de calibración para dominio IT: 0.12 (ajusta escala ~120 días → ~14 días)
        CALIBRATION_FACTOR = 0.12
        predicted_days_calibrated = predicted_days_raw * CALIBRATION_FACTOR
        
        # ESTRATEGIA HÍBRIDA: Combinar CatBoost calibrado + heurística
        # - Si predicción calibrada < 5 días → usar heurística (modelo subestima)
        # - Si predicción calibrada > 50 días → usar heurística (modelo sobreestima)
        # - Si predicción calibrada 5-50 días → usar calibrada (rango confiable)
        
        if predicted_days_calibrated < 5.0:
            print(f"     CatBoost calibrado: {predicted_days_calibrated:.1f}d (< 5d) → usando heurística")
            return predict_duration_heuristic(task_data)
        elif predicted_days_calibrated > 50.0:
            print(f"     CatBoost calibrado: {predicted_days_calibrated:.1f}d (> 50d) → usando heurística")
            return predict_duration_heuristic(task_data)
        
        # Usar predicción calibrada (rango confiable 5-50 días)
        predicted_days = predicted_days_calibrated
        print(f"   ✓  CatBoost: {predicted_days_raw:.1f}d → calibrado: {predicted_days:.1f}d (factor {CALIBRATION_FACTOR})")
        
        # Intervalo de confianza (±20%)
        min_days = max(1, predicted_days * 0.8)
        max_days = predicted_days * 1.2
        confidence_interval = {
            'min': round(min_days, 1),
            'max': round(max_days, 1),
            'mean': round(predicted_days, 1)
        }
        
        # Factores que afectan la duración
        factors = identify_duration_factors(task_data, person_id)
        
        return {
            'duration_days': round(predicted_days, 1),
            'confidence_interval': confidence_interval,
            'factors': factors,
            'mode': mode
        }
        
    except Exception as e:
        print(f"Error en predicción de duración: {str(e)}")
        import traceback
        traceback.print_exc()
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


def prepare_features(task_data, person_id=None):
    """
    Preparar features para el modelo NUMERIC_ONLY según columns_regression_numeric.json
    
    Features del modelo (SOLO NUMÉRICAS):
    1. duration_est_imputed         (días) -  MÁS IMPORTANTE (correlación ~0.9)
    2. experience_years_imputed     (años)
    3. availability_hours_week_imputed (horas/semana)
    4. current_load_imputed         (número de tareas)
    5. performance_index_imputed    (0-1, normalizado)
    6. rework_rate_imputed          (0-1)
    7. load_ratio                   (carga/capacidad)
    8. complexity_numeric           (1=Baja, 2=Media, 3=Alta)
    
    MODO DUAL:
    - Si person_id es None → usa promedios (modo genérico)
    - Si person_id existe → usa datos reales de la persona (modo personalizado)
    """
    global _config
    
    # complexity_numeric: Convertir texto a escala numérica 1-3
    complexity_map = {'Baja': 1.0, 'baja': 1.0, 'LOW': 1.0, 'Low': 1.0,
                      'Media': 2.0, 'media': 2.0, 'MEDIUM': 2.0, 'Medium': 2.0,
                      'Alta': 3.0, 'alta': 3.0, 'HIGH': 3.0, 'High': 3.0}
    complexity_input = task_data.get('complexity_level', 'Media')
    complexity_numeric = float(complexity_map.get(complexity_input, 2.0))
    
    # duration_est_imputed: LA FEATURE MÁS IMPORTANTE (correlación ~0.9 con target)
    # El modelo espera DÍAS (no minutos, ya convertido en entrenamiento)
    duration_est_days = float(task_data.get('duration_est_days', 10))
    duration_est_imputed = duration_est_days  # Ya en días
    
    # Features de persona (personalizado vs genérico)
    # IMPORTANTE: Estas features NUMÉRICAS son las que harán la diferencia real
    
    if person_id:
        # MODO PERSONALIZADO: Usar datos reales de la persona
        from app.models.web_user import WebUser
        person = WebUser.query.get(person_id)
        
        if person:
            # Features numéricas personalizadas
            experience_years_imputed = float(person.experience_years or 2.0)
            availability_hours_week_imputed = float(person.availability_hours_week or 40.0)
            current_load_imputed = float(person.current_load or 0.0)
            # Normalizar performance_index a escala 0-1 (modelo espera 0-1, no 0-100)
            performance_index_imputed = float(person.performance_index or 0.5) / 100.0 if person.performance_index and person.performance_index > 1 else float(person.performance_index or 0.5)
            rework_rate_imputed = float(person.rework_rate or 0.1)
        else:
            # Fallback a promedios
            experience_years_imputed = 2.0
            availability_hours_week_imputed = 40.0
            current_load_imputed = 0.0
            performance_index_imputed = 0.5  # 50% normalizado
            rework_rate_imputed = 0.1
    else:
        # MODO GENÉRICO: Promedios del dominio IT
        experience_years_imputed = 2.0
        availability_hours_week_imputed = 40.0
        current_load_imputed = 0.0
        performance_index_imputed = 0.5  # 50% normalizado a 0-1
        rework_rate_imputed = 0.1
    
    # Feature derivada: load_ratio (carga actual / capacidad máxima)
    max_capacity = 10.0  # Capacidad típica de tareas simultáneas
    load_ratio = current_load_imputed / max_capacity if max_capacity > 0 else 0.0
    
    # Crear diccionario con las 8 features numéricas
    feature_dict = {
        'duration_est_imputed': float(duration_est_imputed),
        'experience_years_imputed': float(experience_years_imputed),
        'availability_hours_week_imputed': float(availability_hours_week_imputed),
        'current_load_imputed': float(current_load_imputed),
        'performance_index_imputed': float(performance_index_imputed),
        'rework_rate_imputed': float(rework_rate_imputed),
        'load_ratio': float(load_ratio),
        'complexity_numeric': float(complexity_numeric)
    }
    
    # Crear DataFrame con el orden exacto del entrenamiento
    # Orden según columns_regression_numeric.json
    feature_order = [
        'duration_est_imputed',
        'experience_years_imputed',
        'availability_hours_week_imputed',
        'current_load_imputed',
        'performance_index_imputed',
        'rework_rate_imputed',
        'load_ratio',
        'complexity_numeric'
    ]
    
    df = pd.DataFrame([feature_dict], columns=feature_order)
    
    return df


def identify_duration_factors(task_data, person_id=None):
    """
    Identificar factores que afectan la duración
    """
    factors = []
    
    # Factores de la tarea
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
    
    # Factores de la persona (si está en modo personalizado)
    if person_id:
        from app.models.web_user import WebUser
        person = WebUser.query.get(person_id)
        
        if person:
            # Performance
            if person.performance_index and person.performance_index >= 80:
                factors.append(f'{person.full_name} tiene alto desempeño ({person.performance_index:.0f}%)')
            elif person.performance_index and person.performance_index < 60:
                factors.append(f'Desempeño por debajo del promedio puede aumentar duración')
            
            # Experiencia
            if person.experience_years and person.experience_years >= 5:
                factors.append(f'{person.experience_years} años de experiencia aceleran ejecución')
            elif person.experience_years and person.experience_years < 2:
                factors.append('Poca experiencia puede requerir más tiempo')
            
            # Carga de trabajo
            if person.current_load and person.current_load > 3:
                factors.append(f'Alta carga actual ({person.current_load} tareas) puede retrasar inicio')
            elif person.current_load == 0:
                factors.append('Sin carga actual: puede iniciar inmediatamente')
    
    return factors if factors else ['Factores estándar de duración']
