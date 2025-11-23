-- ====================================
-- SCRIPT 3: POBLAR COLABORADORES EN PRODUCCIÓN
-- ====================================
-- Copia colaboradores activos de sb_training a sb_production
-- Solo los de mejor desempeño y que no han renunciado
-- Ejecutar DESPUÉS de crear sb_production y sb_training
-- ====================================

USE sb_production;

-- Limpiar tabla people si tiene datos
TRUNCATE TABLE people;

-- Copiar colaboradores activos y de alto rendimiento
-- Filtramos: no renunciados, performance >= 3.5, sin problemas graves
INSERT INTO people (
    person_id, area, role, experience_years, skills, certifications,
    availability_hours_week, current_load, tasks_assigned, performance_index,
    rework_rate, absences, gender, age, hire_date, education_level,
    monthly_salary, overtime_hours, remote_work_frequency, team_size,
    training_hours, promotions, satisfaction_score, resigned
)
SELECT 
    person_id, area, role, experience_years, skills, certifications,
    availability_hours_week, current_load, tasks_assigned, performance_index,
    rework_rate, absences, gender, age, hire_date, education_level,
    monthly_salary, overtime_hours, remote_work_frequency, team_size,
    training_hours, promotions, satisfaction_score, resigned
FROM sb_training.people
WHERE resigned = 0                      -- No renunciados
  AND performance_index >= 3.5          -- Alto rendimiento
  AND (satisfaction_score IS NULL 
       OR satisfaction_score >= 0.6)    -- Satisfechos
  AND (rework_rate IS NULL 
       OR rework_rate < 0.3)            -- Bajo retrabajo
LIMIT 500;                              -- Máximo 500 colaboradores

-- Verificar cuántos se copiaron
SELECT 
    COUNT(*) as total_colaboradores,
    COUNT(DISTINCT area) as areas_con_personal,
    ROUND(AVG(performance_index), 2) as performance_promedio,
    ROUND(AVG(experience_years), 1) as experiencia_promedio
FROM people;

-- Ver distribución por área
SELECT 
    area,
    COUNT(*) as colaboradores,
    ROUND(AVG(performance_index), 2) as avg_performance,
    ROUND(AVG(current_load), 1) as avg_load
FROM people
GROUP BY area
ORDER BY colaboradores DESC;

-- Verificar colaboradores disponibles para asignar
SELECT 
    COUNT(*) as disponibles,
    area
FROM people
WHERE current_load < 40  -- Menos del 40% de carga
  AND performance_index >= 4
GROUP BY area;

SELECT '✅ Colaboradores copiados a sb_production exitosamente' as resultado;
