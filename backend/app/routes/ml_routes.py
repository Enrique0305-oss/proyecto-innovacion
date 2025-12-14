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
    from app.ml.attrition_model import predict_attrition
except ImportError as e:
    # Los módulos ML se crearán después
    predict_risk = None
    predict_duration = None
    recommend_person = None
    predict_performance = None
    analyze_process = None
    predict_attrition = None

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


@ml_bp.route('/analisis-desempeno', methods=['POST'])
@jwt_required()
def hybrid_performance_analysis():
    """
    Análisis híbrido de desempeño del colaborador
    
    CAPA 1: Métricas SQL (rendimiento, tareas, calidad, tiempo)
    CAPA 2: Predicción CatBoost (at_risk, high_performer, resignation_risk)
    CAPA 3: Motor de reglas (recomendaciones accionables)
    
    Body JSON:
        - user_id: int (requerido)
    
    Returns:
        JSON con:
        - metrics: dict con métricas calculadas de SQL
        - prediction: dict con clase predicha y probabilidades
        - recommendations: list con acciones sugeridas según reglas
    """
    try:
        if predict_attrition is None:
            return jsonify({
                'error': 'Modelo de predicción de desempeño no disponible',
                'message': 'El modelo aún no ha sido cargado'
            }), 503
        
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id es requerido'}), 400
        
        # ============================================================
        # CAPA 1: MÉTRICAS SQL + AGREGACIÓN
        # ============================================================
        from app.models.web_user import WebUser
        from app.models.web_task import WebTask
        from app.extensions import db
        from sqlalchemy import func
        
        user = WebUser.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Calcular métricas agregadas desde WebTask
        task_stats = db.session.query(
            func.count(WebTask.id).label('total_tasks'),
            func.sum(
                db.case(
                    (WebTask.status == 'completada', 1),
                    else_=0
                )
            ).label('completed_tasks'),
            func.avg(WebTask.actual_hours).label('avg_hours')
        ).filter(
            WebTask.assigned_to == user_id
        ).first()
        
        total_tasks = int(task_stats.total_tasks or 0)
        completed_tasks = int(task_stats.completed_tasks or 0)
        avg_hours = float(task_stats.avg_hours or 0)
        
        # Calcular tasa de éxito
        success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calcular tiempo promedio en días (asumiendo 8h/día)
        avg_time = round(avg_hours / 8, 1) if avg_hours > 0 else 0
        
        metrics = {
            'rendimiento': round(float(user.performance_index or 75), 1),
            'tareas_completadas': completed_tasks,
            'tareas_totales': total_tasks,
            'calidad': round(success_rate, 1),
            'tiempo_promedio': avg_time,
            'carga_actual': round(float(user.current_load or 0), 0),
            'tasa_retrabajos': round(float(user.rework_rate or 0) * 100, 1)
        }
        
        # ============================================================
        # CAPA 2: PREDICCIÓN ML (CatBoost)
        # ============================================================
        # Para web_users usamos un modelo heurístico simplificado
        # basado en las métricas disponibles
        
        rendimiento = metrics['rendimiento']
        tasa_retrabajos = metrics['tasa_retrabajos']
        carga_actual = metrics['carga_actual']
        
        # Clasificación heurística basada en rendimiento y métricas
        # Calcular probabilidad de renuncia de forma gradual
        base_attrition = 0.10  # Base 10%
        
        # Factores que aumentan riesgo de renuncia
        if rendimiento < 60:
            base_attrition += 0.25
        elif rendimiento < 70:
            base_attrition += 0.15
        elif rendimiento < 75:
            base_attrition += 0.05
            
        if tasa_retrabajos > 25:
            base_attrition += 0.20
        elif tasa_retrabajos > 15:
            base_attrition += 0.10
        elif tasa_retrabajos > 10:
            base_attrition += 0.05
            
        if carga_actual > 90:
            base_attrition += 0.25
        elif carga_actual > 80:
            base_attrition += 0.15
        elif carga_actual > 70:
            base_attrition += 0.05
            
        # Factores que disminuyen riesgo de renuncia
        if rendimiento >= 85:
            base_attrition -= 0.05
        if tasa_retrabajos < 5:
            base_attrition -= 0.05
        if carga_actual < 50:
            base_attrition -= 0.05
            
        # Limitar entre 0.05 y 0.95
        attrition_prob = max(0.05, min(0.95, base_attrition))
        
        # Clasificar según el riesgo calculado
        if rendimiento >= 80 and attrition_prob < 0.20:
            performance_class = 'high_performer'
            prob_high = 0.70 + (rendimiento - 80) / 100
            prob_at_risk = 0.20
            prob_resignation = attrition_prob
        elif attrition_prob > 0.40:
            performance_class = 'resignation_risk'
            prob_high = 0.10
            prob_at_risk = 0.40
            prob_resignation = attrition_prob
        elif rendimiento < 65 or tasa_retrabajos > 20:
            performance_class = 'at_risk'
            prob_high = 0.15
            prob_at_risk = 0.60
            prob_resignation = attrition_prob
        else:
            # Rendimiento medio (65-80)
            performance_class = 'at_risk'
            prob_high = 0.30 + (rendimiento - 65) / 100
            prob_at_risk = 0.50
            prob_resignation = attrition_prob
        
        probabilities = {
            'high_performer': prob_high,
            'at_risk': prob_at_risk,
            'resignation_risk': prob_resignation
        }
        
        # Factores contribuyentes
        factors = []
        if rendimiento < 70:
            factors.append({
                'factor': 'Rendimiento bajo del colaborador',
                'value': f'{rendimiento}%',
                'impact': 'crítico' if rendimiento < 50 else 'alto'
            })
        if tasa_retrabajos > 15:
            factors.append({
                'factor': 'Alta tasa de retrabajos detectada',
                'value': f'{tasa_retrabajos}%',
                'impact': 'crítico' if tasa_retrabajos > 25 else 'alto'
            })
        if carga_actual > 80:
            factors.append({
                'factor': 'Sobrecarga de trabajo actual',
                'value': f'{carga_actual}%',
                'impact': 'crítico' if carga_actual > 95 else 'medio'
            })
        if total_tasks < 5:
            factors.append({
                'factor': 'Poca experiencia en tareas asignadas',
                'value': f'{total_tasks} tareas',
                'impact': 'medio'
            })
        if success_rate < 70:
            factors.append({
                'factor': 'Baja tasa de éxito en tareas',
                'value': f'{success_rate:.0f}%',
                'impact': 'alto'
            })
        
        if not factors:
            factors.append({
                'factor': 'Sin factores de riesgo detectados',
                'value': '✓',
                'impact': 'bajo'
            })
        
        prediction = {
            'clase': performance_class,
            'probabilidad_renuncia': round(attrition_prob * 100, 1),
            'probabilidades': {
                k: round(v * 100, 1) for k, v in probabilities.items()
            },
            'factores': factors[:5]  # Top 5
        }
        
        # ============================================================
        # CAPA 3: MOTOR DE REGLAS (Rule-Based System)
        # ============================================================
        recommendations = []
        
        rendimiento = metrics['rendimiento']
        prob_renuncia = attrition_prob * 100
        
        # REGLA 1: Alto impacto + Liderazgo
        if rendimiento >= 90 and prob_renuncia < 15:
            recommendations.append({
                'tipo': 'proyectos_alto_impacto',
                'titulo': 'Asignar a Proyectos de Alto Impacto',
                'descripcion': 'Alto desempeño y baja probabilidad de renuncia. Ideal para liderar proyectos críticos.',
                'prioridad': 'alta',
                'icono': '🚀'
            })
            recommendations.append({
                'tipo': 'liderazgo',
                'titulo': 'Considerar para Rol de Liderazgo',
                'descripcion': 'Excelente candidato para roles de mentoría o liderazgo de equipo.',
                'prioridad': 'media',
                'icono': '👨‍💼'
            })
        
        # REGLA 2: Retención crítica
        if prob_renuncia > 50 and rendimiento > 80:
            recommendations.append({
                'tipo': 'retencion_critica',
                'titulo': '⚠️ Retención Crítica - Talento en Riesgo',
                'descripcion': 'Alto desempeño pero alta probabilidad de renuncia. Requiere intervención inmediata.',
                'prioridad': 'crítica',
                'icono': '🚨'
            })
            recommendations.append({
                'tipo': 'entrevista_retencion',
                'titulo': 'Agendar Entrevista de Retención',
                'descripcion': 'Conversar sobre satisfacción laboral, crecimiento y expectativas.',
                'prioridad': 'alta',
                'icono': '💬'
            })
        
        # REGLA 3: Plan de mejora
        if rendimiento < 60:
            recommendations.append({
                'tipo': 'plan_mejora',
                'titulo': 'Implementar Plan de Mejora',
                'descripcion': f'Desempeño bajo ({rendimiento}%). Requiere capacitación y seguimiento.',
                'prioridad': 'alta',
                'icono': '📚'
            })
            recommendations.append({
                'tipo': 'capacitacion',
                'titulo': 'Asignar Capacitación',
                'descripcion': 'Identificar brechas de habilidades y ofrecer entrenamiento específico.',
                'prioridad': 'media',
                'icono': '🎓'
            })
        
        # REGLA 4: Reconocimiento
        if rendimiento > 95 and prob_renuncia < 5:
            recommendations.append({
                'tipo': 'reconocimiento',
                'titulo': '⭐ Reconocimiento Público',
                'descripcion': f'Desempeño excepcional ({rendimiento}%). Considerar bonos o reconocimientos.',
                'prioridad': 'media',
                'icono': '🏆'
            })
        
        # REGLA 5: Redistribución de carga
        if metrics['carga_actual'] > 90:
            recommendations.append({
                'tipo': 'redistribucion_carga',
                'titulo': 'Redistribuir Carga de Trabajo',
                'descripcion': f'Sobrecarga detectada ({metrics["carga_actual"]}%). Reasignar tareas para evitar burnout.',
                'prioridad': 'alta',
                'icono': '⚖️'
            })
        
        # REGLA 6: Monitoreo moderado
        if 60 <= rendimiento < 80 and 15 <= prob_renuncia < 40:
            recommendations.append({
                'tipo': 'monitoreo',
                'titulo': 'Monitoreo Regular',
                'descripcion': 'Desempeño moderado. Establecer seguimientos quincenales.',
                'prioridad': 'baja',
                'icono': '📊'
            })
        
        # REGLA 7: Buen desempeño - mantener motivación
        if 75 <= rendimiento < 90 and prob_renuncia < 15:
            recommendations.append({
                'tipo': 'mantener_motivacion',
                'titulo': 'Mantener Motivación',
                'descripcion': f'Buen desempeño ({rendimiento}%). Continuar seguimiento y ofrecer oportunidades de desarrollo.',
                'prioridad': 'media',
                'icono': '💪'
            })
            recommendations.append({
                'tipo': 'desarrollo',
                'titulo': 'Oportunidades de Crecimiento',
                'descripcion': 'Asignar proyectos desafiantes para mantener el interés y desarrollo profesional.',
                'prioridad': 'media',
                'icono': '📈'
            })
        
        # REGLA 8: Riesgo moderado de renuncia
        if 25 <= prob_renuncia < 50 and rendimiento >= 70:
            recommendations.append({
                'tipo': 'prevencion_renuncia',
                'titulo': 'Prevención de Renuncia',
                'descripcion': f'Riesgo moderado de salida ({prob_renuncia:.0f}%). Revisar satisfacción y plan de carrera.',
                'prioridad': 'media',
                'icono': '⚠️'
            })
        
        # REGLA 9: Alta tasa de retrabajos
        if metrics['tasa_retrabajos'] > 15:
            recommendations.append({
                'tipo': 'calidad',
                'titulo': 'Mejorar Calidad de Trabajo',
                'descripcion': f'Tasa de retrabajos elevada ({metrics["tasa_retrabajos"]}%). Revisar procesos y capacitar en QA.',
                'prioridad': 'alta',
                'icono': '🔍'
            })
        
        # REGLA 10: Pocas tareas completadas
        if total_tasks < 10 and user.created_at:
            from datetime import datetime
            days_since_join = (datetime.utcnow() - user.created_at).days
            if days_since_join > 30:
                recommendations.append({
                    'tipo': 'productividad',
                    'titulo': 'Aumentar Productividad',
                    'descripcion': f'Solo {total_tasks} tareas asignadas. Considerar aumentar carga gradualmente.',
                    'prioridad': 'baja',
                    'icono': '📋'
                })
        
        # REGLA 11: Desempeño estable y alto (sin problemas)
        if rendimiento >= 80 and prob_renuncia < 10 and metrics['tasa_retrabajos'] < 10 and metrics['carga_actual'] < 80:
            recommendations.append({
                'tipo': 'sin_acciones',
                'titulo': 'Desempeño Óptimo',
                'descripcion': 'El colaborador mantiene un excelente nivel. Continuar con seguimiento regular.',
                'prioridad': 'baja',
                'icono': '✅'
            })
        
        # ============================================================
        # OUTPUT: Dashboard
        # ============================================================
        return jsonify({
            'user_name': user.full_name,
            'metricas': metrics,
            'prediccion': prediction,
            'recomendaciones': recommendations
        }), 200
        
    except Exception as e:
        print(f"✗ Error en análisis de desempeño híbrido: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': 'Error en análisis de desempeño',
            'message': str(e)
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
