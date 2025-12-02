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
    from app.routes.task_routes import tasks_bp
    from app.routes.area_routes import areas_bp
    from app.routes.ml_routes import ml_bp
    from app.routes.ml_training_routes import ml_training_bp
    from app.routes.user_routes import users_bp
    from app.routes.person_routes import persons_bp
    
    # Prefijo base para todas las rutas de API
    api_prefix = '/api'
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(tasks_bp, url_prefix=f'{api_prefix}/tasks')
    app.register_blueprint(areas_bp, url_prefix=f'{api_prefix}/areas')
    app.register_blueprint(ml_bp, url_prefix=f'{api_prefix}/ml')
    app.register_blueprint(ml_training_bp, url_prefix=f'{api_prefix}/ml')  # Rutas de entrenamiento
    app.register_blueprint(users_bp, url_prefix=f'{api_prefix}/users')
    app.register_blueprint(persons_bp, url_prefix=f'{api_prefix}/persons')
    
    print("✅ Blueprints registrados correctamente")
