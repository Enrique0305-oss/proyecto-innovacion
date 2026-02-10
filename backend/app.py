"""
Punto de entrada de la aplicación Flask
Ejecuta el servidor en modo desarrollo o producción
"""
import os
from app import create_app
from config import get_config

# Crear la aplicación con la configuración apropiada
config = get_config()
app = create_app(config)


if __name__ == "__main__":
    # Configuración del servidor
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ╔═══════════════════════════════════════════════════╗
    ║    BACKEND FLASK - SISTEMA DE PRODUCTIVIDAD   ║
    ║                                                   ║
    ║   Entorno: {os.getenv('FLASK_ENV', 'development').upper():<38} ║
    ║   Puerto:  {port:<38}  ║
    ║   Debug:   {str(debug):<38} ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    app.run(
        host='0.0.0.0',  # Permite conexiones externas (importante para VM)
        port=port,
        debug=debug,
        threaded=True
    )
