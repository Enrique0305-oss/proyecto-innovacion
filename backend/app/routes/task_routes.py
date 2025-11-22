"""
Rutas de Tareas
Endpoints para CRUD de tareas y gestión de asignaciones
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_, and_

from app.extensions import db
from app.models.task import Task, Assignee, TaskDependency
from app.models.person import Person

# Crear Blueprint
task_bp = Blueprint('tasks', __name__)


@task_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Obtener lista de tareas con filtros y paginación
    
    Query Params:
        - page: int (default: 1)
        - per_page: int (default: 20)
        - status: str (filtro por estado)
        - area: str (filtro por área)
        - priority: str (filtro por prioridad)
        - search: str (búsqueda por nombre)
    
    Returns:
        JSON con lista paginada de tareas
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Construir query
        query = Task.query
        
        # Filtros
        status = request.args.get('status')
        if status:
            query = query.filter(Task.status == status)
        
        area = request.args.get('area')
        if area:
            query = query.filter(Task.area == area)
        
        priority = request.args.get('priority')
        if priority:
            query = query.filter(Task.priority == priority)
        
        search = request.args.get('search')
        if search:
            query = query.filter(
                or_(
                    Task.task_name.ilike(f'%{search}%'),
                    Task.task_id.ilike(f'%{search}%')
                )
            )
        
        # Ejecutar paginación
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'tasks': [task.to_dict(include_assignees=True) for task in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener tareas',
            'details': str(e)
        }), 500


@task_bp.route('/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """
    Obtener una tarea específica por ID
    
    Path Params:
        task_id: ID de la tarea
    
    Returns:
        JSON con los detalles de la tarea
    """
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        return jsonify({
            'task': task.to_dict(include_assignees=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener tarea',
            'details': str(e)
        }), 500


@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """
    Crear una nueva tarea
    
    Body JSON:
        - task_id: str (requerido)
        - task_name: str (requerido)
        - project_id: str
        - area: str
        - task_type: str
        - start_date_est: str (YYYY-MM-DD)
        - end_date_est: str (YYYY-MM-DD)
        - status: str
        - priority: str
        - complexity_level: str
        - assignees: list[str] (person_ids)
    
    Returns:
        JSON con la tarea creada
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        task_id = data.get('task_id')
        task_name = data.get('task_name')
        
        if not all([task_id, task_name]):
            return jsonify({
                'error': 'Faltan campos requeridos',
                'required': ['task_id', 'task_name']
            }), 400
        
        # Verificar que no exista
        if Task.query.get(task_id):
            return jsonify({'error': 'La tarea ya existe'}), 409
        
        # Crear tarea
        new_task = Task(
            task_id=task_id,
            task_name=task_name,
            project_id=data.get('project_id'),
            area=data.get('area'),
            task_type=data.get('task_type'),
            status=data.get('status', 'Pending'),
            priority=data.get('priority'),
            complexity_level=data.get('complexity_level'),
            completion=data.get('completion', '0')
        )
        
        # Agregar fechas si vienen
        from datetime import datetime
        if data.get('start_date_est'):
            new_task.start_date_est = datetime.strptime(data['start_date_est'], '%Y-%m-%d')
        if data.get('end_date_est'):
            new_task.end_date_est = datetime.strptime(data['end_date_est'], '%Y-%m-%d')
        
        db.session.add(new_task)
        
        # Asignar personas si vienen
        assignees = data.get('assignees', [])
        for person_id in assignees:
            if Person.query.get(person_id):
                assignee = Assignee(task_id=task_id, person_id=person_id)
                db.session.add(assignee)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea creada exitosamente',
            'task': new_task.to_dict(include_assignees=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear tarea',
            'details': str(e)
        }), 500


@task_bp.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Actualizar una tarea existente
    
    Path Params:
        task_id: ID de la tarea
    
    Body JSON:
        Campos a actualizar (todos opcionales)
    
    Returns:
        JSON con la tarea actualizada
    """
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        updatable_fields = [
            'task_name', 'project_id', 'area', 'task_type', 'status',
            'priority', 'complexity_level', 'completion', 'tools_used',
            'dependencies', 'duration_est', 'duration_real'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(task, field, data[field])
        
        # Actualizar fechas
        from datetime import datetime
        if 'start_date_est' in data and data['start_date_est']:
            task.start_date_est = datetime.strptime(data['start_date_est'], '%Y-%m-%d')
        if 'end_date_est' in data and data['end_date_est']:
            task.end_date_est = datetime.strptime(data['end_date_est'], '%Y-%m-%d')
        if 'start_date_real' in data and data['start_date_real']:
            task.start_date_real = datetime.strptime(data['start_date_real'], '%Y-%m-%d')
        if 'end_date_real' in data and data['end_date_real']:
            task.end_date_real = datetime.strptime(data['end_date_real'], '%Y-%m-%d')
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea actualizada exitosamente',
            'task': task.to_dict(include_assignees=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al actualizar tarea',
            'details': str(e)
        }), 500


@task_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Eliminar una tarea
    
    Path Params:
        task_id: ID de la tarea
    
    Returns:
        JSON con mensaje de confirmación
    """
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al eliminar tarea',
            'details': str(e)
        }), 500


@task_bp.route('/<task_id>/assignees', methods=['POST'])
@jwt_required()
def assign_person(task_id):
    """
    Asignar una persona a una tarea
    
    Path Params:
        task_id: ID de la tarea
    
    Body JSON:
        - person_id: str (requerido)
    
    Returns:
        JSON con la asignación creada
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        data = request.get_json()
        person_id = data.get('person_id')
        
        if not person_id:
            return jsonify({'error': 'person_id es requerido'}), 400
        
        person = Person.query.get(person_id)
        if not person:
            return jsonify({'error': 'Persona no encontrada'}), 404
        
        # Verificar si ya está asignado
        existing = Assignee.query.filter_by(
            task_id=task_id,
            person_id=person_id
        ).first()
        
        if existing:
            return jsonify({'error': 'La persona ya está asignada a esta tarea'}), 409
        
        # Crear asignación
        assignee = Assignee(task_id=task_id, person_id=person_id)
        db.session.add(assignee)
        db.session.commit()
        
        return jsonify({
            'message': 'Persona asignada exitosamente',
            'assignee': assignee.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al asignar persona',
            'details': str(e)
        }), 500


@task_bp.route('/<task_id>/assignees/<person_id>', methods=['DELETE'])
@jwt_required()
def remove_assignee(task_id, person_id):
    """
    Remover una persona de una tarea
    
    Path Params:
        task_id: ID de la tarea
        person_id: ID de la persona
    
    Returns:
        JSON con mensaje de confirmación
    """
    try:
        assignee = Assignee.query.filter_by(
            task_id=task_id,
            person_id=person_id
        ).first()
        
        if not assignee:
            return jsonify({'error': 'Asignación no encontrada'}), 404
        
        db.session.delete(assignee)
        db.session.commit()
        
        return jsonify({
            'message': 'Asignación eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al eliminar asignación',
            'details': str(e)
        }), 500


@task_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Obtener estadísticas generales de tareas
    
    Returns:
        JSON con estadísticas
    """
    try:
        total = Task.query.count()
        completed = Task.query.filter(Task.status == 'Completed').count()
        in_progress = Task.query.filter(Task.status == 'In - Progress').count()
        pending = Task.query.filter(Task.status == 'Pending').count()
        
        # Contar por área
        areas = db.session.query(
            Task.area,
            db.func.count(Task.task_id)
        ).group_by(Task.area).all()
        
        return jsonify({
            'total_tasks': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 2),
            'tasks_by_area': [{'area': a[0], 'count': a[1]} for a in areas]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener estadísticas',
            'details': str(e)
        }), 500
