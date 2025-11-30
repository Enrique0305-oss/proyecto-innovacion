# Sistema de Control de Acceso Basado en Roles (RBAC)

## Descripción General

El sistema implementa un control de acceso basado en roles para la gestión de tareas, permitiendo diferentes niveles de permisos según el rol del usuario.

## Roles Disponibles

### 1. **Admin** (Administrador)
- **Permisos completos** sobre todas las funcionalidades
- Puede crear, leer, actualizar y eliminar cualquier tarea
- Puede modificar todos los campos de una tarea
- Acceso total a la interfaz de edición de tareas

### 2. **Supervisor**
- Permisos similares al administrador para gestión de tareas
- Puede editar todos los campos de las tareas
- Ideal para jefes de área o coordinadores de equipo

### 3. **Colaborador** (Usuario Regular)
- Permisos limitados de solo lectura y cambio de estado
- **NO puede editar** los campos principales de la tarea
- Solo puede cambiar el estado de las tareas siguiendo transiciones válidas
- Interfaz simplificada con selector de estado rápido

---

## Funcionalidades por Rol

### Administrador y Supervisor

#### Interfaz de Usuario
- Botón **"Ver detalles"** (ícono ojo) - Ver información completa de la tarea
- Botón **"Editar"** (ícono lápiz) - Abre modal de edición completa

#### Modal de Edición
Pueden modificar todos los campos:
- ✅ Título de la tarea
- ✅ Área asignada
- ✅ Descripción
- ✅ Tiempo estimado (días)
- ✅ Responsable asignado
- ✅ Estado (pendiente, en_progreso, completada, retrasada, cancelada)
- ✅ Prioridad (baja, media, alta)

### Colaborador

#### Interfaz de Usuario
- Botón **"Ver detalles"** (ícono ojo) - Ver información completa de la tarea
- **Selector de estado** (dropdown) - Cambio rápido de estado

#### Cambio de Estado
Solo puede cambiar el estado mediante un selector con opciones limitadas según el estado actual:

**Desde "Pendiente":**
- ▶ Iniciar → Cambia a "En Progreso"
- ✗ Cancelar → Cambia a "Cancelada"

**Desde "En Progreso":**
- ✓ Completar → Cambia a "Completada"
- ✗ Cancelar → Cambia a "Cancelada"

**Desde "Retrasada":**
- ▶ Reiniciar → Cambia a "En Progreso"
- ✗ Cancelar → Cambia a "Cancelada"

**Estados finales** (sin cambios permitidos):
- ❌ Completada - No se puede modificar
- ❌ Cancelada - No se puede modificar

---

## Validación Backend

### Endpoint: `PUT /api/tasks/<id>`

#### Para Colaboradores
```python
# Solo acepta el campo 'status'
{
  "status": "en_progreso"
}

# ❌ Rechazado con 403 Forbidden
{
  "title": "Nuevo título",
  "status": "en_progreso"
}
```

**Respuesta de error:**
```json
{
  "error": "Permiso denegado",
  "message": "Los colaboradores solo pueden cambiar el estado de las tareas"
}
```

#### Validación de Transiciones
El backend valida que las transiciones de estado sean válidas:

```python
valid_transitions = {
    'pendiente': ['en_progreso', 'cancelada'],
    'en_progreso': ['completada', 'cancelada'],
    'completada': [],
    'retrasada': ['en_progreso', 'cancelada'],
    'cancelada': []
}
```

**Respuesta si la transición es inválida:**
```json
{
  "error": "Transición de estado no válida",
  "message": "No se puede cambiar de 'completada' a 'pendiente'"
}
```

#### Para Admin/Supervisor
Todos los campos son editables sin restricciones:
```json
{
  "title": "Nueva tarea actualizada",
  "description": "Descripción modificada",
  "area": "Desarrollo",
  "status": "en_progreso",
  "priority": "alta",
  "estimated_hours": 40,
  "assigned_to": "developer@example.com"
}
```

---

## Implementación Frontend

### Detección de Rol
```typescript
function getUserRole(): string {
  const userStr = localStorage.getItem('user');
  if (!userStr) return 'colaborador';
  
  const user = JSON.parse(userStr);
  return user.role?.name || 'colaborador';
}

function canEditFullTask(): boolean {
  const role = getUserRole();
  return role === 'admin' || role === 'supervisor';
}
```

### Renderizado Condicional
```typescript
// En la tabla de tareas
${canEditFullTask() ? `
  <!-- Botón de editar completo -->
  <button class="btn-icon btn-edit-task">...</button>
` : `
  <!-- Selector de cambio rápido -->
  <select class="status-quick-change">
    <option value="">Cambiar estado</option>
    ...
  </select>
`}
```

### Modal de Edición
```typescript
// Campo de estado solo visible para admin/supervisor
const statusRow = document.getElementById('taskStatusRow');
if (statusRow && canEditFullTask()) {
  statusRow.style.display = 'flex';
}
```

---

## Flujo de Trabajo

### Usuario Admin/Supervisor
1. Ve la tabla de tareas con botón "Editar" en cada fila
2. Click en "Editar" → Se abre modal con todos los campos
3. Modifica cualquier campo necesario
4. Click en "Guardar" → Backend valida y actualiza
5. La tabla se recarga con los datos actualizados

### Usuario Colaborador
1. Ve la tabla de tareas con selector de estado en cada fila
2. Click en el selector → Ve opciones según el estado actual
3. Selecciona nueva opción (ej: "▶ Iniciar")
4. Aparece confirmación → Click "Aceptar"
5. Backend valida la transición y actualiza solo el estado
6. La tabla se recarga mostrando el nuevo estado

---

## Seguridad

### Frontend
- Oculta opciones de interfaz según el rol
- Previene acciones no autorizadas desde la UI
- Validación de permisos en tiempo de renderizado

### Backend
- **Autenticación obligatoria** con JWT (`@jwt_required()`)
- Valida el rol del usuario en cada petición
- Rechaza solicitudes no autorizadas con códigos HTTP apropiados:
  - `401` - No autenticado
  - `403` - Sin permisos
  - `400` - Transición inválida
- Validación de transiciones de estado
- Logging de acciones para auditoría

---

## Estilos CSS

### Selector de Cambio Rápido
```css
.status-quick-change {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
  min-width: 140px;
  cursor: pointer;
  transition: all 0.2s;
}

.status-quick-change:hover {
  border-color: var(--color-primary);
  background-color: var(--bg-secondary);
}
```

---

## Extensibilidad

Para agregar nuevos roles o permisos:

1. **Backend** - Modificar `task_routes.py`:
   ```python
   if user_role in ['admin', 'supervisor', 'nuevo_rol']:
       # Permisos completos
   ```

2. **Frontend** - Actualizar `Tasks.ts`:
   ```typescript
   function canEditFullTask(): boolean {
     const role = getUserRole();
     return ['admin', 'supervisor', 'nuevo_rol'].includes(role);
   }
   ```

3. **Base de datos** - Agregar nuevo rol en tabla `roles`:
   ```sql
   INSERT INTO roles (name, description) 
   VALUES ('nuevo_rol', 'Descripción del nuevo rol');
   ```

---

## Pruebas

### Casos de Prueba

1. **Login como Admin**
   - Verificar que se muestra botón "Editar"
   - Abrir modal y verificar todos los campos editables
   - Modificar múltiples campos y guardar

2. **Login como Colaborador**
   - Verificar que NO se muestra botón "Editar"
   - Verificar que aparece selector de estado
   - Intentar cambio de estado válido
   - Verificar mensaje de éxito

3. **Validación Backend**
   - Como colaborador, intentar enviar `PUT` con múltiples campos
   - Verificar respuesta 403
   - Intentar transición inválida de estado
   - Verificar respuesta 400

---

## Archivos Modificados

- `backend/app/routes/task_routes.py` - Validación de permisos y transiciones
- `sistema-productivo/src/pages/Tasks.ts` - Lógica de renderizado condicional
- `sistema-productivo/src/styles/tasks.css` - Estilos para selector de estado
- `sistema-productivo/src/utils/api.ts` - Ya soportaba actualizaciones parciales

---

## Notas Técnicas

- El rol se obtiene desde el token JWT decodificado y almacenado en `localStorage`
- Las validaciones frontend son para UX, la seguridad real está en el backend
- Todos los estados de tarea son manejados de forma consistente en ambos lados
- El sistema es fácilmente extensible para agregar más roles o permisos
