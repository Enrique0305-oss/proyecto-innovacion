import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { api } from '../utils/api';

export function TasksPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('tareas')}
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
          <!-- Header de sección -->
          <div class="section-header">
            <div class="section-info">
              <h2 class="section-title">Gestión de Tareas</h2>
              <p class="section-description">Registro y seguimiento de todas las tareas del sistema</p>
            </div>
            <div class="section-actions">
              <button class="btn-secondary" id="exportTasksBtn">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 14V3M10 14l-4-4M10 14l4-4M3 17h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Exportar
              </button>
              <button class="btn-primary" id="newTaskBtn">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Nueva Tarea
              </button>
            </div>
          </div>

          <!-- Filtros y búsqueda -->
          <div class="filters-bar">
            <div class="search-box">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.5"/>
                <path d="M13 13l4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <input type="text" placeholder="Buscar por ID o nombre de tarea..." />
            </div>
            <select class="filter-select">
              <option>Todos los estados</option>
              <option>En Progreso</option>
              <option>Completada</option>
              <option>Bloqueada</option>
              <option>Por Hacer</option>
            </select>
            <select class="filter-select">
              <option>Todos los riesgos</option>
              <option>Bajo</option>
              <option>Medio</option>
              <option>Alto</option>
              <option>Crítico</option>
            </select>
          </div>

          <!-- Lista de tareas -->
          <div class="tasks-table-container">
            <div class="tasks-table-header">
              <h3>Lista de Tareas</h3>
              <p id="tasksCount">Cargando...</p>
            </div>

            <table class="tasks-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Área</th>
                  <th>Responsables</th>
                  <th>Tiempo Est.</th>
                  <th>Tiempo Real</th>
                  <th>Estado</th>
                  <th>Riesgo</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody id="tasksTableBody">
                <!-- Las tareas se cargarán dinámicamente desde el API -->
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <!-- Modal Nueva Tarea -->
      <div class="modal-overlay" id="newTaskModal">
        <div class="modal-container">
          <div class="modal-header">
            <h3>Crear Nueva Tarea</h3>
            <button class="modal-close" id="closeModalBtn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <p class="modal-subtitle">Complete los datos de la nueva tarea</p>
            
            <form class="task-form" id="taskForm">
              <div class="form-row">
                <div class="form-group">
                  <label>Nombre de la Tarea</label>
                  <input type="text" id="taskTitle" placeholder="Ej: Implementación sistema" required />
                </div>
                <div class="form-group">
                  <label>Área</label>
                  <select id="taskArea" required>
                    <option value="">Cargando áreas...</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Descripción</label>
                <textarea id="taskDescription" rows="3" placeholder="Descripción detallada de la tarea"></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Tiempo Estimado (días)</label>
                  <input type="number" id="taskEstimatedDays" placeholder="10" min="1" />
                </div>
                <div class="form-group">
                  <label>Responsable</label>
                  <select id="taskResponsible">
                    <option value="">Cargando usuarios...</option>
                  </select>
                </div>
              </div>

              <div class="form-row" id="taskStatusRow" style="display: none;">
                <div class="form-group">
                  <label>Estado</label>
                  <select id="taskStatus">
                    <option value="pendiente">Pendiente</option>
                    <option value="en_progreso">En Progreso</option>
                    <option value="completada">Completada</option>
                    <option value="retrasada">Retrasada</option>
                    <option value="cancelada">Cancelada</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Prioridad</label>
                  <select id="taskPriority">
                    <option value="baja">Baja</option>
                    <option value="media">Media</option>
                    <option value="alta">Alta</option>
                  </select>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" id="cancelModalBtn">Cancelar</button>
            <button class="btn-primary" id="createTaskBtn">Crear Tarea</button>
          </div>
        </div>
      </div>

      <!-- Modal Ver Detalles de Tarea -->
      <div class="modal-overlay" id="taskDetailsModal">
        <div class="modal-container modal-details">
          <div class="modal-header">
            <h3>Detalles de la Tarea</h3>
            <button class="modal-close" id="closeDetailsModalBtn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="task-details-grid">
              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2v20M2 12h20"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>ID</label>
                  <p id="detailId">-</p>
                </div>
              </div>

              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 11l3 3L22 4"/>
                    <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Nombre de la Tarea</label>
                  <p id="detailTitle">-</p>
                </div>
              </div>

              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="7" height="7" rx="1"/>
                    <rect x="14" y="3" width="7" height="7" rx="1"/>
                    <rect x="14" y="14" width="7" height="7" rx="1"/>
                    <rect x="3" y="14" width="7" height="7" rx="1"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Área</label>
                  <p id="detailArea">-</p>
                </div>
              </div>

              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="8" r="4"/>
                    <path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Responsable</label>
                  <p id="detailAssigned">-</p>
                </div>
              </div>

              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Tiempo Estimado</label>
                  <p id="detailEstimated">-</p>
                </div>
              </div>

              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Tiempo Real</label>
                  <p id="detailActual">-</p>
                </div>
              </div>

              <div class="detail-card full-width">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Descripción</label>
                  <p id="detailDescription">-</p>
                </div>
              </div>

              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 16v-4M12 8h.01"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Estado</label>
                  <p id="detailStatus">-</p>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" id="closeDetailsBtn">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  `;
}

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

// Función para verificar si el usuario puede editar tareas completas
function canEditFullTask(): boolean {
  const role = getUserRole();
  return role === 'super_admin' || role === 'gerente' || role === 'supervisor';
}

// Función para cargar áreas dinámicamente
async function loadAreasForTaskForm() {
  try {
    const response = await api.getAreas();
    const areas = response.areas || [];
    
    // Filtrar solo áreas activas
    const activeAreas = areas.filter((area: any) => area.status === 'active');
    
    const taskAreaSelect = document.getElementById('taskArea') as HTMLSelectElement;
    if (taskAreaSelect) {
      taskAreaSelect.innerHTML = '<option value="">Seleccionar área</option>';
      activeAreas.forEach((area: any) => {
        const option = document.createElement('option');
        option.value = area.name;
        option.textContent = area.name;
        taskAreaSelect.appendChild(option);
      });
    }
  } catch (error) {
    console.error('Error al cargar áreas:', error);
    const taskAreaSelect = document.getElementById('taskArea') as HTMLSelectElement;
    if (taskAreaSelect) {
      taskAreaSelect.innerHTML = '<option value="">Error al cargar áreas</option>';
    }
  }
}

// Función para cargar usuarios dinámicamente
async function loadUsersForTaskForm() {
  try {
    const response = await api.getUsers();
    const users = response.users || [];
    
    // Filtrar solo usuarios activos
    const activeUsers = users.filter((user: any) => user.status === 'active');
    
    const taskResponsibleSelect = document.getElementById('taskResponsible') as HTMLSelectElement;
    if (taskResponsibleSelect) {
      taskResponsibleSelect.innerHTML = '<option value="">Asignar responsable</option>';
      activeUsers.forEach((user: any) => {
        const option = document.createElement('option');
        option.value = user.email; // Usamos email como identificador
        option.textContent = user.full_name;
        taskResponsibleSelect.appendChild(option);
      });
    }
  } catch (error) {
    console.error('Error al cargar usuarios:', error);
    const taskResponsibleSelect = document.getElementById('taskResponsible') as HTMLSelectElement;
    if (taskResponsibleSelect) {
      taskResponsibleSelect.innerHTML = '<option value="">Error al cargar usuarios</option>';
    }
  }
}

// Función para cargar tareas desde el API
async function loadTasks() {
  try {
    const response = await api.getTasks();
    const tasks = response.tasks || [];
    
    // Actualizar contador
    const tasksCount = document.getElementById('tasksCount');
    if (tasksCount) {
      tasksCount.textContent = `Total: ${tasks.length} tareas`;
    }

    // Renderizar tareas
    const tbody = document.getElementById('tasksTableBody');
    if (!tbody) return;

    if (tasks.length === 0) {
      tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 40px;">No hay tareas registradas</td></tr>';
      return;
    }

    tbody.innerHTML = tasks.map((task: any) => {
      const statusMap: any = {
        'pendiente': { class: 'status-pending', label: 'Pendiente' },
        'en_progreso': { class: 'status-progress', label: 'En Progreso' },
        'completada': { class: 'status-completed', label: 'Completada' },
        'retrasada': { class: 'status-blocked', label: 'Retrasada' },
        'cancelada': { class: 'status-blocked', label: 'Cancelada' }
      };

      const status = statusMap[task.status] || { class: 'status-pending', label: task.status };
      const estimatedDays = task.estimated_hours ? (task.estimated_hours / 8).toFixed(1) + 'd' : '-';
      const actualDays = task.actual_hours ? (task.actual_hours / 8).toFixed(1) + 'd' : '-';
      
      // Calcular riesgo simple basado en complejidad
      let riskClass = 'risk-low';
      let riskLabel = 'Bajo';
      if (task.complexity_score >= 8) {
        riskClass = 'risk-critical';
        riskLabel = 'Crítico';
      } else if (task.complexity_score >= 6) {
        riskClass = 'risk-high';
        riskLabel = 'Alto';
      } else if (task.complexity_score >= 4) {
        riskClass = 'risk-medium';
        riskLabel = 'Medio';
      }

      return `
        <tr>
          <td class="task-id">${task.id}</td>
          <td class="task-name">${task.title}</td>
          <td><span class="area-badge">${task.area || 'Sin área'}</span></td>
          <td class="task-responsibles">
            <div>${task.assigned_name || task.assigned_to || 'Sin asignar'}</div>
          </td>
          <td>${estimatedDays}</td>
          <td>${actualDays}</td>
          <td><span class="status-badge ${status.class}">${status.label}</span></td>
          <td><span class="risk-badge ${riskClass}">${riskLabel}</span></td>
          <td class="task-actions">
            <button class="btn-icon btn-view-task" 
              data-id="${task.id}"
              data-title="${task.title}"
              data-area="${task.area || 'Sin área'}"
              data-description="${task.description || 'Sin descripción'}"
              data-status="${task.status}"
              data-assigned="${task.assigned_name || task.assigned_to || 'Sin asignar'}"
              data-estimated="${estimatedDays}"
              data-actual="${actualDays}"
              title="Ver detalles">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <circle cx="9" cy="9" r="2" stroke="currentColor" stroke-width="1.5"/>
                <path d="M1 9s3-6 8-6 8 6 8 6-3 6-8 6-8-6-8-6z" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </button>
            ${getUserRole() === 'super_admin' || getUserRole() === 'gerente' || getUserRole() === 'supervisor' ? `
              <button class="btn-icon btn-edit-task" 
                data-id="${task.id}"
                data-title="${task.title}"
                data-area="${task.area || ''}"
                data-description="${task.description || ''}"
                data-estimated-hours="${task.estimated_hours || ''}"
                data-assigned="${task.assigned_to || ''}"
                data-status="${task.status || 'pendiente'}"
                data-priority="${task.priority || 'media'}"
                title="Editar">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                  <path d="M12 3l3 3-9 9H3v-3l9-9z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            ` : `
              <select class="status-quick-change" data-task-id="${task.id}" data-current-status="${task.status}">
                <option value="">Cambiar estado</option>
                ${task.status === 'pendiente' ? '<option value="en_progreso">▶ Iniciar</option>' : ''}
                ${task.status === 'en_progreso' ? '<option value="completada">✓ Completar</option>' : ''}
                ${task.status === 'pendiente' || task.status === 'en_progreso' ? '<option value="cancelada">✗ Cancelar</option>' : ''}
              </select>
            `}
          </td>
        </tr>
      `;
    }).join('');

    // Agregar event listeners a los botones de acción
    attachTaskActionListeners();

  } catch (error) {
    console.error('Error al cargar tareas:', error);
    const tbody = document.getElementById('tasksTableBody');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 40px; color: red;">Error al cargar tareas</td></tr>';
    }
  }
}

// Función para agregar event listeners a los botones de acción
function attachTaskActionListeners() {
  // Botones de ver detalles
  const viewButtons = document.querySelectorAll('.btn-view-task');
  viewButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const btn = e.currentTarget as HTMLElement;
      const taskData = {
        id: btn.dataset.id!,
        title: btn.dataset.title!,
        area: btn.dataset.area!,
        description: btn.dataset.description!,
        status: btn.dataset.status!,
        assigned: btn.dataset.assigned!,
        estimated: btn.dataset.estimated!,
        actual: btn.dataset.actual!
      };
      
      showTaskDetails(taskData);
    });
  });

  // Botones de editar
  const editButtons = document.querySelectorAll('.btn-edit-task');
  editButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const btn = e.currentTarget as HTMLElement;
      const taskData = {
        id: parseInt(btn.dataset.id!),
        title: btn.dataset.title!,
        area: btn.dataset.area!,
        description: btn.dataset.description!,
        estimatedHours: parseFloat(btn.dataset.estimatedHours!) || 0,
        assigned: btn.dataset.assigned!,
        status: btn.dataset.status!,
        priority: btn.dataset.priority!
      };
      
      openEditTaskModal(taskData);
    });
  });

  // Selectores de cambio rápido de estado (para colaboradores)
  const statusSelects = document.querySelectorAll('.status-quick-change');
  statusSelects.forEach(select => {
    select.addEventListener('change', async (e) => {
      const selectEl = e.currentTarget as HTMLSelectElement;
      const taskId = selectEl.dataset.taskId;
      const newStatus = selectEl.value;

      if (!newStatus) return;

      try {
        // Confirmar cambio
        if (confirm(`¿Cambiar estado de la tarea a "${newStatus}"?`)) {
          // Actualizar solo el estado de la tarea
          await api.updateTask(parseInt(taskId!), { status: newStatus });
          
          // Recargar tareas
          await loadTasks();
          
          alert('Estado actualizado correctamente');
        } else {
          // Restaurar valor anterior
          selectEl.value = '';
        }
      } catch (error) {
        console.error('Error al cambiar estado:', error);
        alert('Error al cambiar el estado de la tarea');
        selectEl.value = '';
      }
    });
  });
}

// Función para mostrar detalles de la tarea
// Función para mostrar detalles de la tarea en modal
function showTaskDetails(task: any) {
  // Poblar datos en el modal
  const detailId = document.getElementById('detailId');
  const detailTitle = document.getElementById('detailTitle');
  const detailArea = document.getElementById('detailArea');
  const detailDescription = document.getElementById('detailDescription');
  const detailStatus = document.getElementById('detailStatus');
  const detailAssigned = document.getElementById('detailAssigned');
  const detailEstimated = document.getElementById('detailEstimated');
  const detailActual = document.getElementById('detailActual');

  if (detailId) detailId.textContent = `#${task.id}`;
  if (detailTitle) detailTitle.textContent = task.title;
  if (detailArea) detailArea.textContent = task.area;
  if (detailDescription) detailDescription.textContent = task.description || 'Sin descripción';
  if (detailAssigned) detailAssigned.textContent = task.assigned;
  if (detailEstimated) detailEstimated.textContent = task.estimated;
  if (detailActual) detailActual.textContent = task.actual;
  
  // Formatear estado con badge
  if (detailStatus) {
    const statusMap: any = {
      'pendiente': { class: 'status-pending', label: 'Pendiente' },
      'en_progreso': { class: 'status-progress', label: 'En Progreso' },
      'completada': { class: 'status-completed', label: 'Completada' },
      'retrasada': { class: 'status-blocked', label: 'Retrasada' },
      'cancelada': { class: 'status-blocked', label: 'Cancelada' }
    };
    const status = statusMap[task.status] || { class: 'status-pending', label: task.status };
    detailStatus.innerHTML = `<span class="status-badge ${status.class}">${status.label}</span>`;
  }

  // Mostrar modal
  const modal = document.getElementById('taskDetailsModal');
  if (modal) {
    modal.classList.add('active');
  }
}

// Función para abrir modal de edición de tarea
function openEditTaskModal(task: any) {
  const modal = document.getElementById('newTaskModal');
  if (!modal) return;

  // Cambiar título del modal
  const modalTitle = modal.querySelector('.modal-header h3');
  if (modalTitle) modalTitle.textContent = 'Editar Tarea';

  // Cargar áreas y usuarios
  loadAreasForTaskForm();
  loadUsersForTaskForm();

  // Esperar un momento para que se carguen los selects
  setTimeout(() => {
    // Rellenar formulario
    (document.getElementById('taskTitle') as HTMLInputElement).value = task.title;
    (document.getElementById('taskArea') as HTMLSelectElement).value = task.area;
    (document.getElementById('taskDescription') as HTMLTextAreaElement).value = task.description;
    (document.getElementById('taskEstimatedDays') as HTMLInputElement).value = (task.estimatedHours / 8).toString();
    (document.getElementById('taskResponsible') as HTMLSelectElement).value = task.assigned;

    // Mostrar campo de estado solo al editar y si tiene permisos
    const statusRow = document.getElementById('taskStatusRow');
    if (statusRow && canEditFullTask()) {
      statusRow.style.display = 'flex';
      (document.getElementById('taskStatus') as HTMLSelectElement).value = task.status || 'pendiente';
      (document.getElementById('taskPriority') as HTMLSelectElement).value = task.priority || 'media';
    }

    // Guardar ID y estado en el formulario
    const titleInput = document.getElementById('taskTitle') as HTMLInputElement;
    titleInput.dataset.editing = 'true';
    titleInput.dataset.taskId = task.id.toString();
    titleInput.dataset.currentStatus = task.status;
  }, 300);

  // Cambiar texto del botón
  const submitBtn = document.getElementById('createTaskBtn') as HTMLButtonElement;
  if (submitBtn) submitBtn.textContent = 'Actualizar Tarea';

  modal.classList.add('active');
}

// Función para cerrar modal y resetear estado
function resetTaskModal() {
  const modal = document.getElementById('newTaskModal');
  const modalTitle = modal?.querySelector('.modal-header h3');
  if (modalTitle) modalTitle.textContent = 'Crear Nueva Tarea';

  const titleInput = document.getElementById('taskTitle') as HTMLInputElement;
  if (titleInput) {
    delete titleInput.dataset.editing;
    delete titleInput.dataset.taskId;
    delete titleInput.dataset.currentStatus;
  }

  // Ocultar campo de estado
  const statusRow = document.getElementById('taskStatusRow');
  if (statusRow) statusRow.style.display = 'none';

  const submitBtn = document.getElementById('createTaskBtn') as HTMLButtonElement;
  if (submitBtn) submitBtn.textContent = 'Crear Tarea';

  const form = document.getElementById('taskForm') as HTMLFormElement;
  form?.reset();
}

export function initTasks() {
  // Inicializar AI Assistant
  initAIAssistant();

  // Cargar tareas desde el API
  loadTasks();

  // Modal handlers
  const newTaskBtn = document.getElementById('newTaskBtn');
  const modal = document.getElementById('newTaskModal');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const cancelModalBtn = document.getElementById('cancelModalBtn');
  const createTaskBtn = document.getElementById('createTaskBtn');

  if (newTaskBtn && modal) {
    newTaskBtn.addEventListener('click', () => {
      modal.classList.add('active');
      // Cargar áreas y usuarios al abrir el modal
      loadAreasForTaskForm();
      loadUsersForTaskForm();
    });
  }

  const closeModal = () => {
    modal?.classList.remove('active');
    resetTaskModal();
  };

  closeModalBtn?.addEventListener('click', closeModal);
  cancelModalBtn?.addEventListener('click', closeModal);

  // Cerrar al hacer click fuera
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  // Modal de detalles handlers
  const detailsModal = document.getElementById('taskDetailsModal');
  const closeDetailsModalBtn = document.getElementById('closeDetailsModalBtn');
  const closeDetailsBtn = document.getElementById('closeDetailsBtn');

  const closeDetailsModal = () => {
    detailsModal?.classList.remove('active');
  };

  closeDetailsModalBtn?.addEventListener('click', closeDetailsModal);
  closeDetailsBtn?.addEventListener('click', closeDetailsModal);

  // Cerrar modal detalles al hacer click fuera
  detailsModal?.addEventListener('click', (e) => {
    if (e.target === detailsModal) {
      closeDetailsModal();
    }
  });

  // Crear/Editar tarea
  createTaskBtn?.addEventListener('click', async () => {
    try {
      // Obtener valores del formulario
      const titleInput = document.getElementById('taskTitle') as HTMLInputElement;
      const title = titleInput?.value;
      const area = (document.getElementById('taskArea') as HTMLSelectElement)?.value;
      const description = (document.getElementById('taskDescription') as HTMLTextAreaElement)?.value;
      const estimatedDays = (document.getElementById('taskEstimatedDays') as HTMLInputElement)?.value;
      const responsible = (document.getElementById('taskResponsible') as HTMLSelectElement)?.value;

      // Verificar si estamos editando
      const isEditing = titleInput.dataset.editing === 'true';
      const taskId = titleInput.dataset.taskId;

      // Validar campos requeridos
      if (!title || !area) {
        alert('Por favor complete los campos requeridos: Nombre y Área');
        return;
      }

      // Deshabilitar botón mientras se procesa
      (createTaskBtn as HTMLButtonElement).disabled = true;
      createTaskBtn.textContent = isEditing ? 'Actualizando...' : 'Creando...';

      // Preparar datos de la tarea
      const taskStatus = (document.getElementById('taskStatus') as HTMLSelectElement)?.value || 'pendiente';
      const taskPriority = (document.getElementById('taskPriority') as HTMLSelectElement)?.value || 'media';
      
      const taskData: any = {
        title,
        area,
        description: description || '',
        priority: isEditing ? taskPriority : 'media',
        estimated_hours: estimatedDays ? parseFloat(estimatedDays) * 8 : null,
        assigned_to: responsible || null,
        status: isEditing ? taskStatus : 'pendiente'
      };

      if (isEditing && taskId) {
        // Actualizar tarea existente
        await api.updateTask(parseInt(taskId), taskData);
        alert('¡Tarea actualizada exitosamente!');
      } else {
        // Crear nueva tarea
        await api.createTask(taskData);
        alert('¡Tarea creada exitosamente!');
      }

      // Limpiar formulario
      (document.getElementById('taskForm') as HTMLFormElement)?.reset();

      // Resetear modal
      resetTaskModal();

      // Cerrar modal
      closeModal();

      // Recargar las tareas
      loadTasks();

    } catch (error) {
      console.error('Error al crear tarea:', error);
      alert('Error al crear la tarea: ' + (error as Error).message);
    } finally {
      // Rehabilitar botón
      if (createTaskBtn) {
        (createTaskBtn as HTMLButtonElement).disabled = false;
        createTaskBtn.textContent = 'Crear Tarea';
      }
    }
  });

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
