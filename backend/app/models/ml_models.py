"""
Modelos ML
Tablas: ml_models, ml_predictions
"""
from app.extensions import db
from datetime import datetime


class MLModel(db.Model):
    __tablename__ = 'ml_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(
        db.Enum('risk', 'duration', 'recommendation', 'performance', 'simulation'),
        nullable=False
    )
    algorithm = db.Column(db.String(50))
    version = db.Column(db.String(20), default='v1.0')
    precision = db.Column(db.Numeric(5, 2))
    recall_score = db.Column(db.Numeric(5, 2))
    f1_score = db.Column(db.Numeric(5, 2))
    mae = db.Column(db.Numeric(10, 2))
    rmse = db.Column(db.Numeric(10, 2))
    r2_score = db.Column(db.Numeric(5, 4))
    status = db.Column(
        db.Enum('activo', 'entrenando', 'error', 'deprecated'),
        default='activo'
    )
    model_path = db.Column(db.String(255), nullable=False)
    samples_count = db.Column(db.Integer)
    features_used = db.Column(db.JSON)
    hyperparameters = db.Column(db.JSON)
    metrics = db.Column(db.JSON)
    description = db.Column(db.Text)
    last_trained = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    predictions = db.relationship('MLPrediction', backref='model', lazy=True)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'algorithm': self.algorithm,
            'version': self.version,
            'precision': float(self.precision) if self.precision else None,
            'recall_score': float(self.recall_score) if self.recall_score else None,
            'f1_score': float(self.f1_score) if self.f1_score else None,
            'mae': float(self.mae) if self.mae else None,
            'rmse': float(self.rmse) if self.rmse else None,
            'r2_score': float(self.r2_score) if self.r2_score else None,
            'status': self.status,
            'model_path': self.model_path,
            'samples_count': self.samples_count,
            'features_used': self.features_used,
            'hyperparameters': self.hyperparameters,
            'metrics': self.metrics,
            'description': self.description,
            'last_trained': self.last_trained.isoformat() if self.last_trained else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<MLModel {self.name} v{self.version}>'


class MLPrediction(db.Model):
    __tablename__ = 'ml_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    task_reference = db.Column(db.String(100), nullable=False)
    task_source = db.Column(db.Enum('historical', 'web'), default='web')
    model_id = db.Column(db.Integer, db.ForeignKey('ml_models.id'))
    model_type = db.Column(
        db.Enum('risk', 'duration', 'recommendation', 'performance', 'simulation'),
        nullable=False
    )
    prediction_value = db.Column(db.JSON, nullable=False)
    confidence = db.Column(db.Numeric(5, 2))
    input_features = db.Column(db.JSON)
    actual_result = db.Column(db.JSON)
    is_correct = db.Column(db.Boolean)
    model_version = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'task_reference': self.task_reference,
            'task_source': self.task_source,
            'model_id': self.model_id,
            'model_type': self.model_type,
            'prediction_value': self.prediction_value,
            'confidence': float(self.confidence) if self.confidence else None,
            'input_features': self.input_features,
            'actual_result': self.actual_result,
            'is_correct': self.is_correct,
            'model_version': self.model_version,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<MLPrediction {self.model_type} for {self.task_reference}>'
