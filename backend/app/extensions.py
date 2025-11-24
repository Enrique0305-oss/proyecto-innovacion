"""
Extensiones de Flask
Inicialización de SQLAlchemy, CORS, Migrate, JWT, etc.
"""
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
    
    return app
