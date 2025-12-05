"""
Script para verificar personas en la base de datos
"""
from app import create_app
from app.models.person import Person

app = create_app()

with app.app_context():
    total = Person.query.count()
    print(f'\n📊 Total personas en DB: {total}')
    
    if total > 0:
        print('\n👥 Primeras 5 personas:')
        personas = Person.query.limit(5).all()
        for p in personas:
            print(f'  - {p.first_name} {p.last_name}')
            print(f'    Area: {p.area}, Role: {p.role}')
            print(f'    Activo: {not p.resigned}')
    else:
        print('\n⚠️ NO HAY PERSONAS EN LA BASE DE DATOS')
        print('   Ejecuta: python init_database.py')
