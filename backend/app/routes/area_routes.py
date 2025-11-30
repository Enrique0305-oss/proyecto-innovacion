"""
Rutas de Áreas
Endpoints para CRUD de áreas/departamentos
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.area import Area
from app.models.web_user import WebUser

# Crear Blueprint
areas_bp = Blueprint('areas', __name__)


@areas_bp.route('/', methods=['GET'])
def get_areas():
    """
    Obtener lista de áreas
    
    Query Params:
        - status: str (filtro por estado: active/inactive)
    
    Returns:
        JSON con lista de áreas
    """
    try:
        query = Area.query
        
        # Filtro por status
        status = request.args.get('status')
        if status:
            query = query.filter(Area.status == status)
        
        # Ordenar por nombre
        query = query.order_by(Area.name)
        
        areas = query.all()
        
        # Enriquecer con datos calculados
        areas_data = []
        for area in areas:
            area_dict = area.to_dict()
            
            # Calcular número real de empleados (usuarios) en esta área
            employee_count = WebUser.query.filter_by(area=area.name, status='active').count()
            area_dict['employee_count'] = employee_count
            
            # Calcular número de tareas de esta área
            from app.models.web_task import WebTask
            task_count = WebTask.query.filter_by(area=area.name).count()
            area_dict['task_count'] = task_count
            
            # Agregar nombre del supervisor (si existe)
            if area.supervisor_person_id:
                from app.models.person import Person
                supervisor = Person.query.filter_by(person_id=area.supervisor_person_id).first()
                area_dict['supervisor_name'] = supervisor.role if supervisor else 'Sin supervisor'
            else:
                area_dict['supervisor_name'] = 'Sin supervisor'
            
            areas_data.append(area_dict)
        
        return jsonify({
            'areas': areas_data,
            'total': len(areas_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener áreas',
            'details': str(e)
        }), 500


@areas_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_area(id):
    """
    Obtener un área específica por ID
    
    Path Params:
        id: ID del área
    
    Returns:
        JSON con los detalles del área
    """
    try:
        area = Area.query.get(id)
        
        if not area:
            return jsonify({'error': 'Área no encontrada'}), 404
        
        return jsonify({
            'area': area.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener área',
            'details': str(e)
        }), 500


@areas_bp.route('/', methods=['POST'])
@jwt_required()
def create_area():
    """
    Crear una nueva área
    Solo super_admin puede crear áreas
    
    Body JSON:
        - name: str (requerido, único)
        - description: str
        - supervisor_person_id: str
        - employee_count: int
        - efficiency_score: float (0-100)
    
    Returns:
        JSON con el área creada
    """
    try:
        # Obtener usuario actual
        current_user_email = get_jwt_identity()
        current_user = WebUser.query.filter_by(email=current_user_email).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        # Solo super_admin puede crear áreas
        user_role = current_user.role.name if current_user.role else 'colaborador'
        if user_role != 'super_admin':
            return jsonify({
                'error': 'Permiso denegado',
                'message': 'Solo el Administrador TI puede gestionar áreas'
            }), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        name = data.get('name')
        
        if not name:
            return jsonify({
                'error': 'Campo requerido faltante',
                'required': ['name']
            }), 400
        
        # Verificar que no exista
        if Area.query.filter_by(name=name).first():
            return jsonify({'error': 'Ya existe un área con ese nombre'}), 409
        
        # Crear área
        new_area = Area(
            name=name,
            description=data.get('description'),
            supervisor_person_id=data.get('supervisor_person_id'),
            employee_count=data.get('employee_count', 0),
            efficiency_score=data.get('efficiency_score'),
            status='active'
        )
        
        db.session.add(new_area)
        db.session.commit()
        
        return jsonify({
            'message': 'Área creada exitosamente',
            'area': new_area.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear área',
            'details': str(e)
        }), 500


@areas_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_area(id):
    """
    Actualizar un área existente
    Solo super_admin puede actualizar áreas
    
    Path Params:
        id: ID del área
    
    Body JSON:
        Campos a actualizar (todos opcionales)
    
    Returns:
        JSON con el área actualizada
    """
    try:
        # Obtener usuario actual
        current_user_email = get_jwt_identity()
        current_user = WebUser.query.filter_by(email=current_user_email).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        # Solo super_admin puede actualizar áreas
        user_role = current_user.role.name if current_user.role else 'colaborador'
        if user_role != 'super_admin':
            return jsonify({
                'error': 'Permiso denegado',
                'message': 'Solo el Administrador TI puede gestionar áreas'
            }), 403
        
        area = Area.query.get(id)
        
        if not area:
            return jsonify({'error': 'Área no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'name' in data:
            # Verificar que no exista otro con ese nombre
            existing = Area.query.filter_by(name=data['name']).first()
            if existing and existing.id != id:
                return jsonify({'error': 'Ya existe un área con ese nombre'}), 409
            area.name = data['name']
        
        if 'description' in data:
            area.description = data['description']
        if 'supervisor_person_id' in data:
            area.supervisor_person_id = data['supervisor_person_id']
        if 'employee_count' in data:
            area.employee_count = data['employee_count']
        if 'efficiency_score' in data:
            area.efficiency_score = data['efficiency_score']
        if 'status' in data:
            area.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Área actualizada exitosamente',
            'area': area.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al actualizar área',
            'details': str(e)
        }), 500


@areas_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_area(id):
    """
    Eliminar un área
    Solo super_admin puede eliminar áreas
    
    Path Params:
        id: ID del área
    
    Returns:
        JSON con mensaje de confirmación
    """
    try:
        # Obtener usuario actual
        current_user_email = get_jwt_identity()
        current_user = WebUser.query.filter_by(email=current_user_email).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        # Solo super_admin puede eliminar áreas
        user_role = current_user.role.name if current_user.role else 'colaborador'
        if user_role != 'super_admin':
            return jsonify({
                'error': 'Permiso denegado',
                'message': 'Solo el Administrador TI puede gestionar áreas'
            }), 403
        
        area = Area.query.get(id)
        
        if not area:
            return jsonify({'error': 'Área no encontrada'}), 404
        
        db.session.delete(area)
        db.session.commit()
        
        return jsonify({
            'message': 'Área eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al eliminar área',
            'details': str(e)
        }), 500
