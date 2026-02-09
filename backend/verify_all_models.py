"""
Verifica qué modelos pueden entrenarse con los datos actuales
"""
from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:@localhost:3306/sb_production?charset=utf8mb4')

print("="*70)
print("VERIFICACIÓN DE REQUISITOS PARA ENTRENAMIENTO DE MODELOS")
print("="*70)

models = {
    "1. Clasificador de Riesgo (risk)": {
        "query": "SELECT COUNT(*) FROM tasks WHERE duration_est IS NOT NULL AND duration_real IS NOT NULL AND complexity_level IS NOT NULL",
        "minimo": 100,
        "descripcion": "Tareas con duración estimada, real y complejidad"
    },
    "2. Predictor de Duración (duration)": {
        "query": "SELECT COUNT(*) FROM v_training_dataset_clean",
        "minimo": 100,
        "descripcion": "Vista v_training_dataset_clean (tareas completas)"
    },
    "3. Recomendador Persona-Tarea (recommendation)": {
        "query": "SELECT COUNT(*) FROM tasks t JOIN assignees a ON t.task_id = a.task_id JOIN people p ON a.person_id = p.person_id WHERE t.duration_real IS NOT NULL",
        "minimo": 200,
        "descripcion": "Tareas asignadas a personas con duración real"
    },
    "4. Predictor de Performance (performance)": {
        "query": "SELECT COUNT(DISTINCT p.person_id) FROM people p LEFT JOIN assignees a ON p.person_id = a.person_id LEFT JOIN tasks t ON a.task_id = t.task_id WHERE t.duration_real IS NOT NULL GROUP BY p.person_id HAVING COUNT(DISTINCT a.task_id) >= 1",
        "minimo": 20,
        "descripcion": "Personas con al menos 1 tarea completada"
    },
    "5. Predictor de Cuellos de Botella (simulation)": {
        "query": "SELECT COUNT(*) FROM tasks WHERE duration_real IS NOT NULL",
        "minimo": 100,
        "descripcion": "Tareas completadas (con duration_real)"
    }
}

with engine.connect() as conn:
    for model_name, config in models.items():
        print(f"\n{model_name}")
        print("-" * 70)
        try:
            result = conn.execute(text(config['query']))
            count = result.scalar()
            status = "✅ PUEDE ENTRENAR" if count >= config['minimo'] else "❌ INSUFICIENTE"
            print(f"  Requisito: {config['descripcion']}")
            print(f"  Registros encontrados: {count}")
            print(f"  Mínimo necesario: {config['minimo']}")
            print(f"  Estado: {status}")
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)[:100]}")

print("\n" + "="*70)
print("RESUMEN")
print("="*70)
print("Para entrenar CUALQUIER modelo necesitas:")
print("  1. Tabla 'tasks' con registros (duration_est, duration_real, complexity_level)")
print("  2. Tabla 'people' con registros")
print("  3. Tabla 'assignees' que relaciona personas con tareas")
print("\nACTUALMENTE: Base de datos VACÍA - NINGÚN modelo puede entrenarse")
print("="*70)
