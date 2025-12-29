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


# Instancia global
training_scheduler = TrainingScheduler()
