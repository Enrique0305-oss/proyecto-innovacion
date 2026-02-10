/**
 * Control de Acceso por Rol - Frontend
 * ======================================
 * Funciones para mostrar/ocultar elementos según permisos del usuario
 */

// Obtener permisos del usuario desde localStorage
export function getUserPermissions() {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  
  try {
    const user = JSON.parse(userStr);
    return {
      role_id: user.role_id,
      permissions: user.permissions || {},
      area: user.area,
      accessible_areas: user.accessible_areas
    };
  } catch (e) {
    console.error('Error parseando permisos:', e);
    return null;
  }
}

// Verificar si el usuario tiene un permiso específico
export function hasPermission(permissionName: string): boolean {
  const userPerms = getUserPermissions();
  if (!userPerms) return false;
  
  return userPerms.permissions[permissionName] === true;
}

// Verificar si el usuario tiene uno de varios permisos
export function hasAnyPermission(...permissionNames: string[]): boolean {
  return permissionNames.some(perm => hasPermission(perm));
}

// Verificar si el usuario tiene un rol específico
export function hasRole(...roleIds: number[]): boolean {
  const userPerms = getUserPermissions();
  if (!userPerms) return false;
  
  return roleIds.includes(userPerms.role_id);
}

// Verificar si el usuario está restringido por área
export function isAreaRestricted(): boolean {
  return hasPermission('area_restricted');
}

// Obtener rol del usuario
export function getUserRole(): number | null {
  const userPerms = getUserPermissions();
  return userPerms ? userPerms.role_id : null;
}

// Mostrar/ocultar elemento según permisos
export function toggleElementByPermission(
  elementId: string, 
  permissionName: string
): void {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  if (hasPermission(permissionName)) {
    element.style.display = '';
  } else {
    element.style.display = 'none';
  }
}

// Mostrar/ocultar elemento según rol
export function toggleElementByRole(
  elementId: string,
  ...allowedRoles: number[]
): void {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  if (hasRole(...allowedRoles)) {
    element.style.display = '';
  } else {
    element.style.display = 'none';
  }
}

// Mostrar/ocultar elementos con clase según permiso
export function toggleClassByPermission(
  className: string,
  permissionName: string
): void {
  const elements = document.querySelectorAll(`.${className}`);
  const shouldShow = hasPermission(permissionName);
  
  elements.forEach(el => {
    (el as HTMLElement).style.display = shouldShow ? '' : 'none';
  });
}

// Definición de módulos y sus permisos requeridos
export const MODULE_PERMISSIONS = {
  'dashboard': null,  // Todos
  'tareas': null,  // Todos
  'riesgo': 'access_ml_models',
  'duracion': 'access_ml_models',
  'recomendacion': 'access_ml_models',
  'asignacion': 'access_ml_models',
  'desempeno': 'access_ml_models',
  'flujo': 'access_ml_models',
  'usuarios': 'manage_users',
  'areas': 'view_all_areas',
  'configuracion': 'system_config'
};

// Verificar si puede acceder a un módulo
export function canAccessModule(moduleName: string): boolean {
  const requiredPermission = MODULE_PERMISSIONS[moduleName as keyof typeof MODULE_PERMISSIONS];
  
  // Si no requiere permiso especial, todos pueden acceder
  if (!requiredPermission) return true;
  
  return hasPermission(requiredPermission);
}

// Obtener nombre del rol en español
export function getRoleName(roleId: number): string {
  const roleNames: { [key: number]: string } = {
    1: 'Super Admin',
    2: 'Gerente General',
    3: 'Supervisor General',
    4: 'Colaborador',
    5: 'Supervisor de Área'
  };
  
  return roleNames[roleId] || 'Desconocido';
}

// Obtener badge HTML del rol
export function getRoleBadge(roleId: number): string {
  const roleBadges: { [key: number]: string } = {
    1: '<span class="role-badge role-super-admin">Super Admin</span>',
    2: '<span class="role-badge role-gerente">Gerente General</span>',
    3: '<span class="role-badge role-supervisor">Supervisor General</span>',
    4: '<span class="role-badge role-colaborador">Colaborador</span>',
    5: '<span class="role-badge role-supervisor-area">Supervisor de Área</span>'
  };
  
  return roleBadges[roleId] || '<span class="role-badge">-</span>';
}
