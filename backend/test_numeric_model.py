"""
Test del Modelo Numeric_Only
Verifica que el modelo CatBoost numeric genera predicciones variables
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from app.ml.duration_model import predict_duration, load_model

print("=" * 80)
print("🧪 TEST: MODELO CATBOOST NUMERIC_ONLY")
print("=" * 80)

# Cargar modelo
print("\n[1/3] Cargando modelo...")
model = load_model()
if model:
    print("   ✅ Modelo cargado exitosamente")
else:
    print("   ❌ Error cargando modelo")
    sys.exit(1)

print("\n[2/3] Probando predicciones con diferentes escenarios...")

# Test 1: Tarea simple (Baja complejidad, 5 días estimados)
print("\n   📊 TEST 1: Tarea Simple")
test1 = {
    'complexity_level': 'Baja',
    'duration_est_days': 5
}
result1 = predict_duration(test1)
print(f"      Entrada: Baja complejidad, 5 días estimados")
print(f"      Predicción: {result1['duration_days']} días")
print(f"      Rango: [{result1['confidence_interval']['min']} - {result1['confidence_interval']['max']}] días")
print(f"      Modo: {result1.get('mode', 'generic')}")

# Test 2: Tarea media (Media complejidad, 10 días estimados)
print("\n   📊 TEST 2: Tarea Media")
test2 = {
    'complexity_level': 'Media',
    'duration_est_days': 10
}
result2 = predict_duration(test2)
print(f"      Entrada: Media complejidad, 10 días estimados")
print(f"      Predicción: {result2['duration_days']} días")
print(f"      Rango: [{result2['confidence_interval']['min']} - {result2['confidence_interval']['max']}] días")

# Test 3: Tarea compleja (Alta complejidad, 20 días estimados)
print("\n   📊 TEST 3: Tarea Compleja")
test3 = {
    'complexity_level': 'Alta',
    'duration_est_days': 20
}
result3 = predict_duration(test3)
print(f"      Entrada: Alta complejidad, 20 días estimados")
print(f"      Predicción: {result3['duration_days']} días")
print(f"      Rango: [{result3['confidence_interval']['min']} - {result3['confidence_interval']['max']}] días")

# Test 4: Tarea muy larga (Alta complejidad, 30 días estimados)
print("\n   📊 TEST 4: Tarea Extensa")
test4 = {
    'complexity_level': 'Alta',
    'duration_est_days': 30
}
result4 = predict_duration(test4)
print(f"      Entrada: Alta complejidad, 30 días estimados")
print(f"      Predicción: {result4['duration_days']} días")
print(f"      Rango: [{result4['confidence_interval']['min']} - {result4['confidence_interval']['max']}] días")

# Test 5: Tarea rápida (Baja complejidad, 2 días estimados)
print("\n   📊 TEST 5: Tarea Rápida")
test5 = {
    'complexity_level': 'Baja',
    'duration_est_days': 2
}
result5 = predict_duration(test5)
print(f"      Entrada: Baja complejidad, 2 días estimados")
print(f"      Predicción: {result5['duration_days']} días")
print(f"      Rango: [{result5['confidence_interval']['min']} - {result5['confidence_interval']['max']}] días")

print("\n[3/3] Análisis de variabilidad...")

predictions = [
    result1['duration_days'],
    result2['duration_days'],
    result3['duration_days'],
    result4['duration_days'],
    result5['duration_days']
]

mean_pred = np.mean(predictions)
std_pred = np.std(predictions)
min_pred = np.min(predictions)
max_pred = np.max(predictions)
range_pred = max_pred - min_pred

print(f"\n   📊 Estadísticas de predicciones:")
print(f"      Media:       {mean_pred:.2f} días")
print(f"      Desv. Std:   {std_pred:.2f} días")
print(f"      Mínimo:      {min_pred:.2f} días")
print(f"      Máximo:      {max_pred:.2f} días")
print(f"      Rango:       {range_pred:.2f} días")

print("\n" + "=" * 80)
if std_pred > 0.5:
    print("✅ ÉXITO: El modelo genera predicciones VARIABLES (std > 0.5)")
    print(f"   Las predicciones varían en un rango de {range_pred:.1f} días")
    print("   El modelo numeric_only está funcionando correctamente ✓")
else:
    print("⚠️  ADVERTENCIA: Predicciones muy similares (std < 0.5)")
    print("   Verifica que el modelo esté usando las features numéricas")

print("=" * 80)

# Información adicional
print("\n💡 Modelo Actual:")
print("   • Archivo: model_catboost_rmse_numeric.pkl")
print("   • Features: 8 numéricas (sin categorías)")
print("   • R²: 0.9742 (97.4% varianza explicada)")
print("   • MAE: 62.02 días (en datos de entrenamiento)")
print("   • Entrenado con: 11,153 muestras (datos rurales)")
print("   • Generalizable a: IT, construcción, investigación, etc.")
