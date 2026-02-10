import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { api } from '../utils/api';

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

// Función para verificar si el usuario puede gestionar áreas
function canManageAreas(): boolean {
  return getUserRole() === 'super_admin';
}

export function AreasPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('areas')}
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
          <div class="areas-header">
            <div class="module-icon areas">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="white" stroke-width="2">
                <rect x="8" y="8" width="10" height="10" rx="2"/>
                <rect x="22" y="8" width="10" height="10" rx="2"/>
                <rect x="8" y="22" width="10" height="10" rx="2"/>
                <rect x="22" y="22" width="10" height="10" rx="2"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Gestión de Áreas</h2>
              <p class="module-description">Administración de áreas </p>
            </div>
            ${canManageAreas() ? `
            <button class="btn-primary" id="btnNewArea">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="10" y1="4" x2="10" y2="16"/>
                <line x1="4" y1="10" x2="16" y2="10"/>
              </svg>
              Nueva Área
            </button>
            ` : ''}
          </div>

          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-label">Total Áreas</div>
              <div class="stat-value" id="totalAreas">--</div>
              <div class="stat-description">Áreas activas</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Áreas Activas</div>
              <div class="stat-value" id="activeAreas">--</div>
              <div class="stat-description">En operación</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Áreas Inactivas</div>
              <div class="stat-value" id="inactiveAreas">--</div>
              <div class="stat-description">Suspendidas</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Última Actualización</div>
              <div class="stat-value" id="lastUpdate">--</div>
              <div class="stat-description">Datos del sistema</div>
            </div>
          </div>

          <!-- Areas Grid -->
          <div class="areas-grid" id="areasContainer">
            <p style="text-align: center; padding: 40px;">Cargando áreas...</p>
          </div>
        </div>
      </main>
    </div>

    <!-- Modal: Crear Nueva Área -->
    <div class="modal" id="modalNewArea">
      <div class="modal-overlay"></div>
      <div class="modal-content modal-small">
        <div class="modal-header">
          <h3>Crear Nueva Área</h3>
          <button class="modal-close" id="btnCloseModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p class="modal-subtitle">Complete los datos del área o departamento</p>
          
          <form id="formNewArea">
            <div class="form-group">
              <label for="areaName">Nombre del Área</label>
              <input type="text" id="areaName" placeholder="Ej: Finanzas" required>
            </div>

            <div class="form-group">
              <label for="areaDescription">Descripción</label>
              <textarea id="areaDescription" rows="3" placeholder="Descripción breve del área"></textarea>
            </div>

            <div class="form-group">
              <label for="areaSupervisor">Asignar Supervisor</label>
              <select id="areaSupervisor" required>
                <option value="">Seleccionar supervisor</option>
              </select>
            </div>

            <div class="form-group">
              <label for="areaEfficiency">Meta de Eficiencia (%)</label>
              <input type="number" id="areaEfficiency" placeholder="85" min="0" max="100" required>
            </div>

            <div class="modal-actions">
              <button type="button" class="btn-secondary" id="btnCancelModal">Cancelar</button>
              <button type="submit" class="btn-primary">Crear Área</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal: Detalles del Área -->
    <div class="modal-overlay" id="areaDetailsModal">
      <div class="modal-content modal-large">
        <div class="modal-header">
          <h3>Detalles del Área</h3>
          <button class="modal-close" id="btnCloseDetailsModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="area-details-grid">
            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <rect x="3" y="3" width="7" height="7" rx="1"/>
                  <rect x="14" y="3" width="7" height="7" rx="1"/>
                  <rect x="3" y="14" width="7" height="7" rx="1"/>
                  <rect x="14" y="14" width="7" height="7" rx="1"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Nombre del Área</div>
                <div class="detail-value" id="detailAreaName">--</div>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Descripción</div>
                <div class="detail-value" id="detailAreaDescription">--</div>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Supervisor</div>
                <div class="detail-value" id="detailAreaSupervisor">--</div>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Empleados</div>
                <div class="detail-value" id="detailAreaEmployees">--</div>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="9" y1="15" x2="15" y2="15"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Tareas Asignadas</div>
                <div class="detail-value" id="detailAreaTasks">--</div>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Eficiencia</div>
                <div class="detail-value" id="detailAreaEfficiency">--</div>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Estado</div>
                <div class="detail-value" id="detailAreaStatus">--</div>
              </div>
            </div>

            <div class="detail-card">
              <div class="detail-icon" style="background: linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </div>
              <div class="detail-content">
                <div class="detail-label">Fecha de Creación</div>
                <div class="detail-value" id="detailAreaCreated">--</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Confirmación de Eliminación -->
    <div class="modal" id="modalConfirmDelete" style="display: none;">
      <div class="modal-overlay"></div>
      <div class="modal-content modal-small" style="max-width: 450px;">
        <div class="modal-body" style="padding: 30px;">
          <div style="width: 70px; height: 70px; margin: 0 auto 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <h3 style="font-size: 22px; margin-bottom: 12px; color: #1a202c; text-align: center;">¿Estás seguro?</h3>
          <p style="color: #718096; margin-bottom: 8px; text-align: center;" id="confirmMessage">¿Deseas eliminar el área?</p>
          <p style="color: #e53e3e; font-size: 14px; margin-bottom: 24px; text-align: center;">Esta acción desactivará el área.</p>
          <div style="display: flex; gap: 12px;">
            <button class="btn-secondary" id="btnCancelDelete" style="flex: 1; padding: 12px;">Cancelar</button>
            <button class="btn-danger" id="btnConfirmDelete" style="flex: 1; padding: 12px; background: #e53e3e;">Eliminar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Éxito -->
    <div class="modal" id="modalSuccess" style="display: none;">
      <div class="modal-overlay"></div>
      <div class="modal-content modal-small" style="max-width: 400px; text-align: center;">
        <div class="modal-body" style="padding: 40px 30px;">
          <div style="width: 80px; height: 80px; margin: 0 auto 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </div>
          <h3 style="font-size: 24px; margin-bottom: 12px; color: #1a202c;" id="successTitle">¡Éxito!</h3>
          <p style="color: #718096; margin-bottom: 30px;" id="successMessage">Operación realizada correctamente</p>
          <button class="btn-primary" id="btnCloseSuccess" style="width: 100%; padding: 12px;">Aceptar</button>
        </div>
      </div>
    </div>
  `;
}

function generateAreaCard(
  id: number,
  name: string,
  description: string,
  supervisor: string,
  initials: string,
  employees: number,
  tasks: number,
  efficiency: number,
  trend: string,
  trendType: 'success' | 'warning' | 'danger'
): string {
  const trendColors: { [key: string]: { bg: string; text: string } } = {
    'success': { bg: '#4caf50', text: 'white' },
    'warning': { bg: '#ff9800', text: 'white' },
    'danger': { bg: '#f44336', text: 'white' }
  };

  const trendColor = trendColors[trendType];
  const efficiencyColor = efficiency >= 85 ? '#4caf50' : efficiency >= 75 ? '#ff9800' : '#f44336';

  return `
    <div class="area-card" data-area-id="${id}">
      <div class="area-card-header">
        <div class="area-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" rx="1"/>
            <rect x="14" y="3" width="7" height="7" rx="1"/>
            <rect x="3" y="14" width="7" height="7" rx="1"/>
            <rect x="14" y="14" width="7" height="7" rx="1"/>
          </svg>
        </div>
        <div class="area-actions">
          ${canManageAreas() ? `
          <button class="btn-icon btn-edit-area" 
            data-id="${id}"
            data-name="${name}"
            data-description="${description}"
            data-supervisor="${supervisor}"
            title="Editar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="btn-icon btn-delete-area" 
            data-id="${id}"
            data-name="${name}"
            title="Eliminar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
          ` : ''}
        </div>
      </div>

      <h3 class="area-name">${name}</h3>
      <p class="area-description">${description}</p>

      <div class="area-supervisor">
        <div class="supervisor-avatar">${initials}</div>
        <div class="supervisor-info">
          <div class="supervisor-label">Supervisor</div>
          <div class="supervisor-name">${supervisor}</div>
        </div>
      </div>

      <div class="area-stats">
        <div class="stat-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          <div>
            <div class="stat-number">${employees}</div>
            <div class="stat-label">Empleados</div>
          </div>
        </div>
        <div class="stat-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
          <div>
            <div class="stat-number">${tasks}</div>
            <div class="stat-label">Tareas</div>
          </div>
        </div>
      </div>

      <div class="area-efficiency">
        <div class="efficiency-header">
          <span>Eficiencia</span>
          <span class="efficiency-value" style="color: ${efficiencyColor};">${efficiency}%</span>
        </div>
        <div class="efficiency-bar">
          <div class="efficiency-fill" style="width: ${efficiency}%; background: ${efficiencyColor};"></div>
        </div>
      </div>

      <div class="area-trend">
        <span class="trend-label">Tendencia</span>
        <span class="trend-badge" style="background: ${trendColor.bg}; color: ${trendColor.text};">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
            <polyline points="17 6 23 6 23 12"/>
          </svg>
          ${trend}
        </span>
      </div>

      <button class="btn-details btn-view-details" data-name="${name}" data-employees="${employees}" data-tasks="${tasks}" data-efficiency="${efficiency}">Ver Detalles</button>
    </div>
  `;
}

async function loadSupervisors() {
  try {
    const response = await api.getUsers();
    const users = response.users || [];
    
    // Filtrar solo usuarios con rol de supervisor
    const supervisors = users.filter((user: any) => user.role?.name === 'supervisor');
    
    const supervisorSelect = document.getElementById('areaSupervisor') as HTMLSelectElement;
    if (supervisorSelect) {
      // Mantener la opción por defecto
      supervisorSelect.innerHTML = '<option value="">Seleccionar supervisor</option>';
      
      // Agregar supervisores como opciones
      supervisors.forEach((supervisor: any) => {
        const option = document.createElement('option');
        option.value = supervisor.person_id;
        option.textContent = supervisor.full_name || supervisor.email;
        supervisorSelect.appendChild(option);
      });
      
      // Si no hay supervisores, mostrar mensaje
      if (supervisors.length === 0) {
        supervisorSelect.innerHTML = '<option value="">No hay supervisores disponibles</option>';
      }
    }
  } catch (error) {
    console.error('Error al cargar supervisores:', error);
    // Si falla, dejamos las opciones por defecto vacías
    const supervisorSelect = document.getElementById('areaSupervisor') as HTMLSelectElement;
    if (supervisorSelect) {
      supervisorSelect.innerHTML = '<option value="">Error al cargar supervisores</option>';
    }
  }
}

async function loadAreas() {
  try {
    const response = await api.getAreas();
    const areas = response.areas || [];
    
    // Actualizar estadísticas
    const totalAreas = areas.length;
    const activeAreas = areas.filter((a: any) => a.status === 'active').length;
    const inactiveAreas = areas.filter((a: any) => a.status === 'inactive').length;
    
    const totalEl = document.getElementById('totalAreas');
    const activeEl = document.getElementById('activeAreas');
    const inactiveEl = document.getElementById('inactiveAreas');
    const updateEl = document.getElementById('lastUpdate');
    
    if (totalEl) totalEl.textContent = totalAreas.toString();
    if (activeEl) activeEl.textContent = activeAreas.toString();
    if (inactiveEl) inactiveEl.textContent = inactiveAreas.toString();
    if (updateEl) updateEl.textContent = new Date().toLocaleDateString();
    
    // Renderizar áreas
    const container = document.getElementById('areasContainer');
    if (!container) return;
    
    if (areas.length === 0) {
      container.innerHTML = '<p style="text-align: center; padding: 40px;">No hay áreas registradas</p>';
      return;
    }
    
    container.innerHTML = areas.map((area: any) => {
      const initials = area.name.substring(0, 2).toUpperCase();
      const trend = area.status === 'active' ? 'Activo' : 'Inactivo';
      const trendType = area.status === 'active' ? 'success' : 'warning';
      
      return generateAreaCard(
        area.id,
        area.name,
        area.description || 'Sin descripción',
        area.supervisor_name || 'Sin supervisor',
        initials,
        area.employee_count || 0,
        area.task_count || 0,
        area.efficiency_score || 0,
        trend,
        trendType
      );
    }).join('');

    // Agregar event listeners después de renderizar
    attachAreaActionListeners();
    
  } catch (error) {
    console.error('Error al cargar áreas:', error);
    const container = document.getElementById('areasContainer');
    if (container) {
      container.innerHTML = '<p style="text-align: center; padding: 40px; color: red;">Error al cargar áreas</p>';
    }
  }
}

// Función para agregar event listeners a los botones de acción
function attachAreaActionListeners() {
  // Botones de ver detalles
  const detailButtons = document.querySelectorAll('.btn-view-details');
  detailButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const btn = e.currentTarget as HTMLElement;
      const name = btn.dataset.name!;
      const employees = btn.dataset.employees!;
      const tasks = btn.dataset.tasks!;
      const efficiency = btn.dataset.efficiency!;
      
      openDetailsModal(name, employees, tasks, efficiency);
    });
  });

  // Botones de editar
  const editButtons = document.querySelectorAll('.btn-edit-area');
  editButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const btn = e.currentTarget as HTMLElement;
      const id = parseInt(btn.dataset.id!);
      const name = btn.dataset.name!;
      const description = btn.dataset.description!;
      const supervisor = btn.dataset.supervisor!;
      
      openEditAreaModal(id, name, description, supervisor);
    });
  });

  // Botones de eliminar
  const deleteButtons = document.querySelectorAll('.btn-delete-area');
  deleteButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      const btn = e.currentTarget as HTMLElement;
      const id = parseInt(btn.dataset.id!);
      const name = btn.dataset.name!;
      
      showConfirmDeleteModal(id, name);
    });
  });
}

// Función para abrir modal de detalles
function openDetailsModal(name: string, employees: string, tasks: string, efficiency: string) {
  // Determinar el estado basado en la eficiencia
  const efficiencyNum = parseFloat(efficiency);
  let statusBadge = '';
  
  if (efficiencyNum >= 85) {
    statusBadge = '<span class="status-badge status-completed">Óptimo</span>';
  } else if (efficiencyNum >= 75) {
    statusBadge = '<span class="status-badge status-progress">Bueno</span>';
  } else if (efficiencyNum >= 60) {
    statusBadge = '<span class="status-badge status-pending">Regular</span>';
  } else {
    statusBadge = '<span class="status-badge status-blocked">Bajo</span>';
  }

  // Buscar información adicional del área en las tarjetas renderizadas
  const areaCards = document.querySelectorAll('.area-card');
  let description = 'Sin descripción';
  let supervisorName = 'No asignado';
  
  areaCards.forEach(card => {
    const cardName = card.querySelector('.area-name')?.textContent;
    if (cardName === name) {
      description = card.querySelector('.area-description')?.textContent || 'Sin descripción';
      supervisorName = card.querySelector('.supervisor-name')?.textContent || 'No asignado';
    }
  });

  // Obtener fecha actual formateada
  const currentDate = new Date().toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  // Poblar el modal con los datos
  const detailAreaName = document.getElementById('detailAreaName');
  const detailAreaDescription = document.getElementById('detailAreaDescription');
  const detailAreaSupervisor = document.getElementById('detailAreaSupervisor');
  const detailAreaEmployees = document.getElementById('detailAreaEmployees');
  const detailAreaTasks = document.getElementById('detailAreaTasks');
  const detailAreaEfficiency = document.getElementById('detailAreaEfficiency');
  const detailAreaStatus = document.getElementById('detailAreaStatus');
  const detailAreaCreated = document.getElementById('detailAreaCreated');

  if (detailAreaName) detailAreaName.textContent = name;
  if (detailAreaDescription) detailAreaDescription.textContent = description;
  if (detailAreaSupervisor) detailAreaSupervisor.textContent = supervisorName;
  if (detailAreaEmployees) detailAreaEmployees.textContent = `${employees} persona(s)`;
  if (detailAreaTasks) detailAreaTasks.textContent = `${tasks} tarea(s)`;
  if (detailAreaEfficiency) {
    const efficiencyColor = efficiencyNum >= 85 ? '#4caf50' : efficiencyNum >= 75 ? '#ff9800' : '#f44336';
    detailAreaEfficiency.innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 1.5em; font-weight: bold; color: ${efficiencyColor};">${efficiency}%</span>
      </div>
    `;
  }
  if (detailAreaStatus) detailAreaStatus.innerHTML = statusBadge;
  if (detailAreaCreated) detailAreaCreated.textContent = currentDate;

  // Mostrar el modal
  const modal = document.getElementById('areaDetailsModal');
  if (modal) {
    modal.style.display = 'flex';
  }
}

// Variable para almacenar el ID del área a eliminar
let areaToDelete: { id: number, name: string } | null = null;

// Función para mostrar modal de éxito
function showSuccessModal(title: string, message: string) {
  const modal = document.getElementById('modalSuccess');
  const titleEl = document.getElementById('successTitle');
  const messageEl = document.getElementById('successMessage');
  
  if (modal && titleEl && messageEl) {
    titleEl.textContent = title;
    messageEl.textContent = message;
    modal.style.display = 'flex';
  }
}

// Función para mostrar modal de confirmación de eliminación
function showConfirmDeleteModal(id: number, name: string) {
  areaToDelete = { id, name };
  const modal = document.getElementById('modalConfirmDelete');
  const messageEl = document.getElementById('confirmMessage');
  
  if (modal && messageEl) {
    messageEl.textContent = `¿Deseas eliminar el área "${name}"?`;
    modal.style.display = 'flex';
  }
}

// Función para abrir modal de edición
function openEditAreaModal(id: number, name: string, description: string, _supervisor: string) {
  const modal = document.getElementById('modalNewArea');
  if (!modal) return;

  // Cambiar título del modal
  const modalTitle = modal.querySelector('.modal-header h3');
  if (modalTitle) modalTitle.textContent = 'Editar Área';

  // Rellenar formulario
  (document.getElementById('areaName') as HTMLInputElement).value = name;
  (document.getElementById('areaDescription') as HTMLTextAreaElement).value = description;
  (document.getElementById('areaName') as HTMLInputElement).dataset.editing = 'true';
  (document.getElementById('areaName') as HTMLInputElement).dataset.areaId = id.toString();

  // Cambiar texto del botón
  const submitBtn = modal.querySelector('button[type="submit"]') as HTMLButtonElement;
  if (submitBtn) submitBtn.textContent = 'Actualizar Área';

  modal.classList.add('active');
}

// Función para eliminar área
async function deleteArea(areaId: number) {
  try {
    await api.deleteArea(areaId);
    showSuccessModal('¡Área Eliminada!', 'El área se ha eliminado exitosamente');
    loadAreas();
  } catch (error) {
    console.error('Error al eliminar área:', error);
    alert('Error al eliminar área: ' + (error as Error).message);
  }
}

export function initAreas(): void {
  // Initialize AI Assistant
  initAIAssistant();
  
  // Cargar áreas desde el backend
  loadAreas();

  // Modal controls
  const modal = document.getElementById('modalNewArea');
  const btnNewArea = document.getElementById('btnNewArea');
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
    
    // Limpiar formulario y flags de edición
    const form = document.getElementById('formNewArea') as HTMLFormElement;
    form?.reset();
    
    const areaNameInput = document.getElementById('areaName') as HTMLInputElement;
    if (areaNameInput) {
      delete areaNameInput.dataset.editing;
      delete areaNameInput.dataset.areaId;
    }
    
    // Restaurar título del modal
    const modalTitle = modal?.querySelector('.modal-header h3');
    if (modalTitle) modalTitle.textContent = 'Crear Nueva Área';
    
    // Restaurar texto del botón
    const submitBtn = modal?.querySelector('button[type="submit"]') as HTMLButtonElement;
    if (submitBtn) submitBtn.textContent = 'Crear Área';
  };

  btnNewArea?.addEventListener('click', () => {
    openModal();
    loadSupervisors(); // Cargar supervisores al abrir el modal
  });
  btnCloseModal?.addEventListener('click', closeModal);
  btnCancelModal?.addEventListener('click', closeModal);
  modalOverlay?.addEventListener('click', closeModal);

  // Event listeners para el modal de detalles
  const btnCloseDetailsModal = document.getElementById('btnCloseDetailsModal');
  const areaDetailsModal = document.getElementById('areaDetailsModal');
  
  btnCloseDetailsModal?.addEventListener('click', () => {
    if (areaDetailsModal) {
      areaDetailsModal.style.display = 'none';
    }
  });

  areaDetailsModal?.addEventListener('click', (e) => {
    if (e.target === areaDetailsModal) {
      areaDetailsModal.style.display = 'none';
    }
  });

  // Event listeners para el modal de éxito
  const btnCloseSuccess = document.getElementById('btnCloseSuccess');
  const modalSuccess = document.getElementById('modalSuccess');
  
  btnCloseSuccess?.addEventListener('click', () => {
    if (modalSuccess) {
      modalSuccess.style.display = 'none';
    }
  });

  modalSuccess?.addEventListener('click', (e) => {
    if (e.target === modalSuccess || (e.target as HTMLElement).classList.contains('modal-overlay')) {
      modalSuccess.style.display = 'none';
    }
  });

  // Event listeners para el modal de confirmación de eliminación
  const btnCancelDelete = document.getElementById('btnCancelDelete');
  const btnConfirmDelete = document.getElementById('btnConfirmDelete');
  const modalConfirmDelete = document.getElementById('modalConfirmDelete');
  
  btnCancelDelete?.addEventListener('click', () => {
    if (modalConfirmDelete) {
      modalConfirmDelete.style.display = 'none';
      areaToDelete = null;
    }
  });

  btnConfirmDelete?.addEventListener('click', async () => {
    if (areaToDelete && modalConfirmDelete) {
      modalConfirmDelete.style.display = 'none';
      await deleteArea(areaToDelete.id);
      areaToDelete = null;
    }
  });

  modalConfirmDelete?.addEventListener('click', (e) => {
    if (e.target === modalConfirmDelete || (e.target as HTMLElement).classList.contains('modal-overlay')) {
      modalConfirmDelete.style.display = 'none';
      areaToDelete = null;
    }
  });

  // Form submission
  const form = document.getElementById('formNewArea') as HTMLFormElement;
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const areaNameInput = document.getElementById('areaName') as HTMLInputElement;
    const areaName = areaNameInput.value;
    const areaDescription = (document.getElementById('areaDescription') as HTMLTextAreaElement).value;
    const areaSupervisor = (document.getElementById('areaSupervisor') as HTMLSelectElement).value;
    const areaEfficiency = (document.getElementById('areaEfficiency') as HTMLInputElement).value;

    // Verificar si estamos editando
    const isEditing = areaNameInput.dataset.editing === 'true';
    const areaId = areaNameInput.dataset.areaId;

    if (!areaName || !areaSupervisor || !areaEfficiency) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    try {
      const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
      submitBtn.disabled = true;
      submitBtn.textContent = isEditing ? 'Actualizando...' : 'Creando...';

      const areaData = {
        name: areaName,
        description: areaDescription,
        supervisor_person_id: areaSupervisor,
        efficiency_score: parseFloat(areaEfficiency),
        employee_count: 0
      };

      if (isEditing && areaId) {
        // Actualizar área existente
        await api.updateArea(parseInt(areaId), areaData);
        showSuccessModal('¡Área Actualizada!', `El área "${areaName}" se ha actualizado exitosamente`);
      } else {
        // Crear nueva área
        await api.createArea(areaData);
        showSuccessModal('¡Área Creada!', `El área "${areaName}" se ha creado exitosamente`);
      }

      closeModal();
      form.reset();
      
      // Limpiar flags de edición
      delete areaNameInput.dataset.editing;
      delete areaNameInput.dataset.areaId;
      
      // Restaurar título del modal
      const modalTitle = document.querySelector('#modalNewArea .modal-header h3');
      if (modalTitle) modalTitle.textContent = 'Crear Nueva Área';
      
      loadAreas(); // Recargar áreas en vez de toda la página
    } catch (error) {
      console.error('Error al guardar área:', error);
      alert('Error al guardar el área: ' + (error as Error).message);
    } finally {
      const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
      submitBtn.disabled = false;
      submitBtn.textContent = isEditing ? 'Actualizar Área' : 'Crear Área';
    }
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
