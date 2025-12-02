# 🤖 Sistema de Machine Learning - ProcessMart

## 📋 Descripción

Sistema completo de Machine Learning para clasificación de riesgo de tareas usando CatBoost Multiclass.

---

## 🗂️ Estructura de Directorios

```
ml/
├── models/
│   ├── risk/                          ⭐ MODELO DE CLASIFICACIÓN DE RIESGO
│   │   ├── model_catboost_multiclass.pkl       (Modelo entrenado)
│   │   ├── preprocessor.pkl                    (Preprocessor - CRÍTICO)
│   │   ├── model_config.json                   (Configuración y features)
│   │   ├── optuna_study.json                   (Hiperparámetros optimizados)
│   │   └── metrics/
│   │       ├── confusion_matrix.png
│   │       ├── feature_importance.png
│   │       ├── feature_importance.csv
│   │       └── classification_report.csv
│   │
│   └── training/
│       └── train_catboost_multiclass.py        (Script de entrenamiento)
│
└── README.md (este archivo)
```

---

## 🚀 Quick Start

### 1. Copiar tu modelo entrenado

```powershell
# Desde tu proyecto de entrenamiento
$origen = "C:\ruta\a\tu\modelo"

# Copiar archivos esenciales
Copy-Item "$origen\model_catboost_multiclass.pkl" ".\ml\models\risk\"
Copy-Item "$origen\preprocessor.pkl" ".\ml\models\risk\"
Copy-Item "$origen\model_config.json" ".\ml\models\risk\"

# Copiar métricas (opcional)
Copy-Item "$origen\*.png" ".\ml\models\risk\metrics\"
Copy-Item "$origen\*.csv" ".\ml\models\risk\metrics\"
```

### 2. Instalar dependencias

```bash
pip install catboost optuna scikit-learn pandas numpy
```

### 3. Verificar

```python
from app.ml.risk_model import load_model
model = load_model()
print("✅ Modelo cargado correctamente" if model else "❌ Error")
```

---

## 📦 Archivos del Modelo

### `model_catboost_multiclass.pkl` ⭐
- **Descripción:** Modelo CatBoost entrenado
- **Tamaño:** Variable (~5-50 MB)
- **Uso:** Hacer predicciones en producción
- **Obligatorio:** ✅ SÍ

### `preprocessor.pkl` ⭐⭐⭐
- **Descripción:** Preprocessor (scaler + label encoders)
- **Contiene:**
  - `scaler`: StandardScaler para normalizar features numéricas
  - `label_encoders`: LabelEncoders para features categóricas
  - `feature_columns`: Lista de columnas en orden
  - `categorical_features` y `numerical_features`
- **Uso:** Transformar datos antes de predecir
- **Obligatorio:** ✅ SÍ (sin esto las predicciones fallan)

### `model_config.json` ⭐
- **Descripción:** Configuración completa del modelo
- **Contiene:**
  ```json
  {
    "model_type": "CatBoostClassifier",
    "features": [...],          // 32 features usadas
    "n_features": 32,
    "classes": ["bajo", "medio", "alto"],
    "training_date": "20231130_140500",
    "accuracy": 0.8956,
    "best_params": {...}
  }
  ```
- **Obligatorio:** ✅ SÍ

### `optuna_study.json`
- **Descripción:** Estudio de optimización de Optuna
- **Uso:** Documentación del proceso de optimización
- **Obligatorio:** ❌ NO (opcional)

### `metrics/confusion_matrix.png`
- **Descripción:** Visualización de la matriz de confusión
- **Uso:** Mostrar en UI de Configuración IA
- **Obligatorio:** ❌ NO (recomendado)

### `metrics/feature_importance.png`
- **Descripción:** Top 20 features más importantes
- **Uso:** Mostrar en UI de Configuración IA
- **Obligatorio:** ❌ NO (recomendado)

### `metrics/feature_importance.csv`
- **Descripción:** Tabla completa de importancia de features
- **Uso:** Análisis detallado
- **Obligatorio:** ❌ NO

### `metrics/classification_report.csv`
- **Descripción:** Métricas detalladas por clase (precision, recall, f1-score)
- **Uso:** Evaluar rendimiento del modelo
- **Obligatorio:** ❌ NO

---

## 🔧 Cómo Funciona

### Flujo de Predicción

```python
# 1. Usuario envía datos
task_data = {
    'complexity_level': 'alta',
    'priority': 'alta',
    'area': 'Desarrollo',
    'task_type': 'Implementación',
    'duration_est': 20,
    'assignees_count': 3,
    'dependencies': 2
}

# 2. Backend carga modelo y preprocessor
model = load_model()
preprocessor = load_preprocessor()

# 3. Preparar features
features = prepare_features(task_data)
# -> Aplica label encoding a categóricas
# -> Normaliza numéricas con scaler
# -> Resultado: array de 32 valores

# 4. Hacer predicción
prediction = model.predict([features])
probabilities = model.predict_proba([features])

# 5. Retornar resultado
{
    'risk_level': 'alto',
    'probability': 0.87,
    'probabilities': {
        'bajo': 0.05,
        'medio': 0.08,
        'alto': 0.87
    }
}
```

### Flujo de Reentrenamiento

```python
# 1. Usuario Super Admin hace clic en "Reentrenar"
# 2. Backend extrae datos de la BD (tabla 'task')
data = get_training_data_from_db()

# 3. Preparar features
X, y, feature_names, preprocessor = prepare_risk_features(data)

# 4. Optimizar hiperparámetros con Optuna (opcional)
best_params = optimize_catboost(X_train, y_train, n_trials=50)

# 5. Entrenar modelo
model = CatBoostClassifier(**best_params)
model.fit(X_train, y_train)

# 6. Evaluar
accuracy = accuracy_score(y_test, y_pred)

# 7. Guardar modelo, preprocessor, config, métricas
joblib.dump(model, 'model_catboost_multiclass.pkl')
joblib.dump(preprocessor, 'preprocessor.pkl')
# ... guardar otros archivos

# 8. Modelo actualizado disponible inmediatamente
```

---

## 📊 Features del Modelo

### Features Categóricas (ejemplo)
- `complexity_level` → ['baja', 'media', 'alta']
- `priority` → ['baja', 'media', 'alta', 'crítica']
- `area_name` → ['Ventas', 'Desarrollo', 'Marketing', ...]
- `task_type` → ['Implementación', 'Análisis', 'Diseño', ...]
- `status` → ['pendiente', 'en_progreso', 'completada', ...]

### Features Numéricas (ejemplo)
- `duration_est` → Días estimados (0-365)
- `assignees_count` → Número de personas asignadas (0-10)
- `dependencies_count` → Número de dependencias (0-20)
- `completion_percentage` → Porcentaje completado (0-100)
- `days_elapsed` → Días transcurridos (0-365)

**IMPORTANTE:** Ajusta estas features según tu modelo original.

---

## 🔄 Actualizar el Modelo

### Opción 1: Copiar modelo nuevo (Manual)

```powershell
# Copiar desde tu proyecto de entrenamiento
Copy-Item "C:\nuevo\modelo\model_catboost_multiclass.pkl" ".\ml\models\risk\" -Force
Copy-Item "C:\nuevo\modelo\preprocessor.pkl" ".\ml\models\risk\" -Force
Copy-Item "C:\nuevo\modelo\model_config.json" ".\ml\models\risk\" -Force

# Reiniciar servidor Flask
```

### Opción 2: Reentrenar desde la UI (Automático)

1. Ir a "Configuración IA"
2. Click en "Reentrenar Modelo"
3. El modelo se entrena con datos actuales de la BD
4. Se guarda automáticamente
5. Disponible de inmediato (sin reiniciar)

---

## 🧪 Testing

### Test Manual

```python
# backend/test_risk_model.py
from app.ml.risk_model import predict_risk

test_cases = [
    # Caso 1: Riesgo Alto
    {
        'complexity_level': 'alta',
        'priority': 'crítica',
        'area': 'Desarrollo',
        'task_type': 'Implementación',
        'duration_est': 45,
        'assignees_count': 0,
        'dependencies': 5
    },
    # Caso 2: Riesgo Bajo
    {
        'complexity_level': 'baja',
        'priority': 'baja',
        'area': 'Ventas',
        'task_type': 'Seguimiento',
        'duration_est': 5,
        'assignees_count': 2,
        'dependencies': 0
    }
]

for i, test in enumerate(test_cases, 1):
    result = predict_risk(test)
    print(f"Test {i}: {result['risk_level']} ({result['probability']:.2%})")
```

### Test de Endpoint

```bash
curl -X POST http://localhost:5000/api/ml/prediccion-riesgo \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "complexity_level": "alta",
    "priority": "alta",
    "area": "Desarrollo",
    "task_type": "Implementación",
    "duration_est": 20,
    "assignees_count": 3,
    "dependencies": 2
  }'
```

---

## 📝 Notas Importantes

### ⚠️ Compatibilidad
- El `preprocessor.pkl` debe ser compatible con el modelo
- Ambos deben generarse juntos en el mismo entrenamiento
- No mezclar preprocessor de un entrenamiento con modelo de otro

### 🔒 Seguridad
- Solo usuarios `super_admin` pueden reentrenar modelos
- Los archivos `.pkl` son binarios - verifica su integridad
- No expongas endpoints de entrenamiento sin autenticación

### 📈 Performance
- Modelo se carga una vez al iniciar el servidor (lazy loading)
- Predicciones son muy rápidas (~5-20ms)
- Reentrenamiento puede tomar varios minutos (según datos y Optuna trials)

### 🐛 Debugging
```python
# Ver features del modelo
from app.ml.risk_model import _model_config
print(_model_config['features'])

# Ver classes
print(_model_config['classes'])

# Ver accuracy
print(_model_config['accuracy'])
```

---

## 🆘 Troubleshooting

### Problema: "Modelo no se carga"
**Solución:**
```bash
# Verificar que existen los archivos
ls ml/models/risk/model_catboost_multiclass.pkl
ls ml/models/risk/preprocessor.pkl

# Ver logs del servidor
python app.py  # Buscar mensajes de error
```

### Problema: "Features no coinciden"
**Solución:**
```python
# Comparar features enviadas vs esperadas
from app.ml.risk_model import _model_config
print("Features esperadas:", _model_config['features'])

# Asegúrate de enviar exactamente esas features
```

### Problema: "ValueError: Unknown label"
**Solución:**
- Un valor categórico no existe en el LabelEncoder
- Ejemplo: enviaste `complexity_level='muy_alta'` pero el modelo solo conoce `['baja', 'media', 'alta']`
- Solución: Usar solo valores que existan en el entrenamiento

---

## 📚 Referencias

- [CatBoost Documentation](https://catboost.ai/docs/)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)

---

## 👥 Contacto

Para dudas sobre el modelo ML, contactar al equipo de Data Science.
