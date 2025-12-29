"""
Training Routes - API para gestión de reentrenamiento de modelos
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app.extensions import db
from app.models.ml_models import MLModel, MLDataset, MLTrainingJob
from app.models.training_schedule import TrainingSchedule
from app.ml.training_manager import training_manager
import threading

bp = Blueprint('training', __name__, url_prefix='/api/ml/training')


@bp.route('/models', methods=['GET'])
def get_models():
    """Listar todos los modelos ML"""
    try:
        models = MLModel.query.all()
        
        # Agregar estadísticas adicionales
        result = []
        for model in models:
            model_dict = model.to_dict()
            
            # Días desde último entrenamiento
            if model.last_trained:
                days_since = (datetime.now() - model.last_trained).days
                model_dict['days_since_training'] = days_since
                model_dict['needs_retraining'] = days_since > 30
            else:
                model_dict['days_since_training'] = None
                model_dict['needs_retraining'] = True
            
            # Jobs recientes
            recent_jobs = MLTrainingJob.query.filter_by(
                model_id=model.id
            ).order_by(MLTrainingJob.created_at.desc()).limit(3).all()
            
            model_dict['recent_jobs'] = [job.to_dict() for job in recent_jobs]
            
            result.append(model_dict)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/models/<int:model_id>', methods=['GET'])
def get_model_detail(model_id):
    """Detalle de un modelo específico"""
    try:
        model = MLModel.query.get_or_404(model_id)
        model_dict = model.to_dict()
        
        # Historial de entrenamientos
        jobs = MLTrainingJob.query.filter_by(
            model_id=model_id
        ).order_by(MLTrainingJob.created_at.desc()).limit(10).all()
        
        model_dict['training_history'] = [job.to_dict() for job in jobs]
        
        # Predicciones recientes
        predictions_count = model.predictions.count()
        model_dict['total_predictions'] = predictions_count
        
        return jsonify(model_dict), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/data-stats', methods=['GET'])
def get_data_stats():
    """Estadísticas de datos disponibles para reentrenamiento"""
    try:
        stats = training_manager.get_available_data_stats()
        
        # Agregar recomendaciones
        recommendations = []
        
        if stats['tasks']['with_actual_hours'] < 500:
            recommendations.append({
                'type': 'warning',
                'message': f"Solo {stats['tasks']['with_actual_hours']} tareas con horas reales. Se recomiendan al menos 500 para reentrenamiento óptimo."
            })
        else:
            recommendations.append({
                'type': 'success',
                'message': f"{stats['tasks']['with_actual_hours']} tareas disponibles. Suficientes datos para reentrenar modelos."
            })
        
        stats['recommendations'] = recommendations
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/datasets/generate', methods=['POST'])
def generate_dataset():
    """Generar dataset para un modelo"""
    try:
        data = request.get_json()
        model_type = data.get('model_type')
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        if not model_type:
            return jsonify({'error': 'model_type requerido'}), 400
        
        # Extraer datos
        df = training_manager.extract_dataset_for_model(model_type, date_from, date_to)
        
        if len(df) == 0:
            return jsonify({'error': 'No hay datos disponibles para el rango seleccionado'}), 400
        
        # Guardar dataset
        dataset = training_manager.save_dataset(df, model_type, uploaded_by=1)
        
        return jsonify({
            'message': 'Dataset generado exitosamente',
            'dataset': dataset.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/datasets', methods=['GET'])
def get_datasets():
    """Listar datasets disponibles"""
    try:
        datasets = MLDataset.query.order_by(MLDataset.uploaded_at.desc()).limit(20).all()
        return jsonify([d.to_dict() for d in datasets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/jobs', methods=['POST'])
def create_training_job():
    """Crear un nuevo job de entrenamiento"""
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        dataset_id = data.get('dataset_id')
        config = data.get('config', {})
        
        if not model_id:
            return jsonify({'error': 'model_id requerido'}), 400
        
        # Verificar modelo existe
        model = MLModel.query.get(model_id)
        if not model:
            return jsonify({'error': 'Modelo no encontrado'}), 404
        
        # Crear job
        job = MLTrainingJob(
            model_id=model_id,
            dataset_id=dataset_id,
            job_name=f"Reentrenamiento {model.name}",
            status='pending',
            config=config,
            created_by=1
        )
        
        db.session.add(job)
        db.session.commit()
        
        # Lanzar entrenamiento en background
        thread = threading.Thread(
            target=_run_training_job,
            args=(job.id,)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'message': 'Job de entrenamiento creado',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job_status(job_id):
    """Obtener estado de un job"""
    try:
        job = MLTrainingJob.query.get_or_404(job_id)
        return jsonify(job.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Listar todos los jobs"""
    try:
        status_filter = request.args.get('status')
        limit = int(request.args.get('limit', 20))
        
        query = MLTrainingJob.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        jobs = query.order_by(MLTrainingJob.created_at.desc()).limit(limit).all()
        
        return jsonify([job.to_dict() for job in jobs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/jobs/<int:job_id>/activate', methods=['POST'])
def activate_trained_model(job_id):
    """Activar modelo entrenado manualmente"""
    try:
        model = training_manager.activate_model(job_id, replace_current=True)
        
        return jsonify({
            'message': 'Modelo activado exitosamente',
            'model': model.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/schedules', methods=['POST'])
def create_schedule():
    """Crear programación de entrenamiento automático"""
    try:
        data = request.get_json()
        
        schedule = TrainingSchedule(
            model_type=data.get('model_type'),
            scheduled_date=datetime.fromisoformat(data.get('scheduled_date')),
            scheduled_time=data.get('scheduled_time'),
            parameters=data.get('parameters'),
            is_recurring=data.get('is_recurring', False),
            recurrence_pattern=data.get('recurrence_pattern'),
            created_by=1
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        return jsonify({
            'message': 'Programación creada exitosamente',
            'schedule': schedule.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/schedules', methods=['GET'])
def get_schedules():
    """Listar programaciones"""
    try:
        schedules = TrainingSchedule.query.order_by(
            TrainingSchedule.created_at.desc()
        ).all()
        
        return jsonify([s.to_dict() for s in schedules]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """Eliminar programación"""
    try:
        schedule = TrainingSchedule.query.get_or_404(schedule_id)
        db.session.delete(schedule)
        db.session.commit()
        
        return jsonify({'message': 'Programación eliminada'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def _run_training_job(job_id):
    """
    Ejecuta un job de entrenamiento en background
    
    NOTA: Esta es una implementación simplificada.
    En producción, usar Celery o RQ para jobs asíncronos.
    """
    from app import create_app
    app = create_app()
    
    with app.app_context():
        try:
            job = MLTrainingJob.query.get(job_id)
            if not job:
                return
            
            # Actualizar a running
            job.status = 'running'
            job.started_at = datetime.now()
            job.progress = 10
            job.current_step = 'Inicializando'
            db.session.commit()
            
            print(f"🚀 Job #{job_id} iniciado")
            
            # Obtener modelo
            model = MLModel.query.get(job.model_id)
            
            # Paso 1: Extraer datos (si no hay dataset)
            if not job.dataset_id:
                job.current_step = 'Extrayendo datos'
                job.progress = 20
                db.session.commit()
                
                df = training_manager.extract_dataset_for_model(model.type)
                dataset = training_manager.save_dataset(df, model.type, uploaded_by=job.created_by)
                job.dataset_id = dataset.id
                db.session.commit()
            
            # Paso 2: Simular entrenamiento (placeholder)
            job.current_step = 'Entrenando modelo'
            job.progress = 50
            db.session.commit()
            
            import time
            time.sleep(5)  # Simular entrenamiento
            
            # Paso 3: Generar métricas de ejemplo
            job.current_step = 'Validando modelo'
            job.progress = 80
            db.session.commit()
            
            # Métricas simuladas (en producción, usar modelo real)
            import random
            current_precision = float(model.precision) if model.precision else 90.0
            new_precision = current_precision + random.uniform(-1, 3)
            
            metrics = {
                'accuracy': new_precision,
                'precision': new_precision,
                'recall': new_precision - 1,
                'f1_score': new_precision - 0.5,
                'samples_used': 450,
                'training_time_seconds': 5
            }
            
            # Paso 4: Comparar con modelo anterior
            job.current_step = 'Comparando con modelo anterior'
            job.progress = 90
            db.session.commit()
            
            old_metrics = {
                'accuracy': current_precision,
                'precision': current_precision
            }
            
            comparison = training_manager.compare_models(old_metrics, metrics)
            
            # Paso 5: Guardar modelo (simulado)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"ml/models/{model.type}_model_{timestamp}.pkl"
            
            job.output_model_path = output_path
            job.metrics = metrics
            job.metrics['comparison'] = comparison
            
            # Completar
            job.status = 'completed'
            job.progress = 100
            job.current_step = 'Completado'
            job.completed_at = datetime.now()
            job.duration_seconds = int((job.completed_at - job.started_at).total_seconds())
            
            # Auto-activar si mejora significativamente
            if comparison['should_replace']:
                print(f"✅ Modelo mejoró: {comparison['reason']}")
                training_manager.activate_model(job_id, replace_current=True)
            else:
                print(f"⚠️ Modelo no reemplazado: {comparison['reason']}")
            
            db.session.commit()
            print(f"✅ Job #{job_id} completado")
            
        except Exception as e:
            print(f"❌ Error en job #{job_id}: {str(e)}")
            job.status = 'failed'
            job.error_message = str(e)
            job.completed_at = datetime.now()
            if job.started_at:
                job.duration_seconds = int((job.completed_at - job.started_at).total_seconds())
            db.session.commit()
