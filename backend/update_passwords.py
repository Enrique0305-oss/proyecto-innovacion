"""
Script para actualizar contraseñas de usuarios con bcrypt
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.web_user import WebUser

app = create_app()

with app.app_context():
    print("🔐 Actualizando contraseñas de usuarios...")
    print("=" * 60)
    
    # Obtener todos los usuarios
    users = WebUser.query.all()
    
    if not users:
        print("❌ No se encontraron usuarios")
    else:
        # Actualizar contraseña a 'admin123' para todos
        for user in users:
            user.set_password('admin123')
            print(f"✅ {user.email} - Contraseña actualizada")
        
        db.session.commit()
        print("=" * 60)
        print(f"✅ {len(users)} contraseñas actualizadas exitosamente")
        print("   Contraseña para todos: admin123")
