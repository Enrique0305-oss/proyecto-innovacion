



proyecto-innovacion/
├─ backend/  (Flask + ML)
│  ├─ app.py | config.py | requirements.txt
│  ├─ app/
│  │  ├─ __init__.py | extensions.py
│  │  ├─ models/  [__init__.py, user.py, role.py, area.py, person.py, task.py, web_user.py, web_task.py, ml_models.py]
│  │  ├─ routes/  [__init__.py, auth_routes.py, user_routes.py, area_routes.py, person_routes.py, task_routes.py, ml_routes.py, ml_training_routes.py]
│  │  └─ ml/      [__init__.py, risk_model.py, duration_model.py, recommender_model.py, performance_model.py, process_mining.py, model_trainer.py]
│  ├─ ml/
│  │  ├─ models/risk/  [model_binary_task_risk.cbm, columns_binary.json, metrics_binary.json]
│  │  └─ training/     [scripts de entrenamiento]
│  └─ scripts/         [init_database.py, check_users.py, cleanup_roles.py, update_passwords.py]
│
├─ sistema-productivo/  (Frontend TS + Vite)
│  ├─ index.html | package.json | tsconfig.json
│  ├─ public/
│  └─ src/
│     ├─ main.ts | counter.ts | style.css
│     ├─ components/  [Sidebar.ts, AIAssistant.ts, MetricCard.ts]
│     ├─ pages/       [Login.ts, Dashboard.ts, Areas.ts, Tasks.ts, Users.ts, Performance.ts, RiskClassification.ts,
│     │               DurationPrediction.ts, PersonTaskRecommendation.ts, ProcessSimulation.ts, IntelligentVisualization.ts, IAConfiguration.ts]
│     ├─ styles/      [reset.css, variables.css, login.css, dashboard.css, areas.css, tasks.css, users.css, performance.css,
│     │               risk-classification.css, duration-prediction.css, person-task-recommendation.css, process-simulation.css,
│     │               intelligent-visualization.css, ia-configuration.css, ai-assistant.css]
│     └─ utils/       [api.ts, router.ts]
│
├─ database/  (SQL + docs)
│  ├─ 01_create_sb_production.sql | 02_rename_sb_to_training.sql | 03_populate_production_people.sql
│  └─ README.md
│
└─ docs/
   ├─ GUIA_INTEGRACION_MODELO_CATBOOST.md | GUIA_ROLES.md | INTEGRACION_COMPLETA.md | INTEGRACION_ML_COMPLETADA.md
   ├─ RESUMEN_INTEGRACION_ML.md | ROLE_BASED_ACCESS.md | API_ENDPOINTS.md
