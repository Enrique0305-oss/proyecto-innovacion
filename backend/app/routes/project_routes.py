"""
Rutas de API para gestión de proyectos
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.project import Project
from app.models.task_dependency import WebTaskDependency
from app.models.web_task import WebTask
from app.models.web_user import WebUser
from app.utils.permissions import (
    get_current_user, 
    apply_area_filter,
    can_access_resource,
    require_permission
)
from sqlalchemy import func

project_bp = Blueprint('projects', __name__)


@project_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    """Obtiene todos los proyectos con estadísticas (filtrado por área si aplica)"""
    try:
        # Obtener usuario actual
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
        include_stats = request.args.get('include_stats', 'false').lower() == 'true'
        include_tasks = request.args.get('include_tasks', 'false').lower() == 'true'
        status_filter = request.args.get('status')
        
        query = Project.query
        
        # Aplicar filtro por área según permisos del usuario
        query = apply_area_filter(query, Project, user)
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        projects = query.all()
        
        return jsonify({
            'status': 'success',
            'projects': [p.to_dict(include_tasks=include_tasks, include_stats=include_stats) for p in projects],
            'count': len(projects),
            'user_area': user.area,
            'user_role': user.role_id
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/projects/<project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """Obtiene un proyecto específico con todas sus relaciones"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 401
            
        include_stats = request.args.get('include_stats', 'true').lower() == 'true'
        include_tasks = request.args.get('include_tasks', 'true').lower() == 'true'
        
        project = Project.query.get_or_404(project_id)
        
        # Verificar si el usuario puede acceder a este proyecto
        if not can_access_resource(user, project):
            return jsonify({
                'error': 'No tienes permiso para ver este proyecto',
                'project_area': project.area,
                'user_area': user.area
            }), 403
        
        return jsonify({
            'status': 'success',
            'project': project.to_dict(include_tasks=include_tasks, include_stats=include_stats)
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404


@project_bp.route('/projects', methods=['POST'])
def create_project():
    """Crea un nuevo proyecto"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('project_id') or not data.get('name'):
            return jsonify({'status': 'error', 'message': 'project_id y name son requeridos'}), 400
        
        # Verificar que no exista
        if Project.query.get(data['project_id']):
            return jsonify({'status': 'error', 'message': 'El project_id ya existe'}), 400
        
        project = Project(
            project_id=data['project_id'],
            name=data['name'],
            description=data.get('description'),
            start_date=data.get('start_date'),
            expected_end_date=data.get('expected_end_date'),
            status=data.get('status', 'planning'),
            priority=data.get('priority', 'medium'),
            budget=data.get('budget'),
            manager_id=data.get('manager_id')
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Proyecto creado exitosamente',
            'project': project.to_dict(include_stats=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Actualiza un proyecto existente"""
    try:
        project = Project.query.get_or_404(project_id)
        data = request.get_json()
        
        # Actualizar campos permitidos
        allowed_fields = ['name', 'description', 'start_date', 'expected_end_date', 
                          'actual_end_date', 'status', 'priority', 'budget', 
                          'progress_percentage', 'manager_id']
        
        for field in allowed_fields:
            if field in data:
                setattr(project, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Proyecto actualizado',
            'project': project.to_dict(include_stats=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Elimina un proyecto (en cascada sus dependencias)"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Las tareas quedan con project_id NULL (SET NULL)
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Proyecto eliminado'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/projects/<project_id>/graph', methods=['GET'])
def get_project_graph(project_id):
    """Obtiene el grafo de tareas del proyecto para GNN"""
    try:
        project = Project.query.get_or_404(project_id)
        graph = project.get_task_graph()
        
        return jsonify({
            'status': 'success',
            'project_id': project_id,
            'graph': graph
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/projects/<project_id>/critical-path', methods=['GET'])
def get_critical_path(project_id):
    """
    Calcula el camino crítico del proyecto
    TODO: Implementar algoritmo CPM (Critical Path Method)
    """
    try:
        project = Project.query.get_or_404(project_id)
        
        # Placeholder: retornar tareas con más dependencias
        tasks = WebTask.query.filter_by(project_id=project_id).all()
        dependencies = WebTaskDependency.query.filter_by(project_id=project_id).all()
        
        # Contar dependencias por tarea
        task_deps = {}
        for task in tasks:
            pred_count = len([d for d in dependencies if d.successor_task_id == task.id])
            succ_count = len([d for d in dependencies if d.predecessor_task_id == task.id])
            task_deps[task.id] = {
                'task': task.to_dict(),
                'predecessor_count': pred_count,
                'successor_count': succ_count,
                'total_connections': pred_count + succ_count
            }
        
        # Ordenar por total de conexiones
        critical_tasks = sorted(task_deps.values(), key=lambda x: x['total_connections'], reverse=True)
        
        return jsonify({
            'status': 'success',
            'project_id': project_id,
            'critical_path_candidates': critical_tasks[:10]  # Top 10
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================
# RUTAS DE DEPENDENCIAS
# ============================================

@project_bp.route('/projects/<project_id>/dependencies', methods=['GET'])
def get_dependencies(project_id):
    """Obtiene todas las dependencias de un proyecto"""
    try:
        dependencies = WebTaskDependency.query.filter_by(project_id=project_id).all()
        
        return jsonify({
            'status': 'success',
            'project_id': project_id,
            'dependencies': [d.to_dict() for d in dependencies],
            'count': len(dependencies)
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/dependencies', methods=['POST'])
def create_dependency():
    """Crea una nueva dependencia entre tareas"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['project_id', 'predecessor_task_id', 'successor_task_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'{field} es requerido'}), 400
        
        # Validar que las tareas existan
        pred_task = WebTask.query.get(data['predecessor_task_id'])
        succ_task = WebTask.query.get(data['successor_task_id'])
        
        if not pred_task or not succ_task:
            return jsonify({'status': 'error', 'message': 'Tarea no encontrada'}), 404
        
        # Verificar que no haya ciclos (simplificado)
        if data['predecessor_task_id'] == data['successor_task_id']:
            return jsonify({'status': 'error', 'message': 'Una tarea no puede depender de sí misma'}), 400
        
        # Verificar que no exista ya
        existing = WebTaskDependency.query.filter_by(
            predecessor_task_id=data['predecessor_task_id'],
            successor_task_id=data['successor_task_id']
        ).first()
        
        if existing:
            return jsonify({'status': 'error', 'message': 'La dependencia ya existe'}), 400
        
        dependency = WebTaskDependency(
            project_id=data['project_id'],
            predecessor_task_id=data['predecessor_task_id'],
            successor_task_id=data['successor_task_id'],
            dependency_type=data.get('dependency_type', 'finish_to_start'),
            lag_days=data.get('lag_days', 0)
        )
        
        db.session.add(dependency)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Dependencia creada',
            'dependency': dependency.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/dependencies/<int:dependency_id>', methods=['DELETE'])
def delete_dependency(dependency_id):
    """Elimina una dependencia"""
    try:
        dependency = WebTaskDependency.query.get_or_404(dependency_id)
        
        db.session.delete(dependency)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Dependencia eliminada'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@project_bp.route('/dependencies/<int:dependency_id>/status', methods=['GET'])
def get_dependency_status(dependency_id):
    """Obtiene el estado de una dependencia (bloqueante o no)"""
    try:
        dependency = WebTaskDependency.query.get_or_404(dependency_id)
        
        return jsonify({
            'status': 'success',
            'dependency': dependency.to_dict(),
            'is_blocking': dependency.is_blocking(),
            'edge_status': dependency.get_edge_status()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
