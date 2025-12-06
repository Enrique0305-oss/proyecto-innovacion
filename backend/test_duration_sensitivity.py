"""
Test para verificar la sensibilidad del modelo de duración a diferentes inputs
"""
from app import create_app
from app.ml.duration_model import predict_duration

app = create_app()
app.app_context().push()

print("="*80)
print("🧪 TEST: SENSIBILIDAD DEL MODELO DE DURACIÓN")
print("="*80)

# Configuraciones de prueba
test_cases = [
    {
        "name": "Tarea BAJA - 5 días est.",
        "data": {
            'area': 'IT',
            'task_type': 'Mantenimiento',
            'complexity_level': 'Baja',
            'duration_est_days': 5
        }
    },
    {
        "name": "Tarea MEDIA - 10 días est.",
        "data": {
            'area': 'IT',
            'task_type': 'Desarrollo',
            'complexity_level': 'Media',
            'duration_est_days': 10
        }
    },
    {
        "name": "Tarea ALTA - 10 días est.",
        "data": {
            'area': 'IT',
            'task_type': 'Desarrollo',
            'complexity_level': 'Alta',
            'duration_est_days': 10
        }
    },
    {
        "name": "Tarea ALTA - 20 días est.",
        "data": {
            'area': 'IT',
            'task_type': 'Desarrollo',
            'complexity_level': 'Alta',
            'duration_est_days': 20
        }
    },
    {
        "name": "Tarea ALTA - 30 días est.",
        "data": {
            'area': 'IT',
            'task_type': 'Investigación',
            'complexity_level': 'Alta',
            'duration_est_days': 30
        }
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. {test['name']}")
    print("-" * 60)
    
    # Modo genérico
    result_generic = predict_duration(test['data'])
    
    # Modo personalizado con Analista (mejor desempeño)
    test_personalized = test['data'].copy()
    test_personalized['person_id'] = 3
    result_personalized = predict_duration(test_personalized)
    
    print(f"   Genérico:     {result_generic['duration_days']} días ({result_generic['confidence_interval']['min']}-{result_generic['confidence_interval']['max']})")
    print(f"   Analista:     {result_personalized['duration_days']} días ({result_personalized['confidence_interval']['min']}-{result_personalized['confidence_interval']['max']})")
    print(f"   Diferencia:   {result_generic['duration_days'] - result_personalized['duration_days']:.1f} días")

print("\n" + "="*80)
print("CONCLUSIÓN:")
print("="*80)
print("Si el modelo predice siempre lo mismo, puede ser que:")
print("  1. El modelo fue entrenado con datos de escala diferente")
print("  2. Las features categóricas tienen valores no vistos en entrenamiento")
print("  3. El modelo tiene overfitting a ciertos valores")
print("="*80)
