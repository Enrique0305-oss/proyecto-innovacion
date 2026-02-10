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
    print(" INICIALIZANDO BASE DE DATOS")
    print("="*60)
    
    # ==========================================
    # 1. CREAR ROLES
    # ==========================================
    print("\n Creando roles...")
    
    roles_data = [
        {
            'name': 'super_admin',
            'display_name': 'Super Administrador',
            'description': 'Administrador TI - Gestión completa del sistema',
            'level': 1,
            'permissions': [
                'tasks.view', 'tasks.create', 'tasks.edit', 'tasks.delete',
                'users.view', 'users.create', 'users.edit', 'users.delete',
                'areas.view', 'areas.create', 'areas.edit', 'areas.delete',
                'ml.view', 'ml.train', 'ml.predict', 'ml.configure',
                'reports.view', 'reports.export',
                'settings.manage',
                'system.configure'
            ]
        },
        {
            'name': 'gerente',
            'display_name': 'Gerente General',
            'description': 'Visión ejecutiva - Dashboards y reportes solamente',
            'level': 2,
            'permissions': [
                'dashboard.executive',
                'tasks.view',
                'users.view',
                'areas.view',
                'ml.view', 'ml.predict',
                'reports.view', 'reports.export'
            ]
        },
        {
            'name': 'supervisor',
            'display_name': 'Supervisor',
            'description': 'Jefe de área - Gestión de tareas de su área',
            'level': 3,
            'permissions': [
                'dashboard.area',
                'tasks.view', 'tasks.create', 'tasks.edit', 'tasks.delete',
                'tasks.assign',
                'users.view',
                'areas.view',
                'ml.view', 'ml.predict',
                'reports.view', 'reports.export'
            ]
        },
        {
            'name': 'colaborador',
            'display_name': 'Colaborador',
            'description': 'Usuario regular - Solo sus tareas',
            'level': 4,
            'permissions': [
                'dashboard.personal',
                'tasks.view', 'tasks.update_status',
                'areas.view'
            ]
        }
    ]
    
    for role_data in roles_data:
        existing_role = Role.query.filter_by(name=role_data['name']).first()
        if not existing_role:
            role = Role(**role_data)
            db.session.add(role)
            print(f"   Rol creado: {role_data['display_name']}")
        else:
            print(f"    Rol ya existe: {role_data['display_name']}")
    
    db.session.commit()
    
    # ==========================================
    # 2. CREAR USUARIOS
    # ==========================================
    print("\n Creando usuarios...")
    
    # Obtener roles
    super_admin_role = Role.query.filter_by(name='super_admin').first()
    gerente_role = Role.query.filter_by(name='gerente').first()
    supervisor_role = Role.query.filter_by(name='supervisor').first()
    colaborador_role = Role.query.filter_by(name='colaborador').first()
    
    users_data = [
        {
            'email': 'admin@processmart.com',
            'full_name': 'Administrador TI',
            'role_id': super_admin_role.id,
            'area': 'TI',
            'password': 'admin123'
        },
        {
            'email': 'gerente@processmart.com',
            'full_name': 'Gerente General',
            'role_id': gerente_role.id,
            'area': 'Gerencia',
            'password': 'gerente123'
        },
        {
            'email': 'supervisor@processmart.com',
            'full_name': 'Supervisor de Ventas',
            'role_id': supervisor_role.id,
            'area': 'Ventas',
            'password': 'supervisor123'
        },
        {
            'email': 'usuario@processmart.com',
            'full_name': 'Usuario Colaborador',
            'role_id': colaborador_role.id,
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
            print(f"   Usuario creado: {user_data['email']} (contraseña: {password})")
        else:
            print(f"    Usuario ya existe: {user_data['email']}")
    
    db.session.commit()
    
    # ==========================================
    # 3. RESUMEN
    # ==========================================
    print("\n" + "="*60)
    print(" RESUMEN")
    print("="*60)
    print(f"  Roles creados: {Role.query.count()}")
    print(f"  Usuarios creados: {WebUser.query.count()}")
    print("\n CREDENCIALES DE ACCESO:")
    print("  Super Admin:  admin@processmart.com / admin123")
    print("  Gerente:      gerente@processmart.com / gerente123")
    print("  Supervisor:   supervisor@processmart.com / supervisor123")
    print("  Colaborador:  usuario@processmart.com / usuario123")
    print("="*60)
    print(" ¡Base de datos inicializada correctamente!")
    print("="*60 + "\n")
