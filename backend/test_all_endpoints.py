"""
Script para probar todos los endpoints del backend
Ejecutar: python test_all_endpoints.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"
token = None

def print_result(name, response):
    """Imprime el resultado de una petición"""
    status = "✅" if response.status_code < 400 else "❌"
    print(f"{status} {name}: {response.status_code}")
    if response.status_code >= 400:
        try:
            print(f"   Error: {response.json()}")
        except:
            print(f"   Error: {response.text}")

def test_health():
    """Probar health check"""
    print("\n🔍 PROBANDO HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    print_result("GET /health", response)
    
    response = requests.get(f"{BASE_URL}/")
    print_result("GET /", response)

def test_auth():
    """Probar endpoints de autenticación"""
    global token
    print("\n🔐 PROBANDO AUTENTICACIÓN")
    
    # Login
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "admin@processmart.com",
        "password": "admin123"
    })
    print_result("POST /api/auth/login", response)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"   Token obtenido: {token[:30]}...")
    
    # Get current user
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print_result("GET /api/auth/me", response)

def test_tasks():
    """Probar endpoints de tareas"""
    print("\n📋 PROBANDO TAREAS")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get tasks
    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    print_result("GET /api/tasks", response)
    
    # Get stats
    response = requests.get(f"{BASE_URL}/api/tasks/stats", headers=headers)
    print_result("GET /api/tasks/stats", response)
    
    # Create task
    response = requests.post(f"{BASE_URL}/api/tasks", 
        headers=headers,
        json={
            "title": "Tarea de Prueba",
            "description": "Esta es una tarea de prueba",
            "priority": "media",
            "area": "TI",
            "estimated_hours": 5
        }
    )
    print_result("POST /api/tasks", response)

def test_areas():
    """Probar endpoints de áreas"""
    print("\n🏢 PROBANDO ÁREAS")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get areas
    response = requests.get(f"{BASE_URL}/api/areas", headers=headers)
    print_result("GET /api/areas", response)

def test_users():
    """Probar endpoints de usuarios"""
    print("\n👥 PROBANDO USUARIOS")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get users
    response = requests.get(f"{BASE_URL}/api/users", headers=headers)
    print_result("GET /api/users", response)
    
    # Get roles
    response = requests.get(f"{BASE_URL}/api/users/roles", headers=headers)
    print_result("GET /api/users/roles", response)

def test_persons():
    """Probar endpoints de personas"""
    print("\n👤 PROBANDO PERSONAS")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get persons
    response = requests.get(f"{BASE_URL}/api/persons", headers=headers)
    print_result("GET /api/persons", response)
    
    # Get stats
    response = requests.get(f"{BASE_URL}/api/persons/stats", headers=headers)
    print_result("GET /api/persons/stats", response)

def test_ml():
    """Probar endpoints de ML"""
    print("\n🤖 PROBANDO MACHINE LEARNING")
    headers = {"Authorization": f"Bearer {token}"}
    
    # ML health
    response = requests.get(f"{BASE_URL}/api/ml/health", headers=headers)
    print_result("GET /api/ml/health", response)

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PROBANDO TODOS LOS ENDPOINTS DEL BACKEND")
    print("=" * 60)
    
    try:
        test_health()
        test_auth()
        
        if token:
            test_tasks()
            test_areas()
            test_users()
            test_persons()
            test_ml()
        else:
            print("\n❌ No se pudo obtener token, saltando pruebas autenticadas")
        
        print("\n" + "=" * 60)
        print("✅ PRUEBAS COMPLETADAS")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
