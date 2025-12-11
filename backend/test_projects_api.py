"""
Test de endpoints de proyectos
"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_get_projects():
    """Test GET /projects"""
    print("\n1. TEST: GET /api/projects")
    print("="*50)
    
    response = requests.get(f'{BASE_URL}/projects?include_stats=true')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total proyectos: {data['count']}")
        for project in data['projects']:
            print(f"  - {project['project_id']}: {project['name']} ({project['status']})")
            if 'stats' in project:
                print(f"    Stats: {project['stats']}")
    else:
        print(f"Error: {response.text}")

def test_get_project_detail():
    """Test GET /projects/{id}"""
    print("\n2. TEST: GET /api/projects/PROJ-2025-001")
    print("="*50)
    
    response = requests.get(f'{BASE_URL}/projects/PROJ-2025-001?include_stats=true&include_tasks=true')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        project = data['project']
        print(f"Proyecto: {project['name']}")
        print(f"Manager ID: {project['manager_id']}")
        print(f"Tareas: {len(project.get('tasks', []))}")
        print(f"Stats: {project.get('stats', {})}")
    else:
        print(f"Error: {response.text}")

def test_create_project():
    """Test POST /projects"""
    print("\n3. TEST: POST /api/projects")
    print("="*50)
    
    new_project = {
        "project_id": "PROJ-TEST-001",
        "name": "Proyecto de Prueba",
        "description": "Proyecto creado desde test",
        "status": "planning",
        "priority": "medium",
        "start_date": "2025-12-15",
        "expected_end_date": "2026-06-15",
        "manager_id": 1
    }
    
    response = requests.post(
        f'{BASE_URL}/projects',
        json=new_project,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"✓ Proyecto creado: {data['project']['project_id']}")
    else:
        print(f"Error: {response.text}")

def test_get_project_graph():
    """Test GET /projects/{id}/graph"""
    print("\n4. TEST: GET /api/projects/PROJ-DEFAULT/graph")
    print("="*50)
    
    response = requests.get(f'{BASE_URL}/projects/PROJ-DEFAULT/graph')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        graph = data['graph']
        print(f"Nodos (tareas): {len(graph['nodes'])}")
        print(f"Edges (dependencias): {len(graph['edges'])}")
        for node in graph['nodes'][:3]:  # Mostrar solo 3
            print(f"  - Tarea {node['id']}: {node['title']}")
    else:
        print(f"Error: {response.text}")

def test_create_dependency():
    """Test POST /dependencies"""
    print("\n5. TEST: POST /api/dependencies")
    print("="*50)
    
    # Primero obtener tareas del proyecto
    response = requests.get(f'{BASE_URL}/projects/PROJ-DEFAULT?include_tasks=true')
    if response.status_code == 200:
        tasks = response.json()['project']['tasks']
        if len(tasks) >= 2:
            task1_id = tasks[0]['id']
            task2_id = tasks[1]['id']
            
            dependency = {
                "project_id": "PROJ-DEFAULT",
                "predecessor_task_id": task1_id,
                "successor_task_id": task2_id,
                "dependency_type": "finish_to_start",
                "lag_days": 1
            }
            
            response = requests.post(
                f'{BASE_URL}/dependencies',
                json=dependency,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                print(f"✓ Dependencia creada: {task1_id} -> {task2_id}")
            else:
                print(f"Error: {response.text}")
        else:
            print("No hay suficientes tareas para crear dependencia")
    else:
        print(f"Error obteniendo proyecto: {response.text}")

def test_get_dependencies():
    """Test GET /projects/{id}/dependencies"""
    print("\n6. TEST: GET /api/projects/PROJ-DEFAULT/dependencies")
    print("="*50)
    
    response = requests.get(f'{BASE_URL}/projects/PROJ-DEFAULT/dependencies')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total dependencias: {data['count']}")
        for dep in data['dependencies']:
            print(f"  - {dep['predecessor_task_id']} -> {dep['successor_task_id']} ({dep['dependency_type']})")
    else:
        print(f"Error: {response.text}")

def test_critical_path():
    """Test GET /projects/{id}/critical-path"""
    print("\n7. TEST: GET /api/projects/PROJ-DEFAULT/critical-path")
    print("="*50)
    
    response = requests.get(f'{BASE_URL}/projects/PROJ-DEFAULT/critical-path')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        candidates = data['critical_path_candidates']
        print(f"Candidatos a camino crítico: {len(candidates)}")
        for i, cand in enumerate(candidates[:5]):
            task = cand['task']
            print(f"  {i+1}. {task['title']} - Conexiones: {cand['total_connections']}")
    else:
        print(f"Error: {response.text}")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("TEST DE ENDPOINTS DE PROYECTOS")
    print("="*50)
    
    try:
        test_get_projects()
        test_get_project_detail()
        test_create_project()
        test_get_project_graph()
        test_create_dependency()
        test_get_dependencies()
        test_critical_path()
        
        print("\n" + "="*50)
        print("✅ TESTS COMPLETADOS")
        print("="*50)
    except Exception as e:
        print(f"\n❌ Error en tests: {e}")
