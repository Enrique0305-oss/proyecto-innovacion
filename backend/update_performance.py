"""
Script para actualizar performance_index de usuarios con valores más realistas
"""
from app import create_app
from app.models.web_user import WebUser
from app.extensions import db
from config import Config
import random

app = create_app(Config)

with app.app_context():
    # Valores realistas de rendimiento (distribución normal)
    # Super admin: alto rendimiento
    admin = WebUser.query.get(1)
    if admin:
        admin.performance_index = 85.0
        print(f"✅ {admin.full_name}: 85%")
    
    # Gerente: buen rendimiento
    gerente = WebUser.query.get(2)
    if gerente:
        gerente.performance_index = 78.0
        print(f"✅ {gerente.full_name}: 78%")
    
    # Supervisor: rendimiento promedio-alto
    supervisor = WebUser.query.get(3)
    if supervisor:
        supervisor.performance_index = 72.0
        print(f"✅ {supervisor.full_name}: 72%")
    
    # Colaborador: rendimiento variable
    colaborador = WebUser.query.get(4)
    if colaborador:
        colaborador.performance_index = 65.0
        print(f"✅ {colaborador.full_name}: 65%")
    
    # Si hay más usuarios, asignar valores aleatorios realistas
    otros_usuarios = WebUser.query.filter(WebUser.id > 4).all()
    for user in otros_usuarios:
        # Distribución normal: media=75, std=10, rango 50-95
        perf = max(50, min(95, random.gauss(75, 10)))
        user.performance_index = round(perf, 1)
        print(f"✅ {user.full_name}: {user.performance_index}%")
    
    db.session.commit()
    print("\n✅ Performance index actualizado para todos los usuarios")
