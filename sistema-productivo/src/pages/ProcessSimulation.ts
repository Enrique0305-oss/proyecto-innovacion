import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function ProcessSimulationPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('flujo')}
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
            <div class="module-icon" style="background: rgba(0, 114, 198, 0.2);">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <circle cx="8" cy="16" r="3" stroke="white" stroke-width="2"/>
                <circle cx="24" cy="16" r="3" stroke="white" stroke-width="2"/>
                <path d="M11 16h10" stroke="white" stroke-width="2"/>
                <path d="M16 11v10" stroke="white" stroke-width="2"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Simulación de Flujo de Procesos</h2>
              <p class="module-description">Modelo 5: Process Mining y predicción secuencial con análisis What-If</p>
            </div>
          </div>

          <!-- Panel de Control -->
          <div class="control-panel">
            <h3>Panel de Control</h3>
            <p class="section-subtitle">Configure y ejecute simulaciones de proceso</p>
            
            <div class="control-buttons">
              <button class="btn-execute" id="executeBtn">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 3l12 7-12 7V3z" fill="currentColor"/>
                </svg>
                Ejecutar Simulación
              </button>
              <button class="btn-reset" id="resetBtn">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M4 10a6 6 0 0112 0M10 4v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <path d="M7 7l3 3 3-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Reiniciar
              </button>
            </div>
          </div>

          <!-- Tabs -->
          <div class="simulation-tabs">
            <button class="tab-btn active" data-tab="actual">Flujo Actual</button>
            <button class="tab-btn" data-tab="whatif">Simulación What-If</button>
          </div>

          <!-- Tab Content -->
          <div class="tab-content active" id="actualTab">
            <!-- Mapa de Proceso -->
            <div class="process-section">
              <h3>Mapa de Proceso (BPMN Simplificado)</h3>
              <p class="section-subtitle">Flujo actual de trabajo con indicadores de congestión</p>

              <div class="process-flow">
                ${generateProcessStep('Inicio', '0.5d', '15%', 'low')}
                ${generateProcessStep('Análisis Inicial', '2d', '45%', 'medium')}
                ${generateProcessStep('Aprobación', '3d', '75%', 'high')}
                ${generateProcessStep('Desarrollo', '8d', '35%', 'medium')}
                ${generateProcessStep('Revisión QA', '2.5d', '60%', 'high')}
                ${generateProcessStep('Implementación', '1.5d', '25%', 'low')}
                ${generateProcessStep('Cierre', '0.5d', '10%', 'low')}
              </div>
            </div>

            <!-- Mapa de Calor -->
            <div class="heatmap-section">
              <h3>Mapa de Calor de Demoras</h3>
              <p class="section-subtitle">Identificación de cuellos de botella por paso</p>

              <div class="heatmap-list">
                ${generateHeatmapRow('Inicio', '0.5d', '15%', 'low')}
                ${generateHeatmapRow('Análisis Inicial', '2d', '45%', 'medium')}
                ${generateHeatmapRow('Aprobación', '3d', '75%', 'high')}
                ${generateHeatmapRow('Desarrollo', '8d', '35%', 'medium')}
                ${generateHeatmapRow('Revisión QA', '2.5d', '60%', 'high')}
                ${generateHeatmapRow('Implementación', '1.5d', '25%', 'low')}
                ${generateHeatmapRow('Cierre', '0.5d', '10%', 'low')}
              </div>
            </div>
          </div>

          <div class="tab-content" id="whatifTab">
            <div class="whatif-container">
              <!-- Configuración What-If -->
              <div class="whatif-config">
                <h3>Configurar Escenario What-If</h3>
                <p class="section-subtitle">Modifique parámetros para simular optimizaciones</p>

                <form id="whatifForm">
                  <div class="form-group">
                    <label>Paso a Optimizar</label>
                    <select id="stepToOptimize">
                      <option value="">Seleccionar paso</option>
                      <option value="aprobacion">Aprobación</option>
                      <option value="desarrollo">Desarrollo</option>
                      <option value="revision">Revisión QA</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label>Cambiar Responsable</label>
                    <select id="changeResponsible">
                      <option value="actual">Responsable Actual</option>
                      <option value="optimizado">Responsable Optimizado</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label>Ajustar Recursos (%)</label>
                    <div class="slider-container">
                      <input type="range" id="resourceSlider" min="50" max="200" value="100" step="10" />
                      <span class="slider-value" id="sliderValue">100%</span>
                    </div>
                    <p class="slider-label">Mantener recursos</p>
                  </div>

                  <button type="submit" class="btn-simulate">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <path d="M5 3l12 7-12 7V3z" fill="currentColor"/>
                    </svg>
                    Simular Escenario
                  </button>
                </form>
              </div>

              <!-- Resultados (oculto inicialmente) -->
              <div class="whatif-results" id="whatifResults" style="display: none;">
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

function generateProcessStep(name: string, time: string, congestion: string, level: string): string {
  const colors: { [key: string]: string } = {
    low: '#28a745',
    medium: '#ff9800',
    high: '#dc3545'
  };

  return `
    <div class="process-step">
      <div class="step-box">
        <div class="step-name">${name}</div>
        <div class="step-time">${time}</div>
      </div>
      <div class="step-arrow">→</div>
      <div class="step-congestion">
        <span>Congestión</span>
        <div class="congestion-bar">
          <div class="congestion-fill" style="width: ${congestion}; background: ${colors[level]}"></div>
        </div>
        <span class="congestion-value">${congestion}</span>
      </div>
    </div>
  `;
}

function generateHeatmapRow(name: string, time: string, congestion: string, level: string): string {
  const colors: { [key: string]: string } = {
    low: '#28a745',
    medium: '#ff9800',
    high: '#dc3545'
  };

  const badges: { [key: string]: string } = {
    low: 'Bajo',
    medium: 'Medio',
    high: 'Alto'
  };

  return `
    <div class="heatmap-row">
      <div class="heatmap-label">${name}</div>
      <div class="heatmap-bar">
        <div class="heatmap-fill" style="width: ${congestion}; background: ${colors[level]}"></div>
      </div>
      <div class="heatmap-value">${congestion} congestión</div>
      <div class="heatmap-time">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="7" r="5.5" stroke="#6c757d" stroke-width="1"/>
          <path d="M7 4v3l2 2" stroke="#6c757d" stroke-width="1" stroke-linecap="round"/>
        </svg>
        ${time}
      </div>
      <span class="heatmap-badge ${level}">${badges[level]}</span>
    </div>
  `;
}

export function initProcessSimulation() {
  initAIAssistant();

  // Tab switching
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabName = btn.getAttribute('data-tab');
      
      tabButtons.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      
      btn.classList.add('active');
      document.getElementById(`${tabName}Tab`)?.classList.add('active');
    });
  });

  // Slider
  const slider = document.getElementById('resourceSlider') as HTMLInputElement;
  const sliderValue = document.getElementById('sliderValue');
  const sliderLabel = document.querySelector('.slider-label');

  if (slider && sliderValue && sliderLabel) {
    slider.addEventListener('input', (e) => {
      const value = (e.target as HTMLInputElement).value;
      sliderValue.textContent = `${value}%`;
      
      if (parseInt(value) < 100) {
        sliderLabel.textContent = 'Reducir recursos';
      } else if (parseInt(value) > 100) {
        sliderLabel.textContent = 'Aumentar recursos';
      } else {
        sliderLabel.textContent = 'Mantener recursos';
      }
    });
  }

  // What-If Form
  const whatifForm = document.getElementById('whatifForm') as HTMLFormElement;
  const whatifResults = document.getElementById('whatifResults');

  if (whatifForm && whatifResults) {
    whatifForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      whatifResults.style.display = 'block';
      whatifResults.innerHTML = `
        <div class="results-header">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M5 12l5 5L22 5" stroke="#28a745" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <h3>Resultados del Escenario</h3>
        </div>
        <p class="results-subtitle">Comparación: Flujo actual vs optimizado</p>

        <div class="comparison-grid">
          <div class="comparison-item">
            <span class="comparison-label">Tiempo Actual</span>
            <span class="comparison-value">18d</span>
          </div>
          <div class="comparison-item highlight">
            <span class="comparison-label">Tiempo Optimizado</span>
            <span class="comparison-value success">14.5d</span>
          </div>
          <div class="comparison-item">
            <span class="comparison-label">Eficiencia Actual</span>
            <span class="comparison-value">68%</span>
          </div>
          <div class="comparison-item highlight">
            <span class="comparison-label">Eficiencia Optimizada</span>
            <span class="comparison-value success">82%</span>
          </div>
        </div>

        <div class="improvement-banner">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 3v10M7 10l3 3 3-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Mejora: +19%</span>
          <p>La optimización propuesta reduciría el tiempo total en 3.5 días</p>
        </div>

        <div class="recommendations-section">
          <h4>Recomendaciones</h4>
          <ul class="recommendations-list">
            <li>• La optimización propuesta reduciría el tiempo total en 3.5 días</li>
            <li>• La eficiencia aumentaría de 68% a 82%</li>
            <li>• Solo quedaría un cuello de botella menor</li>
          </ul>
        </div>
      `;

      whatifResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
