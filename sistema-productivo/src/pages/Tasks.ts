import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function TasksPage(): string {
  return `
    <div class="dashboard-layout">
      ${getSidebar()}
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
              <p>Total: 5 tareas</p>
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
              <tbody>
                <tr>
                  <td class="task-id">T-001</td>
                  <td class="task-name">Implementación CRM</td>
                  <td><span class="area-badge area-ti">TI</span></td>
                  <td class="task-responsibles">
                    <div>Juan Pérez</div>
                    <div>Ana García</div>
                  </td>
                  <td>10d</td>
                  <td>7.5d</td>
                  <td><span class="status-badge status-progress">En Progreso</span></td>
                  <td><span class="risk-badge risk-low">Bajo</span></td>
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
                <tr>
                  <td class="task-id">T-002</td>
                  <td class="task-name">Campaña Marketing Q4</td>
                  <td><span class="area-badge area-marketing">Marketing</span></td>
                  <td class="task-responsibles">
                    <div>María López</div>
                  </td>
                  <td>15d</td>
                  <td>18d</td>
                  <td><span class="status-badge status-completed">Completada</span></td>
                  <td><span class="risk-badge risk-medium">Medio</span></td>
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
                <tr>
                  <td class="task-id">T-003</td>
                  <td class="task-name">Auditoría de Procesos</td>
                  <td><span class="area-badge area-operations">Operaciones</span></td>
                  <td class="task-responsibles">
                    <div>Carlos Ruiz</div>
                    <div>Laura Díaz</div>
                  </td>
                  <td>8d</td>
                  <td>12d</td>
                  <td><span class="status-badge status-blocked">Bloqueada</span></td>
                  <td><span class="risk-badge risk-high">Alto</span></td>
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
                <tr>
                  <td class="task-id">T-004</td>
                  <td class="task-name">Capacitación Personal</td>
                  <td><span class="area-badge area-rrhh">RRHH</span></td>
                  <td class="task-responsibles">
                    <div>Pedro Sánchez</div>
                  </td>
                  <td>5d</td>
                  <td>-</td>
                  <td><span class="status-badge status-pending">Por Hacer</span></td>
                  <td><span class="risk-badge risk-low">Bajo</span></td>
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
                <tr>
                  <td class="task-id">T-005</td>
                  <td class="task-name">Optimización Base Datos</td>
                  <td><span class="area-badge area-ti">TI</span></td>
                  <td class="task-responsibles">
                    <div>Juan Pérez</div>
                  </td>
                  <td>12d</td>
                  <td>14d</td>
                  <td><span class="status-badge status-progress">En Progreso</span></td>
                  <td><span class="risk-badge risk-critical">Crítico</span></td>
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
                  <input type="text" placeholder="Ej: Implementación sistema" required />
                </div>
                <div class="form-group">
                  <label>Área</label>
                  <select required>
                    <option value="">Seleccionar área</option>
                    <option>TI</option>
                    <option>Marketing</option>
                    <option>Operaciones</option>
                    <option>RRHH</option>
                    <option>Ventas</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Descripción</label>
                <textarea rows="3" placeholder="Descripción detallada de la tarea"></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Tiempo Estimado (días)</label>
                  <input type="number" placeholder="10" min="1" />
                </div>
                <div class="form-group">
                  <label>Responsable</label>
                  <select>
                    <option value="">Asignar responsable</option>
                    <option>Juan Pérez</option>
                    <option>Ana García</option>
                    <option>María López</option>
                    <option>Carlos Ruiz</option>
                    <option>Laura Díaz</option>
                    <option>Pedro Sánchez</option>
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

function getSidebar(): string {
  // Reutilizar el sidebar del dashboard (importado)
  return `<aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <div class="sidebar-logo">
        <svg width="32" height="32" viewBox="0 0 48 48" fill="none">
          <rect width="48" height="48" rx="8" fill="white"/>
          <circle cx="24" cy="24" r="12" stroke="#005a9c" stroke-width="2"/>
          <circle cx="20" cy="21" r="2" fill="#005a9c"/>
          <circle cx="28" cy="21" r="2" fill="#005a9c"/>
          <path d="M18 28c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="#005a9c" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="sidebar-brand">
        <h2>Processmart</h2>
        <p>Sistema IA</p>
      </div>
    </div>
    <nav class="sidebar-nav">
      <div class="nav-section">
        <div class="nav-section-title">Principal</div>
        <a href="#dashboard" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <rect x="3" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="11" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="3" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="11" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
          </svg>
          Dashboard
        </a>
        <a href="#tareas" class="nav-item active">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M6 10l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
          </svg>
          Gestión de Tareas
        </a>
      </div>
      <div class="nav-section">
        <div class="nav-section-title">Módulos IA</div>
        <a href="#riesgo" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
            <path d="M10 6v4M10 13v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Clasificación de Riesgo
        </a>
        <a href="#duracion" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
            <path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Predicción de Duración
        </a>
        <a href="#recomendacion" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M7 10h6M10 7v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
          </svg>
          Recomendación Persona-Tarea
        </a>
        <a href="#desempeno" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M16 14l-6-6-3 3-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Desempeño del Colaborador
        </a>
        <a href="#flujo" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="5" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/>
            <circle cx="15" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/>
            <path d="M7 10h6" stroke="currentColor" stroke-width="1.5"/>
          </svg>
          Simulación de Flujo
        </a>
      </div>
      <div class="nav-section">
        <div class="nav-section-title">Administración</div>
        <a href="#usuarios" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5"/>
            <path d="M5 17c0-2.8 2.2-5 5-5s5 2.2 5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Usuarios
        </a>
        <a href="#areas" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M4 6h12M4 10h12M4 14h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Áreas
        </a>
        <a href="#configuracion" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="3" stroke="currentColor" stroke-width="1.5"/>
            <path d="M10 3v2M10 15v2M17 10h-2M5 10H3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Configuración IA
        </a>
      </div>
    </nav>
    <div class="sidebar-footer">
      <button class="nav-item logout-btn" id="logoutBtn">
        <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M7 17H4a1 1 0 01-1-1V4a1 1 0 011-1h3M13 13l4-4-4-4M17 9H7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Cerrar Sesión
      </button>
    </div>
  </aside>`;
}

export function initTasks() {
  // Inicializar AI Assistant
  initAIAssistant();

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
  createTaskBtn?.addEventListener('click', () => {
    // Aquí iría la lógica para crear la tarea
    alert('Funcionalidad de crear tarea - Conectar con backend');
    closeModal();
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
