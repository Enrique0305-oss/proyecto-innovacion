"""
Script de prueba de conexión a base de datos
Verifica que las dos bases de datos estén accesibles
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models import WebUser, Role, Area, MLModel
from sqlalchemy import text


def test_database_connections():
    """Prueba las conexiones a ambas bases de datos"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("🔍 PRUEBA DE CONEXIÓN A BASES DE DATOS")
        print("=" * 60)
        
        # Test 1: Conexión a sb_production
        try:
            result = db.session.execute(text("SELECT DATABASE()")).scalar()
            print(f"\n✅ Conectado a: {result}")
            
            # Contar tablas
            tables = db.session.execute(text("SHOW TABLES")).fetchall()
            print(f"   Tablas encontradas: {len(tables)}")
            for table in tables[:5]:
                print(f"   - {table[0]}")
            if len(tables) > 5:
                print(f"   ... y {len(tables) - 5} más")
                
        except Exception as e:
            print(f"\n❌ Error en sb_production: {e}")
            return False
        
        # Test 2: Conexión a sb_training
        try:
            with db.get_engine(app, bind='training').connect() as conn:
                result = conn.execute(text("SELECT DATABASE()")).scalar()
                print(f"\n✅ Conectado a: {result} (training)")
                
                # Contar registros en people
                people_count = conn.execute(text("SELECT COUNT(*) FROM people")).scalar()
                tasks_count = conn.execute(text("SELECT COUNT(*) FROM tasks")).scalar()
                
                print(f"   Registros en people: {people_count:,}")
                print(f"   Registros en tasks: {tasks_count:,}")
                
        except Exception as e:
            print(f"\n❌ Error en sb_training: {e}")
            print("   Verifica que la BD sb_training existe")
        
        # Test 3: Leer datos de producción
        print(f"\n📊 DATOS EN sb_production:")
        print("-" * 60)
        
        try:
            roles_count = Role.query.count()
            areas_count = Area.query.count()
            users_count = WebUser.query.count()
            models_count = MLModel.query.count()
            
            print(f"   Roles: {roles_count}")
            print(f"   Áreas: {areas_count}")
            print(f"   Usuarios web: {users_count}")
            print(f"   Modelos ML: {models_count}")
            
            # Listar usuarios
            if users_count > 0:
                print(f"\n👥 Usuarios registrados:")
                users = WebUser.query.limit(5).all()
                for user in users:
                    role_name = user.role.name if user.role else 'sin rol'
                    print(f"   - {user.email} ({role_name})")
            
            # Listar modelos ML
            if models_count > 0:
                print(f"\n🤖 Modelos ML:")
                models = MLModel.query.all()
                for model in models:
                    status_icon = "✅" if model.status == 'activo' else "⏸️"
                    print(f"   {status_icon} {model.name} v{model.version} ({model.type}) - {model.precision}% precisión")
            
        except Exception as e:
            print(f"   ❌ Error al leer datos: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Pruebas completadas")
        print("=" * 60)
        return True


if __name__ == '__main__':
    success = test_database_connections()
    sys.exit(0 if success else 1)
