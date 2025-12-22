# 📍 Ubicación de Fórmulas Matemáticas en Archivos de Entrenamiento

## Directorio: `backend/ml/models/training/`

---

## 📄 **1. train_binary_task_risk.py** (Clasificación de Riesgo)

### **Fórmulas de Conversión (Líneas 113-115)**
```python
# LÍNEA 113: Convertir minutos a días
df['duration_real_days'] = df['duration_real'] / 1440.0

# LÍNEA 114: Convertir estimación a días  
df['duration_est_days'] = df['duration_est'] / 1440.0

# LÍNEA 115: Calcular retraso en días
df['delay_days'] = df['duration_real_days'] - df['duration_est_days']
```
**Fórmula:** `delay = duración_real - duración_estimada`

---

### **Creación de Target Binario (Línea 118)**
```python
# LÍNEA 118: Clasificar riesgo según percentil 70
delay_threshold = df['delay_days'].quantile(0.70)
df['risk_binary'] = (df['delay_days'] > delay_threshold).astype(int)
```
**Fórmula:** 
```
risk_binary = {
    1 (ALTO RIESGO)  si delay > percentil_70
    0 (BAJO RIESGO)  si delay ≤ percentil_70
}
```

---

### **Features Numéricas Derivadas (Líneas 143-150)**
```python
# LÍNEA 143: Mapeo de complejidad a números
df['complexity_numeric'] = df['complexity_level'].map({
    'Low': 1, 'Medium': 2, 'High': 3
}).fillna(2)

# LÍNEA 144: Mapeo de prioridad a números
df['priority_numeric'] = df['priority'].map({
    'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4
}).fillna(2)

# LÍNEA 145: Carga de trabajo por persona
df['workload_per_person'] = df['duration_est_days'] / (df['assignees_count'] + 0.1)

# LÍNEA 146: Ratio de dependencias
df['dependency_ratio'] = df['dependencies'] / (df['duration_est_days'] + 0.1)

# LÍNEA 147: Interacción complejidad × prioridad
df['complexity_priority'] = df['complexity_numeric'] * df['priority_numeric']

# LÍNEA 148: Duración al cuadrado
df['duration_est_squared'] = df['duration_est_days'] ** 2

# LÍNEA 149: Logaritmo de duración
df['duration_est_log'] = np.log1p(df['duration_est_days'])

# LÍNEA 150: Indicador binario de dependencias
df['has_dependencies'] = (df['dependencies'] > 0).astype(int)
```

**Fórmulas aplicadas:**
1. `workload_per_person = duración / (n_personas + 0.1)`
2. `dependency_ratio = n_dependencias / (duración + 0.1)`
3. `complexity_priority = complejidad × prioridad`
4. `duration_squared = duración²`
5. `duration_log = log(1 + duración)`

---

## 📄 **2. train_catboost_recommender.py** (Recomendación Persona-Tarea)

### **Target Binario (Líneas 220-228)**
```python
# LÍNEA 220-228: Calcular si la tarea se completó a tiempo
CASE 
    WHEN t.duration_real IS NULL OR t.duration_est IS NULL THEN NULL
    -- Tolerancia de +10%
    WHEN t.duration_real <= 1.1 * t.duration_est THEN 1  -- Éxito
    ELSE 0  -- Fracaso
END AS completed_on_time_alt
```
**Fórmula:** 
```
completed_on_time = {
    1  si duration_real ≤ 1.1 × duration_est
    0  en caso contrario
}
```

---

### **Feature Engineering (Líneas 313-329)**
```python
# LÍNEA 308: Match de área (binario)
df['match_area'] = (df['task_area'] == df['person_area']).astype(float)

# LÍNEA 313-320: Ratio experiencia / complejidad
complexity_map = {'Low': 1, 'Medium': 2, 'High': 3}
df['complexity_numeric'] = df['complexity_level'].map(complexity_map).fillna(2)

df['experience_complexity_ratio'] = (
    df['experience_years_imputed'] / df['complexity_numeric'].clip(lower=1)
)

# LÍNEA 323-327: Ratio carga / capacidad
max_capacity = 10.0
df['load_capacity_ratio'] = (
    df['current_load_imputed'] / max_capacity
)

# LÍNEA 329: Limitar ratio entre 0 y 2
df['load_capacity_ratio'] = df['load_capacity_ratio'].clip(0, 2)
```

**Fórmulas aplicadas:**
1. `match_area = 1 si área_tarea = área_persona, 0 si no`
2. `experience_complexity_ratio = años_experiencia / complejidad_numérica`
3. `load_capacity_ratio = carga_actual / 10.0`
4. `ratio_limitado = min(max(ratio, 0), 2)`

---

## 📄 **3. train_catboost_regressor_numeric_only.py** (Predicción Duración)

### **Conversión de Unidades (Líneas 326-327)**
```python
# LÍNEA 326: Convertir target de minutos a días
df[target_col] = df[target_col] / (60 * 24)

# LÍNEA 327: Convertir estimación a días
df['duration_est_imputed'] = df['duration_est_imputed'] / (60 * 24)
```
**Fórmula:** `días = minutos / (60 × 24)`

---

### **Normalización de Complejidad (Líneas 390-397)**
```python
# LÍNEA 390: Mapeo de complejidad categórica
complexity_map = {'Low': 1, 'Medium': 2, 'High': 3}
df['complexity_numeric'] = df['complexity_level'].map(complexity_map)

# LÍNEA 393-397: Normalización min-max a rango [1, 3]
if df['complexity_numeric'].max() > 10:
    min_val = df['complexity_numeric'].min()
    max_val = df['complexity_numeric'].max()
    df['complexity_numeric'] = 1 + 2 * (df['complexity_numeric'] - min_val) / (max_val - min_val)
```
**Fórmula Min-Max:**
```
valor_normalizado = min_nuevo + rango_nuevo × (valor - min_original) / (max_original - min_original)
                  = 1 + 2 × (valor - min) / (max - min)
```

---

### **Métricas de Evaluación (Líneas 112, 138)**
```python
# LÍNEA 112: RMSE (Root Mean Squared Error)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

# LÍNEA 138: RMSE en Bootstrap
rmse_bootstrap.append(np.sqrt(mean_squared_error(y_true[indices], y_pred[indices])))
```
**Fórmula RMSE:**
```
RMSE = √[(1/n) × Σ(y_real - y_predicho)²]
```

---

## 📄 **4. train_performance_predictor_fixed.py** (Predicción de Desempeño)

### **Cálculo de Métricas de Persona (líneas típicas)**
```python
# Ratio de tareas completadas
completion_ratio = tareas_completadas / tareas_totales

# Promedio de retraso
avg_delay_ratio = promedio(delay_ratio por tarea)
    donde: delay_ratio = (tiempo_real - tiempo_estimado) / tiempo_estimado

# Load ratio
load_ratio = carga_actual / horas_disponibles_semana
```

---

## 📄 **5. train_process_mining.py** (Análisis de Procesos)

### **Métricas de Proceso**
```python
# Tiempo promedio por tarea
avg_duration = Σ(duraciones) / n_tareas

# Tasa de completitud
completion_rate = tareas_completadas / tareas_totales × 100

# Desviación estándar de tiempos
std_deviation = √[Σ(duración - promedio)² / n]

# Ratio de eficiencia
efficiency_ratio = tiempo_estimado_total / tiempo_real_total
```

---

## 🎯 **RESUMEN DE FÓRMULAS CLAVE POR ARCHIVO**

### **train_binary_task_risk.py:**
- ✅ `delay = real - estimado`
- ✅ `workload_per_person = duración / n_personas`
- ✅ `dependency_ratio = dependencias / duración`
- ✅ `complexity_priority = complejidad × prioridad`
- ✅ `log_transform = log(1 + x)`

### **train_catboost_recommender.py:**
- ✅ `completed_on_time = real ≤ 1.1 × estimado`
- ✅ `experience_complexity_ratio = experiencia / complejidad`
- ✅ `load_capacity_ratio = carga / 10`
- ✅ `match_area = área_persona = área_tarea`

### **train_catboost_regressor_numeric_only.py:**
- ✅ `días = minutos / 1440`
- ✅ `normalización = 1 + 2 × (x - min) / (max - min)`
- ✅ `RMSE = √(MSE)`

### **Métricas Comunes:**
- ✅ `delay_ratio = (real - estimado) / estimado`
- ✅ `completion_ratio = completadas / totales`
- ✅ `load_ratio = carga / capacidad`

---

## 📚 **DOCUMENTOS RELACIONADOS**

1. **FORMULAS_MATEMATICAS_MODELOS.md** - Explicación detallada de todas las fórmulas
2. **Archivos de entrenamiento** - Implementación real de las fórmulas
3. **Modelos ML** en `backend/app/ml/` - Uso de las fórmulas en producción

---

📅 **Fecha:** 16 de diciembre de 2025  
🏢 **Sistema:** Processmart S.A.C. - Training Scripts  
📍 **Ubicación:** `backend/ml/models/training/`
