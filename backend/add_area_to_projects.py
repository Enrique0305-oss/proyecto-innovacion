"""
Migración: Agregar columna area a la tabla projects
"""
from app import create_app
from app.extensions import db
from config import Config

app = create_app(Config)

with app.app_context():
    try:
        # Agregar columna area usando text()
        from sqlalchemy import text
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE projects ADD COLUMN area VARCHAR(100)'))
            conn.commit()
        print("✅ Columna 'area' agregada a la tabla projects")
        
        # Verificar
        from app.models.project import Project
        projects = Project.query.all()
        print(f"✅ Verificación exitosa. Total proyectos: {len(projects)}")
        
        # Actualizar proyectos existentes con un área por defecto
        for project in projects:
            if not project.area:
                # Asignar área basada en el nombre del proyecto
                if 'CRM' in project.name or 'Sistema' in project.name:
                    project.area = 'Tecnología'
                elif 'AWS' in project.name or 'Cloud' in project.name:
                    project.area = 'Operaciones'
                elif 'Móvil' in project.name or 'E-commerce' in project.name:
                    project.area = 'Comercial'
                else:
                    project.area = 'Tecnología'  # Default
                
                print(f"  - {project.project_id}: {project.area}")
        
        db.session.commit()
        print(f"\n✅ {len(projects)} proyectos actualizados con áreas")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if "Duplicate column name" in str(e):
            print("⚠️  La columna 'area' ya existe")
        db.session.rollback()
