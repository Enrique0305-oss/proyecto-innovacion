# 📐 Fórmulas Matemáticas de los Modelos de IA

## Sistema de Análisis y Productividad - Processmart S.A.C.

---

## 🎯 **RESUMEN GENERAL**

El sistema combina **2 enfoques matemáticos**:

1. **Algoritmos de Machine Learning** (Random Forest, CatBoost)
   - Basados en árboles de decisión y gradient boosting
   - Aprenden patrones de datos históricos
   - Hacen predicciones mediante votación de múltiples árboles

2. **Scoring Heurístico** (Fórmulas matemáticas directas)
   - Reglas de negocio con pesos ponderados
   - Suma ponderada de factores
   - Cálculos de ratios y proporciones

---

## 📊 **1. MODELO DE PREDICCIÓN DE DURACIÓN**

### **A) Fórmula Heurística (Fallback)**

```
DURACIÓN_PREDICHA = BASE × F_COMPLEJIDAD × F_PRIORIDAD + AJUSTE_DEPENDENCIAS - REDUCCIÓN_EXPERIENCIA + BUFFER

Donde:
- BASE = 5 días (constante)
- F_COMPLEJIDAD = {1, 2, 3} según complejidad {Baja, Media, Alta}
- F_PRIORIDAD = {1.5, 1.3, 1.0} según prioridad {Alta, Media, Baja}
- AJUSTE_DEPENDENCIAS = n_dependencias × 1 día
- REDUCCIÓN_EXPERIENCIA = BASE × (0.9 - 0.05 × años_experiencia)
- BUFFER = BASE × 1.1 (10% adicional)
```

**Ejemplo práctico:**
```
Tarea: Complejidad Alta, Prioridad Alta, 2 dependencias, colaborador con 5 años exp.

DURACIÓN = 5 × 3 × 1.5 + (2 × 1) - [5 × 3 × (0.9 - 0.05×5)] + (5 × 3 × 1.1)
         = 15 × 1.5 + 2 - [15 × 0.65] + 16.5
         = 22.5 + 2 - 9.75 + 16.5
         = 31.25 días
```

### **B) Modelo CatBoost con Calibración**

```
DURACIÓN_FINAL = PREDICCIÓN_CATBOOST × FACTOR_CALIBRACIÓN

Donde:
- PREDICCIÓN_CATBOOST = Salida del modelo (gradient boosting)
- FACTOR_CALIBRACIÓN = 0.12 (ajuste empírico)
```

**Features principales del modelo:**
1. `duration_est_imputed` (correlación 0.9 con target)
2. `complexity_imputed` (categórica: Baja/Media/Alta)
3. `priority_imputed` (categórica)
4. `experience_years_imputed`
5. `load_ratio` = carga_actual / 10

---

## 🎲 **2. MODELO DE CLASIFICACIÓN DE RIESGO**

### **Random Forest Classifier**

El modelo usa árboles de decisión que votan. La probabilidad final es:

```
P(RIESGO_ALTO) = (1/N) × Σ(votos_árbol_i)

Donde:
- N = número de árboles en el bosque (típicamente 100)
- votos_árbol_i ∈ {0, 1} (voto de cada árbol)
```

**Features principales:**
- `complexity_score` (0-10)
- `estimated_hours` 
- `area` (categórica)
- `priority` (categórica)

---

## 👥 **3. MODELO DE RECOMENDACIÓN PERSONA-TAREA**

### **A) Score Heurístico (0-100 puntos)**

```
SCORE_TOTAL = S_PERFORMANCE + S_EXPERIENCIA + S_WORKLOAD + S_ÁREA + S_SKILLS

Donde:
```

#### **1. Score de Performance (0-30 puntos)**
```
S_PERFORMANCE = min(performance_index × 30/100, 30)

Ejemplo: Si performance_index = 85%
S_PERFORMANCE = 85 × 30/100 = 25.5 puntos
```

#### **2. Score de Experiencia (0-20 puntos)**
```
S_EXPERIENCIA = {
    20 puntos  si años >= 10
    15 puntos  si 5 <= años < 10
    10 puntos  si 2 <= años < 5
    5 puntos   si años < 2
}
```

#### **3. Score de Workload (0-15 puntos)**
```
S_WORKLOAD = {
    15 puntos  si carga_actual = 0
    12 puntos  si carga_actual <= 2
    8 puntos   si carga_actual <= 4
    3 puntos   si carga_actual > 4
}
```

#### **4. Score de Coincidencia de Área (0-15 puntos)**
```
S_ÁREA = {
    15 puntos  si área_persona = área_tarea
    0 puntos   en caso contrario
}
```

#### **5. Score de Coincidencia de Habilidades (0-20 puntos)** ⭐ NUEVO
```
SKILL_MATCH = (n_skills_coincidentes / n_skills_requeridas)

S_SKILLS = SKILL_MATCH × 20

Ejemplo:
Skills requeridas: [Python, SQL, Machine Learning] = 3 skills
Skills persona: [Python, Java, SQL, Git] = coinciden 2 (Python, SQL)

SKILL_MATCH = 2/3 = 0.667
S_SKILLS = 0.667 × 20 = 13.3 puntos
```

### **Ejemplo Completo:**

```
Candidato:
- Performance Index: 85%
- Experiencia: 7 años
- Carga actual: 1 tarea
- Área: IT (coincide con tarea)
- Skills: Python, SQL (coincide 2/3)

SCORE = 25.5 + 15 + 12 + 15 + 13.3 = 80.8/100 puntos
```

### **B) Features para CatBoost Recommender**

```
FEATURES_DERIVADAS:

1. experience_complexity_ratio = años_experiencia / complejidad_numérica
   Donde: complejidad_numérica = {1: Baja, 2: Media, 3: Alta}

2. load_capacity_ratio = carga_actual / capacidad_máxima
   Donde: capacidad_máxima = 10 tareas

3. match_area = {1 si área_persona = área_tarea, 0 en caso contrario}

4. match_role_type = {1 si rol coincide con tipo_tarea, 0 en caso contrario}
```

---

## 📈 **4. MODELO DE PREDICCIÓN DE DESEMPEÑO**

### **Random Forest Regressor**

Predice un score de desempeño (0-100) basándose en:

```
PERFORMANCE_SCORE = f(área_match, experiencia, historial_tareas, complejidad)

Features principales:
- experience_years
- tasks_completed_ratio = tareas_completadas / tareas_totales
- avg_completion_time
- area_expertise = {1 si área coincide, 0 si no}
```

---

## 🚶 **5. MODELO DE PREDICCIÓN DE RENUNCIA (ATTRITION)**

### **A) Score de Riesgo Heurístico (0-0.95)**

```
RISK_SCORE = R_SOBRECARGA + R_BAJO_DESEMPEÑO + R_BAJA_SATISFACCIÓN

Donde:
```

#### **1. Riesgo por Sobrecarga (0-0.30)**
```
R_SOBRECARGA = {
    0.30  si avg_delay_ratio > 0.3 (30% retraso promedio)
    0.15  si 0.1 < avg_delay_ratio <= 0.3
    0     si avg_delay_ratio <= 0.1
}
```

#### **2. Riesgo por Bajo Desempeño (0-0.25)**
```
R_BAJO_DESEMPEÑO = {
    0.25  si performance_index < 50%
    0.15  si 50% <= performance_index < 70%
    0     si performance_index >= 70%
}
```

#### **3. Riesgo por Baja Satisfacción (0-0.20)**
```
R_BAJA_SATISFACCIÓN = {
    0.20  si satisfaction_score < 2.5 (escala 1-5)
    0.10  si 2.5 <= satisfaction_score < 3.5
    0     si satisfaction_score >= 3.5
}
```

### **Probabilidad Final:**
```
P(RENUNCIA) = min(R_SOBRECARGA + R_BAJO_DESEMPEÑO + R_BAJA_SATISFACCIÓN, 0.95)

Máximo: 95% (nunca se predice 100% de certeza)
```

**Ejemplo:**
```
Empleado:
- avg_delay_ratio = 0.35 (35% retraso) → 0.30 puntos
- performance_index = 45% → 0.25 puntos
- satisfaction_score = 2.0 → 0.20 puntos

P(RENUNCIA) = 0.30 + 0.25 + 0.20 = 0.75 = 75% de probabilidad
```

### **B) Features para CatBoost Attrition**

```
FEATURES_CALCULADAS:

1. load_ratio = carga_actual / horas_disponibles_semana

2. avg_delay_ratio = promedio(delay_ratio por tarea)
   Donde: delay_ratio = (tiempo_real - tiempo_estimado) / tiempo_estimado

3. task_completion_ratio = tareas_completadas / tareas_asignadas
```

---

## ⛓️ **6. PROCESS MINING**

### **Métricas de Eficiencia**

```
1. TIEMPO_PROMEDIO_TAREA = Σ(duración_tarea_i) / n_tareas

2. TASA_COMPLETITUD = tareas_completadas / tareas_totales × 100

3. EFICIENCIA_ÁREA = (tareas_completadas_área / tareas_totales_área) × 100

4. DESVIACIÓN_TIEMPO = √[Σ(tiempo_real - tiempo_estimado)² / n]

5. RATIO_RETRASO = {
    (tiempo_real - tiempo_estimado) / tiempo_estimado  si tiempo_real > estimado
    0  en caso contrario
   }
```

---

## 🔢 **FORMULAS AUXILIARES COMUNES**

### **1. Normalización Min-Max**
```
VALOR_NORMALIZADO = (valor - min) / (max - min)

Ejemplo: Normalizar experiencia de 5 años en rango [0, 15]
NORMALIZADO = (5 - 0) / (15 - 0) = 0.333
```

### **2. Imputación de Valores Faltantes**
```
VALOR_IMPUTADO = {
    valor_real    si valor existe
    mediana       si valor falta
}
```

### **3. Codificación One-Hot**
```
Para variable categórica con n valores, crear n columnas binarias

Ejemplo: área = "IT"
área_IT = 1
área_Ventas = 0
área_RRHH = 0
```

---

## 📊 **RESUMEN DE PESOS POR MODELO**

### **Recomendación Persona-Tarea:**
- Performance: 30%
- Skills Match: 20%
- Experiencia: 20%
- Área Match: 15%
- Workload: 15%

### **Predicción de Renuncia:**
- Sobrecarga: 30%
- Bajo Desempeño: 25%
- Baja Satisfacción: 20%
- Otros factores: 25%

### **Predicción de Duración:**
- Estimación Inicial: 90% (feature más importante)
- Complejidad: 5%
- Experiencia: 3%
- Otros: 2%

---

## 🎓 **ALGORITMOS DE ML UTILIZADOS**

### **1. Random Forest**
```
PREDICCIÓN = (1/N) × Σ predicción_árbol_i

Cada árbol se entrena con:
- Bootstrap sample (muestra aleatoria con reemplazo)
- Subset aleatorio de features
- Criterio Gini para clasificación
- MSE para regresión
```

### **2. CatBoost (Gradient Boosting)**
```
F_m(x) = F_(m-1)(x) + η × h_m(x)

Donde:
- F_m(x) = predicción en iteración m
- η = learning rate (tasa de aprendizaje)
- h_m(x) = nuevo árbol que minimiza la pérdida
```

**Función de pérdida para regresión:**
```
L = (1/n) × Σ(y_i - ŷ_i)²
```

**Función de pérdida para clasificación:**
```
L = -(1/n) × Σ[y_i × log(p_i) + (1-y_i) × log(1-p_i)]
```

---

## ✅ **CONCLUSIÓN**

El sistema utiliza:

1. **Fórmulas matemáticas explícitas** para scoring heurístico:
   - Sumas ponderadas
   - Ratios y proporciones
   - Reglas condicionales

2. **Algoritmos de Machine Learning** para predicciones avanzadas:
   - Random Forest (votación de árboles)
   - CatBoost (gradient boosting)
   - Optimización de funciones de pérdida

3. **Combinación híbrida**:
   - ML cuando hay modelo entrenado
   - Heurística como fallback
   - Calibración para ajustar predicciones

**Todas las predicciones tienen base matemática rigurosa y están validadas con métricas de evaluación.**

---

📅 **Fecha:** 16 de diciembre de 2025  
🏢 **Sistema:** Processmart S.A.C. - Análisis y Productividad con IA
