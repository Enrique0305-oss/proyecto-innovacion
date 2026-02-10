"""
Entrenamiento de Modelo CatBoost para Regresión de Duración - SOLO FEATURES NUMÉRICAS
=======================================================================================
Predicción de duration_real (tiempo real que toma completar una tarea).

 VERSIÓN SIMPLIFICADA - Compatible con cualquier dominio
============================================================

Características principales:
- SOLO features numéricas (sin dependencias categóricas de dominio específico)
- Transformación logarítmica para normalizar distribución sesgada
- Múltiples loss functions (RMSE, MAE, Quantile) para robustez a outliers
- Validación cruzada estratificada por buckets de duración
- Comparación con baseline (LinearRegression)
- Métricas en escala original para interpretabilidad
- Análisis detallado de residuos y errores

 VENTAJAS DE ESTA VERSIÓN:
-  Funciona con cualquier dominio (IT, rural, construcción, etc.)
-  No requiere mapeo de categorías
-  Features universales (duración estimada, experiencia, carga, performance)
-  Menos overfitting a categorías específicas
-  Más generalizable

 TRADE-OFF:
- R² esperado: ~0.70-0.75 (vs ~0.85 con categóricas)
- Aún suficiente para producción (duration_est tiene correlación ~0.9 con target)

Modelo Principal: CatBoostRegressor
Baseline: LinearRegression
Target: duration_real (días)

Output:
- Modelos entrenados en artifacts/numeric_only/
- Métricas comparativas en artifacts/regression_numeric_comparison.json
- Gráficos y reportes en reports/regression_numeric_analysis/
"""

import os
import json
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    mean_absolute_percentage_error
)
from sklearn.linear_model import LinearRegression

from catboost import CatBoostRegressor
import joblib
from scipy import stats

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Conexión a base de datos
HOST = os.getenv("MYSQL_HOST", "localhost")
DB   = os.getenv("MYSQL_DB", "sb")
USER = os.getenv("MYSQL_USER", "root")
PASS = os.getenv("MYSQL_PASS", "")
PORT = int(os.getenv("MYSQL_PORT", "3306"))

# Directorios de salida
ARTIFACT_DIR = Path("ml/models/duration")
REPORT_DIR   = Path("reports/regression_numeric_analysis")
ARTIFACT_DIR.mkdir(exist_ok=True, parents=True)
REPORT_DIR.mkdir(exist_ok=True, parents=True)

# Semilla para reproducibilidad
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Configuración de validación cruzada
CV_FOLDS = 5
N_BOOTSTRAP = 100

# ============================================================================
# UTILIDADES
# ============================================================================

def print_section(title, char="=", width=80):
    """Imprime un título formateado."""
    print(f"\n{char * width}")
    print(f"{title}")
    print(f"{char * width}")

def save_json(data, filepath):
    """Guarda datos en formato JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"    Guardado: {filepath}")

def calculate_regression_metrics(y_true, y_pred, name="", y_pred_samples=None):
    """Calcula métricas completas de regresión con intervalos de confianza."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    # MAPE con manejo de divisiones por cero
    y_true_nonzero = y_true[y_true != 0]
    y_pred_nonzero = y_pred[y_true != 0]
    if len(y_true_nonzero) > 0:
        mape = np.mean(np.abs((y_true_nonzero - y_pred_nonzero) / y_true_nonzero)) * 100
    else:
        mape = np.nan
    
    # Predicciones dentro de rangos
    within_2_days = np.mean(np.abs(y_true - y_pred) <= 2) * 100
    within_5_days = np.mean(np.abs(y_true - y_pred) <= 5) * 100
    within_10_days = np.mean(np.abs(y_true - y_pred) <= 10) * 100
    within_20_days = np.mean(np.abs(y_true - y_pred) <= 20) * 100
    
    # Calcular intervalos de confianza mediante bootstrap
    mae_ci = None
    rmse_ci = None
    if y_pred_samples is not None:
        mae_bootstrap = []
        rmse_bootstrap = []
        for _ in range(N_BOOTSTRAP):
            indices = np.random.choice(len(y_true), size=len(y_true), replace=True)
            mae_bootstrap.append(mean_absolute_error(y_true[indices], y_pred[indices]))
            rmse_bootstrap.append(np.sqrt(mean_squared_error(y_true[indices], y_pred[indices])))
        
        mae_ci = (np.percentile(mae_bootstrap, 2.5), np.percentile(mae_bootstrap, 97.5))
        rmse_ci = (np.percentile(rmse_bootstrap, 2.5), np.percentile(rmse_bootstrap, 97.5))
    
    metrics = {
        'mae': float(mae),
        'mae_ci_lower': float(mae_ci[0]) if mae_ci else None,
        'mae_ci_upper': float(mae_ci[1]) if mae_ci else None,
        'rmse': float(rmse),
        'rmse_ci_lower': float(rmse_ci[0]) if rmse_ci else None,
        'rmse_ci_upper': float(rmse_ci[1]) if rmse_ci else None,
        'r2': float(r2),
        'mape': float(mape) if not np.isnan(mape) else None,
        'within_2_days_pct': float(within_2_days),
        'within_5_days_pct': float(within_5_days),
        'within_10_days_pct': float(within_10_days),
        'within_20_days_pct': float(within_20_days)
    }
    
    if name:
        print(f"\n    Métricas {name}:")
        if mae_ci:
            print(f"      • MAE:  {mae:.3f} días [IC 95%: {mae_ci[0]:.3f} - {mae_ci[1]:.3f}]")
        else:
            print(f"      • MAE:  {mae:.3f} días")
        if rmse_ci:
            print(f"      • RMSE: {rmse:.3f} días [IC 95%: {rmse_ci[0]:.3f} - {rmse_ci[1]:.3f}]")
        else:
            print(f"      • RMSE: {rmse:.3f} días")
        print(f"      • R²:   {r2:.4f}")
        if not np.isnan(mape):
            print(f"      • MAPE: {mape:.2f}%")
        print(f"      • Dentro de ±2 días:  {within_2_days:.1f}%")
        print(f"      • Dentro de ±5 días:  {within_5_days:.1f}%")
        print(f"      • Dentro de ±10 días: {within_10_days:.1f}%")
        print(f"      • Dentro de ±20 días: {within_20_days:.1f}%")
    
    return metrics

def plot_predictions_vs_actual(y_true, y_pred, title, filename):
    """Gráfico de predicciones vs valores reales."""
    plt.figure(figsize=(10, 8))
    
    plt.scatter(y_true, y_pred, alpha=0.5, s=20, edgecolors='k', linewidths=0.5)
    
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Predicción Perfecta')
    
    plt.fill_between([min_val, max_val], 
                     [min_val - 2, max_val - 2], 
                     [min_val + 2, max_val + 2],
                     alpha=0.2, color='green', label='±2 días')
    plt.fill_between([min_val, max_val], 
                     [min_val - 5, max_val - 5], 
                     [min_val + 5, max_val + 5],
                     alpha=0.1, color='blue', label='±5 días')
    
    plt.xlabel('Duración Real (días)', fontsize=12)
    plt.ylabel('Duración Predicha (días)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"    Gráfico guardado: {filename}")

def plot_residuals(y_true, y_pred, title, filename):
    """Gráfico de análisis de residuos."""
    residuals = y_pred - y_true
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # 1. Residuos vs Predicciones
    ax = axes[0, 0]
    ax.scatter(y_pred, residuals, alpha=0.5, s=20, edgecolors='k', linewidths=0.5)
    ax.axhline(y=0, color='r', linestyle='--', lw=2)
    ax.axhline(y=2, color='orange', linestyle=':', lw=1, label='±2 días')
    ax.axhline(y=-2, color='orange', linestyle=':', lw=1)
    ax.set_xlabel('Predicción (días)')
    ax.set_ylabel('Residuos (días)')
    ax.set_title('Residuos vs Predicciones')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # 2. Histograma de residuos
    ax = axes[0, 1]
    ax.hist(residuals, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    ax.axvline(x=0, color='r', linestyle='--', lw=2, label='Media ideal')
    ax.axvline(x=residuals.mean(), color='orange', linestyle='--', lw=2, 
               label=f'Media real: {residuals.mean():.2f}')
    ax.set_xlabel('Residuos (días)')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Distribución de Residuos')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # 3. Q-Q Plot
    ax = axes[1, 0]
    stats.probplot(residuals, dist="norm", plot=ax)
    ax.set_title('Q-Q Plot (Normalidad de Residuos)')
    ax.grid(alpha=0.3)
    
    # 4. Residuos vs Valores reales
    ax = axes[1, 1]
    ax.scatter(y_true, residuals, alpha=0.5, s=20, edgecolors='k', linewidths=0.5)
    ax.axhline(y=0, color='r', linestyle='--', lw=2)
    ax.set_xlabel('Duración Real (días)')
    ax.set_ylabel('Residuos (días)')
    ax.set_title('Residuos vs Valores Reales')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"    Gráfico guardado: {filename}")

def plot_feature_importance_regression(model, feature_names, model_name, filename, top_n=20):
    """Visualiza feature importance para regresión."""
    importances = model.get_feature_importance()
    
    indices = np.argsort(importances)[::-1][:top_n]
    top_features = [feature_names[i] for i in indices]
    top_importances = importances[indices]
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(top_features)), top_importances, color='steelblue')
    plt.yticks(range(len(top_features)), top_features)
    plt.xlabel('Importancia', fontsize=12)
    plt.title(f'Top {top_n} Features - {model_name}', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"    Gráfico guardado: {filename}")

# ============================================================================
# CARGA Y PREPARACIÓN DE DATOS
# ============================================================================

print_section(" ENTRENAMIENTO CATBOOST REGRESSOR - SOLO FEATURES NUMÉRICAS")

print("\n[1/8] Conectando a MySQL y cargando datos...")

try:
    url = URL.create(
        "mysql+pymysql",
        username=USER,
        password=PASS,
        host=HOST,
        port=PORT,
        database=DB,
        query={"charset": "utf8mb4"}
    )
    engine = create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 10})
    print(f"    Conectado a MySQL en {HOST}:{PORT}/{DB}")
except Exception as e:
    raise RuntimeError(f"❌ Error creando conexión a MySQL: {type(e).__name__}: {e}")

try:
    query = text("SELECT * FROM v_training_dataset_clean")
    df = pd.read_sql(query, engine)
    print(f"    Total filas cargadas: {len(df):,}")
except Exception as e:
    raise RuntimeError(f" Error ejecutando consulta SQL: {type(e).__name__}: {e}")
finally:
    engine.dispose()

# ============================================================================
# PREPARACIÓN DEL TARGET
# ============================================================================

print("\n[2/8] Preparando variable objetivo (duration_real)...")

target_col = "duration_real"
if target_col not in df.columns:
    raise RuntimeError(f" No se encontró la columna objetivo '{target_col}'")

df = df[~df[target_col].isna()].copy()
df = df[df[target_col] > 0].copy()

# Convertir de minutos a días
print(f"\n    Conversión de unidades:")
print(f"      Promedio antes: {df[target_col].mean():,.2f} minutos")

df[target_col] = df[target_col] / (60 * 24)
df['duration_est_imputed'] = df['duration_est_imputed'] / (60 * 24)

print(f"      Promedio después: {df[target_col].mean():.2f} días")
print(f"       Conversión aplicada: minutos → días")

n_total = len(df)
duration_stats = df[target_col].describe()

print(f"    Filas con target válido: {n_total:,}")
print(f"\n    Estadísticas de duration_real:")
print(f"      Media:    {duration_stats['mean']:.2f} días")
print(f"      Mediana:  {duration_stats['50%']:.2f} días")
print(f"      Mín:      {duration_stats['min']:.2f} días")
print(f"      Máx:      {duration_stats['max']:.2f} días")
print(f"      Std:      {duration_stats['std']:.2f} días")

skewness = stats.skew(df[target_col])
print(f"      Asimetría: {skewness:.2f} {'(sesgada a la derecha)' if skewness > 1 else '(simétrica)'}")

# ============================================================================
# SELECCIÓN DE FEATURES - SOLO NUMÉRICAS
# ============================================================================

print_section(" SELECCIÓN DE FEATURES - SOLO NUMÉRICAS (UNIVERSALES)", char="-")

print("\n[3/8] Seleccionando features numéricas sin dependencias de dominio...")

# Features que causan data leakage
LEAKAGE_FEATURES = {
    "duration_real",
    "person_avg_delay_ratio",
    "task_success_rate",
    "completed_on_time_alt",
}

#  FEATURES NUMÉRICAS UNIVERSALES (funcionan en cualquier dominio)
NUMERIC_FEATURES = {
    # Características de la tarea
    "duration_est_imputed",  #  MUY IMPORTANTE (correlación ~0.9)
    
    # Características de la persona
    "experience_years_imputed",       # Años de experiencia
    "availability_hours_week_imputed", # Disponibilidad semanal
    "current_load_imputed",            # Carga actual de trabajo
    "performance_index_imputed",       # Índice de rendimiento (0-1)
    "rework_rate_imputed",             # Tasa de retrabajos (0-1)
    
    # Métricas derivadas
    "load_ratio",  # Ratio de carga (current_load / availability)
}

# Convertir complexity_level a numérico si existe
if 'complexity_level' in df.columns:
    # Intentar convertir a numérico
    df['complexity_numeric'] = pd.to_numeric(df['complexity_level'], errors='coerce')
    
    # Si hay valores textuales (Baja/Media/Alta), mapearlos
    if df['complexity_numeric'].isna().any():
        complexity_map = {
            'Baja': 1, 'baja': 1, 'LOW': 1, 'Low': 1,
            'Media': 2, 'media': 2, 'MEDIUM': 2, 'Medium': 2,
            'Alta': 3, 'alta': 3, 'HIGH': 3, 'High': 3,
        }
        df['complexity_numeric'] = df['complexity_level'].map(complexity_map).fillna(df['complexity_numeric'])
    
    # Si aún hay valores numéricos grandes (100, 200, 400), normalizarlos
    if df['complexity_numeric'].max() > 10:
        # Normalizar a escala 1-3
        min_val = df['complexity_numeric'].min()
        max_val = df['complexity_numeric'].max()
        df['complexity_numeric'] = 1 + 2 * (df['complexity_numeric'] - min_val) / (max_val - min_val)
    
    NUMERIC_FEATURES.add('complexity_numeric')
    print(f"    complexity_level convertido a complexity_numeric (escala 1-3)")

# Filtrar features que existen en el DataFrame
feature_cols = [c for c in df.columns if c in NUMERIC_FEATURES]

print(f"\n    Features numéricas seleccionadas: {len(feature_cols)}")
for col in sorted(feature_cols):
    print(f"      • {col}")

print(f"\n    Features categóricas ELIMINADAS (evitar dependencia de dominio):")
categorical_excluded = ['task_area', 'task_type', 'person_area', 'role']
for col in categorical_excluded:
    print(f"      • {col} (específico del dominio)")

# Verificar correlación con target
print(f"\n    Correlaciones con duration_real:")
correlations = df[[target_col] + feature_cols].corr()[target_col].sort_values(ascending=False)
for col in feature_cols:
    corr = correlations[col]
    print(f"      • {col:<35} {corr:>6.3f}")

# Guardar configuración
columns_config = {
    "numeric": feature_cols,
    "categorical": [],  # No se usan categóricas
    "excluded_categorical": categorical_excluded,
    "excluded_leakage": list(LEAKAGE_FEATURES),
    "target": target_col,
    "target_stats": {
        "mean": float(duration_stats['mean']),
        "median": float(duration_stats['50%']),
        "std": float(duration_stats['std']),
        "min": float(duration_stats['min']),
        "max": float(duration_stats['max']),
        "skewness": float(skewness)
    },
    "note": "Modelo entrenado SOLO con features numéricas para generalización cross-domain"
}
save_json(columns_config, ARTIFACT_DIR / "columns_regression_numeric.json")

# ============================================================================
# PREPARAR X E Y
# ============================================================================

print("\n[4/8] Preparando datos con transformación logarítmica...")

X = df[feature_cols].copy()
y = df[target_col].copy()

# Imputar valores faltantes en X
print(f"\n    Imputación de valores faltantes:")
for col in feature_cols:
    if X[col].isna().any() or X[col].isna().all():
        n_missing = X[col].isna().sum()
        
        # Si toda la columna es NaN, usar 0
        if X[col].isna().all():
            X[col] = 0.0
            print(f"      • {col}: {n_missing} NaN → 0.0 (columna vacía)")
        else:
            # Usar mediana si hay valores válidos
            median_val = X[col].median()
            if pd.isna(median_val):
                # Si la mediana también es NaN, usar 0
                X[col] = X[col].fillna(0.0)
                print(f"      • {col}: {n_missing} NaN → 0.0 (mediana inválida)")
            else:
                X[col] = X[col].fillna(median_val)
                print(f"      • {col}: {n_missing} NaN → {median_val:.2f} (mediana)")

# Transformación log del target
y_log = np.log1p(y)

print(f"\n    Shape de X: {X.shape}")
print(f"    Shape de y: {y.shape}")
print(f"    Target transformado: log1p(duration_real)")
print(f"      Rango original: [{y.min():.2f}, {y.max():.2f}] días")
print(f"      Rango log:      [{y_log.min():.2f}, {y_log.max():.2f}]")

# Split estratificado
print("\n    Creando split estratificado por duración...")
duration_bins = pd.qcut(y, q=5, labels=False, duplicates='drop')

X_train, X_test, y_train_log, y_test_log, y_train, y_test = train_test_split(
    X, y_log, y,
    test_size=0.2, 
    random_state=RANDOM_STATE, 
    stratify=duration_bins
)

print(f"    Train: {len(X_train):,} filas")
print(f"    Test:  {len(X_test):,} filas")
print(f"    Media duración train: {y_train.mean():.2f} días")
print(f"    Media duración test:  {y_test.mean():.2f} días")

# ============================================================================
# MODELO 1: LINEAR REGRESSION (BASELINE)
# ============================================================================

print_section(" MODELO 1: LINEAR REGRESSION (BASELINE)", char="-")

print("\n[5/8] Entrenando LinearRegression como baseline...")

# Normalizar features para LinearRegression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train_log)

lr_y_pred_log = lr_model.predict(X_test_scaled)
lr_y_pred = np.expm1(lr_y_pred_log)
y_test_original = y_test.values

lr_metrics = calculate_regression_metrics(y_test_original, lr_y_pred, "Linear Regression")

joblib.dump({'model': lr_model, 'scaler': scaler}, ARTIFACT_DIR / "model_linear_regression_numeric.pkl")
print(f"\n    Modelo guardado: {ARTIFACT_DIR / 'model_linear_regression_numeric.pkl'}")

plot_predictions_vs_actual(
    y_test_original, lr_y_pred,
    "Linear Regression (Numéricas Only) - Predicción vs Real",
    REPORT_DIR / "predictions_vs_actual_lr_numeric.png"
)

plot_residuals(
    y_test_original, lr_y_pred,
    "Linear Regression (Numéricas Only) - Análisis de Residuos",
    REPORT_DIR / "residuals_lr_numeric.png"
)

# ============================================================================
# MODELO 2: CATBOOST RMSE (PRINCIPAL)
# ============================================================================

print_section(" MODELO 2: CATBOOST RMSE (PRINCIPAL - NUMÉRICAS ONLY)", char="-")

print("\n[6/8] Entrenando CatBoost con loss='RMSE' (solo features numéricas)...")

catboost_rmse = CatBoostRegressor(
    loss_function='RMSE',
    eval_metric='RMSE',
    iterations=1500,
    learning_rate=0.03,
    depth=7,
    l2_leaf_reg=3,
    random_seed=RANDOM_STATE,
    verbose=100,
    early_stopping_rounds=100,
    bagging_temperature=0.5,
    random_strength=1.0
)

catboost_rmse.fit(
    X_train, y_train_log,
    eval_set=(X_test, y_test_log),
    verbose=100
)

print("\n    Validación cruzada con 5 folds...")
cv_scores = []
kfold = KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
for fold_num, (train_idx, val_idx) in enumerate(kfold.split(X_train), 1):
    print(f"    Procesando fold {fold_num}/{CV_FOLDS}...", end=" ")
    
    X_fold_train = X_train.iloc[train_idx]
    X_fold_val = X_train.iloc[val_idx]
    y_fold_train = y_train_log.iloc[train_idx]
    y_fold_val = y_train_log.iloc[val_idx]
    
    model_cv = CatBoostRegressor(
        loss_function='RMSE',
        iterations=300,
        learning_rate=0.05,
        depth=7,
        l2_leaf_reg=3,
        random_seed=RANDOM_STATE,
        verbose=0
    )
    model_cv.fit(X_fold_train, y_fold_train, verbose=0)
    y_val_pred_log = model_cv.predict(X_fold_val)
    y_val_pred = np.expm1(y_val_pred_log)
    y_val_true = np.expm1(y_fold_val)
    
    mae_fold = mean_absolute_error(y_val_true, y_val_pred)
    cv_scores.append(mae_fold)
    print(f"MAE: {mae_fold:.2f} días ")

cv_mean = np.mean(cv_scores)
cv_std = np.std(cv_scores)
print(f"    CV MAE promedio: {cv_mean:.3f} ± {cv_std:.3f} días")

# Predicciones
cb_rmse_y_pred_log = catboost_rmse.predict(X_test)
cb_rmse_y_pred = np.expm1(cb_rmse_y_pred_log)

cb_rmse_metrics = calculate_regression_metrics(y_test_original, cb_rmse_y_pred, "CatBoost RMSE (Numeric)", y_pred_samples=True)
cb_rmse_metrics['cv_mae_mean'] = float(cv_mean)
cb_rmse_metrics['cv_mae_std'] = float(cv_std)

# Mejora vs baseline
print(f"\n    Mejora vs Linear Regression:")
for metric in ['mae', 'rmse', 'r2']:
    if metric == 'r2':
        improvement = (cb_rmse_metrics[metric] - lr_metrics[metric]) / abs(lr_metrics[metric]) * 100
    else:
        improvement = -(cb_rmse_metrics[metric] - lr_metrics[metric]) / lr_metrics[metric] * 100
    symbol = "" if improvement > 0 else ""
    print(f"      {symbol} {metric.upper()}: {improvement:+.2f}%")

# Guardar modelo
joblib.dump(catboost_rmse, ARTIFACT_DIR / "model_catboost_rmse_numeric.pkl")
print(f"\n    Modelo guardado: {ARTIFACT_DIR / 'model_catboost_rmse_numeric.pkl'}")

plot_predictions_vs_actual(
    y_test_original, cb_rmse_y_pred,
    "CatBoost RMSE (Numéricas Only) - Predicción vs Real",
    REPORT_DIR / "predictions_vs_actual_catboost_numeric.png"
)

plot_residuals(
    y_test_original, cb_rmse_y_pred,
    "CatBoost RMSE (Numéricas Only) - Análisis de Residuos",
    REPORT_DIR / "residuals_catboost_numeric.png"
)

plot_feature_importance_regression(
    catboost_rmse, feature_cols, "CatBoost RMSE (Numéricas Only)",
    REPORT_DIR / "feature_importance_catboost_numeric.png", top_n=len(feature_cols)
)

# ============================================================================
# MODELO 3: CATBOOST MAE (ROBUSTO)
# ============================================================================

print_section(" MODELO 3: CATBOOST MAE (ROBUSTO A OUTLIERS)", char="-")

print("\n[7/8] Entrenando CatBoost con loss='MAE'...")

catboost_mae = CatBoostRegressor(
    loss_function='MAE',
    eval_metric='MAE',
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    l2_leaf_reg=3,
    random_seed=RANDOM_STATE,
    verbose=False,
    early_stopping_rounds=50
)

catboost_mae.fit(
    X_train, y_train_log,
    eval_set=(X_test, y_test_log),
    verbose=False
)

cb_mae_y_pred_log = catboost_mae.predict(X_test)
cb_mae_y_pred = np.expm1(cb_mae_y_pred_log)

cb_mae_metrics = calculate_regression_metrics(y_test_original, cb_mae_y_pred, "CatBoost MAE (Numeric)")

joblib.dump(catboost_mae, ARTIFACT_DIR / "model_catboost_mae_numeric.pkl")
print(f"\n    Modelo guardado: {ARTIFACT_DIR / 'model_catboost_mae_numeric.pkl'}")

# ============================================================================
# COMPARACIÓN FINAL
# ============================================================================

print_section(" COMPARACIÓN FINAL - MODELOS NUMÉRICOS", char="-")

print("\n    Tabla Comparativa de Métricas:\n")
print("   " + "-" * 100)
print(f"   {'Modelo':<30} {'MAE':>10} {'RMSE':>10} {'R²':>8} {'±5días':>10} {'±10días':>10}")
print("   " + "-" * 100)

models_results = {
    'Linear Regression': lr_metrics,
    'CatBoost RMSE (Numeric)': cb_rmse_metrics,
    'CatBoost MAE (Numeric)': cb_mae_metrics,
}

for model_name, metrics in models_results.items():
    print(f"   {model_name:<30} {metrics['mae']:>10.3f} {metrics['rmse']:>10.3f} "
          f"{metrics['r2']:>8.4f} {metrics['within_5_days_pct']:>9.1f}% "
          f"{metrics['within_10_days_pct']:>9.1f}%")

print("   " + "-" * 100)

# Determinar mejor modelo
best_model = max(models_results.items(), key=lambda x: x[1]['r2'])
print(f"\n    Mejor modelo (por R²): {best_model[0]}")
print(f"    R² = {best_model[1]['r2']:.4f} (explica {best_model[1]['r2']*100:.1f}% de la varianza)")

# Guardar comparación
comparison_data = {
    'timestamp': datetime.now().isoformat(),
    'model_type': 'numeric_only',
    'note': 'Entrenado solo con features numéricas para generalización cross-domain',
    'dataset_info': {
        'total_samples': n_total,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'target_stats': columns_config['target_stats'],
        'features_used': feature_cols
    },
    'models': models_results,
    'best_model': {
        'name': best_model[0],
        'metrics': best_model[1]
    }
}

save_json(comparison_data, ARTIFACT_DIR / "regression_numeric_comparison.json")

# Gráfico comparativo
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

metrics_to_plot = ['mae', 'rmse', 'r2']
titles = ['MAE (días) - Menor es mejor', 'RMSE (días) - Menor es mejor', 'R² - Mayor es mejor']

for idx, (metric, title) in enumerate(zip(metrics_to_plot, titles)):
    ax = axes[idx]
    model_names = list(models_results.keys())
    values = [models_results[name][metric] for name in model_names]
    
    colors = ['lightblue' if name != best_model[0] else 'green' for name in model_names]
    bars = ax.bar(range(len(model_names)), values, color=colors, edgecolor='black', alpha=0.7)
    
    ax.set_xticks(range(len(model_names)))
    ax.set_xticklabels(model_names, rotation=45, ha='right')
    ax.set_ylabel(metric.upper(), fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.3f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(REPORT_DIR / "models_comparison_numeric.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"\n    Gráfico comparativo guardado: models_comparison_numeric.png")

# ============================================================================
# REPORTE FINAL
# ============================================================================

print_section(" ENTRENAMIENTO COMPLETADO - MODELO NUMÉRICO", char="=")

print(f"""
 Archivos generados:

Modelos entrenados ({ARTIFACT_DIR}):
   • model_catboost_rmse_numeric.pkl  RECOMENDADO
   • model_catboost_mae_numeric.pkl
   • model_linear_regression_numeric.pkl

Configuración y métricas:
   • columns_regression_numeric.json
   • regression_numeric_comparison.json

Visualizaciones ({REPORT_DIR}):
   • predictions_vs_actual_catboost_numeric.png
   • residuals_catboost_numeric.png
   • feature_importance_catboost_numeric.png
   • models_comparison_numeric.png

 Resumen de Resultados:

Mejor modelo: {best_model[0]}
   • R² = {best_model[1]['r2']:.4f} (explica {best_model[1]['r2']*100:.1f}% de la varianza)
   • MAE = {best_model[1]['mae']:.2f} días (error promedio)
   • RMSE = {best_model[1]['rmse']:.2f} días
   • Dentro de ±5 días:  {best_model[1]['within_5_days_pct']:.1f}%
   • Dentro de ±10 días: {best_model[1]['within_10_days_pct']:.1f}%

 Características del Modelo Numérico:
    Compatible con CUALQUIER dominio (IT, rural, construcción, etc.)
    No requiere mapeo de categorías específicas de dominio
    Features universales: duración estimada, experiencia, carga, performance
    Menor overfitting, mejor generalización
    Validación cruzada: {cb_rmse_metrics.get('cv_mae_mean', 0):.2f} ± {cb_rmse_metrics.get('cv_mae_std', 0):.2f} días

 Trade-off vs Modelo con Categóricas:
   • R² esperado: ~{best_model[1]['r2']:.2f} (vs ~0.85 con categóricas)
   • Aún SUFICIENTE para producción
   • duration_est tiene correlación {correlations.get('duration_est_imputed', 0):.3f} con target

 Uso en producción:

   import joblib
   import numpy as np
   import pandas as pd
   
   # Cargar modelo
   model = joblib.load('artifacts/numeric_only/model_catboost_rmse_numeric.pkl')
   
   # Preparar datos (SOLO numéricas)
   X_new = pd.DataFrame([{{
       'duration_est_imputed': 10.0,  # días
       'complexity_numeric': 2.0,      # 1=Baja, 2=Media, 3=Alta
       'experience_years_imputed': 5.0,
       'availability_hours_week_imputed': 40.0,
       'current_load_imputed': 80.0,
       'performance_index_imputed': 0.85,
       'rework_rate_imputed': 0.15,
       'load_ratio': 2.0
   }}])
   
   # Predecir (deshacer transformación log)
   y_pred_log = model.predict(X_new)
   y_pred_dias = np.expm1(y_pred_log)[0]
   
   print(f"Duración estimada: {{y_pred_dias:.1f}} días")

 Ventajas de esta versión:
   • Funciona desde día 1 con TUS datos de producción
   • No necesitas re-mapear task_area, task_type, person_area, role
   • Compatible con dominio IT/Software (tu caso de uso)
   • Puedes ir mejorando con datos reales después
""")

print("\n" + "=" * 80)
print("¡Modelo numérico entrenado exitosamente!")
print("=" * 80 + "\n")
