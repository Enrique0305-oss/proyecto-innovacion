import { canAccessModule } from '../utils/permissions';

export function Sidebar(activePage: string = 'dashboard'): string {
  const isActive = (page: string) => page === activePage ? 'active' : '';
  
  // Función helper para mostrar/ocultar nav-item
  const navItem = (moduleName: string, href: string, label: string, icon: string, isActiveCheck: string = '') => {
    if (!canAccessModule(moduleName)) return '';
    
    return `
      <a href="${href}" class="nav-item ${isActiveCheck}">
        ${icon}
        ${label}
      </a>
    `;
  };
  
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
          ${navItem('dashboard', '#dashboard', 'Dashboard', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="11" y="3" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="3" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              <rect x="11" y="11" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          `, isActive('dashboard'))}
          ${navItem('tareas', '#tareas', 'Gestión de Tareas', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M6 10l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          `, isActive('tareas'))}
        </div>

        <div class="nav-section">
          <div class="nav-section-title">Módulos IA</div>
          ${navItem('riesgo', '#riesgo', 'Clasificación de Riesgo', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 6v4M10 13v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          `, isActive('riesgo'))}
          ${navItem('duracion', '#duracion', 'Predicción de Duración', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          `, isActive('duracion'))}
          ${navItem('recomendacion', '#recomendacion', 'Recomendación Persona-Tarea', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7 10h6M10 7v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          `, isActive('recomendacion'))}
          ${navItem('asignacion', '#asignacion', 'Asignación Inteligente', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
            </svg>
          `, isActive('asignacion'))}
          ${navItem('desempeno', '#desempeno', 'Desempeño del Colaborador', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M16 14l-6-6-3 3-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          `, isActive('desempeno'))}
          ${navItem('flujo', '#flujo', 'Simulación de Flujo', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="5" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/>
              <circle cx="15" cy="10" r="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M7 10h6" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          `, isActive('flujo'))}
        </div>

        <div class="nav-section">
          <div class="nav-section-title">Administración</div>
          ${navItem('usuarios', '#usuarios', 'Usuarios', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5"/>
              <path d="M5 17c0-2.8 2.2-5 5-5s5 2.2 5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          `, isActive('usuarios'))}
          ${navItem('areas', '#areas', 'Áreas', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 6h12M4 10h12M4 14h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          `, isActive('areas'))}
          ${navItem('configuracion', '#configuracion-ia', 'Configuración IA', `
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="3" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 3v2M10 15v2M17 10h-2M5 10H3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          `, isActive('configuracion-ia'))}
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
