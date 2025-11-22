# Backend - Sistema de Análisis de Productividad con Machine Learning

Backend profesional en Flask para análisis de productividad con predicciones ML.

## 📋 Características

- ✅ **Autenticación JWT** con registro y login seguro
- ✅ **CRUD completo de tareas** con paginación y filtros
- ✅ **5 Endpoints de Machine Learning**:
  1. Predicción de riesgo de tareas
  2. Estimación de duración real
  3. Recomendación de personas para tareas
  4. Predicción de desempeño
  5. Minería de procesos (process mining)
- ✅ **Base de datos MySQL** con SQLAlchemy ORM
- ✅ **Migraciones** con Flask-Migrate
- ✅ **CORS configurado** para integración con frontend
- ✅ **Estructura modular** lista para producción

## 🗂️ Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py              # Factory pattern de Flask
│   ├── extensions.py            # Inicialización de extensiones
│   ├── models/                  # Modelos de base de datos
│   │   ├── __init__.py
│   │   ├── user.py             # Modelo de usuarios con auth
│   │   ├── person.py           # Modelo de personas/empleados
│   │   └── task.py             # Tareas, asignaciones y dependencias
│   ├── routes/                  # Blueprints de rutas
│   │   ├── __init__.py
│   │   ├── auth_routes.py      # Autenticación (login, register)
│   │   ├── task_routes.py      # CRUD de tareas
│   │   └── ml_routes.py        # Endpoints de ML
│   └── ml/                      # Módulos de Machine Learning
│       ├── __init__.py
│       ├── risk_model.py       # Predicción de riesgo
│       ├── duration_model.py   # Predicción de duración
│       ├── recommender_model.py # Recomendación de personas
│       ├── performance_model.py # Predicción de desempeño
│       └── process_mining.py   # Análisis de procesos
├── models/                      # Archivos .pkl de modelos ML (crear aquí)
├── migrations/                  # Migraciones de base de datos
├── config.py                    # Configuración por entornos
├── app.py                       # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias de Python
├── .env.example                # Ejemplo de variables de entorno
├── .gitignore                  # Archivos a ignorar en Git
└── README.md                   # Este archivo
```

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

- Python 3.8+
- MySQL Server
- pip (gestor de paquetes de Python)

### 2. Clonar o Navegar al Proyecto

```powershell
cd d:\proyecto-innovacion\backend
```

### 3. Crear Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay error de políticas de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```powershell
Copy-Item .env.example .env
```

Editar `.env` con tus credenciales:

```env
# Configuración de Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion

# Configuración de Base de Datos MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=sb

# JWT
JWT_SECRET_KEY=otra-clave-secreta-para-jwt-cambiar-en-produccion

# CORS (dominios permitidos)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Modelos ML
MODELS_PATH=models
```

### 6. Configurar Base de Datos

#### Opción A: Usar base de datos existente

Si ya tienes la base de datos `sb` creada con el archivo `sb.sql`:

```powershell
# Importar el archivo SQL a MySQL
mysql -u root -p sb < ../sb.sql
```

#### Opción B: Crear desde cero con migraciones

```powershell
# Inicializar migraciones
flask db init

# Crear primera migración
flask db migrate -m "Initial migration"

# Aplicar migración
flask db upgrade
```

### 7. Crear Usuario Administrador (Opcional)

Abrir Python interactivo:

```powershell
python
```

```python
from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Usuario admin creado!')
```

Salir con `exit()`.

### 8. Ejecutar Servidor de Desarrollo

```powershell
python app.py
```

El servidor estará disponible en: **http://localhost:5000**

## 📡 API Endpoints

### Autenticación (`/api/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Registrar nuevo usuario | No |
| POST | `/api/auth/login` | Iniciar sesión | No |
| GET | `/api/auth/me` | Obtener usuario actual | Sí |
| PUT | `/api/auth/change-password` | Cambiar contraseña | Sí |
| GET | `/api/auth/users` | Listar usuarios (admin) | Sí |

### Tareas (`/api/tasks`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/tasks/` | Listar tareas (paginado) | Sí |
| GET | `/api/tasks/<id>` | Obtener tarea por ID | Sí |
| POST | `/api/tasks/` | Crear nueva tarea | Sí |
| PUT | `/api/tasks/<id>` | Actualizar tarea | Sí |
| DELETE | `/api/tasks/<id>` | Eliminar tarea | Sí |
| POST | `/api/tasks/<id>/assignees` | Asignar persona | Sí |
| DELETE | `/api/tasks/<id>/assignees/<person_id>` | Remover asignación | Sí |
| GET | `/api/tasks/stats` | Estadísticas generales | Sí |

### Machine Learning (`/api/ml`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/ml/prediccion-riesgo` | Predecir riesgo de tarea | Sí |
| POST | `/api/ml/tiempo-real` | Predecir duración real | Sí |
| POST | `/api/ml/recomendar-persona` | Recomendar persona para tarea | Sí |
| POST | `/api/ml/desempeno` | Predecir desempeño | Sí |
| POST | `/api/ml/proceso` | Análisis de minería de procesos | Sí |
| GET | `/api/ml/health` | Estado de modelos ML | No |

### Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Estado del servidor |

## 🔐 Autenticación

La API usa **JWT (JSON Web Tokens)**. Para endpoints protegidos:

1. Hacer login en `/api/auth/login`
2. Obtener el `access_token` de la respuesta
3. Incluir en headers: `Authorization: Bearer <access_token>`

### Ejemplo con cURL

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Usar token
curl -X GET http://localhost:5000/api/tasks/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbG..."
```

## 🤖 Modelos de Machine Learning

Los modelos ML se cargan automáticamente desde la carpeta `models/`. Si no existen archivos `.pkl`, los endpoints usan **lógica heurística** como fallback.

### Archivos de Modelos Esperados

```
models/
├── risk_model.pkl              # Modelo de predicción de riesgo
├── risk_encoders.pkl           # Label encoders para riesgo
├── duration_model.pkl          # Modelo de duración
├── duration_scaler.pkl         # Scaler para duración
├── recommender_model.pkl       # Modelo de recomendación
├── performance_model.pkl       # Modelo de desempeño
└── process_mining.pkl          # Analizador de procesos
```

### Entrenar Modelos (Ejemplo)

```python
import joblib
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Entrenar modelo de riesgo (ejemplo básico)
X_train = pd.DataFrame(...)  # Features
y_train = pd.Series(...)     # Labels

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Guardar modelo
joblib.dump(model, 'models/risk_model.pkl')
```

## 🔧 Configuración para Producción

### 1. Variables de Entorno

```env
FLASK_ENV=production
SECRET_KEY=clave-super-secreta-genera-con-secrets.token_hex(32)
JWT_SECRET_KEY=otra-clave-diferente-para-jwt

DB_HOST=tu-servidor-mysql.com
DB_USER=usuario_produccion
DB_PASSWORD=password-segura-produccion
```

### 2. Ejecutar con Gunicorn

```powershell
# Instalar gunicorn (ya en requirements.txt)
pip install gunicorn

# Ejecutar servidor
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. HTTPS con Nginx

Configurar Nginx como reverse proxy:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Supervisor (mantener proceso activo)

```ini
[program:flask-backend]
command=/ruta/a/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
directory=/ruta/a/backend
user=tu-usuario
autostart=true
autorestart=true
```

## 🧪 Testing

```powershell
# Ejecutar health check
curl http://localhost:5000/health

# Verificar modelos ML
curl http://localhost:5000/api/ml/health
```

## 📊 Migraciones de Base de Datos

```powershell
# Crear nueva migración después de cambios en modelos
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir última migración
flask db downgrade
```

## 🛠️ Troubleshooting

### Error: "No module named 'flask_jwt_extended'"

```powershell
pip install flask-jwt-extended
```

### Error: "Access denied for user"

Verificar credenciales en `.env` y que MySQL esté corriendo.

### Error: "Can't connect to MySQL server"

```powershell
# Iniciar MySQL
net start MySQL80

# O en XAMPP
# Iniciar desde el panel de control
```

### Warning de importación en VSCode

Los warnings de `pylance` sobre imports son normales si las dependencias están instaladas. Ejecutar:

```powershell
pip list | Select-String flask
```

## 📚 Tecnologías Utilizadas

- **Flask 3.0.0** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **Flask-Migrate** - Migraciones de BD
- **Flask-JWT-Extended** - Autenticación JWT
- **Flask-CORS** - Cross-Origin Resource Sharing
- **PyMySQL** - Conector MySQL
- **scikit-learn** - Machine Learning
- **pandas & numpy** - Procesamiento de datos
- **CatBoost** - Gradient boosting ML
- **joblib** - Serialización de modelos

## 👨‍💻 Desarrollo

### Añadir Nueva Ruta

1. Crear archivo en `app/routes/`
2. Definir Blueprint
3. Registrar en `app/routes/__init__.py`

```python
# app/routes/nueva_ruta.py
from flask import Blueprint

nueva_bp = Blueprint('nueva', __name__)

@nueva_bp.route('/test')
def test():
    return {'message': 'Hola'}
```

```python
# app/routes/__init__.py
from app.routes.nueva_ruta import nueva_bp

def register_blueprints(app):
    # ... blueprints existentes
    app.register_blueprint(nueva_bp, url_prefix='/api/nueva')
```

### Añadir Nuevo Modelo

1. Crear archivo en `app/models/`
2. Definir clase heredando de `db.Model`
3. Exportar en `app/models/__init__.py`
4. Crear migración

```python
# app/models/nuevo_modelo.py
from app.extensions import db

class NuevoModelo(db.Model):
    __tablename__ = 'nueva_tabla'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
```

```powershell
flask db migrate -m "Añadir NuevoModelo"
flask db upgrade
```

## 📄 Licencia

Este proyecto es privado y confidencial.

## 📞 Soporte

Para soporte técnico, contactar al equipo de desarrollo.

---

**Desarrollado con ❤️ para análisis de productividad**
