"""
Script para recrear la tabla meetings con tipos VARCHAR
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db

def recreate_meetings_table():
    """Elimina y recrea la tabla meetings"""
    app = create_app()
    
    with app.app_context():
        try:
            from sqlalchemy import text
            
            # Eliminar tabla si existe
            with db.engine.connect() as conn:
                conn.execute(text("DROP TABLE IF EXISTS meetings"))
                conn.commit()
            print("✅ Tabla meetings eliminada")
            
            # Crear tabla con SQL directo
            create_table_sql = """
            CREATE TABLE meetings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                project_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
                meeting_date DATE NOT NULL,
                meeting_time VARCHAR(10),
                duration INT DEFAULT 60,
                meeting_type VARCHAR(20) DEFAULT 'virtual',
                location VARCHAR(255),
                status VARCHAR(20) DEFAULT 'programada',
                participant_ids TEXT,
                created_by INT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
                FOREIGN KEY (created_by) REFERENCES web_users(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            with db.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
            print("✅ Tabla meetings creada exitosamente con VARCHAR")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    recreate_meetings_table()
