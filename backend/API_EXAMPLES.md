# Ejemplos de Uso de la API

Colección de ejemplos para probar todos los endpoints de la API.

## 🔐 Autenticación

### 1. Registrar Usuario

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario1",
    "email": "usuario1@example.com",
    "password": "password123",
    "role": "user"
  }'
```

**Respuesta:**
```json
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "username": "usuario1",
    "email": "usuario1@example.com",
    "role": "user"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLC..."
}
```

### 2. Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario1",
    "password": "password123"
  }'
```

**Respuesta:**
```json
{
  "message": "Login exitoso",
  "access_token": "eyJ0eXAiOiJKV1QiLC...",
  "user": {
    "id": 1,
    "username": "usuario1",
    "email": "usuario1@example.com",
    "role": "user"
  }
}
```

### 3. Obtener Usuario Actual

```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLC..."
```

### 4. Cambiar Contraseña

```bash
curl -X PUT http://localhost:5000/api/auth/change-password \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLC..." \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "password123",
    "new_password": "nueva_password456"
  }'
```

---

## 📋 Tareas

### 1. Listar Tareas (con paginación y filtros)

```bash
# Listar todas
curl -X GET http://localhost:5000/api/tasks/ \
  -H "Authorization: Bearer TOKEN"

# Con filtros
curl -X GET "http://localhost:5000/api/tasks/?page=1&per_page=10&status=Pending&area=IT" \
  -H "Authorization: Bearer TOKEN"

# Búsqueda
curl -X GET "http://localhost:5000/api/tasks/?search=desarrollo" \
  -H "Authorization: Bearer TOKEN"
```

**Respuesta:**
```json
{
  "tasks": [
    {
      "task_id": "TASK001",
      "task_name": "Desarrollar módulo de autenticación",
      "status": "In - Progress",
      "area": "IT",
      "priority": "High",
      "assignees": [
        {
          "person_id": "P001",
          "name": "Juan Pérez"
        }
      ]
    }
  ],
  "total": 45,
  "pages": 5,
  "current_page": 1,
  "per_page": 10
}
```

### 2. Obtener Tarea Específica

```bash
curl -X GET http://localhost:5000/api/tasks/TASK001 \
  -H "Authorization: Bearer TOKEN"
```

### 3. Crear Nueva Tarea

```bash
curl -X POST http://localhost:5000/api/tasks/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK999",
    "task_name": "Nueva tarea de prueba",
    "project_id": "PROJ001",
    "area": "IT",
    "task_type": "Development",
    "start_date_est": "2024-01-15",
    "end_date_est": "2024-01-30",
    "status": "Pending",
    "priority": "Medium",
    "complexity_level": "Medium",
    "assignees": ["P001", "P002"]
  }'
```

### 4. Actualizar Tarea

```bash
curl -X PUT http://localhost:5000/api/tasks/TASK999 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In - Progress",
    "completion": "50",
    "start_date_real": "2024-01-16"
  }'
```

### 5. Eliminar Tarea

```bash
curl -X DELETE http://localhost:5000/api/tasks/TASK999 \
  -H "Authorization: Bearer TOKEN"
```

### 6. Asignar Persona a Tarea

```bash
curl -X POST http://localhost:5000/api/tasks/TASK001/assignees \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": "P003"
  }'
```

### 7. Remover Asignación

```bash
curl -X DELETE http://localhost:5000/api/tasks/TASK001/assignees/P003 \
  -H "Authorization: Bearer TOKEN"
```

### 8. Estadísticas de Tareas

```bash
curl -X GET http://localhost:5000/api/tasks/stats \
  -H "Authorization: Bearer TOKEN"
```

**Respuesta:**
```json
{
  "total_tasks": 100,
  "completed": 45,
  "in_progress": 30,
  "pending": 25,
  "completion_rate": 45.0,
  "tasks_by_area": [
    {"area": "IT", "count": 40},
    {"area": "Marketing", "count": 30},
    {"area": "Sales", "count": 30}
  ]
}
```

---

## 🤖 Machine Learning

### 1. Predicción de Riesgo

```bash
curl -X POST http://localhost:5000/api/ml/prediccion-riesgo \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK001",
    "complexity_level": "High",
    "priority": "Critical",
    "area": "IT",
    "task_type": "Development",
    "duration_est": 30,
    "assignees_count": 2,
    "dependencies": 5
  }'
```

**Respuesta:**
```json
{
  "task_id": "TASK001",
  "risk_level": "alto",
  "risk_probability": 0.85,
  "risk_factors": [
    "Alta complejidad técnica",
    "Prioridad crítica",
    "Múltiples dependencias (5)",
    "Duración prolongada"
  ],
  "recommendations": [
    "Realizar seguimiento diario del progreso",
    "Asignar recursos adicionales si es posible",
    "Establecer puntos de control frecuentes",
    "Validar que las dependencias estén en progreso"
  ]
}
```

### 2. Predicción de Duración Real

```bash
curl -X POST http://localhost:5000/api/ml/tiempo-real \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK002",
    "complexity_level": "Medium",
    "task_type": "Development",
    "area": "IT",
    "assignees_count": 3,
    "tools_used": "Python,Docker,PostgreSQL",
    "dependencies": 2
  }'
```

**Respuesta:**
```json
{
  "task_id": "TASK002",
  "predicted_duration_days": 12.5,
  "confidence_interval": {
    "min": 10.0,
    "max": 15.0,
    "mean": 12.5
  },
  "factors": [
    "Complejidad media: x2 tiempo",
    "Desarrollo: +50% tiempo",
    "Equipo de 3: reducción parcial"
  ]
}
```

### 3. Recomendación de Persona para Tarea

```bash
curl -X POST http://localhost:5000/api/ml/recomendar-persona \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK003",
    "area": "IT",
    "task_type": "Development",
    "complexity_level": "High",
    "skills_required": ["Python", "Machine Learning", "SQL"],
    "exclude_person_ids": ["P001"],
    "top_n": 5
  }'
```

**Respuesta:**
```json
{
  "task_id": "TASK003",
  "recommendations": [
    {
      "person_id": "P042",
      "name": "María García",
      "score": 92.5,
      "area": "IT",
      "role": "Senior Developer",
      "experience_years": 8,
      "performance_index": 95,
      "satisfaction_score": 88,
      "current_workload": 2,
      "reasons": [
        "Experiencia en IT",
        "Alto rendimiento (95%)",
        "8 años de experiencia",
        "Baja carga de trabajo actual"
      ]
    },
    {
      "person_id": "P028",
      "name": "Carlos Rodríguez",
      "score": 87.3,
      "area": "IT",
      "role": "Developer",
      "experience_years": 5,
      "performance_index": 85,
      "reasons": [
        "Experiencia en IT",
        "5 años de experiencia",
        "Baja carga de trabajo actual"
      ]
    }
  ],
  "total_candidates": 15,
  "criteria_used": ["area_match", "performance", "experience", "workload", "satisfaction"]
}
```

### 4. Predicción de Desempeño

```bash
curl -X POST http://localhost:5000/api/ml/desempeno \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "person_id": "P042",
    "task_id": "TASK003",
    "task_type": "Development",
    "complexity_level": "High",
    "area": "IT"
  }'
```

**Respuesta:**
```json
{
  "person_id": "P042",
  "task_id": "TASK003",
  "performance_score": 88.5,
  "performance_level": "alto",
  "strengths": [
    "Historial de alto rendimiento (95%)",
    "Amplia experiencia (8 años)",
    "Especialista en IT",
    "Alta motivación y satisfacción laboral"
  ],
  "weaknesses": [],
  "confidence": 0.89
}
```

### 5. Minería de Procesos

```bash
# Análisis general
curl -X POST http://localhost:5000/api/ml/proceso \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "area": "IT",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "analysis_type": "bottleneck"
  }'
```

**Respuesta:**
```json
{
  "analysis_type": "bottleneck",
  "process_flow": [
    {
      "status": "Completed",
      "count": 45,
      "avg_duration_days": 12.3,
      "percentage": 45.0
    },
    {
      "status": "In - Progress",
      "count": 30,
      "avg_duration_days": 8.5,
      "percentage": 30.0
    },
    {
      "status": "Pending",
      "count": 25,
      "avg_duration_days": 0,
      "percentage": 25.0
    }
  ],
  "bottlenecks": [
    {
      "type": "delays",
      "severity": "high",
      "count": 8,
      "description": "8 tareas con retrasos significativos",
      "examples": [
        {
          "task_id": "TASK045",
          "task_name": "Migración de base de datos",
          "delay_percentage": 120.5,
          "estimated_days": 10,
          "actual_days": 22
        }
      ]
    },
    {
      "type": "area_overload",
      "severity": "medium",
      "count": 15,
      "area": "IT",
      "description": "Área IT con 15 tareas pendientes/en progreso"
    }
  ],
  "avg_duration": {
    "mean": 12.3,
    "min": 2,
    "max": 45,
    "tasks_with_duration": 45
  },
  "task_sequences": [
    {
      "sequence": "Planning -> Development -> Testing -> Deployment",
      "frequency": 12
    },
    {
      "sequence": "Research -> Development -> Review",
      "frequency": 8
    }
  ],
  "insights": [
    "Se analizaron 100 tareas en total",
    "El 45.0% de las tareas están en estado \"Completed\"",
    "Duración promedio de tareas: 12.3 días (rango: 2-45 días)",
    "⚠️ Se detectaron 2 cuellos de botella de alta severidad",
    "Tasa de completitud: 45.0%"
  ],
  "total_tasks_analyzed": 100
}
```

### 6. Estado de Modelos ML

```bash
curl -X GET http://localhost:5000/api/ml/health
```

**Respuesta:**
```json
{
  "status": "partial",
  "models": {
    "risk_model": false,
    "duration_model": false,
    "recommender_model": false,
    "performance_model": false,
    "process_mining": false
  },
  "message": "Algunos modelos no están disponibles (usando lógica heurística)"
}
```

---

## 📊 Health Check

```bash
# Endpoint raíz
curl http://localhost:5000/

# Health check
curl http://localhost:5000/health
```

---

## 🧪 Testing con PowerShell

### Variables de entorno

```powershell
# Guardar token en variable
$TOKEN = "eyJ0eXAiOiJKV1QiLC..."

# O hacer login y guardar automáticamente
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"admin123"}'

$TOKEN = $response.access_token
```

### Ejemplos con PowerShell

```powershell
# Login
Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username":"usuario1","password":"password123"}'

# Listar tareas
Invoke-RestMethod -Uri "http://localhost:5000/api/tasks/" `
  -Headers @{ Authorization = "Bearer $TOKEN" }

# Crear tarea
$body = @{
  task_id = "TASK_TEST_001"
  task_name = "Tarea de prueba desde PowerShell"
  area = "IT"
  status = "Pending"
  priority = "Medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/tasks/" `
  -Method POST `
  -Headers @{ Authorization = "Bearer $TOKEN" } `
  -ContentType "application/json" `
  -Body $body

# Predicción de riesgo
$riskBody = @{
  complexity_level = "High"
  priority = "High"
  area = "IT"
  task_type = "Development"
  duration_est = 25
  assignees_count = 2
  dependencies = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/ml/prediccion-riesgo" `
  -Method POST `
  -Headers @{ Authorization = "Bearer $TOKEN" } `
  -ContentType "application/json" `
  -Body $riskBody
```

---

## 🔍 Códigos de Respuesta HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o expirado |
| 403 | Forbidden - No tiene permisos |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Recurso ya existe |
| 500 | Internal Server Error - Error del servidor |
| 503 | Service Unavailable - Servicio no disponible |

---

## 📝 Notas Importantes

1. **Autenticación**: Todos los endpoints (excepto login/register y health) requieren JWT token
2. **Formato de fechas**: Usar formato ISO `YYYY-MM-DD` (ej: `2024-01-15`)
3. **Paginación**: Por defecto 20 items por página, máximo configurable
4. **Modelos ML**: Si no hay archivos .pkl, se usa lógica heurística automáticamente
5. **CORS**: Configurar dominios permitidos en `.env` para producción

---

**Última actualización:** Enero 2024
