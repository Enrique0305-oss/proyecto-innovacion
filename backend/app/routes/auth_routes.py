"""
Rutas de Autenticación
Endpoints para login, registro y gestión de usuarios web
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

from app.extensions import db
from app.models.web_user import WebUser
from app.models.role import Role
from app.utils.permissions import get_user_permissions, get_accessible_areas

# Crear Blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registrar un nuevo usuario web
    
    Body JSON:
        - email: str (requerido)
        - password: str (requerido)
        - full_name: str (requerido)
        - role_name: str (opcional, default: 'user')
        - area: str (opcional)
    
    Returns:
        JSON con el usuario creado y token JWT
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        if not all([email, password, full_name]):
            return jsonify({
                'error': 'Faltan campos requeridos',
                'required': ['email', 'password', 'full_name']
            }), 400
        
        # Verificar si el usuario ya existe
        if WebUser.query.filter_by(email=email).first():
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        # Obtener rol (default: user)
        role_name = data.get('role_name', 'user')
        role = Role.query.filter_by(name=role_name).first()
        
        if not role:
            return jsonify({'error': f'Rol {role_name} no existe'}), 400
        
        # Crear nuevo usuario
        new_user = WebUser(
            email=email,
            full_name=full_name,
            role_id=role.id,
            area=data.get('area'),
            status='active'
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Crear token JWT con el email del usuario
        access_token = create_access_token(identity=new_user.email)
        
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
        - email: str (requerido)
        - password: str (requerido)
    
    Returns:
        JSON con el usuario y token JWT
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({
                'error': 'Faltan campos requeridos',
                'required': ['email', 'password']
            }), 400
        
        # Buscar usuario
        print(f"🔍 Buscando usuario: {email}")
        user = WebUser.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ Usuario no encontrado: {email}")
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401
        
        print(f"✅ Usuario encontrado: {user.email}")
        
        # Verificar contraseña
        print(f"🔐 Verificando contraseña...")
        if not user.check_password(password):
            print(f"❌ Contraseña incorrecta")
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401
        
        print(f"✅ Contraseña correcta")
        
        # Verificar si está activo
        if user.status != 'active':
            print(f"❌ Usuario inactivo")
            return jsonify({'error': 'Usuario inactivo'}), 403
        
        print(f"✅ Usuario activo")
        
        # Actualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        print(f"✅ Last login actualizado")
        
        # Crear token JWT con el email del usuario
        access_token = create_access_token(identity=user.email)
        
        print(f"✅ Token JWT creado")
        
        # Convertir usuario a dict
        print(f"📦 Convirtiendo usuario a dict...")
        user_dict = user.to_dict()
        
        # Agregar permisos y áreas accesibles
        user_dict['permissions'] = get_user_permissions(user)
        user_dict['accessible_areas'] = get_accessible_areas(user)
        
        print(f"✅ Usuario convertido a dict")
        
        return jsonify({
            'message': 'Login exitoso',
            'user': user_dict,
            'access_token': access_token
        }), 200
        
    except Exception as e:
        import traceback
        print(f"💥 ERROR EN LOGIN:")
        print(traceback.format_exc())
        db.session.rollback()
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
        user_email = get_jwt_identity()  # Obtener email del JWT
        user = WebUser.query.filter_by(email=user_email).first()
        
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
        user_id = int(get_jwt_identity())  # Convertir de string a int
        user = WebUser.query.get(user_id)
        
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
    Listar todos los usuarios (requiere permiso users.view)
    
    Headers:
        Authorization: Bearer <token>
    
    Query Params:
        - page: int (default: 1)
        - per_page: int (default: 20)
    
    Returns:
        JSON con lista paginada de usuarios
    """
    try:
        user_id = int(get_jwt_identity())  # Convertir de string a int
        current_user = WebUser.query.get(user_id)
        
        # Verificar permisos
        if not current_user.can('users.view'):
            return jsonify({'error': 'Acceso denegado - permisos insuficientes'}), 403
        
        # Paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Consultar usuarios
        pagination = WebUser.query.paginate(
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
