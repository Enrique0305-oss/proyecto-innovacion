"""
Script para actualizar permisos del rol supervisor_area
"""
from app import create_app
from app.models.role import Role
from app.extensions import db
from config import Config
import json

app = create_app(Config)

with app.app_context():
    # Obtener el rol supervisor_area
    role = Role.query.filter_by(name='supervisor_area').first()
    
    if not role:
        print("❌ Rol supervisor_area no encontrado")
        exit(1)
    
    print(f"📋 Rol encontrado: {role.name}")
    print(f"   Display: {role.display_name}")
    print(f"   Permisos actuales: {role.permissions}")
    
    # Definir permisos para supervisor de área
    # Similar a supervisor pero limitado a su área
    permissions_supervisor_area = [
        # Dashboard y visualización
        "dashboard.personal",
        
        # Tareas - solo de su área
        "tasks.view",
        "tasks.view_area",  # Solo tareas de su área
        "tasks.create",
        "tasks.edit",
        "tasks.assign",
        "tasks.delete",
        
        # Proyectos - solo de su área
        "projects.view",
        "projects.view_area",  # Solo proyectos de su área
        "projects.create",
        "projects.edit",
        
        # Personas - solo de su área
        "persons.view",
        "persons.view_area",  # Solo personas de su área
        
        # Áreas - solo puede ver
        "areas.view",
        
        # ML - puede usar predicciones
        "ml.predict_risk",
        "ml.predict_duration",
        "ml.recommend_person",
        "ml.analyze_performance"
    ]
    
    # Actualizar permisos
    role.permissions = json.dumps(permissions_supervisor_area)
    
    db.session.commit()
    
    print(f"\n✅ Permisos actualizados para {role.name}")
    print(f"   Total permisos: {len(permissions_supervisor_area)}")
    print(f"\nPermisos asignados:")
    for perm in permissions_supervisor_area:
        print(f"   - {perm}")
    
    # Verificar
    role_check = Role.query.filter_by(name='supervisor_area').first()
    perms_loaded = json.loads(role_check.permissions)
    print(f"\n✅ Verificación: {len(perms_loaded)} permisos guardados correctamente")
