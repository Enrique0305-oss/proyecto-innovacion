"""
Modelo de Persona (People)
Basado en la tabla 'people' de la base de datos
"""
from datetime import datetime
from app.extensions import db


class Person(db.Model):
    """
    Modelo de Persona
    
    Representa a los empleados/personas del sistema
    """
    __tablename__ = 'people'
    
    # ID principal
    person_id = db.Column(db.String(64), primary_key=True, nullable=False)
    
    # Información profesional
    area = db.Column(db.String(64))
    role = db.Column(db.String(64))
    experience_years = db.Column(db.Numeric(4, 1))
    skills = db.Column(db.JSON)
    certifications = db.Column(db.Text)
    
    # Disponibilidad y carga
    availability_hours_week = db.Column(db.Numeric(5, 2))
    current_load = db.Column(db.Numeric(5, 2))
    tasks_assigned = db.Column(db.Integer)
    
    # Métricas de desempeño
    performance_index = db.Column(db.Numeric(5, 2))
    rework_rate = db.Column(db.Numeric(5, 2))
    absences = db.Column(db.Integer)
    
    # Información personal
    gender = db.Column(db.String(20))
    age = db.Column(db.Integer)
    hire_date = db.Column(db.Date)
    education_level = db.Column(db.String(50))
    
    # Información laboral
    monthly_salary = db.Column(db.Numeric(10, 2))
    overtime_hours = db.Column(db.Integer)
    remote_work_frequency = db.Column(db.Integer)  # Porcentaje
    team_size = db.Column(db.Integer)
    training_hours = db.Column(db.Integer)
    promotions = db.Column(db.Integer)
    
    # Satisfacción y retención
    satisfaction_score = db.Column(db.Numeric(3, 2))
    resigned = db.Column(db.Boolean, default=False)
    
    # Relaciones
    assigned_tasks = db.relationship('Assignee', back_populates='person', lazy='dynamic')
    
    def to_dict(self, include_tasks=False):
        """
        Convierte la persona a diccionario
        
        Args:
            include_tasks: Si se deben incluir las tareas asignadas
            
        Returns:
            dict: Representación de la persona
        """
        data = {
            'person_id': self.person_id,
            'area': self.area,
            'role': self.role,
            'experience_years': float(self.experience_years) if self.experience_years else None,
            'skills': self.skills,
            'certifications': self.certifications,
            'availability_hours_week': float(self.availability_hours_week) if self.availability_hours_week else None,
            'current_load': float(self.current_load) if self.current_load else None,
            'tasks_assigned': self.tasks_assigned,
            'performance_index': float(self.performance_index) if self.performance_index else None,
            'rework_rate': float(self.rework_rate) if self.rework_rate else None,
            'absences': self.absences,
            'gender': self.gender,
            'age': self.age,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'education_level': self.education_level,
            'monthly_salary': float(self.monthly_salary) if self.monthly_salary else None,
            'overtime_hours': self.overtime_hours,
            'remote_work_frequency': self.remote_work_frequency,
            'team_size': self.team_size,
            'training_hours': self.training_hours,
            'promotions': self.promotions,
            'satisfaction_score': float(self.satisfaction_score) if self.satisfaction_score else None,
            'resigned': self.resigned
        }
        
        if include_tasks:
            data['tasks'] = [a.to_dict() for a in self.assigned_tasks.limit(100)]
        
        return data
    
    def __repr__(self):
        return f'<Person {self.person_id} - {self.role}>'
