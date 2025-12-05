"""
Script de prueba para verificar la integración del modelo CatBoost Recommender
"""
import os
import sys

# Agregar path del backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ml.recommender_model import load_model, recommend_person

print("=" * 70)
print("🧪 TEST: Verificación del Modelo CatBoost Recommender")
print("=" * 70)

# Test 1: Cargar modelo
print("\n1️⃣ Cargando modelo...")
model = load_model()

if model is None:
    print("❌ ERROR: El modelo no se pudo cargar")
    print("\n📝 INSTRUCCIONES:")
    print("1. Copia 'model_catboost_recommender.pkl' a:")
    print("   backend/ml/models/recommender/")
    print("2. Copia 'columns_recommender.json' a:")
    print("   backend/ml/models/recommender/")
    print("3. Copia 'recommender_metrics.json' a:")
    print("   backend/ml/models/recommender/")
    sys.exit(1)

print("\n✅ Modelo cargado exitosamente!")

# Test 2: Hacer una predicción de prueba
print("\n2️⃣ Probando recomendación...")

task_data = {
    'area': 'TI',
    'task_type': 'Desarrollo',
    'complexity_level': 'Media',
    'duration_est': 10,
    'priority': 'Alta',
    'skills_required': ['Python', 'React', 'SQL'],
    'top_n': 5
}

print(f"\nDatos de la tarea:")
print(f"  - Área: {task_data['area']}")
print(f"  - Tipo: {task_data['task_type']}")
print(f"  - Complejidad: {task_data['complexity_level']}")
print(f"  - Duración: {task_data['duration_est']} días")
print(f"  - Prioridad: {task_data['priority']}")

result = recommend_person(task_data)

print(f"\n✅ Resultado:")
print(f"  - Total candidatos evaluados: {result['total_candidates']}")
print(f"  - Recomendaciones generadas: {len(result['recommendations'])}")
print(f"  - Modelo usado: {result.get('model_used', 'unknown')}")

if result['recommendations']:
    print(f"\n🏆 Top Recomendación:")
    top = result['recommendations'][0]
    print(f"  - Nombre: {top['name']}")
    print(f"  - Score: {top['score_percentage']:.2f}%")
    print(f"  - Área: {top['area']}")
    print(f"  - Performance: {top['performance_index']}%")
    print(f"  - Experiencia: {top['experience_years']} años")
    print(f"  - Workload actual: {top['current_workload']} tareas")
    print(f"  - Razones: {', '.join(top['reasons'][:2])}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO EXITOSAMENTE")
print("=" * 70)
print("\n📌 El modelo está listo para usarse en el sistema web")
