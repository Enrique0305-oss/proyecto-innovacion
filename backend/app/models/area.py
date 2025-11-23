"""
Modelo de Áreas
Tabla: areas
"""
from app.extensions import db
from datetime import datetime


class Area(db.Model):
    __tablename__ = 'areas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    supervisor_person_id = db.Column(db.String(64))
    employee_count = db.Column(db.Integer, default=0)
    efficiency_score = db.Column(db.Numeric(5, 2))
    status = db.Column(db.Enum('active', 'inactive'), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones se definirán en WebTask con foreign_keys
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'supervisor_person_id': self.supervisor_person_id,
            'employee_count': self.employee_count,
            'efficiency_score': float(self.efficiency_score) if self.efficiency_score else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Area {self.name}>'
