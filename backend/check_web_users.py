"""
Script para verificar usuarios web con role_id = 1 (colaboradores)
"""
from app import create_app
from app.models.web_user import WebUser

app = create_app()

with app.app_context():
    total = WebUser.query.filter_by(role_id=7, status='active').count()
    print(f'\n📊 Total colaboradores activos (role_id=7): {total}')
    
    if total > 0:
        print('\n👥 Colaboradores encontrados:')
        users = WebUser.query.filter_by(role_id=7, status='active').all()
        for u in users:
            print(f'  - {u.full_name}')
            print(f'    Email: {u.email}')
            print(f'    Área: {u.area}')
            print(f'    Person ID: {u.person_id}')
    else:
        print('\n⚠️ NO HAY COLABORADORES CON ROLE_ID=7 EN web_users')
        print('   Verifica la tabla web_users y roles')
