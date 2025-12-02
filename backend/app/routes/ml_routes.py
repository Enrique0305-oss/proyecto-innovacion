"""
Rutas de Machine Learning
Endpoints para predicciones usando modelos ML entrenados
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import traceback

# Imports de los módulos ML (se crearán después)
try:
    from app.ml.risk_model import predict_risk
    from app.ml.duration_model import predict_duration
    from app.ml.recommender_model import recommend_person
    from app.ml.performance_model import predict_performance
    from app.ml.process_mining import analyze_process
except ImportError as e:
    # Los módulos ML se crearán después
    predict_risk = None
    predict_duration = None
    recommend_person = None
    predict_performance = None
    analyze_process = None

# Crear Blueprint
ml_bp = Blueprint('ml', __name__)


@ml_bp.route('/prediccion-riesgo', methods=['POST'])
@jwt_required()
def prediction_risk():
    """
    Predecir el riesgo de una tarea
    
    Body JSON:
        - task_id: str (opcional, para referencia)
        - complexity_level: str
        - priority: str
        - area: str
        - task_type: str
        - duration_est: int (días estimados)
        - assignees_count: int (número de personas asignadas)
        - dependencies: int (número de dependencias)
    
    Returns:
        JSON con predicción de riesgo (bajo/medio/alto) y probabilidad
    """
    try:
        if predict_risk is None:
            return jsonify({
                'error': 'Modelo de predicción de riesgo no disponible',
                'message': 'El módulo ML aún no está configurado'
            }), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        # Validar campos requeridos
        required_fields = ['complexity_level', 'priority', 'area', 'task_type']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            return jsonify({
                'error': 'Faltan campos requeridos',
                'missing_fields': missing
            }), 400
        
        # Llamar al modelo de predicción
        result = predict_risk(data)
        
        print(f"📊 Resultado del modelo:")
        print(f"   risk_level: {result.get('risk_level')}")
        print(f"   probability: {result.get('probability')}")
        print(f"   probabilities: {result.get('probabilities')}")
        print(f"   factors: {result.get('factors')}")
        
        return jsonify({
            'task_id': data.get('task_id'),
            'risk_level': result['risk_level'],
            'risk_probability': result['probability'],
            'probabilities': result.get('probabilities', {}),
            'risk_factors': result.get('factors', []),
            'recommendations': result.get('recommendations', [])
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al predecir riesgo',
            'details': str(e),
            'trace': traceback.format_exc()
        }), 500


@ml_bp.route('/tiempo-real', methods=['POST'])
@jwt_required()
def prediction_duration():
    """
    Predecir la duración real de una tarea
    
    Body JSON:
        - task_id: str (opcional)
        - complexity_level: str
        - task_type: str
        - area: str
        - assignees_count: int
        - tools_used: str (separados por coma)
        - dependencies: int
    
    Returns:
        JSON con duración estimada en días
    """
    try:
        if predict_duration is None:
            return jsonify({
                'error': 'Modelo de predicción de duración no disponible',
                'message': 'El módulo ML aún no está configurado'
            }), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        required_fields = ['complexity_level', 'task_type', 'area']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            return jsonify({
                'error': 'Faltan campos requeridos',
                'missing_fields': missing
            }), 400
        
        # Llamar al modelo
        result = predict_duration(data)
        
        return jsonify({
            'task_id': data.get('task_id'),
            'predicted_duration_days': result['duration'],
            'confidence_interval': result.get('confidence_interval'),
            'factors': result.get('factors', [])
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al predecir duración',
            'details': str(e),
            'trace': traceback.format_exc()
        }), 500


@ml_bp.route('/recomendar-persona', methods=['POST'])
@jwt_required()
def recommendation_person():
    """
    Recomendar la mejor persona para una tarea
    
    Body JSON:
        - task_id: str (opcional)
        - area: str (requerido)
        - task_type: str
        - complexity_level: str
        - skills_required: list[str] (habilidades requeridas)
        - exclude_person_ids: list[str] (personas a excluir)
        - top_n: int (default: 5, número de recomendaciones)
    
    Returns:
        JSON con lista de personas recomendadas ordenadas por score
    """
    try:
        if recommend_person is None:
            return jsonify({
                'error': 'Modelo de recomendación no disponible',
                'message': 'El módulo ML aún no está configurado'
            }), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if 'area' not in data:
            return jsonify({
                'error': 'Campo requerido faltante',
                'missing_fields': ['area']
            }), 400
        
        # Llamar al modelo
        result = recommend_person(data)
        
        return jsonify({
            'task_id': data.get('task_id'),
            'recommendations': result['recommendations'],
            'total_candidates': result.get('total_candidates', 0),
            'criteria_used': result.get('criteria', [])
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al recomendar persona',
            'details': str(e),
            'trace': traceback.format_exc()
        }), 500


@ml_bp.route('/desempeno', methods=['POST'])
@jwt_required()
def prediction_performance():
    """
    Predecir el desempeño de una persona en una tarea
    
    Body JSON:
        - person_id: str (requerido)
        - task_id: str (opcional)
        - task_type: str
        - complexity_level: str
        - area: str
    
    Returns:
        JSON con predicción de desempeño (score 0-100)
    """
    try:
        if predict_performance is None:
            return jsonify({
                'error': 'Modelo de predicción de desempeño no disponible',
                'message': 'El módulo ML aún no está configurado'
            }), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        if 'person_id' not in data:
            return jsonify({
                'error': 'Campo requerido faltante',
                'missing_fields': ['person_id']
            }), 400
        
        # Llamar al modelo
        result = predict_performance(data)
        
        return jsonify({
            'person_id': data['person_id'],
            'task_id': data.get('task_id'),
            'performance_score': result['score'],
            'performance_level': result['level'],
            'strengths': result.get('strengths', []),
            'weaknesses': result.get('weaknesses', []),
            'confidence': result.get('confidence', 0)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al predecir desempeño',
            'details': str(e),
            'trace': traceback.format_exc()
        }), 500


@ml_bp.route('/proceso', methods=['POST'])
@jwt_required()
def analysis_process():
    """
    Análisis de minería de procesos
    
    Body JSON:
        - area: str (opcional, filtro por área)
        - start_date: str (YYYY-MM-DD, opcional)
        - end_date: str (YYYY-MM-DD, opcional)
        - task_type: str (opcional)
        - analysis_type: str (frequency/duration/bottleneck)
    
    Returns:
        JSON con análisis de procesos (cuellos de botella, flujos, tiempos)
    """
    try:
        if analyze_process is None:
            return jsonify({
                'error': 'Módulo de minería de procesos no disponible',
                'message': 'El módulo ML aún no está configurado'
            }), 503
        
        data = request.get_json()
        
        if not data:
            data = {}
        
        # Llamar al módulo de process mining
        result = analyze_process(data)
        
        return jsonify({
            'analysis_type': data.get('analysis_type', 'general'),
            'process_flow': result.get('flow', []),
            'bottlenecks': result.get('bottlenecks', []),
            'average_duration': result.get('avg_duration'),
            'task_sequences': result.get('sequences', []),
            'insights': result.get('insights', [])
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al analizar proceso',
            'details': str(e),
            'trace': traceback.format_exc()
        }), 500


@ml_bp.route('/health', methods=['GET'])
def ml_health():
    """
    Verificar estado de los modelos ML
    
    Returns:
        JSON con estado de cada modelo
    """
    models_status = {
        'risk_model': predict_risk is not None,
        'duration_model': predict_duration is not None,
        'recommender_model': recommend_person is not None,
        'performance_model': predict_performance is not None,
        'process_mining': analyze_process is not None
    }
    
    all_ready = all(models_status.values())
    
    return jsonify({
        'status': 'ready' if all_ready else 'partial',
        'models': models_status,
        'message': 'Todos los modelos disponibles' if all_ready else 'Algunos modelos no están disponibles'
    }), 200 if all_ready else 503
