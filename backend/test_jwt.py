"""
Script para probar JWT completo
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.web_user import WebUser
from flask_jwt_extended import create_access_token
import requests
import json

app = create_app()

print("\n" + "="*70)
print("🔐 TEST COMPLETO DE JWT")
print("="*70)

with app.app_context():
    # 1. Verificar configuración
    print("\n1️⃣ VERIFICANDO CONFIGURACIÓN")
    print(f"   SECRET_KEY: {app.config['SECRET_KEY'][:20]}...")
    print(f"   JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY'][:20]}...")
    print(f"   JWT_EXPIRES: {app.config['JWT_ACCESS_TOKEN_EXPIRES']} segundos")
    
    # 2. Buscar usuario admin
    print("\n2️⃣ BUSCANDO USUARIO ADMIN")
    admin = WebUser.query.filter_by(email='admin@processmart.com').first()
    if not admin:
        print("   ❌ Usuario admin no encontrado")
        exit(1)
    print(f"   ✅ Usuario encontrado: {admin.email} (ID: {admin.id})")
    
    # 3. Generar token
    print("\n3️⃣ GENERANDO TOKEN JWT")
    token = create_access_token(identity=admin.id)
    print(f"   ✅ Token generado: {token[:50]}...")
    
    # 4. Guardar token para usar en frontend
    print("\n4️⃣ GUARDANDO TOKEN PARA PRUEBAS")
    with open('test_token.txt', 'w') as f:
        f.write(token)
    print("   ✅ Token guardado en test_token.txt")

print("\n" + "="*70)
print("🧪 PROBANDO API CON EL TOKEN")
print("="*70)

# 5. Probar login endpoint
print("\n5️⃣ PROBANDO LOGIN")
try:
    response = requests.post(
        'http://127.0.0.1:5000/api/auth/login',
        json={
            'email': 'admin@processmart.com',
            'password': 'admin123'
        },
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code == 200:
        data = response.json()
        login_token = data.get('access_token')
        print(f"   ✅ Login exitoso (Status: {response.status_code})")
        print(f"   Token del login: {login_token[:50]}...")
    else:
        print(f"   ❌ Login falló (Status: {response.status_code})")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    login_token = token

# 6. Probar endpoint /persons
print("\n6️⃣ PROBANDO ENDPOINT /api/persons CON TOKEN")
try:
    response = requests.get(
        'http://127.0.0.1:5000/api/persons',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {login_token}'
        }
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ API respondió correctamente (Status: {response.status_code})")
        print(f"   Total de personas: {len(data.get('persons', []))}")
    else:
        print(f"   ❌ API falló (Status: {response.status_code})")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("✅ TEST COMPLETADO")
print("="*70)
print("\nPuedes usar este token en el frontend:")
print(f"{login_token}\n")
