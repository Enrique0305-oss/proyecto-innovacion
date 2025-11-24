"""
Inicialización de la aplicación Flask
Factory Pattern para crear la app
"""
from flask import Flask, jsonify
from app.extensions import init_extensions, db
from app.routes import register_blueprints


def create_app(config_class=None):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_class: Clase de configuración a usar
        
    Returns:
        app: Instancia configurada de Flask
    """
    app = Flask(__name__)
    
    # Desactivar redirección automática de rutas con/sin slash
    app.url_map.strict_slashes = False
    
    # Cargar configuración
    if config_class:
        app.config.from_object(config_class)
    else:
        from config import get_config
        app.config.from_object(get_config())
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Registrar blueprints (rutas)
    register_blueprints(app)
    
    # Crear carpeta de modelos ML si no existe
    import os
    models_path = app.config.get('ML_MODELS_PATH', app.config.get('MODELS_PATH'))
    if not os.path.exists(models_path):
        os.makedirs(models_path, exist_ok=True)
        print(f"✅ Carpeta de modelos ML creada: {models_path}")
    
    # Manejadores de errores globales
    register_error_handlers(app)
    
    # Ruta de health check
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint para verificar que el servidor está funcionando"""
        return jsonify({
            'status': 'ok',
            'message': 'Backend Flask está funcionando correctamente',
            'environment': app.config.get('FLASK_ENV', 'development')
        }), 200
    
    @app.route('/', methods=['GET'])
    def index():
        """Página de inicio del API"""
        return jsonify({
            'message': 'API de Sistema de Análisis de Productividad',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'auth': '/api/auth/*',
                'tasks': '/api/tasks/*',
                'ml': '/api/ml/*'
            }
        }), 200
    
    return app


def register_error_handlers(app):
    """Registra manejadores de errores personalizados"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Recurso no encontrado',
            'message': str(error)
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Error interno del servidor',
            'message': str(error)
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Solicitud inválida',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'No autorizado',
            'message': 'Se requiere autenticación'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Acceso denegado',
            'message': 'No tienes permisos para acceder a este recurso'
        }), 403
