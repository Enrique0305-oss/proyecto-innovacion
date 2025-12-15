"""
Migración: Convertir campo area de VARCHAR a foreign key
Corrige el diseño de la tabla projects para usar relación con tabla areas
"""
import pymysql
from sqlalchemy import text
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    try:
        print("\n🔧 MIGRACIÓN: Convertir area de VARCHAR a FOREIGN KEY")
        print("=" * 70)
        
        # 1. Verificar áreas existentes
        print("\n1️⃣ Verificando áreas en tabla areas...")
        areas = db.session.execute(text("SELECT id, name FROM areas WHERE status = 'active'")).fetchall()
        
        area_map = {area.name: area.id for area in areas}
        print(f"   ✅ Encontradas {len(areas)} áreas:")
        for name, id in area_map.items():
            print(f"      - {name} (ID: {id})")
        
        # 2. Verificar proyectos actuales
        print("\n2️⃣ Verificando proyectos existentes...")
        projects = db.session.execute(text("SELECT project_id, name, area FROM projects")).fetchall()
        print(f"   ✅ Encontrados {len(projects)} proyectos")
        
        # 3. Agregar columna area_id temporal
        print("\n3️⃣ Agregando columna area_id...")
        try:
            db.session.execute(text("""
                ALTER TABLE projects 
                ADD COLUMN area_id INT NULL
            """))
            db.session.commit()
            print("   ✅ Columna area_id agregada")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("   ⚠️ Columna area_id ya existe, continuando...")
                db.session.rollback()
            else:
                raise
        
        # 4. Migrar datos: mapear nombres de área a IDs
        print("\n4️⃣ Migrando datos de area (VARCHAR) a area_id (INT)...")
        migrated = 0
        for project in projects:
            project_id, name, area_name = project
            
            if area_name and area_name in area_map:
                area_id = area_map[area_name]
                db.session.execute(
                    text("UPDATE projects SET area_id = :area_id WHERE project_id = :project_id"),
                    {'area_id': area_id, 'project_id': project_id}
                )
                migrated += 1
                print(f"   ✅ {name}: '{area_name}' → ID {area_id}")
            else:
                print(f"   ⚠️ {name}: '{area_name}' no encontrada en tabla areas")
        
        db.session.commit()
        print(f"\n   ✅ {migrated}/{len(projects)} proyectos migrados")
        
        # 5. Eliminar columna area antigua
        print("\n5️⃣ Eliminando columna area antigua (VARCHAR)...")
        try:
            db.session.execute(text("ALTER TABLE projects DROP COLUMN area"))
            db.session.commit()
            print("   ✅ Columna area eliminada")
        except Exception as e:
            if "check that it exists" in str(e) or "Unknown column" in str(e):
                print("   ⚠️ Columna area ya fue eliminada")
                db.session.rollback()
            else:
                raise
        
        # 6. Agregar foreign key constraint
        print("\n6️⃣ Agregando constraint de foreign key...")
        try:
            db.session.execute(text("""
                ALTER TABLE projects 
                ADD CONSTRAINT fk_projects_area 
                FOREIGN KEY (area_id) REFERENCES areas(id)
            """))
            db.session.commit()
            print("   ✅ Foreign key constraint agregada")
        except Exception as e:
            if "Duplicate foreign key" in str(e) or "already exists" in str(e):
                print("   ⚠️ Foreign key ya existe")
                db.session.rollback()
            else:
                raise
        
        # 7. Verificar resultado final
        print("\n7️⃣ Verificando estructura final...")
        result = db.session.execute(text("""
            SELECT 
                p.project_id, 
                p.name, 
                p.area_id,
                a.name as area_name
            FROM projects p
            LEFT JOIN areas a ON p.area_id = a.id
            LIMIT 5
        """)).fetchall()
        
        print("\n   📋 Primeros 5 proyectos con nueva estructura:")
        for row in result:
            print(f"      {row.project_id}: {row.name} → Área: {row.area_name} (ID: {row.area_id})")
        
        print("\n" + "=" * 70)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("\nCambios realizados:")
        print("  • Campo 'area' (VARCHAR) → Eliminado")
        print("  • Campo 'area_id' (INT) → Agregado con FK a tabla areas")
        print("  • Relación establecida: projects.area_id → areas.id")
        print("\n💡 Ahora los proyectos usan foreign key correctamente")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ ERROR en la migración: {str(e)}")
        import traceback
        traceback.print_exc()
