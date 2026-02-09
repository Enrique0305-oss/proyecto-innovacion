"""
APScheduler para entrenamientos automáticos programados
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.extensions import db
from app.models.training_schedule import TrainingSchedule
from app.models.ml_models import MLModel
import requests
import subprocess
import logging
import os

logger = logging.getLogger(__name__)

# Mapeo de tipos de modelo a scripts de entrenamiento
TRAINING_SCRIPTS = {
    'risk': 'ml/models/training/train_binary_task_risk.py',
    'duration': 'ml/models/training/train_catboost_regressor_numeric_only.py',
    'recommendation': 'ml/models/training/train_catboost_recommender.py',
    'performance': 'ml/models/training/train_performance_predictor_fixed.py',
    'simulation': 'ml/models/training/train_bottleneck_predictor_FIXED.py'
}


class TrainingScheduler:
    """Gestiona programaciones de entrenamiento automático"""
    
    def __init__(self, app=None):
        self.scheduler = BackgroundScheduler()
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa el scheduler con la app Flask"""
        self.app = app
        
        # Configuración del scheduler
        self.scheduler.start()
        
        # Cargar schedules existentes
        with app.app_context():
            self.load_schedules()
        
        print("✅ Training Scheduler iniciado")
    
    
    def load_schedules(self):
        """Carga todas las programaciones activas desde BD"""
        try:
            schedules = TrainingSchedule.query.filter_by(
                status='programado',
                is_recurring=True
            ).all()
            
            for schedule in schedules:
                self.add_schedule(schedule)
            
            print(f"📅 {len(schedules)} programaciones cargadas")
            
        except Exception as e:
            print(f"❌ Error cargando schedules: {e}")
    
    
    def add_schedule(self, schedule):
        """Agrega una programación al scheduler"""
        try:
            # Convertir patrón a cron trigger
            trigger = self._parse_recurrence_pattern(schedule.recurrence_pattern, schedule.scheduled_time)
            
            if not trigger:
                print(f"⚠️ Patrón no válido: {schedule.recurrence_pattern}")
                return
            
            # Agregar job
            job_id = f"training_schedule_{schedule.id}"
            
            self.scheduler.add_job(
                func=self._execute_scheduled_training,
                trigger=trigger,
                args=[schedule.id],
                id=job_id,
                replace_existing=True,
                misfire_grace_time=3600  # 1 hora de gracia
            )
            
            print(f"✅ Schedule #{schedule.id} agregado: {schedule.model_type} {schedule.recurrence_pattern}")
            
        except Exception as e:
            print(f"❌ Error agregando schedule #{schedule.id}: {e}")
    
    
    def remove_schedule(self, schedule_id):
        """Elimina una programación del scheduler"""
        try:
            job_id = f"training_schedule_{schedule_id}"
            self.scheduler.remove_job(job_id)
            print(f"🗑️ Schedule #{schedule_id} eliminado")
        except Exception as e:
            print(f"⚠️ Error eliminando schedule: {e}")
    
    
    def _parse_recurrence_pattern(self, pattern, time_str):
        """
        Convierte patrón de recurrencia a CronTrigger
        
        Patrones soportados:
        - daily: Todos los días
        - weekly: Cada semana (domingos)
        - monthly: Cada mes (día 1)
        """
        hour, minute = 0, 0
        
        if time_str:
            try:
                parts = time_str.split(':')
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
            except:
                pass
        
        if pattern == 'daily':
            return CronTrigger(hour=hour, minute=minute)
        
        elif pattern == 'weekly':
            # Domingos
            return CronTrigger(day_of_week=6, hour=hour, minute=minute)
        
        elif pattern == 'monthly':
            # Día 1 de cada mes
            return CronTrigger(day=1, hour=hour, minute=minute)
        
        return None
    
    
    def _execute_scheduled_training(self, schedule_id):
        """Ejecuta un entrenamiento programado"""
        from app import create_app
        app = create_app()
        
        with app.app_context():
            try:
                print(f"\n⏰ Ejecutando schedule #{schedule_id}...")
                
                schedule = TrainingSchedule.query.get(schedule_id)
                if not schedule:
                    print(f"❌ Schedule #{schedule_id} no encontrado")
                    return
                
                # Buscar modelo por tipo
                models = MLModel.query.filter_by(type=schedule.model_type).all()
                
                if not models:
                    print(f"❌ No se encontró modelo tipo '{schedule.model_type}'")
                    schedule.execution_result = "Error: Modelo no encontrado"
                    db.session.commit()
                    return
                
                model = models[0]  # Tomar el primero
                
                # Verificar condiciones (si las hay)
                import json
                params = {}
                if schedule.parameters:
                    try:
                        params = json.loads(schedule.parameters)
                    except:
                        pass
                
                min_records = params.get('min_records', 0)
                
                if min_records > 0:
                    # Verificar datos disponibles
                    from app.ml.training_manager import training_manager
                    stats = training_manager.get_available_data_stats()
                    available = stats['tasks']['with_actual_hours']
                    
                    if available < min_records:
                        msg = f"Condición no cumplida: {available} registros (mínimo {min_records})"
                        print(f"⏭️ {msg}")
                        schedule.execution_result = msg
                        schedule.last_execution = datetime.now()
                        db.session.commit()
                        return
                
                # Crear training job vía API
                # En producción, hacer request HTTP al endpoint
                # Por simplicidad, crear directamente
                from app.models.ml_models import MLTrainingJob
                
                job = MLTrainingJob(
                    model_id=model.id,
                    job_name=f"Auto-entrenamiento {model.name}",
                    status='pending',
                    config={'scheduled': True, 'schedule_id': schedule_id},
                    created_by=None
                )
                
                db.session.add(job)
                db.session.commit()
                
                # Lanzar entrenamiento
                from app.routes.training_routes import _run_training_job
                import threading
                
                thread = threading.Thread(target=_run_training_job, args=(job.id,))
                thread.daemon = True
                thread.start()
                
                # Actualizar schedule
                schedule.last_execution = datetime.now()
                schedule.execution_result = f"Job #{job.id} creado exitosamente"
                db.session.commit()
                
                print(f"✅ Training job #{job.id} iniciado para {model.name}")
                
            except Exception as e:
                print(f"❌ Error ejecutando schedule #{schedule_id}: {e}")
                schedule.execution_result = f"Error: {str(e)}"
                schedule.last_execution = datetime.now()
                db.session.commit()
    
    
    def shutdown(self):
        """Detiene el scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("🛑 Training Scheduler detenido")
    
    
    def execute_training_script(self, model_type: str) -> bool:
        """
        Ejecuta directamente el script de entrenamiento (sin usar BD ni jobs).
        
        Args:
            model_type: Tipo de modelo ('risk', 'duration', 'recommendation', 'performance', 'simulation')
        
        Returns:
            True si el entrenamiento fue exitoso, False en caso contrario
        """
        script_path = TRAINING_SCRIPTS.get(model_type)
        
        if not script_path:
            logger.error(f"❌ Modelo '{model_type}' no encontrado")
            return False
        
        logger.info(f"▶️ Ejecutando script: {script_path}")
        
        # Obtener directorio backend (un nivel arriba de app/)
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_script_path = os.path.join(backend_dir, script_path)
        
        if not os.path.exists(full_script_path):
            logger.error(f"❌ Script no encontrado: {full_script_path}")
            return False
        
        logger.info(f"📂 Ruta completa: {full_script_path}")
        logger.info(f"📂 Directorio de trabajo: {backend_dir}")
        
        # Configurar variables de entorno para el script
        env = os.environ.copy()
        if self.app:
            from config import Config
            env['MYSQL_HOST'] = Config.DB_HOST
            env['MYSQL_DB'] = Config.DB_NAME
            env['MYSQL_USER'] = Config.DB_USER
            env['MYSQL_PASS'] = Config.DB_PASSWORD
            env['MYSQL_PORT'] = str(Config.DB_PORT)
            logger.info(f"🔧 Variables configuradas: host={Config.DB_HOST}, db={Config.DB_NAME}, user={Config.DB_USER}")
        
        try:
            result = subprocess.run(
                ['python', full_script_path],
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hora máximo
                cwd=backend_dir,  # Ejecutar desde backend/
                env=env  # Pasar variables de entorno
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Entrenamiento de '{model_type}' completado")
                logger.info(f"📄 Output: {result.stdout[:500]}")  # Primeros 500 caracteres
                return True
            else:
                logger.error(f"❌ Error en '{model_type}' (código {result.returncode})")
                logger.error(f"📄 STDOUT: {result.stdout}")
                logger.error(f"📄 STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏱️ Timeout: '{model_type}' excedió 1 hora")
            return False
        except Exception as e:
            logger.error(f"❌ Excepción en '{model_type}': {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"📄 Traceback: {traceback.format_exc()}")
            return False
    
    
    def schedule_training_simple(self, model_type: str, training_date: str, frequency: str) -> str:
        """
        Programa entrenamiento recurrente usando scripts directos.
        
        Args:
            model_type: Tipo de modelo
            training_date: Fecha ISO (YYYY-MM-DD)
            frequency: 'quarterly' | 'biannual' | 'annual'
        
        Returns:
            ID del job programado
        """
        try:
            date_obj = datetime.strptime(training_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {training_date}")
        
        day = date_obj.day
        month = date_obj.month
        
        # Configurar trigger
        if frequency == 'quarterly':
            trigger = CronTrigger(day=day, month='*/3', hour=2, minute=0)
        elif frequency == 'biannual':
            trigger = CronTrigger(day=day, month='*/6', hour=2, minute=0)
        elif frequency == 'annual':
            trigger = CronTrigger(day=day, month=month, hour=2, minute=0)
        else:
            raise ValueError(f"Frecuencia inválida: {frequency}")
        
        job_id = f'retrain_{model_type}_scheduled'
        
        self.scheduler.add_job(
            func=self.execute_training_script,
            trigger=trigger,
            args=[model_type],
            id=job_id,
            replace_existing=True,
            name=f'Reentrenamiento: {model_type}'
        )
        
        logger.info(f"📅 Programado: {model_type} - Día {day} - {frequency}")
        return job_id
    
    
    def get_all_jobs(self):
        """Obtiene todos los jobs programados"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        return jobs
    
    
    def remove_job(self, job_id: str) -> bool:
        """Elimina un job programado"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"🗑️ Job eliminado: {job_id}")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Error eliminando job: {e}")
            return False


# Instancia global
training_scheduler = TrainingScheduler()
