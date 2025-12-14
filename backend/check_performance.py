"""
Script para verificar performance_index de usuarios
"""
from app import create_app
from app.models.web_user import WebUser
from config import Config

app = create_app(Config)

with app.app_context():
    users = WebUser.query.all()
    
    print("\n=== PERFORMANCE INDEX DE USUARIOS ===\n")
    for user in users:
        print(f"ID: {user.id} | {user.full_name:30s} | performance_index: {user.performance_index}")
    
    print(f"\nTotal usuarios: {len(users)}")
    users_with_perf = [u for u in users if u.performance_index is not None]
    print(f"Usuarios con performance_index: {len(users_with_perf)}")
    print(f"Usuarios sin performance_index: {len(users) - len(users_with_perf)}")
