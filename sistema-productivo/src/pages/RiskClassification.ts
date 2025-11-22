import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function RiskClassificationPage(): string {
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
          <!-- Header de módulo -->
          <div class="module-header">
            <div class="module-icon">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <circle cx="20" cy="20" r="16" stroke="white" stroke-width="2"/>
                <path d="M20 12v8M20 26v2" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Clasificación Multiclase de Riesgo</h2>
              <p class="module-description">Modelo 1: Predicción del nivel de riesgo de retraso en tareas</p>
            </div>
          </div>

          <div class="risk-container">
            <!-- Formulario -->
            <div class="risk-form-card">
              <h3>Datos de la Tarea</h3>
              <p class="form-subtitle">Complete la información para calcular el riesgo</p>

              <form id="riskForm">
                <div class="form-group">
                  <label>Nombre de la Tarea</label>
                  <input type="text" id="taskName" placeholder="Ej: Implementación CRM" />
                </div>

                <div class="form-group">
                  <label>Área</label>
                  <select id="taskArea">
                    <option value="">Seleccionar área</option>
                    <option value="TI">TI</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Operaciones">Operaciones</option>
                    <option value="RRHH">RRHH</option>
                    <option value="Ventas">Ventas</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Complejidad</label>
                  <select id="taskComplexity">
                    <option value="">Seleccionar complejidad</option>
                    <option value="Baja">Baja</option>
                    <option value="Media">Media</option>
                    <option value="Alta">Alta</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Tiempo Estimado (días)</label>
                  <input type="number" id="estimatedTime" placeholder="Ej: 10" min="1" />
                </div>

                <div class="form-group">
                  <label>Recursos Disponibles</label>
                  <select id="availableResources">
                    <option value="">Nivel de recursos</option>
                    <option value="Abundantes">Abundantes</option>
                    <option value="Suficientes">Suficientes</option>
                    <option value="Limitados">Limitados</option>
                    <option value="Escasos">Escasos</option>
                  </select>
                </div>

                <button type="submit" class="btn-calculate">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M10 6v4M10 13v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  Calcular Riesgo
                </button>
              </form>
            </div>

            <!-- Resultado (oculto inicialmente) -->
            <div class="risk-result-card" id="riskResult">
              <div class="result-empty">
                <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                  <circle cx="40" cy="40" r="35" stroke="#cbd5e0" stroke-width="3"/>
                  <path d="M40 20v20M40 50v4" stroke="#cbd5e0" stroke-width="3" stroke-linecap="round"/>
                </svg>
                <h3>Complete los datos de la tarea</h3>
                <p>El modelo calculará el nivel de riesgo automáticamente</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

function getSidebar(): string {
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
        <a href="#tareas" class="nav-item">
          <svg class="nav-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M6 10l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
          </svg>
          Gestión de Tareas
        </a>
      </div>
      <div class="nav-section">
        <div class="nav-section-title">Módulos IA</div>
        <a href="#riesgo" class="nav-item active">
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

export function initRiskClassification() {
  initAIAssistant();

  const form = document.getElementById('riskForm') as HTMLFormElement;
  const resultCard = document.getElementById('riskResult');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Simular cálculo de riesgo
      if (resultCard) {
        resultCard.style.display = 'block';
        resultCard.innerHTML = `
          <div class="result-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="9" stroke="#ff5722" stroke-width="2"/>
              <path d="M12 8v4M12 16v1" stroke="#ff5722" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <h3>Predicción de Riesgo</h3>
            <p>Nivel de riesgo calculado por el modelo de IA</p>
          </div>

          <div class="risk-prediction">
            <div class="risk-level risk-high">
              RIESGO ALTO
            </div>
            <div class="risk-probability">Probabilidad: 55%</div>
          </div>

          <div class="risk-distribution">
            <div class="risk-bar-item">
              <span class="risk-bar-label">10%</span>
              <div class="risk-bar">
                <div class="risk-bar-fill risk-low" style="width: 10%"></div>
              </div>
              <span class="risk-badge-small risk-low">Bajo</span>
            </div>
            <div class="risk-bar-item">
              <span class="risk-bar-label">25%</span>
              <div class="risk-bar">
                <div class="risk-bar-fill risk-medium" style="width: 25%"></div>
              </div>
              <span class="risk-badge-small risk-medium">Medio</span>
            </div>
            <div class="risk-bar-item">
              <span class="risk-bar-label">55%</span>
              <div class="risk-bar">
                <div class="risk-bar-fill risk-high" style="width: 55%"></div>
              </div>
              <span class="risk-badge-small risk-high">Alto</span>
            </div>
            <div class="risk-bar-item">
              <span class="risk-bar-label">10%</span>
              <div class="risk-bar">
                <div class="risk-bar-fill risk-critical" style="width: 10%"></div>
              </div>
              <span class="risk-badge-small risk-critical">Crítico</span>
            </div>
          </div>

          <div class="shap-section">
            <h4>Importancia de Variables (SHAP)</h4>
            <p class="shap-subtitle">Factores que más influyen en la predicción</p>
            
            <div class="shap-item">
              <div class="shap-label">
                <span>Complejidad</span>
                <span class="shap-value">85%</span>
              </div>
              <div class="shap-bar">
                <div class="shap-fill" style="width: 85%"></div>
              </div>
              <p class="shap-description">Tarea altamente compleja</p>
            </div>

            <div class="shap-item">
              <div class="shap-label">
                <span>Recursos disponibles</span>
                <span class="shap-value">60%</span>
              </div>
              <div class="shap-bar">
                <div class="shap-fill" style="width: 60%"></div>
              </div>
              <p class="shap-description">Recursos limitados</p>
            </div>

            <div class="shap-item">
              <div class="shap-label">
                <span>Histórico del área</span>
                <span class="shap-value">45%</span>
              </div>
              <div class="shap-bar">
                <div class="shap-fill" style="width: 45%"></div>
              </div>
              <p class="shap-description">Área con historial de retrasos</p>
            </div>

            <div class="shap-item">
              <div class="shap-label">
                <span>Tiempo estimado</span>
                <span class="shap-value">70%</span>
              </div>
              <div class="shap-bar">
                <div class="shap-fill" style="width: 70%"></div>
              </div>
              <p class="shap-description">Plazo ajustado</p>
            </div>

            <div class="shap-item">
              <div class="shap-label">
                <span>Dependencias</span>
                <span class="shap-value">40%</span>
              </div>
              <div class="shap-bar">
                <div class="shap-fill" style="width: 40%"></div>
              </div>
              <p class="shap-description">Múltiples dependencias</p>
            </div>
          </div>

          <div class="comparison-section">
            <h4>Comparación con Tareas Similares</h4>
            <p class="comparison-subtitle">Benchmark de riesgo</p>
            
            <svg class="comparison-chart" width="100%" height="200" viewBox="0 0 600 200">
              <rect x="100" y="40" width="120" height="140" fill="#00bcd4" rx="4"/>
              <text x="160" y="195" text-anchor="middle" font-size="14" fill="#6c757d">Tarea Actual</text>
              <text x="160" y="30" text-anchor="middle" font-size="16" font-weight="600" fill="#005a9c">55</text>
              
              <rect x="260" y="80" width="120" height="100" fill="#0072c6" rx="4"/>
              <text x="320" y="195" text-anchor="middle" font-size="14" fill="#6c757d">Promedio Área</text>
              <text x="320" y="70" text-anchor="middle" font-size="16" font-weight="600" fill="#005a9c">38</text>
              
              <rect x="420" y="60" width="120" height="120" fill="#005a9c" rx="4"/>
              <text x="480" y="195" text-anchor="middle" font-size="14" fill="#6c757d">Tareas Similares</text>
              <text x="480" y="50" text-anchor="middle" font-size="16" font-weight="600" fill="#005a9c">42</text>
            </svg>
          </div>

          <div class="interpretation-section">
            <h4>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="#00bcd4"/>
              </svg>
              Interpretación Automática
            </h4>
            
            <div class="interpretation-item success">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="8" fill="#28a745"/>
                <path d="M6 10l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <p>La tarea presenta un nivel de riesgo alto debido principalmente a su complejidad y recursos limitados.</p>
            </div>

            <div class="interpretation-item warning">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 2l8 14H2l8-14z" fill="#ffc107"/>
                <path d="M10 8v3M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <p>Se recomienda asignar recursos adicionales y establecer puntos de control frecuentes.</p>
            </div>

            <div class="interpretation-item danger">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="8" fill="#dc3545"/>
                <path d="M7 7l6 6M7 13l6-6" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <p>El historial del área muestra tendencia a retrasos. Considerar reasignación o soporte cruzado.</p>
            </div>
          </div>
        `;

        // Scroll al resultado
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
