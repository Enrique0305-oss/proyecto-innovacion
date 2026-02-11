"""
Modelo de Predicción de Riesgo Binario - CatBoost
Predice si una tarea tiene BAJO o ALTO riesgo de retraso
"""
import os
import json
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier


# Variables globales para modelo y configuración
_model = None
_config = None
_metrics = None


def load_model():
    """
    Cargar el modelo CatBoost binario (.cbm) y sus configuraciones
    """
    global _model, _config, _metrics
    
    if _model is not None:
        return _model
    
    try:
        # Ruta al modelo
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(base_path, 'ml', 'models', 'risk')
        
        model_file = os.path.join(model_path, 'model_binary_task_risk.cbm')
        config_file = os.path.join(model_path, 'columns_binary.json')
        metrics_file = os.path.join(model_path, 'metrics_binary.json')
        
        # Cargar modelo CatBoost
        if os.path.exists(model_file):
            _model = CatBoostClassifier()
            _model.load_model(model_file)
            print(f" Modelo CatBoost binario cargado: {model_file}")
        else:
            print(f" Modelo no encontrado: {model_file}")
            return None
        
        # Cargar configuración de columnas
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                _config = json.load(f)
            print(f"✓ Configuración cargada: {config_file}")
            print(f"   Features: {_config.get('n_features', len(_config.get('all_columns', [])))} (4 cat + {len(_config.get('numeric', []))} num)")
        
        # Cargar métricas
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r', encoding='utf-8') as f:
                _metrics = json.load(f)
            print(f"✓ Métricas cargadas")
            print(f"   Accuracy: {_metrics.get('accuracy', 0):.4f}")
            print(f"   ROC-AUC: {_metrics.get('roc_auc', 0):.4f}")
            print(f"   Recall ALTO_RIESGO: {_metrics.get('classification_report', {}).get('ALTO_RIESGO', {}).get('recall', 0):.4f}")
        
        return _model
        
    except Exception as e:
        print(f"✗ Error al cargar modelo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def prepare_features(task_data):
    """
    Preparar todas las features que el modelo espera (25 features totales)
    
    Args:
        task_data: dict con los datos del formulario
            - area: str
            - task_type: str
            - complexity_level: str
            - priority: str
            - duration_est: int (días)
            - assignees_count: int
            - dependencies: int
    
    Returns:
        pandas.DataFrame con 1 fila y 25 columnas en el orden correcto
    """
    global _config
    
    print(f"\n Preparando features desde: {task_data}")
    
    # Features base del formulario
    area = str(task_data.get('area', 'TI'))
    task_type = str(task_data.get('task_type', 'Desarrollo'))
    complexity_level = str(task_data.get('complexity_level', 'Media'))
    priority = str(task_data.get('priority', 'Media'))
    duration_est = float(task_data.get('duration_est', 10))
    assignees_count = float(task_data.get('assignees_count', 1))
    dependencies = float(task_data.get('dependencies', 0))
    
    # Mapeos numéricos
    complexity_map = {'Baja': 1, 'Media': 2, 'Alta': 3, 'baja': 1, 'media': 2, 'alta': 3}
    priority_map = {'Baja': 1, 'Media': 2, 'Alta': 3, 'Crítica': 4, 
                    'baja': 1, 'media': 2, 'alta': 3, 'crítica': 4}
    
    complexity_numeric = float(complexity_map.get(complexity_level, 2))
    priority_numeric = float(priority_map.get(priority, 2))
    
    # Features derivadas básicas
    workload_per_person = duration_est / max(assignees_count, 1)
    dependency_ratio = dependencies / max(duration_est, 1)
    complexity_priority = complexity_numeric * priority_numeric
    duration_est_squared = duration_est ** 2
    duration_est_log = np.log1p(duration_est)  # log(1 + x) para evitar log(0)
    
    # Features booleanas (0/1)
    has_dependencies = 1.0 if dependencies > 0 else 0.0
    is_single_person = 1.0 if assignees_count == 1 else 0.0
    is_high_complexity = 1.0 if complexity_numeric >= 3 else 0.0
    is_critical_priority = 1.0 if priority_numeric >= 4 else 0.0
    
    # Features de contexto (promedios históricos - valores por defecto)
    # Estos se calcularían de la BD en producción real
    area_defaults = {
        'TI': (15.2, 8.3, 12.1),  # (avg_delay, std_delay, median_delay)
        'Marketing': (8.5, 5.2, 7.0),
        'Operaciones': (12.0, 6.8, 10.5),
        'RRHH': (6.3, 3.9, 5.5),
        'Ventas': (9.8, 5.5, 8.2)
    }
    
    type_defaults = {
        'Desarrollo': (18.5, 9.2),  # (avg_delay, std_delay)
        'Diseño': (10.2, 5.8),
        'Testing': (7.5, 4.1),
        'Análisis': (8.9, 5.0),
        'Documentación': (5.2, 2.8),
        'Soporte': (6.8, 3.5)
    }
    
    complexity_defaults = {
        'Baja': (5.5, 3.2),
        'Media': (10.8, 5.9),
        'Alta': (20.3, 10.5),
        'baja': (5.5, 3.2),
        'media': (10.8, 5.9),
        'alta': (20.3, 10.5)
    }
    
    area_stats = area_defaults.get(area, (10.0, 6.0, 8.5))
    type_stats = type_defaults.get(task_type, (10.0, 6.0))
    complexity_stats = complexity_defaults.get(complexity_level, (10.0, 6.0))
    
    area_avg_delay = float(area_stats[0])
    area_std_delay = float(area_stats[1])
    area_median_delay = float(area_stats[2])
    type_avg_delay = float(type_stats[0])
    type_std_delay = float(type_stats[1])
    complexity_avg_delay = float(complexity_stats[0])
    complexity_std_delay = float(complexity_stats[1])
    
    # Crear diccionario con TODAS las features en el orden correcto
    feature_dict = {
        # Categóricas (4)
        'area': area,
        'task_type': task_type,
        'complexity_level': complexity_level,
        'priority': priority,
        
        # Numéricas (21)
        'duration_est_days': duration_est,
        'assignees_count': assignees_count,
        'dependencies': dependencies,
        'complexity_numeric': complexity_numeric,
        'priority_numeric': priority_numeric,
        'workload_per_person': workload_per_person,
        'dependency_ratio': dependency_ratio,
        'complexity_priority': complexity_priority,
        'duration_est_squared': duration_est_squared,
        'duration_est_log': duration_est_log,
        'has_dependencies': has_dependencies,
        'is_single_person': is_single_person,
        'is_high_complexity': is_high_complexity,
        'is_critical_priority': is_critical_priority,
        'area_avg_delay': area_avg_delay,
        'area_std_delay': area_std_delay,
        'area_median_delay': area_median_delay,
        'type_avg_delay': type_avg_delay,
        'type_std_delay': type_std_delay,
        'complexity_avg_delay': complexity_avg_delay,
        'complexity_std_delay': complexity_std_delay
    }
    
    # Crear DataFrame con las columnas en el orden correcto
    df = pd.DataFrame([feature_dict])
    
    # Asegurar orden correcto según config
    if _config and 'all_columns' in _config:
        df = df[_config['all_columns']]
    
    print(f"✓ Features preparados: {df.shape}")
    print(f"  - Categóricas: {area}, {task_type}, {complexity_level}, {priority}")
    print(f"  - Numéricas clave: duration={duration_est}, assignees={assignees_count}, deps={dependencies}")
    print(f"  - Derivadas: workload={workload_per_person:.1f}, complexity_priority={complexity_priority:.1f}")
    
    return df


def predict_risk(task_data):
    """
    Predecir el riesgo de una tarea (BAJO o ALTO)
    
    Returns:
        dict con:
            - risk_level: 'BAJO_RIESGO' o 'ALTO_RIESGO'
            - probability: float (probabilidad de ALTO_RIESGO)
            - probabilities: dict con probabilidades de ambas clases
            - factors: list de factores de riesgo identificados
            - recommendations: list de recomendaciones
    """
    model = load_model()
    
    if model is None:
        print("⚠ Modelo no disponible, usando heurística")
        return predict_risk_heuristic(task_data)
    
    try:
        # Preparar features
        features_df = prepare_features(task_data)
        
        # Hacer predicción
        prediction = model.predict(features_df)[0]  # 0 o 1
        probabilities = model.predict_proba(features_df)[0]  # [prob_bajo, prob_alto]
        
        # Mapear a nombres de clases
        classes = ['BAJO_RIESGO', 'ALTO_RIESGO']
        model_prediction = classes[int(prediction)]
        model_prob_alto = float(probabilities[1])
        
        # Crear diccionario de probabilidades del modelo
        model_prob_dict = {
            'BAJO_RIESGO': float(probabilities[0]),
            'ALTO_RIESGO': float(probabilities[1])
        }
        
        print(f" Predicción del modelo: {model_prediction} (prob: {model_prob_alto:.2%})")
        
        # Aplicar reglas de negocio para ajustar si es necesario
        business_result = apply_business_rules(
            task_data, 
            model_prediction, 
            model_prob_alto,
            model_prob_dict
        )
        
        risk_level = business_result['risk_level']
        probability = business_result['probability']
        prob_dict = business_result['probabilities']
        factors = business_result['factors']
        
        if business_result.get('adjusted'):
            print(f"⚠ Ajustado por reglas de negocio: {risk_level} (prob: {probability:.2%})")
        
        # Generar recomendaciones
        recommendations = generate_recommendations(task_data, risk_level, probability)
        
        return {
            'risk_level': risk_level,
            'probability': probability,
            'probabilities': prob_dict,
            'factors': factors,
            'recommendations': recommendations,
            'model_used': 'catboost_binary' + (' + business_rules' if business_result.get('adjusted') else '')
        }
        
    except Exception as e:
        print(f"✗ Error en predicción: {str(e)}")
        import traceback
        traceback.print_exc()
        return predict_risk_heuristic(task_data)


def identify_risk_factors(task_data, risk_level, probability):
    """
    Identificar factores de riesgo basados en la predicción
    """
    factors = []
    
    complexity = task_data.get('complexity_level', '').lower()
    priority = task_data.get('priority', '').lower()
    duration = task_data.get('duration_est', 0)
    assignees = task_data.get('assignees_count', 1)
    dependencies = task_data.get('dependencies', 0)
    
    if risk_level == 'ALTO_RIESGO':
        if 'alta' in complexity or 'high' in complexity:
            factors.append('Alta complejidad técnica')
        
        if 'crítica' in priority or 'critical' in priority or 'alta' in priority:
            factors.append('Prioridad elevada/crítica')
        
        if duration > 30:
            factors.append(f'Duración prolongada ({duration} días)')
        
        if assignees == 1:
            factors.append('Recurso único asignado (punto único de falla)')
        
        if dependencies > 2:
            factors.append(f'Múltiples dependencias ({dependencies})')
        
        if assignees == 0:
            factors.append('Sin recursos asignados')
    
    return factors if factors else ['Riesgo general identificado por el modelo']


def generate_recommendations(task_data, risk_level, probability):
    """
    Generar recomendaciones según el nivel de riesgo
    """
    recommendations = []
    duration = task_data.get('duration_est', 10)
    
    if risk_level == 'ALTO_RIESGO':
        if probability > 0.8:
            recommendations.append(' CRÍTICO: Revisar factibilidad antes de iniciar')
        
        # Frecuencia de seguimiento basada en duración
        if duration <= 7:
            recommendations.append('Realizar seguimiento diario del progreso')
        elif duration <= 14:
            recommendations.append('Realizar seguimiento cada 2-3 días del progreso')
        else:
            recommendations.append('Realizar seguimiento semanal del progreso')
        
        recommendations.append('Considerar asignar recursos adicionales')
        recommendations.append('Establecer puntos de control tempranos')
        
        if task_data.get('assignees_count', 1) <= 1:
            recommendations.append('Asignar un segundo recurso como respaldo')
        
        if task_data.get('dependencies', 0) > 2:
            recommendations.append('Validar disponibilidad de dependencias antes de iniciar')
    
    else:  # BAJO_RIESGO
        recommendations.append('✓ Continuar con el flujo normal de trabajo')
        
        # Frecuencia de seguimiento basada en duración
        if duration <= 7:
            recommendations.append('Seguimiento cada 2-3 días es suficiente')
        elif duration <= 14:
            recommendations.append('Seguimiento semanal es suficiente')
        else:
            recommendations.append('Seguimiento quincenal es suficiente')
    
    return recommendations


def apply_business_rules(task_data, model_prediction, model_probability, model_probabilities):
    """
    Aplicar reglas de negocio sobre la predicción del modelo
    Ajustar predicción si hay factores críticos evidentes
    """
    risk_score = 0
    factors = []
    
    complexity = task_data.get('complexity_level', '').lower()
    if 'alta' in complexity or 'high' in complexity:
        risk_score += 3
        factors.append('Alta complejidad técnica')
    elif 'media' in complexity or 'medium' in complexity:
        risk_score += 1
    
    priority = task_data.get('priority', '').lower()
    if 'crítica' in priority or 'critical' in priority:
        risk_score += 3
        factors.append('Prioridad crítica')
    elif 'alta' in priority or 'high' in priority:
        risk_score += 2
        factors.append('Prioridad alta')
    
    duration = task_data.get('duration_est', 0)
    if duration > 30:
        risk_score += 2
        factors.append(f'Duración prolongada ({duration} días)')
    elif duration > 20:
        risk_score += 1
    
    dependencies = task_data.get('dependencies', 0)
    if dependencies > 3:
        risk_score += 2
        factors.append(f'Múltiples dependencias ({dependencies})')
    elif dependencies > 1:
        risk_score += 1
    
    assignees = task_data.get('assignees_count', 1)
    if assignees == 0:
        risk_score += 3
        factors.append('Sin recursos asignados')
    elif assignees == 1:
        risk_score += 1
        factors.append('Recurso único asignado (punto único de falla)')
    
    # Si hay muchos factores de riesgo, sobrescribir predicción del modelo
    if risk_score >= 7:
        # Alto riesgo claro por reglas de negocio
        adjusted_prob = min(0.95, 0.5 + (risk_score * 0.08))
        return {
            'risk_level': 'ALTO_RIESGO',
            'probability': adjusted_prob,
            'probabilities': {
                'BAJO_RIESGO': 1 - adjusted_prob,
                'ALTO_RIESGO': adjusted_prob
            },
            'factors': factors,
            'adjusted': True
        }
    elif risk_score >= 4 and model_prediction == 'BAJO_RIESGO':
        # Riesgo moderado pero modelo dice bajo - ajustar hacia arriba
        adjusted_prob = min(0.75, model_probability + 0.3)
        if adjusted_prob > 0.5:
            return {
                'risk_level': 'ALTO_RIESGO',
                'probability': adjusted_prob,
                'probabilities': {
                    'BAJO_RIESGO': 1 - adjusted_prob,
                    'ALTO_RIESGO': adjusted_prob
                },
                'factors': factors,
                'adjusted': True
            }
    
    # Usar predicción del modelo
    return {
        'risk_level': model_prediction,
        'probability': model_probability,
        'probabilities': model_probabilities,
        'factors': factors if factors else ['Sin factores críticos evidentes'],
        'adjusted': False
    }


def predict_risk_heuristic(task_data):
    """
    Predicción heurística de respaldo (si el modelo no está disponible)
    """
    risk_score = 0
    factors = []
    
    complexity = task_data.get('complexity_level', '').lower()
    if 'alta' in complexity or 'high' in complexity:
        risk_score += 3
        factors.append('Alta complejidad')
    elif 'media' in complexity or 'medium' in complexity:
        risk_score += 2
    
    priority = task_data.get('priority', '').lower()
    if 'crítica' in priority or 'critical' in priority:
        risk_score += 3
        factors.append('Prioridad crítica')
    elif 'alta' in priority or 'high' in priority:
        risk_score += 2
        factors.append('Prioridad alta')
    
    duration = task_data.get('duration_est', 0)
    if duration > 30:
        risk_score += 2
        factors.append('Duración prolongada')
    
    dependencies = task_data.get('dependencies', 0)
    if dependencies > 2:
        risk_score += 2
        factors.append('Múltiples dependencias')
    
    assignees = task_data.get('assignees_count', 1)
    if assignees == 0:
        risk_score += 3
        factors.append('Sin recursos')
    
    # Determinar riesgo
    if risk_score >= 6:
        risk_level = 'ALTO_RIESGO'
        probability = min(0.9, 0.5 + (risk_score * 0.06))
    else:
        risk_level = 'BAJO_RIESGO'
        probability = max(0.15, risk_score * 0.08)
    
    recommendations = generate_recommendations(task_data, risk_level, probability)
    
    return {
        'risk_level': risk_level,
        'probability': probability if risk_level == 'ALTO_RIESGO' else probability,
        'probabilities': {
            'BAJO_RIESGO': 1 - probability if risk_level == 'ALTO_RIESGO' else 1 - probability,
            'ALTO_RIESGO': probability if risk_level == 'ALTO_RIESGO' else probability
        },
        'factors': factors if factors else ['Sin factores críticos'],
        'recommendations': recommendations,
        'model_used': 'heuristic_fallback'
    }
