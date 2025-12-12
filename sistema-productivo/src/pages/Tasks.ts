import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { api, API_URL } from '../utils/api';

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
          <!-- Vista de Proyectos (inicial) -->
          <div id="projectsView">
            <div class="section-header">
              <div class="section-info">
                <h2 class="section-title">Gestión de Proyectos</h2>
                <p class="section-description">Selecciona un proyecto para ver y gestionar sus tareas</p>
              </div>
              <div class="section-actions">
                <button class="btn-secondary" id="newProjectBtn">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  Nuevo Proyecto
                </button>
              </div>
            </div>

            <!-- Grid de proyectos -->
            <div class="projects-grid" id="projectsGrid">
              <!-- Los proyectos se cargarán dinámicamente -->
            </div>
          </div>

          <!-- Vista de Tareas (se muestra al seleccionar un proyecto) -->
          <div id="tasksView" style="display: none;">
            <div class="section-header">
              <div class="section-info">
                <button class="btn-back" id="backToProjectsBtn">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M12 4l-8 6 8 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Volver a Proyectos
                </button>
                <h2 class="section-title" id="projectTitleHeader">Proyecto</h2>
                <p class="section-description" id="projectDescriptionHeader">Gestión de tareas del proyecto</p>
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
                <input type="text" id="taskSearchInput" placeholder="Buscar por nombre de tarea..." />
              </div>
              <select class="filter-select" id="statusFilter">
                <option value="">Todos los estados</option>
                <option value="pendiente">Pendiente</option>
                <option value="en_progreso">En Progreso</option>
                <option value="completada">Completada</option>
                <option value="retrasada">Retrasada</option>
                <option value="cancelada">Cancelada</option>
              </select>
              <select class="filter-select" id="priorityFilter">
                <option value="">Todas las prioridades</option>
                <option value="baja">Baja</option>
                <option value="media">Media</option>
                <option value="alta">Alta</option>
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

      <!-- Modal Nuevo Proyecto -->
      <div class="modal-overlay" id="newProjectModal">
        <div class="modal-container">
          <div class="modal-header">
            <h3>Crear Nuevo Proyecto</h3>
            <button class="modal-close" id="closeProjectModalBtn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <p class="modal-subtitle">Complete los datos del nuevo proyecto</p>
            
            <form id="projectForm" class="task-form">
              <div class="form-row">
                <div class="form-group">
                  <label for="projectId">ID del Proyecto *</label>
                  <input type="text" id="projectId" placeholder="PROJ-2025-XXX" required />
                  <small>Ejemplo: PROJ-2025-004</small>
                </div>
                <div class="form-group">
                  <label for="projectName">Nombre del Proyecto *</label>
                  <input type="text" id="projectName" placeholder="Nombre descriptivo" required />
                </div>
              </div>

              <div class="form-group">
                <label for="projectDescription">Descripción</label>
                <textarea id="projectDescription" rows="3" placeholder="Describe el objetivo del proyecto..."></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="projectStartDate">Fecha de Inicio</label>
                  <input type="date" id="projectStartDate" />
                </div>
                <div class="form-group">
                  <label for="projectEndDate">Fecha de Finalización</label>
                  <input type="date" id="projectEndDate" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="projectStatus">Estado</label>
                  <select id="projectStatus">
                    <option value="planning">Planificación</option>
                    <option value="in_progress">En Progreso</option>
                    <option value="on_hold">En Pausa</option>
                    <option value="completed">Completado</option>
                    <option value="cancelled">Cancelado</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="projectPriority">Prioridad</label>
                  <select id="projectPriority">
                    <option value="low">Baja</option>
                    <option value="medium" selected>Media</option>
                    <option value="high">Alta</option>
                    <option value="critical">Crítica</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="projectManager">Responsable del Proyecto *</label>
                <select id="projectManager" required>
                  <option value="">Seleccionar responsable...</option>
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button class="btn-secondary" id="cancelProjectBtn">Cancelar</button>
            <button class="btn-primary" id="createProjectBtn">Crear Proyecto</button>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Estado global
let currentProjectId: string | null = null;
let allTasks: any[] = [];

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

// Función para cargar proyectos desde el API
async function loadProjects() {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.error('No hay token de autenticación');
      window.location.href = '/login';
      return;
    }
    
    console.log('Cargando proyectos desde:', `${API_URL}/projects?include_stats=true`);
    const response = await fetch(`${API_URL}/projects?include_stats=true`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Respuesta recibida:', response.status, response.statusText);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error del servidor:', errorText);
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Proyectos cargados:', data);
    const projects = data.projects || [];
    
    const projectsGrid = document.getElementById('projectsGrid');
    if (!projectsGrid) return;
    
    if (projects.length === 0) {
      projectsGrid.innerHTML = `
        <div class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
          </svg>
          <h3>No hay proyectos disponibles</h3>
          <p>Crea un nuevo proyecto para comenzar</p>
        </div>
      `;
      return;
    }
    
    projectsGrid.innerHTML = projects.map((project: any) => {
      const stats = project.stats || {};
      const completion = stats.completion_percentage || 0;
      const statusClass = project.status === 'completed' ? 'completed' : 
                         project.status === 'in_progress' ? 'in-progress' : 
                         project.status === 'on_hold' ? 'on-hold' : 'planning';
      const priorityClass = project.priority === 'critical' ? 'critical' : 
                           project.priority === 'high' ? 'high' : 
                           project.priority === 'medium' ? 'medium' : 'low';
      
      return `
        <div class="project-card" data-project-id="${project.project_id}">
          <div class="project-header">
            <div class="project-title">
              <h3>${project.name}</h3>
              <span class="project-id">${project.project_id}</span>
            </div>
            <div class="project-header-actions">
              <button class="btn-icon-small btn-edit-project" data-project-id="${project.project_id}" title="Editar proyecto">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <span class="priority-badge priority-${priorityClass}">${project.priority}</span>
            </div>
          </div>
          
          <p class="project-description">${project.description || 'Sin descripción'}</p>
          
          ${project.manager_name ? `
          <div class="project-manager">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <span>Responsable: <strong>${project.manager_name}</strong></span>
          </div>
          ` : ''}
          
          <div class="project-stats">
            <div class="stat">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 11l3 3L22 4M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
              </svg>
              <span>${stats.total_tasks || 0} tareas</span>
            </div>
            <div class="stat">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8z"/>
              </svg>
              <span>${stats.team_size || 0} miembros</span>
            </div>
            <div class="stat">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              <span>${stats.dependencies_count || 0} dependencias</span>
            </div>
          </div>
          
          <div class="project-progress">
            <div class="progress-header">
              <span>Progreso</span>
              <span class="progress-percentage">${completion.toFixed(0)}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: ${completion}%"></div>
            </div>
          </div>
          
          <div class="project-footer">
            <span class="status-badge status-${statusClass}">${translateStatus(project.status)}</span>
            <button class="btn-view-tasks" data-project-id="${project.project_id}">
              Ver Tareas
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>
      `;
    }).join('');
    
    // Event listeners para ver tareas de cada proyecto
    document.querySelectorAll('.btn-view-tasks').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const projectId = (e.currentTarget as HTMLElement).dataset.projectId;
        if (projectId) {
          showProjectTasks(projectId);
        }
      });
    });
    
    // Event listeners para editar proyectos
    document.querySelectorAll('.btn-edit-project').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.stopPropagation();
        const projectId = (e.currentTarget as HTMLElement).dataset.projectId;
        if (projectId) {
          const project = projects.find((p: any) => p.project_id === projectId);
          if (project) {
            await openEditProjectModal(project);
          }
        }
      });
    });
    
  } catch (error) {
    console.error('Error al cargar proyectos:', error);
    const projectsGrid = document.getElementById('projectsGrid');
    if (projectsGrid) {
      projectsGrid.innerHTML = `
        <div class="error-state">
          <p>Error al cargar proyectos. Por favor, intenta nuevamente.</p>
        </div>
      `;
    }
  }
}

// Función para traducir estados
function translateStatus(status: string): string {
  const translations: any = {
    'planning': 'Planificación',
    'in_progress': 'En Progreso',
    'completed': 'Completado',
    'on_hold': 'En Pausa',
    'cancelled': 'Cancelado'
  };
  return translations[status] || status;
}

// Función para mostrar tareas de un proyecto
async function showProjectTasks(projectId: string) {
  try {
    currentProjectId = projectId;
    
    // Obtener detalles del proyecto
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.error('No hay token de autenticación');
      window.location.href = '/login';
      return;
    }
    
    const projectResponse = await fetch(`${API_URL}/projects/${projectId}?include_tasks=true`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!projectResponse.ok) {
      const errorText = await projectResponse.text();
      console.error('Error al obtener proyecto:', errorText);
      throw new Error(`HTTP error! status: ${projectResponse.status}`);
    }
    
    const projectData = await projectResponse.json();
    const project = projectData.project;
    
    // Actualizar header
    const projectTitleHeader = document.getElementById('projectTitleHeader');
    const projectDescriptionHeader = document.getElementById('projectDescriptionHeader');
    if (projectTitleHeader) projectTitleHeader.textContent = project.name;
    if (projectDescriptionHeader) projectDescriptionHeader.textContent = project.description || 'Gestión de tareas del proyecto';
    
    // Obtener todas las tareas del proyecto
    const tasksResponse = await api.getTasks();
    allTasks = (tasksResponse.tasks || []).filter((task: any) => task.project_id === projectId);
    
    // Cambiar a vista de tareas
    const projectsView = document.getElementById('projectsView');
    const tasksView = document.getElementById('tasksView');
    if (projectsView) projectsView.style.display = 'none';
    if (tasksView) tasksView.style.display = 'block';
    
    // Renderizar tareas
    renderTasks(allTasks);
    
  } catch (error) {
    console.error('Error al cargar tareas del proyecto:', error);
    alert('Error al cargar las tareas del proyecto');
  }
}

// Función para volver a la vista de proyectos
function showProjectsView() {
  currentProjectId = null;
  allTasks = [];
  
  const projectsView = document.getElementById('projectsView');
  const tasksView = document.getElementById('tasksView');
  if (projectsView) projectsView.style.display = 'block';
  if (tasksView) tasksView.style.display = 'none';
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

// Función para cargar tareas desde el API (filtradas por proyecto)
async function loadTasks() {
  if (!currentProjectId) {
    // Si no hay proyecto seleccionado, cargar vista de proyectos
    await loadProjects();
    return;
  }
  
  try {
    const response = await api.getTasks();
    allTasks = (response.tasks || []).filter((task: any) => task.project_id === currentProjectId);
    renderTasks(allTasks);
  } catch (error) {
    console.error('Error al cargar tareas:', error);
    const tbody = document.querySelector('.tasks-table tbody');
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 2rem;">
            <p>Error al cargar tareas. Por favor, intenta nuevamente.</p>
          </td>
        </tr>
      `;
    }
  }
}

// Función para renderizar tareas en la tabla
function renderTasks(tasks: any[]) {
  const tbody = document.querySelector('.tasks-table tbody');
  if (!tbody) return;
  
  if (tasks.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 2rem;">
          <p>No hay tareas en este proyecto.</p>
          <p style="color: var(--text-secondary); margin-top: 0.5rem;">Crea una nueva tarea para comenzar.</p>
        </td>
      </tr>
    `;
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
    
    const priorityMap: any = {
      'baja': { class: 'priority-low', label: 'Baja' },
      'media': { class: 'priority-medium', label: 'Media' },
      'alta': { class: 'priority-high', label: 'Alta' }
    };
    
    const status = statusMap[task.status] || { class: 'status-pending', label: task.status };
    const priority = priorityMap[task.priority] || { class: 'priority-medium', label: task.priority };
    
    return `
      <tr data-task-id="${task.id}">
        <td class="task-id-cell">#${task.id}</td>
        <td class="task-name-cell">
          <div class="task-name">
            <strong>${task.title}</strong>
            ${task.description ? `<span class="task-subtitle">${task.description.substring(0, 50)}${task.description.length > 50 ? '...' : ''}</span>` : ''}
          </div>
        </td>
        <td>${task.area || '-'}</td>
        <td><span class="status-badge ${status.class}">${status.label}</span></td>
        <td><span class="priority-badge ${priority.class}">${priority.label}</span></td>
        <td>${task.assigned_name || task.assigned_to || 'Sin asignar'}</td>
        <td class="actions-cell">
          <button class="btn-icon btn-view" data-task-id="${task.id}" title="Ver detalles">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
          </button>
          ${canEditFullTask() ? `
            <button class="btn-icon btn-edit" data-task-id="${task.id}" title="Editar">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="btn-icon btn-delete" data-task-id="${task.id}" title="Eliminar">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
              </svg>
            </button>
          ` : ''}
        </td>
      </tr>
    `;
  }).join('');
  
  // Event listeners para botones de acciones
  document.querySelectorAll('.btn-view').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const taskId = (e.currentTarget as HTMLElement).dataset.taskId;
      const task = tasks.find(t => t.id === parseInt(taskId || '0'));
      if (task) showTaskDetails(task);
    });
  });
  
  if (canEditFullTask()) {
    document.querySelectorAll('.btn-edit').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const taskId = (e.currentTarget as HTMLElement).dataset.taskId;
        const task = tasks.find(t => t.id === parseInt(taskId || '0'));
        if (task) openEditTaskModal(task);
      });
    });
    
    document.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const taskId = (e.currentTarget as HTMLElement).dataset.taskId;
        if (confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
          try {
            await api.deleteTask(parseInt(taskId || '0'));
            alert('Tarea eliminada exitosamente');
            loadTasks();
          } catch (error) {
            console.error('Error al eliminar tarea:', error);
            alert('Error al eliminar la tarea');
          }
        }
      });
    });
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

// Función para cargar gerentes/administradores para el select de responsable
async function loadManagersForProject() {
  try {
    const response = await api.getUsers();
    const users = response.users || [];
    
    // Filtrar solo gerentes y super_admin
    const managers = users.filter((user: any) => 
      user.role?.name === 'gerente' || user.role?.name === 'super_admin'
    );
    
    const managerSelect = document.getElementById('projectManager') as HTMLSelectElement;
    if (managerSelect) {
      managerSelect.innerHTML = '<option value="">Seleccionar responsable...</option>' +
        managers.map((user: any) => 
          `<option value="${user.email}">${user.full_name} (${user.role?.display_name || user.role?.name})</option>`
        ).join('');
    }
  } catch (error) {
    console.error('Error al cargar gerentes:', error);
  }
}

// Función para abrir modal de nuevo proyecto
function openNewProjectModal() {
  const modal = document.getElementById('newProjectModal');
  if (!modal) return;
  
  // Cambiar título
  const modalTitle = modal.querySelector('.modal-header h3');
  if (modalTitle) modalTitle.textContent = 'Crear Nuevo Proyecto';
  
  // Limpiar formulario
  const form = document.getElementById('projectForm') as HTMLFormElement;
  form?.reset();
  
  // Limpiar flag de edición
  const projectIdInput = document.getElementById('projectId') as HTMLInputElement;
  if (projectIdInput) {
    projectIdInput.removeAttribute('data-editing');
    projectIdInput.readOnly = false;
  }
  
  // Generar ID sugerido
  const today = new Date();
  const year = today.getFullYear();
  const nextNumber = String(Math.floor(Math.random() * 1000)).padStart(3, '0');
  const suggestedId = `PROJ-${year}-${nextNumber}`;
  projectIdInput.value = suggestedId;
  
  // Establecer fecha de inicio a hoy
  const startDateInput = document.getElementById('projectStartDate') as HTMLInputElement;
  if (startDateInput) {
    startDateInput.valueAsDate = today;
  }
  
  // Cargar gerentes
  loadManagersForProject();
  
  // Cambiar texto del botón
  const createBtn = document.getElementById('createProjectBtn');
  if (createBtn) createBtn.textContent = 'Crear Proyecto';
  
  // Mostrar modal
  modal.classList.add('active');
}

// Función para abrir modal en modo edición
async function openEditProjectModal(project: any) {
  const modal = document.getElementById('newProjectModal');
  if (!modal) return;
  
  // Cambiar título
  const modalTitle = modal.querySelector('.modal-header h3');
  if (modalTitle) modalTitle.textContent = 'Editar Proyecto';
  
  // Cargar gerentes primero
  await loadManagersForProject();
  
  // Esperar un momento para que se carguen los selects
  setTimeout(() => {
    // Rellenar formulario
    const projectIdInput = document.getElementById('projectId') as HTMLInputElement;
    if (projectIdInput) {
      projectIdInput.value = project.project_id;
      projectIdInput.readOnly = true; // No permitir cambiar el ID
      projectIdInput.setAttribute('data-editing', 'true');
    }
    
    (document.getElementById('projectName') as HTMLInputElement).value = project.name || '';
    (document.getElementById('projectDescription') as HTMLTextAreaElement).value = project.description || '';
    
    if (project.start_date) {
      (document.getElementById('projectStartDate') as HTMLInputElement).value = project.start_date;
    }
    if (project.expected_end_date) {
      (document.getElementById('projectEndDate') as HTMLInputElement).value = project.expected_end_date;
    }
    
    (document.getElementById('projectStatus') as HTMLSelectElement).value = project.status || 'planning';
    (document.getElementById('projectPriority') as HTMLSelectElement).value = project.priority || 'medium';
    
    // Seleccionar manager por ID
    if (project.manager_id) {
      const managerSelect = document.getElementById('projectManager') as HTMLSelectElement;
      // Buscar la opción que corresponde al manager
      for (let i = 0; i < managerSelect.options.length; i++) {
        const option = managerSelect.options[i];
        if (option.value) {
          // Necesitamos comparar por email, así que buscaremos el email del manager
          // Por ahora usamos el valor directamente
          managerSelect.selectedIndex = i;
          break;
        }
      }
    }
    
    // Cambiar texto del botón
    const createBtn = document.getElementById('createProjectBtn');
    if (createBtn) createBtn.textContent = 'Actualizar Proyecto';
  }, 100);
  
  // Mostrar modal
  modal.classList.add('active');
}

// Función para crear o actualizar proyecto
async function createProject() {
  try {
    const projectIdInput = document.getElementById('projectId') as HTMLInputElement;
    const projectId = projectIdInput?.value;
    const isEditing = projectIdInput?.getAttribute('data-editing') === 'true';
    
    const name = (document.getElementById('projectName') as HTMLInputElement)?.value;
    const description = (document.getElementById('projectDescription') as HTMLTextAreaElement)?.value;
    const startDate = (document.getElementById('projectStartDate') as HTMLInputElement)?.value;
    const endDate = (document.getElementById('projectEndDate') as HTMLInputElement)?.value;
    const status = (document.getElementById('projectStatus') as HTMLSelectElement)?.value;
    const priority = (document.getElementById('projectPriority') as HTMLSelectElement)?.value;
    const managerEmail = (document.getElementById('projectManager') as HTMLSelectElement)?.value;
    
    // Validar campos requeridos
    if (!projectId || !name || !managerEmail) {
      alert('Por favor complete los campos requeridos: ID, Nombre y Responsable');
      return;
    }
    
    // Obtener el ID del usuario por su email
    const usersResponse = await api.getUsers();
    const manager = usersResponse.users.find((u: any) => u.email === managerEmail);
    
    if (!manager) {
      alert('No se encontró el usuario responsable');
      return;
    }
    
    const projectData: any = {
      project_id: projectId,
      name: name,
      description: description || null,
      start_date: startDate || null,
      expected_end_date: endDate || null,
      status: status || 'planning',
      priority: priority || 'medium',
      manager_id: manager.id
    };
    
    const token = localStorage.getItem('access_token');
    const url = isEditing ? `${API_URL}/projects/${projectId}` : `${API_URL}/projects`;
    const method = isEditing ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
      method: method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(projectData)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Error al ${isEditing ? 'actualizar' : 'crear'} proyecto`);
    }
    
    const data = await response.json();
    console.log(`Proyecto ${isEditing ? 'actualizado' : 'creado'}:`, data);
    
    alert(`¡Proyecto ${isEditing ? 'actualizado' : 'creado'} exitosamente!`);
    
    // Cerrar modal
    const modal = document.getElementById('newProjectModal');
    modal?.classList.remove('active');
    
    // Recargar lista de proyectos
    loadProjects();
    
  } catch (error: any) {
    console.error('Error al procesar proyecto:', error);
    alert('Error: ' + error.message);
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
        status: isEditing ? taskStatus : 'pendiente',
        project_id: currentProjectId // Asignar al proyecto actual
      };

      if (isEditing && taskId) {
        // Actualizar tarea existente
        await api.updateTask(parseInt(taskId), taskData);
        alert('¡Tarea actualizada exitosamente!');
      } else {
        // Crear nueva tarea
        if (!currentProjectId) {
          alert('Debes seleccionar un proyecto primero');
          return;
        }
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
  
  // Botón volver a proyectos
  const backToProjectsBtn = document.getElementById('backToProjectsBtn');
  if (backToProjectsBtn) {
    backToProjectsBtn.addEventListener('click', () => {
      showProjectsView();
    });
  }
  
  // Filtros de búsqueda
  const searchInput = document.getElementById('taskSearchInput');
  const statusFilter = document.getElementById('statusFilter');
  const priorityFilter = document.getElementById('priorityFilter');
  
  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }
  if (statusFilter) {
    statusFilter.addEventListener('change', applyFilters);
  }
  if (priorityFilter) {
    priorityFilter.addEventListener('change', applyFilters);
  }
  
  // Modal de nuevo proyecto
  const newProjectBtn = document.getElementById('newProjectBtn');
  const projectModal = document.getElementById('newProjectModal');
  const closeProjectModalBtn = document.getElementById('closeProjectModalBtn');
  const cancelProjectBtn = document.getElementById('cancelProjectBtn');
  const createProjectBtn = document.getElementById('createProjectBtn');
  
  if (newProjectBtn) {
    newProjectBtn.addEventListener('click', openNewProjectModal);
  }
  
  const closeProjectModal = () => {
    projectModal?.classList.remove('active');
  };
  
  closeProjectModalBtn?.addEventListener('click', closeProjectModal);
  cancelProjectBtn?.addEventListener('click', closeProjectModal);
  
  // Cerrar al hacer click fuera del modal
  projectModal?.addEventListener('click', (e) => {
    if (e.target === projectModal) {
      closeProjectModal();
    }
  });
  
  // Crear proyecto
  createProjectBtn?.addEventListener('click', createProject);
}

// Función para aplicar filtros a las tareas
function applyFilters() {
  const searchInput = document.getElementById('taskSearchInput') as HTMLInputElement;
  const statusFilter = document.getElementById('statusFilter') as HTMLSelectElement;
  const priorityFilter = document.getElementById('priorityFilter') as HTMLSelectElement;
  
  if (!searchInput || !statusFilter || !priorityFilter) return;
  
  const searchTerm = searchInput.value.toLowerCase();
  const statusValue = statusFilter.value;
  const priorityValue = priorityFilter.value;
  
  const filteredTasks = allTasks.filter(task => {
    const matchesSearch = !searchTerm || 
      task.title.toLowerCase().includes(searchTerm) ||
      (task.description && task.description.toLowerCase().includes(searchTerm));
    
    const matchesStatus = !statusValue || task.status === statusValue;
    const matchesPriority = !priorityValue || task.priority === priorityValue;
    
    return matchesSearch && matchesStatus && matchesPriority;
  });
  
  renderTasks(filteredTasks);
}
