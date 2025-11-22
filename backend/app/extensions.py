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
    
    # CORS
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}},
        supports_credentials=True
    )
    
    # JWT
    jwt.init_app(app)
    
    return app
