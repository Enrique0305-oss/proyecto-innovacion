-- ====================================
-- SCRIPT 1: CREAR BASE DE DATOS DE PRODUCCIÓN
-- ====================================
-- Base de datos nueva para el sistema web
-- Se ejecuta en MySQL 8.0+
-- Fecha: 2025-11-23
-- ====================================

CREATE DATABASE IF NOT EXISTS `sb_production` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_0900_ai_ci;

USE sb_production;

-- ====================================
-- SECCIÓN 1: TABLAS DE ESTRUCTURA BASE
-- (Copiadas de sb, sin datos iniciales)
-- ====================================

-- Tabla: Personas/Colaboradores
CREATE TABLE `people` (
  `person_id` VARCHAR(64) NOT NULL,
  `area` VARCHAR(64) DEFAULT NULL,
  `role` VARCHAR(64) DEFAULT NULL,
  `experience_years` DECIMAL(4,1) DEFAULT NULL,
  `skills` JSON DEFAULT NULL,
  `certifications` TEXT,
  `availability_hours_week` DECIMAL(5,2) DEFAULT NULL,
  `current_load` DECIMAL(5,2) DEFAULT NULL,
  `tasks_assigned` INT DEFAULT NULL,
  `performance_index` DECIMAL(5,2) DEFAULT NULL,
  `rework_rate` DECIMAL(5,2) DEFAULT NULL,
  `absences` INT DEFAULT NULL,
  `gender` VARCHAR(20) DEFAULT NULL COMMENT 'Género del empleado',
  `age` INT DEFAULT NULL COMMENT 'Edad del empleado',
  `hire_date` DATE DEFAULT NULL COMMENT 'Fecha de contratación',
  `education_level` VARCHAR(50) DEFAULT NULL COMMENT 'Nivel educativo',
  `monthly_salary` DECIMAL(10,2) DEFAULT NULL COMMENT 'Salario mensual',
  `overtime_hours` INT DEFAULT NULL COMMENT 'Horas extra trabajadas',
  `remote_work_frequency` INT DEFAULT NULL COMMENT 'Frecuencia de trabajo remoto (%)',
  `team_size` INT DEFAULT NULL COMMENT 'Tamaño del equipo',
  `training_hours` INT DEFAULT NULL COMMENT 'Horas de capacitación',
  `promotions` INT DEFAULT NULL COMMENT 'Número de promociones',
  `satisfaction_score` DECIMAL(3,2) DEFAULT NULL COMMENT 'Índice de satisfacción del empleado',
  `resigned` TINYINT(1) DEFAULT 0 COMMENT 'Si el empleado renunció',
  PRIMARY KEY (`person_id`),
  INDEX idx_area (area),
  INDEX idx_performance (performance_index),
  INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Colaboradores del sistema - estructura copiada de sb_training';

-- Tabla: Tareas históricas
CREATE TABLE `tasks` (
  `task_id` VARCHAR(64) NOT NULL,
  `project_id` VARCHAR(64) DEFAULT NULL,
  `area` VARCHAR(100) DEFAULT NULL,
  `task_name` VARCHAR(255) DEFAULT NULL,
  `task_type` VARCHAR(200) DEFAULT NULL,
  `start_date_est` DATE DEFAULT NULL,
  `end_date_est` DATE DEFAULT NULL,
  `start_date_real` DATE DEFAULT NULL,
  `end_date_real` DATE DEFAULT NULL,
  `duration_est` DECIMAL(10,2) DEFAULT NULL,
  `duration_real` DECIMAL(10,2) DEFAULT NULL,
  `status` VARCHAR(100) DEFAULT NULL,
  `priority` VARCHAR(100) DEFAULT NULL,
  `dependencies` TEXT,
  `complexity_level` VARCHAR(100) DEFAULT NULL,
  `tools_used` TEXT,
  `completion` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  INDEX idx_area (area),
  INDEX idx_status (status),
  INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Tareas históricas - estructura copiada de sb_training';

-- Tabla: Asignaciones persona-tarea
CREATE TABLE `assignees` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `task_id` VARCHAR(64) DEFAULT NULL,
  `person_id` VARCHAR(64) DEFAULT NULL,
  `assigned_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX idx_task (task_id),
  INDEX idx_person (person_id),
  INDEX idx_assigned_at (assigned_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Relación muchos a muchos: tareas-personas';

-- Tabla: Dependencias entre tareas
CREATE TABLE `task_dependencies` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `task_id` VARCHAR(64) DEFAULT NULL,
  `depends_on_task_id` VARCHAR(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX idx_task (task_id),
  INDEX idx_depends (depends_on_task_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Dependencias entre tareas para process mining';

-- ====================================
-- SECCIÓN 2: TABLAS DEL SISTEMA WEB
-- ====================================

-- Tabla: Roles del sistema
CREATE TABLE `roles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) UNIQUE NOT NULL COMMENT 'admin, supervisor, analyst, user',
  `display_name` VARCHAR(100) NOT NULL COMMENT 'Nombre para mostrar en UI',
  `description` TEXT,
  `permissions` JSON DEFAULT NULL COMMENT 'Permisos del rol en formato JSON',
  `level` INT DEFAULT 1 COMMENT 'Nivel jerárquico (admin=4, supervisor=3, analyst=2, user=1)',
  `status` ENUM('active', 'inactive') DEFAULT 'active',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_level (level),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Roles y permisos del sistema';

-- Tabla: Áreas/Departamentos
CREATE TABLE `areas` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) UNIQUE NOT NULL,
  `description` TEXT,
  `supervisor_person_id` VARCHAR(64) DEFAULT NULL COMMENT 'ID del supervisor (referencia a people)',
  `employee_count` INT DEFAULT 0,
  `efficiency_score` DECIMAL(5,2) DEFAULT NULL COMMENT 'Puntuación de eficiencia (0-100)',
  `status` ENUM('active', 'inactive') DEFAULT 'active',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_status (status),
  INDEX idx_supervisor (supervisor_person_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Áreas/Departamentos de la organización';

-- Tabla: Usuarios del sistema web
CREATE TABLE `web_users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(100) UNIQUE NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(150),
  `role_id` INT NOT NULL COMMENT 'FK a tabla roles',
  `area` VARCHAR(100) DEFAULT NULL,
  `person_id` VARCHAR(64) DEFAULT NULL COMMENT 'Relación opcional con people',
  `status` ENUM('active', 'inactive') DEFAULT 'active',
  `avatar_url` VARCHAR(255) DEFAULT NULL,
  `last_login` TIMESTAMP NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT,
  INDEX idx_email (email),
  INDEX idx_role_id (role_id),
  INDEX idx_status (status),
  INDEX idx_area (area)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Usuarios administradores/analistas del sistema web';

-- Tabla: Tareas web (creadas desde la interfaz)
CREATE TABLE `web_tasks` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(200) NOT NULL,
  `description` TEXT,
  `priority` ENUM('alta', 'media', 'baja') DEFAULT 'media',
  `status` ENUM('pendiente', 'en_progreso', 'completada', 'retrasada', 'cancelada') DEFAULT 'pendiente',
  `area` VARCHAR(100) DEFAULT NULL,
  `assigned_to` VARCHAR(64) DEFAULT NULL COMMENT 'person_id del colaborador asignado',
  `complexity_score` INT CHECK (complexity_score BETWEEN 1 AND 10),
  `estimated_hours` DECIMAL(10,2) DEFAULT NULL,
  `actual_hours` DECIMAL(10,2) NULL,
  `deadline` DATETIME DEFAULT NULL,
  `start_date` DATETIME NULL,
  `completed_at` DATETIME NULL,
  `created_by` INT DEFAULT NULL COMMENT 'web_users.id del creador',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES web_users(id) ON DELETE SET NULL,
  INDEX idx_status (status),
  INDEX idx_area (area),
  INDEX idx_assigned (assigned_to),
  INDEX idx_priority (priority),
  INDEX idx_deadline (deadline),
  INDEX idx_created_by (created_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Tareas operacionales creadas desde el sistema web';

-- ====================================
-- SECCIÓN 3: TABLAS MACHINE LEARNING
-- ====================================

-- Tabla: Modelos ML registrados
CREATE TABLE `ml_models` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `type` ENUM('risk', 'duration', 'recommendation', 'performance', 'simulation') NOT NULL,
  `algorithm` VARCHAR(50) DEFAULT NULL COMMENT 'Random Forest, XGBoost, LSTM, etc.',
  `version` VARCHAR(20) DEFAULT 'v1.0',
  `precision` DECIMAL(5,2) DEFAULT NULL COMMENT 'Accuracy/Precisión del modelo (%)',
  `recall_score` DECIMAL(5,2) DEFAULT NULL COMMENT 'Recall/Exhaustividad',
  `f1_score` DECIMAL(5,2) DEFAULT NULL COMMENT 'F1 Score',
  `mae` DECIMAL(10,2) DEFAULT NULL COMMENT 'Mean Absolute Error',
  `rmse` DECIMAL(10,2) DEFAULT NULL COMMENT 'Root Mean Squared Error',
  `r2_score` DECIMAL(5,4) DEFAULT NULL COMMENT 'R² Score (regresión)',
  `status` ENUM('activo', 'entrenando', 'error', 'deprecated') DEFAULT 'activo',
  `model_path` VARCHAR(255) NOT NULL COMMENT 'Ruta al archivo .pkl',
  `samples_count` INT DEFAULT NULL COMMENT 'Cantidad de muestras usadas para entrenar',
  `features_used` JSON DEFAULT NULL COMMENT 'Lista de features usadas',
  `hyperparameters` JSON DEFAULT NULL COMMENT 'Hiperparámetros del modelo',
  `metrics` JSON DEFAULT NULL COMMENT 'Métricas adicionales en formato JSON',
  `description` TEXT COMMENT 'Descripción del modelo',
  `last_trained` TIMESTAMP NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_type (type),
  INDEX idx_status (status),
  INDEX idx_version (version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Registro de modelos ML con metadata y métricas';

-- Tabla: Predicciones generadas por los modelos
CREATE TABLE `ml_predictions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `task_reference` VARCHAR(100) NOT NULL COMMENT 'ID de la tarea (task_id o web_tasks.id)',
  `task_source` ENUM('historical', 'web') DEFAULT 'web',
  `model_id` INT DEFAULT NULL COMMENT 'Referencia al modelo usado',
  `model_type` ENUM('risk', 'duration', 'recommendation', 'performance', 'simulation') NOT NULL,
  `prediction_value` JSON NOT NULL COMMENT 'Resultado de la predicción',
  `confidence` DECIMAL(5,2) DEFAULT NULL COMMENT 'Confianza de la predicción (0-1)',
  `input_features` JSON DEFAULT NULL COMMENT 'Features usadas para la predicción',
  `actual_result` JSON DEFAULT NULL COMMENT 'Resultado real (se llena después)',
  `is_correct` BOOLEAN DEFAULT NULL COMMENT 'Si la predicción fue correcta',
  `model_version` VARCHAR(50) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (model_id) REFERENCES ml_models(id) ON DELETE SET NULL,
  INDEX idx_task (task_reference, task_source),
  INDEX idx_model_type (model_type),
  INDEX idx_model_id (model_id),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Predicciones ML con auditoría completa';

-- Tabla: Datasets subidos
CREATE TABLE `ml_datasets` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `filename` VARCHAR(255) NOT NULL,
  `original_name` VARCHAR(255) NOT NULL,
  `file_path` VARCHAR(255) NOT NULL,
  `file_type` VARCHAR(20) DEFAULT 'csv' COMMENT 'csv, excel, json',
  `file_size_bytes` BIGINT DEFAULT NULL,
  `record_count` INT DEFAULT NULL,
  `columns_count` INT DEFAULT NULL,
  `columns_info` JSON DEFAULT NULL COMMENT 'Metadata de las columnas',
  `data_preview` JSON DEFAULT NULL COMMENT 'Primeras 5 filas como preview',
  `status` ENUM('uploaded', 'processing', 'processed', 'error', 'archived') DEFAULT 'uploaded',
  `processing_log` TEXT COMMENT 'Log del procesamiento',
  `uploaded_by` INT DEFAULT NULL,
  `uploaded_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `processed_at` TIMESTAMP NULL,
  FOREIGN KEY (uploaded_by) REFERENCES web_users(id) ON DELETE SET NULL,
  INDEX idx_status (status),
  INDEX idx_uploaded_by (uploaded_by),
  INDEX idx_uploaded_at (uploaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Datasets subidos para entrenar/validar modelos';

-- Tabla: Jobs de entrenamiento
CREATE TABLE `ml_training_jobs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `model_id` INT DEFAULT NULL,
  `dataset_id` INT DEFAULT NULL,
  `job_name` VARCHAR(150) DEFAULT NULL,
  `status` ENUM('pending', 'running', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
  `progress` INT DEFAULT 0 COMMENT 'Progreso 0-100',
  `current_step` VARCHAR(100) DEFAULT NULL COMMENT 'Paso actual del entrenamiento',
  `config` JSON DEFAULT NULL COMMENT 'Configuración del entrenamiento',
  `started_at` TIMESTAMP NULL,
  `completed_at` TIMESTAMP NULL,
  `duration_seconds` INT DEFAULT NULL,
  `metrics` JSON DEFAULT NULL COMMENT 'Métricas resultantes del entrenamiento',
  `error_message` TEXT,
  `output_model_path` VARCHAR(255) DEFAULT NULL COMMENT 'Ruta del modelo generado',
  `created_by` INT DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (model_id) REFERENCES ml_models(id) ON DELETE CASCADE,
  FOREIGN KEY (dataset_id) REFERENCES ml_datasets(id) ON DELETE SET NULL,
  FOREIGN KEY (created_by) REFERENCES web_users(id) ON DELETE SET NULL,
  INDEX idx_status (status),
  INDEX idx_model_id (model_id),
  INDEX idx_dataset_id (dataset_id),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
COMMENT='Historial de trabajos de entrenamiento de modelos';

-- ====================================
-- SECCIÓN 4: DATOS INICIALES
-- ====================================

-- Insertar roles del sistema
INSERT INTO `roles` (name, display_name, description, permissions, level, status) VALUES
('admin', 'Administrador', 'Acceso total al sistema, gestión de usuarios y configuración', 
  JSON_ARRAY('users.create', 'users.edit', 'users.delete', 'ml.manage', 'ml.train', 'ml.delete', 'tasks.all', 'reports.all', 'settings.manage'), 
  3, 'active'),
('supervisor', 'Supervisor', 'Supervisión de áreas, aprobación de tareas y reportes avanzados',
  JSON_ARRAY('tasks.create', 'tasks.edit', 'tasks.assign', 'tasks.approve', 'reports.view', 'ml.view', 'users.view'),
  2, 'active'),
('analyst', 'Analista', 'Análisis de datos, visualización de métricas y predicciones ML',
  JSON_ARRAY('tasks.view', 'tasks.create', 'ml.predict', 'reports.view', 'dashboard.view'),
  1, 'active'),
('user', 'Usuario', 'Usuario básico con acceso limitado',
  JSON_ARRAY('tasks.view', 'dashboard.view'),
  0, 'active');

-- Insertar áreas base
INSERT INTO `areas` (name, description, employee_count, status) VALUES
('IT', 'Tecnología de la Información', 0, 'active'),
('Engineering', 'Ingeniería', 0, 'active'),
('Customer Support', 'Soporte al Cliente', 0, 'active'),
('HR', 'Recursos Humanos', 0, 'active'),
('Finance', 'Finanzas', 0, 'active'),
('Marketing', 'Marketing', 0, 'active'),
('Sales', 'Ventas', 0, 'active'),
('Operations', 'Operaciones', 0, 'active');

-- Usuarios iniciales (password: admin123 - CAMBIAR EN PRODUCCIÓN)
-- Hash bcrypt generado: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zq.a06VMl6u6
INSERT INTO `web_users` (email, password_hash, full_name, role_id, area, status) VALUES
('admin@processmart.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zq.a06VMl6u6', 'Administrador Sistema', 1, 'IT', 'active'),
('supervisor@processmart.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zq.a06VMl6u6', 'Supervisor General', 2, 'Operations', 'active'),
('analyst@processmart.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zq.a06VMl6u6', 'Analista Demo', 3, 'Engineering', 'active'),
('user@processmart.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zq.a06VMl6u6', 'Usuario Demo', 4, 'IT', 'active');

-- Modelos ML iniciales (actualizarás después del entrenamiento real)
INSERT INTO `ml_models` (name, type, algorithm, version, `precision`, samples_count, status, model_path, last_trained, description) VALUES
('Clasificación de Riesgo', 'risk', 'Random Forest', 'v1.0', 94.00, 1250, 'activo', 'models/risk_classifier_v1.pkl', NOW(), 'Predice riesgo de retraso en tareas basado en complejidad y recursos'),
('Predicción de Duración', 'duration', 'CatBoost', 'v1.0', 92.00, 980, 'activo', 'models/duration_predictor_v1.pkl', NOW(), 'Estima duración de tareas considerando histórico y features'),
('Recomendación Persona-Tarea', 'recommendation', 'Collaborative Filtering', 'v1.0', 89.00, 2100, 'activo', 'models/recommendation_model_v1.pkl', NOW(), 'Sugiere mejor persona para asignar según skills y disponibilidad'),
('Desempeño Colaborador', 'performance', 'XGBoost', 'v1.0', 91.00, 756, 'activo', 'models/performance_model_v1.pkl', NOW(), 'Evalúa desempeño de colaboradores basado en métricas históricas'),
('Simulación de Flujo', 'simulation', 'LSTM', 'v1.0', 88.00, 1450, 'entrenando', 'models/flow_simulator_v1.pkl', NOW(), 'Simula flujos de proceso usando redes neuronales recurrentes');

-- ====================================
-- SECCIÓN 5: VISTAS PARA ANALYTICS
-- ====================================

-- Vista: Métricas por área
CREATE OR REPLACE VIEW v_area_metrics AS
SELECT 
    a.id as area_id,
    a.name as area_name,
    a.employee_count,
    a.efficiency_score,
    COUNT(DISTINCT wt.id) as total_tasks,
    COUNT(DISTINCT CASE WHEN wt.status = 'completada' THEN wt.id END) as completed_tasks,
    COUNT(DISTINCT CASE WHEN wt.status = 'retrasada' THEN wt.id END) as delayed_tasks,
    COUNT(DISTINCT CASE WHEN wt.status = 'en_progreso' THEN wt.id END) as in_progress_tasks,
    AVG(CASE WHEN wt.actual_hours IS NOT NULL THEN wt.actual_hours END) as avg_task_hours,
    AVG(CASE WHEN wt.actual_hours IS NOT NULL AND wt.estimated_hours IS NOT NULL 
        THEN (wt.actual_hours / NULLIF(wt.estimated_hours, 0)) * 100 END) as avg_estimation_accuracy
FROM areas a
LEFT JOIN web_tasks wt ON a.name = wt.area
GROUP BY a.id, a.name, a.employee_count, a.efficiency_score;

-- Vista: Top colaboradores por performance
CREATE OR REPLACE VIEW v_top_performers AS
SELECT 
    p.person_id,
    p.area,
    p.role,
    p.performance_index,
    p.experience_years,
    COUNT(a.task_id) as total_tasks_historical,
    COUNT(CASE WHEN t.status = 'Completed' THEN 1 END) as completed_tasks,
    p.satisfaction_score,
    p.rework_rate,
    p.current_load
FROM people p
LEFT JOIN assignees a ON p.person_id = a.person_id
LEFT JOIN tasks t ON a.task_id = t.task_id
WHERE p.performance_index >= 4 AND p.resigned = 0
GROUP BY p.person_id, p.area, p.role, p.performance_index, p.experience_years, p.satisfaction_score, p.rework_rate, p.current_load
ORDER BY p.performance_index DESC, completed_tasks DESC
LIMIT 10;

-- Vista: Tareas con retraso
CREATE OR REPLACE VIEW v_delayed_tasks AS
SELECT 
    wt.id,
    wt.title,
    wt.area,
    wt.priority,
    wt.complexity_score,
    wt.estimated_hours,
    wt.actual_hours,
    wt.deadline,
    wt.assigned_to,
    CASE 
        WHEN wt.actual_hours IS NOT NULL AND wt.estimated_hours IS NOT NULL 
        THEN (wt.actual_hours - wt.estimated_hours)
        WHEN wt.deadline < NOW() AND wt.status != 'completada' 
        THEN TIMESTAMPDIFF(HOUR, wt.deadline, NOW())
        ELSE NULL
    END as delay_hours,
    wt.status
FROM web_tasks wt
WHERE (wt.actual_hours > wt.estimated_hours) 
   OR (wt.deadline < NOW() AND wt.status NOT IN ('completada', 'cancelada'))
ORDER BY delay_hours DESC;

-- Vista: Accuracy de predicciones ML
CREATE OR REPLACE VIEW v_ml_prediction_accuracy AS
SELECT 
    mp.model_type,
    m.name as model_name,
    m.version,
    COUNT(*) as total_predictions,
    SUM(CASE WHEN mp.is_correct = 1 THEN 1 ELSE 0 END) as correct_predictions,
    (SUM(CASE WHEN mp.is_correct = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100 as accuracy_percentage,
    AVG(mp.confidence) as avg_confidence,
    DATE(mp.created_at) as prediction_date
FROM ml_predictions mp
LEFT JOIN ml_models m ON mp.model_id = m.id
WHERE mp.actual_result IS NOT NULL
GROUP BY mp.model_type, m.name, m.version, DATE(mp.created_at)
ORDER BY prediction_date DESC;

-- Vista: Estado de entrenamientos
CREATE OR REPLACE VIEW v_training_status AS
SELECT 
    tj.id as job_id,
    tj.job_name,
    m.name as model_name,
    m.type as model_type,
    d.filename as dataset_filename,
    tj.status,
    tj.progress,
    tj.current_step,
    tj.started_at,
    tj.completed_at,
    tj.duration_seconds,
    u.full_name as created_by_user
FROM ml_training_jobs tj
LEFT JOIN ml_models m ON tj.model_id = m.id
LEFT JOIN ml_datasets d ON tj.dataset_id = d.id
LEFT JOIN web_users u ON tj.created_by = u.id
ORDER BY tj.created_at DESC;

-- ====================================
-- SECCIÓN 6: TRIGGERS PARA AUDITORÍA
-- ====================================

-- Trigger: Actualizar timestamp de última actualización en areas
DELIMITER //
CREATE TRIGGER tr_areas_update_timestamp
BEFORE UPDATE ON areas
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- Trigger: Calcular duración de training job al completarse
DELIMITER //
CREATE TRIGGER tr_training_job_duration
BEFORE UPDATE ON ml_training_jobs
FOR EACH ROW
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        SET NEW.duration_seconds = TIMESTAMPDIFF(SECOND, NEW.started_at, NEW.completed_at);
    END IF;
END//
DELIMITER ;

-- ====================================
-- VERIFICACIÓN FINAL
-- ====================================

-- Mostrar todas las tablas creadas
SELECT 'Tablas creadas exitosamente en sb_production:' as mensaje;
SHOW TABLES;

-- Contar registros iniciales
SELECT 'roles' as tabla, COUNT(*) as registros FROM roles
UNION ALL
SELECT 'areas', COUNT(*) FROM areas
UNION ALL
SELECT 'web_users', COUNT(*) FROM web_users
UNION ALL
SELECT 'ml_models', COUNT(*) FROM ml_models
UNION ALL
SELECT 'people', COUNT(*) FROM people
UNION ALL
SELECT 'tasks', COUNT(*) FROM tasks
UNION ALL
SELECT 'assignees', COUNT(*) FROM assignees;

-- Mostrar vistas creadas
SELECT 'Vistas creadas:' as mensaje;
SHOW FULL TABLES WHERE Table_type = 'VIEW';

SELECT '✅ Base de datos sb_production creada exitosamente' as resultado;
