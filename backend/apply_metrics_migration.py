"""
Ejecutar script SQL para agregar métricas a web_users
"""
import subprocess
import sys

sql_file = r"D:\proyecto-innovacion\database\04_add_person_metrics_to_web_users.sql"

print("🔧 Ejecutando script SQL...")
print(f"   Archivo: {sql_file}\n")

try:
    result = subprocess.run(
        ['mysql', '-u', 'root', '-p123456'],
        stdin=open(sql_file, 'r', encoding='utf-8'),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Script ejecutado correctamente\n")
        print(result.stdout)
    else:
        print("❌ Error al ejecutar script\n")
        print(result.stderr)
        sys.exit(1)
        
except FileNotFoundError:
    print("❌ MySQL no encontrado en PATH")
    print("   Ejecuta manualmente en MySQL:")
    print(f"   SOURCE {sql_file};")
    sys.exit(1)

print("\n✅ Columnas agregadas a web_users")
print("   Reinicia el servidor Flask: python app.py")
