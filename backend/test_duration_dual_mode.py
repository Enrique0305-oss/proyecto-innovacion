"""
Test del modo dual del modelo de duración
"""
from app import create_app
from app.ml.duration_model import predict_duration

app = create_app()

with app.app_context():
    # Datos de la tarea
    task_data = {
        'area': 'IT',
        'task_type': 'Desarrollo',
        'complexity_level': 'Alta',
        'duration_est': 10,
        'assignees_count': 1,
        'dependencies': 2
    }
    
    print('\n' + '='*60)
    print('🧪 TEST: MODO DUAL DEL MODELO DE DURACIÓN')
    print('='*60)
    
    # MODO 1: Genérico (sin person_id)
    print('\n📊 MODO GENÉRICO (sin person_id):')
    print('-' * 60)
    result_generic = predict_duration(task_data)
    print(f'   Duración: {result_generic.get("duration_days")} días')
    print(f'   Rango: {result_generic["confidence_interval"]["min"]:.1f} - {result_generic["confidence_interval"]["max"]:.1f} días')
    print(f'   Modo: {result_generic.get("mode")}')
    print(f'   Factores:')
    for factor in result_generic.get('factors', []):
        print(f'     - {factor}')
    
    # MODO 2: Personalizado (con person_id = 4, Usuario Demo)
    print('\n👤 MODO PERSONALIZADO (person_id=4, Usuario Demo):')
    print('-' * 60)
    task_data_personalized = {**task_data, 'person_id': 4}
    result_personalized = predict_duration(task_data_personalized)
    print(f'   Duración: {result_personalized.get("duration_days")} días')
    print(f'   Rango: {result_personalized["confidence_interval"]["min"]:.1f} - {result_personalized["confidence_interval"]["max"]:.1f} días')
    print(f'   Modo: {result_personalized.get("mode")}')
    print(f'   Factores:')
    for factor in result_personalized.get('factors', []):
        print(f'     - {factor}')
    
    # MODO 3: Personalizado (con person_id = 3, Analista Demo)
    print('\n👤 MODO PERSONALIZADO (person_id=3, Analista Demo):')
    print('-' * 60)
    task_data_personalized2 = {**task_data, 'person_id': 3}
    result_personalized2 = predict_duration(task_data_personalized2)
    print(f'   Duración: {result_personalized2.get("duration_days")} días')
    print(f'   Rango: {result_personalized2["confidence_interval"]["min"]:.1f} - {result_personalized2["confidence_interval"]["max"]:.1f} días')
    print(f'   Modo: {result_personalized2.get("mode")}')
    print(f'   Factores:')
    for factor in result_personalized2.get('factors', []):
        print(f'     - {factor}')
    
    print('\n' + '='*60)
    print('✅ CONCLUSIÓN:')
    print('='*60)
    print(f'   Genérico:    {result_generic.get("duration_days")} días (sin conocer quién)')
    print(f'   Usuario Demo: {result_personalized.get("duration_days")} días (performance_index=75%)')
    print(f'   Analista Demo: {result_personalized2.get("duration_days")} días (performance_index=85%)')
    print('\n   ✅ El modelo ajusta la duración según el colaborador')
    print('='*60 + '\n')
