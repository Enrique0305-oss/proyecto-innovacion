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
    Predecir la duración real de una tarea usando modelo CatBoost numeric_only
    
    Body JSON:
        - complexity_level: str (requerido) - 'Baja', 'Media', 'Alta'
        - duration_est_days: float (requerido) - Estimación inicial en días
        - person_id: int (opcional) - Para predicción personalizada
    
    Returns:
        JSON con duración estimada en días, intervalo de confianza y factores
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
        
        # Campos requeridos para modelo numeric_only
        required_fields = ['complexity_level', 'duration_est_days']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            return jsonify({
                'error': 'Faltan campos requeridos',
                'missing_fields': missing,
                'required': required_fields
            }), 400
        
        # Llamar al modelo
        result = predict_duration(data)
        
        return jsonify({
            'predicted_duration_days': result.get('duration_days', result.get('duration', 0)),
            'confidence_interval': result.get('confidence_interval'),
            'factors': result.get('factors', []),
            'mode': result.get('mode', 'generico')
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


@ml_bp.route('/asignacion-inteligente', methods=['POST'])
@jwt_required()
def intelligent_assignment():
    """
    Asignación inteligente de tareas (COMBINA 3 MODELOS)
    
    Ejecuta en paralelo:
    1. Clasificación de Riesgo → Nivel de riesgo de la tarea
    2. Recomendación de Personas → Top 5 candidatos ideales
    3. Predicción de Duración → Duración personalizada por cada candidato
    
    Body JSON:
        - complexity_level: str (requerido) - 'Baja', 'Media', 'Alta'
        - duration_est_days: float (requerido) - Estimación inicial en días
        - area: str (opcional) - Para filtrar recomendaciones
        - top_n: int (default: 5) - Número de candidatos
    
    Returns:
        JSON con análisis completo:
        - risk: {level, probability, factors}
        - recommendations: [{person_id, name, score, predicted_duration, observations}]
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        # Validar campos requeridos
        required_fields = ['complexity_level', 'duration_est_days']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            return jsonify({
                'error': 'Faltan campos requeridos',
                'missing_fields': missing,
                'required': required_fields
            }), 400
        
        # 1. CLASIFICACIÓN DE RIESGO
        risk_result = {'level': 'MEDIO', 'probability': 50, 'factors': []}
        if predict_risk:
            try:
                risk_result = predict_risk(data)
            except Exception as e:
                print(f"⚠️ Error en clasificación de riesgo: {e}")
        
        # 2. RECOMENDACIÓN DE PERSONAS
        recommendations = []
        if recommend_person:
            try:
                rec_data = {
                    'area': data.get('area', 'General'),
                    'complexity_level': data['complexity_level'],
                    'task_type': data.get('task_type', 'desarrollo'),
                    'top_n': data.get('top_n', 5)
                }
                rec_result = recommend_person(rec_data)
                recommended_persons = rec_result.get('recommendations', [])
                
                # FALLBACK: Si no hay recomendaciones, obtener usuarios de la BD
                if not recommended_persons:
                    print("⚠️ No hay recomendaciones del modelo, obteniendo usuarios de BD...")
                    from app.models.web_user import WebUser
                    from app import db
                    
                    # Obtener usuarios activos con rol colaborador (role_id=7), filtrar por área si se especificó
                    query = WebUser.query.filter_by(status='active', role_id=7)
                    if data.get('area'):
                        query = query.filter(WebUser.area == data.get('area'))
                    
                    users = query.order_by(WebUser.full_name).limit(data.get('top_n', 5)).all()
                    
                    # Convertir a formato de recomendaciones
                    recommended_persons = []
                    for user in users:
                        recommended_persons.append({
                            'person_id': user.id,
                            'person_name': user.full_name or user.email,
                            'score': 80.0,  # Score genérico
                            'experience_years': user.experience_years or 2,
                            'current_load': user.current_load or 3,
                            'performance_index': user.performance_index or 50,
                            'area': user.area
                        })
                    print(f"✓ Obtenidos {len(recommended_persons)} usuarios de BD")
                
                # 3. PREDICCIÓN DE DURACIÓN para cada persona recomendada
                for person in recommended_persons:
                    person_id = person.get('person_id')
                    
                    # Predicción personalizada de duración
                    duration_days = None
                    if predict_duration and person_id:
                        try:
                            duration_data = {
                                'complexity_level': data['complexity_level'],
                                'duration_est_days': data['duration_est_days'],
                                'person_id': person_id
                            }
                            duration_result = predict_duration(duration_data)
                            duration_days = duration_result.get('duration_days')
                        except Exception as e:
                            print(f"⚠️ Error en predicción de duración para {person_id}: {e}")
                    
                    # Generar observaciones
                    observations = []
                    if person.get('score', 0) >= 90:
                        observations.append('✅ Candidato ideal')
                    if person.get('current_load', 0) > 5:
                        observations.append('⚠️ Carga alta')
                    if person.get('experience_years', 0) < 2:
                        observations.append('⚠️ Experiencia baja')
                    
                    recommendations.append({
                        'person_id': person.get('person_id'),
                        'person_name': person.get('name') or person.get('person_name', 'Sin nombre'),
                        'score': round(person.get('score', 0), 1),
                        'predicted_duration_days': round(duration_days, 1) if duration_days else None,
                        'experience_years': person.get('experience_years', 0),
                        'current_load': person.get('current_load') or person.get('current_workload', 0),
                        'performance_index': person.get('performance_index', 50),
                        'observations': observations
                    })
            except Exception as e:
                print(f"⚠️ Error en recomendación de personas: {e}")
                traceback.print_exc()
        
        # Convertir nivel de riesgo del modelo al formato del frontend
        risk_level_raw = risk_result.get('risk_level', 'MEDIO')
        probabilities = risk_result.get('probabilities', {})
        
        # Convertir BAJO_RIESGO → BAJO, ALTO_RIESGO → ALTO
        if risk_level_raw == 'BAJO_RIESGO':
            risk_level = 'BAJO'
            # Para bajo riesgo, la probabilidad es la de BAJO_RIESGO
            risk_probability = probabilities.get('BAJO_RIESGO', 0) * 100
        elif risk_level_raw == 'ALTO_RIESGO':
            risk_level = 'ALTO'
            # Para alto riesgo, la probabilidad es la de ALTO_RIESGO
            risk_probability = probabilities.get('ALTO_RIESGO', 0) * 100
        else:
            risk_level = 'MEDIO'
            risk_probability = 50
        
        return jsonify({
            'risk': {
                'level': risk_level,
                'probability': round(risk_probability, 0),
                'factors': risk_result.get('factors', [])
            },
            'recommendations': recommendations,
            'total_candidates': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error en asignación inteligente',
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
