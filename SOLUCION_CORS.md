# 🔧 Solución al Error CORS - Process Mining

## ❌ Error Original
```
Access to fetch at 'http://127.0.0.1:5000/api/ml/process-mining/analyze' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

## ✅ Cambios Realizados

### 1. **Backend Corregido**
- ✅ Agregado `import traceback` para mejor logging
- ✅ Agregado manejo de OPTIONS para CORS preflight
- ✅ **CAMBIADO:** Usar tabla `tasks` en lugar de `web_tasks`
- ✅ **CAMBIADO:** Usar tabla `task_dependencies` en lugar de `web_task_dependencies`
- ✅ Agregados prints de debug para ver qué pasa
- ✅ Manejo robusto de errores con mensajes claros

### 2. **Archivos Modificados**
```
backend/app/routes/process_mining_routes.py  ✅ Actualizado
backend/test_process_mining.py              ✅ Script de diagnóstico creado
```

---

## 🚀 Pasos para Probar

### **1. Diagnosticar el Problema**
```bash
cd backend
python test_process_mining.py
```

Este script te dirá:
- ✅ Si MySQL está conectado
- ✅ Si la tabla `tasks` existe y tiene datos
- ✅ Si el modelo PKL está en su lugar

### **2. Reiniciar el Backend Flask**

**Si está corriendo, detén el servidor (Ctrl+C) y vuelve a iniciarlo:**
```bash
cd backend
python app.py
```

Deberías ver:
```
    ╔═══════════════════════════════════════════════════╗
    ║   🚀 BACKEND FLASK - SISTEMA DE PRODUCTIVIDAD   ║
    ║                                                   ║
    ║   Entorno: DEVELOPMENT                           ║
    ║   Puerto:  5000                                  ║
    ╚═══════════════════════════════════════════════════╝

✅ Blueprints registrados correctamente
 * Running on http://0.0.0.0:5000
```

### **3. Probar desde el Frontend**

1. Ir a: `http://localhost:5173/proceso`
2. Click en **"Analizar Cuellos de Botella"**
3. **Revisar la consola del backend** (donde corre `python app.py`)

Deberías ver:
```
🔍 Iniciando análisis de bottlenecks (project_id=None)...
   📊 Ejecutando query SQL en tabla 'tasks'...
   ✅ Query ejecutada: 150 registros obtenidos
   🤖 Ejecutando predicción con modelo CatBoost...
   ✅ Predicción completada
   🚧 Bottlenecks detectados: 23
   📦 Preparando respuesta JSON...
   ✅ Análisis completado exitosamente
```

---

## 🐛 Solución de Problemas

### **Problema 1: "No hay datos en tabla 'tasks'"**

**Causa:** La tabla está vacía

**Solución:** Insertar datos de prueba o verificar que tienes tareas en la BD:
```sql
SELECT COUNT(*) FROM tasks;
```

---

### **Problema 2: "Tabla tasks no existe"**

**Causa:** Base de datos incorrecta

**Solución:** Verificar en `backend/.env` o variables de entorno:
```env
MYSQL_DB=sb_production   # ← ¿Es la BD correcta?
```

---

### **Problema 3: "Error al cargar modelo"**

**Causa:** Modelo PKL no está donde debe

**Solución:** Verificar que existe:
```bash
ls -l backend/ml/models/mining/model_bottleneck_corregido.pkl
```

Si no existe, copiarlo desde artifacts:
```bash
cp backend/ml/models/training/artifacts/modelo5_corregido/model_bottleneck_corregido.pkl \
   backend/ml/models/mining/
```

---

### **Problema 4: CORS sigue fallando**

**Causa:** Backend no está corriendo o puerto incorrecto

**Solución:** 
1. Verificar que Flask corra en puerto 5000
2. Verificar que frontend apunte a `http://127.0.0.1:5000` en `api.ts`

---

## 📊 Logs Esperados (Backend)

Cuando funcione correctamente verás en la terminal del backend:

```bash
127.0.0.1 - - [24/Dec/2025 14:30:22] "OPTIONS /api/ml/process-mining/analyze HTTP/1.1" 200 -

🔍 Iniciando análisis de bottlenecks (project_id=None)...
   📊 Ejecutando query SQL en tabla 'tasks'...
   ✅ Query ejecutada: 234 registros obtenidos
   🔗 Dependencias cargadas: 156 edges
   🤖 Ejecutando predicción con modelo CatBoost...
✓ Modelo bottleneck cargado: D:\proyecto-innovacion\backend\ml\models\mining\model_bottleneck_corregido.pkl
   ✅ Predicción completada
   🚧 Bottlenecks detectados: 34
   📦 Preparando respuesta JSON...
   ✅ Análisis completado exitosamente

127.0.0.1 - - [24/Dec/2025 14:30:25] "GET /api/ml/process-mining/analyze HTTP/1.1" 200 -
```

---

## ✅ Checklist de Verificación

Antes de probar, verifica:

- [ ] Backend Flask corriendo en puerto 5000
- [ ] Frontend dev server corriendo en puerto 5173
- [ ] MySQL corriendo y accesible
- [ ] Tabla `tasks` existe y tiene datos
- [ ] Modelo PKL en `backend/ml/models/mining/`
- [ ] Variables de entorno configuradas (`.env`)

---

## 🎯 Resultado Esperado

Si todo funciona, en el frontend verás:

```
✅ Accuracy: 99.9%
✅ Bottlenecks Detectados: 34

Tabla con lista de cuellos de botella
```

---

## 📝 Notas Importantes

1. **Tabla Cambiada:** Ahora usa `tasks` en lugar de `web_tasks`
2. **Columnas Mapeadas:**
   - `web_tasks.id` → `tasks.task_id`
   - `web_tasks.title` → `tasks.task_name`
   - `web_tasks.estimated_hours` → `tasks.duration_est` (en días)

3. **CORS:** Ya está configurado en `extensions.py` para permitir todos los orígenes

---

## 🆘 Si Nada Funciona

Ejecuta este comando para ver el error exacto:
```bash
cd backend
python -c "from app.routes.process_mining_routes import process_mining_bp; print('✅ OK')"
```

Si sale error, copia el traceback y analízalo.
