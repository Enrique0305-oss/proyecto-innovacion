"""
Modelo de Usuarios Web
Tabla: web_users
"""
from app.extensions import db
from datetime import datetime
import bcrypt


class WebUser(db.Model):
    __tablename__ = 'web_users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    area = db.Column(db.String(100))
    person_id = db.Column(db.String(64))
    status = db.Column(db.Enum('active', 'inactive'), default='active')
    avatar_url = db.Column(db.String(255))
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Métricas profesionales para ML
    experience_years = db.Column(db.Integer, default=2)
    performance_index = db.Column(db.Float, default=50.0)
    rework_rate = db.Column(db.Float, default=0.10)
    satisfaction_score = db.Column(db.Float, default=3.0)
    current_load = db.Column(db.Integer, default=0)
    tasks_completed = db.Column(db.Integer, default=0)
    availability_hours_week = db.Column(db.Float, default=40.0)
    
    # Relaciones
    created_tasks = db.relationship('WebTask', backref='creator', lazy=True, foreign_keys='WebTask.created_by')
    
    def set_password(self, password):
        """Hash de la contraseña con bcrypt"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def can(self, permission):
        """Verifica si el usuario tiene un permiso específico"""
        if not self.role:
            return False
        return self.role.has_permission(permission)
    
    def to_dict(self, include_role=True):
        """Convierte el modelo a diccionario"""
        data = {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role_id': self.role_id,
            'area': self.area,
            'person_id': self.person_id,
            'status': self.status,
            'avatar_url': self.avatar_url,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Métricas de desempeño
            'experience_years': self.experience_years,
            'performance_index': float(self.performance_index) if self.performance_index else 50.0,
            'rework_rate': float(self.rework_rate) if self.rework_rate else 0.10,
            'satisfaction_score': float(self.satisfaction_score) if self.satisfaction_score else 3.0,
            'current_load': int(self.current_load) if self.current_load else 0,
            'tasks_completed': self.tasks_completed,
            'availability_hours_week': float(self.availability_hours_week) if self.availability_hours_week else 40.0
        }
        
        if include_role and self.role:
            data['role'] = self.role.to_dict()
        
        return data
    
    def __repr__(self):
        return f'<WebUser {self.email}>'
