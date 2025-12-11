"""
Modelos de Tareas
Basado en las tablas 'tasks', 'assignees' y 'task_dependencies'
"""
from datetime import datetime
from app.extensions import db


class Task(db.Model):
    """
    Modelo de Tarea
    
    Representa las tareas/proyectos del sistema
    """
    __tablename__ = 'tasks'
    
    # ID principal
    task_id = db.Column(db.String(64), primary_key=True, nullable=False)
    
    # Información del proyecto
    project_id = db.Column(db.String(64))
    area = db.Column(db.String(100))
    task_name = db.Column(db.String(255))
    task_type = db.Column(db.String(200))
    
    # Fechas estimadas
    start_date_est = db.Column(db.Date)
    end_date_est = db.Column(db.Date)
    
    # Fechas reales
    start_date_real = db.Column(db.Date)
    end_date_real = db.Column(db.Date)
    
    # Duración
    duration_est = db.Column(db.Numeric(10, 2))
    duration_real = db.Column(db.Numeric(10, 2))
    
    # Estado y prioridad
    status = db.Column(db.String(100))
    priority = db.Column(db.String(100))
    dependencies = db.Column(db.Text)
    
    # Complejidad y herramientas
    complexity_level = db.Column(db.String(100))
    tools_used = db.Column(db.Text)
    completion = db.Column(db.String(50))
    
    # Relaciones
    assignees = db.relationship('Assignee', back_populates='task', lazy='dynamic', cascade='all, delete-orphan')
    dependencies_from = db.relationship(
        'app.models.task.TaskDependency',
        foreign_keys='app.models.task.TaskDependency.task_id',
        back_populates='task',
        cascade='all, delete-orphan'
    )
    dependencies_to = db.relationship(
        'app.models.task.TaskDependency',
        foreign_keys='app.models.task.TaskDependency.depends_on_task_id',
        back_populates='depends_on_task',
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_assignees=False):
        """
        Convierte la tarea a diccionario
        
        Args:
            include_assignees: Si se deben incluir los asignados
            
        Returns:
            dict: Representación de la tarea
        """
        data = {
            'task_id': self.task_id,
            'project_id': self.project_id,
            'area': self.area,
            'task_name': self.task_name,
            'task_type': self.task_type,
            'start_date_est': self.start_date_est.isoformat() if self.start_date_est else None,
            'end_date_est': self.end_date_est.isoformat() if self.end_date_est else None,
            'start_date_real': self.start_date_real.isoformat() if self.start_date_real else None,
            'end_date_real': self.end_date_real.isoformat() if self.end_date_real else None,
            'duration_est': float(self.duration_est) if self.duration_est else None,
            'duration_real': float(self.duration_real) if self.duration_real else None,
            'status': self.status,
            'priority': self.priority,
            'dependencies': self.dependencies,
            'complexity_level': self.complexity_level,
            'tools_used': self.tools_used,
            'completion': self.completion
        }
        
        if include_assignees:
            data['assignees'] = [a.to_dict() for a in self.assignees]
            data['assignees_count'] = self.assignees.count()
        
        return data
    
    def __repr__(self):
        return f'<Task {self.task_id} - {self.task_name}>'


class Assignee(db.Model):
    """
    Modelo de Asignación de Persona a Tarea
    
    Tabla intermedia entre Task y Person
    """
    __tablename__ = 'assignees'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(64), db.ForeignKey('tasks.task_id'), nullable=False)
    person_id = db.Column(db.String(64), db.ForeignKey('people.person_id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    task = db.relationship('Task', back_populates='assignees')
    person = db.relationship('Person', back_populates='assigned_tasks')
    
    def to_dict(self):
        """Convierte la asignación a diccionario"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'person_id': self.person_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None
        }
    
    def __repr__(self):
        return f'<Assignee Task:{self.task_id} Person:{self.person_id}>'


class TaskDependency(db.Model):
    """
    Modelo de Dependencias entre Tareas
    
    Representa las relaciones de dependencia entre tareas
    """
    __tablename__ = 'task_dependencies'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(64), db.ForeignKey('tasks.task_id'), nullable=False)
    depends_on_task_id = db.Column(db.String(64), db.ForeignKey('tasks.task_id'), nullable=False)
    
    # Relaciones
    task = db.relationship(
        'app.models.task.Task',
        foreign_keys=[task_id],
        back_populates='dependencies_from'
    )
    depends_on_task = db.relationship(
        'app.models.task.Task',
        foreign_keys=[depends_on_task_id],
        back_populates='dependencies_to'
    )
    
    def to_dict(self):
        """Convierte la dependencia a diccionario"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'depends_on_task_id': self.depends_on_task_id
        }
    
    def __repr__(self):
        return f'<TaskDependency {self.task_id} depends on {self.depends_on_task_id}>'
