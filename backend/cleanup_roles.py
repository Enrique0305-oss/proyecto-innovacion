"""
Script para limpiar roles antiguos de la base de datos
Mantiene solo los 4 roles del nuevo modelo
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
    print("\n" + "="*70)
    print("🧹 LIMPIEZA DE ROLES ANTIGUOS")
    print("="*70)
    
    # Roles a eliminar
    roles_to_delete = ['admin', 'analyst', 'user']
    
    # Roles a mantener (NUEVO MODELO)
    roles_to_keep = ['super_admin', 'gerente', 'supervisor', 'colaborador']
    
    print("\n📋 ANÁLISIS DE ROLES:")
    print("-" * 70)
    
    all_roles = Role.query.all()
    print(f"\nRoles actuales en BD: {len(all_roles)}")
    for role in all_roles:
        status = "✅ MANTENER" if role.name in roles_to_keep else "❌ ELIMINAR"
        print(f"  {role.id}. {role.name:15} - {role.display_name:25} {status}")
    
    # PASO 1: Migrar usuarios de roles antiguos a nuevos
    print("\n" + "="*70)
    print("📦 PASO 1: MIGRAR USUARIOS")
    print("="*70)
    
    # Obtener IDs de roles nuevos
    super_admin_role = Role.query.filter_by(name='super_admin').first()
    colaborador_role = Role.query.filter_by(name='colaborador').first()
    
    if not super_admin_role or not colaborador_role:
        print("❌ Error: No se encontraron los roles 'super_admin' o 'colaborador'")
        print("   Ejecuta primero: python init_database.py")
        sys.exit(1)
    
    # Migración de usuarios
    migration_map = {
        'admin': super_admin_role.id,      # admin → super_admin
        'analyst': colaborador_role.id,    # analyst → colaborador
        'user': colaborador_role.id        # user → colaborador
    }
    
    total_migrated = 0
    for old_role_name, new_role_id in migration_map.items():
        old_role = Role.query.filter_by(name=old_role_name).first()
        if old_role:
            users = WebUser.query.filter_by(role_id=old_role.id).all()
            if users:
                print(f"\n🔄 Migrando usuarios del rol '{old_role_name}':")
                for user in users:
                    old_role_name_display = old_role.display_name
                    new_role = Role.query.get(new_role_id)
                    print(f"   • {user.email:30} {old_role_name_display:20} → {new_role.display_name}")
                    user.role_id = new_role_id
                    total_migrated += 1
                db.session.commit()
            else:
                print(f"\n✓ No hay usuarios con rol '{old_role_name}'")
    
    print(f"\n✅ Total de usuarios migrados: {total_migrated}")
    
    # PASO 2: Eliminar roles antiguos
    print("\n" + "="*70)
    print("🗑️  PASO 2: ELIMINAR ROLES ANTIGUOS")
    print("="*70)
    
    for role_name in roles_to_delete:
        role = Role.query.filter_by(name=role_name).first()
        if role:
            # Verificar que no haya usuarios con este rol
            users_count = WebUser.query.filter_by(role_id=role.id).count()
            if users_count == 0:
                print(f"\n🗑️  Eliminando rol: {role.name} ({role.display_name})")
                db.session.delete(role)
                db.session.commit()
                print(f"   ✅ Eliminado exitosamente")
            else:
                print(f"\n⚠️  No se puede eliminar '{role.name}': aún tiene {users_count} usuario(s)")
        else:
            print(f"\n✓ Rol '{role_name}' no existe en BD")
    
    # RESUMEN FINAL
    print("\n" + "="*70)
    print("📊 RESUMEN FINAL")
    print("="*70)
    
    remaining_roles = Role.query.order_by(Role.level).all()
    print(f"\n✅ Roles finales en BD: {len(remaining_roles)}")
    print("\n  ID | Nombre          | Display Name          | Level | Usuarios")
    print("  " + "-"*67)
    
    for role in remaining_roles:
        users_count = WebUser.query.filter_by(role_id=role.id).count()
        print(f"  {role.id:2} | {role.name:15} | {role.display_name:20} | {role.level:5} | {users_count:3} usuarios")
    
    total_users = WebUser.query.count()
    print(f"\n  Total de usuarios: {total_users}")
    
    # Validar que solo queden los 4 roles correctos
    expected_roles = {'super_admin', 'gerente', 'supervisor', 'colaborador'}
    actual_roles = {r.name for r in remaining_roles}
    
    if actual_roles == expected_roles:
        print("\n" + "="*70)
        print("✅ ¡LIMPIEZA COMPLETADA EXITOSAMENTE!")
        print("="*70)
        print("\n🎯 Sistema configurado con los 4 roles correctos:")
        print("   1. super_admin  - Administrador TI")
        print("   2. gerente      - Gerente General")
        print("   3. supervisor   - Supervisor de área")
        print("   4. colaborador  - Usuario regular")
        print("\n" + "="*70 + "\n")
    else:
        print("\n⚠️  ADVERTENCIA: Hay roles inesperados en la BD")
        extra_roles = actual_roles - expected_roles
        if extra_roles:
            print(f"   Roles adicionales: {extra_roles}")
        missing_roles = expected_roles - actual_roles
        if missing_roles:
            print(f"   Roles faltantes: {missing_roles}")
