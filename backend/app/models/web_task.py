"""
Modelo de Tareas Web
Tabla: web_tasks
"""
from app.extensions import db
from datetime import datetime


class WebTask(db.Model):
    __tablename__ = 'web_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(64), db.ForeignKey('projects.project_id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.Enum('alta', 'media', 'baja'), default='media')
    status = db.Column(
        db.Enum('pendiente', 'en_progreso', 'completada', 'retrasada', 'cancelada'),
        default='pendiente'
    )
    area = db.Column(db.String(100))
    assigned_to = db.Column(db.String(64))  # person_id
    complexity_score = db.Column(db.Integer)  # 1-10
    estimated_hours = db.Column(db.Numeric(10, 2))
    actual_hours = db.Column(db.Numeric(10, 2))
    deadline = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('web_users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        # Buscar el nombre completo del usuario asignado
        assigned_name = None
        if self.assigned_to:
            from app.models.web_user import WebUser
            user = WebUser.query.filter_by(email=self.assigned_to).first()
            if user:
                assigned_name = user.full_name
        
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'area': self.area,
            'assigned_to': self.assigned_to,
            'assigned_name': assigned_name,  # Nombre completo del usuario
            'complexity_score': self.complexity_score,
            'estimated_hours': float(self.estimated_hours) if self.estimated_hours else None,
            'actual_hours': float(self.actual_hours) if self.actual_hours else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<WebTask {self.title}>'
