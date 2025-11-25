"""
Script de diagnóstico completo para JWT
"""
import os
import sys
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

print("="*60)
print("DIAGNÓSTICO DE CONFIGURACIÓN JWT")
print("="*60)

# 1. Verificar variables de entorno
print("\n1. VARIABLES DE ENTORNO:")
secret_key = os.getenv('SECRET_KEY')
jwt_secret = os.getenv('JWT_SECRET_KEY')
print(f"   SECRET_KEY: {secret_key[:50] if secret_key else 'NO DEFINIDA'}...")
print(f"   JWT_SECRET_KEY: {jwt_secret[:50] if jwt_secret else 'NO DEFINIDA'}...")
print(f"   ¿Son iguales?: {secret_key == jwt_secret}")

# 2. Verificar config.py
print("\n2. CONFIG.PY:")
from config import get_config
config = get_config()
print(f"   Config.SECRET_KEY: {config.SECRET_KEY[:50] if config.SECRET_KEY else 'NO DEFINIDA'}...")
print(f"   Config.JWT_SECRET_KEY: {config.JWT_SECRET_KEY[:50] if config.JWT_SECRET_KEY else 'NO DEFINIDA'}...")
print(f"   ¿Son iguales?: {config.SECRET_KEY == config.JWT_SECRET_KEY}")

# 3. Crear aplicación Flask y verificar configuración
print("\n3. APLICACIÓN FLASK:")
from app import create_app
app = create_app()
with app.app_context():
    print(f"   app.config['SECRET_KEY']: {app.config['SECRET_KEY'][:50]}...")
    print(f"   app.config['JWT_SECRET_KEY']: {app.config['JWT_SECRET_KEY'][:50]}...")
    print(f"   ¿Son iguales?: {app.config['SECRET_KEY'] == app.config['JWT_SECRET_KEY']}")

# 4. Probar generación y decodificación de token
print("\n4. PRUEBA DE TOKEN:")
from flask_jwt_extended import create_access_token, decode_token
import jwt as pyjwt

with app.app_context():
    # Crear token
    test_token = create_access_token(identity=1)
    print(f"   Token generado: {test_token[:50]}...")
    
    # Intentar decodificar con Flask-JWT-Extended
    try:
        decoded_flask = decode_token(test_token)
        print(f"   ✅ Decodificación con Flask-JWT-Extended: EXITOSA")
        print(f"      Identity: {decoded_flask.get('sub')}")
    except Exception as e:
        print(f"   ❌ Error con Flask-JWT-Extended: {str(e)}")
    
    # Intentar decodificar con PyJWT directamente
    try:
        decoded_pyjwt = pyjwt.decode(
            test_token,
            app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        print(f"   ✅ Decodificación con PyJWT: EXITOSA")
        print(f"      Identity: {decoded_pyjwt.get('sub')}")
    except Exception as e:
        print(f"   ❌ Error con PyJWT: {str(e)}")

# 5. Probar endpoint /api/auth/login
print("\n5. PRUEBA DE LOGIN ENDPOINT:")
from app.models.web_user import WebUser
with app.app_context():
    user = WebUser.query.filter_by(email='admin@processmart.com').first()
    if user:
        print(f"   Usuario encontrado: {user.email}")
        print(f"   Role: {user.role.name if user.role else 'N/A'}")
        token = create_access_token(identity=user.id)
        print(f"   Token generado para usuario: {token[:50]}...")
    else:
        print("   ❌ Usuario admin@processmart.com no encontrado")

print("\n" + "="*60)
print("FIN DEL DIAGNÓSTICO")
print("="*60)
