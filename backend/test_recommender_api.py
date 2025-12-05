"""
Test directo del endpoint de recomendación
"""
from app import create_app

app = create_app()

with app.app_context():
    from app.ml.recommender_model import recommend_person
    
    # Datos de prueba
    task_data = {
        'area': 'IT',
        'task_type': 'Desarrollo',
        'complexity_level': 'Media',
        'priority': 'Alta',
        'duration_est': 10,
        'skills_required': ['Python', 'SQL']
    }
    
    print('\n🧪 Probando recomendación con datos:')
    print(f'   Área: {task_data["area"]}')
    print(f'   Tipo: {task_data["task_type"]}')
    print(f'   Complejidad: {task_data["complexity_level"]}')
    print(f'   Duración: {task_data["duration_est"]} días')
    
    try:
        result = recommend_person(task_data)
        
        print(f'\n✅ Resultado:')
        print(f'   Total candidatos: {result.get("total_candidates")}')
        print(f'   Recomendaciones: {len(result.get("recommendations", []))}')
        
        if result.get('recommendations'):
            print('\n👥 Candidatos:')
            for i, rec in enumerate(result['recommendations'], 1):
                print(f'\n   #{i} {rec["name"]}')
                print(f'      Score: {rec["score_percentage"]}%')
                print(f'      Área: {rec["area"]}')
        else:
            print('\n⚠️ No se encontraron candidatos')
            print(f'   Mensaje: {result.get("message")}')
            
    except Exception as e:
        print(f'\n❌ Error: {str(e)}')
        import traceback
        traceback.print_exc()
