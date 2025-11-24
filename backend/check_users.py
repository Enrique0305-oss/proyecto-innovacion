"""Script para verificar usuarios y crear uno de prueba si es necesario"""
from app.extensions import db
from app import create_app
from config import get_config
from app.models.web_user import WebUser
from app.models.role import Role

app = create_app(get_config())
app.app_context().push()

print("\n=== USUARIOS EXISTENTES ===")
users = WebUser.query.all()
for u in users:
    rol_name = u.role.name if u.role else "Sin rol"
    print(f"ID: {u.id} | Email: {u.email} | Rol: {rol_name} | Status: {u.status}")

print("\n=== ROLES EXISTENTES ===")
roles = Role.query.all()
for r in roles:
    print(f"ID: {r.id} | Name: {r.name} | Display: {r.display_name}")

# Verificar si existe un usuario admin
admin_user = WebUser.query.filter_by(email='admin@processmart.com').first()

if not admin_user:
    print("\n=== CREANDO USUARIO ADMIN DE PRUEBA ===")
    admin_role = Role.query.filter_by(name='admin').first()
    
    if not admin_role:
        print("Creando rol admin...")
        admin_role = Role(
            name='admin',
            display_name='Administrador',
            description='Acceso completo al sistema',
            permissions=['*'],
            level=100,
            status='active'
        )
        db.session.add(admin_role)
        db.session.commit()
    
    admin_user = WebUser(
        email='admin@processmart.com',
        full_name='Administrador',
        role_id=admin_role.id,
        status='active'
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    db.session.commit()
    print(f"✅ Usuario creado: admin@processmart.com / admin123")
else:
    print(f"\n✅ Usuario admin ya existe: {admin_user.email}")
    # Actualizar password por si acaso
    admin_user.set_password('admin123')
    db.session.commit()
    print("✅ Password actualizada a: admin123")

print("\n=== CREDENCIALES PARA LOGIN ===")
print("Email: admin@processmart.com")
print("Password: admin123")
