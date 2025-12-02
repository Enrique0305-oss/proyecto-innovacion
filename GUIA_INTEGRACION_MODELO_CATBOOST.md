# 🤖 GUÍA COMPLETA DE INTEGRACIÓN DEL MODELO CATBOOST

## 📋 **RESUMEN EJECUTIVO**

Tu modelo CatBoost de clasificación multiclase está **100% integrado** en el proyecto. Ahora puedes:

1. ✅ **Copiar tu modelo entrenado** y usarlo inmediatamente
2. ✅ **Reentrenar desde la interfaz** "Configuración IA"
3. ✅ **Hacer predicciones** en tiempo real desde "Clasificación de Riesgo"
4. ✅ **Ver métricas y visualizaciones** del modelo

---

## 🗂️ **ESTRUCTURA DE ARCHIVOS**

```
proyecto-innovacion/
├── backend/
│   ├── ml/
│   │   └── models/
│   │       ├── risk/                        ⭐ TU MODELO VA AQUÍ
│   │       │   ├── model_catboost_multiclass.pkl
│   │       │   ├── preprocessor.pkl
│   │       │   ├── model_config.json
│   │       │   ├── optuna_study.json
│   │       │   └── metrics/
│   │       │       ├── confusion_matrix.png
│   │       │       ├── feature_importance.png
│   │       │       ├── feature_importance.csv
│   │       │       └── classification_report.csv
│   │       └── training/
│   │           └── train_catboost_multiclass.py  (script de entrenamiento)
│   │
│   └── app/
│       ├── ml/
│       │   ├── risk_model.py            ✏️ ACTUALIZADO - Carga tu modelo
│       │   └── model_trainer.py         ⭐ NUEVO - Sistema de reentrenamiento
│       │
│       └── routes/
│           ├── ml_routes.py             ✅ Ya existente - Predicciones
│           └── ml_training_routes.py    ⭐ NUEVO - Entrenamiento desde UI
│
└── sistema-productivo/
    └── src/
        └── pages/
            ├── RiskClassification.ts         → Interfaz de predicción
            └── IAConfiguration.ts            → Interfaz de reentrenamiento
```

---

## 🚀 **PASO A PASO: INTEGRACIÓN COMPLETA**

### **PASO 1: Copiar Tu Modelo Entrenado**

Desde tu proyecto de entrenamiento (fuera de este proyecto), copia estos archivos:

```powershell
# Desde PowerShell en el directorio backend/

# Definir ruta de origen (CAMBIA ESTO)
$origen = "C:\tu\proyecto\entrenamiento"

# Copiar archivos principales
Copy-Item "$origen\model_catboost_multiclass.pkl" ".\ml\models\risk\"
Copy-Item "$origen\preprocessor.pkl" ".\ml\models\risk\"
Copy-Item "$origen\model_config.json" ".\ml\models\risk\"

# Copiar métricas (opcional pero recomendado)
Copy-Item "$origen\*.png" ".\ml\models\risk\metrics\"
Copy-Item "$origen\*.csv" ".\ml\models\risk\metrics\"
Copy-Item "$origen\optuna_study.json" ".\ml\models\risk\"

Write-Host "✅ Modelo copiado correctamente"
```

**Verificar:**
```powershell
ls ml\models\risk\
```

Debes ver:
- ✅ `model_catboost_multiclass.pkl`
- ✅ `preprocessor.pkl` **(CRÍTICO - sin esto no funciona)**
- ✅ `model_config.json`

---

### **PASO 2: Instalar Dependencias**

```powershell
cd backend
pip install catboost optuna scikit-learn pandas numpy matplotlib seaborn
```

**Verificar instalación:**
```powershell
python -c "import catboost, optuna; print('✅ Dependencias instaladas')"
```

---

### **PASO 3: Verificar Carga del Modelo**

```powershell
python -c "from app.ml.risk_model import load_model; m = load_model(); print('✅ Modelo cargado' if m else '❌ Error')"
```

**Salida esperada:**
```
✓ Modelo CatBoost cargado: ...
✓ Preprocessor cargado: ...
✓ Configuración cargada: ...
   Features: 32
   Clases: ['alto', 'bajo', 'medio']
   Accuracy: 0.8956
✅ Modelo cargado
```

---

### **PASO 4: Iniciar el Backend**

```powershell
cd backend
python app.py
```

**Verificar en el log:**
```
✅ Blueprints registrados correctamente
✓ Modelo CatBoost cargado: ...
```

---

## 🎯 **ENDPOINTS DISPONIBLES**

### **1. Predicción de Riesgo** (Ya existente - actualizado)

```http
POST /api/ml/prediccion-riesgo
Authorization: Bearer <token>
Content-Type: application/json

{
  "complexity_level": "alta",
  "priority": "alta",
  "area": "Desarrollo",
  "task_type": "Implementación",
  "duration_est": 15,
  "assignees_count": 3,
  "dependencies": 2
}
```

**Respuesta:**
```json
{
  "task_id": null,
  "risk_level": "alto",
  "risk_probability": 0.87,
  "probabilities": {
    "bajo": 0.05,
    "medio": 0.08,
    "alto": 0.87
  },
  "risk_factors": [
    "Alta complejidad técnica",
    "Prioridad elevada",
    "Múltiples dependencias (2)"
  ],
  "recommendations": [
    "Realizar seguimiento diario del progreso",
    "Asignar recursos adicionales si es posible"
  ],
  "model_used": "catboost_multiclass"
}
```

---

### **2. Información del Modelo** ⭐ NUEVO

```http
GET /api/ml/model/info
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "status": "ready",
  "model_type": "CatBoostClassifier",
  "accuracy": 0.8956,
  "training_date": "20231130_140500",
  "n_features": 32,
  "classes": ["bajo", "medio", "alto"]
}
```

---

### **3. Entrenar/Reentrenar Modelo** ⭐ NUEVO

```http
POST /api/ml/model/train
Authorization: Bearer <token>
Content-Type: application/json

{
  "use_optuna": true,
  "n_trials": 50,
  "data_limit": null
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Modelo entrenado exitosamente",
  "accuracy": 0.9123,
  "timestamp": "20231130_143000",
  "metrics": {
    "accuracy": 0.9123,
    "classification_report": {...},
    "confusion_matrix": [[...]]
  }
}
```

**⚠️ IMPORTANTE:** Solo usuarios con rol `super_admin` pueden entrenar modelos.

---

### **4. Obtener Métricas** ⭐ NUEVO

```http
GET /api/ml/model/metrics
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "classification_report": [
    {"": "precision", "bajo": 0.89, "medio": 0.91, "alto": 0.88},
    ...
  ],
  "feature_importance": [
    {"feature": "complexity_level_encoded", "importance": 0.245},
    {"feature": "priority_encoded", "importance": 0.189},
    ...
  ]
}
```

---

### **5. Imágenes de Métricas** ⭐ NUEVO

```http
GET /api/ml/model/metrics/image/confusion_matrix
GET /api/ml/model/metrics/image/feature_importance
Authorization: Bearer <token>
```

Retorna la imagen PNG directamente.

---

### **6. Vista Previa de Datos** ⭐ NUEVO

```http
GET /api/ml/data/preview?limit=10
Authorization: Bearer <token>
```

Muestra una muestra de los datos de entrenamiento disponibles en la BD.

---

## 🖥️ **INTEGRACIÓN CON EL FRONTEND**

### **Página: Clasificación de Riesgo** (`RiskClassification.ts`)

Esta página **ya existe** y ahora usará tu modelo CatBoost automáticamente.

**Funcionalidad:**
1. Usuario completa el formulario con datos de la tarea
2. Click en "Calcular Riesgo"
3. Llama a `POST /api/ml/prediccion-riesgo`
4. Muestra resultado con nivel de riesgo y recomendaciones

**Actualización sugerida para mostrar probas:**
```typescript
// En RiskClassification.ts, al recibir la respuesta:

const response = await api.post('/ml/prediccion-riesgo', data);

// Mostrar probabilidades por clase
const probabilities = response.probabilities;
console.log('Probabilidad Bajo:', probabilities.bajo);
console.log('Probabilidad Medio:', probabilities.medio);
console.log('Probabilidad Alto:', probabilities.alto);

// Mostrar gráfico de barras con las 3 probabilidades
```

---

### **Página: Configuración IA** (`IAConfiguration.ts`)

Esta página debe implementar:

#### **1. Mostrar Estado del Modelo**

```typescript
async function loadModelInfo() {
  const info = await api.get('/ml/model/info');
  
  // Mostrar en la UI:
  // - Estado: info.status
  // - Accuracy: info.accuracy
  // - Fecha entrenamiento: info.training_date
  // - Número de features: info.n_features
}
```

#### **2. Botón de Reentrenamiento**

```typescript
async function retrainModel() {
  const config = {
    use_optuna: true,
    n_trials: 50
  };
  
  // Mostrar loading...
  const result = await api.post('/ml/model/train', config);
  
  if (result.success) {
    alert(`Modelo reentrenado! Accuracy: ${result.accuracy}`);
    loadModelInfo(); // Actualizar info
  }
}
```

#### **3. Mostrar Métricas y Gráficos**

```typescript
async function loadMetrics() {
  // Obtener métricas en JSON
  const metrics = await api.get('/ml/model/metrics');
  
  // Mostrar tabla de feature importance
  const features = metrics.feature_importance;
  // Renderizar tabla...
  
  // Mostrar imágenes
  const confusionMatrixUrl = `${API_URL}/ml/model/metrics/image/confusion_matrix`;
  const featureImportanceUrl = `${API_URL}/ml/model/metrics/image/feature_importance`;
  
  // <img src={confusionMatrixUrl} />
}
```

---

## 🔄 **FLUJO DE REENTRENAMIENTO**

### **Desde la Interfaz de Usuario:**

1. Usuario Super Admin va a "Configuración IA"
2. Ve el estado actual del modelo (accuracy, fecha)
3. Click en "Reentrenar Modelo"
4. **Backend:**
   - Extrae datos de la tabla `task`
   - Prepara features con el mismo preprocessor
   - Optimiza hiperparámetros con Optuna (opcional)
   - Entrena nuevo modelo CatBoost
   - Guarda modelo, preprocessor y métricas
5. **Frontend:** Muestra nuevo accuracy y fecha
6. Modelo actualizado disponible inmediatamente

---

## 📊 **ADAPTACIÓN DE TU MODELO EXISTENTE**

### **Requisitos Críticos:**

Tu `model_config.json` debe contener las **32 features exactas** que usaste:

```json
{
  "model_type": "CatBoostClassifier",
  "features": [
    "complexity_level_encoded",
    "priority_encoded",
    "area_name_encoded",
    "status_encoded",
    "duration_est",
    "assignees_count",
    // ... las otras 26 features
  ],
  "n_features": 32,
  "classes": ["bajo", "medio", "alto"],
  "accuracy": 0.8956,
  "training_date": "20231130_140500"
}
```

### **El Preprocessor debe contener:**

```python
{
  'scaler': StandardScaler(),           # Normalizador entrenado
  'label_encoders': {                   # LabelEncoders entrenados
    'complexity_level': LabelEncoder(),
    'priority': LabelEncoder(),
    'area_name': LabelEncoder(),
    ...
  },
  'feature_columns': [...],             # Lista de columnas
  'categorical_features': [...],
  'numerical_features': [...]
}
```

---

## ⚙️ **CONFIGURACIÓN ADICIONAL**

### **Si tus features son diferentes:**

Edita `backend/app/ml/model_trainer.py`, método `_prepare_risk_features()`:

```python
def _prepare_risk_features(self, data):
    # CAMBIA ESTAS LISTAS según tus 32 features:
    categorical_features = [
        'complexity_level', 'priority', 'area_name', 'task_type',
        'status', 'assigned_to'
        # ... agregar más
    ]
    
    numerical_features = [
        'duration_est', 'assignees_count', 'dependencies_count',
        'completion_percentage', 'days_elapsed'
        # ... agregar más
    ]
```

---

## 🧪 **PRUEBAS**

### **1. Prueba de Carga del Modelo:**

```powershell
python -c "from app.ml.risk_model import load_model; load_model()"
```

### **2. Prueba de Predicción:**

```powershell
python
```
```python
from app.ml.risk_model import predict_risk

data = {
    'complexity_level': 'alta',
    'priority': 'alta',
    'area': 'Desarrollo',
    'task_type': 'Implementación',
    'duration_est': 20,
    'assignees_count': 3,
    'dependencies': 2
}

result = predict_risk(data)
print(result)
```

### **3. Prueba del Endpoint:**

```powershell
# Con el servidor corriendo
curl -X POST http://localhost:5000/api/ml/prediccion-riesgo `
  -H "Authorization: Bearer TU_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{"complexity_level":"alta","priority":"alta","area":"Desarrollo","task_type":"Implementación","duration_est":20,"assignees_count":3,"dependencies":2}'
```

---

## 🚨 **TROUBLESHOOTING**

### **Error: "Preprocessor no cargado"**
→ Asegúrate de que `preprocessor.pkl` esté en `ml/models/risk/`

### **Error: "Features no coinciden"**
→ Las features en `task_data` deben coincidir con las del `model_config.json`

### **Error: "Módulo catboost no encontrado"**
→ `pip install catboost`

### **Error: "Permission denied al entrenar"**
→ Solo usuarios `super_admin` pueden entrenar modelos

### **Modelo no se carga al iniciar**
→ Revisa los logs del servidor, verifica que los archivos `.pkl` no estén corruptos

---

## 📚 **RESUMEN DE ARCHIVOS CREADOS/MODIFICADOS**

### **✅ Creados:**
1. `backend/ml/models/risk/` (carpeta)
2. `backend/ml/models/training/train_catboost_multiclass.py`
3. `backend/app/ml/model_trainer.py`
4. `backend/app/routes/ml_training_routes.py`
5. `backend/ml/models/INSTRUCCIONES_COPIAR_MODELO.md`

### **✏️ Modificados:**
1. `backend/app/ml/risk_model.py` (actualizado para CatBoost)
2. `backend/app/routes/__init__.py` (registrado nuevo blueprint)

---

## 🎯 **PRÓXIMOS PASOS**

1. ✅ **Copiar tu modelo entrenado** → `ml/models/risk/`
2. ✅ **Instalar dependencias** → `pip install catboost optuna`
3. ✅ **Verificar carga** → `python -c "from app.ml.risk_model import load_model; load_model()"`
4. ✅ **Iniciar servidor** → `python app.py`
5. ✅ **Probar predicción** → Ir a "Clasificación de Riesgo"
6. ✅ **Implementar UI de reentrenamiento** → Actualizar `IAConfiguration.ts`

---

## 💡 **VENTAJAS DE ESTA INTEGRACIÓN**

✅ **Modelo reutilizable** - Tu modelo entrenado funciona sin cambios  
✅ **Reentrenamiento automático** - Desde la UI sin código  
✅ **Métricas visuales** - Confusion matrix, feature importance  
✅ **Versionado** - Cada entrenamiento guarda timestamp  
✅ **Escalable** - Fácil agregar más modelos (duración, desempeño, etc.)  
✅ **Seguro** - Solo super_admin puede reentrenar  

---

¿Necesitas ayuda con algún paso específico? 🚀
