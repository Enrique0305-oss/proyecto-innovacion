-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 15-12-2025 a las 01:09:42
-- Versión del servidor: 8.0.44
-- Versión de PHP: 8.4.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sb_production`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas`
--

CREATE TABLE `areas` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text,
  `supervisor_person_id` varchar(64) DEFAULT NULL COMMENT 'ID del supervisor (referencia a people)',
  `employee_count` int DEFAULT '0',
  `efficiency_score` decimal(5,2) DEFAULT NULL COMMENT 'Puntuación de eficiencia (0-100)',
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Áreas/Departamentos de la organización';

--
-- Volcado de datos para la tabla `areas`
--

INSERT INTO `areas` (`id`, `name`, `description`, `supervisor_person_id`, `employee_count`, `efficiency_score`, `status`, `created_at`, `updated_at`) VALUES
(1, 'IT', 'Tecnología de la Información', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(2, 'Engineering', 'Ingeniería', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(3, 'Customer Support', 'Soporte al Cliente', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(4, 'HR', 'Recursos Humanos', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(5, 'Finance', 'Finanzas', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(6, 'Marketing', 'Marketing', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(7, 'Sales', 'Ventas', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(8, 'Operations', 'Operaciones', NULL, 0, NULL, 'active', '2025-11-23 05:37:44', '2025-11-23 05:37:44');

--
-- Disparadores `areas`
--
DELIMITER $$
CREATE TRIGGER `tr_areas_update_timestamp` BEFORE UPDATE ON `areas` FOR EACH ROW BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `assignees`
--

CREATE TABLE `assignees` (
  `id` bigint NOT NULL,
  `task_id` varchar(64) DEFAULT NULL,
  `person_id` varchar(64) DEFAULT NULL,
  `assigned_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Relación muchos a muchos: tareas-personas';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ml_datasets`
--

CREATE TABLE `ml_datasets` (
  `id` int NOT NULL,
  `filename` varchar(255) NOT NULL,
  `original_name` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `file_type` varchar(20) DEFAULT 'csv' COMMENT 'csv, excel, json',
  `file_size_bytes` bigint DEFAULT NULL,
  `record_count` int DEFAULT NULL,
  `columns_count` int DEFAULT NULL,
  `columns_info` json DEFAULT NULL COMMENT 'Metadata de las columnas',
  `data_preview` json DEFAULT NULL COMMENT 'Primeras 5 filas como preview',
  `status` enum('uploaded','processing','processed','error','archived') DEFAULT 'uploaded',
  `processing_log` text COMMENT 'Log del procesamiento',
  `uploaded_by` int DEFAULT NULL,
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `processed_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Datasets subidos para entrenar/validar modelos';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ml_models`
--

CREATE TABLE `ml_models` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('risk','duration','recommendation','performance','simulation') NOT NULL,
  `algorithm` varchar(50) DEFAULT NULL COMMENT 'Random Forest, XGBoost, LSTM, etc.',
  `version` varchar(20) DEFAULT 'v1.0',
  `precision` decimal(5,2) DEFAULT NULL COMMENT 'Accuracy/Precisión del modelo (%)',
  `recall_score` decimal(5,2) DEFAULT NULL COMMENT 'Recall/Exhaustividad',
  `f1_score` decimal(5,2) DEFAULT NULL COMMENT 'F1 Score',
  `mae` decimal(10,2) DEFAULT NULL COMMENT 'Mean Absolute Error',
  `rmse` decimal(10,2) DEFAULT NULL COMMENT 'Root Mean Squared Error',
  `r2_score` decimal(5,4) DEFAULT NULL COMMENT 'R² Score (regresión)',
  `status` enum('activo','entrenando','error','deprecated') DEFAULT 'activo',
  `model_path` varchar(255) NOT NULL COMMENT 'Ruta al archivo .pkl',
  `samples_count` int DEFAULT NULL COMMENT 'Cantidad de muestras usadas para entrenar',
  `features_used` json DEFAULT NULL COMMENT 'Lista de features usadas',
  `hyperparameters` json DEFAULT NULL COMMENT 'Hiperparámetros del modelo',
  `metrics` json DEFAULT NULL COMMENT 'Métricas adicionales en formato JSON',
  `description` text COMMENT 'Descripción del modelo',
  `last_trained` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Registro de modelos ML con metadata y métricas';

--
-- Volcado de datos para la tabla `ml_models`
--

INSERT INTO `ml_models` (`id`, `name`, `type`, `algorithm`, `version`, `precision`, `recall_score`, `f1_score`, `mae`, `rmse`, `r2_score`, `status`, `model_path`, `samples_count`, `features_used`, `hyperparameters`, `metrics`, `description`, `last_trained`, `created_at`, `updated_at`) VALUES
(1, 'Clasificación de Riesgo', 'risk', 'Random Forest', 'v1.0', 94.00, NULL, NULL, NULL, NULL, NULL, 'activo', 'models/risk_classifier_v1.pkl', 1250, NULL, NULL, NULL, 'Predice riesgo de retraso en tareas basado en complejidad y recursos', '2025-11-23 05:37:44', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(2, 'Predicción de Duración', 'duration', 'CatBoost', 'v1.0', 92.00, NULL, NULL, NULL, NULL, NULL, 'activo', 'models/duration_predictor_v1.pkl', 980, NULL, NULL, NULL, 'Estima duración de tareas considerando histórico y features', '2025-11-23 05:37:44', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(3, 'Recomendación Persona-Tarea', 'recommendation', 'Collaborative Filtering', 'v1.0', 89.00, NULL, NULL, NULL, NULL, NULL, 'activo', 'models/recommendation_model_v1.pkl', 2100, NULL, NULL, NULL, 'Sugiere mejor persona para asignar según skills y disponibilidad', '2025-11-23 05:37:44', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(4, 'Desempeño Colaborador', 'performance', 'XGBoost', 'v1.0', 91.00, NULL, NULL, NULL, NULL, NULL, 'activo', 'models/performance_model_v1.pkl', 756, NULL, NULL, NULL, 'Evalúa desempeño de colaboradores basado en métricas históricas', '2025-11-23 05:37:44', '2025-11-23 05:37:44', '2025-11-23 05:37:44'),
(5, 'Simulación de Flujo', 'simulation', 'LSTM', 'v1.0', 88.00, NULL, NULL, NULL, NULL, NULL, 'entrenando', 'models/flow_simulator_v1.pkl', 1450, NULL, NULL, NULL, 'Simula flujos de proceso usando redes neuronales recurrentes', '2025-11-23 05:37:44', '2025-11-23 05:37:44', '2025-11-23 05:37:44');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ml_predictions`
--

CREATE TABLE `ml_predictions` (
  `id` int NOT NULL,
  `task_reference` varchar(100) NOT NULL COMMENT 'ID de la tarea (task_id o web_tasks.id)',
  `task_source` enum('historical','web') DEFAULT 'web',
  `model_id` int DEFAULT NULL COMMENT 'Referencia al modelo usado',
  `model_type` enum('risk','duration','recommendation','performance','simulation') NOT NULL,
  `prediction_value` json NOT NULL COMMENT 'Resultado de la predicción',
  `confidence` decimal(5,2) DEFAULT NULL COMMENT 'Confianza de la predicción (0-1)',
  `input_features` json DEFAULT NULL COMMENT 'Features usadas para la predicción',
  `actual_result` json DEFAULT NULL COMMENT 'Resultado real (se llena después)',
  `is_correct` tinyint(1) DEFAULT NULL COMMENT 'Si la predicción fue correcta',
  `model_version` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Predicciones ML con auditoría completa';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ml_training_jobs`
--

CREATE TABLE `ml_training_jobs` (
  `id` int NOT NULL,
  `model_id` int DEFAULT NULL,
  `dataset_id` int DEFAULT NULL,
  `job_name` varchar(150) DEFAULT NULL,
  `status` enum('pending','running','completed','failed','cancelled') DEFAULT 'pending',
  `progress` int DEFAULT '0' COMMENT 'Progreso 0-100',
  `current_step` varchar(100) DEFAULT NULL COMMENT 'Paso actual del entrenamiento',
  `config` json DEFAULT NULL COMMENT 'Configuración del entrenamiento',
  `started_at` timestamp NULL DEFAULT NULL,
  `completed_at` timestamp NULL DEFAULT NULL,
  `duration_seconds` int DEFAULT NULL,
  `metrics` json DEFAULT NULL COMMENT 'Métricas resultantes del entrenamiento',
  `error_message` text,
  `output_model_path` varchar(255) DEFAULT NULL COMMENT 'Ruta del modelo generado',
  `created_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Historial de trabajos de entrenamiento de modelos';

--
-- Disparadores `ml_training_jobs`
--
DELIMITER $$
CREATE TRIGGER `tr_training_job_duration` BEFORE UPDATE ON `ml_training_jobs` FOR EACH ROW BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        SET NEW.duration_seconds = TIMESTAMPDIFF(SECOND, NEW.started_at, NEW.completed_at);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `people`
--

CREATE TABLE `people` (
  `person_id` varchar(64) NOT NULL,
  `area` varchar(64) DEFAULT NULL,
  `role` varchar(64) DEFAULT NULL,
  `experience_years` decimal(4,1) DEFAULT NULL,
  `skills` json DEFAULT NULL,
  `certifications` text,
  `availability_hours_week` decimal(5,2) DEFAULT NULL,
  `current_load` decimal(5,2) DEFAULT NULL,
  `tasks_assigned` int DEFAULT NULL,
  `performance_index` decimal(5,2) DEFAULT NULL,
  `rework_rate` decimal(5,2) DEFAULT NULL,
  `absences` int DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL COMMENT 'Género del empleado',
  `age` int DEFAULT NULL COMMENT 'Edad del empleado',
  `hire_date` date DEFAULT NULL COMMENT 'Fecha de contratación',
  `education_level` varchar(50) DEFAULT NULL COMMENT 'Nivel educativo',
  `monthly_salary` decimal(10,2) DEFAULT NULL COMMENT 'Salario mensual',
  `overtime_hours` int DEFAULT NULL COMMENT 'Horas extra trabajadas',
  `remote_work_frequency` int DEFAULT NULL COMMENT 'Frecuencia de trabajo remoto (%)',
  `team_size` int DEFAULT NULL COMMENT 'Tamaño del equipo',
  `training_hours` int DEFAULT NULL COMMENT 'Horas de capacitación',
  `promotions` int DEFAULT NULL COMMENT 'Número de promociones',
  `satisfaction_score` decimal(3,2) DEFAULT NULL COMMENT 'Índice de satisfacción del empleado',
  `resigned` tinyint(1) DEFAULT '0' COMMENT 'Si el empleado renunció'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Colaboradores del sistema - estructura copiada de sb_training';

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `projects`
--

CREATE TABLE `projects` (
  `project_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `start_date` date DEFAULT NULL,
  `expected_end_date` date DEFAULT NULL,
  `actual_end_date` date DEFAULT NULL,
  `status` enum('planning','in_progress','completed','on_hold','cancelled') COLLATE utf8mb4_unicode_ci DEFAULT 'planning',
  `budget` decimal(15,2) DEFAULT NULL,
  `priority` enum('low','medium','high','critical') COLLATE utf8mb4_unicode_ci DEFAULT 'medium',
  `manager_id` int DEFAULT NULL,
  `progress_percentage` decimal(5,2) DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `area_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `projects`
--

INSERT INTO `projects` (`project_id`, `name`, `description`, `start_date`, `expected_end_date`, `actual_end_date`, `status`, `budget`, `priority`, `manager_id`, `progress_percentage`, `created_at`, `updated_at`, `area_id`) VALUES
('PROJ-2025-001', 'Implementación Sistema CRM', 'Desarrollo e implementación del nuevo sistema CRM para gestión de clientes', '2025-01-15', '2025-06-30', NULL, 'in_progress', NULL, 'high', 1, 0.00, '2025-12-11 17:02:11', '2025-12-14 20:24:26', 1),
('PROJ-2025-002', 'Migración a Cloud AWS', 'Migración de infraestructura on-premise a AWS Cloud', '2025-02-01', '2025-08-31', NULL, 'planning', NULL, 'critical', 2, 0.00, '2025-12-11 17:02:11', '2025-12-14 20:24:26', 8),
('PROJ-2025-003', 'App Móvil E-commerce', 'Desarrollo de aplicación móvil para plataforma de ventas', '2025-01-10', '2025-05-15', NULL, 'in_progress', NULL, 'high', 1, 0.00, '2025-12-11 17:02:11', '2025-12-14 20:24:26', 7),
('PROJ-2025-734', 'Creacion del CRM', 'Implementar un CRM en la empresa', '2025-12-11', '2026-01-01', NULL, 'planning', NULL, 'medium', 2, 0.00, '2025-12-11 23:58:35', '2025-12-14 20:24:26', 1),
('PROJ-DEFAULT', 'Tareas sin proyecto asignado', 'Proyecto contenedor para tareas creadas antes de implementar la gestión de proyectos', '2025-12-11', NULL, NULL, 'in_progress', NULL, 'medium', 1, 0.00, '2025-12-11 17:02:11', '2025-12-14 20:24:26', 1),
('PROJ-TEST-001', 'Proyecto de Prueba', 'Proyecto creado desde test', '2025-12-15', '2026-06-15', NULL, 'planning', NULL, 'medium', 2, 0.00, '2025-12-11 22:19:34', '2025-12-14 20:24:26', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL COMMENT 'admin, supervisor, analyst, user',
  `display_name` varchar(100) NOT NULL COMMENT 'Nombre para mostrar en UI',
  `description` text,
  `permissions` json DEFAULT NULL COMMENT 'Permisos del rol en formato JSON',
  `level` int DEFAULT '1' COMMENT 'Nivel jerárquico (admin=4, supervisor=3, analyst=2, user=1)',
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Roles y permisos del sistema';

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `name`, `display_name`, `description`, `permissions`, `level`, `status`, `created_at`, `updated_at`) VALUES
(1, 'super_admin', 'Super Administrador', 'Administrador TI - Gestión completa del sistema', '\"[\\\"tasks.view\\\", \\\"tasks.create\\\", \\\"tasks.edit\\\", \\\"tasks.delete\\\", \\\"tasks.assign\\\", \\\"users.manage\\\", \\\"areas.manage\\\", \\\"projects.manage\\\"]\"', 1, 'active', '2025-12-12 03:42:49', '2025-12-12 03:42:49'),
(2, 'gerente', 'Gerente General', 'Visión ejecutiva - Dashboards y reportes + gestión de proyectos', '\"[\\\"dashboard.executive\\\", \\\"tasks.view\\\", \\\"users.view\\\", \\\"projects.manage\\\", \\\"projects.view\\\"]\"', 2, 'active', '2025-12-12 03:42:49', '2025-12-12 03:42:49'),
(3, 'supervisor', 'Supervisor', 'Supervisión de áreas, aprobación de tareas y reportes', '\"[\\\"tasks.create\\\", \\\"tasks.edit\\\", \\\"tasks.assign\\\", \\\"tasks.approve\\\", \\\"dashboard.area\\\", \\\"projects.view\\\"]\"', 2, 'active', '2025-12-12 03:42:49', '2025-12-12 03:42:49'),
(4, 'colaborador', 'Colaborador', 'Usuario regular - Solo sus tareas', '\"[\\\"dashboard.personal\\\", \\\"tasks.view\\\", \\\"tasks.update_own\\\"]\"', 4, 'active', '2025-12-12 03:42:49', '2025-12-12 03:42:49'),
(5, 'supervisor_area', 'Supervisor de Área', 'Supervisión de una área específica - Solo ve proyectos y tareas de su área asignada', '\"[\\\"dashboard.personal\\\", \\\"tasks.view\\\", \\\"tasks.view_area\\\", \\\"tasks.create\\\", \\\"tasks.edit\\\", \\\"tasks.assign\\\", \\\"tasks.delete\\\", \\\"projects.view\\\", \\\"projects.view_area\\\", \\\"projects.create\\\", \\\"projects.edit\\\", \\\"persons.view\\\", \\\"persons.view_area\\\", \\\"areas.view\\\", \\\"ml.predict_risk\\\", \\\"ml.predict_duration\\\", \\\"ml.recommend_person\\\", \\\"ml.analyze_performance\\\"]\"', 1, 'active', '2025-12-14 05:01:46', '2025-12-14 10:36:24');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tasks`
--

CREATE TABLE `tasks` (
  `task_id` varchar(64) NOT NULL,
  `project_id` varchar(64) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `task_name` varchar(255) DEFAULT NULL,
  `task_type` varchar(200) DEFAULT NULL,
  `start_date_est` date DEFAULT NULL,
  `end_date_est` date DEFAULT NULL,
  `start_date_real` date DEFAULT NULL,
  `end_date_real` date DEFAULT NULL,
  `duration_est` decimal(10,2) DEFAULT NULL,
  `duration_real` decimal(10,2) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `priority` varchar(100) DEFAULT NULL,
  `dependencies` text,
  `complexity_level` varchar(100) DEFAULT NULL,
  `tools_used` text,
  `completion` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tareas históricas - estructura copiada de sb_training';

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `v_area_metrics`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `v_area_metrics` (
`area_id` int
,`area_name` varchar(100)
,`employee_count` int
,`efficiency_score` decimal(5,2)
,`total_tasks` bigint
,`completed_tasks` bigint
,`delayed_tasks` bigint
,`in_progress_tasks` bigint
,`avg_task_hours` decimal(14,6)
,`avg_estimation_accuracy` decimal(23,10)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `v_delayed_tasks`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `v_delayed_tasks` (
`id` int
,`title` varchar(200)
,`area` varchar(100)
,`priority` enum('alta','media','baja')
,`complexity_score` int
,`estimated_hours` decimal(10,2)
,`actual_hours` decimal(10,2)
,`deadline` datetime
,`assigned_to` varchar(64)
,`delay_hours` decimal(22,2)
,`status` enum('pendiente','en_progreso','completada','retrasada','cancelada')
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `v_ml_prediction_accuracy`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `v_ml_prediction_accuracy` (
`model_type` enum('risk','duration','recommendation','performance','simulation')
,`model_name` varchar(100)
,`version` varchar(20)
,`total_predictions` bigint
,`correct_predictions` decimal(23,0)
,`accuracy_percentage` decimal(30,4)
,`avg_confidence` decimal(9,6)
,`prediction_date` date
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `v_top_performers`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `v_top_performers` (
`person_id` varchar(64)
,`area` varchar(64)
,`role` varchar(64)
,`performance_index` decimal(5,2)
,`experience_years` decimal(4,1)
,`total_tasks_historical` bigint
,`completed_tasks` bigint
,`satisfaction_score` decimal(3,2)
,`rework_rate` decimal(5,2)
,`current_load` decimal(5,2)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `v_training_status`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `v_training_status` (
`job_id` int
,`job_name` varchar(150)
,`model_name` varchar(100)
,`model_type` enum('risk','duration','recommendation','performance','simulation')
,`dataset_filename` varchar(255)
,`status` enum('pending','running','completed','failed','cancelled')
,`progress` int
,`current_step` varchar(100)
,`started_at` timestamp
,`completed_at` timestamp
,`duration_seconds` int
,`created_by_user` varchar(150)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `web_tasks`
--

CREATE TABLE `web_tasks` (
  `id` int NOT NULL,
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `description` text,
  `priority` enum('alta','media','baja') DEFAULT 'media',
  `status` enum('pendiente','en_progreso','completada','retrasada','cancelada') DEFAULT 'pendiente',
  `area` varchar(100) DEFAULT NULL,
  `assigned_to` varchar(64) DEFAULT NULL COMMENT 'person_id del colaborador asignado',
  `complexity_score` int DEFAULT NULL,
  `estimated_hours` decimal(10,2) DEFAULT NULL,
  `actual_hours` decimal(10,2) DEFAULT NULL,
  `deadline` datetime DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `created_by` int DEFAULT NULL COMMENT 'web_users.id del creador',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `web_tasks`
--

INSERT INTO `web_tasks` (`id`, `project_id`, `title`, `description`, `priority`, `status`, `area`, `assigned_to`, `complexity_score`, `estimated_hours`, `actual_hours`, `deadline`, `start_date`, `completed_at`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 'PROJ-DEFAULT', 'Realizar el plan de navidad', 'A', 'media', 'pendiente', 'Marketing', 'usuario@processmart.com', NULL, 80.00, NULL, NULL, NULL, NULL, NULL, '2025-12-08 09:09:03', '2025-12-11 17:02:11'),
(2, 'PROJ-DEFAULT', 'Implementacion CRM', 'Nose', 'media', 'pendiente', 'IT', 'admin@processmart.com', NULL, 80.00, NULL, NULL, NULL, NULL, NULL, '2025-12-11 06:35:24', '2025-12-11 17:02:11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `web_task_dependencies`
--

CREATE TABLE `web_task_dependencies` (
  `id` int NOT NULL,
  `project_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `predecessor_task_id` int NOT NULL COMMENT 'Tarea que debe completarse primero',
  `successor_task_id` int NOT NULL COMMENT 'Tarea que depende de la anterior',
  `dependency_type` enum('finish_to_start','start_to_start','finish_to_finish','start_to_finish') COLLATE utf8mb4_unicode_ci DEFAULT 'finish_to_start',
  `lag_days` int DEFAULT '0' COMMENT 'Días de espera entre tareas',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `web_task_dependencies`
--

INSERT INTO `web_task_dependencies` (`id`, `project_id`, `predecessor_task_id`, `successor_task_id`, `dependency_type`, `lag_days`, `created_at`, `updated_at`) VALUES
(1, 'PROJ-DEFAULT', 1, 2, 'finish_to_start', 1, '2025-12-11 22:19:40', '2025-12-11 22:19:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `web_users`
--

CREATE TABLE `web_users` (
  `id` int NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(150) DEFAULT NULL,
  `role_id` int NOT NULL COMMENT 'FK a tabla roles',
  `area` varchar(100) DEFAULT NULL,
  `person_id` varchar(64) DEFAULT NULL COMMENT 'Relación opcional con people',
  `status` enum('active','inactive') DEFAULT 'active',
  `avatar_url` varchar(255) DEFAULT NULL,
  `last_login` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `experience_years` int DEFAULT '2' COMMENT 'Años de experiencia profesional',
  `performance_index` float DEFAULT '50' COMMENT 'Índice de desempeño (0-100)',
  `rework_rate` float DEFAULT '0.1' COMMENT 'Tasa de retrabajo (0-1)',
  `satisfaction_score` float DEFAULT '3' COMMENT 'Satisfacción del colaborador (1-5)',
  `current_load` int DEFAULT '0' COMMENT 'Número de tareas activas asignadas',
  `tasks_completed` int DEFAULT '0' COMMENT 'Total de tareas completadas',
  `availability_hours_week` float DEFAULT '40' COMMENT 'Horas disponibles por semana'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Usuarios administradores/analistas del sistema web';

--
-- Volcado de datos para la tabla `web_users`
--

INSERT INTO `web_users` (`id`, `email`, `password_hash`, `full_name`, `role_id`, `area`, `person_id`, `status`, `avatar_url`, `last_login`, `created_at`, `updated_at`, `experience_years`, `performance_index`, `rework_rate`, `satisfaction_score`, `current_load`, `tasks_completed`, `availability_hours_week`) VALUES
(1, 'admin@processmart.com', '$2b$12$K5KOHE1acTt8EUagVW6BYehyp4MRkXKwBdXYBwoYYHGzgywfvoDBy', 'Administrador Sistema', 1, 'TI', NULL, 'active', NULL, '2025-12-15 05:33:42', '2025-12-12 03:42:49', '2025-12-15 05:33:42', 2, 85, 0.1, 3, 0, 0, 40),
(2, 'gerente@processmart.com', '$2b$12$myGMaq/maCs.eyh6aMj4FuWLY0/b129HqrSxzN0VzkkdCsH.KzMIq', 'Gerente General', 2, 'Gerencia', NULL, 'active', NULL, NULL, '2025-12-12 03:42:49', '2025-12-14 10:24:44', 2, 78, 0.1, 3, 0, 0, 40),
(3, 'supervisor@processmart.com', '$2b$12$uW5PxWkkkwAr.c9d4G7Rw.MweAnmnq/Flx0h98NEDDXeuDQESpAX.', 'Supervisor Producción', 3, 'Producción', NULL, 'active', NULL, NULL, '2025-12-12 03:42:50', '2025-12-14 10:24:44', 2, 72, 0.1, 3, 0, 0, 40),
(4, 'usuario@processmart.com', '$2b$12$yCovC9UyTe3mMexBuuxez.ebRVIepgJM4S8nnvWPwIR.1Z0o3oQo.', 'Usuario Colaborador', 4, 'Operaciones', NULL, 'active', NULL, '2025-12-14 09:39:43', '2025-12-12 03:42:50', '2025-12-14 10:24:44', 2, 65, 0.1, 3, 0, 0, 40);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `areas`
--
ALTER TABLE `areas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `idx_name` (`name`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_supervisor` (`supervisor_person_id`);

--
-- Indices de la tabla `assignees`
--
ALTER TABLE `assignees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_task` (`task_id`),
  ADD KEY `idx_person` (`person_id`),
  ADD KEY `idx_assigned_at` (`assigned_at`);

--
-- Indices de la tabla `ml_datasets`
--
ALTER TABLE `ml_datasets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_uploaded_by` (`uploaded_by`),
  ADD KEY `idx_uploaded_at` (`uploaded_at`);

--
-- Indices de la tabla `ml_models`
--
ALTER TABLE `ml_models`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_type` (`type`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_version` (`version`);

--
-- Indices de la tabla `ml_predictions`
--
ALTER TABLE `ml_predictions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_task` (`task_reference`,`task_source`),
  ADD KEY `idx_model_type` (`model_type`),
  ADD KEY `idx_model_id` (`model_id`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indices de la tabla `ml_training_jobs`
--
ALTER TABLE `ml_training_jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_model_id` (`model_id`),
  ADD KEY `idx_dataset_id` (`dataset_id`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indices de la tabla `people`
--
ALTER TABLE `people`
  ADD PRIMARY KEY (`person_id`),
  ADD KEY `idx_area` (`area`),
  ADD KEY `idx_performance` (`performance_index`),
  ADD KEY `idx_role` (`role`);

--
-- Indices de la tabla `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`project_id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_manager` (`manager_id`),
  ADD KEY `idx_dates` (`start_date`,`expected_end_date`),
  ADD KEY `fk_projects_area` (`area_id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `idx_name` (`name`),
  ADD KEY `idx_level` (`level`),
  ADD KEY `idx_status` (`status`);

--
-- Indices de la tabla `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`task_id`),
  ADD KEY `idx_area` (`area`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_priority` (`priority`);

--
-- Indices de la tabla `web_tasks`
--
ALTER TABLE `web_tasks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_area` (`area`),
  ADD KEY `idx_assigned` (`assigned_to`),
  ADD KEY `idx_priority` (`priority`),
  ADD KEY `idx_deadline` (`deadline`),
  ADD KEY `idx_created_by` (`created_by`),
  ADD KEY `idx_task_project` (`project_id`);

--
-- Indices de la tabla `web_task_dependencies`
--
ALTER TABLE `web_task_dependencies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_dependency` (`predecessor_task_id`,`successor_task_id`),
  ADD KEY `idx_project` (`project_id`),
  ADD KEY `idx_predecessor` (`predecessor_task_id`),
  ADD KEY `idx_successor` (`successor_task_id`);

--
-- Indices de la tabla `web_users`
--
ALTER TABLE `web_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_role_id` (`role_id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_area` (`area`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `areas`
--
ALTER TABLE `areas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `assignees`
--
ALTER TABLE `assignees`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ml_datasets`
--
ALTER TABLE `ml_datasets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ml_models`
--
ALTER TABLE `ml_models`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ml_predictions`
--
ALTER TABLE `ml_predictions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ml_training_jobs`
--
ALTER TABLE `ml_training_jobs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `web_tasks`
--
ALTER TABLE `web_tasks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `web_task_dependencies`
--
ALTER TABLE `web_task_dependencies`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `web_users`
--
ALTER TABLE `web_users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

-- --------------------------------------------------------

--
-- Estructura para la vista `v_area_metrics`
--
DROP TABLE IF EXISTS `v_area_metrics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_area_metrics`  AS SELECT `a`.`id` AS `area_id`, `a`.`name` AS `area_name`, `a`.`employee_count` AS `employee_count`, `a`.`efficiency_score` AS `efficiency_score`, count(distinct `wt`.`id`) AS `total_tasks`, count(distinct (case when (`wt`.`status` = 'completada') then `wt`.`id` end)) AS `completed_tasks`, count(distinct (case when (`wt`.`status` = 'retrasada') then `wt`.`id` end)) AS `delayed_tasks`, count(distinct (case when (`wt`.`status` = 'en_progreso') then `wt`.`id` end)) AS `in_progress_tasks`, avg((case when (`wt`.`actual_hours` is not null) then `wt`.`actual_hours` end)) AS `avg_task_hours`, avg((case when ((`wt`.`actual_hours` is not null) and (`wt`.`estimated_hours` is not null)) then ((`wt`.`actual_hours` / nullif(`wt`.`estimated_hours`,0)) * 100) end)) AS `avg_estimation_accuracy` FROM (`areas` `a` left join `web_tasks` `wt` on((`a`.`name` = `wt`.`area`))) GROUP BY `a`.`id`, `a`.`name`, `a`.`employee_count`, `a`.`efficiency_score` ;

-- --------------------------------------------------------

--
-- Estructura para la vista `v_delayed_tasks`
--
DROP TABLE IF EXISTS `v_delayed_tasks`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_delayed_tasks`  AS SELECT `wt`.`id` AS `id`, `wt`.`title` AS `title`, `wt`.`area` AS `area`, `wt`.`priority` AS `priority`, `wt`.`complexity_score` AS `complexity_score`, `wt`.`estimated_hours` AS `estimated_hours`, `wt`.`actual_hours` AS `actual_hours`, `wt`.`deadline` AS `deadline`, `wt`.`assigned_to` AS `assigned_to`, (case when ((`wt`.`actual_hours` is not null) and (`wt`.`estimated_hours` is not null)) then (`wt`.`actual_hours` - `wt`.`estimated_hours`) when ((`wt`.`deadline` < now()) and (`wt`.`status` <> 'completada')) then timestampdiff(HOUR,`wt`.`deadline`,now()) else NULL end) AS `delay_hours`, `wt`.`status` AS `status` FROM `web_tasks` AS `wt` WHERE ((`wt`.`actual_hours` > `wt`.`estimated_hours`) OR ((`wt`.`deadline` < now()) AND (`wt`.`status` not in ('completada','cancelada')))) ORDER BY (case when ((`wt`.`actual_hours` is not null) and (`wt`.`estimated_hours` is not null)) then (`wt`.`actual_hours` - `wt`.`estimated_hours`) when ((`wt`.`deadline` < now()) and (`wt`.`status` <> 'completada')) then timestampdiff(HOUR,`wt`.`deadline`,now()) else NULL end) DESC ;

-- --------------------------------------------------------

--
-- Estructura para la vista `v_ml_prediction_accuracy`
--
DROP TABLE IF EXISTS `v_ml_prediction_accuracy`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_ml_prediction_accuracy`  AS SELECT `mp`.`model_type` AS `model_type`, `m`.`name` AS `model_name`, `m`.`version` AS `version`, count(0) AS `total_predictions`, sum((case when (`mp`.`is_correct` = 1) then 1 else 0 end)) AS `correct_predictions`, ((sum((case when (`mp`.`is_correct` = 1) then 1 else 0 end)) / count(0)) * 100) AS `accuracy_percentage`, avg(`mp`.`confidence`) AS `avg_confidence`, cast(`mp`.`created_at` as date) AS `prediction_date` FROM (`ml_predictions` `mp` left join `ml_models` `m` on((`mp`.`model_id` = `m`.`id`))) WHERE (`mp`.`actual_result` is not null) GROUP BY `mp`.`model_type`, `m`.`name`, `m`.`version`, cast(`mp`.`created_at` as date) ORDER BY `prediction_date` DESC ;

-- --------------------------------------------------------

--
-- Estructura para la vista `v_top_performers`
--
DROP TABLE IF EXISTS `v_top_performers`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_top_performers`  AS SELECT `p`.`person_id` AS `person_id`, `p`.`area` AS `area`, `p`.`role` AS `role`, `p`.`performance_index` AS `performance_index`, `p`.`experience_years` AS `experience_years`, count(`a`.`task_id`) AS `total_tasks_historical`, count((case when (`t`.`status` = 'Completed') then 1 end)) AS `completed_tasks`, `p`.`satisfaction_score` AS `satisfaction_score`, `p`.`rework_rate` AS `rework_rate`, `p`.`current_load` AS `current_load` FROM ((`people` `p` left join `assignees` `a` on((`p`.`person_id` = `a`.`person_id`))) left join `tasks` `t` on((`a`.`task_id` = `t`.`task_id`))) WHERE ((`p`.`performance_index` >= 4) AND (`p`.`resigned` = 0)) GROUP BY `p`.`person_id`, `p`.`area`, `p`.`role`, `p`.`performance_index`, `p`.`experience_years`, `p`.`satisfaction_score`, `p`.`rework_rate`, `p`.`current_load` ORDER BY `p`.`performance_index` DESC, `completed_tasks` DESC LIMIT 0, 10 ;

-- --------------------------------------------------------

--
-- Estructura para la vista `v_training_status`
--
DROP TABLE IF EXISTS `v_training_status`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_training_status`  AS SELECT `tj`.`id` AS `job_id`, `tj`.`job_name` AS `job_name`, `m`.`name` AS `model_name`, `m`.`type` AS `model_type`, `d`.`filename` AS `dataset_filename`, `tj`.`status` AS `status`, `tj`.`progress` AS `progress`, `tj`.`current_step` AS `current_step`, `tj`.`started_at` AS `started_at`, `tj`.`completed_at` AS `completed_at`, `tj`.`duration_seconds` AS `duration_seconds`, `u`.`full_name` AS `created_by_user` FROM (((`ml_training_jobs` `tj` left join `ml_models` `m` on((`tj`.`model_id` = `m`.`id`))) left join `ml_datasets` `d` on((`tj`.`dataset_id` = `d`.`id`))) left join `web_users` `u` on((`tj`.`created_by` = `u`.`id`))) ORDER BY `tj`.`created_at` DESC ;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ml_datasets`
--
ALTER TABLE `ml_datasets`
  ADD CONSTRAINT `ml_datasets_ibfk_1` FOREIGN KEY (`uploaded_by`) REFERENCES `web_users` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `ml_predictions`
--
ALTER TABLE `ml_predictions`
  ADD CONSTRAINT `ml_predictions_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `ml_models` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `ml_training_jobs`
--
ALTER TABLE `ml_training_jobs`
  ADD CONSTRAINT `ml_training_jobs_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `ml_models` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ml_training_jobs_ibfk_2` FOREIGN KEY (`dataset_id`) REFERENCES `ml_datasets` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `ml_training_jobs_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `web_users` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `fk_projects_area` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`),
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `web_users` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `web_tasks`
--
ALTER TABLE `web_tasks`
  ADD CONSTRAINT `fk_task_project` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `web_tasks_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `web_users` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `web_task_dependencies`
--
ALTER TABLE `web_task_dependencies`
  ADD CONSTRAINT `web_task_dependencies_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `web_task_dependencies_ibfk_2` FOREIGN KEY (`predecessor_task_id`) REFERENCES `web_tasks` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `web_task_dependencies_ibfk_3` FOREIGN KEY (`successor_task_id`) REFERENCES `web_tasks` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `web_users`
--
ALTER TABLE `web_users`
  ADD CONSTRAINT `web_users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
