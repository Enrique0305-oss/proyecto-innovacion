import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { API_URL, api } from '../utils/api';

// Función para obtener el rol del usuario actual
function getUserRole(): string {
  const userStr = localStorage.getItem('user');
  if (!userStr) return 'colaborador';
  
  try {
    const user = JSON.parse(userStr);
    return user.role?.name || 'colaborador';
  } catch {
    return 'colaborador';
  }
}

// Función para verificar si el usuario puede gestionar usuarios
function canManageUsers(): boolean {
  return getUserRole() === 'super_admin';
}

// Variable para almacenar el usuario a eliminar
let userToDelete: { id: number; name: string } | null = null;

// Función para mostrar modal de confirmación de eliminación
function showConfirmDeleteModal(userId: number, userName: string) {
  userToDelete = { id: userId, name: userName };
  
  const modal = document.getElementById('modalConfirmDelete');
  const messageEl = document.getElementById('modalConfirmDeleteMessage');
  
  if (messageEl) {
    messageEl.textContent = `¿Estás seguro de que deseas desactivar al usuario "${userName}"?`;
  }
  
  if (modal) {
    modal.classList.add('active');
    const dashboardLayout = document.querySelector('.dashboard-layout');
    dashboardLayout?.classList.add('blur-background');
    document.body.style.overflow = 'hidden';
  }
}

function closeConfirmDeleteModal() {
  const modal = document.getElementById('modalConfirmDelete');
  if (modal) {
    modal.classList.remove('active');
    const dashboardLayout = document.querySelector('.dashboard-layout');
    dashboardLayout?.classList.remove('blur-background');
    document.body.style.overflow = '';
  }
  userToDelete = null;
}

// Función para obtener los filtros actuales
function getCurrentFilters(): { role?: string; status?: string; search?: string } {
  const filters: { role?: string; status?: string; search?: string } = {};
  
  const roleFilter = document.getElementById('roleFilter') as HTMLSelectElement;
  const statusFilter = document.getElementById('statusFilter') as HTMLSelectElement;
  const searchInput = document.getElementById('searchInput') as HTMLInputElement;
  
  if (roleFilter?.value) filters.role = roleFilter.value;
  if (statusFilter?.value) filters.status = statusFilter.value;
  if (searchInput?.value) filters.search = searchInput.value;
  
  return filters;
}

// Función para mostrar modal de éxito
function showSuccessModal(title: string, message: string) {
  const modal = document.getElementById('modalSuccess');
  const titleEl = document.getElementById('modalSuccessTitle');
  const messageEl = document.getElementById('modalSuccessMessage');
  
  if (titleEl) titleEl.textContent = title;
  if (messageEl) messageEl.textContent = message;
  
  if (modal) {
    modal.classList.add('active');
    const dashboardLayout = document.querySelector('.dashboard-layout');
    dashboardLayout?.classList.add('blur-background');
    document.body.style.overflow = 'hidden';
  }
}

function closeSuccessModal() {
  const modal = document.getElementById('modalSuccess');
  if (modal) {
    modal.classList.remove('active');
    const dashboardLayout = document.querySelector('.dashboard-layout');
    dashboardLayout?.classList.remove('blur-background');
    document.body.style.overflow = '';
  }
}

export function UsersPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('usuarios')}
      ${AIAssistant()}
      
      <main class="dashboard-main">
        <header class="dashboard-header">
          <div class="header-top">
            <button class="btn-mobile-menu">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
            <h1 class="page-title">Sistema de Análisis y Productividad</h1>
            <button class="btn-ai-assistant">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
              </svg>
              AI Assistant
            </button>
          </div>
          <div class="header-subtitle">Processmart S.A.C.</div>
        </header>

        <div class="dashboard-content">
          <div class="users-header">
            <div class="module-icon users">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="white" stroke-width="2">
                <circle cx="15" cy="12" r="5"/>
                <circle cx="28" cy="12" r="4"/>
                <path d="M5 32c0-5.5 4.5-10 10-10s10 4.5 10 10"/>
                <path d="M22 32c0-4 3-7 6-7s6 3 6 7"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Gestión de Usuarios</h2>
              <p class="module-description">Administración de usuarios y permisos del sistema</p>
            </div>
            ${canManageUsers() ? `
            <button class="btn-primary" id="btnNewUser">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="10" y1="4" x2="10" y2="16"/>
                <line x1="4" y1="10" x2="16" y2="10"/>
              </svg>
              Nuevo Usuario
            </button>
            ` : ''}
          </div>

          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-label">Total Usuarios</div>
              <div class="stat-value" id="totalUsers">0</div>
              <div class="stat-description">En el sistema</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Activos</div>
              <div class="stat-value" id="activeUsers">0</div>
              <div class="stat-description">Usuarios activos</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Administradores</div>
              <div class="stat-value" id="adminUsers">0</div>
              <div class="stat-description">Con permisos admin</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Supervisores</div>
              <div class="stat-value" id="supervisorUsers">0</div>
              <div class="stat-description">Rol supervisor</div>
            </div>
          </div>

          <!-- Filters -->
          <div class="filters-bar">
            <div class="search-box">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="#999" stroke-width="2">
                <circle cx="8" cy="8" r="6"/>
                <line x1="13" y1="13" x2="18" y2="18"/>
              </svg>
              <input type="text" placeholder="Buscar por nombre o email..." id="searchInput">
            </div>
            <select class="filter-select" id="roleFilter">
              <option value="">Cargando roles...</option>
            </select>
            <select class="filter-select" id="statusFilter">
              <option value="">Todos</option>
              <option value="activo">Activos</option>
              <option value="inactivo">Inactivos</option>
            </select>
          </div>

          <!-- Users Table -->
          <div class="users-section">
            <h3>Lista de Usuarios</h3>
            <p class="section-subtitle" id="usersCount">Cargando...</p>

            <div class="users-table" id="usersTableContainer">
              <!-- Se cargará dinámicamente -->
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Modal: Crear Nuevo Usuario -->
    <div class="modal" id="modalNewUser">
      <div class="modal-overlay"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>Crear Nuevo Usuario</h3>
          <button class="modal-close" id="btnCloseModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p class="modal-subtitle">Complete los datos del usuario</p>
          
          <form id="formNewUser">
            <div class="form-row">
              <div class="form-group">
                <label for="userName">Nombre Completo</label>
                <input type="text" id="userName" placeholder="Ej: Juan Pérez" required>
              </div>
              <div class="form-group">
                <label for="userEmail">Email</label>
                <input type="email" id="userEmail" placeholder="usuario@processmart.com" required>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="userRole">Rol</label>
                <select id="userRole" required>
                  <option value="">Cargando roles...</option>
                </select>
              </div>
              <div class="form-group">
                <label for="userArea">Área</label>
                <select id="userArea" required>
                  <option value="">Cargando áreas...</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="userPassword">Contraseña Temporal</label>
                <input type="password" id="userPassword" placeholder="••••••••" required>
              </div>
              <div class="form-group">
                <label for="userPasswordConfirm">Confirmar Contraseña</label>
                <input type="password" id="userPasswordConfirm" placeholder="••••••••" required>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="userExperience">Años de Experiencia</label>
                <input type="number" id="userExperience" placeholder="2" min="0" max="50" value="2">
              </div>
              <div class="form-group">
                <label for="userSkills">Habilidades</label>
                <input type="text" id="userSkills" placeholder="Python, JavaScript, SQL, Machine Learning">
                <small style="color: #666; font-size: 12px;">Separadas por comas</small>
              </div>
            </div>

            <div class="form-group">
              <div class="toggle-group">
                <label for="userStatus">Estado del Usuario</label>
                <div class="toggle-container">
                  <label class="toggle-switch">
                    <input type="checkbox" id="userStatus" checked>
                    <span class="toggle-slider"></span>
                  </label>
                  <span class="toggle-label">Activar cuenta inmediatamente</span>
                </div>
              </div>
            </div>

            <div class="modal-actions">
              <button type="button" class="btn-secondary" id="btnCancelModal">Cancelar</button>
              <button type="submit" class="btn-primary">Crear Usuario</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal: Editar Usuario -->
    <div class="modal" id="modalEditUser">
      <div class="modal-overlay"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>Editar Usuario</h3>
          <button class="modal-close" id="btnCloseEditModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p class="modal-subtitle">Modificar los datos del usuario</p>
          
          <form id="formEditUser">
            <input type="hidden" id="editUserId">
            <div class="form-row">
              <div class="form-group">
                <label for="editUserName">Nombre Completo</label>
                <input type="text" id="editUserName" placeholder="Ej: Juan Pérez" required>
              </div>
              <div class="form-group">
                <label for="editUserEmail">Email</label>
                <input type="email" id="editUserEmail" placeholder="usuario@processmart.com" required>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="editUserRole">Rol</label>
                <select id="editUserRole" required>
                  <option value="">Cargando roles...</option>
                </select>
              </div>
              <div class="form-group">
                <label for="editUserArea">Área</label>
                <select id="editUserArea" required>
                  <option value="">Cargando áreas...</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <div class="toggle-group">
                <label for="editUserStatus">Estado del Usuario</label>
                <div class="toggle-container">
                  <label class="toggle-switch">
                    <input type="checkbox" id="editUserStatus">
                    <span class="toggle-slider"></span>
                  </label>
                  <span class="toggle-label">Cuenta activa</span>
                </div>
              </div>
            </div>

            <div class="modal-actions">
              <button type="button" class="btn-secondary" id="btnCancelEditModal">Cancelar</button>
              <button type="submit" class="btn-primary">Actualizar Usuario</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal: Confirmación de Eliminación -->
    <div class="modal" id="modalConfirmDelete" style="z-index: 10000;">
      <div class="modal-overlay" id="modalConfirmDeleteOverlay" style="background: rgba(0, 0, 0, 0.7);"></div>
      <div class="modal-content" style="max-width: 450px; text-align: center;">
        <div class="modal-body" style="padding: 40px 30px;">
          <div style="width: 70px; height: 70px; margin: 0 auto 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </div>
          <h3 style="margin: 0 0 10px 0; color: #1a1a1a; font-size: 1.5rem;">¿Desactivar Usuario?</h3>
          <p id="modalConfirmDeleteMessage" style="margin: 0 0 30px 0; color: #666; line-height: 1.6;">¿Estás seguro de que deseas desactivar este usuario?</p>
          <div style="display: flex; gap: 12px; justify-content: center;">
            <button id="btnCancelDelete" class="btn-secondary" style="min-width: 120px; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; background: #f0f0f0; border: none; color: #333;">
              Cancelar
            </button>
            <button id="btnConfirmDelete" class="btn-primary" style="min-width: 120px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; color: white;">
              Desactivar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Éxito -->
    <div class="modal" id="modalSuccess" style="z-index: 10000;">
      <div class="modal-overlay" id="modalSuccessOverlay" style="background: rgba(0, 0, 0, 0.7);"></div>
      <div class="modal-content" style="max-width: 450px; text-align: center;">
        <div class="modal-body" style="padding: 40px 30px;">
          <div style="width: 70px; height: 70px; margin: 0 auto 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <h3 id="modalSuccessTitle" style="margin: 0 0 10px 0; color: #1a1a1a; font-size: 1.5rem;">¡Éxito!</h3>
          <p id="modalSuccessMessage" style="margin: 0 0 30px 0; color: #666; line-height: 1.6;">Operación completada correctamente</p>
          <div style="display: flex; justify-content: center;">
            <button id="btnAcceptSuccess" class="btn-primary" style="min-width: 120px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: transform 0.2s;">
              Aceptar
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Función para cargar usuarios desde el API
async function loadUsers(filters: { role?: string; status?: string; search?: string } = {}) {
  try {
    const response = await api.getUsers();
    let users = response.users || [];
    
    // Aplicar filtros
    if (filters.role) {
      users = users.filter((u: any) => u.role?.name === filters.role);
    }
    
    if (filters.status) {
      const statusValue = filters.status === 'activo' ? 'active' : 'inactive';
      users = users.filter((u: any) => u.status === statusValue);
    }
    
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      users = users.filter((u: any) => 
        u.full_name?.toLowerCase().includes(searchLower) ||
        u.email?.toLowerCase().includes(searchLower)
      );
    }
    
    // Ordenar: Activos primero, luego inactivos
    users.sort((a: any, b: any) => {
      if (a.status === 'active' && b.status !== 'active') return -1;
      if (a.status !== 'active' && b.status === 'active') return 1;
      return 0;
    });
    
    // Actualizar estadísticas (con datos sin filtrar)
    const allUsers = response.users || [];
    const totalUsers = allUsers.length;
    const activeUsers = allUsers.filter((u: any) => u.status === 'active').length;
    const adminUsers = allUsers.filter((u: any) => u.role?.name === 'admin').length;
    const supervisorUsers = allUsers.filter((u: any) => u.role?.name === 'supervisor').length;
    
    const totalEl = document.getElementById('totalUsers');
    const activeEl = document.getElementById('activeUsers');
    const adminEl = document.getElementById('adminUsers');
    const supervisorEl = document.getElementById('supervisorUsers');
    const countEl = document.getElementById('usersCount');
    
    if (totalEl) totalEl.textContent = totalUsers.toString();
    if (activeEl) activeEl.textContent = activeUsers.toString();
    if (adminEl) adminEl.textContent = adminUsers.toString();
    if (supervisorEl) supervisorEl.textContent = supervisorUsers.toString();
    if (countEl) countEl.textContent = `Total: ${users.length} usuarios${users.length !== totalUsers ? ` (${totalUsers} total)` : ''}`;
    
    // Renderizar tabla
    const container = document.getElementById('usersTableContainer');
    if (!container) return;

    if (users.length === 0) {
      container.innerHTML = '<p style="text-align: center; padding: 40px;">No hay usuarios registrados</p>';
      return;
    }

    const getInitials = (name: string) => {
      const parts = name.split(' ');
      return parts.length >= 2 
        ? parts[0][0] + parts[1][0] 
        : parts[0].substring(0, 2);
    };

    const getRoleColor = (roleName: string) => {
      const colors: any = {
        'admin': { bg: '#dc3545', text: 'white' },
        'supervisor': { bg: '#007bff', text: 'white' },
        'analyst': { bg: '#28a745', text: 'white' },
        'user': { bg: '#28a745', text: 'white' }
      };
      return colors[roleName] || colors['user'];
    };

    container.innerHTML = `
      <div class="table-header">
        <div class="th-cell">Usuario</div>
        <div class="th-cell">Email</div>
        <div class="th-cell">Rol</div>
        <div class="th-cell">Área</div>
        <div class="th-cell">Estado</div>
        <div class="th-cell">Acciones</div>
      </div>
      ${users.map((user: any) => {
        const initials = getInitials(user.full_name || 'Usuario');
        const roleName = user.role?.display_name || user.role?.name || 'Sin rol';
        const roleColor = getRoleColor(user.role?.name || 'user');
        const statusColor = user.status === 'active' 
          ? { bg: '#28a745', text: 'white' }
          : { bg: '#dc3545', text: 'white' };
        const statusText = user.status === 'active' ? 'Activo' : 'Inactivo';

        return `
          <div class="table-row">
            <div class="td-cell user-cell">
              <div class="user-avatar">${initials}</div>
              <span class="user-name">${user.full_name}</span>
            </div>
            <div class="td-cell">${user.email}</div>
            <div class="td-cell">
              <span class="role-badge" style="background: ${roleColor.bg}; color: ${roleColor.text};">
                ${roleName}
              </span>
            </div>
            <div class="td-cell">${user.area || '-'}</div>
            <div class="td-cell">
              <span class="status-badge" style="background: ${statusColor.bg}; color: ${statusColor.text};">
                ${statusText}
              </span>
            </div>
            <div class="td-cell actions-cell">
              ${canManageUsers() ? `
              <button class="btn-icon btn-edit-user" 
                data-id="${user.id}" 
                data-name="${user.full_name}" 
                data-email="${user.email}" 
                data-role="${user.role_id}" 
                data-area="${user.area || ''}" 
                data-status="${user.status}"
                title="Editar">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
              <button class="btn-icon btn-delete btn-delete-user" 
                data-id="${user.id}" 
                data-name="${user.full_name}"
                title="Eliminar">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                </svg>
              </button>
              ` : '<span style="color: var(--text-secondary); font-size: 0.875rem;">Solo lectura</span>'}
            </div>
          </div>
        `;
      }).join('')}
    `;

    // Agregar event listeners a los botones de editar y eliminar
    attachUserActionListeners();

  } catch (error) {
    console.error('Error al cargar usuarios:', error);
    const container = document.getElementById('usersTableContainer');
    if (container) {
      container.innerHTML = '<p style="text-align: center; padding: 40px; color: red;">Error al cargar usuarios</p>';
    }
  }
}

// Función para agregar event listeners a los botones de acción
function attachUserActionListeners() {
  // Botones de editar
  const editButtons = document.querySelectorAll('.btn-edit-user');
  editButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const btn = e.currentTarget as HTMLElement;
      const userId = btn.dataset.id;
      const userName = btn.dataset.name;
      const userEmail = btn.dataset.email;
      const userRole = btn.dataset.role;
      const userArea = btn.dataset.area;
      const userStatus = btn.dataset.status;
      
      openEditModal(userId!, userName!, userEmail!, userRole!, userArea!, userStatus!);
    });
  });

  // Botones de eliminar
  const deleteButtons = document.querySelectorAll('.btn-delete-user');
  deleteButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      const btn = e.currentTarget as HTMLElement;
      const userId = btn.dataset.id;
      const userName = btn.dataset.name;
      
      showConfirmDeleteModal(parseInt(userId!), userName!);
    });
  });
}

// Función para abrir el modal de edición
function openEditModal(id: string, name: string, email: string, role: string, area: string, status: string) {
  const modal = document.getElementById('modalEditUser');
  if (!modal) return;

  (document.getElementById('editUserId') as HTMLInputElement).value = id;
  (document.getElementById('editUserName') as HTMLInputElement).value = name;
  (document.getElementById('editUserEmail') as HTMLInputElement).value = email;
  (document.getElementById('editUserStatus') as HTMLInputElement).checked = status === 'active';

  // Cargar roles y áreas, luego seleccionar valores actuales
  Promise.all([loadAreasForSelect(), loadRolesForSelect()]).then(() => {
    (document.getElementById('editUserArea') as HTMLSelectElement).value = area;
    (document.getElementById('editUserRole') as HTMLSelectElement).value = role;
  });

  modal.classList.add('active');
}

// Función para cerrar el modal de edición
function closeEditModal() {
  const modal = document.getElementById('modalEditUser');
  modal?.classList.remove('active');
}

// Función para eliminar/desactivar usuario
async function deleteUser(userId: number) {
  try {
    await api.deleteUser(userId);
    closeConfirmDeleteModal();
    showSuccessModal('¡Usuario Desactivado!', 'El usuario se ha desactivado exitosamente');
    setTimeout(() => {
      loadUsers(getCurrentFilters()); // Recargar la lista con filtros actuales
    }, 1500);
  } catch (error) {
    console.error('Error al eliminar usuario:', error);
    alert('Error al desactivar usuario: ' + (error as Error).message);
  }
}

// Función para cargar áreas dinámicamente
async function loadAreasForSelect() {
  try {
    const response = await api.getAreas();
    const areas = response.areas || [];
    
    // Filtrar solo áreas activas
    const activeAreas = areas.filter((area: any) => area.status === 'active');
    
    // Actualizar select de crear usuario
    const userAreaSelect = document.getElementById('userArea') as HTMLSelectElement;
    if (userAreaSelect) {
      userAreaSelect.innerHTML = '<option value="">Seleccionar área</option>';
      activeAreas.forEach((area: any) => {
        const option = document.createElement('option');
        option.value = area.name;
        option.textContent = area.name;
        userAreaSelect.appendChild(option);
      });
    }
    
    // Actualizar select de editar usuario
    const editUserAreaSelect = document.getElementById('editUserArea') as HTMLSelectElement;
    if (editUserAreaSelect) {
      editUserAreaSelect.innerHTML = '<option value="">Seleccionar área</option>';
      activeAreas.forEach((area: any) => {
        const option = document.createElement('option');
        option.value = area.name;
        option.textContent = area.name;
        editUserAreaSelect.appendChild(option);
      });
    }
  } catch (error) {
    console.error('Error al cargar áreas:', error);
    // Si falla, poner mensaje de error
    const userAreaSelect = document.getElementById('userArea') as HTMLSelectElement;
    const editUserAreaSelect = document.getElementById('editUserArea') as HTMLSelectElement;
    
    if (userAreaSelect) {
      userAreaSelect.innerHTML = '<option value="">Error al cargar áreas</option>';
    }
    if (editUserAreaSelect) {
      editUserAreaSelect.innerHTML = '<option value="">Error al cargar áreas</option>';
    }
  }
}

// Función para cargar roles dinámicamente
async function loadRolesForSelect() {
  try {
    const response = await api.getRoles();
    const roles = response.roles || [];
    
    // Filtrar solo roles activos
    const activeRoles = roles.filter((role: any) => role.status === 'active');
    
    // Actualizar select de crear usuario
    const userRoleSelect = document.getElementById('userRole') as HTMLSelectElement;
    if (userRoleSelect) {
      userRoleSelect.innerHTML = '<option value="">Seleccionar rol</option>';
      activeRoles.forEach((role: any) => {
        const option = document.createElement('option');
        option.value = role.id.toString();
        option.textContent = role.display_name || role.name;
        userRoleSelect.appendChild(option);
      });
    }
    
    // Actualizar select de editar usuario
    const editUserRoleSelect = document.getElementById('editUserRole') as HTMLSelectElement;
    if (editUserRoleSelect) {
      editUserRoleSelect.innerHTML = '<option value="">Seleccionar rol</option>';
      activeRoles.forEach((role: any) => {
        const option = document.createElement('option');
        option.value = role.id.toString();
        option.textContent = role.display_name || role.name;
        editUserRoleSelect.appendChild(option);
      });
    }

    // Actualizar filtro de roles
    const roleFilterSelect = document.getElementById('roleFilter') as HTMLSelectElement;
    if (roleFilterSelect) {
      // Guardar el valor actual del filtro
      const currentValue = roleFilterSelect.value;
      roleFilterSelect.innerHTML = '<option value="">Todos los roles</option>';
      activeRoles.forEach((role: any) => {
        const option = document.createElement('option');
        option.value = role.name;
        option.textContent = role.display_name || role.name;
        roleFilterSelect.appendChild(option);
      });
      // Restaurar el valor del filtro si existía
      if (currentValue) {
        roleFilterSelect.value = currentValue;
      }
    }
  } catch (error) {
    console.error('Error al cargar roles:', error);
    // Si falla, poner mensaje de error
    const userRoleSelect = document.getElementById('userRole') as HTMLSelectElement;
    const editUserRoleSelect = document.getElementById('editUserRole') as HTMLSelectElement;
    
    if (userRoleSelect) {
      userRoleSelect.innerHTML = '<option value="">Error al cargar roles</option>';
    }
    if (editUserRoleSelect) {
      editUserRoleSelect.innerHTML = '<option value="">Error al cargar roles</option>';
    }
  }
}

export function initUsers(): void {
  // Initialize AI Assistant
  initAIAssistant();

  // Cargar usuarios desde el API
  loadUsers();

  // Cargar roles para el filtro
  loadRolesForSelect();

  // Modal controls
  const modal = document.getElementById('modalNewUser');
  const btnNewUser = document.getElementById('btnNewUser');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const btnCancelModal = document.getElementById('btnCancelModal');
  const modalOverlay = modal?.querySelector('.modal-overlay');
  const dashboardLayout = document.querySelector('.dashboard-layout');

  const openModal = () => {
    modal?.classList.add('active');
    dashboardLayout?.classList.add('blur-background');
    document.body.style.overflow = 'hidden';
    loadAreasForSelect(); // Cargar áreas al abrir el modal
    loadRolesForSelect(); // Cargar roles al abrir el modal
  };

  const closeModal = () => {
    modal?.classList.remove('active');
    dashboardLayout?.classList.remove('blur-background');
    document.body.style.overflow = '';
  };

  btnNewUser?.addEventListener('click', openModal);
  btnCloseModal?.addEventListener('click', closeModal);
  btnCancelModal?.addEventListener('click', closeModal);
  modalOverlay?.addEventListener('click', closeModal);

  // Form submission
  const form = document.getElementById('formNewUser') as HTMLFormElement;
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userName = (document.getElementById('userName') as HTMLInputElement).value;
    const userEmail = (document.getElementById('userEmail') as HTMLInputElement).value;
    const userRole = (document.getElementById('userRole') as HTMLSelectElement).value;
    const userArea = (document.getElementById('userArea') as HTMLSelectElement).value;
    const userPassword = (document.getElementById('userPassword') as HTMLInputElement).value;
    const userPasswordConfirm = (document.getElementById('userPasswordConfirm') as HTMLInputElement).value;
    const userStatus = (document.getElementById('userStatus') as HTMLInputElement).checked;

    if (userPassword !== userPasswordConfirm) {
      alert('Las contraseñas no coinciden');
      return;
    }

    if (!userName || !userEmail || !userRole || !userArea || !userPassword) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    try {
      const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Creando...';

      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          email: userEmail,
          password: userPassword,
          full_name: userName,
          role_id: parseInt(userRole),
          area: userArea,
          status: userStatus ? 'active' : 'inactive',
          experience_years: parseInt((document.getElementById('userExperience') as HTMLInputElement).value) || 2,
          skills: (document.getElementById('userSkills') as HTMLInputElement).value || ''
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Error al crear usuario');
      }

      showSuccessModal('¡Usuario Creado!', `El usuario "${userName}" se ha creado exitosamente`);
      closeModal();
      form.reset();
      setTimeout(() => {
        loadUsers(getCurrentFilters());
      }, 1500);
    } catch (error) {
      console.error('Error al crear usuario:', error);
      alert('Error al crear el usuario: ' + (error as Error).message);
    } finally {
      const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
      submitBtn.disabled = false;
      submitBtn.textContent = 'Crear Usuario';
    }
  });

  // Search functionality
  const searchInput = document.getElementById('searchInput') as HTMLInputElement;
  const roleFilter = document.getElementById('roleFilter') as HTMLSelectElement;
  const statusFilter = document.getElementById('statusFilter') as HTMLSelectElement;
  
  const applyFilters = () => {
    loadUsers(getCurrentFilters());
  };
  
  searchInput?.addEventListener('input', applyFilters);
  roleFilter?.addEventListener('change', applyFilters);
  statusFilter?.addEventListener('change', applyFilters);

  // Mobile menu
  const mobileToggle = document.querySelector('.btn-mobile-menu');
  const sidebar = document.querySelector('.sidebar');
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-active');
    });
  }

  // AI Assistant button
  const aiButton = document.querySelector('.btn-ai-assistant');
  if (aiButton) {
    aiButton.addEventListener('click', () => {
      const assistant = document.getElementById('aiAssistant');
      if (assistant) {
        assistant.classList.add('active');
      }
    });
  }

  // Modal de edición
  const btnCloseEditModal = document.getElementById('btnCloseEditModal');
  const btnCancelEditModal = document.getElementById('btnCancelEditModal');

  btnCloseEditModal?.addEventListener('click', closeEditModal);
  btnCancelEditModal?.addEventListener('click', closeEditModal);

  // Formulario de edición
  const formEditUser = document.getElementById('formEditUser') as HTMLFormElement;
  formEditUser?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userId = parseInt((document.getElementById('editUserId') as HTMLInputElement).value);
    const userName = (document.getElementById('editUserName') as HTMLInputElement).value;
    const userEmail = (document.getElementById('editUserEmail') as HTMLInputElement).value;
    const userRole = parseInt((document.getElementById('editUserRole') as HTMLSelectElement).value);
    const userArea = (document.getElementById('editUserArea') as HTMLSelectElement).value;
    const userStatus = (document.getElementById('editUserStatus') as HTMLInputElement).checked;

    if (!userName || !userEmail) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    try {
      const submitBtn = formEditUser.querySelector('button[type="submit"]') as HTMLButtonElement;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Actualizando...';

      await api.updateUser(userId, {
        full_name: userName,
        email: userEmail,
        role_id: userRole,
        area: userArea,
        status: userStatus ? 'active' : 'inactive'
      });

      showSuccessModal('¡Usuario Actualizado!', `El usuario "${userName}" se ha actualizado exitosamente`);
      closeEditModal();
      setTimeout(() => {
        // Recargar la lista con filtros actuales
        loadUsers(getCurrentFilters());
      }, 1500);
    } catch (error) {
      console.error('Error al actualizar usuario:', error);
      alert('Error al actualizar el usuario: ' + (error as Error).message);
    } finally {
      const submitBtn = formEditUser.querySelector('button[type="submit"]') as HTMLButtonElement;
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Actualizar Usuario';
      }
    }
  });

  // Event listeners para modal de confirmación de eliminación
  const btnCancelDelete = document.getElementById('btnCancelDelete');
  const btnConfirmDelete = document.getElementById('btnConfirmDelete');
  const modalConfirmDeleteOverlay = document.getElementById('modalConfirmDeleteOverlay');
  
  btnCancelDelete?.addEventListener('click', closeConfirmDeleteModal);
  btnConfirmDelete?.addEventListener('click', async () => {
    if (userToDelete) {
      await deleteUser(userToDelete.id);
    }
  });
  modalConfirmDeleteOverlay?.addEventListener('click', closeConfirmDeleteModal);

  // Event listeners para modal de éxito
  const btnAcceptSuccess = document.getElementById('btnAcceptSuccess');
  const modalSuccessOverlay = document.getElementById('modalSuccessOverlay');
  
  btnAcceptSuccess?.addEventListener('click', closeSuccessModal);
  modalSuccessOverlay?.addEventListener('click', closeSuccessModal);

  // Logout
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('access_token');
      window.location.hash = '#login';
    });
  }
}
