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
                    <option value="">Seleccionar área</option>
                    <option value="TI">TI</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Operaciones">Operaciones</option>
                    <option value="RRHH">RRHH</option>
                    <option value="Ventas">Ventas</option>
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
                    <option value="">Asignar responsable</option>
                    <option value="P001">Juan Pérez</option>
                    <option value="P002">Ana García</option>
                    <option value="P003">María López</option>
                    <option value="P004">Carlos Ruiz</option>
                    <option value="P005">Laura Díaz</option>
                    <option value="P006">Pedro Sánchez</option>
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
    </div>
  `;
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
            <div>${task.assigned_to || 'Sin asignar'}</div>
          </td>
          <td>${estimatedDays}</td>
          <td>${actualDays}</td>
          <td><span class="status-badge ${status.class}">${status.label}</span></td>
          <td><span class="risk-badge ${riskClass}">${riskLabel}</span></td>
          <td class="task-actions">
            <button class="btn-icon" title="Ver detalles">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <circle cx="9" cy="9" r="2" stroke="currentColor" stroke-width="1.5"/>
                <path d="M1 9s3-6 8-6 8 6 8 6-3 6-8 6-8-6-8-6z" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </button>
            <button class="btn-icon" title="Editar">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M12 3l3 3-9 9H3v-3l9-9z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </td>
        </tr>
      `;
    }).join('');

  } catch (error) {
    console.error('Error al cargar tareas:', error);
    const tbody = document.getElementById('tasksTableBody');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 40px; color: red;">Error al cargar tareas</td></tr>';
    }
  }
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
    });
  }

  const closeModal = () => {
    modal?.classList.remove('active');
  };

  closeModalBtn?.addEventListener('click', closeModal);
  cancelModalBtn?.addEventListener('click', closeModal);

  // Cerrar al hacer click fuera
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  // Crear tarea
  createTaskBtn?.addEventListener('click', async () => {
    try {
      // Obtener valores del formulario
      const title = (document.getElementById('taskTitle') as HTMLInputElement)?.value;
      const area = (document.getElementById('taskArea') as HTMLSelectElement)?.value;
      const description = (document.getElementById('taskDescription') as HTMLTextAreaElement)?.value;
      const estimatedDays = (document.getElementById('taskEstimatedDays') as HTMLInputElement)?.value;
      const responsible = (document.getElementById('taskResponsible') as HTMLSelectElement)?.value;

      // Validar campos requeridos
      if (!title || !area) {
        alert('Por favor complete los campos requeridos: Nombre y Área');
        return;
      }

      // Deshabilitar botón mientras se crea
      createTaskBtn.disabled = true;
      createTaskBtn.textContent = 'Creando...';

      // Crear la tarea
      const taskData = {
        title,
        area,
        description: description || '',
        priority: 'media',
        estimated_hours: estimatedDays ? parseFloat(estimatedDays) * 8 : null, // Convertir días a horas
        assigned_to: responsible || null,
        status: 'pendiente'
      };

      await api.createTask(taskData);

      // Limpiar formulario
      (document.getElementById('taskForm') as HTMLFormElement)?.reset();

      // Cerrar modal
      closeModal();

      // Mostrar mensaje de éxito
      alert('¡Tarea creada exitosamente!');

      // Recargar las tareas sin recargar toda la página
      loadTasks();

    } catch (error) {
      console.error('Error al crear tarea:', error);
      alert('Error al crear la tarea: ' + (error as Error).message);
    } finally {
      // Rehabilitar botón
      if (createTaskBtn) {
        createTaskBtn.disabled = false;
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
