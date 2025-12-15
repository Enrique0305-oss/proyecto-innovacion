from app.extensions import db
from datetime import datetime

class TrainingSchedule(db.Model):
    __tablename__ = 'training_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String(50), nullable=False)  # 'attrition', 'duration', 'performance', etc.
    scheduled_date = db.Column(db.Date, nullable=False)
    scheduled_time = db.Column(db.String(10), nullable=False)  # formato HH:MM
    status = db.Column(db.String(20), default='programado')  # programado, ejecutando, completado, fallido
    parameters = db.Column(db.Text)  # JSON con parámetros de entrenamiento
    last_execution = db.Column(db.DateTime)
    execution_result = db.Column(db.Text)  # Resultado del último entrenamiento
    created_by = db.Column(db.Integer, db.ForeignKey('web_users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos para reentrenamiento recurrente
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(20))  # 'daily', 'weekly', 'monthly'
    
    def to_dict(self):
        return {
            'id': self.id,
            'model_type': self.model_type,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'scheduled_time': self.scheduled_time,
            'status': self.status,
            'parameters': self.parameters,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None,
            'execution_result': self.execution_result,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_recurring': self.is_recurring,
            'recurrence_pattern': self.recurrence_pattern
        }
