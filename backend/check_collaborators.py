"""
Script para verificar colaboradores en la BD
"""
from app import create_app
from app.extensions import db
from app.models.web_user import WebUser

app = create_app()

with app.app_context():
    # Verificar usuarios
    print("=" * 60)
    print("VERIFICACIÓN DE COLABORADORES")
    print("=" * 60)
    
    # Total usuarios
    total_users = WebUser.query.count()
    print(f"\n📊 Total de usuarios: {total_users}")
    
    # Usuarios por rol
    print("\n👥 Usuarios por rol:")
    roles = db.session.execute(db.text("""
        SELECT role_id, COUNT(*) as count 
        FROM web_users 
        GROUP BY role_id
    """)).fetchall()
    
    for role in roles:
        print(f"  - Role ID {role[0]}: {role[1]} usuarios")
    
    # Colaboradores activos (role_id = 7)
    colaboradores = WebUser.query.filter(
        WebUser.role_id == 7,
        WebUser.status == 'active'
    ).all()
    
    print(f"\n✅ Colaboradores activos (role_id=7, status='active'): {len(colaboradores)}")
    
    if colaboradores:
        print("\nLista de colaboradores:")
        for collab in colaboradores:
            print(f"  - ID: {collab.id} | {collab.full_name} | Área: {collab.area} | Email: {collab.email}")
    else:
        print("\n⚠️  NO HAY COLABORADORES ACTIVOS CON role_id=7")
        
    # Ver todos los usuarios
    print("\n📋 Todos los usuarios:")
    all_users = WebUser.query.all()
    for user in all_users:
        print(f"  - ID: {user.id} | {user.full_name} | Role: {user.role_id} | Status: {user.status} | Área: {user.area}")
    
    print("\n" + "=" * 60)
