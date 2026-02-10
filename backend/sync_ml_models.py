"""
Script para sincronizar archivos PKL reales con la tabla ml_models
Escanea las carpetas de modelos y registra/actualiza en la BD
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.ml_models import MLModel


def get_model_file_info(model_dir):
    """Extrae información del archivo de modelo y sus métricas"""
    info = {
        'model_file': None,
        'metrics_file': None,
        'columns_file': None,
        'metrics': {},
        'file_date': None
    }
    
    # Buscar archivo de modelo (.pkl o .cbm)
    for file in os.listdir(model_dir):
        if file.endswith('.pkl') or file.endswith('.cbm'):
            info['model_file'] = os.path.join(model_dir, file)
            info['file_date'] = datetime.fromtimestamp(os.path.getmtime(info['model_file']))
        elif file.endswith('_metrics.json'):
            info['metrics_file'] = os.path.join(model_dir, file)
        elif file.startswith('columns_'):
            info['columns_file'] = os.path.join(model_dir, file)
    
    # Leer métricas si existen
    if info['metrics_file'] and os.path.exists(info['metrics_file']):
        try:
            with open(info['metrics_file'], 'r', encoding='utf-8') as f:
                info['metrics'] = json.load(f)
        except:
            pass
    
    # Leer columnas si existen
    if info['columns_file'] and os.path.exists(info['columns_file']):
        try:
            with open(info['columns_file'], 'r', encoding='utf-8') as f:
                info['columns'] = json.load(f)
        except:
            info['columns'] = []
    else:
        info['columns'] = []
    
    return info


def sync_models():
    """Sincroniza los archivos PKL con la tabla ml_models"""
    app = create_app()
    
    with app.app_context():
        models_base_path = os.path.join(os.path.dirname(__file__), 'ml', 'models')
        
        # Definir modelos a sincronizar
        models_config = {
            'risk': {
                'name': 'Clasificador de Riesgo de Tareas',
                'type': 'risk',
                'description': 'Clasifica tareas como Bajo, Medio o Alto riesgo basándose en características históricas'
            },
            'duration': {
                'name': 'Predictor de Duración de Tareas',
                'type': 'duration',
                'description': 'Predice las horas reales que tomará completar una tarea'
            },
            'recommender': {
                'name': 'Recomendador Persona-Tarea',
                'type': 'recommendation',
                'description': 'Recomienda el mejor personal para cada tarea basándose en habilidades y experiencia'
            },
            'training': {
                'name': 'Predictor de Rendimiento',
                'type': 'performance',
                'description': 'Predice el rendimiento esperado de una persona en una tarea'
            },
            'mining': {
                'name': 'Analizador de Procesos',
                'type': 'simulation',
                'description': 'Analiza y simula flujos de procesos para optimización'
            },
            'attrition': {
                'name': 'Predictor de Rotación',
                'type': 'risk',
                'description': 'Predice la probabilidad de que un empleado abandone la organización'
            }
        }
        
        synced_count = 0
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        print("\n" + "="*70)
        print("SINCRONIZACIÓN DE MODELOS PKL CON BASE DE DATOS")
        print("="*70 + "\n")
        
        for folder_name, config in models_config.items():
            model_dir = os.path.join(models_base_path, folder_name)
            
            if not os.path.exists(model_dir):
                print(f"  Carpeta no existe: {folder_name}")
                skipped_count += 1
                continue
            
            # Obtener info del archivo
            info = get_model_file_info(model_dir)
            
            if not info['model_file']:
                print(f"  No se encontró archivo PKL/CBM en: {folder_name}")
                skipped_count += 1
                continue
            
            print(f"\n Procesando: {folder_name}")
            print(f"   Archivo: {os.path.basename(info['model_file'])}")
            print(f"   Fecha del archivo: {info['file_date'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Buscar si ya existe el modelo en BD
            existing_model = MLModel.query.filter_by(
                type=config['type'],
                name=config['name']
            ).first()
            
            # Extraer métricas
            metrics_data = info['metrics']
            
            if existing_model:
                # Actualizar modelo existente
                print(f"     Actualizando modelo existente (ID: {existing_model.id})")
                
                existing_model.model_path = info['model_file']
                existing_model.last_trained = info['file_date']
                existing_model.features_used = info['columns']
                existing_model.updated_at = datetime.utcnow()
                
                # Actualizar métricas según el tipo
                if 'accuracy' in metrics_data:
                    existing_model.precision = metrics_data.get('accuracy', 0) * 100
                if 'precision' in metrics_data:
                    existing_model.precision = metrics_data.get('precision', 0) * 100
                if 'recall' in metrics_data:
                    existing_model.recall_score = metrics_data.get('recall', 0) * 100
                if 'f1_score' in metrics_data:
                    existing_model.f1_score = metrics_data.get('f1_score', 0) * 100
                if 'rmse' in metrics_data:
                    existing_model.rmse = metrics_data.get('rmse', 0)
                if 'mae' in metrics_data:
                    existing_model.mae = metrics_data.get('mae', 0)
                if 'r2' in metrics_data:
                    existing_model.r2_score = metrics_data.get('r2', 0)
                
                existing_model.metrics = metrics_data
                existing_model.algorithm = metrics_data.get('algorithm', 'CatBoost')
                existing_model.samples_count = metrics_data.get('samples', 0)
                
                updated_count += 1
                
            else:
                # Crear nuevo modelo
                print(f"    Creando nuevo registro")
                
                new_model = MLModel(
                    name=config['name'],
                    type=config['type'],
                    description=config['description'],
                    model_path=info['model_file'],
                    algorithm=metrics_data.get('algorithm', 'CatBoost'),
                    version='v1.0',
                    status='activo',
                    last_trained=info['file_date'],
                    features_used=info['columns'],
                    metrics=metrics_data,
                    samples_count=metrics_data.get('samples', 0)
                )
                
                # Asignar métricas específicas
                if 'accuracy' in metrics_data:
                    new_model.precision = metrics_data.get('accuracy', 0) * 100
                if 'precision' in metrics_data:
                    new_model.precision = metrics_data.get('precision', 0) * 100
                if 'recall' in metrics_data:
                    new_model.recall_score = metrics_data.get('recall', 0) * 100
                if 'f1_score' in metrics_data:
                    new_model.f1_score = metrics_data.get('f1_score', 0) * 100
                if 'rmse' in metrics_data:
                    new_model.rmse = metrics_data.get('rmse', 0)
                if 'mae' in metrics_data:
                    new_model.mae = metrics_data.get('mae', 0)
                if 'r2' in metrics_data:
                    new_model.r2_score = metrics_data.get('r2', 0)
                
                db.session.add(new_model)
                created_count += 1
            
            synced_count += 1
        
        # Guardar cambios
        try:
            db.session.commit()
            print("\n" + "="*70)
            print("RESUMEN DE SINCRONIZACIÓN")
            print("="*70)
            print(f" Modelos procesados: {synced_count}")
            print(f" Nuevos creados: {created_count}")
            print(f" Actualizados: {updated_count}")
            print(f" Omitidos: {skipped_count}")
            print("="*70 + "\n")
            print(" Sincronización completada exitosamente\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n Error al guardar en BD: {e}\n")
            return False
        
        # Mostrar modelos en BD
        print("\n" + "="*70)
        print("MODELOS REGISTRADOS EN BASE DE DATOS")
        print("="*70 + "\n")
        
        all_models = MLModel.query.all()
        for model in all_models:
            print(f"ID: {model.id}")
            print(f"   Nombre: {model.name}")
            print(f"   Tipo: {model.type}")
            print(f"   Archivo: {model.model_path}")
            print(f"   Última actualización: {model.last_trained or 'N/A'}")
            print(f"   Estado: {model.status}")
            if model.precision:
                print(f"   Precisión: {model.precision:.2f}%")
            if model.rmse:
                print(f"   RMSE: {model.rmse:.2f}")
            print()
        
        return True


if __name__ == '__main__':
    print("\n Iniciando sincronización de modelos ML...\n")
    success = sync_models()
    sys.exit(0 if success else 1)
