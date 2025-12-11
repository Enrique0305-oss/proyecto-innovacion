"""
Process Mining - Análisis de Procesos
Analiza flujos de trabajo, cuellos de botella y patrones en las tareas
"""
import os
import joblib
from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy import and_, func

from app.extensions import db
from app.models.task import Task
from app.models.task import TaskDependency as TrainingTaskDependency


_analyzer = None


def load_model():
    """
    Cargar modelo/analizador de procesos
    """
    global _analyzer
    
    if _analyzer is not None:
        return _analyzer
    
    try:
        # Cargar desde la misma carpeta app/ml/
        ml_path = os.path.dirname(os.path.abspath(__file__))
        model_file = os.path.join(ml_path, 'process_mining.pkl')
        
        if os.path.exists(model_file):
            _analyzer = joblib.load(model_file)
            print(f"✓ Analizador de procesos cargado: {model_file}")
        
        return _analyzer
        
    except Exception as e:
        print(f"✗ Error al cargar analizador de procesos: {str(e)}")
        return None


def analyze_process(filters):
    """
    Analizar procesos de trabajo
    
    Args:
        filters (dict):
            - area: str (opcional)
            - start_date: str (YYYY-MM-DD)
            - end_date: str (YYYY-MM-DD)
            - task_type: str
            - analysis_type: str (frequency/duration/bottleneck)
    
    Returns:
        dict:
            - flow: list[dict] (flujo de procesos)
            - bottlenecks: list[dict] (cuellos de botella)
            - avg_duration: float (duración promedio)
            - task_sequences: list[dict] (secuencias comunes)
            - insights: list[str] (insights generados)
    """
    analyzer = load_model()
    
    # Análisis heurístico si no hay modelo
    if analyzer is None:
        return analyze_process_heuristic(filters)
    
    try:
        # Usar modelo ML para análisis avanzado
        tasks = get_filtered_tasks(filters)
        
        # Aplicar modelo
        process_data = prepare_process_data(tasks)
        analysis_result = analyzer.transform(process_data)
        
        return parse_analysis_result(analysis_result, filters)
        
    except Exception as e:
        print(f"Error en process mining: {str(e)}")
        return analyze_process_heuristic(filters)


def analyze_process_heuristic(filters):
    """
    Análisis heurístico de procesos
    """
    try:
        # Obtener tareas según filtros
        tasks = get_filtered_tasks(filters)
        
        analysis_type = filters.get('analysis_type', 'general')
        
        # Análisis de flujo
        flow = analyze_task_flow(tasks)
        
        # Cuellos de botella
        bottlenecks = identify_bottlenecks(tasks)
        
        # Duración promedio
        avg_duration = calculate_average_duration(tasks)
        
        # Secuencias comunes
        sequences = find_common_sequences(tasks)
        
        # Insights
        insights = generate_insights(tasks, flow, bottlenecks, avg_duration)
        
        return {
            'flow': flow,
            'bottlenecks': bottlenecks,
            'avg_duration': avg_duration,
            'task_sequences': sequences,
            'insights': insights,
            'total_tasks_analyzed': len(tasks),
            'analysis_type': analysis_type
        }
        
    except Exception as e:
        return {
            'flow': [],
            'bottlenecks': [],
            'avg_duration': 0,
            'task_sequences': [],
            'insights': [f'Error en análisis: {str(e)}'],
            'total_tasks_analyzed': 0
        }


def get_filtered_tasks(filters):
    """
    Obtener tareas según filtros
    """
    query = Task.query
    
    # Filtro por área
    if filters.get('area'):
        query = query.filter(Task.area == filters['area'])
    
    # Filtro por tipo
    if filters.get('task_type'):
        query = query.filter(Task.task_type == filters['task_type'])
    
    # Filtro por fechas
    if filters.get('start_date'):
        try:
            start = datetime.strptime(filters['start_date'], '%Y-%m-%d')
            query = query.filter(Task.start_date_real >= start)
        except:
            pass
    
    if filters.get('end_date'):
        try:
            end = datetime.strptime(filters['end_date'], '%Y-%m-%d')
            query = query.filter(Task.end_date_real <= end)
        except:
            pass
    
    return query.all()


def analyze_task_flow(tasks):
    """
    Analizar el flujo de tareas por estado
    """
    flow = {}
    
    for task in tasks:
        status = task.status or 'Unknown'
        
        if status not in flow:
            flow[status] = {
                'count': 0,
                'avg_duration': 0,
                'tasks': []
            }
        
        flow[status]['count'] += 1
        flow[status]['tasks'].append(task.task_id)
        
        # Calcular duración si tiene fechas
        if task.start_date_real and task.end_date_real:
            duration = (task.end_date_real - task.start_date_real).days
            current_avg = flow[status]['avg_duration']
            new_avg = (current_avg * (flow[status]['count'] - 1) + duration) / flow[status]['count']
            flow[status]['avg_duration'] = round(new_avg, 1)
    
    # Convertir a lista
    flow_list = []
    for status, data in flow.items():
        flow_list.append({
            'status': status,
            'count': data['count'],
            'avg_duration_days': data['avg_duration'],
            'percentage': round((data['count'] / len(tasks)) * 100, 1) if tasks else 0
        })
    
    # Ordenar por cantidad
    flow_list.sort(key=lambda x: x['count'], reverse=True)
    
    return flow_list


def identify_bottlenecks(tasks):
    """
    Identificar cuellos de botella
    """
    bottlenecks = []
    
    # 1. Tareas con duración real > estimada
    delayed_tasks = []
    for task in tasks:
        if task.duration_real and task.duration_est:
            if task.duration_real > task.duration_est * 1.5:  # 50% más de lo estimado
                delay_percentage = ((task.duration_real - task.duration_est) / task.duration_est) * 100
                delayed_tasks.append({
                    'task_id': task.task_id,
                    'task_name': task.task_name,
                    'delay_percentage': round(delay_percentage, 1),
                    'estimated_days': task.duration_est,
                    'actual_days': task.duration_real
                })
    
    if delayed_tasks:
        bottlenecks.append({
            'type': 'delays',
            'severity': 'high' if len(delayed_tasks) > 5 else 'medium',
            'count': len(delayed_tasks),
            'description': f'{len(delayed_tasks)} tareas con retrasos significativos',
            'examples': delayed_tasks[:3]
        })
    
    # 2. Áreas con muchas tareas pendientes
    pending_by_area = {}
    for task in tasks:
        if task.status in ['Pending', 'In - Progress']:
            area = task.area or 'Unknown'
            pending_by_area[area] = pending_by_area.get(area, 0) + 1
    
    for area, count in pending_by_area.items():
        if count > 10:
            bottlenecks.append({
                'type': 'area_overload',
                'severity': 'high' if count > 20 else 'medium',
                'count': count,
                'area': area,
                'description': f'Área {area} con {count} tareas pendientes/en progreso'
            })
    
    # 3. Tareas con muchas dependencias sin completar
    for task in tasks:
        if task.status != 'Completed':
            dependencies = TrainingTaskDependency.query.filter_by(
                task_id=task.task_id
            ).count()
            
            if dependencies > 3:
                bottlenecks.append({
                    'type': 'blocked_by_dependencies',
                    'severity': 'medium',
                    'task_id': task.task_id,
                    'task_name': task.task_name,
                    'dependencies_count': dependencies,
                    'description': f'Tarea bloqueada por {dependencies} dependencias'
                })
    
    return bottlenecks


def calculate_average_duration(tasks):
    """
    Calcular duración promedio de tareas completadas
    """
    durations = []
    
    for task in tasks:
        if task.start_date_real and task.end_date_real:
            duration = (task.end_date_real - task.start_date_real).days
            durations.append(duration)
    
    if durations:
        return {
            'mean': round(sum(durations) / len(durations), 1),
            'min': min(durations),
            'max': max(durations),
            'tasks_with_duration': len(durations)
        }
    
    return {
        'mean': 0,
        'min': 0,
        'max': 0,
        'tasks_with_duration': 0
    }


def find_common_sequences(tasks):
    """
    Encontrar secuencias comunes de tareas (por tipo)
    """
    sequences = {}
    
    # Agrupar por proyecto
    by_project = {}
    for task in tasks:
        project = task.project_id or 'No Project'
        if project not in by_project:
            by_project[project] = []
        by_project[project].append(task)
    
    # Analizar secuencias en cada proyecto
    for project, project_tasks in by_project.items():
        if len(project_tasks) < 2:
            continue
        
        # Ordenar por fecha de inicio
        sorted_tasks = sorted(
            [t for t in project_tasks if t.start_date_real],
            key=lambda x: x.start_date_real
        )
        
        # Extraer secuencia de tipos
        sequence = ' -> '.join([t.task_type or 'Unknown' for t in sorted_tasks[:5]])
        
        if sequence:
            sequences[sequence] = sequences.get(sequence, 0) + 1
    
    # Convertir a lista ordenada
    sequence_list = [
        {'sequence': seq, 'frequency': freq}
        for seq, freq in sequences.items()
    ]
    sequence_list.sort(key=lambda x: x['frequency'], reverse=True)
    
    return sequence_list[:10]  # Top 10


def generate_insights(tasks, flow, bottlenecks, avg_duration):
    """
    Generar insights del análisis
    """
    insights = []
    
    # Total de tareas
    total = len(tasks)
    if total == 0:
        return ['No hay suficientes datos para generar insights']
    
    insights.append(f'Se analizaron {total} tareas en total')
    
    # Estado más común
    if flow:
        most_common = flow[0]
        insights.append(
            f'El {most_common["percentage"]}% de las tareas están en estado "{most_common["status"]}"'
        )
    
    # Duración promedio
    if avg_duration['mean'] > 0:
        insights.append(
            f'Duración promedio de tareas: {avg_duration["mean"]} días '
            f'(rango: {avg_duration["min"]}-{avg_duration["max"]} días)'
        )
    
    # Cuellos de botella
    if bottlenecks:
        high_severity = [b for b in bottlenecks if b.get('severity') == 'high']
        if high_severity:
            insights.append(
                f'⚠️ Se detectaron {len(high_severity)} cuellos de botella de alta severidad'
            )
    else:
        insights.append('✓ No se detectaron cuellos de botella significativos')
    
    # Tareas completadas
    completed = sum(1 for t in tasks if t.status == 'Completed')
    if completed > 0:
        completion_rate = (completed / total) * 100
        insights.append(f'Tasa de completitud: {round(completion_rate, 1)}%')
    
    return insights


def prepare_process_data(tasks):
    """
    Preparar datos para el modelo de process mining
    """
    # Convertir tareas a formato para el modelo
    process_data = []
    
    for task in tasks:
        process_data.append({
            'task_id': task.task_id,
            'status': task.status,
            'area': task.area,
            'task_type': task.task_type,
            'start_date': task.start_date_real,
            'end_date': task.end_date_real,
            'duration': task.duration_real
        })
    
    return process_data


def parse_analysis_result(result, filters):
    """
    Parsear resultado del modelo ML
    """
    # Implementar según el formato de salida del modelo
    return {
        'flow': result.get('flow', []),
        'bottlenecks': result.get('bottlenecks', []),
        'avg_duration': result.get('avg_duration', 0),
        'task_sequences': result.get('sequences', []),
        'insights': result.get('insights', [])
    }
