from app import create_app, db
from sqlalchemy import text

app = create_app()

def create_training_schedules_table():
    """Crea la tabla training_schedules en la base de datos"""
    
    drop_table_sql = "DROP TABLE IF EXISTS training_schedules"
    
    create_table_sql = """
    CREATE TABLE training_schedules (
        id INT AUTO_INCREMENT PRIMARY KEY,
        model_type VARCHAR(50) NOT NULL,
        scheduled_date DATE NOT NULL,
        scheduled_time VARCHAR(10) NOT NULL,
        status VARCHAR(20) DEFAULT 'programado',
        parameters TEXT,
        last_execution DATETIME,
        execution_result TEXT,
        created_by INT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        is_recurring BOOLEAN DEFAULT FALSE,
        recurrence_pattern VARCHAR(20),
        FOREIGN KEY (created_by) REFERENCES web_users(id) ON DELETE SET NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Eliminar tabla si existe
                conn.execute(text(drop_table_sql))
                conn.commit()
                print("✅ Tabla training_schedules eliminada (si existía)")
                
                # Crear nueva tabla
                conn.execute(text(create_table_sql))
                conn.commit()
                print("✅ Tabla training_schedules creada exitosamente")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

if __name__ == "__main__":
    create_training_schedules_table()
