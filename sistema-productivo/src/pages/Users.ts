import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

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
            <button class="btn-primary" id="btnNewUser">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="10" y1="4" x2="10" y2="16"/>
                <line x1="4" y1="10" x2="16" y2="10"/>
              </svg>
              Nuevo Usuario
            </button>
          </div>

          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-label">Total Usuarios</div>
              <div class="stat-value">5</div>
              <div class="stat-description">En el sistema</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Activos</div>
              <div class="stat-value">4</div>
              <div class="stat-description">Usuarios activos</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Administradores</div>
              <div class="stat-value">1</div>
              <div class="stat-description">Con permisos admin</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Supervisores</div>
              <div class="stat-value">2</div>
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
              <option value="">Todos los roles</option>
              <option value="admin">Administrador</option>
              <option value="supervisor">Supervisor</option>
              <option value="colaborador">Colaborador</option>
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
            <p class="section-subtitle">Total: 5 usuarios</p>

            <div class="users-table">
              <div class="table-header">
                <div class="th-cell">Usuario</div>
                <div class="th-cell">Email</div>
                <div class="th-cell">Rol</div>
                <div class="th-cell">Área</div>
                <div class="th-cell">Estado</div>
                <div class="th-cell">Acciones</div>
              </div>

              ${generateUserRow('JP', 'Juan Pérez', 'juan.perez@processmart.com', 'Admin', 'TI', 'Activo', 'admin')}
              ${generateUserRow('ML', 'María López', 'maria.lopez@processmart.com', 'Supervisor', 'Marketing', 'Activo', 'supervisor')}
              ${generateUserRow('CR', 'Carlos Ruiz', 'carlos.ruiz@processmart.com', 'Colaborador', 'Operaciones', 'Activo', 'colaborador')}
              ${generateUserRow('AG', 'Ana García', 'ana.garcia@processmart.com', 'Colaborador', 'TI', 'Activo', 'colaborador')}
              ${generateUserRow('PS', 'Pedro Sánchez', 'pedro.sanchez@processmart.com', 'Supervisor', 'RRHH', 'Inactivo', 'supervisor')}
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
                  <option value="">Seleccionar rol</option>
                  <option value="admin">Administrador</option>
                  <option value="supervisor">Supervisor</option>
                  <option value="colaborador">Colaborador</option>
                </select>
              </div>
              <div class="form-group">
                <label for="userArea">Área</label>
                <select id="userArea" required>
                  <option value="">Seleccionar área</option>
                  <option value="TI">TI</option>
                  <option value="Marketing">Marketing</option>
                  <option value="Operaciones">Operaciones</option>
                  <option value="Ventas">Ventas</option>
                  <option value="RRHH">RRHH</option>
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
  `;
}

function generateUserRow(
  initials: string,
  name: string,
  email: string,
  role: string,
  area: string,
  status: string,
  roleType: string
): string {
  const roleColors: { [key: string]: { bg: string; text: string } } = {
    'admin': { bg: '#f44336', text: 'white' },
    'supervisor': { bg: '#2196f3', text: 'white' },
    'colaborador': { bg: '#4caf50', text: 'white' }
  };

  const statusColors: { [key: string]: { bg: string; text: string } } = {
    'Activo': { bg: '#d4edda', text: '#155724' },
    'Inactivo': { bg: '#f8d7da', text: '#721c24' }
  };

  const roleColor = roleColors[roleType];
  const statusColor = statusColors[status];

  return `
    <div class="table-row">
      <div class="td-cell user-cell">
        <div class="user-avatar">${initials}</div>
        <span class="user-name">${name}</span>
      </div>
      <div class="td-cell">${email}</div>
      <div class="td-cell">
        <span class="role-badge" style="background: ${roleColor.bg}; color: ${roleColor.text};">
          ${role}
        </span>
      </div>
      <div class="td-cell">${area}</div>
      <div class="td-cell">
        <span class="status-badge" style="background: ${statusColor.bg}; color: ${statusColor.text};">
          ${status}
        </span>
      </div>
      <div class="td-cell actions-cell">
        <button class="btn-icon" title="Editar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </button>
        <button class="btn-icon btn-delete" title="Eliminar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
        </button>
      </div>
    </div>
  `;
}

export function initUsers(): void {
  // Initialize AI Assistant
  initAIAssistant();

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
  form?.addEventListener('submit', (e) => {
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

    console.log('Nuevo usuario:', {
      name: userName,
      email: userEmail,
      role: userRole,
      area: userArea,
      active: userStatus
    });

    alert(`Usuario ${userName} creado exitosamente`);
    closeModal();
    form.reset();
  });

  // Search functionality
  const searchInput = document.getElementById('searchInput') as HTMLInputElement;
  searchInput?.addEventListener('input', (e) => {
    const searchTerm = (e.target as HTMLInputElement).value.toLowerCase();
    console.log('Buscar:', searchTerm);
    // Implement search logic
  });

  // Filter functionality
  const roleFilter = document.getElementById('roleFilter') as HTMLSelectElement;
  const statusFilter = document.getElementById('statusFilter') as HTMLSelectElement;

  roleFilter?.addEventListener('change', (e) => {
    console.log('Filtrar por rol:', (e.target as HTMLSelectElement).value);
    // Implement filter logic
  });

  statusFilter?.addEventListener('change', (e) => {
    console.log('Filtrar por estado:', (e.target as HTMLSelectElement).value);
    // Implement filter logic
  });

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

  // Logout
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userEmail');
      window.location.hash = '#login';
    });
  }
}
