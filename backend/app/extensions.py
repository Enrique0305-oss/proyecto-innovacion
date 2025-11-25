"""
Extensiones de Flask
Inicialización de SQLAlchemy, CORS, Migrate, JWT, etc.
"""
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()


def init_extensions(app):
    """
    Inicializa todas las extensiones de Flask
    
    Args:
        app: Instancia de Flask
    """
    # SQLAlchemy
    db.init_app(app)
    
    # Flask-Migrate
    migrate.init_app(app, db)
    
    # CORS - Configuración completa y permisiva
    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": False,
                "max_age": 3600
            }
        }
    )
    
    # JWT
    jwt.init_app(app)
    
    # Manejadores de errores de JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token expirado',
            'message': 'El token de autenticación ha expirado'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Token inválido',
            'message': 'La firma del token es inválida'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Token requerido',
            'message': 'Se requiere un token de autenticación para acceder a este recurso'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token revocado',
            'message': 'El token ha sido revocado'
        }), 401
    
    return app
