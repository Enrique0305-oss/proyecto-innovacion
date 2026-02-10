"""
Script para preparar la base de datos para la presentación de tesis
Limpia datos de prueba y crea usuarios reales
"""
from app import create_app
from app.models.web_user import WebUser
from app.models.role import Role
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.area import Area
from app.extensions import db
import bcrypt

app = create_app()

# Contraseña común para todos: 123456
PASSWORD = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Usuarios a crear
USERS = [
    # Super Admins (role_id = 1)
    {
        'email': 'raul.yanez@processmart.net',
        'full_name': 'Raul Enrique Yañez Cruz',
        'role_id': 1,
        'area': 'IT',
        'skills': 'Python,Machine Learning,Flask,SQL,Data Science,React',
        'experience_years': 5,
        'performance_index': 0.92,
        'satisfaction_score': 4.8
    },
    {
        'email': 'omar.carlos@processmart.net',
        'full_name': 'Omar Alexis Carlos Manrique',
        'role_id': 1,
        'area': 'IT',
        'skills': 'JavaScript,TypeScript,Node.js,React,MongoDB,AWS',
        'experience_years': 4,
        'performance_index': 0.90,
        'satisfaction_score': 4.7
    },
    {
        'email': 'anthony.moru@processmart.net',
        'full_name': 'Anthony Alfonso Moru Titto',
        'role_id': 1,
        'area': 'IT',
        'skills': 'Java,Spring Boot,Docker,Kubernetes,PostgreSQL,CI/CD',
        'experience_years': 4,
        'performance_index': 0.88,
        'satisfaction_score': 4.6
    },
    
    # Gerente (role_id = 2)
    {
        'email': 'jhonatan.coronado@processmart.net',
        'full_name': 'Jhonatan Jair Coronado Roman',
        'role_id': 2,
        'area': 'IT',
        'skills': 'Project Management,Scrum,Agile,Leadership,Strategic Planning',
        'experience_years': 8,
        'performance_index': 0.95,
        'satisfaction_score': 4.9
    },
    
    # Supervisor (role_id = 3)
    {
        'email': 'joel.arapa@processmart.net',
        'full_name': 'Joel Yirbel Arapa Casas',
        'role_id': 3,
        'area': 'IT',
        'skills': 'Team Leadership,Code Review,DevOps,Python,JavaScript,SQL',
        'experience_years': 6,
        'performance_index': 0.91,
        'satisfaction_score': 4.7
    },
    
    # Colaboradores (role_id = 4)
    {
        'email': 'enzo.rueda@processmart.net',
        'full_name': 'Enzo Joel Rueda Gallardo',
        'role_id': 4,
        'area': 'IT',
        'skills': 'Python,Django,REST APIs,PostgreSQL,Git,Linux',
        'experience_years': 2,
        'performance_index': 0.85,
        'satisfaction_score': 4.5
    },
    {
        'email': 'maria.sanchez@processmart.net',
        'full_name': 'María Elena Sánchez Vargas',
        'role_id': 4,
        'area': 'IT',
        'skills': 'Frontend,React,Vue.js,CSS,HTML,UX/UI Design',
        'experience_years': 3,
        'performance_index': 0.87,
        'satisfaction_score': 4.6
    },
    {
        'email': 'carlos.mendoza@processmart.net',
        'full_name': 'Carlos Alberto Mendoza Quispe',
        'role_id': 4,
        'area': 'IT',
        'skills': 'Backend,Node.js,Express,MongoDB,Testing,Docker',
        'experience_years': 2,
        'performance_index': 0.83,
        'satisfaction_score': 4.4
    },
]

with app.app_context():
    print("\n" + "="*80)
    print("PREPARANDO BASE DE DATOS PARA PRESENTACIÓN DE TESIS")
    print("="*80)
    
    # 1. Eliminar datos de prueba
    print("\n Paso 1: Eliminando datos de prueba...")
    
    # Eliminar reuniones
    meetings_deleted = Meeting.query.delete()
    print(f"   - Reuniones eliminadas: {meetings_deleted}")
    
    # Eliminar tareas
    tasks_deleted = Task.query.delete()
    print(f"   - Tareas eliminadas: {tasks_deleted}")
    
    # Eliminar proyectos
    projects_deleted = Project.query.delete()
    print(f"   - Proyectos eliminados: {projects_deleted}")
    
    # Eliminar usuarios actuales
    users_deleted = WebUser.query.delete()
    print(f"   - Usuarios eliminados: {users_deleted}")
    
    db.session.commit()
    print("    Datos de prueba eliminados")
    
    # 2. Crear nuevos usuarios
    print("\n👥 Paso 2: Creando usuarios para la presentación...")
    
    for user_data in USERS:
        user = WebUser(
            email=user_data['email'],
            password_hash=PASSWORD,
            full_name=user_data['full_name'],
            role_id=user_data['role_id'],
            area=user_data['area'],
            status='active',
            skills=user_data['skills'],
            experience_years=user_data['experience_years'],
            performance_index=user_data['performance_index'],
            satisfaction_score=user_data['satisfaction_score'],
            rework_rate=0.05,
            current_load=0,
            tasks_completed=0,
            availability_hours_week=40
        )
        db.session.add(user)
        
        # Obtener nombre del rol
        role = Role.query.get(user_data['role_id'])
        role_name = role.name if role else 'N/A'
        print(f"    {user_data['full_name']} ({role_name}) - {user_data['email']}")
    
    db.session.commit()
    
    # 3. Verificar áreas existentes
    print("\n Paso 3: Verificando áreas...")
    areas = Area.query.filter_by(status='active').all()
    if areas:
        print(f"   Áreas activas: {len(areas)}")
        for area in areas:
            print(f"   - {area.name}")
    else:
        print("    No hay áreas creadas. Puedes crearlas desde la interfaz.")
    
    # Resumen final
    print("\n" + "="*80)
    print(" BASE DE DATOS PREPARADA PARA LA PRESENTACIÓN")
    print("="*80)
    
    print("\n RESUMEN DE USUARIOS CREADOS:")
    print("-"*80)
    
    users = WebUser.query.order_by(WebUser.role_id, WebUser.id).all()
    
    current_role = None
    for u in users:
        role_name = u.role.display_name if u.role else 'N/A'
        if current_role != role_name:
            current_role = role_name
            print(f"\n{role_name.upper()}:")
        print(f"    {u.email}")
        print(f"      Nombre: {u.full_name}")
        print(f"      Área: {u.area}")
        print(f"      Skills: {u.skills}")
    
    print("\n" + "="*80)
    print(" CONTRASEÑA PARA TODOS LOS USUARIOS: 123456")
    print("="*80)
    
    print("\n FLUJO SUGERIDO PARA LA PRESENTACIÓN:")
    print("-"*80)
    print("1. Login como Super Admin (raul.yanez@processmart.net)")
    print("   → Mostrar gestión de Áreas y Usuarios")
    print("")
    print("2. Login como Gerente (jhonatan.coronado@processmart.net)")
    print("   → Crear un nuevo Proyecto")
    print("   → Crear Tareas con predicción de duración IA")
    print("")
    print("3. Usar módulos de IA:")
    print("   → Clasificación de Riesgo")
    print("   → Predicción de Duración")
    print("   → Recomendación Persona-Tarea")
    print("   → Asignación Inteligente")
    print("")
    print("4. Mostrar Desempeño del Colaborador")
    print("5. Mostrar Simulación de Flujo (Process Mining)")
    print("="*80 + "\n")
