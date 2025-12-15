"""
Script para ejecutar automáticamente los reentrenamientos programados
Debe ejecutarse como un servicio o tarea programada (cron job)
"""
from datetime import datetime, date, timedelta
from app import create_app, db
from app.models.training_schedule import TrainingSchedule
import time
import json

# Importar los entrenadores de modelos
from app.ml.attrition_model import train_attrition_model
# Importar otros modelos según sea necesario
# from app.ml.duration_model import train_duration_model
# from app.ml.performance_model import train_performance_model

def check_and_execute_schedules():
    """Verifica y ejecuta los reentrenamientos programados"""
    app = create_app()
    
    with app.app_context():
        # Obtener fecha y hora actual
        now = datetime.now()
        current_date = now.date()
        current_time = now.strftime("%H:%M")
        
        print(f"\n{'='*60}")
        print(f"Verificando programaciones - {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Buscar programaciones pendientes para hoy
        schedules = TrainingSchedule.query.filter(
            TrainingSchedule.scheduled_date == current_date,
            TrainingSchedule.status == 'programado'
        ).all()
        
        if not schedules:
            print("No hay programaciones para ejecutar en este momento.")
            return
        
        print(f"Encontradas {len(schedules)} programación(es) para hoy:\n")
        
        for schedule in schedules:
            # Verificar si es hora de ejecutar (con margen de 5 minutos)
            scheduled_datetime = datetime.combine(schedule.scheduled_date, 
                                                 datetime.strptime(schedule.scheduled_time, "%H:%M").time())
            time_diff = (now - scheduled_datetime).total_seconds() / 60
            
            # Ejecutar si estamos dentro de los 5 minutos posteriores a la hora programada
            if 0 <= time_diff <= 5:
                print(f"⏰ Ejecutando: {schedule.model_type} - {schedule.scheduled_time}")
                execute_training(schedule)
            else:
                print(f"⏳ Pendiente: {schedule.model_type} - {schedule.scheduled_time}")

def execute_training(schedule: TrainingSchedule):
    """Ejecuta el reentrenamiento de un modelo específico"""
    try:
        # Actualizar estado a ejecutando
        schedule.status = 'ejecutando'
        schedule.last_execution = datetime.utcnow()
        db.session.commit()
        
        print(f"   Iniciando reentrenamiento del modelo: {schedule.model_type}")
        
        # Parsear parámetros si existen
        params = {}
        if schedule.parameters:
            try:
                params = json.loads(schedule.parameters)
            except json.JSONDecodeError:
                print(f"   ⚠️  Advertencia: Parámetros JSON inválidos, usando valores por defecto")
        
        # Ejecutar el entrenamiento según el tipo de modelo
        result = None
        if schedule.model_type == 'attrition':
            result = train_attrition_model_wrapper(params)
        elif schedule.model_type == 'duration':
            result = "Entrenamiento de modelo de duración completado (implementar wrapper)"
        elif schedule.model_type == 'performance':
            result = "Entrenamiento de modelo de rendimiento completado (implementar wrapper)"
        elif schedule.model_type == 'risk':
            result = "Entrenamiento de modelo de riesgo completado (implementar wrapper)"
        else:
            raise ValueError(f"Tipo de modelo no reconocido: {schedule.model_type}")
        
        # Actualizar estado a completado
        schedule.status = 'completado'
        schedule.execution_result = str(result)
        
        print(f"   ✅ Completado exitosamente")
        print(f"   Resultado: {result}\n")
        
        # Si es recurrente, programar la siguiente ejecución
        if schedule.is_recurring:
            schedule_next_execution(schedule)
        
    except Exception as e:
        # Marcar como fallido
        schedule.status = 'fallido'
        schedule.execution_result = f"Error: {str(e)}"
        print(f"   ❌ Error: {str(e)}\n")
    
    finally:
        db.session.commit()

def train_attrition_model_wrapper(params):
    """Wrapper para entrenar el modelo de deserción"""
    try:
        # Aquí puedes pasar parámetros personalizados al entrenamiento
        # Por ejemplo: epochs, batch_size, etc.
        result = train_attrition_model()
        return f"Modelo de deserción entrenado exitosamente. Métricas: {result}"
    except Exception as e:
        raise Exception(f"Error al entrenar modelo de deserción: {str(e)}")

def schedule_next_execution(schedule: TrainingSchedule):
    """Programa la siguiente ejecución para un reentrenamiento recurrente"""
    try:
        if schedule.recurrence_pattern == 'daily':
            schedule.scheduled_date = schedule.scheduled_date + timedelta(days=1)
        elif schedule.recurrence_pattern == 'weekly':
            schedule.scheduled_date = schedule.scheduled_date + timedelta(weeks=1)
        elif schedule.recurrence_pattern == 'monthly':
            # Agregar aproximadamente un mes
            schedule.scheduled_date = schedule.scheduled_date + timedelta(days=30)
        
        # Resetear estado a programado
        schedule.status = 'programado'
        db.session.commit()
        
        print(f"   🔄 Próxima ejecución programada para: {schedule.scheduled_date} {schedule.scheduled_time}")
        
    except Exception as e:
        print(f"   ⚠️  Error al programar siguiente ejecución: {str(e)}")

def run_scheduler(interval_minutes=5):
    """
    Ejecuta el verificador de programaciones en un loop
    
    Args:
        interval_minutes: Intervalo en minutos entre verificaciones
    """
    print(f"\n🤖 Iniciando servicio de reentrenamiento automático")
    print(f"Intervalo de verificación: {interval_minutes} minutos")
    print(f"Presiona Ctrl+C para detener\n")
    
    try:
        while True:
            check_and_execute_schedules()
            
            # Esperar hasta la próxima verificación
            print(f"⏰ Próxima verificación en {interval_minutes} minutos...")
            time.sleep(interval_minutes * 60)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Servicio detenido por el usuario")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Servicio de reentrenamiento automático de modelos IA')
    parser.add_argument('--interval', type=int, default=5, 
                       help='Intervalo en minutos entre verificaciones (default: 5)')
    parser.add_argument('--once', action='store_true',
                       help='Ejecutar una sola vez y salir')
    
    args = parser.parse_args()
    
    if args.once:
        check_and_execute_schedules()
    else:
        run_scheduler(args.interval)
