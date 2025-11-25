"""
Script para inicializar la base de datos con roles y usuarios
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.web_user import WebUser
from app.models.role import Role

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("🚀 INICIALIZANDO BASE DE DATOS")
    print("="*60)
    
    # ==========================================
    # 1. CREAR ROLES
    # ==========================================
    print("\n📋 Creando roles...")
    
    roles_data = [
        {
            'name': 'admin',
            'display_name': 'Administrador',
            'description': 'Acceso total al sistema',
            'level': 1,
            'permissions': [
                'tasks.view', 'tasks.create', 'tasks.edit', 'tasks.delete',
                'users.view', 'users.create', 'users.edit', 'users.delete',
                'areas.view', 'areas.create', 'areas.edit', 'areas.delete',
                'ml.view', 'ml.train', 'ml.predict',
                'reports.view', 'reports.export',
                'settings.manage'
            ]
        },
        {
            'name': 'manager',
            'display_name': 'Gerente',
            'description': 'Gestión de tareas y reportes',
            'level': 2,
            'permissions': [
                'tasks.view', 'tasks.create', 'tasks.edit', 'tasks.delete',
                'users.view',
                'areas.view',
                'ml.view', 'ml.predict',
                'reports.view', 'reports.export'
            ]
        },
        {
            'name': 'analyst',
            'display_name': 'Analista',
            'description': 'Análisis y visualización de datos',
            'level': 3,
            'permissions': [
                'tasks.view', 'tasks.create', 'tasks.edit',
                'areas.view',
                'ml.view', 'ml.predict',
                'reports.view'
            ]
        },
        {
            'name': 'user',
            'display_name': 'Usuario',
            'description': 'Usuario básico del sistema',
            'level': 4,
            'permissions': [
                'tasks.view', 'tasks.create',
                'areas.view',
                'reports.view'
            ]
        }
    ]
    
    for role_data in roles_data:
        existing_role = Role.query.filter_by(name=role_data['name']).first()
        if not existing_role:
            role = Role(**role_data)
            db.session.add(role)
            print(f"  ✅ Rol creado: {role_data['display_name']}")
        else:
            print(f"  ℹ️  Rol ya existe: {role_data['display_name']}")
    
    db.session.commit()
    
    # ==========================================
    # 2. CREAR USUARIOS
    # ==========================================
    print("\n👥 Creando usuarios...")
    
    # Obtener roles
    admin_role = Role.query.filter_by(name='admin').first()
    manager_role = Role.query.filter_by(name='manager').first()
    analyst_role = Role.query.filter_by(name='analyst').first()
    user_role = Role.query.filter_by(name='user').first()
    
    users_data = [
        {
            'email': 'admin@processmart.com',
            'full_name': 'Administrador del Sistema',
            'role_id': admin_role.id,
            'area': 'TI',
            'password': 'admin123'
        },
        {
            'email': 'gerente@processmart.com',
            'full_name': 'Gerente General',
            'role_id': manager_role.id,
            'area': 'Gerencia',
            'password': 'gerente123'
        },
        {
            'email': 'analista@processmart.com',
            'full_name': 'Analista de Datos',
            'role_id': analyst_role.id,
            'area': 'TI',
            'password': 'analista123'
        },
        {
            'email': 'usuario@processmart.com',
            'full_name': 'Usuario de Prueba',
            'role_id': user_role.id,
            'area': 'Ventas',
            'password': 'usuario123'
        }
    ]
    
    for user_data in users_data:
        existing_user = WebUser.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            password = user_data.pop('password')
            user = WebUser(**user_data)
            user.set_password(password)
            db.session.add(user)
            print(f"  ✅ Usuario creado: {user_data['email']} (contraseña: {password})")
        else:
            print(f"  ℹ️  Usuario ya existe: {user_data['email']}")
    
    db.session.commit()
    
    # ==========================================
    # 3. RESUMEN
    # ==========================================
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    print(f"  Roles creados: {Role.query.count()}")
    print(f"  Usuarios creados: {WebUser.query.count()}")
    print("\n🔐 CREDENCIALES DE ACCESO:")
    print("  Admin:    admin@processmart.com / admin123")
    print("  Gerente:  gerente@processmart.com / gerente123")
    print("  Analista: analista@processmart.com / analista123")
    print("  Usuario:  usuario@processmart.com / usuario123")
    print("="*60)
    print("✅ ¡Base de datos inicializada correctamente!")
    print("="*60 + "\n")
