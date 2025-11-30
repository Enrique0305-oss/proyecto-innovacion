"""
Rutas de Usuarios Web
Endpoints para gestión de usuarios del sistema web
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt

from app.extensions import db
from app.models.web_user import WebUser
from app.models.role import Role

# Crear Blueprint
users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['GET'])
def get_users():
    """
    Obtener lista de usuarios
    
    Query Params:
        - status: str (filtro por estado)
        - role_id: int (filtro por rol)
        - area: str (filtro por área)
    
    Returns:
        JSON con lista de usuarios
    """
    try:
        query = WebUser.query
        
        # Filtros
        status = request.args.get('status')
        if status:
            query = query.filter(WebUser.status == status)
        
        role_id = request.args.get('role_id')
        if role_id:
            query = query.filter(WebUser.role_id == role_id)
        
        area = request.args.get('area')
        if area:
            query = query.filter(WebUser.area == area)
        
        # Ordenar por fecha de creación descendente
        query = query.order_by(WebUser.created_at.desc())
        
        users = query.all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener usuarios',
            'details': str(e)
        }), 500


@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    """
    Obtener un usuario específico por ID
    
    Path Params:
        id: ID del usuario
    
    Returns:
        JSON con los detalles del usuario
    """
    try:
        current_user_id = int(get_jwt_identity())  # Convertir de string a int
        current_user = WebUser.query.get(current_user_id)
        
        # Puede ver su propio perfil o tener permiso
        if current_user_id != id and not current_user.can('users.view'):
            return jsonify({'error': 'Acceso denegado'}), 403
        
        user = WebUser.query.get(id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener usuario',
            'details': str(e)
        }), 500


@users_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """
    Actualizar un usuario existente
    Solo super_admin puede editar usuarios
    
    Path Params:
        id: ID del usuario
    
    Body JSON:
        Campos a actualizar (todos opcionales)
    
    Returns:
        JSON con el usuario actualizado
    """
    try:
        # Obtener usuario actual
        current_user_email = get_jwt_identity()
        current_user = WebUser.query.filter_by(email=current_user_email).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        # Solo super_admin puede editar usuarios
        user_role = current_user.role.name if current_user.role else 'colaborador'
        if user_role != 'super_admin':
            return jsonify({
                'error': 'Permiso denegado',
                'message': 'Solo el Administrador TI puede gestionar usuarios'
            }), 403
        
        user = WebUser.query.get(id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'full_name' in data:
            user.full_name = data['full_name']
        
        if 'email' in data:
            # Verificar que no exista otro con ese email
            existing = WebUser.query.filter_by(email=data['email']).first()
            if existing and existing.id != id:
                return jsonify({'error': 'Ya existe un usuario con ese email'}), 409
            user.email = data['email']
        
        # Solo admins pueden cambiar estos campos
        if current_user.can('users.edit'):
            if 'role_id' in data:
                user.role_id = data['role_id']
            if 'area' in data:
                user.area = data['area']
            if 'person_id' in data:
                user.person_id = data['person_id']
            if 'status' in data:
                user.status = data['status']
        
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al actualizar usuario',
            'details': str(e)
        }), 500


@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """
    Eliminar/desactivar un usuario
    Solo super_admin puede eliminar usuarios
    
    Path Params:
        id: ID del usuario
    
    Returns:
        JSON con mensaje de confirmación
    """
    try:
        # Obtener usuario actual
        current_user_email = get_jwt_identity()
        current_user = WebUser.query.filter_by(email=current_user_email).first()
        
        if not current_user:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        # Solo super_admin puede eliminar usuarios
        user_role = current_user.role.name if current_user.role else 'colaborador'
        if user_role != 'super_admin':
            return jsonify({
                'error': 'Permiso denegado',
                'message': 'Solo el Administrador TI puede gestionar usuarios'
            }), 403
        
        # No puede eliminarse a sí mismo
        if current_user.id == id:
            return jsonify({'error': 'No puedes eliminar tu propio usuario'}), 400
        
        user = WebUser.query.get(id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # En lugar de eliminar, desactivar
        user.status = 'inactive'
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario desactivado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al desactivar usuario',
            'details': str(e)
        }), 500


@users_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    """
    Obtener lista de roles disponibles
    
    Returns:
        JSON con lista de roles
    """
    try:
        roles = Role.query.filter_by(status='active').order_by(Role.level).all()
        
        return jsonify({
            'roles': [role.to_dict() for role in roles],
            'total': len(roles)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener roles',
            'details': str(e)
        }), 500
