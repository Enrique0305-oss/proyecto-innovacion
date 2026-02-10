export function LoginPage(): string {
  return `
    <div class="login-container">
      <div class="login-split">
        <!-- Panel izquierdo - Formulario -->
        <div class="login-form-panel">
          <div class="login-card">
            <div class="login-header">
              <div class="login-logo">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <rect width="48" height="48" rx="8" fill="#005a9c"/>
                  <circle cx="24" cy="24" r="12" stroke="white" stroke-width="2"/>
                  <circle cx="20" cy="21" r="2" fill="white"/>
                  <circle cx="28" cy="21" r="2" fill="white"/>
                  <path d="M18 28c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <h1 class="login-title">Processmart S.A.C.</h1>
              <p class="login-subtitle">Sistema de Análisis y Mejora de Productividad</p>
            </div>
            
            <form class="login-form" id="loginForm">
              <div class="form-group">
                <label for="email">Email</label>
                <div class="input-wrapper">
                  <svg class="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M3 4h14a1 1 0 011 1v10a1 1 0 01-1 1H3a1 1 0 01-1-1V5a1 1 0 011-1z" stroke="#6c757d" stroke-width="1.5"/>
                    <path d="M2 5l8 6 8-6" stroke="#6c757d" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  <input 
                    type="email" 
                    id="email" 
                    name="email" 
                    placeholder="usuario@processmart.com"
                    required
                    style="padding-left: 48px !important;"
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label for="password">Contraseña</label>
                <div class="input-wrapper">
                  <svg class="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <rect x="4" y="9" width="12" height="8" rx="1" stroke="#6c757d" stroke-width="1.5"/>
                    <path d="M7 9V6a3 3 0 016 0v3" stroke="#6c757d" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  <input 
                    type="password" 
                    id="password" 
                    name="password" 
                    placeholder="••••••••"
                    required
                    style="padding-left: 48px !important;"
                  />
                </div>
              </div>
              
              <button type="submit" class="btn-login">Ingresar</button>
              
              <a href="#" class="forgot-password">¿Olvidaste tu contraseña?</a>
            </form>
          </div>
        </div>
        
        <!-- Panel derecho - Información -->
        <div class="login-info-panel">
          <div class="login-info-content">
            <h2 class="info-title">Transformación Digital</h2>
            <p class="info-description">
              Optimiza tu productividad con inteligencia artificial. Analiza, predice y 
              mejora los procesos de tu organización en tiempo real.
            </p>
            
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">+40%</div>
                <div class="stat-label">Productividad</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">-30%</div>
                <div class="stat-label">Tiempo de Espera</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">95%</div>
                <div class="stat-label">Precisión IA</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

export function initLogin() {
  const form = document.getElementById('loginForm') as HTMLFormElement;
  
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const email = (document.getElementById('email') as HTMLInputElement).value;
      const password = (document.getElementById('password') as HTMLInputElement).value;
      const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
      
      // Deshabilitar botón
      submitBtn.disabled = true;
      submitBtn.textContent = 'Ingresando...';
      
      try {
        // Importar API dinámicamente
        const { api } = await import('../utils/api');
        
        // Intentar login
        await api.login(email, password);
        
        // Redirigir al dashboard
        window.location.hash = '#dashboard';
      } catch (error) {
        // Mostrar error
        alert(error instanceof Error ? error.message : 'Error al iniciar sesión');
        
        // Rehabilitar botón
        submitBtn.disabled = false;
        submitBtn.textContent = 'Ingresar';
      }
    });
  }
}
