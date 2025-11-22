"""
Registro de Blueprints (rutas)
Centraliza el registro de todas las rutas de la API
"""
def register_blueprints(app):
    """
    Registra todos los blueprints de la aplicación
    
    Args:
        app: Instancia de Flask
    """
    from app.routes.auth_routes import auth_bp
    from app.routes.task_routes import task_bp
    from app.routes.ml_routes import ml_bp
    
    # Prefijo base para todas las rutas de API
    api_prefix = '/api'
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(task_bp, url_prefix=f'{api_prefix}/tasks')
    app.register_blueprint(ml_bp, url_prefix=f'{api_prefix}/ml')
    
    print("✅ Blueprints registrados correctamente")
