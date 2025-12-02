"""
🎯 CLASIFICADOR BINARIO DE RIESGO DE TAREAS - SIN DATOS DE PERSONA
===================================================================

MODELO PARA PREDICCIÓN EN SISTEMA WEB (antes de asignar personas)

CARACTERÍSTICAS:
✅ Solo usa features de la TAREA (tabla tasks)
✅ NO usa datos de persona ni asignaciones
✅ Sin data leakage - solo info disponible al CREAR la tarea
✅ 2 clases de riesgo: BAJO_RIESGO, ALTO_RIESGO

TARGET (risk_binary):
- 0 (✅ BAJO_RIESGO): Delay <= percentil 70
- 1 (⚠️ ALTO_RIESGO): Delay > percentil 70

Autor: Sistema de Gestión de Tareas
Fecha: 1/12/2025
"""

import os
import json
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    roc_auc_score, roc_curve
)

from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE
import optuna

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

HOST = os.getenv("MYSQL_HOST", "localhost")
DB   = os.getenv("MYSQL_DB", "sb_production")  # Cambiado de "sb" a "sb_production"
USER = os.getenv("MYSQL_USER", "root")
PASS = os.getenv("MYSQL_PASS", "1234")
PORT = int(os.getenv("MYSQL_PORT", "3306"))

ARTIFACTS_DIR = 'artifacts/binary_task_risk'
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

print_section("🎯 CLASIFICADOR BINARIO DE RIESGO - SOLO FEATURES DE TAREA")

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================

print("\n[1/8] Conectando a MySQL y cargando datos de tareas...")

url = URL.create(
    "mysql+pymysql",
    username=USER,
    password=PASS,
    host=HOST,
    port=PORT,
    database=DB,
    query={"charset": "utf8mb4"}
)

engine = create_engine(url, pool_pre_ping=True)

query_tasks = text("""
SELECT 
    t.task_id,
    t.area,
    t.task_type,
    t.complexity_level,
    t.priority,
    t.duration_est,
    t.duration_real,
    t.dependencies,
    (SELECT COUNT(*) FROM assignees a WHERE a.task_id = t.task_id) as assignees_count
FROM tasks t
WHERE t.duration_est IS NOT NULL 
    AND t.duration_real IS NOT NULL
    AND t.complexity_level IS NOT NULL
    AND t.duration_est > 0
""")

df = pd.read_sql(query_tasks, engine)
engine.dispose()

print(f"   ✅ Datos cargados: {len(df):,} tareas")

# ============================================================================
# 2. CREAR TARGET BINARIO
# ============================================================================

print("\n[2/8] Creando variable target binaria...")

# Convertir minutos a días
df['duration_real_days'] = df['duration_real'] / 1440.0
df['duration_est_days'] = df['duration_est'] / 1440.0
df['delay_days'] = df['duration_real_days'] - df['duration_est_days']

# Umbral: percentil 70 (30% ALTO_RIESGO, 70% BAJO_RIESGO)
delay_threshold = df['delay_days'].quantile(0.70)
df['risk_binary'] = (df['delay_days'] > delay_threshold).astype(int)

print(f"   Umbral (percentil 70): {delay_threshold:.2f} días")
print(f"   Distribución del target:")
for risk_val in [0, 1]:
    count = (df['risk_binary'] == risk_val).sum()
    pct = count / len(df) * 100
    label = "BAJO_RIESGO" if risk_val == 0 else "ALTO_RIESGO"
    print(f"     {label}: {count:,} ({pct:.1f}%)")

# ============================================================================
# 3. INGENIERÍA DE FEATURES
# ============================================================================

print("\n[3/8] Generando features...")

# Features categóricas base
categorical_features = ['area', 'task_type', 'complexity_level', 'priority']

# Features numéricas base
df['assignees_count'] = df['assignees_count'].fillna(1).astype(int)
df['dependencies'] = df['dependencies'].fillna(0).astype(int)

# Features derivadas simples
df['complexity_numeric'] = df['complexity_level'].map({'Low': 1, 'Medium': 2, 'High': 3}).fillna(2)
df['priority_numeric'] = df['priority'].map({'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}).fillna(2)
df['workload_per_person'] = df['duration_est_days'] / (df['assignees_count'] + 0.1)
df['dependency_ratio'] = df['dependencies'] / (df['duration_est_days'] + 0.1)
df['complexity_priority'] = df['complexity_numeric'] * df['priority_numeric']
df['duration_est_squared'] = df['duration_est_days'] ** 2
df['duration_est_log'] = np.log1p(df['duration_est_days'])
df['has_dependencies'] = (df['dependencies'] > 0).astype(int)
df['is_single_person'] = (df['assignees_count'] == 1).astype(int)
df['is_high_complexity'] = (df['complexity_level'] == 'High').astype(int)
df['is_critical_priority'] = (df['priority'] == 'Critical').astype(int)

# Estadísticas agregadas por área
area_stats = df.groupby('area')['delay_days'].agg(['mean', 'std', 'median']).reset_index()
area_stats.columns = ['area', 'area_avg_delay', 'area_std_delay', 'area_median_delay']
area_stats['area_std_delay'].fillna(0, inplace=True)
df = df.merge(area_stats, on='area', how='left')

# Estadísticas agregadas por tipo
type_stats = df.groupby('task_type')['delay_days'].agg(['mean', 'std']).reset_index()
type_stats.columns = ['task_type', 'type_avg_delay', 'type_std_delay']
type_stats['type_std_delay'].fillna(0, inplace=True)
df = df.merge(type_stats, on='task_type', how='left')

# Estadísticas agregadas por complejidad
complexity_stats = df.groupby('complexity_level')['delay_days'].agg(['mean', 'std']).reset_index()
complexity_stats.columns = ['complexity_level', 'complexity_avg_delay', 'complexity_std_delay']
complexity_stats['complexity_std_delay'].fillna(0, inplace=True)
df = df.merge(complexity_stats, on='complexity_level', how='left')

# Features numéricas finales
numeric_features = [
    'duration_est_days',
    'assignees_count',
    'dependencies',
    'complexity_numeric',
    'priority_numeric',
    'workload_per_person',
    'dependency_ratio',
    'complexity_priority',
    'duration_est_squared',
    'duration_est_log',
    'has_dependencies',
    'is_single_person',
    'is_high_complexity',
    'is_critical_priority',
    'area_avg_delay',
    'area_std_delay',
    'area_median_delay',
    'type_avg_delay',
    'type_std_delay',
    'complexity_avg_delay',
    'complexity_std_delay'
]

# Rellenar cualquier NaN residual
for col in numeric_features:
    df[col].fillna(df[col].median(), inplace=True)

print(f"   ✅ Features generadas:")
print(f"      Categóricas: {len(categorical_features)}")
print(f"      Numéricas: {len(numeric_features)}")
print(f"      Total: {len(categorical_features) + len(numeric_features)}")

# ============================================================================
# 4. PREPARAR DATOS
# ============================================================================

print("\n[4/8] Preparando conjuntos de entrenamiento y prueba...")

X = df[categorical_features + numeric_features].copy()
y = df['risk_binary'].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Train: {len(X_train):,} | Test: {len(X_test):,}")
print(f"   Distribución train original:")
for risk_val in [0, 1]:
    count = (y_train == risk_val).sum()
    pct = count / len(y_train) * 100
    label = "BAJO_RIESGO" if risk_val == 0 else "ALTO_RIESGO"
    print(f"     {label}: {count:,} ({pct:.1f}%)")

# ============================================================================
# 5. APLICAR SMOTE
# ============================================================================

print("\n[5/8] Aplicando SMOTE para balancear clases...")

# Codificar categóricas con LabelEncoder
label_encoders = {}
X_train_encoded = X_train.copy()

for col in categorical_features:
    le = LabelEncoder()
    X_train_encoded[col] = le.fit_transform(X_train[col].astype(str))
    label_encoders[col] = le

# Aplicar SMOTE
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_encoded, y_train)

# Convertir a DataFrame
X_train_balanced = pd.DataFrame(X_train_balanced, columns=categorical_features + numeric_features)

# Decodificar categóricas
for col in categorical_features:
    # Redondear y asegurar rango válido
    X_train_balanced[col] = X_train_balanced[col].round().astype(int)
    n_classes = len(label_encoders[col].classes_)
    X_train_balanced[col] = X_train_balanced[col].clip(lower=0, upper=n_classes-1)
    # Decodificar
    X_train_balanced[col] = label_encoders[col].inverse_transform(X_train_balanced[col])
    
y_train_balanced = pd.Series(y_train_balanced, dtype=int)

print(f"   ✅ SMOTE aplicado:")
for risk_val in [0, 1]:
    count = (y_train_balanced == risk_val).sum()
    pct = count / len(y_train_balanced) * 100
    label = "BAJO_RIESGO" if risk_val == 0 else "ALTO_RIESGO"
    print(f"     {label}: {count:,} ({pct:.1f}%)")

# ============================================================================
# 6. OPTIMIZACIÓN CON OPTUNA
# ============================================================================

print("\n[6/8] Optimizando hiperparámetros con Optuna (10 trials)...")

def objective(trial):
    params = {
        'iterations': trial.suggest_int('iterations', 500, 1500),
        'depth': trial.suggest_int('depth', 4, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
        'border_count': trial.suggest_int('border_count', 32, 255),
        'random_strength': trial.suggest_float('random_strength', 0, 10),
        'bagging_temperature': trial.suggest_float('bagging_temperature', 0, 1),
        'loss_function': 'Logloss',
        'eval_metric': 'AUC',
        'random_seed': 42,
        'verbose': False,
        'cat_features': list(range(len(categorical_features)))
    }
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = []
    
    for train_idx, val_idx in cv.split(X_train_balanced, y_train_balanced):
        X_cv_train = X_train_balanced.iloc[train_idx]
        y_cv_train = y_train_balanced.iloc[train_idx]
        X_cv_val = X_train_balanced.iloc[val_idx]
        y_cv_val = y_train_balanced.iloc[val_idx]
        
        model = CatBoostClassifier(**params)
        model.fit(X_cv_train, y_cv_train, verbose=False)
        
        y_pred_proba = model.predict_proba(X_cv_val)[:, 1]
        score = roc_auc_score(y_cv_val, y_pred_proba)
        scores.append(score)
    
    return np.mean(scores)

study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=42))
study.optimize(objective, n_trials=10, show_progress_bar=True)

print(f"\n   ✅ Optimización completada")
print(f"   Mejor AUC (CV): {study.best_value:.4f}")
print(f"   Mejores parámetros:")
for key, value in study.best_params.items():
    print(f"     {key}: {value}")

# ============================================================================
# 7. ENTRENAR MODELO FINAL
# ============================================================================

print("\n[7/8] Entrenando modelo final...")

best_params = study.best_params.copy()
best_params['loss_function'] = 'Logloss'
best_params['eval_metric'] = 'AUC'
best_params['random_seed'] = 42
best_params['verbose'] = False
best_params['cat_features'] = list(range(len(categorical_features)))

model = CatBoostClassifier(**best_params)
model.fit(X_train_balanced, y_train_balanced, verbose=100)

print("\n   ✅ Modelo entrenado")

# ============================================================================
# 8. EVALUACIÓN
# ============================================================================

print("\n[8/8] Evaluando modelo...")

# Limpiar X_test de NaN en categóricas
for col in categorical_features:
    if X_test[col].isna().any():
        # Usar moda del train, o el primer valor no-nulo
        mode_series = X_train[col].mode()
        if len(mode_series) > 0:
            mode_val = mode_series[0]
        else:
            mode_val = X_train[col].dropna().iloc[0] if len(X_train[col].dropna()) > 0 else "Unknown"
        X_test[col] = X_test[col].fillna(mode_val)

y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print_section("RESULTADOS FINALES - MODELO BINARIO")
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"ROC-AUC: {auc:.4f}")
print(f"\nReporte de clasificación:")
print(classification_report(y_test, y_pred, target_names=['BAJO_RIESGO', 'ALTO_RIESGO'], digits=4))

cm = confusion_matrix(y_test, y_pred)
print("\nMatriz de confusión:")
print(cm)
print(f"\nInterpretación:")
print(f"  VN (BAJO correctos): {cm[0,0]}")
print(f"  FP (Falsos ALTO): {cm[0,1]}")
print(f"  FN (Falsos BAJO): {cm[1,0]}")
print(f"  VP (ALTO correctos): {cm[1,1]}")

# ============================================================================
# 9. GUARDAR ARTEFACTOS
# ============================================================================

print("\n[9/9] Guardando modelo y artefactos...")

# Modelo
model_path = os.path.join(ARTIFACTS_DIR, 'model_binary_task_risk.cbm')
model.save_model(model_path)
print(f"   ✅ Modelo: {model_path}")

# Columnas
columns_info = {
    'categorical': categorical_features,
    'numeric': numeric_features,
    'all_columns': categorical_features + numeric_features,
    'threshold_percentile': 70,
    'threshold_value': float(delay_threshold)
}
columns_path = os.path.join(ARTIFACTS_DIR, 'columns_binary.json')
with open(columns_path, 'w') as f:
    json.dump(columns_info, f, indent=2)
print(f"   ✅ Columnas: {columns_path}")

# Métricas
metrics = {
    'accuracy': float(accuracy),
    'roc_auc': float(auc),
    'classification_report': classification_report(y_test, y_pred, target_names=['BAJO_RIESGO', 'ALTO_RIESGO'], output_dict=True),
    'confusion_matrix': cm.tolist(),
    'best_params': study.best_params,
    'n_features': len(categorical_features) + len(numeric_features),
    'n_train': len(X_train_balanced),
    'n_test': len(X_test)
}
metrics_path = os.path.join(ARTIFACTS_DIR, 'metrics_binary.json')
with open(metrics_path, 'w') as f:
    json.dump(metrics, f, indent=2)
print(f"   ✅ Métricas: {metrics_path}")

# ============================================================================
# 10. VISUALIZACIONES
# ============================================================================

print("\n[10/10] Generando visualizaciones...")

# Matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['BAJO_RIESGO', 'ALTO_RIESGO'],
            yticklabels=['BAJO_RIESGO', 'ALTO_RIESGO'])
plt.title('Matriz de Confusión - Modelo Binario')
plt.ylabel('Real')
plt.xlabel('Predicción')
cm_path = os.path.join(ARTIFACTS_DIR, 'confusion_matrix.png')
plt.savefig(cm_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"   ✅ Matriz: {cm_path}")

# Curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC (AUC = {auc:.4f})')
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Azar')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tasa de Falsos Positivos')
plt.ylabel('Tasa de Verdaderos Positivos')
plt.title('Curva ROC - Modelo Binario')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
roc_path = os.path.join(ARTIFACTS_DIR, 'roc_curve.png')
plt.savefig(roc_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"   ✅ ROC: {roc_path}")

# Feature importance
feature_importance = model.get_feature_importance()
feature_names = categorical_features + numeric_features
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

plt.figure(figsize=(10, 12))
top_n = 20
sns.barplot(data=importance_df.head(top_n), y='feature', x='importance', palette='viridis')
plt.title(f'Top {top_n} Features Más Importantes')
plt.xlabel('Importancia')
plt.ylabel('Feature')
plt.tight_layout()
importance_path = os.path.join(ARTIFACTS_DIR, 'feature_importance.png')
plt.savefig(importance_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"   ✅ Importancia: {importance_path}")

importance_df.to_csv(os.path.join(ARTIFACTS_DIR, 'feature_importance.csv'), index=False)

print_section("✅ ENTRENAMIENTO COMPLETADO")
print(f"Modelo: BAJO_RIESGO vs ALTO_RIESGO")
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"ROC-AUC: {auc:.4f}")
print(f"Umbral: {delay_threshold:.2f} días (percentil 70)")
print(f"Artefactos: {ARTIFACTS_DIR}")
print("="*70)
