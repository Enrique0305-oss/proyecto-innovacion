"""
Asignar responsables a los proyectos
"""
from app import create_app
from app.models.project import Project
from app.models.web_user import WebUser
from app.extensions import db
from config import Config

app = create_app(Config)

with app.app_context():
    # Obtener usuarios que pueden ser managers (gerentes y super_admin)
    managers = WebUser.query.filter(
        WebUser.role_id.in_([1, 2])  # 1=super_admin, 2=gerente
    ).all()
    
    if not managers:
        print("❌ No hay gerentes disponibles")
        exit(1)
    
    print(f"👥 Managers disponibles:")
    for m in managers:
        print(f"  - ID {m.id}: {m.full_name} ({m.role.name})")
    
    # Asignar managers a proyectos
    projects = Project.query.all()
    print(f"\n📋 Asignando responsables a {len(projects)} proyectos:\n")
    
    for i, project in enumerate(projects):
        # Alternar entre los managers disponibles
        manager = managers[i % len(managers)]
        project.manager_id = manager.id
        
        print(f"✅ {project.project_id}: {manager.full_name}")
    
    db.session.commit()
    print(f"\n✅ Responsables asignados correctamente")
    
    # Verificar
    print("\n📊 Verificación:")
    for project in Project.query.all():
        data = project.to_dict()
        print(f"  - {project.project_id}: {data['manager_name']}")
