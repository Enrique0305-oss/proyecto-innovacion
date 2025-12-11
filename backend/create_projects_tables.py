"""
Script simplificado para crear tablas de proyectos
"""
import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'sb_production'
}

def create_tables():
    """Crea las tablas necesarias"""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(buffered=True)
        
        print("Creando tabla 'projects'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id VARCHAR(64) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                start_date DATE,
                expected_end_date DATE,
                actual_end_date DATE,
                status ENUM('planning', 'in_progress', 'completed', 'on_hold', 'cancelled') DEFAULT 'planning',
                budget DECIMAL(15,2),
                priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
                manager_id INT,
                progress_percentage DECIMAL(5,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (manager_id) REFERENCES web_users(id) ON DELETE SET NULL,
                INDEX idx_status (status),
                INDEX idx_manager (manager_id),
                INDEX idx_dates (start_date, expected_end_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        conn.commit()
        print("✓ Tabla 'projects' creada")
        
        print("\nModificando tabla 'web_tasks'...")
        # Verificar si la columna ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = 'sb_production' 
            AND TABLE_NAME = 'web_tasks' 
            AND COLUMN_NAME = 'project_id'
        """)
        exists = cursor.fetchone()[0]
        
        if not exists:
            # Primero agregar la columna sin FK
            cursor.execute("""
                ALTER TABLE web_tasks 
                ADD COLUMN project_id VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL AFTER id
            """)
            conn.commit()
            
            # Luego agregar el índice
            cursor.execute("""
                ALTER TABLE web_tasks
                ADD INDEX idx_task_project (project_id)
            """)
            conn.commit()
            
            # Finalmente agregar la FK
            cursor.execute("""
                ALTER TABLE web_tasks
                ADD CONSTRAINT fk_task_project FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE SET NULL
            """)
            conn.commit()
            print("✓ Columna 'project_id' agregada a 'web_tasks'")
        else:
            print("✓ Columna 'project_id' ya existe en 'web_tasks'")
        
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
        print("✓ Tabla 'task_dependencies' creada")
        
        print("\nInsertando proyecto por defecto...")
        cursor.execute("""
            INSERT IGNORE INTO projects (
                project_id, 
                name, 
                description, 
                status, 
                start_date,
                priority
            ) VALUES (
                'PROJ-DEFAULT',
                'Tareas sin proyecto asignado',
                'Proyecto contenedor para tareas creadas antes de implementar la gestión de proyectos',
                'in_progress',
                CURDATE(),
                'medium'
            )
        """)
        conn.commit()
        print("✓ Proyecto 'PROJ-DEFAULT' creado")
        
        print("\nAsignando tareas existentes al proyecto por defecto...")
        cursor.execute("UPDATE web_tasks SET project_id = 'PROJ-DEFAULT' WHERE project_id IS NULL")
        affected = cursor.rowcount
        conn.commit()
        print(f"✓ {affected} tareas asignadas a 'PROJ-DEFAULT'")
        
        print("\nInsertando proyectos de ejemplo...")
        cursor.execute("""
            INSERT IGNORE INTO projects (project_id, name, description, status, start_date, expected_end_date, priority, manager_id) VALUES
            ('PROJ-2025-001', 'Implementación Sistema CRM', 'Desarrollo e implementación del nuevo sistema CRM para gestión de clientes', 'in_progress', '2025-01-15', '2025-06-30', 'high', 1),
            ('PROJ-2025-002', 'Migración a Cloud AWS', 'Migración de infraestructura on-premise a AWS Cloud', 'planning', '2025-02-01', '2025-08-31', 'critical', 2),
            ('PROJ-2025-003', 'App Móvil E-commerce', 'Desarrollo de aplicación móvil para plataforma de ventas', 'in_progress', '2025-01-10', '2025-05-15', 'high', 3)
        """)
        conn.commit()
        print("✓ Proyectos de ejemplo insertados")
        
        # Verificar
        print("\n" + "="*50)
        print("VERIFICACIÓN FINAL")
        print("="*50)
        
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        print(f"✓ Total de proyectos: {count}")
        
        cursor.execute("SELECT COUNT(*) FROM web_task_dependencies")
        count = cursor.fetchone()[0]
        print(f"✓ Total de dependencias: {count}")
        
        cursor.execute("SELECT COUNT(*) FROM web_tasks WHERE project_id IS NOT NULL")
        count = cursor.fetchone()[0]
        print(f"✓ Tareas con proyecto asignado: {count}")
        
        print("\n✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Error MySQL: {err}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == '__main__':
    create_tables()
