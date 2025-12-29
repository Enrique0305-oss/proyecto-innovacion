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
    from app.routes.project_routes import project_bp
    from app.routes.process_mining_routes import process_mining_bp
    from app.routes.meeting_routes import meetings_bp
    from app.routes.training_schedule_routes import training_schedule_bp
    from app.routes.training_routes import bp as training_bp  # Nuevo sistema de training
    
    # Prefijo base para todas las rutas de API
    api_prefix = '/api'
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(tasks_bp, url_prefix=f'{api_prefix}/tasks')
    app.register_blueprint(areas_bp, url_prefix=f'{api_prefix}/areas')
    app.register_blueprint(ml_bp, url_prefix=f'{api_prefix}/ml')
    app.register_blueprint(ml_training_bp, url_prefix=f'{api_prefix}/ml')  # Rutas de entrenamiento
    app.register_blueprint(training_bp)  # Training manager (ya tiene url_prefix)
    app.register_blueprint(users_bp, url_prefix=f'{api_prefix}/users')
    app.register_blueprint(persons_bp, url_prefix=f'{api_prefix}/persons')
    app.register_blueprint(project_bp, url_prefix=f'{api_prefix}')
    app.register_blueprint(process_mining_bp, url_prefix=f'{api_prefix}/ml/process-mining')
    app.register_blueprint(meetings_bp, url_prefix=f'{api_prefix}/meetings')
    app.register_blueprint(training_schedule_bp, url_prefix=f'{api_prefix}')  # Programación de reentrenamiento
    
    print("✅ Blueprints registrados correctamente")
