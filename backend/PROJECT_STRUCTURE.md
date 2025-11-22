# Estructura Completa del Backend

```
backend/
│
├── 📁 app/                              # Aplicación Flask
│   │
│   ├── __init__.py                     # Factory pattern, creación de app Flask
│   │                                   # - create_app(config)
│   │                                   # - Error handlers (404, 500, 400, 401, 403)
│   │                                   # - Health check endpoint
│   │
│   ├── extensions.py                   # Inicialización de extensiones
│   │                                   # - SQLAlchemy (db)
│   │                                   # - Flask-Migrate (migrate)
│   │                                   # - Flask-CORS (cors)
│   │                                   # - Flask-JWT-Extended (jwt)
│   │
│   ├── 📁 models/                      # Modelos de base de datos (SQLAlchemy ORM)
│   │   ├── __init__.py                # Exportación de modelos
│   │   │
│   │   ├── user.py                    # Modelo de Usuarios
│   │   │   └── User
│   │   │       ├── id (PK)
│   │   │       ├── username (unique)
│   │   │       ├── email (unique)
│   │   │       ├── password_hash
│   │   │       ├── role (admin/user)
│   │   │       ├── created_at
│   │   │       ├── set_password()
│   │   │       ├── check_password()
│   │   │       └── to_dict()
│   │   │
│   │   ├── person.py                  # Modelo de Personas/Empleados
│   │   │   └── Person
│   │   │       ├── person_id (PK)
│   │   │       ├── first_name, last_name
│   │   │       ├── area, role
│   │   │       ├── experience_years
│   │   │       ├── performance_index
│   │   │       ├── satisfaction_score
│   │   │       ├── attrition_risk
│   │   │       ├── technical_skills
│   │   │       ├── education_level
│   │   │       ├── salary_level
│   │   │       ├── resigned (boolean)
│   │   │       └── to_dict()
│   │   │
│   │   └── task.py                    # Modelos de Tareas
│   │       ├── Task                   # Tarea principal
│   │       │   ├── task_id (PK)
│   │       │   ├── task_name
│   │       │   ├── project_id
│   │       │   ├── area
│   │       │   ├── task_type
│   │       │   ├── start_date_est, end_date_est
│   │       │   ├── start_date_real, end_date_real
│   │       │   ├── duration_est, duration_real
│   │       │   ├── status
│   │       │   ├── priority
│   │       │   ├── complexity_level
│   │       │   ├── completion
│   │       │   ├── tools_used
│   │       │   ├── dependencies
│   │       │   ├── assignees (relationship)
│   │       │   └── to_dict()
│   │       │
│   │       ├── Assignee              # Asignación Persona-Tarea
│   │       │   ├── id (PK)
│   │       │   ├── task_id (FK)
│   │       │   ├── person_id (FK)
│   │       │   ├── person (relationship)
│   │       │   └── to_dict()
│   │       │
│   │       └── TaskDependency        # Dependencias entre tareas
│   │           ├── id (PK)
│   │           ├── task_id (FK)
│   │           ├── depends_on_task_id (FK)
│   │           └── to_dict()
│   │
│   ├── 📁 routes/                      # Blueprints de rutas/endpoints
│   │   ├── __init__.py                # Registro de blueprints
│   │   │
│   │   ├── auth_routes.py             # Rutas de Autenticación
│   │   │   ├── POST   /api/auth/register
│   │   │   ├── POST   /api/auth/login
│   │   │   ├── GET    /api/auth/me
│   │   │   ├── PUT    /api/auth/change-password
│   │   │   └── GET    /api/auth/users (admin)
│   │   │
│   │   ├── task_routes.py             # Rutas de Tareas (CRUD)
│   │   │   ├── GET    /api/tasks/                    (listar con paginación)
│   │   │   ├── GET    /api/tasks/<id>                (obtener una)
│   │   │   ├── POST   /api/tasks/                    (crear)
│   │   │   ├── PUT    /api/tasks/<id>                (actualizar)
│   │   │   ├── DELETE /api/tasks/<id>                (eliminar)
│   │   │   ├── POST   /api/tasks/<id>/assignees      (asignar persona)
│   │   │   ├── DELETE /api/tasks/<id>/assignees/<pid> (remover asignación)
│   │   │   └── GET    /api/tasks/stats               (estadísticas)
│   │   │
│   │   └── ml_routes.py               # Rutas de Machine Learning
│   │       ├── POST   /api/ml/prediccion-riesgo     (riesgo de tarea)
│   │       ├── POST   /api/ml/tiempo-real           (duración estimada)
│   │       ├── POST   /api/ml/recomendar-persona    (mejor persona)
│   │       ├── POST   /api/ml/desempeno             (desempeño esperado)
│   │       ├── POST   /api/ml/proceso               (process mining)
│   │       └── GET    /api/ml/health                (estado de modelos)
│   │
│   └── 📁 ml/                          # Módulos de Machine Learning
│       ├── __init__.py
│       │
│       ├── risk_model.py              # Predicción de Riesgo
│       │   ├── load_model()          # Carga risk_model.pkl
│       │   ├── predict_risk()        # Predicción principal
│       │   └── predict_risk_heuristic() # Fallback sin modelo
│       │
│       ├── duration_model.py          # Predicción de Duración
│       │   ├── load_model()          # Carga duration_model.pkl
│       │   ├── predict_duration()    # Predicción principal
│       │   └── predict_duration_heuristic()
│       │
│       ├── recommender_model.py       # Recomendación de Personas
│       │   ├── load_model()          # Carga recommender_model.pkl
│       │   ├── recommend_person()    # Recomendación principal
│       │   ├── recommend_person_heuristic()
│       │   ├── get_candidates()      # Query a BD
│       │   ├── calculate_heuristic_score()
│       │   └── get_current_workload()
│       │
│       ├── performance_model.py       # Predicción de Desempeño
│       │   ├── load_model()          # Carga performance_model.pkl
│       │   ├── predict_performance() # Predicción principal
│       │   ├── predict_performance_heuristic()
│       │   ├── identify_strengths()
│       │   ├── identify_weaknesses()
│       │   └── get_historical_performance()
│       │
│       └── process_mining.py          # Minería de Procesos
│           ├── load_model()          # Carga process_mining.pkl
│           ├── analyze_process()     # Análisis principal
│           ├── analyze_process_heuristic()
│           ├── analyze_task_flow()
│           ├── identify_bottlenecks()
│           ├── calculate_average_duration()
│           └── find_common_sequences()
│
├── 📁 models/                          # Modelos ML entrenados (.pkl)
│   ├── risk_model.pkl                 # Modelo de riesgo
│   ├── risk_encoders.pkl              # Label encoders para riesgo
│   ├── duration_model.pkl             # Modelo de duración
│   ├── duration_scaler.pkl            # Scaler para features
│   ├── recommender_model.pkl          # Modelo de recomendación
│   ├── performance_model.pkl          # Modelo de desempeño
│   └── process_mining.pkl             # Analizador de procesos
│
├── 📁 migrations/                      # Migraciones de base de datos (Flask-Migrate)
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── *.py                       # Archivos de migración
│
├── 📁 venv/                            # Entorno virtual de Python (no versionar)
│
├── config.py                          # Configuración por entornos
│   ├── Config                        # Clase base
│   ├── DevelopmentConfig             # Desarrollo
│   ├── ProductionConfig              # Producción
│   └── TestingConfig                 # Testing
│
├── app.py                             # Punto de entrada de la aplicación
│   └── if __name__ == '__main__':
│       └── app.run(host='0.0.0.0', port=5000, debug=True)
│
├── requirements.txt                   # Dependencias de Python
│   ├── Flask==3.0.0
│   ├── Flask-SQLAlchemy==3.1.1
│   ├── Flask-Migrate==4.0.5
│   ├── Flask-CORS==4.0.0
│   ├── Flask-JWT-Extended==4.6.0
│   ├── PyMySQL==1.1.0
│   ├── python-dotenv==1.0.0
│   ├── scikit-learn==1.3.2
│   ├── pandas==2.1.4
│   ├── numpy==1.26.2
│   ├── catboost==1.2.2
│   ├── joblib==1.3.2
│   ├── gunicorn==21.2.0
│   └── werkzeug==3.0.1
│
├── .env.example                       # Ejemplo de variables de entorno
│   ├── FLASK_APP=app.py
│   ├── FLASK_ENV=development
│   ├── SECRET_KEY=...
│   ├── DB_HOST=localhost
│   ├── DB_PORT=3306
│   ├── DB_USER=root
│   ├── DB_PASSWORD=...
│   ├── DB_NAME=sb
│   ├── JWT_SECRET_KEY=...
│   ├── CORS_ORIGINS=...
│   └── MODELS_PATH=models
│
├── .env                               # Variables de entorno (NO versionar)
│
├── .gitignore                         # Archivos a ignorar en Git
│   ├── __pycache__/
│   ├── venv/
│   ├── .env
│   ├── *.pyc
│   ├── instance/
│   └── migrations/ (opcional)
│
├── README.md                          # Documentación principal
│   ├── Características
│   ├── Instalación paso a paso
│   ├── Configuración
│   ├── API Endpoints
│   ├── Modelos ML
│   ├── Producción
│   ├── Testing
│   ├── Troubleshooting
│   └── Desarrollo
│
├── API_EXAMPLES.md                    # Ejemplos de uso de la API
│   ├── Autenticación (curl + PowerShell)
│   ├── CRUD de Tareas
│   ├── Endpoints ML con respuestas esperadas
│   └── Códigos HTTP
│
└── init_backend.ps1                   # Script de inicialización rápida
    ├── Verificar Python
    ├── Crear venv
    ├── Instalar dependencias
    ├── Configurar .env
    └── Instrucciones siguientes pasos
```

---

## 📊 Flujo de Datos

### 1. Request Flow
```
Cliente (Frontend/Postman)
    ↓
[Authorization Header: Bearer TOKEN]
    ↓
Flask App (app.py)
    ↓
Blueprint Route (/api/auth, /api/tasks, /api/ml)
    ↓
@jwt_required() Decorator (validación de token)
    ↓
Controller Logic (validaciones, transformaciones)
    ↓
┌─────────────────┬──────────────────┐
│                 │                  │
Model (ORM)   ML Module        Direct Response
    ↓              ↓                 │
Database      Model.pkl            │
    ↓              ↓                 │
└─────────────────┴──────────────────┘
    ↓
JSON Response
    ↓
Cliente
```

### 2. Authentication Flow
```
POST /api/auth/register
    ↓
Validar datos
    ↓
Hash password (werkzeug.security)
    ↓
Guardar en BD (users table)
    ↓
Generar JWT token
    ↓
Retornar {user, access_token}
```

### 3. ML Prediction Flow
```
POST /api/ml/prediccion-riesgo
    ↓
Extraer features del request
    ↓
¿Existe modelo .pkl?
    ├─ Sí → Cargar modelo con joblib
    │        ↓
    │    model.predict(features)
    │        ↓
    │    Clasificar resultado
    │
    └─ No → predict_risk_heuristic()
             ↓
         Reglas de negocio
    ↓
Generar recommendations
    ↓
Retornar {risk_level, probability, factors, recommendations}
```

---

## 🔑 Variables Clave

### Environment Variables (.env)
| Variable | Propósito | Ejemplo |
|----------|-----------|---------|
| `FLASK_APP` | Punto de entrada | `app.py` |
| `FLASK_ENV` | Modo de ejecución | `development`/`production` |
| `SECRET_KEY` | Firma de sesiones | `secrets.token_hex(32)` |
| `DB_HOST` | Host de MySQL | `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_USER` | Usuario de BD | `root` |
| `DB_PASSWORD` | Contraseña de BD | `tu_password` |
| `DB_NAME` | Nombre de BD | `sb` |
| `JWT_SECRET_KEY` | Firma de tokens JWT | `token_hex(32)` |
| `CORS_ORIGINS` | Dominios permitidos | `http://localhost:3000` |
| `MODELS_PATH` | Ruta de modelos ML | `models` |

---

## 🗄️ Esquema de Base de Datos

### Tablas Principales

**users** (Autenticación)
- id (PK)
- username (UNIQUE)
- email (UNIQUE)
- password_hash
- role
- created_at

**people** (Empleados/Personas)
- person_id (PK)
- first_name, last_name
- area, role
- experience_years
- performance_index
- satisfaction_score
- technical_skills
- education_level
- salary_level
- resigned

**tasks** (Tareas)
- task_id (PK)
- task_name
- project_id
- area, task_type
- start_date_est, end_date_est
- start_date_real, end_date_real
- duration_est, duration_real
- status, priority
- complexity_level
- completion
- tools_used
- dependencies

**assignees** (Asignaciones)
- id (PK)
- task_id (FK → tasks)
- person_id (FK → people)

**task_dependencies** (Dependencias)
- id (PK)
- task_id (FK → tasks)
- depends_on_task_id (FK → tasks)

---

## 🚀 Comandos Útiles

```powershell
# Entorno virtual
.\venv\Scripts\Activate.ps1
deactivate

# Dependencias
pip install -r requirements.txt
pip freeze > requirements.txt

# Base de datos
flask db init
flask db migrate -m "Mensaje"
flask db upgrade
flask db downgrade

# Ejecutar servidor
python app.py
flask run
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Testing
curl http://localhost:5000/health
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

---

**Última actualización:** Enero 2024
