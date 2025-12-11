-- ====================================
-- SCRIPT 4: CREAR TABLAS DE PROYECTOS
-- ====================================
-- Agrega la estructura de proyectos al sistema
-- Incluye: projects, task_dependencies
-- ====================================

USE sb_production;

-- ============================================
-- Tabla: PROJECTS
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Modificar tabla WEB_TASKS: Agregar FK a proyectos
-- ============================================
ALTER TABLE web_tasks 
ADD COLUMN project_id VARCHAR(64) DEFAULT NULL AFTER id,
ADD FOREIGN KEY fk_task_project (project_id) REFERENCES projects(project_id) ON DELETE SET NULL,
ADD INDEX idx_task_project (project_id);

-- ============================================
-- Tabla: TASK_DEPENDENCIES
-- ============================================
CREATE TABLE IF NOT EXISTS task_dependencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id VARCHAR(64) NOT NULL,
    predecessor_task_id INT NOT NULL COMMENT 'Tarea que debe completarse primero',
    successor_task_id INT NOT NULL COMMENT 'Tarea que depende de la anterior',
    dependency_type ENUM('finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish') DEFAULT 'finish_to_start',
    lag_days INT DEFAULT 0 COMMENT 'Días de espera entre tareas (puede ser negativo para adelanto)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (predecessor_task_id) REFERENCES web_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (successor_task_id) REFERENCES web_tasks(id) ON DELETE CASCADE,
    UNIQUE KEY unique_dependency (predecessor_task_id, successor_task_id),
    INDEX idx_project (project_id),
    INDEX idx_predecessor (predecessor_task_id),
    INDEX idx_successor (successor_task_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Crear proyecto por defecto para tareas existentes
-- ============================================
INSERT INTO projects (
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
);

-- ============================================
-- Asignar tareas existentes al proyecto default
-- ============================================
UPDATE web_tasks 
SET project_id = 'PROJ-DEFAULT' 
WHERE project_id IS NULL;

-- ============================================
-- Vista: PROJECT_SUMMARY
-- ============================================
CREATE OR REPLACE VIEW v_project_summary AS
SELECT 
    p.project_id,
    p.name,
    p.status,
    p.start_date,
    p.expected_end_date,
    p.actual_end_date,
    p.priority,
    u.full_name as manager_name,
    COUNT(DISTINCT wt.id) as total_tasks,
    SUM(CASE WHEN wt.status = 'completada' THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN wt.status = 'en_progreso' THEN 1 ELSE 0 END) as in_progress_tasks,
    SUM(CASE WHEN wt.status = 'pendiente' THEN 1 ELSE 0 END) as pending_tasks,
    COUNT(DISTINCT wt.assigned_to) as team_size,
    COUNT(DISTINCT td.id) as dependencies_count,
    ROUND(
        SUM(CASE WHEN wt.status = 'completada' THEN 1 ELSE 0 END) * 100.0 / COUNT(wt.id),
        2
    ) as completion_percentage,
    DATEDIFF(IFNULL(p.actual_end_date, CURDATE()), p.start_date) as duration_days
FROM projects p
LEFT JOIN web_tasks wt ON p.project_id = wt.project_id
LEFT JOIN web_users u ON p.manager_id = u.id
LEFT JOIN task_dependencies td ON p.project_id = td.project_id
GROUP BY 
    p.project_id, p.name, p.status, p.start_date, 
    p.expected_end_date, p.actual_end_date, p.priority, u.full_name;

-- ============================================
-- Vista: TASK_NETWORK (para GNN)
-- ============================================
CREATE OR REPLACE VIEW v_task_network AS
SELECT 
    td.project_id,
    td.predecessor_task_id,
    wt1.title as predecessor_title,
    wt1.status as predecessor_status,
    td.successor_task_id,
    wt2.title as successor_title,
    wt2.status as successor_status,
    td.dependency_type,
    td.lag_days,
    CASE 
        WHEN wt1.status = 'completada' THEN 'completed'
        WHEN wt1.status = 'en_progreso' THEN 'active'
        WHEN wt2.status != 'pendiente' AND wt1.status = 'pendiente' THEN 'blocked'
        ELSE 'ready'
    END as edge_status
FROM task_dependencies td
JOIN web_tasks wt1 ON td.predecessor_task_id = wt1.id
JOIN web_tasks wt2 ON td.successor_task_id = wt2.id;

-- ============================================
-- Vista: CRITICAL_PATH_CANDIDATES
-- ============================================
CREATE OR REPLACE VIEW v_critical_path_candidates AS
SELECT 
    wt.project_id,
    wt.id as task_id,
    wt.title,
    wt.estimated_hours,
    COUNT(DISTINCT td_pred.predecessor_task_id) as predecessor_count,
    COUNT(DISTINCT td_succ.successor_task_id) as successor_count,
    wt.priority,
    wt.status
FROM web_tasks wt
LEFT JOIN task_dependencies td_pred ON wt.id = td_pred.successor_task_id
LEFT JOIN task_dependencies td_succ ON wt.id = td_succ.predecessor_task_id
GROUP BY wt.project_id, wt.id, wt.title, wt.estimated_hours, wt.priority, wt.status
ORDER BY (predecessor_count + successor_count) DESC;

-- ============================================
-- Datos de ejemplo: Proyectos de prueba
-- ============================================
INSERT INTO projects (project_id, name, description, status, start_date, expected_end_date, priority, manager_id) VALUES
('PROJ-2025-001', 'Implementación Sistema CRM', 'Desarrollo e implementación del nuevo sistema CRM para gestión de clientes', 'in_progress', '2025-01-15', '2025-06-30', 'high', 1),
('PROJ-2025-002', 'Migración a Cloud AWS', 'Migración de infraestructura on-premise a AWS Cloud', 'planning', '2025-02-01', '2025-08-31', 'critical', 2),
('PROJ-2025-003', 'App Móvil E-commerce', 'Desarrollo de aplicación móvil para plataforma de ventas', 'in_progress', '2025-01-10', '2025-05-15', 'high', 3);

-- ============================================
-- Verificación
-- ============================================
SELECT 'Tablas creadas exitosamente:' as status;
SELECT TABLE_NAME, TABLE_ROWS 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'sb_production' 
AND TABLE_NAME IN ('projects', 'task_dependencies');

SELECT 'Vistas creadas exitosamente:' as status;
SELECT TABLE_NAME 
FROM information_schema.VIEWS 
WHERE TABLE_SCHEMA = 'sb_production' 
AND TABLE_NAME LIKE 'v_%project%' OR TABLE_NAME LIKE 'v_%task%';

SELECT '✅ Script completado' as status;
