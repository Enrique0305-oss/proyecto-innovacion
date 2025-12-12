"""
Script para verificar uso de roles
"""
from app.extensions import db
from app import create_app
from app.models.web_user import WebUser
from app.models.role import Role

app = create_app()

with app.app_context():
    # Verificar usuarios
    users = WebUser.query.all()
    print(f"📊 Total usuarios: {len(users)}\n")
    
    if users:
        print("👥 Usuarios existentes:")
        for u in users:
            role_name = u.role.name if u.role else "Sin rol"
            print(f"  - {u.full_name} ({u.email}) - role_id: {u.role_id} ({role_name})")
    
    # Verificar roles
    print("\n🎭 Roles actuales:")
    roles = Role.query.all()
    for r in roles:
        user_count = WebUser.query.filter_by(role_id=r.id).count()
        print(f"  - ID {r.id}: {r.name} ({r.display_name}) - {user_count} usuarios")
    
    print("\n" + "="*60)
    if len(users) <= 5 and all("@processmart.com" in u.email for u in users):
        print("✅ Son usuarios de prueba - SEGURO reiniciar")
    else:
        print("⚠️  Tienes usuarios reales - NO recomendado reiniciar")
