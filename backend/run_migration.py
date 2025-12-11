"""
Script para ejecutar la migración de proyectos
"""
import mysql.connector
from pathlib import Path

# Configuración de conexión
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  # Tomado de config.py
    'database': 'sb_production'
}

def run_migration():
    """Ejecuta el script SQL de migración"""
    try:
        # Leer el archivo SQL
        sql_file = Path(__file__).parent.parent / 'database' / '04_create_projects_tables.sql'
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Conectar a la base de datos
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(buffered=True)  # Usar cursor buffered para manejar múltiples resultados
        
        # Ejecutar cada statement por separado
        statements = [s.strip() for s in sql_script.split(';') if s.strip()]
        
        for i, statement in enumerate(statements):
            # Saltar comentarios
            if statement.startswith('--') or statement.startswith('/*'):
                continue
            
            try:
                print(f"Ejecutando statement {i+1}/{len(statements)}...")
                cursor.execute(statement)
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Error en statement {i+1}: {err}")
                print(f"Statement: {statement[:100]}...")
                # Continuar con el siguiente statement
        
        print("\n✅ Migración completada exitosamente")
        
        # Verificar tablas creadas
        cursor.execute("SHOW TABLES LIKE 'projects'")
        if cursor.fetchone():
            print("✓ Tabla 'projects' creada")
        
        cursor.execute("SHOW TABLES LIKE 'task_dependencies'")
        if cursor.fetchone():
            print("✓ Tabla 'task_dependencies' creada")
        
        # Verificar datos de ejemplo
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        print(f"✓ Proyectos insertados: {count}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error ejecutando migración: {e}")
        raise

if __name__ == '__main__':
    run_migration()
