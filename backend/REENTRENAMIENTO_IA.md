# Servicio de Reentrenamiento Automático de IA

Este módulo permite programar y ejecutar automáticamente el reentrenamiento de los modelos de Machine Learning.

## Componentes

### 1. Base de Datos
- **Tabla**: `training_schedules`
- **Modelo**: `TrainingSchedule` en `app/models/training_schedule.py`

### 2. API Endpoints
- `GET /api/training-schedules` - Listar todas las programaciones
- `POST /api/training-schedules` - Crear nueva programación
- `GET /api/training-schedules/<id>` - Obtener programación específica
- `PUT /api/training-schedules/<id>` - Actualizar programación
- `DELETE /api/training-schedules/<id>` - Eliminar programación
- `POST /api/training-schedules/<id>/execute` - Ejecutar manualmente
- `GET /api/training-schedules/model-types` - Listar tipos de modelos

### 3. Interfaz Web
- **Ruta**: `#reentrenamiento-ia`
- **Componente**: `RetrainIA.ts`
- Permite crear, editar y visualizar programaciones
- Filtros por modelo y estado
- Ejecución manual de reentrenamientos

### 4. Servicio de Ejecución Automática
- **Script**: `training_scheduler_service.py`
- Verifica y ejecuta programaciones según fecha/hora
- Soporta reentrenamientos recurrentes (diario, semanal, mensual)

## Uso

### Crear Programación (Interfaz)
1. Navegar a "Reentrenamiento IA" en el menú
2. Hacer clic en "Programar Reentrenamiento"
3. Seleccionar modelo, fecha, hora
4. Opcionalmente activar recurrencia
5. Guardar

### Ejecutar Servicio Automático

```bash
# Ejecutar en modo continuo (verifica cada 5 minutos)
python backend/training_scheduler_service.py

# Ejecutar con intervalo personalizado (cada 10 minutos)
python backend/training_scheduler_service.py --interval 10

# Ejecutar una sola vez y salir
python backend/training_scheduler_service.py --once
```

### Ejecutar como Servicio en Windows

Crear archivo `run_training_scheduler.bat`:
```batch
@echo off
cd C:\ruta\a\proyecto\backend
python training_scheduler_service.py --interval 5
pause
```

### Ejecutar como Cron Job en Linux

```bash
# Editar crontab
crontab -e

# Agregar (ejecutar cada 5 minutos)
*/5 * * * * cd /ruta/proyecto/backend && python training_scheduler_service.py --once
```

## Estados de Programación

- **programado**: Esperando fecha/hora de ejecución
- **ejecutando**: En proceso de entrenamiento
- **completado**: Entrenamiento finalizado exitosamente
- **fallido**: Ocurrió un error durante el entrenamiento

## Modelos Soportados

- `attrition`: Modelo de Deserción
- `duration`: Modelo de Duración de Tareas
- `performance`: Modelo de Rendimiento
- `risk`: Modelo de Riesgo de Proyectos

## Parámetros de Entrenamiento

Se pueden especificar parámetros adicionales en formato JSON:

```json
{
  "epochs": 100,
  "batch_size": 32,
  "learning_rate": 0.001
}
```

## Arquitectura

```
┌─────────────────┐
│   Frontend      │
│  RetrainIA.ts   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   API Routes    │
│training_schedule│
│   _routes.py    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  TrainingSchedule│◄────►│    Database      │
│     Model       │      │ training_schedules│
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│   Scheduler     │
│    Service      │
│  (Background)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ML Training    │
│    Functions    │
└─────────────────┘
```

## Próximos Pasos

1. Implementar wrappers para todos los modelos
2. Agregar notificaciones por email al completar
3. Implementar métricas de comparación entre entrenamientos
4. Dashboard con historial de entrenamientos
5. Validación automática de modelos entrenados
