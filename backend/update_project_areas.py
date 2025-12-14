"""
Actualizar áreas de proyectos existentes
"""
from app import create_app
from app.models.project import Project
from app.extensions import db
from config import Config

app = create_app(Config)

with app.app_context():
    projects = Project.query.all()
    print(f"📋 Actualizando {len(projects)} proyectos\n")
    
    for project in projects:
        old_area = project.area
        
        # Asignar área basada en el nombre del proyecto
        if not project.area or project.area == 'NULL':
            if 'CRM' in project.name or 'Sistema' in project.name:
                project.area = 'Tecnología'
            elif 'AWS' in project.name or 'Cloud' in project.name or 'Migración' in project.name:
                project.area = 'Operaciones'
            elif 'Móvil' in project.name or 'E-commerce' in project.name or 'App' in project.name:
                project.area = 'Comercial'
            elif 'Prueba' in project.name or 'Test' in project.name:
                project.area = 'Tecnología'
            else:
                project.area = 'Tecnología'  # Default
            
            print(f"✅ {project.project_id}: {old_area} → {project.area}")
    
    db.session.commit()
    print(f"\n✅ Actualización completada")
    
    # Verificar
    print("\n📊 Resumen:")
    for project in Project.query.all():
        print(f"  - {project.project_id}: {project.area}")
