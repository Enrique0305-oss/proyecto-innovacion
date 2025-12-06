"""
Script para identificar los valores categóricos esperados por el modelo de duración.
Genera predicciones con diferentes valores categóricos para encontrar el mapeo correcto.
"""
import joblib
import json
import pandas as pd
import numpy as np
from itertools import product

# Cargar modelo
model_path = r"D:\proyecto-innovacion\backend\ml\models\duration\model_catboost_rmse.pkl"
config_path = r"D:\proyecto-innovacion\backend\ml\models\duration\columns_regression.json"

print("="*80)
print("🔍 IDENTIFICADOR DE VALORES CATEGÓRICOS DEL MODELO")
print("="*80)

# Cargar modelo y config
model = joblib.load(model_path)
with open(config_path, 'r') as f:
    config = json.load(f)

print(f"\n✅ Modelo cargado: {type(model)}")
print(f"✅ Features: {len(config['numeric']) + len(config['categorical'])}")

# Lista de valores categóricos a probar
category_variants = {
    'task_area': [
        'IT', 'TI', 'Technology', 'Information Technology', 'Engineering', 'Ingenieria',
        'Development', 'Desarrollo', 'Operations', 'Operaciones', 'Support', 'Soporte'
    ],
    'task_type': [
        'Desarrollo', 'Development', 'Dev', 'Maintenance', 'Mantenimiento', 'Mant',
        'Research', 'Investigación', 'Investigacion', 'Testing', 'Pruebas', 
        'Documentation', 'Documentación', 'Documentacion', 'Bug', 'Error'
    ],
    'complexity_level': [
        'Baja', 'Low', 'L', '1', 'Simple', 
        'Media', 'Medium', 'M', '2', 'Normal',
        'Alta', 'High', 'H', '3', 'Complex'
    ],
    'person_area': [
        'IT', 'TI', 'Engineering', 'Ingenieria', 'Development', 'Desarrollo',
        'Operations', 'Operaciones', 'Support', 'Soporte'
    ],
    'role': [
        'Colaborador', 'Contributor', 'Worker', 'Employee', 'Empleado',
        'Developer', 'Desarrollador', 'Analyst', 'Analista', 'Engineer', 'Ingeniero'
    ]
}

# Features numéricas fijas para las pruebas
fixed_numeric = {
    'duration_est_imputed': 240.0,  # 10 días en horas
    'experience_years_imputed': 3.0,
    'availability_hours_week_imputed': 40.0,
    'current_load_imputed': 0.0,
    'performance_index_imputed': 75.0
}

# Orden de columnas según el modelo
training_order = [
    'task_area', 'task_type', 'complexity_level', 'duration_est_imputed',
    'person_area', 'role', 'experience_years_imputed', 'availability_hours_week_imputed',
    'current_load_imputed', 'performance_index_imputed', 'rework_rate_imputed', 'load_ratio'
]

print("\n🧪 PROBANDO COMBINACIONES DE VALORES CATEGÓRICOS")
print("-" * 80)

results = {}

# Test 1: Probar cada categoría individualmente
print("\n📊 TEST 1: Valores individuales de task_area")
for area in category_variants['task_area']:
    test_data = fixed_numeric.copy()
    test_data.update({
        'task_area': str(area),
        'task_type': 'Development',  # Valor por defecto
        'complexity_level': 'Medium',  # Valor por defecto
        'person_area': str(area),  # Mismo que task_area
        'role': 'Developer',  # Valor por defecto
        'rework_rate_imputed': '0.1',
        'load_ratio': '0.0'
    })
    
    df = pd.DataFrame([test_data])[training_order]
    try:
        pred = model.predict(df)[0]
        results[f"area_{area}"] = pred
        print(f"   {area:30s} → {pred:6.1f} horas ({pred/24:4.1f} días)")
    except Exception as e:
        print(f"   {area:30s} → ERROR: {str(e)[:50]}")

print("\n📊 TEST 2: Valores individuales de task_type")
for ttype in category_variants['task_type']:
    test_data = fixed_numeric.copy()
    test_data.update({
        'task_area': 'IT',
        'task_type': str(ttype),
        'complexity_level': 'Medium',
        'person_area': 'IT',
        'role': 'Developer',
        'rework_rate_imputed': '0.1',
        'load_ratio': '0.0'
    })
    
    df = pd.DataFrame([test_data])[training_order]
    try:
        pred = model.predict(df)[0]
        results[f"type_{ttype}"] = pred
        print(f"   {ttype:30s} → {pred:6.1f} horas ({pred/24:4.1f} días)")
    except Exception as e:
        print(f"   {ttype:30s} → ERROR: {str(e)[:50]}")

print("\n📊 TEST 3: Valores individuales de complexity_level")
for complexity in category_variants['complexity_level']:
    test_data = fixed_numeric.copy()
    test_data.update({
        'task_area': 'IT',
        'task_type': 'Development',
        'complexity_level': str(complexity),
        'person_area': 'IT',
        'role': 'Developer',
        'rework_rate_imputed': '0.1',
        'load_ratio': '0.0'
    })
    
    df = pd.DataFrame([test_data])[training_order]
    try:
        pred = model.predict(df)[0]
        results[f"complexity_{complexity}"] = pred
        print(f"   {complexity:30s} → {pred:6.1f} horas ({pred/24:4.1f} días)")
    except Exception as e:
        print(f"   {complexity:30s} → ERROR: {str(e)[:50]}")

# Encontrar valores que generan variación
print("\n" + "="*80)
print("📈 ANÁLISIS DE RESULTADOS")
print("="*80)

predictions = list(results.values())
if predictions:
    print(f"\n  Mínimo:  {min(predictions):6.1f} horas ({min(predictions)/24:4.1f} días)")
    print(f"  Máximo:  {max(predictions):6.1f} horas ({max(predictions)/24:4.1f} días)")
    print(f"  Promedio: {np.mean(predictions):6.1f} horas ({np.mean(predictions)/24:4.1f} días)")
    print(f"  Std Dev:  {np.std(predictions):6.1f} horas")
    
    if np.std(predictions) > 1:
        print("\n  ✅ El modelo SÍ está generando variación!")
        print("\n  🎯 VALORES QUE GENERAN PREDICCIONES DIFERENTES:")
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        for key, pred in sorted_results[:10]:
            print(f"     {key:40s} → {pred:6.1f} horas ({pred/24:4.1f} días)")
    else:
        print("\n  ⚠️  El modelo genera predicciones muy similares.")
        print("      Posibles causas:")
        print("      - Los valores categóricos no coinciden con el entrenamiento")
        print("      - El modelo tiene overfitting")
        print("      - Las features numéricas dominan completamente")

print("\n" + "="*80)
print("💡 SIGUIENTE PASO:")
print("="*80)
print("   Si el modelo genera variación, identifica qué valores generan")
print("   predicciones más altas/bajas y úsalos como referencia para el mapeo.")
print("\n   Si el modelo NO genera variación, necesitas:")
print("   1. Revisar el dataset original de entrenamiento")
print("   2. Verificar si las categorías fueron codificadas numéricamente")
print("   3. Considerar re-entrenar el modelo con las categorías actuales")
print("="*80)
