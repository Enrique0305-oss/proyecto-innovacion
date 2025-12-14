"""
Crear rol 5: Supervisor de Área
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
    cursor = connection.cursor()
    
    # Verificar estructura de la tabla roles
    cursor.execute("DESCRIBE roles")
    columns = cursor.fetchall()
    print("Columnas de la tabla roles:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    
    # Insertar rol 5 si no existe
    cursor.execute("""
        INSERT INTO roles (id, name, display_name, description)
        VALUES (5, 'supervisor_area', 'Supervisor de Área', 
                'Supervisión de una área específica - Solo ve proyectos y tareas de su área asignada')
        ON DUPLICATE KEY UPDATE 
            display_name = VALUES(display_name),
            description = VALUES(description)
    """)
    
    connection.commit()
    print("\n✅ Rol 'Supervisor de Área' creado/actualizado")
    
    # Verificar todos los roles
    cursor.execute("SELECT id, name, display_name FROM roles ORDER BY id")
    roles = cursor.fetchall()
    print(f"\n📋 Roles configurados: {len(roles)}")
    for role in roles:
        print(f"  - Role {role[0]}: {role[1]} ({role[2]})")
    
    # Verificar que web_users tenga columna area
    cursor.execute("DESCRIBE web_users")
    user_columns = [col[0] for col in cursor.fetchall()]
    
    if 'area' in user_columns:
        print("\n✅ Columna 'area' existe en web_users")
    else:
        print("\n⚠️ Agregando columna 'area' a web_users...")
        cursor.execute("ALTER TABLE web_users ADD COLUMN area VARCHAR(50) DEFAULT NULL")
        connection.commit()
        print("✅ Columna 'area' agregada")
    
    # Verificar que projects tenga columna area
    cursor.execute("SHOW TABLES LIKE 'projects'")
    if cursor.fetchone():
        cursor.execute("DESCRIBE projects")
        project_columns = [col[0] for col in cursor.fetchall()]
        
        if 'area' in project_columns:
            print("✅ Columna 'area' existe en projects")
        else:
            print("⚠️ Agregando columna 'area' a projects...")
            cursor.execute("ALTER TABLE projects ADD COLUMN area VARCHAR(50) DEFAULT NULL")
            connection.commit()
            print("✅ Columna 'area' agregada a projects")
    
finally:
    cursor.close()
    connection.close()

print("\n✅ Configuración completa")
