"""
Corregir mapeo de áreas en proyectos
"""
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='sb_production',
    charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # Mapeo de nombres
        area_mapping = {
            'Tecnología': 'IT',  # Tecnología → IT
            'Operaciones': 'Operations',  # Operaciones → Operations
            'Comercial': 'Sales',  # Comercial → Sales
        }
        
        print("\n🔧 CORRIGIENDO MAPEO DE ÁREAS")
        print("=" * 60)
        
        # Obtener IDs de las áreas correctas
        for old_name, new_name in area_mapping.items():
            cursor.execute("SELECT id FROM areas WHERE name = %s", (new_name,))
            result = cursor.fetchone()
            
            if result:
                area_id = result[0]
                
                # Actualizar proyectos que tengan NULL en area_id
                # basándonos en el nombre original que deberían tener
                updates = [
                    ('PROJ-2025-001', 'IT'),  # Implementación Sistema CRM
                    ('PROJ-2025-734', 'IT'),  # Creacion del CRM
                    ('PROJ-DEFAULT', 'IT'),   # Tareas sin proyecto
                    ('PROJ-2025-002', 'Operations'),  # Migración a Cloud AWS
                    ('PROJ-2025-003', 'Sales'),  # App Móvil E-commerce
                    ('PROJ-TEST-001', 'IT'),  # Proyecto de Prueba
                ]
                
                for proj_id, area_name in updates:
                    if area_name == new_name:
                        cursor.execute(
                            "UPDATE projects SET area_id = %s WHERE project_id = %s",
                            (area_id, proj_id)
                        )
                        print(f"✅ {proj_id} → {new_name} (ID: {area_id})")
        
        connection.commit()
        
        # Verificar resultado
        print("\n📊 PROYECTOS ACTUALIZADOS:")
        cursor.execute("""
            SELECT p.project_id, p.name, a.name as area_name 
            FROM projects p 
            LEFT JOIN areas a ON p.area_id = a.id
        """)
        
        for row in cursor.fetchall():
            proj_id, name, area = row
            print(f"  {proj_id}: {name} → {area}")
        
        print("\n✅ Áreas corregidas exitosamente")

finally:
    connection.close()
