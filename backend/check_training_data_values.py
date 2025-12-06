"""
Script para consultar los valores categóricos únicos en v_training_dataset_clean
Esto te mostrará exactamente qué valores espera el modelo CatBoost.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd

# Configuración de conexión (ajusta según tu BD)
HOST = os.getenv("MYSQL_HOST", "localhost")
DB   = os.getenv("MYSQL_DB", "sb")  # O "sb" según tu BD
USER = os.getenv("MYSQL_USER", "root")
PASS = os.getenv("MYSQL_PASS", "1234")
PORT = int(os.getenv("MYSQL_PORT", "3306"))

print("="*80)
print("🔍 VALORES CATEGÓRICOS EN v_training_dataset_clean")
print("="*80)

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
    print(f"\n✅ Conectado a MySQL: {HOST}:{PORT}/{DB}\n")
    
    # Consultar la vista
    query = text("SELECT * FROM v_training_dataset_clean LIMIT 10000")
    df = pd.read_sql(query, engine)
    print(f"📊 Filas consultadas: {len(df):,}\n")
    
    # Columnas categóricas relevantes
    categorical_cols = ['task_area', 'task_type', 'complexity_level', 'person_area', 'role']
    
    print("-"*80)
    for col in categorical_cols:
        if col in df.columns:
            unique_values = df[col].dropna().unique()
            value_counts = df[col].value_counts()
            
            print(f"\n📋 {col.upper()}:")
            print(f"   Valores únicos: {len(unique_values)}")
            print(f"   Top 10 valores más frecuentes:")
            for val, count in value_counts.head(10).items():
                print(f"      • '{val}': {count:,} registros ({count/len(df)*100:.1f}%)")
        else:
            print(f"\n⚠️  {col} no encontrado en la vista")
    
    print("\n" + "="*80)
    print("💡 SOLUCIÓN:")
    print("="*80)
    print("\nActualiza prepare_features() en duration_model.py para usar estos valores.")
    print("Por ejemplo:")
    print("""
    # En prepare_features():
    task_area = str(task_data.get('area', 'valor_por_defecto_de_la_BD'))
    task_type = str(task_data.get('task_type', 'valor_por_defecto_de_la_BD'))
    # ...etc
    """)
    
    # Mostrar estadísticas de duration_est_imputed
    if 'duration_est_imputed' in df.columns:
        print("\n" + "="*80)
        print("📊 ESTADÍSTICAS DE duration_est_imputed:")
        print("="*80)
        stats = df['duration_est_imputed'].describe()
        print(f"\n   Media:    {stats['mean']:.2f}")
        print(f"   Mediana:  {stats['50%']:.2f}")
        print(f"   Mín:      {stats['min']:.2f}")
        print(f"   Máx:      {stats['max']:.2f}")
        print(f"   Unidad:   {'HORAS' if stats['mean'] > 100 else 'DÍAS'}")
        
        if stats['mean'] > 100:
            print(f"\n   ✅ Confirmado: duration_est_imputed está en HORAS")
            print(f"   → En duration_model.py ya convertimos días a horas (×24)")
        else:
            print(f"\n   ℹ️  duration_est_imputed está en DÍAS")
            print(f"   → NO multipliques por 24 en duration_model.py")
    
    engine.dispose()
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    print(f"\n💡 Verifica:")
    print(f"   1. ¿Existe la vista v_training_dataset_clean en {DB}?")
    print(f"   2. ¿Las credenciales son correctas?")
    print(f"   3. ¿La BD es 'sb' o 'sb_production'?")
