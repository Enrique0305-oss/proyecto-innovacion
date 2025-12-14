"""
Script para ejecutar la configuración de roles desde Python
"""
import pymysql
import os

# Leer el archivo SQL
sql_file = os.path.join('..', 'database', '04_setup_area_roles.sql')

with open(sql_file, 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Conectar a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='sb_production',
    charset='utf8mb4'
)

try:
    cursor = connection.cursor()
    
    # Ejecutar cada statement SQL separado por punto y coma
    statements = sql_content.split(';')
    
    for i, statement in enumerate(statements):
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                cursor.execute(statement)
                print(f"✓ Statement {i+1} ejecutado")
            except Exception as e:
                # Ignorar errores de SELECT que son solo informativos
                if 'SELECT' not in statement.upper():
                    print(f"⚠ Error en statement {i+1}: {e}")
    
    connection.commit()
    print("\n✅ Configuración de roles completada exitosamente")
    
    # Verificar roles creados
    cursor.execute("SELECT * FROM roles ORDER BY id")
    roles = cursor.fetchall()
    print(f"\n📋 Roles configurados: {len(roles)}")
    for role in roles:
        print(f"  - Role {role[0]}: {role[1]}")
    
finally:
    cursor.close()
    connection.close()
