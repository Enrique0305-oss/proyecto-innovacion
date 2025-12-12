"""
Script para REINICIAR roles con IDs consecutivos (1,2,3,4)
⚠️  SOLO para ambientes de desarrollo con usuarios de prueba
"""
from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.web_user import WebUser

app = create_app()

with app.app_context():
    print("=" * 70)
    print("🔄 REINICIO DE ROLES Y USUARIOS")
    print("=" * 70)
    
    # 1. Mostrar estado actual
    print("\n📊 Estado ANTES:")
    roles_antes = Role.query.all()
    users_antes = WebUser.query.all()
    print(f"  - Roles: {len(roles_antes)}")
    print(f"  - Usuarios: {len(users_antes)}")
    for r in roles_antes:
        count = WebUser.query.filter_by(role_id=r.id).count()
        print(f"    • ID {r.id}: {r.name} ({count} usuarios)")
    
    # 2. Confirmación
    print("\n⚠️  ADVERTENCIA:")
    print("  - Se eliminarán TODOS los usuarios")
    print("  - Se eliminarán TODOS los roles")
    print("  - Se crearán 4 usuarios de prueba nuevos")
    print("  - Contraseñas: admin123, gerente123, supervisor123, usuario123")
    
    respuesta = input("\n¿Continuar? (escribe 'SI' para confirmar): ")
    
    if respuesta.upper() != 'SI':
        print("\n❌ Operación cancelada")
        exit()
    
    # 3. Eliminar usuarios (por FK)
    print("\n🗑️  Eliminando usuarios...")
    WebUser.query.delete()
    db.session.commit()
    print("  ✅ Usuarios eliminados")
    
    # 4. Eliminar roles
    print("🗑️  Eliminando roles...")
    Role.query.delete()
    db.session.commit()
    print("  ✅ Roles eliminados")
    
    # 5. Reiniciar AUTO_INCREMENT
    print("🔢 Reiniciando AUTO_INCREMENT...")
    db.session.execute(db.text("ALTER TABLE roles AUTO_INCREMENT = 1"))
    db.session.execute(db.text("ALTER TABLE web_users AUTO_INCREMENT = 1"))
    db.session.commit()
    print("  ✅ Contadores reiniciados")
    
    # 6. Crear roles con IDs consecutivos
    print("\n🎭 Creando roles nuevos...")
    
    roles_data = [
        {
            'name': 'super_admin',
            'display_name': 'Super Administrador',
            'description': 'Administrador TI - Gestión completa del sistema',
            'permissions': '["tasks.view", "tasks.create", "tasks.edit", "tasks.delete", "tasks.assign", "users.manage", "areas.manage", "projects.manage"]',
            'level': 1
        },
        {
            'name': 'gerente',
            'display_name': 'Gerente General',
            'description': 'Visión ejecutiva - Dashboards y reportes + gestión de proyectos',
            'permissions': '["dashboard.executive", "tasks.view", "users.view", "projects.manage", "projects.view"]',
            'level': 2
        },
        {
            'name': 'supervisor',
            'display_name': 'Supervisor',
            'description': 'Supervisión de áreas, aprobación de tareas y reportes',
            'permissions': '["tasks.create", "tasks.edit", "tasks.assign", "tasks.approve", "dashboard.area", "projects.view"]',
            'level': 2
        },
        {
            'name': 'colaborador',
            'display_name': 'Colaborador',
            'description': 'Usuario regular - Solo sus tareas',
            'permissions': '["dashboard.personal", "tasks.view", "tasks.update_own"]',
            'level': 4
        }
    ]
    
    roles_creados = {}
    for role_data in roles_data:
        role = Role(**role_data, status='active')
        db.session.add(role)
        db.session.flush()  # Para obtener el ID
        roles_creados[role.name] = role.id
        print(f"  ✅ ID {role.id}: {role.name} ({role.display_name})")
    
    db.session.commit()
    
    # 7. Crear usuarios de prueba
    print("\n👥 Creando usuarios de prueba...")
    
    usuarios_data = [
        {
            'email': 'admin@processmart.com',
            'password': 'admin123',
            'full_name': 'Administrador Sistema',
            'role_name': 'super_admin',
            'area': 'TI'
        },
        {
            'email': 'gerente@processmart.com',
            'password': 'gerente123',
            'full_name': 'Gerente General',
            'role_name': 'gerente',
            'area': 'Gerencia'
        },
        {
            'email': 'supervisor@processmart.com',
            'password': 'supervisor123',
            'full_name': 'Supervisor Producción',
            'role_name': 'supervisor',
            'area': 'Producción'
        },
        {
            'email': 'usuario@processmart.com',
            'password': 'usuario123',
            'full_name': 'Usuario Colaborador',
            'role_name': 'colaborador',
            'area': 'Operaciones'
        }
    ]
    
    for user_data in usuarios_data:
        role_name = user_data.pop('role_name')
        password = user_data.pop('password')
        
        user = WebUser(
            **user_data,
            role_id=roles_creados[role_name],
            status='active'
        )
        user.set_password(password)  # Usar el método del modelo que usa bcrypt
        db.session.add(user)
        db.session.flush()
        print(f"  ✅ {user.full_name} ({user.email}) - Role ID: {user.role_id}")
    
    db.session.commit()
    
    # 8. Verificar resultado final
    print("\n📊 Estado DESPUÉS:")
    roles_despues = Role.query.order_by(Role.id).all()
    users_despues = WebUser.query.all()
    print(f"  - Roles: {len(roles_despues)}")
    print(f"  - Usuarios: {len(users_despues)}")
    for r in roles_despues:
        count = WebUser.query.filter_by(role_id=r.id).count()
        print(f"    • ID {r.id}: {r.name} ({count} usuarios)")
    
    print("\n" + "=" * 70)
    print("✅ REINICIO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print("\n🔑 Credenciales de acceso:")
    print("  • admin@processmart.com / admin123")
    print("  • gerente@processmart.com / gerente123")
    print("  • supervisor@processmart.com / supervisor123")
    print("  • usuario@processmart.com / usuario123")
    print()
