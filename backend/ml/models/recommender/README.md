# Integración del Modelo CatBoost Recommender

## 📋 Instrucciones de Instalación

### Paso 1: Copiar archivos del modelo

Copia los siguientes archivos desde tu carpeta de entrenamiento a:
`D:\proyecto-innovacion\backend\ml\models\recommender\`

**Archivos principales:**
```
✓ model_catboost_recommender.pkl
✓ columns_recommender.json
✓ recommender_metrics.json
```

**Archivos de visualización (opcional, en subcarpeta metrics/):**
`D:\proyecto-innovacion\backend\ml\models\recommender\metrics\`
```
✓ confusion_matrix.png
✓ roc_curve.png
✓ precision_recall_curve.png
✓ feature_importance.png
✓ probability_distribution.png
✓ feature_importance.csv
✓ ranking_positivos_detallado.json
```

### Paso 2: Verificar la estructura

```
backend/
├── ml/
│   └── models/
│       └── recommender/                    ← CARPETA CREADA
│           ├── model_catboost_recommender.pkl
│           ├── columns_recommender.json
│           ├── recommender_metrics.json
│           └── metrics/
│               ├── confusion_matrix.png
│               ├── roc_curve.png
│               ├── ...
└── app/
    └── ml/
        └── recommender_model.py            ← ACTUALIZADO ✓
```

### Paso 3: Copiar el archivo de entrenamiento (opcional, para referencia)

Copia `train_catboost_recommender.py` a:
`D:\proyecto-innovacion\backend\ml\models\training\`

## 🔧 Cambios Realizados

### 1. Frontend (PersonTaskRecommendation.ts)
✅ Agregado campo **Tipo de Tarea**
✅ Agregado campo **Duración Estimada (días)**
✅ Renombrado "Urgencia" → **Prioridad**
✅ Configurado para enviar datos al API correctamente

### 2. Backend (recommender_model.py)
✅ Actualizado para cargar modelo CatBoost
✅ Función `load_model()` busca en `ml/models/recommender/`
✅ Función `prepare_features()` genera features compatibles con el modelo
✅ Función `recommend_person()` usa predicción del modelo
✅ Fallback heurístico si el modelo no está disponible

### 3. API Endpoint (ya existente)
✅ Endpoint: `POST /api/ml/recomendar-persona`
✅ Acepta los nuevos campos del formulario

## 🧪 Cómo Probar

### 1. Copiar archivos del modelo
```powershell
# Desde tu carpeta de entrenamiento, copia los archivos
Copy-Item "model_catboost_recommender.pkl" "D:\proyecto-innovacion\backend\ml\models\recommender\"
Copy-Item "columns_recommender.json" "D:\proyecto-innovacion\backend\ml\models\recommender\"
Copy-Item "recommender_metrics.json" "D:\proyecto-innovacion\backend\ml\models\recommender\"
```

### 2. Reiniciar el servidor Flask
```powershell
cd D:\proyecto-innovacion\backend
python app.py
```

Deberías ver en la consola:
```
✓ Modelo CatBoost Recommender cargado: ...
✓ Configuración cargada: ...
   Features: XX
✓ Métricas cargadas
   ROC-AUC: 0.8988
   Accuracy: 0.7965
   Accuracy@1: 0.5248
```

### 3. Probar desde el Frontend
1. Ir a: http://localhost:5173/#/recomendacion
2. Llenar el formulario:
   - Nombre: "Desarrollo API REST"
   - Área: "TI"
   - Tipo de Tarea: "Desarrollo"
   - Complejidad: "Media"
   - Duración: "10"
   - Prioridad: "Alta"
   - Habilidades: "Python, React, SQL"
3. Click en "Recomendar Colaborador"

### 4. Verificar logs del backend
En la terminal de Flask deberías ver:
```
🔍 Evaluando X candidatos...
🔧 Preparando features para: [Nombre Persona]
✓ Features preparados: (1, XX)
✓ Top 5 recomendaciones generadas
```

## 📊 Features que el Modelo Espera

Según `columns_recommender.json`, el modelo usa estas features:

**Categóricas:**
- area
- task_type
- complexity_level
- priority
- person_area

**Numéricas:**
- performance_index
- experience_years
- satisfaction_score
- current_workload
- duration_est
- complexity_numeric
- priority_numeric
- area_match
- workload_capacity
- performance_experience

## ⚠️ Troubleshooting

### Error: "Modelo no encontrado"
→ Verifica que `model_catboost_recommender.pkl` esté en `backend/ml/models/recommender/`

### Error: "KeyError" en features
→ Verifica que `columns_recommender.json` tenga la estructura correcta

### Predicciones no coherentes
→ Revisa que los mapeos de complejidad/prioridad sean los mismos que en el entrenamiento

### Error: "No se encontraron candidatos"
→ Verifica que haya personas en la BD en el área especificada con `resigned=False`

## 📈 Métricas del Modelo

- **ROC-AUC**: 0.8988 (89.88%) - Excelente capacidad de discriminación
- **Accuracy**: 79.65% - Buena precisión general
- **Precision**: 82.05% - Pocas falsas recomendaciones
- **Recall**: 76.53% - Captura la mayoría de buenas asignaciones
- **Accuracy@1**: 52.48% - La primera recomendación es correcta el 52% del tiempo

## ✅ Próximos Pasos

1. ✅ Copiar archivos del modelo
2. ✅ Reiniciar servidor Flask
3. ✅ Probar desde el frontend
4. 🔄 Integrar los datos reales en `displayRecommendations()` (actualmente usa datos simulados)
5. 🔄 Agregar visualizaciones de métricas en la interfaz de Configuración IA

## 📝 Notas para tu Tesina

Este es un **sistema híbrido**:
- Modelo CatBoost entrenado (80% accuracy, ROC-AUC 0.90)
- Reglas de negocio complementarias
- Fallback heurístico para robustez
- Explicabilidad mediante "reasons" generadas automáticamente

**Justificación académica:**
"Se implementó un sistema de recomendación basado en Machine Learning (CatBoost) 
que combina predicciones probabilísticas con conocimiento del dominio empresarial, 
logrando un balance entre precisión técnica (ROC-AUC 89.88%) y explicabilidad 
para usuarios no técnicos."
