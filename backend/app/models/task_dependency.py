"""
Modelo de Dependencias entre Tareas
Tabla: task_dependencies
"""
from datetime import datetime
from app.extensions import db
from sqlalchemy import Enum


class WebTaskDependency(db.Model):
    """
    Modelo de Dependencia entre Tareas
    
    Representa las relaciones de precedencia entre tareas
    Usado por GNN para construir el grafo de dependencias
    """
    __tablename__ = 'web_task_dependencies'
    
    # ID principal
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Relaciones
    project_id = db.Column(db.String(64), db.ForeignKey('projects.project_id'), nullable=False)
    predecessor_task_id = db.Column(db.Integer, db.ForeignKey('web_tasks.id'), nullable=False)
    successor_task_id = db.Column(db.Integer, db.ForeignKey('web_tasks.id'), nullable=False)
    
    # Tipo de dependencia
    dependency_type = db.Column(
        Enum('finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish'),
        default='finish_to_start',
        nullable=False
    )
    
    # Lag (tiempo de espera entre tareas)
    lag_days = db.Column(db.Integer, default=0, comment='Días de espera (puede ser negativo)')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones inversas para navegación
    predecessor_task = db.relationship(
        'app.models.web_task.WebTask',
        foreign_keys=[predecessor_task_id],
        backref='web_successors'
    )
    successor_task = db.relationship(
        'app.models.web_task.WebTask',
        foreign_keys=[successor_task_id],
        backref='web_predecessors'
    )
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'predecessor_task_id': self.predecessor_task_id,
            'successor_task_id': self.successor_task_id,
            'dependency_type': self.dependency_type,
            'lag_days': self.lag_days,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_blocking(self):
        """
        Verifica si esta dependencia está bloqueando el sucesor
        
        Returns:
            bool: True si el predecesor no está completado
        """
        if not self.predecessor_task:
            return False
        
        return self.predecessor_task.status != 'completada'
    
    def get_edge_status(self):
        """
        Calcula el estado de la relación de dependencia
        
        Returns:
            str: 'completed', 'active', 'blocked', 'ready'
        """
        if not self.predecessor_task or not self.successor_task:
            return 'unknown'
        
        if self.predecessor_task.status == 'completada':
            return 'completed'
        elif self.predecessor_task.status == 'en_progreso':
            return 'active'
        elif self.successor_task.status != 'pendiente' and self.predecessor_task.status == 'pendiente':
            return 'blocked'
        else:
            return 'ready'
    
    def __repr__(self):
        return f'<WebTaskDependency {self.predecessor_task_id} -> {self.successor_task_id}>'
