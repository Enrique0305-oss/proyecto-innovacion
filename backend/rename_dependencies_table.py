"""
Script para renombrar la tabla de dependencias
"""
import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'sb_production'
}

def rename_table():
    """Renombra task_dependencies a web_task_dependencies"""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(buffered=True)
        
        # Verificar si existe la tabla antigua
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'sb_production' 
            AND TABLE_NAME = 'task_dependencies'
        """)
        exists = cursor.fetchone()[0]
        
        if exists:
            print("Eliminando tabla 'task_dependencies' antigua...")
            cursor.execute("DROP TABLE IF EXISTS task_dependencies")
            conn.commit()
            print("✓ Tabla eliminada")
        
        print("\nCreando tabla 'web_task_dependencies'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS web_task_dependencies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                project_id VARCHAR(64) NOT NULL,
                predecessor_task_id INT NOT NULL COMMENT 'Tarea que debe completarse primero',
                successor_task_id INT NOT NULL COMMENT 'Tarea que depende de la anterior',
                dependency_type ENUM('finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish') DEFAULT 'finish_to_start',
                lag_days INT DEFAULT 0 COMMENT 'Días de espera entre tareas',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
                FOREIGN KEY (predecessor_task_id) REFERENCES web_tasks(id) ON DELETE CASCADE,
                FOREIGN KEY (successor_task_id) REFERENCES web_tasks(id) ON DELETE CASCADE,
                UNIQUE KEY unique_dependency (predecessor_task_id, successor_task_id),
                INDEX idx_project (project_id),
                INDEX idx_predecessor (predecessor_task_id),
                INDEX idx_successor (successor_task_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        conn.commit()
        print("✓ Tabla 'web_task_dependencies' creada")
        
        print("\n✅ Renombrado completado exitosamente")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Error MySQL: {err}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == '__main__':
    rename_table()
