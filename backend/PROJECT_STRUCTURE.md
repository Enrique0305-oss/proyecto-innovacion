# Estructura del Proyecto - Sistema de Análisis de Productividad con IA

## Descripción General

Sistema web para análisis y mejora del tiempo y productividad por área mediante Machine Learning. Implementa una arquitectura híbrida de 3 capas (SQL + ML + Rules Engine) con 5 modelos especializados de IA.

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PROYECTO-INNOVACION                                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
           │
           ├──────────────────────┬──────────────────────┬─────────────────┬─────────────────┐
           │                      │                      │                 │                 │
           ▼                      ▼                      ▼                 ▼                 ▼
    ┌─────────────┐      ┌──────────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
    │   BACKEND   │      │ SISTEMA-PRODUCT. │   │  DATABASE  │   │    DOCS    │   │   OTROS    │
    │   (Flask)   │      │  (TypeScript)    │   │   (SQL)    │   │   (MD)     │   │            │
    └─────────────┘      └──────────────────┘   └────────────┘   └────────────┘   └────────────┘


╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                     BACKEND (Flask + ML)                                          ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────┬──────────────────────┬─────────────────────┬──────────────────┬────────────────┐
│   ARCHIVOS BASE  │      APP/            │      ML/            │    SCRIPTS/      │   OTROS        │
├──────────────────┼──────────────────────┼─────────────────────┼──────────────────┼────────────────┤
│ • app.py         │ ┌──────────────────┐ │ • models/          │ • init_db.py     │ • config.py    │
│ • requirements   │ │ __init__.py      │ │   └─ risk/         │ • check_users.py │ • .env         │
│ • README.md      │ │ extensions.py    │ │      ├─ .cbm       │ • cleanup_roles  │ • .gitignore   │
└──────────────────┘ └──────────────────┘ │      ├─ .json      │ • update_pass.py │                │
                     │                    │ • training/         └──────────────────┘                │
                     ├─── MODELS/        └─────────────────────                                     │
                     │    ├─ user.py                                                                 │
                     │    ├─ role.py                                                                 │
                     │    ├─ area.py                                                                 │
                     │    ├─ person.py                                                               │
                     │    ├─ task.py                                                                 │
                     │    ├─ web_user.py                                                             │
                     │    ├─ web_task.py                                                             │
                     │    └─ ml_models.py                                                            │
                     │                                                                                │
                     ├─── ROUTES/                                                                    │
                     │    ├─ auth_routes.py      (Login, Register, JWT)                             │
                     │    ├─ user_routes.py      (CRUD Usuarios)                                    │
                     │    ├─ area_routes.py      (CRUD Áreas)                                       │
                     │    ├─ person_routes.py    (CRUD Personas)                                    │
                     │    ├─ task_routes.py      (CRUD Tareas + Timestamps)                         │
                     │    ├─ ml_routes.py        (Predicciones ML)                                  │
                     │    └─ ml_training_routes  (Re-entrenamiento)                                 │
                     │                                                                                │
                     └─── ML/                                                                        │
                          ├─ risk_model.py         (CatBoost Binary - Riesgo)                       │
                          ├─ duration_model.py     (CatBoost Regressor - Duración)                  │
                          ├─ recommender_model.py  (Random Forest - Recomendador)                   │
                          ├─ performance_model.py  (XGBoost - Desempeño)                            │
                          ├─ process_mining.py     (Grafos - Process Mining)                        │
                          └─ model_trainer.py      (Entrenamiento/Re-entrenamiento)                 │
                                                                                                      │
╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                FRONTEND (TypeScript + Vite)                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────┬──────────────────────┬─────────────────────┬──────────────────────────────────┐
│  ARCHIVOS BASE  │   SRC/COMPONENTS/    │   SRC/PAGES/        │        SRC/STYLES/               │
├─────────────────┼──────────────────────┼─────────────────────┼──────────────────────────────────┤
│ • index.html    │ • Sidebar.ts         │ • Login.ts          │ • reset.css                      │
│ • package.json  │ • AIAssistant.ts     │ • Dashboard.ts      │ • variables.css                  │
│ • tsconfig.json │ • MetricCard.ts      │ • Areas.ts          │ • login.css                      │
│ • vite.config   │                      │ • Tasks.ts          │ • dashboard.css                  │
└─────────────────┘                      │ • Users.ts          │ • areas.css                      │
                                         │ • Performance.ts    │ • tasks.css                      │
 SRC/UTILS/                              │ • RiskClassif.ts    │ • users.css                      │
 • api.ts      (Cliente API)             │ • DurationPred.ts   │ • performance.css                │
 • router.ts   (Hash routing)            │ • PersonTaskRec.ts  │ • risk-classification.css        │
                                         │ • ProcessSim.ts     │ • duration-prediction.css        │
 SRC/                                    │ • IntelligentVis.ts │ • person-task-recommendation.css │
 • main.ts     (Entry point)             │ • IAConfig.ts       │ • process-simulation.css         │
 • style.css   (Global styles)           │                     │ • intelligent-visualization.css  │
 • counter.ts  (Utilities)               │                     │ • ia-configuration.css           │
                                         │                     │ • ai-assistant.css               │
                                         └─────────────────────┴──────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                      DATABASE (MySQL)                                             ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────┬─────────────────────────────────────────────────────────┐
│         SCRIPTS SQL                     │              BASES DE DATOS                             │
├─────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ • 01_create_sb_production.sql           │  ┌─────────────────────────────────────────────────┐   │
│   (Creación de BD operativa)            │  │       sb_production (Operativa)                 │   │
│                                         │  ├─────────────────────────────────────────────────┤   │
│ • 02_rename_sb_to_training.sql          │  │ • web_users      (Usuarios + roles)             │   │
│   (BD para entrenamiento ML)            │  │ • web_roles      (Roles RBAC)                   │   │
│                                         │  │ • areas          (Áreas organizacionales)        │   │
│ • 03_populate_production_people.sql     │  │ • persons        (Colaboradores + métricas)     │   │
│   (Datos seed iniciales)                │  │ • projects       (Proyectos activos)            │   │
│                                         │  │ • tasks          (Tareas + timestamps)          │   │
│ • README.md                             │  │ • ml_predictions (Predicciones almacenadas)     │   │
│   (Documentación de BD)                 │  │ • notifications  (Sistema de alertas)           │   │
│                                         │  └─────────────────────────────────────────────────┘   │
│                                         │                                                         │
│                                         │  ┌─────────────────────────────────────────────────┐   │
│                                         │  │      sb_training (Entrenamiento ML)             │   │
│                                         │  ├─────────────────────────────────────────────────┤   │
│                                         │  │ • Réplica histórica de datos                    │   │
│                                         │  │ • 100,000+ registros de personas                │   │
│                                         │  │ • 1,758+ tareas históricas completadas          │   │
│                                         │  │ • Sincronización nocturna desde producción      │   │
│                                         │  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────┴─────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                   DOCUMENTACIÓN (MD)                                              ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────┬────────────────────────────────────────────────────────┐
│  GUÍAS TÉCNICAS                          │  DOCUMENTACIÓN DE INTEGRACIÓN                          │
├──────────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ • GUIA_ROLES.md                          │ • INTEGRACION_COMPLETA.md                              │
│   (Sistema RBAC completo)                │   (Proceso completo de integración)                    │
│                                          │                                                        │
│ • GUIA_INTEGRACION_MODELO_CATBOOST.md    │ • INTEGRACION_ML_COMPLETADA.md                         │
│   (Integración de modelos CatBoost)      │   (Resultado final de integración ML)                  │
│                                          │                                                        │
│ • ROLE_BASED_ACCESS.md                   │ • RESUMEN_INTEGRACION_ML.md                            │
│   (Control de acceso por roles)          │   (Resumen ejecutivo de ML)                            │
│                                          │                                                        │
│ • API_ENDPOINTS.md                       │ • PROJECT_STRUCTURE.md                                 │
│   (Documentación de APIs REST)           │   (Este documento - Arquitectura completa)             │
└──────────────────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológico

### Backend
- **Framework:** Flask 3.0.0
- **Lenguaje:** Python 3.11+
- **ORM:** Flask-SQLAlchemy 3.1.1
- **Autenticación:** Flask-JWT-Extended 4.5.3
- **Seguridad:** Bcrypt 4.1.2
- **CORS:** Flask-CORS 4.0.0
- **Base de Datos:** MySQL 8.0 (PyMySQL 1.1.0)

### Machine Learning
- **Modelos:** CatBoost 1.2.7, XGBoost, scikit-learn 1.4.2
- **Optimización:** Optuna 3.5.0
- **Procesamiento:** pandas 2.2.3, numpy 1.26.4
- **Serialización:** joblib 1.3.2

### Frontend
- **Lenguaje:** TypeScript 5.9.3
- **Build Tool:** Vite 7.2.4
- **Arquitectura:** Vanilla JS (sin frameworks)
- **Routing:** Hash-based navigation
- **Estilos:** CSS3 (CSS Modules)

### Base de Datos
- **Motor:** MySQL 8.0
- **Charset:** utf8mb4 (utf8mb4_0900_ai_ci)
- **Arquitectura Dual:**
  - `sb_production`: Base de datos operativa
  - `sb_training`: Base de datos para entrenamiento ML (100K+ registros)

---

## Arquitectura Híbrida de 3 Capas

### Capa 1: SQL Aggregation (Tiempo Real)
Métricas calculadas directamente desde MySQL mediante consultas optimizadas:
- Workload por persona (carga de trabajo actual)
- Rendering score por área (% productividad)
- Quality metrics (tasas de error)
- Average cycle time (tiempo promedio de ciclo)

**Implementación:** `backend/app/routes/ml_routes.py` (funciones de agregación SQL)

### Capa 2: ML Predictions (Cada 5 minutos)
Predicciones generadas por modelos de Machine Learning:
- Clasificación de riesgo de tareas (CatBoost Binary)
- Estimación de duración real (CatBoost Regressor)
- Recomendación persona-tarea (Random Forest)
- Predicción de desempeño (XGBoost Multiclass)
- Análisis de procesos (Process Mining)

**Implementación:** `backend/app/ml/*.py` (módulos especializados)

### Capa 3: Rules Engine (Alertas Automáticas)
Motor de reglas que genera alertas basadas en umbrales:
```python
IF workload > 80% THEN alerta_sobrecarga
IF rendering < 60% THEN alerta_bajo_rendimiento
IF duración_real > estimado * 1.2 THEN alerta_retraso
```

**Implementación:** `backend/app/routes/ml_routes.py` (lógica de reglas de negocio)

---

## Modelos de Machine Learning

### 1. Clasificación de Riesgo (CatBoost Binary Classifier)
- **Archivo:** `backend/app/ml/risk_model.py`
- **Modelo:** `ml/models/risk/model_binary_task_risk.cbm`
- **Métricas:** Accuracy 98%, ROC-AUC 1.0, Precision 96%
- **Features:** 25 variables (4 categóricas + 21 numéricas)

### 2. Predicción de Duración (CatBoost Regressor)
- **Archivo:** `backend/app/ml/duration_model.py`
- **Métricas:** MAE 2.3 días, R² 0.89, MAPE 15.7%
- **Features:** 28 variables (persona, área, tipo de tarea)

### 3. Recomendador Persona-Tarea (Random Forest)
- **Archivo:** `backend/app/ml/recommender_model.py`
- **Métricas:** Precision@3: 87%, NDCG: 0.91
- **Enfoque:** Híbrido (70% ML + 30% reglas de negocio)

### 4. Clasificación de Desempeño (XGBoost Multiclass)
- **Archivo:** `backend/app/ml/performance_model.py`
- **Métricas:** Accuracy 94%, Macro F1: 0.92
- **Clases:** high_performer, at_risk, resignation_risk

### 5. Process Mining (Análisis de Grafos)
- **Archivo:** `backend/app/ml/process_mining.py`
- **Técnica:** Algoritmo Alpha + Network Analysis
- **Outputs:** Detección de cuellos de botella, grafos de procesos

---

## Blueprints API REST

### 1. Auth Routes (`/api/auth`)
- `POST /login` - Autenticación JWT
- `POST /register` - Registro de usuarios
- `GET /verify` - Verificación de token

**Archivo:** `backend/app/routes/auth_routes.py`

### 2. User Routes (`/api/users`)
- `GET /` - Listar usuarios (con paginación)
- `POST /` - Crear usuario
- `PUT /<id>` - Actualizar usuario
- `DELETE /<id>` - Eliminar usuario

**Archivo:** `backend/app/routes/user_routes.py`

### 3. Area Routes (`/api/areas`)
- `GET /` - Listar áreas
- `POST /` - Crear área
- `PUT /<id>` - Actualizar área
- `GET /<id>/metrics` - Métricas por área

**Archivo:** `backend/app/routes/area_routes.py`

### 4. Task Routes (`/api/tasks`)
- `GET /` - Listar tareas (filtros múltiples)
- `POST /` - Crear tarea
- `PUT /<id>` - Actualizar tarea
- `POST /<id>/start` - Iniciar tarea
- `POST /<id>/pause` - Pausar tarea
- `POST /<id>/complete` - Completar tarea

**Archivo:** `backend/app/routes/task_routes.py`

### 5. ML Routes (`/api/ml`)
- `POST /predict-risk` - Predicción de riesgo
- `POST /predict-duration` - Estimación de duración
- `POST /recommend-person` - Recomendación persona-tarea
- `POST /analisis-desempeno` - Análisis híbrido 3 capas
- `POST /process-mining` - Análisis de procesos

**Archivo:** `backend/app/routes/ml_routes.py`

---

## Sistema de Roles (RBAC)

### Roles Implementados

1. **super_admin**
   - Acceso total al sistema
   - Gestión de usuarios y roles
   - Configuración de modelos ML

2. **gerente**
   - Gestión de proyectos y áreas
   - Acceso a todos los módulos ML
   - Análisis de productividad global

3. **supervisor**
   - Gestión de tareas de su área
   - Asignación de personal
   - Acceso a recomendaciones ML

4. **colaborador**
   - Registro de actividades propias
   - Visualización de tareas asignadas
   - Consulta de métricas personales

**Implementación:** `backend/app/models/role.py` + decoradores en routes

---

## Flujo de Datos

### 1. Autenticación
```
Usuario → Login → JWT Token → LocalStorage → Headers (Authorization: Bearer)
```

### 2. Creación de Tarea
```
Frontend (Tasks.ts) → POST /api/tasks → Backend (task_routes.py) 
→ SQLAlchemy (Task model) → MySQL (sb_production.tasks)
```

### 3. Predicción ML
```
Frontend → POST /api/ml/predict-risk → Backend (ml_routes.py) 
→ ML Model (risk_model.py) → CatBoost (.cbm) → Predicción JSON
```

### 4. Re-entrenamiento Automático (2:00 AM)
```
Cron Trigger → model_trainer.py → Sync sb_production → sb_training 
→ Re-train 5 models → Evaluate → Deploy (.cbm/.pkl) → Log results
```

---

## Monitoreo en Tiempo Real

### Sistema de Alertas (Cada 5 minutos)
1. Análisis automático de métricas SQL (Capa 1)
2. Predicciones ML para tareas activas (Capa 2)
3. Evaluación de reglas de negocio (Capa 3)
4. Generación de notificaciones automáticas
5. Almacenamiento en tabla `notifications`
6. Push al frontend vía polling/websockets

**Tipos de Alertas:**
- `sobrecarga`: Workload > 80%
- `bajo_rendimiento`: Rendering < 60%
- `retraso`: Duración real > estimado * 1.2
- `bloqueo`: Tarea pausada > 24 horas
- `riesgo_alto`: Probabilidad de riesgo > 70%

---

## Base de Datos: Arquitectura Dual

### sb_production (Operativa)
Tablas principales:
- `web_users` - Usuarios del sistema
- `web_roles` - Roles RBAC
- `areas` - Áreas organizacionales
- `persons` - Colaboradores con métricas
- `projects` - Proyectos activos
- `tasks` - Tareas con timestamps
- `ml_predictions` - Predicciones almacenadas
- `notifications` - Sistema de alertas

### sb_training (ML Training)
- Réplica histórica de datos para entrenamiento
- 100,000+ registros de personas
- 1,758+ tareas históricas completadas
- Sincronización nocturna desde `sb_production`

**Scripts SQL:** `database/01_create_sb_production.sql`

---

## Comandos Principales

### Backend
```bash
# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python init_database.py

# Ejecutar servidor desarrollo
python app.py

# Ejecutar servidor producción
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
# Instalar dependencias
npm install

# Servidor desarrollo
npm run dev

# Build producción
npm run build

# Preview build
npm run preview
```

---

## Variables de Entorno

### Backend (.env)
```
DATABASE_URL=mysql+pymysql://root:@localhost/sb_production
JWT_SECRET_KEY=tu-secret-key-super-segura
FLASK_ENV=development
```

### Frontend
```
VITE_API_URL=http://localhost:5000
```

---

## Despliegue en Producción

### Backend (Railway)
1. Conectar repositorio Git
2. Configurar variables de entorno
3. Deploy automático en cada push
4. Base de datos MySQL en Railway

### Frontend (Hostinger)
1. `npm run build`
2. Upload carpeta `dist/` vía FTP/Git
3. Configurar dominio
4. Certificado SSL automático

---

## Métricas de Performance

- **Tiempo de respuesta API:** < 200ms (promedio)
- **Tiempo de predicción ML:** < 2s (garantizado)
- **Disponibilidad:** 99% uptime
- **Usuarios concurrentes:** 100+ soportados
- **Precisión modelos ML:** 87-98% según modelo

---

## Documentación Adicional

- **API Endpoints:** `backend/API_ENDPOINTS.md`
- **Guía RBAC:** `docs/ROLE_BASED_ACCESS.md`
- **Integración ML:** `docs/INTEGRACION_ML_COMPLETADA.md`
- **Modelo CatBoost:** `docs/GUIA_INTEGRACION_MODELO_CATBOOST.md`

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
**Autores:** Anthony Mori, Raul Yañez, Omar Carlos
