"""
Modelo de Usuario para autenticación
Sistema básico de usuarios para el sistema
"""
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    Modelo de Usuario
    
    Tabla para gestión de usuarios del sistema
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Información adicional
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(50), default='user')  # admin, user, analyst
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __init__(self, username, email, password, **kwargs):
        """
        Constructor del Usuario
        
        Args:
            username: Nombre de usuario único
            email: Email único
            password: Contraseña en texto plano (se hashea automáticamente)
        """
        self.username = username
        self.email = email
        self.set_password(password)
        
        # Campos opcionales
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.role = kwargs.get('role', 'user')
        self.is_active = kwargs.get('is_active', True)
    
    def set_password(self, password):
        """
        Hashea y guarda la contraseña
        
        Args:
            password: Contraseña en texto plano
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verifica si la contraseña es correcta
        
        Args:
            password: Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """
        Convierte el usuario a diccionario (sin contraseña)
        
        Returns:
            dict: Representación del usuario
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
