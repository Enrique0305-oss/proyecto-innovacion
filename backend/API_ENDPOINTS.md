# API Backend - Sistema de Productividad

## Resumen de Endpoints Implementados

### 🔐 Autenticación (`/api/auth`)
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual
- `PUT /api/auth/change-password` - Cambiar contraseña
- `GET /api/auth/users` - Listar todos los usuarios

### 📋 Tareas (`/api/tasks`)
- `GET /api/tasks` - Obtener lista de tareas (con filtros)
- `GET /api/tasks/<id>` - Obtener tarea por ID
- `POST /api/tasks` - Crear nueva tarea
- `PUT /api/tasks/<id>` - Actualizar tarea
- `DELETE /api/tasks/<id>` - Eliminar tarea
- `GET /api/tasks/stats` - Estadísticas de tareas

### 🏢 Áreas (`/api/areas`)
- `GET /api/areas` - Obtener lista de áreas
- `GET /api/areas/<id>` - Obtener área por ID
- `POST /api/areas` - Crear nueva área
- `PUT /api/areas/<id>` - Actualizar área
- `DELETE /api/areas/<id>` - Eliminar área

### 👥 Usuarios Web (`/api/users`)
- `GET /api/users` - Obtener lista de usuarios
- `GET /api/users/<id>` - Obtener usuario por ID
- `PUT /api/users/<id>` - Actualizar usuario
- `DELETE /api/users/<id>` - Desactivar usuario
- `GET /api/users/roles` - Obtener roles disponibles

### 👤 Personas (`/api/persons`)
- `GET /api/persons` - Obtener lista de personas
- `GET /api/persons/<person_id>` - Obtener persona por ID
- `POST /api/persons` - Crear nueva persona
- `PUT /api/persons/<person_id>` - Actualizar persona
- `DELETE /api/persons/<person_id>` - Desactivar persona
- `GET /api/persons/stats` - Estadísticas de personas

### 🤖 Machine Learning (`/api/ml`)
- `POST /api/ml/prediccion-riesgo` - Predecir riesgo de tarea
- `POST /api/ml/tiempo-real` - Predecir duración de tarea
- `POST /api/ml/recomendar-persona` - Recomendar persona para tarea
- `POST /api/ml/desempeno` - Analizar desempeño
- `POST /api/ml/proceso` - Análisis de proceso mining
- `GET /api/ml/health` - Estado de modelos ML

### 🔧 Sistema
- `GET /health` - Health check del servidor
- `GET /` - Información de la API

## Autenticación

Todos los endpoints (excepto `/health`, `/` y `/api/auth/login`) requieren autenticación JWT.

**Header requerido:**
```
Authorization: Bearer <access_token>
```

## Permisos

Los usuarios tienen diferentes permisos según su rol:
- `tasks.view` - Ver tareas
- `tasks.create` - Crear tareas
- `tasks.edit` - Editar tareas
- `tasks.delete` - Eliminar tareas
- `users.view` - Ver usuarios
- `users.create` - Crear usuarios
- `users.edit` - Editar usuarios
- `users.delete` - Eliminar usuarios
- `settings.manage` - Gestionar configuración
- `ml.use` - Usar funciones ML
- `reports.view` - Ver reportes
- `reports.export` - Exportar reportes

## Estado del Backend

✅ **Todos los módulos implementados:**
- ✅ Autenticación y autorización
- ✅ CRUD de tareas
- ✅ CRUD de áreas
- ✅ CRUD de usuarios
- ✅ CRUD de personas
- ✅ Modelos de Machine Learning
- ✅ Estadísticas y reportes
- ✅ Validación y manejo de errores
- ✅ CORS configurado
- ✅ JWT tokens
- ✅ Permisos por rol

## Base de Datos

El sistema utiliza MySQL con dos bases de datos:
- `sb` (producción) - Datos actuales del sistema
- `sb_training` (opcional) - Datos históricos para entrenamiento ML

## Configuración

Ver archivo `.env` para configuración de:
- Credenciales de base de datos
- Claves secretas JWT
- CORS origins
- Variables de entorno

## Ejecución

```bash
cd backend
python app.py
```

El servidor estará disponible en `http://127.0.0.1:5000`
