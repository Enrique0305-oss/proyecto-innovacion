"""
Script de prueba de endpoints del backend
Prueba login, creación de tareas y áreas
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_login():
    """Probar login"""
    print("\n" + "="*60)
    print("🔐 TEST: LOGIN")
    print("="*60)
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "admin@processmart.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login exitoso")
            print(f"   Usuario: {result['user']['email']}")
            print(f"   Rol: {result['user']['role']['name']}")
            print(f"   Token: {result['access_token'][:50]}...")
            return result['access_token']
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None


def test_get_areas(token):
    """Listar áreas"""
    print("\n" + "="*60)
    print("📁 TEST: LISTAR ÁREAS")
    print("="*60)
    
    url = f"{BASE_URL}/areas/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Áreas encontradas: {result['total']}")
            for area in result['areas'][:5]:
                print(f"   - {area['name']}")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_create_task(token):
    """Crear tarea de prueba"""
    print("\n" + "="*60)
    print("📝 TEST: CREAR TAREA")
    print("="*60)
    
    url = f"{BASE_URL}/tasks/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Tarea de prueba desde API",
        "description": "Esta es una tarea creada para probar el backend",
        "priority": "alta",
        "area": "IT",
        "complexity_score": 7,
        "estimated_hours": 8
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Tarea creada")
            print(f"   ID: {result['task']['id']}")
            print(f"   Título: {result['task']['title']}")
            print(f"   Estado: {result['task']['status']}")
            return result['task']['id']
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_get_tasks(token):
    """Listar tareas"""
    print("\n" + "="*60)
    print("📋 TEST: LISTAR TAREAS")
    print("="*60)
    
    url = f"{BASE_URL}/tasks/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Tareas encontradas: {result['total']}")
            for task in result['tasks'][:3]:
                print(f"   - {task['title']} ({task['status']})")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_stats(token):
    """Obtener estadísticas"""
    print("\n" + "="*60)
    print("📊 TEST: ESTADÍSTICAS")
    print("="*60)
    
    url = f"{BASE_URL}/tasks/stats"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Estadísticas obtenidas:")
            print(f"   Total tareas: {result['total_tasks']}")
            print(f"   Completadas: {result['completed']}")
            print(f"   En progreso: {result['in_progress']}")
            print(f"   Pendientes: {result['pending']}")
            print(f"   Tasa de completado: {result['completion_rate']}%")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    print("\n🚀 INICIANDO PRUEBAS DEL BACKEND FLASK")
    print("Asegúrate de que el servidor esté corriendo en http://127.0.0.1:5000")
    
    # 1. Login
    token = test_login()
    
    if token:
        # 2. Listar áreas
        test_get_areas(token)
        
        # 3. Crear tarea
        task_id = test_create_task(token)
        
        # 4. Listar tareas
        test_get_tasks(token)
        
        # 5. Estadísticas
        test_stats(token)
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60 + "\n")
