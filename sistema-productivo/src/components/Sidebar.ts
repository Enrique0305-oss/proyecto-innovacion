export function Sidebar(activePage: string = 'dashboard'): string {
  const isActive = (page: string) => page === activePage ? 'active' : '';
  
  return `
    <aside class="sidebar" id="sidebar">
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
          <a href="#dashboard" class="nav-item ${isActive('dashboard')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="11" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="3" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="11" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            Dashboard
          </a>
          <a href="#tareas" class="nav-item ${isActive('tareas')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M6 10l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            Gestión de Tareas
          </a>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">Módulos IA</div>
          <a href="#riesgo" class="nav-item ${isActive('riesgo')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 6v4M10 13v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Clasificación de Riesgo
          </a>
          <a href="#duracion" class="nav-item ${isActive('duracion')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Predicción de Duración
          </a>
          <a href="#recomendacion" class="nav-item ${isActive('recomendacion')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7 10h6M10 7v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            Recomendación Persona-Tarea
          </a>
          <a href="#desempeno" class="nav-item ${isActive('desempeno')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M16 14l-6-6-3 3-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Desempeño del Colaborador
          </a>
          <a href="#flujo" class="nav-item ${isActive('flujo')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="5" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/>
              <circle cx="15" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M7 10h6" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            Simulación de Flujo
          </a>
          <a href="#visualizacion" class="nav-item ${isActive('visualizacion')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="11" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="3" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="11" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            Visualización Inteligente
          </a>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">Administración</div>
          <a href="#usuarios" class="nav-item ${isActive('usuarios')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5"/>
              <path d="M5 17c0-2.8 2.2-5 5-5s5 2.2 5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Usuarios
          </a>
          <a href="#areas" class="nav-item ${isActive('areas')}">
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 6h12M4 10h12M4 14h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Áreas
          </a>
          <a href="#configuracion-ia" class="nav-item ${isActive('configuracion-ia')}">
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
    </aside>
  `;
}

export function initSidebar() {
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      // Importar API y hacer logout
      const { api } = await import('../utils/api');
      api.logout();
      
      // Redirigir a login
      window.location.hash = '#login';
    });
  }

  // Mobile menu toggle
  const mobileToggle = document.querySelector('.btn-mobile-menu');
  const sidebar = document.getElementById('sidebar');
  
  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      sidebar?.classList.toggle('mobile-active');
    });
  }
}
