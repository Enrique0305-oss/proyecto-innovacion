import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

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
              <p class="module-description">Administración de áreas y departamentos</p>
            </div>
            <button class="btn-primary" id="btnNewArea">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="10" y1="4" x2="10" y2="16"/>
                <line x1="4" y1="10" x2="16" y2="10"/>
              </svg>
              Nueva Área
            </button>
          </div>

          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-label">Total Áreas</div>
              <div class="stat-value">5</div>
              <div class="stat-description">Departamentos activos</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Total Empleados</div>
              <div class="stat-value">51</div>
              <div class="stat-description">En todas las áreas</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Tareas Activas</div>
              <div class="stat-value">107</div>
              <div class="stat-description">En progreso</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Eficiencia Promedio</div>
              <div class="stat-value">83%</div>
              <div class="stat-description">Global</div>
            </div>
          </div>

          <!-- Areas Grid -->
          <div class="areas-grid">
            ${generateAreaCard('TI', 'Tecnologías de la Información', 'Juan Pérez', 'JP', 12, 25, 88, 'Mejorando', 'success')}
            ${generateAreaCard('Marketing', 'Marketing y Comunicaciones', 'María López', 'ML', 8, 18, 90, 'Mejorando', 'success')}
            ${generateAreaCard('Operaciones', 'Operaciones y Procesos', 'Carlos Ruiz', 'CR', 15, 32, 72, 'Estable', 'warning')}
            ${generateAreaCard('Ventas', 'Ventas y Comercial', 'Ana García', 'AG', 10, 20, 85, 'Mejorando', 'success')}
            ${generateAreaCard('RRHH', 'Recursos Humanos', 'Pedro Sánchez', 'PS', 6, 12, 82, 'Estable', 'warning')}
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
                <option value="1">Juan Pérez</option>
                <option value="2">María López</option>
                <option value="3">Carlos Ruiz</option>
                <option value="4">Ana García</option>
                <option value="5">Pedro Sánchez</option>
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
  `;
}

function generateAreaCard(
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
    <div class="area-card">
      <div class="area-card-header">
        <div class="area-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" rx="1"/>
            <rect x="14" y="3" width="7" height="7" rx="1"/>
            <rect x="3" y="14" width="7" height="7" rx="1"/>
            <rect x="14" y="14" width="7" height="7" rx="1"/>
          </svg>
        </div>
        <button class="btn-edit">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </button>
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

      <button class="btn-details">Ver Detalles</button>
    </div>
  `;
}

export function initAreas(): void {
  // Initialize AI Assistant
  initAIAssistant();

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
  };

  btnNewArea?.addEventListener('click', openModal);
  btnCloseModal?.addEventListener('click', closeModal);
  btnCancelModal?.addEventListener('click', closeModal);
  modalOverlay?.addEventListener('click', closeModal);

  // Form submission
  const form = document.getElementById('formNewArea') as HTMLFormElement;
  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const areaName = (document.getElementById('areaName') as HTMLInputElement).value;
    const areaDescription = (document.getElementById('areaDescription') as HTMLTextAreaElement).value;
    const areaSupervisor = (document.getElementById('areaSupervisor') as HTMLSelectElement).value;
    const areaEfficiency = (document.getElementById('areaEfficiency') as HTMLInputElement).value;

    console.log('Nueva área:', {
      name: areaName,
      description: areaDescription,
      supervisor: areaSupervisor,
      efficiency: areaEfficiency
    });

    alert(`Área "${areaName}" creada exitosamente`);
    closeModal();
    form.reset();
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
