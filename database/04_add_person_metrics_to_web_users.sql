-- ====================================
-- SCRIPT 4: AGREGAR MÉTRICAS PROFESIONALES A WEB_USERS
-- ====================================
-- Añade campos de performance y experiencia para mejorar recomendaciones ML
-- ====================================

USE sb_production;

-- Agregar columnas de métricas profesionales
ALTER TABLE web_users
ADD COLUMN experience_years INT DEFAULT 2 COMMENT 'Años de experiencia profesional',
ADD COLUMN performance_index FLOAT DEFAULT 50.0 COMMENT 'Índice de desempeño (0-100)',
ADD COLUMN rework_rate FLOAT DEFAULT 0.10 COMMENT 'Tasa de retrabajo (0-1)',
ADD COLUMN satisfaction_score FLOAT DEFAULT 3.0 COMMENT 'Satisfacción del colaborador (1-5)',
ADD COLUMN current_load INT DEFAULT 0 COMMENT 'Número de tareas activas asignadas',
ADD COLUMN tasks_completed INT DEFAULT 0 COMMENT 'Total de tareas completadas',
ADD COLUMN availability_hours_week FLOAT DEFAULT 40.0 COMMENT 'Horas disponibles por semana';

-- Actualizar valores iniciales para usuarios existentes
UPDATE web_users 
SET 
    experience_years = CASE 
        WHEN email = 'analyst@processmart.com' THEN 5  -- Analista con experiencia
        WHEN email = 'user@processmart.com' THEN 3     -- Usuario intermedio
        WHEN email = 'usuario@processmart.com' THEN 2  -- Usuario junior
        ELSE 2
    END,
    performance_index = CASE 
        WHEN email = 'analyst@processmart.com' THEN 85.0  -- Alto desempeño
        WHEN email = 'user@processmart.com' THEN 75.0     -- Buen desempeño
        WHEN email = 'usuario@processmart.com' THEN 65.0  -- Desempeño promedio
        ELSE 50.0
    END,
    rework_rate = CASE 
        WHEN email = 'analyst@processmart.com' THEN 0.05  -- Bajo retrabajo (5%)
        WHEN email = 'user@processmart.com' THEN 0.08     -- Retrabajo moderado (8%)
        WHEN email = 'usuario@processmart.com' THEN 0.12  -- Retrabajo normal (12%)
        ELSE 0.10
    END,
    satisfaction_score = CASE 
        WHEN email = 'analyst@processmart.com' THEN 4.5
        WHEN email = 'user@processmart.com' THEN 4.0
        WHEN email = 'usuario@processmart.com' THEN 3.5
        ELSE 3.0
    END,
    availability_hours_week = 40.0,
    current_load = 0,
    tasks_completed = CASE 
        WHEN email = 'analyst@processmart.com' THEN 47
        WHEN email = 'user@processmart.com' THEN 32
        WHEN email = 'usuario@processmart.com' THEN 18
        ELSE 0
    END
WHERE role_id = 7;  -- Solo colaboradores

-- Verificar cambios
SELECT 
    id,
    full_name,
    area,
    experience_years,
    performance_index,
    rework_rate,
    satisfaction_score,
    tasks_completed
FROM web_users
WHERE role_id = 7
ORDER BY performance_index DESC;
