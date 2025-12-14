"""
Script para verificar los datos de las tareas
"""
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    print("=" * 60)
    print("VERIFICACIÓN DE DATOS DE TAREAS")
    print("=" * 60)
    
    # Consultar las tareas
    result = db.session.execute(db.text("""
        SELECT 
            id,
            title,
            area,
            estimated_hours,
            actual_hours,
            complexity_score,
            status,
            assigned_to
        FROM web_tasks
        ORDER BY id
        LIMIT 10
    """)).fetchall()
    
    print(f"\n📋 Tareas encontradas: {len(result)}\n")
    
    for task in result:
        print(f"Tarea #{task[0]}: {task[1]}")
        print(f"  Área: {task[2]}")
        print(f"  ⏱️  Horas Estimadas: {task[3]}")
        print(f"  ⏱️  Horas Reales: {task[4]}")
        print(f"  📊 Complejidad: {task[5]}")
        print(f"  📌 Estado: {task[6]}")
        print(f"  👤 Asignado: {task[7]}")
        print("-" * 60)
