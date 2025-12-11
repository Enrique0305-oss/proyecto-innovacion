"""
Modelo de Proyecto
Tabla: projects
"""
from datetime import datetime
from app.extensions import db
from sqlalchemy import Enum


class Project(db.Model):
    """
    Modelo de Proyecto
    
    Agrupa tareas relacionadas y permite simulación de flujo,
    análisis de camino crítico y optimización con Monte Carlo
    """
    __tablename__ = 'projects'
    
    # ID principal
    project_id = db.Column(db.String(64), primary_key=True, nullable=False)
    
    # Información básica
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Fechas
    start_date = db.Column(db.Date)
    expected_end_date = db.Column(db.Date)
    actual_end_date = db.Column(db.Date)
    
    # Estado y prioridad
    status = db.Column(
        Enum('planning', 'in_progress', 'completed', 'on_hold', 'cancelled'),
        default='planning'
    )
    priority = db.Column(
        Enum('low', 'medium', 'high', 'critical'),
        default='medium'
    )
    
    # Métricas
    budget = db.Column(db.Numeric(15, 2))
    progress_percentage = db.Column(db.Numeric(5, 2), default=0.00)
    
    # Gestión
    manager_id = db.Column(db.Integer, db.ForeignKey('web_users.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    tasks = db.relationship('WebTask', backref='project', lazy='dynamic')
    # Note: dependencies se accede via WebTaskDependency.query.filter_by(project_id=...)
    # para evitar conflictos con TaskDependency del sistema de entrenamiento
    
    def to_dict(self, include_tasks=False, include_stats=False):
        """Convierte el modelo a diccionario"""
        # Obtener nombre del manager si existe
        manager_name = None
        if self.manager_id:
            from app.models.web_user import WebUser
            manager = WebUser.query.get(self.manager_id)
            if manager:
                manager_name = manager.full_name
        
        data = {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'expected_end_date': self.expected_end_date.isoformat() if self.expected_end_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'status': self.status,
            'priority': self.priority,
            'budget': float(self.budget) if self.budget else None,
            'progress_percentage': float(self.progress_percentage) if self.progress_percentage else 0.0,
            'manager_id': self.manager_id,
            'manager_name': manager_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_stats:
            data['stats'] = self.get_stats()
        
        if include_tasks:
            from app.models.task_dependency import WebTaskDependency
            data['tasks'] = [task.to_dict() for task in self.tasks.all()]
            dependencies = WebTaskDependency.query.filter_by(project_id=self.project_id).all()
            data['dependencies'] = [dep.to_dict() for dep in dependencies]
        
        return data
    
    def get_stats(self):
        """Calcula estadísticas del proyecto"""
        tasks = self.tasks.all()
        
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == 'completada')
        in_progress_tasks = sum(1 for t in tasks if t.status == 'en_progreso')
        pending_tasks = sum(1 for t in tasks if t.status == 'pendiente')
        
        # Team size
        team_members = set(t.assigned_to for t in tasks if t.assigned_to)
        
        # Dependencies
        from app.models.task_dependency import WebTaskDependency
        dependencies_count = WebTaskDependency.query.filter_by(project_id=self.project_id).count()
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'pending_tasks': pending_tasks,
            'completion_percentage': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,
            'team_size': len(team_members),
            'dependencies_count': dependencies_count
        }
    
    def get_task_graph(self):
        """
        Construye el grafo de tareas para GNN
        
        Returns:
            dict: {
                'nodes': [list of tasks],
                'edges': [list of dependencies]
            }
        """
        from app.models.task_dependency import WebTaskDependency
        
        nodes = []
        for task in self.tasks.all():
            nodes.append({
                'id': task.id,
                'title': task.title,
                'status': task.status,
                'estimated_hours': float(task.estimated_hours) if task.estimated_hours else 0,
                'complexity_score': float(task.complexity_score) if task.complexity_score else 1
            })
        
        edges = []
        dependencies = WebTaskDependency.query.filter_by(project_id=self.project_id).all()
        for dep in dependencies:
            edges.append({
                'source': dep.predecessor_task_id,
                'target': dep.successor_task_id,
                'type': dep.dependency_type,
                'lag_days': dep.lag_days
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def __repr__(self):
        return f'<Project {self.project_id}: {self.name}>'
