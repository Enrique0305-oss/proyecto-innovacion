"""
Script para crear la tabla meetings
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.meeting import Meeting

def create_meetings_table():
    """Crea la tabla meetings si no existe"""
    app = create_app()
    
    with app.app_context():
        try:
            # Crear la tabla
            db.create_all()
            print("✅ Tabla meetings creada exitosamente")
            
        except Exception as e:
            print(f"❌ Error al crear tabla meetings: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    create_meetings_table()
