"""
Middleware de Permisos y Filtrado por Área
==========================================
Decoradores y funciones helper para control de acceso basado en roles
y filtrado automático de datos por área.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.extensions import db
from app.models.web_user import WebUser

# =====================================================
# DEFINICIÓN DE PERMISOS POR ROL
# =====================================================

ROLE_PERMISSIONS = {
    1: {  # Super Admin
        'view_all_projects': True,
        'create_projects': True,
        'delete_projects': True,
        'manage_users': True,
        'view_all_areas': True,
        'approve_tasks': True,
        'access_ml_models': True,
        'system_config': True,
        'area_restricted': False
    },
    2: {  # Gerente General
        'view_all_projects': True,
        'create_projects': True,
        'delete_projects': False,
        'manage_users': False,
        'view_all_areas': True,
        'approve_tasks': True,
        'access_ml_models': True,
        'system_config': False,
        'area_restricted': False
    },
    3: {  # Supervisor General
        'view_all_projects': True,
        'create_projects': True,
        'delete_projects': False,
        'manage_users': False,
        'view_all_areas': True,
        'approve_tasks': True,
        'access_ml_models': True,
        'system_config': False,
        'area_restricted': False
    },
    4: {  # Colaborador
        'view_all_projects': False,
        'create_projects': False,
        'delete_projects': False,
        'manage_users': False,
        'view_all_areas': False,
        'approve_tasks': False,
        'access_ml_models': False,
        'system_config': False,
        'area_restricted': False,
        'view_own_tasks_only': True
    },
    5: {  # Supervisor de Área
        'view_all_projects': False,
        'create_projects': True,
        'delete_projects': False,
        'manage_users': False,
        'view_all_areas': False,
        'approve_tasks': True,
        'access_ml_models': True,
        'system_config': False,
        'area_restricted': True  # SOLO ve su área
    }
}


# =====================================================
# HELPERS - OBTENER USUARIO Y PERMISOS
# =====================================================

def get_current_user():
    """
    Obtener el usuario actual desde el JWT
    
    Returns:
        WebUser: Objeto usuario o None
    """
    try:
        verify_jwt_in_request()
        user_email = get_jwt_identity()
        user = WebUser.query.filter_by(email=user_email).first()
        return user
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
        return None


def get_user_permissions(user):
    """
    Obtener permisos del usuario según su rol
    
    Args:
        user (WebUser): Objeto usuario
        
    Returns:
        dict: Diccionario de permisos
    """
    if not user:
        return {}
    
    return ROLE_PERMISSIONS.get(user.role_id, {})


def has_permission(user, permission_name):
    """
    Verificar si el usuario tiene un permiso específico
    
    Args:
        user (WebUser): Objeto usuario
        permission_name (str): Nombre del permiso
        
    Returns:
        bool: True si tiene el permiso
    """
    permissions = get_user_permissions(user)
    return permissions.get(permission_name, False)


def is_area_restricted(user):
    """
    Verificar si el usuario está restringido a un área
    
    Args:
        user (WebUser): Objeto usuario
        
    Returns:
        bool: True si solo puede ver su área
    """
    return has_permission(user, 'area_restricted')


# =====================================================
# DECORADORES DE PERMISOS
# =====================================================

def require_permission(permission_name):
    """
    Decorador para requerir un permiso específico
    
    Usage:
        @require_permission('create_projects')
        def create_project():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return jsonify({'error': 'Usuario no autenticado'}), 401
            
            if not has_permission(user, permission_name):
                return jsonify({
                    'error': 'Permiso denegado',
                    'required_permission': permission_name,
                    'user_role': user.role_id
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(*permission_names):
    """
    Decorador para requerir al menos uno de varios permisos
    
    Usage:
        @require_any_permission('manage_users', 'view_all_areas')
        def admin_function():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return jsonify({'error': 'Usuario no autenticado'}), 401
            
            has_any = any(has_permission(user, perm) for perm in permission_names)
            
            if not has_any:
                return jsonify({
                    'error': 'Permiso denegado',
                    'required_permissions': list(permission_names),
                    'user_role': user.role_id
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_role(*role_ids):
    """
    Decorador para requerir un rol específico
    
    Usage:
        @require_role(1, 2)  # Solo Super Admin o Gerente
        def executive_function():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return jsonify({'error': 'Usuario no autenticado'}), 401
            
            if user.role_id not in role_ids:
                return jsonify({
                    'error': 'Rol no autorizado',
                    'required_roles': list(role_ids),
                    'user_role': user.role_id
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# =====================================================
# FILTROS DE CONSULTA POR ÁREA
# =====================================================

def apply_area_filter(query, model, user):
    """
    Aplicar filtro de área a una consulta SQLAlchemy
    
    Args:
        query: Consulta SQLAlchemy
        model: Modelo con campo 'area' o 'area_id'
        user: Usuario actual
        
    Returns:
        query: Consulta filtrada
    """
    # Si el usuario no está restringido por área, retornar sin filtro
    if not is_area_restricted(user):
        return query
    
    # Si no tiene área asignada, no puede ver nada
    if not user.area:
        return query.filter(False)  # Retorna vacío
    
    # Obtener ID del área del usuario si existe
    from app.models.area import Area
    user_area_obj = Area.query.filter_by(name=user.area).first()
    
    if not user_area_obj:
        return query.filter(False)  # Si no existe el área, no mostrar nada
    
    # Filtrar por área del usuario
    # Si el modelo tiene area_id (como Project), usar eso
    if hasattr(model, 'area_id'):
        return query.filter(model.area_id == user_area_obj.id)
    # Si tiene area como string (legacy), usar eso
    elif hasattr(model, 'area'):
        return query.filter(model.area == user.area)
    
    return query


def can_access_resource(user, resource):
    """
    Verificar si el usuario puede acceder a un recurso
    (proyecto, tarea, etc) basado en su área
    
    Args:
        user: Usuario actual
        resource: Objeto con campo 'area' o relación 'area'
        
    Returns:
        bool: True si puede acceder
    """
    # Roles sin restricción de área
    if not is_area_restricted(user):
        return True
    
    # Colaborador solo ve sus propias tareas
    if has_permission(user, 'view_own_tasks_only'):
        # Verificar si está asignado
        if hasattr(resource, 'assigned_to'):
            return resource.assigned_to == user.email or resource.assigned_to == str(user.id)
        return False
    
    # Supervisor de área solo ve recursos de su área
    if not user.area:
        return False
    
    # Obtener área del recurso
    resource_area_name = None
    if hasattr(resource, 'area') and resource.area:
        # Si es una relación (objeto Area)
        if hasattr(resource.area, 'name'):
            resource_area_name = resource.area.name
        # Si es un string directo
        else:
            resource_area_name = resource.area
    
    return resource_area_name == user.area


# =====================================================
# FUNCIONES DE UTILIDAD
# =====================================================

def get_accessible_areas(user):
    """
    Obtener lista de áreas accesibles para el usuario
    
    Args:
        user: Usuario actual
        
    Returns:
        list: Lista de nombres de áreas o None (todas)
    """
    if has_permission(user, 'view_all_areas'):
        return None  # Puede ver todas
    
    if is_area_restricted(user) and user.area:
        return [user.area]  # Solo su área
    
    return []  # Sin acceso


def filter_by_accessible_areas(items, user):
    """
    Filtrar una lista de objetos por áreas accesibles
    
    Args:
        items: Lista de objetos con campo 'area'
        user: Usuario actual
        
    Returns:
        list: Lista filtrada
    """
    accessible_areas = get_accessible_areas(user)
    
    # Si puede ver todas, retornar todo
    if accessible_areas is None:
        return items
    
    # Si no tiene acceso a ninguna área
    if not accessible_areas:
        return []
    
    # Filtrar por áreas accesibles
    return [item for item in items if item.area in accessible_areas]


def get_user_info_dict(user):
    """
    Obtener información del usuario incluyendo permisos
    
    Args:
        user: Usuario actual
        
    Returns:
        dict: Información del usuario
    """
    if not user:
        return None
    
    permissions = get_user_permissions(user)
    
    return {
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'role_id': user.role_id,
        'area': user.area,
        'permissions': permissions,
        'accessible_areas': get_accessible_areas(user)
    }
