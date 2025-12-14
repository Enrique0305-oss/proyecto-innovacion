"""
Test: Verificar JSON que devuelve el endpoint
"""
from app import create_app
from app.models.project import Project
from config import Config
import json

app = create_app(Config)

with app.app_context():
    project = Project.query.first()
    
    print("\n=== DATOS DEL MODELO ===")
    print(f"project.area = {project.area}")
    print(f"project.manager_id = {project.manager_id}")
    
    print("\n=== DATOS EN to_dict() ===")
    data = project.to_dict(include_stats=True)
    print(json.dumps(data, indent=2, default=str))
    
    print(f"\n¿Tiene 'area'? {'area' in data}")
    print(f"Valor de 'area': {data.get('area')}")
