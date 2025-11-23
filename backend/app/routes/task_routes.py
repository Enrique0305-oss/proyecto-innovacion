"""
Rutas de Tareas Web
Endpoints para CRUD de web_tasks
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app.extensions import db
from app.models.web_task import WebTask
from app.models.web_user import WebUser

# Crear Blueprint
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/', methods=['GET'])
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
        - search: str (búsqueda por título)
    
    Returns:
        JSON con lista paginada de tareas
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Construir query
        query = WebTask.query
        
        # Filtros
        status = request.args.get('status')
        if status:
            query = query.filter(WebTask.status == status)
        
        area = request.args.get('area')
        if area:
            query = query.filter(WebTask.area == area)
        
        priority = request.args.get('priority')
        if priority:
            query = query.filter(WebTask.priority == priority)
        
        search = request.args.get('search')
        if search:
            query = query.filter(WebTask.title.ilike(f'%{search}%'))
        
        # Ordenar por fecha de creación descendente
        query = query.order_by(WebTask.created_at.desc())
        
        # Ejecutar paginación
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'tasks': [task.to_dict() for task in pagination.items],
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


@tasks_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_task(id):
    """
    Obtener una tarea específica por ID
    
    Path Params:
        id: ID de la tarea
    
    Returns:
        JSON con los detalles de la tarea
    """
    try:
        task = WebTask.query.get(id)
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        return jsonify({
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener tarea',
            'details': str(e)
        }), 500


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """
    Crear una nueva tarea
    
    Body JSON:
        - title: str (requerido)
        - description: str
        - priority: str (alta/media/baja)
        - area: str
        - complexity_score: int (1-10)
        - estimated_hours: float
        - deadline: str (ISO 8601)
        - assigned_to: str (person_id)
    
    Returns:
        JSON con la tarea creada
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        title = data.get('title')
        
        if not title:
            return jsonify({
                'error': 'Campo requerido faltante',
                'required': ['title']
            }), 400
        
        # Crear tarea
        new_task = WebTask(
            title=title,
            description=data.get('description'),
            priority=data.get('priority', 'media'),
            status='pendiente',
            area=data.get('area'),
            assigned_to=data.get('assigned_to'),
            complexity_score=data.get('complexity_score'),
            estimated_hours=data.get('estimated_hours'),
            created_by=user_id
        )
        
        # Deadline
        if data.get('deadline'):
            try:
                new_task.deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
            except:
                pass
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea creada exitosamente',
            'task': new_task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear tarea',
            'details': str(e)
        }), 500


@tasks_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    """
    Actualizar una tarea existente
    
    Path Params:
        id: ID de la tarea
    
    Body JSON:
        Campos a actualizar (todos opcionales)
    
    Returns:
        JSON con la tarea actualizada
    """
    try:
        task = WebTask.query.get(id)
        
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            task.priority = data['priority']
        if 'status' in data:
            task.status = data['status']
            # Si se completa, registrar fecha
            if data['status'] == 'completada' and not task.completed_at:
                task.completed_at = datetime.utcnow()
        if 'area' in data:
            task.area = data['area']
        if 'assigned_to' in data:
            task.assigned_to = data['assigned_to']
        if 'complexity_score' in data:
            task.complexity_score = data['complexity_score']
        if 'estimated_hours' in data:
            task.estimated_hours = data['estimated_hours']
        if 'actual_hours' in data:
            task.actual_hours = data['actual_hours']
        if 'deadline' in data and data['deadline']:
            try:
                task.deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
            except:
                pass
        if 'start_date' in data and data['start_date']:
            try:
                task.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            except:
                pass
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea actualizada exitosamente',
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al actualizar tarea',
            'details': str(e)
        }), 500


@tasks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    """
    Eliminar una tarea
    
    Path Params:
        id: ID de la tarea
    
    Returns:
        JSON con mensaje de confirmación
    """
    try:
        task = WebTask.query.get(id)
        
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


@tasks_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Obtener estadísticas generales de tareas
    
    Returns:
        JSON con estadísticas
    """
    try:
        total = WebTask.query.count()
        completed = WebTask.query.filter(WebTask.status == 'completada').count()
        in_progress = WebTask.query.filter(WebTask.status == 'en_progreso').count()
        pending = WebTask.query.filter(WebTask.status == 'pendiente').count()
        delayed = WebTask.query.filter(WebTask.status == 'retrasada').count()
        
        # Contar por área
        areas = db.session.query(
            WebTask.area,
            db.func.count(WebTask.id)
        ).group_by(WebTask.area).all()
        
        # Contar por prioridad
        priorities = db.session.query(
            WebTask.priority,
            db.func.count(WebTask.id)
        ).group_by(WebTask.priority).all()
        
        return jsonify({
            'total_tasks': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'delayed': delayed,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 2),
            'tasks_by_area': [{'area': a[0] or 'Sin área', 'count': a[1]} for a in areas],
            'tasks_by_priority': [{'priority': p[0], 'count': p[1]} for p in priorities]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener estadísticas',
            'details': str(e)
        }), 500
