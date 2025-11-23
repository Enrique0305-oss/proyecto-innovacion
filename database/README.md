# 📊 Scripts de Base de Datos - Sistema Processmart

Scripts SQL para configurar la arquitectura de bases de datos del proyecto de tesina.

## 🎯 Arquitectura

El sistema utiliza **2 bases de datos separadas**:

```
┌─────────────────────────────────────┐
│  sb_production                      │
│  (Sistema Web - Producción)         │
│  ✓ Tareas operacionales             │
│  ✓ Usuarios del sistema             │
│  ✓ Predicciones ML                  │
│  ✓ Gestión de modelos               │
│  Estado: Vacía inicialmente         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  sb_training                        │
│  (Machine Learning - Training)      │
│  ✓ 100,000 registros de people      │
│  ✓ 1,758 tareas históricas          │
│  ✓ Assignees y dependencias         │
│  ✓ Vistas para datasets             │
│  Estado: Con datos históricos       │
└─────────────────────────────────────┘
```

## 📋 Scripts Disponibles

### 1️⃣ `01_create_sb_production.sql`

**Crea la base de datos de producción** (sistema web)

**Tablas creadas:**
- **Estructura base**: `people`, `tasks`, `assignees`, `task_dependencies`
- **Sistema web**: `areas`, `web_users`, `web_tasks`
- **Machine Learning**: `ml_models`, `ml_predictions`, `ml_datasets`, `ml_training_jobs`

**Vistas creadas:**
- `v_area_metrics` - Métricas por área
- `v_top_performers` - Top colaboradores
- `v_delayed_tasks` - Tareas con retraso
- `v_ml_prediction_accuracy` - Precisión de predicciones
- `v_training_status` - Estado de entrenamientos

**Datos iniciales:**
- 8 áreas base (IT, Engineering, HR, etc.)
- 3 usuarios web (admin, supervisor, analyst)
- 5 modelos ML registrados

**Ejecutar:**
```bash
# Desde MySQL CLI
mysql -u root -p < 01_create_sb_production.sql

# Desde phpMyAdmin
# Copiar y pegar el contenido en la pestaña SQL
```

---

### 2️⃣ `02_rename_sb_to_training.sql`

**Renombra/migra la BD actual `sb` a `sb_training`**

**Métodos disponibles:**

**Opción A - Dump y Restauración (MÁS SEGURO):**
```bash
# 1. Backup
mysqldump -u root -p sb > sb_backup.sql

# 2. Crear y restaurar
mysql -u root -p -e "CREATE DATABASE sb_training CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
mysql -u root -p sb_training < sb_backup.sql

# 3. Verificar
mysql -u root -p sb_training -e "SELECT COUNT(*) FROM people;"

# 4. Opcional: eliminar sb
mysql -u root -p -e "DROP DATABASE sb;"
```

**Opción B - Renombrado tabla por tabla:**
```sql
RENAME TABLE sb.assignees TO sb_training.assignees;
RENAME TABLE sb.people TO sb_training.people;
-- etc...
```

---

## 🚀 Instalación Paso a Paso

### Prerequisitos

- MySQL 8.0+
- Acceso root o usuario con permisos CREATE DATABASE
- BD `sb` existente con datos

### Pasos de Instalación

```bash
# 1. Crear carpeta database si no existe
cd d:\proyecto-innovacion
mkdir database  # si no existe

# 2. Hacer BACKUP de seguridad (CRÍTICO)
mysqldump -u root -p sb > d:\proyecto-innovacion\database\sb_backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql

# 3. Crear sb_production
mysql -u root -p < database\01_create_sb_production.sql

# 4. Migrar sb a sb_training (elige método del script 02)
# Método dump (recomendado):
mysql -u root -p -e "CREATE DATABASE sb_training CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
mysql -u root -p sb_training < d:\proyecto-innovacion\database\sb_backup_*.sql

# 5. Verificar
mysql -u root -p
```

```sql
-- Verificar sb_production
USE sb_production;
SHOW TABLES;
SELECT * FROM web_users;
SELECT * FROM ml_models;

-- Verificar sb_training
USE sb_training;
SELECT COUNT(*) FROM people;    -- Debe mostrar ~100,000
SELECT COUNT(*) FROM tasks;     -- Debe mostrar ~1,758
SELECT COUNT(*) FROM assignees; -- Debe mostrar miles

-- Ver ambas BDs
SHOW DATABASES LIKE 'sb%';
```

---

## 📊 Estructura de Tablas

### sb_production

#### Tablas de Sistema Web
| Tabla | Registros Iniciales | Descripción |
|-------|---------------------|-------------|
| `areas` | 8 | Departamentos/Áreas |
| `web_users` | 3 | Usuarios admin/supervisores |
| `web_tasks` | 0 | Tareas operacionales |

#### Tablas Machine Learning
| Tabla | Registros Iniciales | Descripción |
|-------|---------------------|-------------|
| `ml_models` | 5 | Modelos registrados |
| `ml_predictions` | 0 | Predicciones generadas |
| `ml_datasets` | 0 | Datasets subidos |
| `ml_training_jobs` | 0 | Jobs de entrenamiento |

#### Tablas de Estructura
| Tabla | Registros Iniciales | Descripción |
|-------|---------------------|-------------|
| `people` | 0 | Colaboradores (vacía) |
| `tasks` | 0 | Tareas históricas (vacía) |
| `assignees` | 0 | Asignaciones (vacía) |

---

### sb_training

| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| `people` | ~100,000 | Colaboradores históricos |
| `tasks` | ~1,758 | Tareas completadas |
| `assignees` | Miles | Asignaciones históricas |
| `v_training_dataset` | Vista | Dataset limpio para ML |
| `v_training_dataset_clean` | Vista | Dataset procesado |

---

## 🔧 Configuración Flask

### config.py

```python
import os

class Config:
    # BD Principal: Producción
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/sb_production'
    )
    
    # BD Secundaria: Training
    SQLALCHEMY_BINDS = {
        'training': 'mysql+pymysql://root:password@localhost/sb_training'
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Log de queries (dev only)
```

### Modelos

```python
# backend/app/models/person.py
from app.extensions import db

# Modelo para producción
class Person(db.Model):
    __tablename__ = 'people'
    # __bind_key__ no se especifica = usa BD principal
    person_id = db.Column(db.String(64), primary_key=True)
    area = db.Column(db.String(64))
    # ...

# Modelo para training
class PersonTraining(db.Model):
    __tablename__ = 'people'
    __bind_key__ = 'training'  # Usa sb_training
    person_id = db.Column(db.String(64), primary_key=True)
    # ...

# Uso en rutas
from app.models.person import Person, PersonTraining

@app.route('/api/people/production')
def get_production_people():
    # Lee de sb_production.people
    people = Person.query.all()
    return jsonify([p.to_dict() for p in people])

@app.route('/api/people/training')
def get_training_people():
    # Lee de sb_training.people
    people = PersonTraining.query.all()
    return jsonify([p.to_dict() for p in people])
```

---

## 🧪 Testing

### Verificar conexiones

```python
# backend/test_db_connections.py
from app import create_app, db
from app.models.person import Person, PersonTraining

app = create_app()

with app.app_context():
    # Test producción
    prod_count = Person.query.count()
    print(f"sb_production.people: {prod_count} registros")
    
    # Test training
    train_count = PersonTraining.query.count()
    print(f"sb_training.people: {train_count} registros")
    
    # Verificar BDs
    print("\n✅ Conexiones OK" if train_count > 1000 else "❌ Error en datos")
```

---

## 📝 Notas Importantes

### Credenciales por defecto

**⚠️ CAMBIAR EN PRODUCCIÓN:**

```sql
-- Usuario: admin@processmart.com
-- Password: admin123
-- Hash bcrypt: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zq.a06VMl6u6
```

### Backup antes de ejecutar

```bash
# Backup completo de sb
mysqldump -u root -p sb > backup_sb_$(Get-Date -Format "yyyyMMdd").sql

# Backup solo estructura
mysqldump -u root -p --no-data sb > backup_sb_structure.sql

# Backup solo datos
mysqldump -u root -p --no-create-info sb > backup_sb_data.sql
```

### Restauración de emergencia

```bash
# Si algo sale mal, restaurar desde backup
mysql -u root -p -e "DROP DATABASE sb;"
mysql -u root -p -e "CREATE DATABASE sb CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
mysql -u root -p sb < backup_sb_YYYYMMDD.sql
```

---

## 🎓 Para la Tesina

### Ventajas de esta arquitectura

1. **Separación de responsabilidades**
   - Producción: Sistema operacional
   - Training: Análisis y ML

2. **Seguridad de datos**
   - Training data protegida
   - No se modifica accidentalmente

3. **Escalabilidad**
   - Posible mover a servidores diferentes
   - Backups independientes

4. **Auditoría completa**
   - Tracking de predicciones
   - Versionado de modelos
   - Historial de entrenamientos

### Diagrama para documento

```
┌────────────────────────┐
│   Frontend (Vite+TS)   │
│   sistema-productivo/  │
└───────────┬────────────┘
            │ HTTP Requests
            ▼
┌────────────────────────┐
│   Backend (Flask)      │
│   ├── SQLAlchemy       │
│   ├── ML Models (.pkl) │
│   └── API Routes       │
└─────┬──────────┬───────┘
      │          │
      ▼          ▼
┌────────────┐ ┌────────────┐
│sb_production│ │sb_training │
│(Sistema Web)│ │(ML Train)  │
│  8 tablas   │ │100K records│
└────────────┘ └────────────┘
```

---

## 🆘 Troubleshooting

### Error: "Database already exists"

```sql
-- Eliminar si existe
DROP DATABASE IF EXISTS sb_production;
-- Luego ejecutar script 01
```

### Error: "Access denied"

```bash
# Dar permisos al usuario
mysql -u root -p
GRANT ALL PRIVILEGES ON sb_production.* TO 'tu_usuario'@'localhost';
GRANT ALL PRIVILEGES ON sb_training.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Table doesn't exist"

```sql
-- Verificar en qué BD estás
SELECT DATABASE();

-- Cambiar a la correcta
USE sb_production;
SHOW TABLES;
```

---

## 📞 Soporte

Para problemas con los scripts:
1. Verificar versión MySQL: `mysql --version` (debe ser 8.0+)
2. Revisar logs de MySQL
3. Ejecutar scripts paso a paso en lugar de completo
4. Verificar permisos del usuario MySQL

---

**Última actualización:** 2025-11-23
**Autor:** Sistema Processmart - Proyecto Tesina
