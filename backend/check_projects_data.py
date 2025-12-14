"""
Verificar datos de proyectos
"""
from app import create_app
from app.models.project import Project
from config import Config

app = create_app(Config)

with app.app_context():
    projects = Project.query.all()
    print(f"\n📋 Total proyectos: {len(projects)}\n")
    
    for project in projects:
        data = project.to_dict(include_stats=True)
        print(f"Proyecto: {project.project_id}")
        print(f"  Nombre: {project.name}")
        print(f"  Área: {data.get('area')}")
        print(f"  Manager ID: {data.get('manager_id')}")
        print(f"  Manager Name: {data.get('manager_name')}")
        print()
