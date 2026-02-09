from sqlalchemy import create_engine, text
from config import Config

# Verificar múltiples bases de datos
databases = ['sb', 'sb_production', 'sb_training']

for db_name in databases:
    print(f"\n{'='*60}")
    print(f"Base de datos: {db_name}")
    print(f"{'='*60}")
    
    try:
        uri = f"mysql+pymysql://root:@localhost:3306/{db_name}?charset=utf8mb4"
        engine = create_engine(uri)
        
        with engine.connect() as conn:
            result = conn.execute(text('SELECT COUNT(*) as count FROM tasks'))
            tasks_count = result.fetchone()[0]
            print(f"tasks: {tasks_count} registros")
            
            if tasks_count > 0:
                # Verificar tareas con horas reales
                result = conn.execute(text('SELECT COUNT(*) FROM tasks WHERE actual_hours IS NOT NULL'))
                actual_count = result.fetchone()[0]
                print(f"tasks con actual_hours: {actual_count} registros")
    except Exception as e:
        print(f"Error: {e}")

