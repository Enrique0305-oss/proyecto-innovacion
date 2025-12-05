"""
Ver todos los usuarios de web_users
"""
from app import create_app
from app.models.web_user import WebUser

app = create_app()

with app.app_context():
    total = WebUser.query.count()
    print(f'\n📊 Total usuarios en web_users: {total}')
    
    if total > 0:
        print('\n👥 Todos los usuarios:')
        users = WebUser.query.all()
        for u in users:
            print(f'\n  ID: {u.id}')
            print(f'  Nombre: {u.full_name}')
            print(f'  Email: {u.email}')
            print(f'  Role ID: {u.role_id}')
            print(f'  Área: {u.area}')
            print(f'  Status: {u.status}')
    else:
        print('\n⚠️ NO HAY USUARIOS EN web_users')
        print('   Ejecuta: python init_database.py')
