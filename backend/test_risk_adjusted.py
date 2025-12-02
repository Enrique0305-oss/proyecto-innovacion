"""
Test del modelo de riesgo con ajustes de reglas de negocio
"""
from app.ml.risk_model import predict_risk

# Test 1: Alta complejidad + Crítica prioridad
print("=" * 60)
print("TEST 1: Alta complejidad + Prioridad Crítica + 1 persona + 5 deps")
print("=" * 60)
result = predict_risk({
    'area': 'TI',
    'task_type': 'Desarrollo',
    'complexity_level': 'Alta',
    'priority': 'Crítica',
    'duration_est': 30,
    'assignees_count': 1,
    'dependencies': 5
})
print(f"\n✓ Risk Level: {result['risk_level']}")
print(f"✓ Probability: {result['probability']:.1%}")
print(f"✓ Model Used: {result.get('model_used', 'unknown')}")
print(f"✓ Factors: {result.get('factors', [])}")
print(f"✓ Probabilities: BAJO={result['probabilities']['BAJO_RIESGO']:.1%}, ALTO={result['probabilities']['ALTO_RIESGO']:.1%}")

# Test 2: Media complejidad + Media prioridad
print("\n" + "=" * 60)
print("TEST 2: Media complejidad + Media prioridad")
print("=" * 60)
result2 = predict_risk({
    'area': 'TI',
    'task_type': 'Desarrollo',
    'complexity_level': 'Media',
    'priority': 'Media',
    'duration_est': 10,
    'assignees_count': 1,
    'dependencies': 0
})
print(f"\n✓ Risk Level: {result2['risk_level']}")
print(f"✓ Probability: {result2['probability']:.1%}")
print(f"✓ Model Used: {result2.get('model_used', 'unknown')}")

# Test 3: Baja complejidad + Baja prioridad
print("\n" + "=" * 60)
print("TEST 3: Baja complejidad + Baja prioridad")
print("=" * 60)
result3 = predict_risk({
    'area': 'Marketing',
    'task_type': 'Diseño',
    'complexity_level': 'Baja',
    'priority': 'Baja',
    'duration_est': 5,
    'assignees_count': 2,
    'dependencies': 0
})
print(f"\n✓ Risk Level: {result3['risk_level']}")
print(f"✓ Probability: {result3['probability']:.1%}")
print(f"✓ Model Used: {result3.get('model_used', 'unknown')}")
