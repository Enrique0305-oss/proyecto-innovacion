-- Agregar campo de habilidades a tabla web_users
-- Fecha: 16 de diciembre de 2025
-- Descripción: Agregar columna skills (TEXT) para almacenar habilidades del usuario

USE sb_production;

-- Agregar columna skills
ALTER TABLE web_users 
ADD COLUMN skills TEXT COMMENT 'Habilidades del usuario separadas por comas' 
AFTER experience_years;

-- Actualizar algunos usuarios de ejemplo con habilidades
UPDATE web_users 
SET skills = CASE 
    WHEN area = 'IT' OR area = 'Tecnología' THEN 'Python, JavaScript, SQL, Git, Docker'
    WHEN area = 'Ingeniería' THEN 'AutoCAD, SolidWorks, Gestión de Proyectos'
    WHEN area = 'Operaciones' THEN 'Logística, Planificación, ERP, Excel Avanzado'
    WHEN area = 'Comercial' OR area = 'Ventas' THEN 'CRM, Negociación, Marketing Digital'
    WHEN area = 'Finanzas' THEN 'Excel, SAP, Contabilidad, Análisis Financiero'
    WHEN area = 'Recursos Humanos' THEN 'Reclutamiento, Nómina, Gestión de Talento'
    ELSE 'Comunicación, Trabajo en equipo, Gestión del tiempo'
END
WHERE skills IS NULL OR skills = '';

SELECT 'Columna skills agregada exitosamente' as resultado;
