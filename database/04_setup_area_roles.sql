-- =====================================================
-- CONFIGURACIÓN DE ROLES CON SUPERVISORES DE ÁREA
-- =====================================================
-- Este script configura los 5 roles del sistema:
-- 1. Super Admin - Acceso total
-- 2. Gerente General - Dashboards ejecutivos, reportes
-- 3. Supervisor General - Supervisión de todas las áreas
-- 4. Colaborador - Solo sus tareas
-- 5. Supervisor de Área - Supervisión de una área específica

USE sb_production;

-- =====================================================
-- 1. VERIFICAR TABLA DE ROLES
-- =====================================================

-- Verificar si la tabla roles existe
SELECT 'Verificando tabla roles...' AS info;

-- Si no existe, crearla
CREATE TABLE IF NOT EXISTS roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. INSERTAR/ACTUALIZAR ROLES
-- =====================================================

-- Limpiar roles existentes (opcional, comentar si no quieres)
-- TRUNCATE TABLE roles;

-- Insertar los 5 roles
INSERT INTO roles (id, name, description, permissions) VALUES
(1, 'Super Admin', 
 'Acceso total al sistema - Configuración, usuarios, todas las funcionalidades',
 JSON_OBJECT(
    'view_all_projects', true,
    'create_projects', true,
    'delete_projects', true,
    'manage_users', true,
    'view_all_areas', true,
    'approve_tasks', true,
    'access_ml_models', true,
    'system_config', true
 ))
ON DUPLICATE KEY UPDATE 
    description = VALUES(description),
    permissions = VALUES(permissions);

INSERT INTO roles (id, name, description, permissions) VALUES
(2, 'Gerente General', 
 'Visión ejecutiva - Dashboards, reportes estratégicos, gestión de proyectos',
 JSON_OBJECT(
    'view_all_projects', true,
    'create_projects', true,
    'delete_projects', false,
    'manage_users', false,
    'view_all_areas', true,
    'approve_tasks', true,
    'access_ml_models', true,
    'system_config', false
 ))
ON DUPLICATE KEY UPDATE 
    description = VALUES(description),
    permissions = VALUES(permissions);

INSERT INTO roles (id, name, description, permissions) VALUES
(3, 'Supervisor General', 
 'Supervisión de todas las áreas - Aprobación de tareas, reportes operativos',
 JSON_OBJECT(
    'view_all_projects', true,
    'create_projects', true,
    'delete_projects', false,
    'manage_users', false,
    'view_all_areas', true,
    'approve_tasks', true,
    'access_ml_models', true,
    'system_config', false
 ))
ON DUPLICATE KEY UPDATE 
    description = VALUES(description),
    permissions = VALUES(permissions);

INSERT INTO roles (id, name, description, permissions) VALUES
(4, 'Colaborador', 
 'Usuario regular - Solo ve y gestiona sus tareas asignadas',
 JSON_OBJECT(
    'view_all_projects', false,
    'create_projects', false,
    'delete_projects', false,
    'manage_users', false,
    'view_all_areas', false,
    'approve_tasks', false,
    'access_ml_models', false,
    'system_config', false
 ))
ON DUPLICATE KEY UPDATE 
    description = VALUES(description),
    permissions = VALUES(permissions);

INSERT INTO roles (id, name, description, permissions) VALUES
(5, 'Supervisor de Área', 
 'Supervisión de una área específica - Solo ve proyectos y tareas de su área asignada',
 JSON_OBJECT(
    'view_all_projects', false,
    'create_projects', true,
    'delete_projects', false,
    'manage_users', false,
    'view_all_areas', false,
    'approve_tasks', true,
    'access_ml_models', true,
    'system_config', false,
    'area_restricted', true
 ))
ON DUPLICATE KEY UPDATE 
    description = VALUES(description),
    permissions = VALUES(permissions);

-- =====================================================
-- 3. VERIFICAR QUE web_users TENGA CAMPO 'area'
-- =====================================================

-- Si no existe el campo area, agregarlo
ALTER TABLE web_users 
ADD COLUMN IF NOT EXISTS area VARCHAR(50) DEFAULT NULL;

-- =====================================================
-- 4. VERIFICAR QUE projects TENGA CAMPO 'area'
-- =====================================================

-- Si no existe el campo area, agregarlo
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS area VARCHAR(50) DEFAULT NULL;

-- Agregar manager_id para asignar responsable del proyecto
ALTER TABLE projects
ADD COLUMN IF NOT EXISTS manager_id INT,
ADD CONSTRAINT fk_project_manager 
    FOREIGN KEY (manager_id) REFERENCES web_users(id) 
    ON DELETE SET NULL;

-- =====================================================
-- 5. ACTUALIZAR USUARIOS DE EJEMPLO (OPCIONAL)
-- =====================================================

-- Ejemplo: Crear supervisor de área IT
-- UPDATE web_users SET role_id = 5, area = 'IT' 
-- WHERE email = 'supervisor.it@processmart.com';

-- Ejemplo: Crear supervisor de área Marketing
-- INSERT INTO web_users (email, password_hash, full_name, role_id, area, status)
-- VALUES ('supervisor.marketing@processmart.com', '$2b$12$...hash...', 'Supervisor Marketing', 5, 'Marketing', 'active');

-- =====================================================
-- 6. CREAR ÍNDICES PARA OPTIMIZAR CONSULTAS
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_users_area ON web_users(area);
CREATE INDEX IF NOT EXISTS idx_users_role ON web_users(role_id);
CREATE INDEX IF NOT EXISTS idx_projects_area ON projects(area);
CREATE INDEX IF NOT EXISTS idx_tasks_area ON web_tasks(area);

-- =====================================================
-- 7. VERIFICAR CONFIGURACIÓN
-- =====================================================

SELECT '===== ROLES CONFIGURADOS =====' AS info;
SELECT * FROM roles ORDER BY id;

SELECT '===== USUARIOS POR ROL =====' AS info;
SELECT 
    r.id as role_id,
    r.name as role_name,
    COUNT(u.id) as user_count
FROM roles r
LEFT JOIN web_users u ON r.id = u.role_id
GROUP BY r.id, r.name
ORDER BY r.id;

SELECT '===== USUARIOS CON ÁREA ASIGNADA =====' AS info;
SELECT 
    id,
    full_name,
    email,
    role_id,
    area,
    status
FROM web_users
ORDER BY role_id, area;

SELECT 'Configuración de roles completada exitosamente ✓' AS resultado;
