# 🎭 Guía Rápida de Roles - Sistema de Productividad

## 🚀 Inicio Rápido

### Reiniciar Base de Datos con Nuevos Roles

```bash
# En el directorio backend/
python init_database.py
```

Esto creará los 4 roles nuevos y usuarios de prueba.

---

## 👥 Usuarios de Prueba

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| **Admin TI** | admin@processmart.com | admin123 | super_admin |
| **Gerente** | gerente@processmart.com | gerente123 | gerente |
| **Supervisor** | supervisor@processmart.com | supervisor123 | supervisor |
| **Colaborador** | usuario@processmart.com | usuario123 | colaborador |

---

## 🎯 Permisos por Módulo

### 📊 Dashboard

| Rol | Dashboard Global | Dashboard Área | Dashboard Personal |
|-----|------------------|----------------|--------------------|
| Super Admin | ✅ | ✅ | ✅ |
| Gerente | ✅ | ✅ | ❌ |
| Supervisor | ❌ | ✅ | ✅ |
| Colaborador | ❌ | ❌ | ✅ |

### 👥 Gestión de Usuarios

| Rol | Ver | Crear | Editar | Eliminar |
|-----|-----|-------|--------|----------|
| Super Admin | ✅ | ✅ | ✅ | ✅ |
| Gerente | ✅ | ❌ | ❌ | ❌ |
| Supervisor | ✅ | ❌ | ❌ | ❌ |
| Colaborador | ❌ | ❌ | ❌ | ❌ |

**Interfaz:**
- **Super Admin**: Ve botones "Nuevo Usuario", "Editar" y "Eliminar"
- **Otros roles**: Solo ven la tabla (o no tienen acceso al módulo)

### 🏢 Gestión de Áreas

| Rol | Ver | Crear | Editar | Eliminar |
|-----|-----|-------|--------|----------|
| Super Admin | ✅ | ✅ | ✅ | ✅ |
| Gerente | ✅ | ❌ | ❌ | ❌ |
| Supervisor | ✅ | ❌ | ❌ | ❌ |
| Colaborador | ✅ | ❌ | ❌ | ❌ |

**Interfaz:**
- **Super Admin**: Ve botones "Nueva Área", "Editar" y "Eliminar"
- **Otros roles**: Solo ven las tarjetas de áreas (sin botones de acción)

### 📋 Gestión de Tareas

| Rol | Ver Todas | Crear | Editar Completo | Solo Cambiar Estado |
|-----|-----------|-------|-----------------|---------------------|
| Super Admin | ✅ | ✅ | ✅ | ✅ |
| Gerente | ✅ | ✅ | ✅ | ✅ |
| Supervisor | ✅ | ✅ | ✅ | ✅ |
| Colaborador | ✅ | ❌ | ❌ | ✅ |

**Interfaz:**
- **Super Admin/Gerente/Supervisor**: Botón "Editar" completo con todos los campos
- **Colaborador**: Selector dropdown para cambiar solo el estado

**Campos Editables por Rol:**

**Super Admin, Gerente, Supervisor:**
- Título ✅
- Área ✅
- Descripción ✅
- Tiempo estimado ✅
- Responsable ✅
- Estado ✅
- Prioridad ✅

**Colaborador:**
- Estado ✅ (con transiciones limitadas)
- Todos los demás ❌

### 📈 Reportes y Exportación

| Rol | Ver Reportes | Exportar PDF | Exportar Excel |
|-----|--------------|--------------|----------------|
| Super Admin | ✅ Todo | ✅ | ✅ |
| Gerente | ✅ Todo | ✅ | ✅ |
| Supervisor | ✅ Su área | ✅ | ✅ |
| Colaborador | ❌ | ❌ | ❌ |

### 🤖 Inteligencia Artificial

| Rol | Ver Predicciones | Entrenar Modelos | Configurar IA |
|-----|------------------|------------------|---------------|
| Super Admin | ✅ | ✅ | ✅ |
| Gerente | ✅ | ❌ | ❌ |
| Supervisor | ✅ | ❌ | ❌ |
| Colaborador | ❌ | ❌ | ❌ |

---

## 🔄 Transiciones de Estado (Colaboradores)

Los colaboradores solo pueden cambiar estados siguiendo estas reglas:

```
Pendiente ──────┬──→ En Progreso
                └──→ Cancelada

En Progreso ────┬──→ Completada
                └──→ Cancelada

Retrasada ──────┬──→ En Progreso
                └──→ Cancelada

Completada ──────── ❌ (Sin cambios)

Cancelada ───────── ❌ (Sin cambios)
```

---

## 🎨 Diferencias Visuales por Rol

### Navegación Lateral (Sidebar)

**Super Admin:**
```
📊 Dashboard
👥 Usuarios         ⭐ Con gestión
🏢 Áreas            ⭐ Con gestión
📋 Tareas
📈 Reportes
🤖 IA               ⭐ Con configuración
⚙️ Configuración    ⭐ Exclusivo
```

**Gerente:**
```
📊 Dashboard        ⭐ Vista ejecutiva
👥 Usuarios         (solo lectura)
🏢 Áreas            (solo lectura)
📋 Tareas
📈 Reportes         ⭐ Completos
🤖 IA               (solo predicciones)
```

**Supervisor:**
```
📊 Dashboard        (solo su área)
👥 Usuarios         (de su área)
🏢 Áreas            (solo lectura)
📋 Tareas           (de su área)
📈 Reportes         (de su área)
🤖 IA               (predicciones)
```

**Colaborador:**
```
📋 Mis Tareas
📊 Mi Desempeño
```

---

## 🔐 Validaciones de Seguridad

### Backend (API)

Todos los endpoints críticos validan:

```python
# Ejemplo en user_routes.py
user_role = current_user.role.name
if user_role != 'super_admin':
    return jsonify({
        'error': 'Permiso denegado',
        'message': 'Solo el Administrador TI puede gestionar usuarios'
    }), 403
```

**Endpoints Protegidos:**
- `POST /api/users` - Solo super_admin
- `PUT /api/users/<id>` - Solo super_admin
- `DELETE /api/users/<id>` - Solo super_admin
- `POST /api/areas` - Solo super_admin
- `PUT /api/areas/<id>` - Solo super_admin
- `DELETE /api/areas/<id>` - Solo super_admin
- `PUT /api/tasks/<id>` - Colaborador solo puede cambiar `status`

### Frontend (UI)

Las interfaces se adaptan dinámicamente:

```typescript
// Ejemplo en Users.ts
function canManageUsers(): boolean {
  return getUserRole() === 'super_admin';
}

// En el HTML
${canManageUsers() ? `
  <button class="btn-primary" id="btnNewUser">Nuevo Usuario</button>
` : ''}
```

---

## 📝 Casos de Uso Reales

### Caso 1: Nuevo Empleado (Flujo Completo)

1. **RRHH notifica** → Nuevo empleado Juan Pérez, área Ventas
2. **Super Admin (tú)**:
   ```
   - Ir a "Usuarios"
   - Click "Nuevo Usuario"
   - Email: juan.perez@empresa.com
   - Nombre: Juan Pérez
   - Rol: Colaborador
   - Área: Ventas
   - Guardar
   ```
3. **Se envía email** con credenciales a Juan
4. **Juan inicia sesión** y ve solo sus tareas
5. **Supervisor de Ventas** puede asignarle tareas

### Caso 2: Revisión Ejecutiva (Gerente)

1. **Gerente inicia sesión** (gerente@processmart.com)
2. Ve **Dashboard Ejecutivo** con métricas globales
3. **No puede**:
   - Crear/editar usuarios ❌
   - Crear/editar áreas ❌
   - Cambiar configuraciones ❌
4. **Sí puede**:
   - Ver todas las tareas ✅
   - Exportar reportes PDF/Excel ✅
   - Ver predicciones IA ✅
   - Tomar decisiones estratégicas ✅

### Caso 3: Gestión de Área (Supervisor)

1. **Supervisor inicia sesión** (supervisor@processmart.com)
2. Ve **Dashboard de su área** (Ventas)
3. **Puede**:
   - Crear tareas para su equipo ✅
   - Editar tareas de su área ✅
   - Asignar responsables ✅
   - Ver desempeño de su equipo ✅
4. **No puede**:
   - Crear usuarios ❌
   - Ver/editar otras áreas ❌
   - Acceder a configuraciones ❌

### Caso 4: Trabajo Diario (Colaborador)

1. **Colaborador inicia sesión** (usuario@processmart.com)
2. Ve **solo sus tareas asignadas**
3. Click en tarea → Selector "Cambiar estado"
4. Selecciona "▶ Iniciar" → Confirma
5. Al terminar, selecciona "✓ Completar"
6. **No puede** editar otros campos de la tarea

---

## 🆘 Solución de Problemas

### "Permiso denegado" al crear usuario

**Causa**: No eres super_admin  
**Solución**: Iniciar sesión con admin@processmart.com

### No veo el botón "Nueva Área"

**Causa**: Tu rol no es super_admin  
**Solución**: Solo el Admin TI puede gestionar áreas

### No puedo editar tareas

**Causa 1**: Eres colaborador → Solo puedes cambiar estado  
**Causa 2**: La tarea no es de tu área (supervisor)  
**Solución**: Contacta al supervisor o admin

### "Solo lectura" en columna de acciones

**Causa**: Tu rol no tiene permisos de edición  
**Solución**: Esto es normal para gerentes/supervisores en módulo de usuarios

---

## 🔄 Migración de Roles Antiguos

Si tienes usuarios con roles antiguos (`admin`, `manager`, `analyst`, `user`):

```bash
# Ejecutar script de migración (próximamente)
python migrate_roles.py
```

O manualmente en la base de datos:

```sql
-- Actualizar roles antiguos a nuevos
UPDATE roles SET name = 'super_admin' WHERE name = 'admin';
UPDATE roles SET name = 'gerente' WHERE name = 'manager';
UPDATE roles SET name = 'supervisor' WHERE name = 'analyst';
UPDATE roles SET name = 'colaborador' WHERE name = 'user';
```

---

## 📞 Contacto y Soporte

- **Admin del Sistema**: admin@processmart.com
- **Documentación completa**: Ver `ROLE_BASED_ACCESS.md`
- **Issues técnicos**: Contactar al equipo de TI

---

## ✅ Checklist de Implementación

- [✅] Base de datos actualizada con 4 roles
- [✅] Backend con validaciones de permisos
- [✅] Frontend con renderizado condicional
- [✅] Usuarios de prueba creados
- [✅] Documentación completa
- [ ] Capacitación a usuarios
- [ ] Pruebas con roles reales
- [ ] Despliegue a producción

---

**Última actualización**: 29 de Noviembre de 2025  
**Versión del sistema**: 2.0 - Modelo de 4 Roles
