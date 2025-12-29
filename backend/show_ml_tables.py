"""
Ver estructura de tablas ML
"""
import sys
sys.path.insert(0, 'D:/proyecto-innovacion/backend')

from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

tables = [
    'ml_models',
    'ml_datasets', 
    'ml_training_jobs',
    'training_schedules',
    'ml_predictions'
]

with app.app_context():
    print("="*100)
    print("ESTRUCTURA DE TABLAS ML")
    print("="*100)
    
    for table in tables:
        print(f"\n📋 Tabla: {table}")
        print("-"*100)
        
        # Ver columnas
        columns = db.session.execute(text(f"DESCRIBE {table}")).fetchall()
        
        print(f"{'Columna':<30} {'Tipo':<25} {'Null':<10} {'Default':<15}")
        print("-"*100)
        
        for col in columns:
            default = str(col[4])[:15] if col[4] else '-'
            print(f"{col[0]:<30} {col[1]:<25} {col[2]:<10} {default:<15}")
        
        # Ver contenido
        count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()[0]
        print(f"\n📊 Registros: {count}")
        
        if count > 0:
            print("\n🔍 Datos:")
            rows = db.session.execute(text(f"SELECT * FROM {table} LIMIT 3")).fetchall()
            for row in rows:
                print(f"   {dict(row._mapping)}")
    
    print("\n" + "="*100)
