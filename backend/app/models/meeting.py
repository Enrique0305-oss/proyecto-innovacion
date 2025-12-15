"""
Modelo de Reuniones
Tabla: meetings
"""
from app.extensions import db
from datetime import datetime


class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.String(64), db.ForeignKey('projects.project_id'), nullable=False)
    meeting_date = db.Column(db.Date, nullable=False)
    meeting_time = db.Column(db.String(10))  # Formato HH:MM
    duration = db.Column(db.Integer, default=60)  # Duración en minutos
    meeting_type = db.Column(db.String(20), default='virtual')  # presencial, virtual, hibrido
    location = db.Column(db.String(255))  # Ubicación física o link de videollamada
    status = db.Column(db.String(20), default='programada')  # programada, en_curso, completada, cancelada, reprogramada
    
    # Participantes (JSON con lista de IDs de usuarios)
    participant_ids = db.Column(db.Text)  # Guardaremos como JSON string
    
    # Metadata
    created_by = db.Column(db.Integer, db.ForeignKey('web_users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    project = db.relationship('Project', backref='meetings')
    creator = db.relationship('WebUser', foreign_keys=[created_by])
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        import json
        
        participants = []
        if self.participant_ids:
            try:
                participants = json.loads(self.participant_ids)
            except:
                participants = []
        
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_id': self.project_id,
            'meeting_date': self.meeting_date.isoformat() if self.meeting_date else None,
            'meeting_time': self.meeting_time,
            'duration': self.duration,
            'meeting_type': self.meeting_type,
            'location': self.location,
            'status': self.status,
            'participants': participants,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Meeting {self.title}>'
