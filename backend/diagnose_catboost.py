"""
Diagnóstico del modelo CatBoost para identificar índices de features categóricas
"""
import joblib
import json
import pandas as pd
from catboost import CatBoostRegressor

# Cargar modelo
model_path = r"D:\proyecto-innovacion\backend\ml\models\duration\model_catboost_rmse.pkl"
config_path = r"D:\proyecto-innovacion\backend\ml\models\duration\columns_regression.json"

print("="*80)
print("🔍 DIAGNÓSTICO DEL MODELO CATBOOST")
print("="*80)

# 1. Cargar configuración
with open(config_path, 'r') as f:
    config = json.load(f)

print("\n📋 CONFIGURACIÓN (columns_regression.json):")
print(f"   Numéricas ({len(config['numeric'])}): {config['numeric']}")
print(f"   Categóricas ({len(config['categorical'])}): {config['categorical']}")

# 2. Cargar modelo
model = joblib.load(model_path)
print(f"\n✅ Modelo cargado: {type(model)}")

# 3. Obtener información del modelo
if hasattr(model, 'get_cat_feature_indices'):
    cat_indices = model.get_cat_feature_indices()
    print(f"\n🔢 ÍNDICES DE FEATURES CATEGÓRICAS EN EL MODELO:")
    print(f"   {cat_indices}")
else:
    print("\n⚠️  Modelo no tiene método get_cat_feature_indices()")

if hasattr(model, 'feature_names_'):
    feature_names = model.feature_names_
    print(f"\n📝 NOMBRES DE FEATURES EN EL MODELO ({len(feature_names)}):")
    for i, name in enumerate(feature_names):
        cat_marker = " [CAT]" if hasattr(model, 'get_cat_feature_indices') and i in model.get_cat_feature_indices() else ""
        print(f"   [{i:2d}] {name}{cat_marker}")
else:
    print("\n⚠️  Modelo no tiene atributo feature_names_")

# 4. Crear DataFrame de prueba
all_features = config['numeric'] + config['categorical']
print(f"\n🧪 ORDEN ESPERADO SEGÚN CONFIG ({len(all_features)} features):")
for i, feat in enumerate(all_features):
    tipo = "NUM" if feat in config['numeric'] else "CAT"
    print(f"   [{i:2d}] {feat} ({tipo})")

# 5. Prueba de predicción
print("\n🔬 PRUEBA DE PREDICCIÓN:")
test_data = {
    'duration_est_imputed': 10.0,
    'experience_years_imputed': 2.0,
    'availability_hours_week_imputed': 40.0,
    'current_load_imputed': 0.0,
    'performance_index_imputed': 50.0,
    'task_area': 'IT',
    'task_type': 'Desarrollo',
    'complexity_level': 'Alta',
    'person_area': 'IT',
    'role': 'Colaborador',
    'rework_rate_imputed': 'Baja',
    'load_ratio': 'Baja'
}

df = pd.DataFrame([test_data])

# Reordenar según config
df = df[all_features]

print(f"   Shape: {df.shape}")
print(f"   Dtypes:")
for col in df.columns:
    print(f"     {col}: {df[col].dtype}")

print(f"\n   Valores:")
print(df.iloc[0].to_dict())

# Intentar predicción SIN convertir categóricas
print("\n🧪 INTENTO 1: Sin conversión de categóricas")
try:
    pred1 = model.predict(df)
    print(f"   ✅ Predicción exitosa: {pred1[0]:.2f} horas")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:100]}")

# Intentar predicción CONVIRTIENDO categóricas
print("\n🧪 INTENTO 2: Convirtiendo categóricas a str")
df_cat = df.copy()
for col in config['categorical']:
    df_cat[col] = df_cat[col].astype(str)

print(f"   Dtypes después de conversión:")
for col in df_cat.columns:
    print(f"     {col}: {df_cat[col].dtype}")

try:
    pred2 = model.predict(df_cat)
    print(f"   ✅ Predicción exitosa: {pred2[0]:.2f} horas")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:100]}")

# Intentar predicción con Pool explícito
print("\n🧪 INTENTO 3: Usando Pool con cat_features explícito")
from catboost import Pool

try:
    # Obtener índices categóricos del modelo
    cat_indices = model.get_cat_feature_indices() if hasattr(model, 'get_cat_feature_indices') else []
    
    pool = Pool(
        data=df,
        cat_features=cat_indices
    )
    pred3 = model.predict(pool)
    print(f"   ✅ Predicción exitosa: {pred3[0]:.2f} horas")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:100]}")

print("\n" + "="*80)
