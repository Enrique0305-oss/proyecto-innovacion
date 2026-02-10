"""
Script para limpiar registros de prueba y reiniciar IDs de ml_models
Elimina los primeros 5 registros y reinicia el AUTO_INCREMENT
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.ml_models import MLModel


def clean_ml_models():
    """Elimina registros de prueba y reinicia IDs"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("LIMPIEZA DE TABLA ml_models")
        print("="*70 + "\n")
        
        # Mostrar registros actuales
        all_models = MLModel.query.order_by(MLModel.id).all()
        print(f" Total de modelos: {len(all_models)}\n")
        
        for model in all_models:
            print(f"ID {model.id}: {model.name} ({model.type})")
            print(f"   Archivo: {model.model_path}")
            print()
        
        # Eliminar registros 1-5 (datos de prueba)
        print("\n  Eliminando registros de prueba (IDs 1-5)...\n")
        
        deleted_count = 0
        for model_id in range(1, 6):
            model = MLModel.query.get(model_id)
            if model:
                print(f"   ✓ Eliminando ID {model_id}: {model.name}")
                db.session.delete(model)
                deleted_count += 1
        
        db.session.commit()
        print(f"\n {deleted_count} registros eliminados\n")
        
        # Reiniciar AUTO_INCREMENT
        print(" Reiniciando AUTO_INCREMENT...\n")
        
        # Obtener IDs actuales
        remaining_models = MLModel.query.order_by(MLModel.id).all()
        
        if remaining_models:
            # Deshabilitar foreign key checks temporalmente
            db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Crear tabla temporal
            db.session.execute(db.text("""
                CREATE TEMPORARY TABLE ml_models_temp LIKE ml_models
            """))
            
            # Copiar datos a tabla temporal
            db.session.execute(db.text("""
                INSERT INTO ml_models_temp 
                SELECT * FROM ml_models ORDER BY id
            """))
            
            # Vaciar tabla original
            db.session.execute(db.text("TRUNCATE TABLE ml_models"))
            
            # Copiar de vuelta (AUTO_INCREMENT se reinicia)
            db.session.execute(db.text("""
                INSERT INTO ml_models 
                SELECT NULL as id, name, type, algorithm, version, `precision`, 
                       recall_score, f1_score, mae, rmse, r2_score, status, 
                       model_path, samples_count, features_used, hyperparameters, 
                       metrics, description, last_trained, created_at, updated_at
                FROM ml_models_temp ORDER BY id
            """))
            
            # Eliminar tabla temporal
            db.session.execute(db.text("DROP TEMPORARY TABLE ml_models_temp"))
            
            # Reactivar foreign key checks
            db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
            
            db.session.commit()
            
            print(" AUTO_INCREMENT reiniciado\n")
        
        # Mostrar resultado final
        print("\n" + "="*70)
        print("RESULTADO FINAL")
        print("="*70 + "\n")
        
        final_models = MLModel.query.order_by(MLModel.id).all()
        print(f" Total de modelos: {len(final_models)}\n")
        
        for model in final_models:
            print(f"ID {model.id}: {model.name}")
            print(f"   Tipo: {model.type}")
            print(f"   Archivo: {model.model_path}")
            print(f"   Última actualización: {model.last_trained or 'N/A'}")
            print()
        
        print("="*70)
        print(" Limpieza completada exitosamente")
        print("="*70 + "\n")


if __name__ == '__main__':
    clean_ml_models()
