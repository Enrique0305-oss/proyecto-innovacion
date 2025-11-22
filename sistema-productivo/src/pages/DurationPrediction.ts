import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function DurationPredictionPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('duracion')}
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
            <div class="module-icon" style="background: rgba(0, 188, 212, 0.2);">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="12" stroke="white" stroke-width="2"/>
                <path d="M16 10v6l4 3" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Predicción de Duración Real</h2>
              <p class="module-description">Modelo 2: Estimación de duración real basada en CatBoost Regressor</p>
            </div>
          </div>

          <div class="risk-container">
            <!-- Formulario -->
            <div class="risk-form-card">
              <h3>Características de la Tarea</h3>
              <p class="form-subtitle">Ingrese los datos para estimar la duración</p>

              <form id="durationForm">
                <div class="form-group">
                  <label>Nombre de la Tarea</label>
                  <input type="text" id="taskName" placeholder="Ej: Desarrollo módulo pagos" />
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
                    <option value="">Nivel de complejidad</option>
                    <option value="Baja">Baja</option>
                    <option value="Media">Media</option>
                    <option value="Alta">Alta</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Tiempo Estimado Inicial (días)</label>
                  <input type="number" id="estimatedTime" placeholder="10" min="1" />
                </div>

                <div class="form-group">
                  <label>Tamaño del Equipo</label>
                  <select id="teamSize">
                    <option value="">Número de personas</option>
                    <option value="1-2">1-2 personas</option>
                    <option value="3-5">3-5 personas</option>
                    <option value="6-10">6-10 personas</option>
                    <option value="10+">Más de 10 personas</option>
                  </select>
                </div>

                <button type="submit" class="btn-calculate">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  Estimar Duración Real
                </button>
              </form>
            </div>

            <!-- Resultado -->
            <div class="risk-result-card" id="durationResult">
              <div class="result-empty">
                <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                  <circle cx="40" cy="40" r="35" stroke="#cbd5e0" stroke-width="3"/>
                  <path d="M40 20v20l14 10" stroke="#cbd5e0" stroke-width="3" stroke-linecap="round"/>
                </svg>
                <h3>Ingrese las características de la tarea</h3>
                <p>El modelo predecirá la duración real basándose en datos históricos</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

export function initDurationPrediction() {
  initAIAssistant();

  const form = document.getElementById('durationForm') as HTMLFormElement;
  const resultCard = document.getElementById('durationResult');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const estimatedTime = (document.getElementById('estimatedTime') as HTMLInputElement).value;
      
      // Simular predicción de duración
      if (resultCard && estimatedTime) {
        resultCard.innerHTML = `
          <div class="duration-results">
            <!-- Estimación Inicial -->
            <div class="duration-card">
              <h4>Estimación Inicial</h4>
              <div class="duration-value">${estimatedTime} días</div>
              <p class="duration-label">Tiempo planificado</p>
            </div>

            <!-- Predicción IA -->
            <div class="duration-card duration-highlight">
              <div class="duration-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="9" stroke="#00bcd4" stroke-width="2"/>
                  <path d="M12 7v5l4 3" stroke="#00bcd4" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <h4>Predicción IA</h4>
              <div class="duration-value prediction">13.5 días</div>
              <p class="duration-label">Duración estimada real</p>
            </div>

            <!-- Diferencia -->
            <div class="duration-card">
              <h4>Diferencia</h4>
              <div class="duration-value difference">+3.5 días</div>
              <p class="duration-label">(35% más)</p>
            </div>
          </div>

          <!-- Intervalo de Confianza -->
          <div class="confidence-section">
            <h4>Intervalo de Confianza</h4>
            <p class="section-subtitle">Rango esperado de duración (92% confianza)</p>
            
            <div class="confidence-slider">
              <div class="slider-labels">
                <span class="slider-label">Mínimo<br><strong>12d</strong></span>
                <span class="slider-label optimist">Optimista</span>
                <span class="slider-label realist">Realista</span>
                <span class="slider-label pessimist">Pesimista</span>
                <span class="slider-label">Máximo<br><strong>15d</strong></span>
              </div>
              <div class="slider-track">
                <div class="slider-fill"></div>
                <div class="slider-thumb" style="left: 50%;"></div>
              </div>
            </div>

            <div class="confidence-info">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="8" fill="#ff9800"/>
                <path d="M10 6v4M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <p>Basado en el análisis histórico, la tarea probablemente tomará entre <strong>12 y 15 días</strong>. Se recomienda planificar con 13.5 días.</p>
            </div>
          </div>

          <!-- Gráfico de Dispersión -->
          <div class="chart-section">
            <h4>Gráfico de Dispersión</h4>
            <p class="section-subtitle">Comparación entre tiempo estimado vs tiempo real (tareas históricas)</p>
            
            <svg class="scatter-chart" width="100%" height="300" viewBox="0 0 700 300">
              <!-- Grid -->
              <line x1="60" y1="250" x2="660" y2="250" stroke="#e0e0e0" stroke-width="1"/>
              <line x1="60" y1="50" x2="60" y2="250" stroke="#e0e0e0" stroke-width="1"/>
              
              <!-- Grid lines -->
              <line x1="60" y1="200" x2="660" y2="200" stroke="#f5f5f5" stroke-width="1" stroke-dasharray="4"/>
              <line x1="60" y1="150" x2="660" y2="150" stroke="#f5f5f5" stroke-width="1" stroke-dasharray="4"/>
              <line x1="60" y1="100" x2="660" y2="100" stroke="#f5f5f5" stroke-width="1" stroke-dasharray="4"/>
              
              <!-- Y-axis labels -->
              <text x="45" y="255" text-anchor="end" font-size="12" fill="#6c757d">0</text>
              <text x="45" y="205" text-anchor="end" font-size="12" fill="#6c757d">6</text>
              <text x="45" y="155" text-anchor="end" font-size="12" fill="#6c757d">12</text>
              <text x="45" y="105" text-anchor="end" font-size="12" fill="#6c757d">18</text>
              <text x="45" y="55" text-anchor="end" font-size="12" fill="#6c757d">24</text>
              
              <!-- Y-axis title -->
              <text x="20" y="150" text-anchor="middle" font-size="13" fill="#495057" transform="rotate(-90 20 150)">Real (días)</text>
              
              <!-- X-axis labels -->
              <text x="130" y="270" text-anchor="middle" font-size="12" fill="#6c757d">5</text>
              <text x="230" y="270" text-anchor="middle" font-size="12" fill="#6c757d">8</text>
              <text x="330" y="270" text-anchor="middle" font-size="12" fill="#6c757d">10</text>
              <text x="430" y="270" text-anchor="middle" font-size="12" fill="#6c757d">12</text>
              <text x="530" y="270" text-anchor="middle" font-size="12" fill="#6c757d">15</text>
              <text x="595" y="270" text-anchor="middle" font-size="12" fill="#6c757d">7</text>
              <text x="630" y="270" text-anchor="middle" font-size="12" fill="#6c757d">20</text>
              <text x="660" y="270" text-anchor="middle" font-size="12" fill="#6c757d">6</text>
              
              <!-- X-axis title -->
              <text x="360" y="290" text-anchor="middle" font-size="13" fill="#495057">Estimado (días)</text>
              
              <!-- Data points -->
              <circle cx="130" cy="225" r="6" fill="#00bcd4"/>
              <circle cx="230" cy="183" r="6" fill="#00bcd4"/>
              <circle cx="280" cy="217" r="6" fill="#00bcd4"/>
              <circle cx="330" cy="150" r="6" fill="#00bcd4"/>
              <circle cx="430" cy="183" r="6" fill="#00bcd4"/>
              <circle cx="530" cy="133" r="6" fill="#00bcd4"/>
              <circle cx="595" cy="200" r="6" fill="#00bcd4"/>
              <circle cx="630" cy="92" r="6" fill="#00bcd4"/>
              <circle cx="660" cy="217" r="6" fill="#00bcd4"/>
              
              <!-- Current prediction (highlighted) -->
              <circle cx="430" cy="158" r="8" fill="#ff9800" stroke="#fff" stroke-width="2"/>
            </svg>
          </div>

          <!-- Variables Más Influyentes -->
          <div class="variables-section">
            <h4>Variables Más Influyentes</h4>
            <p class="section-subtitle">Factores que más afectan la duración real</p>
            
            <div class="variable-item">
              <div class="variable-label">
                <span>Complejidad técnica</span>
              </div>
              <div class="variable-bar">
                <div class="variable-fill" style="width: 95%"></div>
              </div>
            </div>

            <div class="variable-item">
              <div class="variable-label">
                <span>Histórico del área</span>
              </div>
              <div class="variable-bar">
                <div class="variable-fill" style="width: 78%"></div>
              </div>
            </div>

            <div class="variable-item">
              <div class="variable-label">
                <span>Recursos asignados</span>
              </div>
              <div class="variable-bar">
                <div class="variable-fill" style="width: 65%"></div>
              </div>
            </div>

            <div class="variable-item">
              <div class="variable-label">
                <span>Dependencias</span>
              </div>
              <div class="variable-bar">
                <div class="variable-fill" style="width: 42%"></div>
              </div>
            </div>
          </div>

          <!-- Recomendaciones -->
          <div class="recommendations-section">
            <h4>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="#00bcd4"/>
              </svg>
              Recomendaciones
            </h4>
            
            <div class="recommendation-item">
              <div class="recommendation-number">1</div>
              <p>Ajustar el cronograma considerando 13.5 días en lugar de ${estimatedTime} días.</p>
            </div>

            <div class="recommendation-item">
              <div class="recommendation-number">2</div>
              <p>Establecer puntos de control cada 3 días para monitorear el progreso real.</p>
            </div>

            <div class="recommendation-item">
              <div class="recommendation-number">3</div>
              <p>Considerar asignar recursos adicionales si se requiere cumplir con el plazo inicial.</p>
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
