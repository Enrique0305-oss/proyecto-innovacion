"""Script para crear datos de prueba en web_tasks y áreas"""
from app.extensions import db
from app import create_app
from config import get_config
from app.models.web_task import WebTask
from app.models.area import Area
from app.models.web_user import WebUser
from datetime import datetime, timedelta

app = create_app(get_config())
app.app_context().push()

print("\n=== VERIFICANDO ÁREAS ===")
areas_count = Area.query.count()
print(f"Áreas existentes: {areas_count}")

if areas_count == 0:
    print("Creando áreas de prueba...")
    areas_data = [
        {'name': 'TI', 'description': 'Tecnologías de la Información', 'status': 'active'},
        {'name': 'Marketing', 'description': 'Marketing y Comunicaciones', 'status': 'active'},
        {'name': 'Ventas', 'description': 'Departamento de Ventas', 'status': 'active'},
        {'name': 'RRHH', 'description': 'Recursos Humanos', 'status': 'active'},
        {'name': 'Finanzas', 'description': 'Finanzas y Contabilidad', 'status': 'active'},
    ]
    
    for area_data in areas_data:
        area = Area(**area_data)
        db.session.add(area)
    
    db.session.commit()
    print(f"✅ {len(areas_data)} áreas creadas")
else:
    areas = Area.query.all()
    for area in areas:
        print(f"  - {area.name}: {area.description}")

print("\n=== VERIFICANDO TAREAS ===")
tasks_count = WebTask.query.count()
print(f"Tareas existentes: {tasks_count}")

if tasks_count < 10:
    print("Creando tareas de prueba...")
    admin_user = WebUser.query.filter_by(email='admin@processmart.com').first()
    areas = Area.query.all()
    
    tasks_data = [
        {
            'title': 'Implementar sistema de autenticación',
            'description': 'Desarrollar módulo de login y registro con JWT',
            'priority': 'alta',
            'status': 'en_progreso',
            'area': 'TI',
            'complexity_score': 8,
            'estimated_hours': 40,
            'deadline': datetime.now() + timedelta(days=15)
        },
        {
            'title': 'Campaña redes sociales Q4',
            'description': 'Planificar y ejecutar campaña de marketing digital',
            'priority': 'alta',
            'status': 'pendiente',
            'area': 'Marketing',
            'complexity_score': 6,
            'estimated_hours': 30,
            'deadline': datetime.now() + timedelta(days=20)
        },
        {
            'title': 'Análisis de ventas mensuales',
            'description': 'Reporte detallado de ventas del mes anterior',
            'priority': 'media',
            'status': 'completada',
            'area': 'Ventas',
            'complexity_score': 4,
            'estimated_hours': 16,
            'actual_hours': 14,
            'completed_at': datetime.now() - timedelta(days=2)
        },
        {
            'title': 'Actualización de base de datos',
            'description': 'Migrar datos a nueva estructura de BD',
            'priority': 'alta',
            'status': 'en_progreso',
            'area': 'TI',
            'complexity_score': 9,
            'estimated_hours': 50,
            'deadline': datetime.now() + timedelta(days=10)
        },
        {
            'title': 'Capacitación de personal',
            'description': 'Organizar sesión de capacitación para nuevo software',
            'priority': 'media',
            'status': 'pendiente',
            'area': 'RRHH',
            'complexity_score': 5,
            'estimated_hours': 20,
            'deadline': datetime.now() + timedelta(days=30)
        },
        {
            'title': 'Optimización de rendimiento web',
            'description': 'Mejorar tiempos de carga del sitio web',
            'priority': 'media',
            'status': 'en_progreso',
            'area': 'TI',
            'complexity_score': 7,
            'estimated_hours': 35,
            'deadline': datetime.now() + timedelta(days=14)
        },
        {
            'title': 'Diseño de landing page',
            'description': 'Crear página de aterrizaje para nueva campaña',
            'priority': 'alta',
            'status': 'pendiente',
            'area': 'Marketing',
            'complexity_score': 6,
            'estimated_hours': 25,
            'deadline': datetime.now() + timedelta(days=12)
        },
        {
            'title': 'Auditoría financiera trimestral',
            'description': 'Revisión completa de cuentas del trimestre',
            'priority': 'alta',
            'status': 'retrasada',
            'area': 'Finanzas',
            'complexity_score': 8,
            'estimated_hours': 60,
            'deadline': datetime.now() - timedelta(days=3)
        },
        {
            'title': 'Mantenimiento de servidores',
            'description': 'Actualización y mantenimiento preventivo',
            'priority': 'media',
            'status': 'completada',
            'area': 'TI',
            'complexity_score': 5,
            'estimated_hours': 12,
            'actual_hours': 10,
            'completed_at': datetime.now() - timedelta(days=5)
        },
        {
            'title': 'Reunión con cliente corporativo',
            'description': 'Presentación de propuesta comercial',
            'priority': 'alta',
            'status': 'pendiente',
            'area': 'Ventas',
            'complexity_score': 3,
            'estimated_hours': 8,
            'deadline': datetime.now() + timedelta(days=7)
        },
        {
            'title': 'Implementar sistema de backups',
            'description': 'Configurar respaldos automáticos de BD',
            'priority': 'alta',
            'status': 'pendiente',
            'area': 'TI',
            'complexity_score': 7,
            'estimated_hours': 28,
            'deadline': datetime.now() + timedelta(days=18)
        },
        {
            'title': 'Análisis de métricas de marketing',
            'description': 'Evaluar ROI de campañas digitales',
            'priority': 'media',
            'status': 'en_progreso',
            'area': 'Marketing',
            'complexity_score': 5,
            'estimated_hours': 15,
            'deadline': datetime.now() + timedelta(days=10)
        },
    ]
    
    for task_data in tasks_data:
        task = WebTask(
            **task_data,
            created_by=admin_user.id if admin_user else None
        )
        db.session.add(task)
    
    db.session.commit()
    print(f"✅ {len(tasks_data)} tareas creadas")
else:
    print("Ya hay suficientes tareas de prueba")

print("\n=== RESUMEN ===")
print(f"Total áreas: {Area.query.count()}")
print(f"Total tareas: {WebTask.query.count()}")
print(f"  - Pendientes: {WebTask.query.filter_by(status='pendiente').count()}")
print(f"  - En progreso: {WebTask.query.filter_by(status='en_progreso').count()}")
print(f"  - Completadas: {WebTask.query.filter_by(status='completada').count()}")
print(f"  - Retrasadas: {WebTask.query.filter_by(status='retrasada').count()}")
print("\n✅ Base de datos lista para usar!")
