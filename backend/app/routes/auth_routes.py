"""
Rutas de Autenticación
Endpoints para login, registro y gestión de usuarios
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

from app.extensions import db
from app.models.user import User

# Crear Blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registrar un nuevo usuario
    
    Body JSON:
        - username: str (requerido)
        - email: str (requerido)
        - password: str (requerido)
        - first_name: str (opcional)
        - last_name: str (opcional)
        - role: str (opcional, default: 'user')
    
    Returns:
        JSON con el usuario creado y token JWT
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({
                'error': 'Faltan campos requeridos',
                'required': ['username', 'email', 'password']
            }), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'El nombre de usuario ya existe'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        # Crear nuevo usuario
        new_user = User(
            username=username,
            email=email,
            password=password,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role', 'user')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Crear token JWT
        access_token = create_access_token(identity=new_user.id)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': new_user.to_dict(),
            'access_token': access_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al registrar usuario',
            'details': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión
    
    Body JSON:
        - username: str (requerido)
        - password: str (requerido)
    
    Returns:
        JSON con el usuario y token JWT
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({
                'error': 'Faltan campos requeridos',
                'required': ['username', 'password']
            }), 400
        
        # Buscar usuario
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
        
        # Verificar contraseña
        if not user.check_password(password):
            return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
        
        # Verificar si está activo
        if not user.is_active:
            return jsonify({'error': 'Usuario inactivo'}), 403
        
        # Actualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Crear token JWT
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login exitoso',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al iniciar sesión',
            'details': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obtener información del usuario actual
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        JSON con la información del usuario
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
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


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    Cambiar contraseña del usuario actual
    
    Headers:
        Authorization: Bearer <token>
    
    Body JSON:
        - old_password: str (requerido)
        - new_password: str (requerido)
    
    Returns:
        JSON con mensaje de éxito
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not all([old_password, new_password]):
            return jsonify({
                'error': 'Faltan campos requeridos',
                'required': ['old_password', 'new_password']
            }), 400
        
        # Verificar contraseña actual
        if not user.check_password(old_password):
            return jsonify({'error': 'Contraseña actual incorrecta'}), 401
        
        # Cambiar contraseña
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'message': 'Contraseña actualizada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al cambiar contraseña',
            'details': str(e)
        }), 500


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """
    Listar todos los usuarios (solo admin)
    
    Headers:
        Authorization: Bearer <token>
    
    Query Params:
        - page: int (default: 1)
        - per_page: int (default: 20)
    
    Returns:
        JSON con lista paginada de usuarios
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        
        # Verificar que sea admin
        if current_user.role != 'admin':
            return jsonify({'error': 'Acceso denegado - se requiere rol admin'}), 403
        
        # Paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Consultar usuarios
        pagination = User.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al listar usuarios',
            'details': str(e)
        }), 500
