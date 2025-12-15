from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.training_schedule import TrainingSchedule
from app.models.web_user import WebUser
from datetime import datetime
import json

training_schedule_bp = Blueprint('training_schedules', __name__)

@training_schedule_bp.route('/training-schedules', methods=['GET'])
@jwt_required()
def get_training_schedules():
    """Obtener todas las programaciones de reentrenamiento"""
    try:
        schedules = TrainingSchedule.query.order_by(TrainingSchedule.scheduled_date.desc()).all()
        return jsonify([schedule.to_dict() for schedule in schedules]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_schedule_bp.route('/training-schedules/<int:schedule_id>', methods=['GET'])
@jwt_required()
def get_training_schedule(schedule_id):
    """Obtener una programación específica"""
    try:
        schedule = TrainingSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'error': 'Programación no encontrada'}), 404
        return jsonify(schedule.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@training_schedule_bp.route('/training-schedules', methods=['POST'])
@jwt_required()
def create_training_schedule():
    """Crear una nueva programación de reentrenamiento"""
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        
        # Validar datos requeridos
        if not data.get('model_type') or not data.get('scheduled_date') or not data.get('scheduled_time'):
            return jsonify({'error': 'Faltan datos requeridos'}), 400
        
        # Crear nueva programación
        schedule = TrainingSchedule(
            model_type=data['model_type'],
            scheduled_date=datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date(),
            scheduled_time=data['scheduled_time'],
            status=data.get('status', 'programado'),
            parameters=json.dumps(data.get('parameters', {})) if data.get('parameters') else None,
            created_by=current_user_id,
            is_recurring=data.get('is_recurring', False),
            recurrence_pattern=data.get('recurrence_pattern')
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        return jsonify({
            'message': 'Programación creada exitosamente',
            'schedule': schedule.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@training_schedule_bp.route('/training-schedules/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update_training_schedule(schedule_id):
    """Actualizar una programación de reentrenamiento"""
    try:
        schedule = TrainingSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'error': 'Programación no encontrada'}), 404
        
        data = request.json
        
        # Actualizar campos
        if 'model_type' in data:
            schedule.model_type = data['model_type']
        if 'scheduled_date' in data:
            schedule.scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date()
        if 'scheduled_time' in data:
            schedule.scheduled_time = data['scheduled_time']
        if 'status' in data:
            schedule.status = data['status']
        if 'parameters' in data:
            schedule.parameters = json.dumps(data['parameters'])
        if 'is_recurring' in data:
            schedule.is_recurring = data['is_recurring']
        if 'recurrence_pattern' in data:
            schedule.recurrence_pattern = data['recurrence_pattern']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Programación actualizada exitosamente',
            'schedule': schedule.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@training_schedule_bp.route('/training-schedules/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_training_schedule(schedule_id):
    """Eliminar una programación de reentrenamiento"""
    try:
        schedule = TrainingSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'error': 'Programación no encontrada'}), 404
        
        db.session.delete(schedule)
        db.session.commit()
        
        return jsonify({'message': 'Programación eliminada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@training_schedule_bp.route('/training-schedules/<int:schedule_id>/execute', methods=['POST'])
@jwt_required()
def execute_training(schedule_id):
    """Ejecutar manualmente un reentrenamiento programado"""
    try:
        schedule = TrainingSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({'error': 'Programación no encontrada'}), 404
        
        # Actualizar estado
        schedule.status = 'ejecutando'
        schedule.last_execution = datetime.utcnow()
        db.session.commit()
        
        # Aquí se ejecutaría el reentrenamiento del modelo
        # Por ahora, simulamos el proceso
        try:
            # Importar el entrenador correspondiente según el tipo de modelo
            result = f"Reentrenamiento de modelo {schedule.model_type} completado exitosamente"
            schedule.status = 'completado'
            schedule.execution_result = result
        except Exception as train_error:
            schedule.status = 'fallido'
            schedule.execution_result = str(train_error)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Ejecución completada',
            'schedule': schedule.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@training_schedule_bp.route('/training-schedules/model-types', methods=['GET'])
@jwt_required()
def get_model_types():
    """Obtener lista de tipos de modelos disponibles"""
    model_types = [
        {'value': 'attrition', 'label': 'Modelo de Deserción'},
        {'value': 'duration', 'label': 'Modelo de Duración de Tareas'},
        {'value': 'performance', 'label': 'Modelo de Rendimiento'},
        {'value': 'risk', 'label': 'Modelo de Riesgo de Proyectos'}
    ]
    return jsonify(model_types), 200
