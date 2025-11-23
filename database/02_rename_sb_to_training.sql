-- ====================================
-- SCRIPT 2: RENOMBRAR BD ACTUAL A SB_TRAINING
-- ====================================
-- Convierte la base de datos sb existente en sb_training
-- (Base de datos para entrenamiento de modelos ML)
-- Fecha: 2025-11-23
-- ====================================

-- IMPORTANTE: Este script renombra tu BD actual 'sb' a 'sb_training'
-- Ejecuta con PRECAUCIÓN y haz un backup primero

-- ====================================
-- OPCIÓN 1: BACKUP Y RENOMBRADO MANUAL
-- ====================================
-- Desde terminal ejecuta:
-- mysqldump -u root -p sb > sb_backup_$(date +%Y%m%d).sql
-- mysql -u root -p -e "CREATE DATABASE sb_training CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
-- mysql -u root -p sb_training < sb_backup_$(date +%Y%m%d).sql

-- ====================================
-- OPCIÓN 2: RENOMBRADO DIRECTO (MySQL 8.0+)
-- ====================================

-- Crear nueva base de datos para training
CREATE DATABASE IF NOT EXISTS `sb_training`
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Verificar que sb existe
SELECT 'Verificando base de datos sb...' as paso;
SELECT SCHEMA_NAME 
FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE SCHEMA_NAME = 'sb';

-- Obtener lista de todas las tablas en sb
SELECT 'Tablas a mover desde sb a sb_training:' as info;
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'sb'
ORDER BY TABLE_NAME;

-- IMPORTANTE: MySQL no permite RENAME DATABASE directamente
-- Necesitas usar uno de estos métodos:

-- MÉTODO A: Renombrar tabla por tabla (RECOMENDADO para seguridad)
-- Descomenta y ejecuta las siguientes líneas:

-- RENAME TABLE sb.assignees TO sb_training.assignees;
-- RENAME TABLE sb.people TO sb_training.people;
-- RENAME TABLE sb.tasks TO sb_training.tasks;
-- RENAME TABLE sb.task_dependencies TO sb_training.task_dependencies;
-- RENAME TABLE sb.v_people_load TO sb_training.v_people_load;
-- RENAME TABLE sb.v_people_stats TO sb_training.v_people_stats;
-- RENAME TABLE sb.v_person_success TO sb_training.v_person_success;
-- RENAME TABLE sb.v_tasks_stats TO sb_training.v_tasks_stats;
-- RENAME TABLE sb.v_task_metrics TO sb_training.v_task_metrics;
-- RENAME TABLE sb.v_training_dataset TO sb_training.v_training_dataset;
-- RENAME TABLE sb.v_training_dataset_clean TO sb_training.v_training_dataset_clean;

-- Después de mover todas las tablas, eliminar BD vacía
-- DROP DATABASE sb;

-- ====================================
-- MÉTODO B: Script automatizado (ejecutar desde terminal)
-- ====================================

-- Guarda esto en un archivo rename_sb.sh y ejecútalo:
/*
#!/bin/bash
# Backup de seguridad
mysqldump -u root -p sb > sb_backup_$(date +%Y%m%d_%H%M%S).sql

# Crear sb_training
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS sb_training CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

# Obtener todas las tablas y renombrarlas
mysql -u root -p -e "SELECT CONCAT('RENAME TABLE sb.', table_name, ' TO sb_training.', table_name, ';') 
FROM information_schema.tables 
WHERE table_schema='sb'" | grep RENAME | mysql -u root -p

# Verificar
mysql -u root -p -e "SHOW TABLES FROM sb_training;"

# Si todo OK, eliminar sb
mysql -u root -p -e "DROP DATABASE sb;"

echo "✅ Base de datos renombrada exitosamente a sb_training"
*/

-- ====================================
-- MÉTODO C: Dump y restauración (MÁS SEGURO)
-- ====================================

-- Desde terminal PowerShell:
-- 1. Hacer backup de sb
--    mysqldump -u root -p sb > sb_backup.sql

-- 2. Crear sb_training y restaurar
--    mysql -u root -p -e "CREATE DATABASE sb_training CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
--    mysql -u root -p sb_training < sb_backup.sql

-- 3. Verificar que todo está OK
--    mysql -u root -p sb_training -e "SHOW TABLES; SELECT COUNT(*) FROM people; SELECT COUNT(*) FROM tasks;"

-- 4. Si todo OK, renombrar sb a sb_old (por si acaso)
--    mysql -u root -p -e "CREATE DATABASE sb_old CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
--    Mover tablas de sb a sb_old como backup
--    mysql -u root -p -e "DROP DATABASE sb;"

-- ====================================
-- VERIFICACIÓN POST-RENOMBRADO
-- ====================================

-- Verificar que sb_training existe y tiene datos
SELECT 'Verificando sb_training...' as paso;

USE sb_training;

-- Contar registros en tablas principales
SELECT 'Conteo de registros en sb_training:' as info;
SELECT 'people' as tabla, COUNT(*) as total FROM people
UNION ALL
SELECT 'tasks', COUNT(*) FROM tasks
UNION ALL
SELECT 'assignees', COUNT(*) FROM assignees
UNION ALL
SELECT 'task_dependencies', COUNT(*) FROM task_dependencies;

-- Mostrar todas las tablas
SHOW TABLES;

-- Verificar integridad de las vistas
SELECT 'Verificando vistas...' as info;
SELECT TABLE_NAME, TABLE_TYPE 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'sb_training' AND TABLE_TYPE = 'VIEW';

-- ====================================
-- AGREGAR ÍNDICES ADICIONALES (OPCIONAL)
-- ====================================

-- Mejorar rendimiento de consultas para ML
USE sb_training;

-- Índices para people
CREATE INDEX IF NOT EXISTS idx_people_area_performance ON people(area, performance_index);
CREATE INDEX IF NOT EXISTS idx_people_resigned ON people(resigned);

-- Índices para tasks
CREATE INDEX IF NOT EXISTS idx_tasks_duration ON tasks(duration_real, duration_est);
CREATE INDEX IF NOT EXISTS idx_tasks_completion ON tasks(completion);

-- Índices para assignees
CREATE INDEX IF NOT EXISTS idx_assignees_person_task ON assignees(person_id, task_id);

SELECT '✅ Índices adicionales creados en sb_training' as resultado;

-- ====================================
-- RESULTADO FINAL
-- ====================================
SELECT 
    '✅ CONFIGURACIÓN COMPLETA' as estado,
    'sb_production: Base de datos de producción (vacía)' as produccion,
    'sb_training: Base de datos de entrenamiento (con datos históricos)' as training,
    'Ahora puedes usar ambas BDs en Flask con SQLALCHEMY_BINDS' as siguiente_paso;
