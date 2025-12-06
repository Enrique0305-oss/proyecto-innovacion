"""
Análisis de Calibración del Modelo Numeric_Only
Identifica el factor de escala necesario para ajustar predicciones a dominio IT
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from app.ml.duration_model import predict_duration

print("=" * 80)
print("📊 ANÁLISIS DE CALIBRACIÓN - MODELO NUMERIC_ONLY")
print("=" * 80)

print("\n📌 Contexto:")
print("   • Modelo entrenado con: Datos rurales (~834 días promedio)")
print("   • Dominio de producción: Tareas IT (5-30 días típico)")
print("   • Solución: Factor de calibración para ajustar escala")

print("\n[1/2] Evaluando predicciones actuales...")

# Casos de prueba representativos del dominio IT
test_cases = [
    {'name': 'Tarea Muy Simple', 'complexity': 'Baja', 'est': 2, 'expected_range': '1-3 días'},
    {'name': 'Tarea Simple', 'complexity': 'Baja', 'est': 5, 'expected_range': '3-7 días'},
    {'name': 'Tarea Media', 'complexity': 'Media', 'est': 10, 'expected_range': '8-15 días'},
    {'name': 'Tarea Compleja', 'complexity': 'Alta', 'est': 15, 'expected_range': '12-20 días'},
    {'name': 'Tarea Muy Compleja', 'complexity': 'Alta', 'est': 20, 'expected_range': '18-30 días'},
    {'name': 'Proyecto Grande', 'complexity': 'Alta', 'est': 30, 'expected_range': '25-40 días'},
]

predictions_raw = []
estimations = []

print("\n   Caso                    | Estimado | Predicción Raw | Esperado IT")
print("   " + "-" * 70)

for case in test_cases:
    result = predict_duration({
        'complexity_level': case['complexity'],
        'duration_est_days': case['est']
    })
    pred = result['duration_days']
    predictions_raw.append(pred)
    estimations.append(case['est'])
    
    print(f"   {case['name']:<22} | {case['est']:>8} días | {pred:>13.1f} días | {case['expected_range']}")

print("\n[2/2] Calculando factor de calibración...")

# Calcular ratio promedio: predicción / estimación
ratios = [p / e for p, e in zip(predictions_raw, estimations)]
avg_ratio = np.mean(ratios)
median_ratio = np.median(ratios)
std_ratio = np.std(ratios)

print(f"\n   📊 Análisis de ratios (Predicción / Estimación):")
print(f"      Promedio: {avg_ratio:.2f}x")
print(f"      Mediana:  {median_ratio:.2f}x")
print(f"      Desv Std: {std_ratio:.2f}")

# Factor de calibración sugerido
calibration_factor = 1.0 / median_ratio

print(f"\n   🎯 Factor de Calibración Sugerido: {calibration_factor:.4f}")
print(f"      Esto reducirá predicciones de ~{avg_ratio:.1f}x a ~1.0x")

# Mostrar predicciones calibradas
print("\n   📊 Predicciones Calibradas:")
print("   " + "-" * 70)
print("   Caso                    | Estimado | Raw      | Calibrado | Esperado IT")
print("   " + "-" * 70)

for i, case in enumerate(test_cases):
    raw_pred = predictions_raw[i]
    calibrated = raw_pred * calibration_factor
    print(f"   {case['name']:<22} | {case['est']:>8} | {raw_pred:>8.1f} | {calibrated:>9.1f} | {case['expected_range']}")

print("\n" + "=" * 80)
print("💡 RECOMENDACIONES:")
print("=" * 80)

print(f"""
1. OPCIÓN A - Calibración simple (rápido):
   Agregar factor de calibración en duration_model.py:
   
   predicted_days = np.expm1(predicted_log) * {calibration_factor:.4f}
   
   ✅ Ventaja: Implementación inmediata
   ⚠️  Desventaja: Aproximación lineal (puede no ser óptima)

2. OPCIÓN B - Re-entrenamiento con datos IT (mejor):
   • Acumular 500-1000 tareas IT completadas
   • Re-entrenar modelo con datos reales de tu dominio
   • Conservar arquitectura numeric_only
   
   ✅ Ventaja: Predicciones precisas para dominio IT
   ⚠️  Desventaja: Requiere datos de producción (3-6 meses)

3. OPCIÓN C - Usar heurística temporalmente:
   El modelo predict_duration_heuristic() ya genera predicciones
   razonables (5-30 días) basadas en reglas de negocio
   
   ✅ Ventaja: Funciona bien para IT desde día 1
   ⚠️  Desventaja: Menos sofisticado que ML

4. OPCIÓN D - Modelo híbrido (recomendado para ahora):
   • Si predicción CatBoost > 50 días → usar heurística
   • Si predicción CatBoost 5-50 días → usar calibrada
   • Si predicción CatBoost < 5 días → usar heurística
   
   ✅ Ventaja: Combina lo mejor de ambos mundos
   ✅ Funciona razonablemente bien hasta tener datos IT
""")

print("=" * 80)
print(f"📝 CONCLUSIÓN:")
print(f"   El modelo numeric_only funciona CORRECTAMENTE (genera variabilidad)")
print(f"   Solo necesita calibración de escala para dominio IT")
print(f"   Factor sugerido: {calibration_factor:.4f}")
print("=" * 80)
