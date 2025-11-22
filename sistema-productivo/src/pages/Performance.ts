import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function PerformancePage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('desempeno')}
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
                <circle cx="16" cy="12" r="5" stroke="white" stroke-width="2"/>
                <path d="M9 26c0-3.9 3.1-7 7-7s7 3.1 7 7" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Predicción de Desempeño del Colaborador</h2>
              <p class="module-description">Modelo 4: Clasificación multiclase del rendimiento y riesgo operativo</p>
            </div>
          </div>

          <!-- Métricas Principales -->
          <div class="performance-metrics">
            <div class="perf-metric-card">
              <div class="perf-metric-icon star">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="#ffc107"/>
                </svg>
              </div>
              <h3>Top Performers</h3>
              <div class="perf-metric-value">8 Colaboradores</div>
              <p class="perf-metric-desc">Desempeño excelente</p>
            </div>

            <div class="perf-metric-card">
              <div class="perf-metric-icon target">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="8" stroke="#00bcd4" stroke-width="2"/>
                  <circle cx="12" cy="12" r="4" stroke="#00bcd4" stroke-width="2"/>
                  <circle cx="12" cy="12" r="2" fill="#00bcd4"/>
                </svg>
              </div>
              <h3>Rendimiento Prom.</h3>
              <div class="perf-metric-value">82%</div>
              <p class="perf-metric-desc">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" style="display: inline-block; vertical-align: middle;">
                  <path d="M7 10V4M4 7l3-3 3 3" stroke="#28a745" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span style="color: #28a745; font-weight: 600;">+3.5%</span>
              </p>
            </div>

            <div class="perf-metric-card">
              <div class="perf-metric-icon alert">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2l10 18H2L12 2z" stroke="#ff5722" stroke-width="2"/>
                  <path d="M12 10v4M12 16v1" stroke="#ff5722" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <h3>En Riesgo</h3>
              <div class="perf-metric-value">3 Personas</div>
              <p class="perf-metric-desc">Requieren atención</p>
            </div>

            <div class="perf-metric-card">
              <div class="perf-metric-icon trend">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M3 12l5 5L20 5" stroke="#ff9800" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <h3>Riesgo de Renuncia</h3>
              <div class="perf-metric-value">12%</div>
              <p class="perf-metric-desc">Tasa estimada</p>
            </div>
          </div>

          <!-- Contenido Principal -->
          <div class="performance-content">
            <!-- Lista de Colaboradores -->
            <div class="collaborators-section">
              <h3>Lista de Colaboradores</h3>
              <p class="section-subtitle">Seleccione un colaborador para ver predicción detallada</p>

              <table class="collaborators-table">
                <thead>
                  <tr>
                    <th>Colaborador</th>
                    <th>Área</th>
                    <th>Rendimiento</th>
                    <th>Acción</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>
                      <div class="collab-info">
                        <div class="collab-avatar">MR</div>
                        <span>María Rodríguez</span>
                      </div>
                    </td>
                    <td><span class="area-badge">Marketing</span></td>
                    <td>
                      <div class="performance-indicator">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                          <path d="M7 10V4M4 7l3-3 3 3" stroke="#28a745" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="perf-value high">92%</span>
                      </div>
                    </td>
                    <td>
                      <button class="btn-predict" data-person="maria">Predecir</button>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="collab-info">
                        <div class="collab-avatar">LG</div>
                        <span>Luis García</span>
                      </div>
                    </td>
                    <td><span class="area-badge">TI</span></td>
                    <td>
                      <div class="performance-indicator">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                          <path d="M7 10V4M4 7l3-3 3 3" stroke="#28a745" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="perf-value high">88%</span>
                      </div>
                    </td>
                    <td>
                      <button class="btn-predict" data-person="luis">Predecir</button>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="collab-info">
                        <div class="collab-avatar">CM</div>
                        <span>Carlos Mendoza</span>
                      </div>
                    </td>
                    <td><span class="area-badge">Operaciones</span></td>
                    <td>
                      <div class="performance-indicator">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                          <path d="M7 4v6M4 7h6" stroke="#ff9800" stroke-width="1.5" stroke-linecap="round"/>
                        </svg>
                        <span class="perf-value medium">75%</span>
                      </div>
                    </td>
                    <td>
                      <button class="btn-predict" data-person="carlos">Predecir</button>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="collab-info">
                        <div class="collab-avatar">AF</div>
                        <span>Ana Fernández</span>
                      </div>
                    </td>
                    <td><span class="area-badge">Ventas</span></td>
                    <td>
                      <div class="performance-indicator">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                          <path d="M7 4V10M10 7L7 10 4 7" stroke="#dc3545" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="perf-value low">65%</span>
                      </div>
                    </td>
                    <td>
                      <button class="btn-predict" data-person="ana">Predecir</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Comparación de Desempeño -->
            <div class="comparison-section">
              <h3>Comparación de Desempeño</h3>
              <p class="section-subtitle">Rendimiento de colaboradores vs promedio</p>

              <svg class="performance-chart" width="100%" height="300" viewBox="0 0 600 300">
                <!-- Grid -->
                <line x1="40" y1="250" x2="560" y2="250" stroke="#e0e0e0" stroke-width="1"/>
                <line x1="40" y1="50" x2="40" y2="250" stroke="#e0e0e0" stroke-width="1"/>
                
                <!-- Grid lines -->
                <line x1="40" y1="200" x2="560" y2="200" stroke="#f5f5f5" stroke-width="1" stroke-dasharray="4"/>
                <line x1="40" y1="150" x2="560" y2="150" stroke="#f5f5f5" stroke-width="1" stroke-dasharray="4"/>
                <line x1="40" y1="100" x2="560" y2="100" stroke="#f5f5f5" stroke-width="1" stroke-dasharray="4"/>
                
                <!-- Y-axis labels -->
                <text x="30" y="255" text-anchor="end" font-size="12" fill="#6c757d">0</text>
                <text x="30" y="205" text-anchor="end" font-size="12" fill="#6c757d">25</text>
                <text x="30" y="155" text-anchor="end" font-size="12" fill="#6c757d">50</text>
                <text x="30" y="105" text-anchor="end" font-size="12" fill="#6c757d">75</text>
                <text x="30" y="55" text-anchor="end" font-size="12" fill="#6c757d">100</text>
                
                <!-- Bars -->
                <rect x="70" y="62" width="90" height="188" fill="#005a9c" rx="4"/>
                <text x="115" y="280" text-anchor="middle" font-size="13" fill="#495057">María R.</text>
                
                <rect x="190" y="74" width="90" height="176" fill="#0072c6" rx="4"/>
                <text x="235" y="280" text-anchor="middle" font-size="13" fill="#495057">Luis G.</text>
                
                <rect x="310" y="112" width="90" height="138" fill="#00bcd4" rx="4"/>
                <text x="355" y="280" text-anchor="middle" font-size="13" fill="#495057">Carlos M.</text>
                
                <rect x="430" y="162" width="90" height="88" fill="#0072c6" rx="4"/>
                <text x="475" y="280" text-anchor="middle" font-size="13" fill="#495057">Ana F.</text>
                
                <!-- Average line -->
                <line x1="40" y1="86" x2="560" y2="86" stroke="#ff9800" stroke-width="2" stroke-dasharray="6"/>
                <text x="565" y="90" font-size="12" fill="#ff9800" font-weight="600">Promedio</text>
              </svg>
            </div>
          </div>

          <!-- Panel de Detalles (oculto inicialmente) -->
          <div class="detail-panel" id="detailPanel" style="display: none;">
          </div>
        </div>
      </main>
    </div>
  `;
}

export function initPerformance() {
  initAIAssistant();

  const predictButtons = document.querySelectorAll('.btn-predict');
  const detailPanel = document.getElementById('detailPanel');

  predictButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      const person = target.getAttribute('data-person');
      
      if (detailPanel && person) {
        const personData: { [key: string]: any } = {
          maria: { name: 'María Rodríguez', area: 'Marketing', badge: 'Excelente', performance: '92%' },
          luis: { name: 'Luis García', area: 'TI', badge: 'Excelente', performance: '88%' },
          carlos: { name: 'Carlos Mendoza', area: 'Operaciones', badge: 'Bueno', performance: '75%' },
          ana: { name: 'Ana Fernández', area: 'Ventas', badge: 'Regular', performance: '65%' }
        };

        const data = personData[person];
        
        detailPanel.style.display = 'block';
        detailPanel.innerHTML = `
          <div class="detail-header">
            <div class="detail-person">
              <div class="detail-avatar">MR</div>
              <div class="detail-person-info">
                <h3>${data.name}</h3>
                <div class="detail-badges">
                  <span class="area-badge">${data.area}</span>
                  <span class="performance-badge success">${data.badge}</span>
                </div>
              </div>
            </div>
            <div class="detail-performance">
              <span class="detail-perf-value">${data.performance}</span>
              <span class="detail-perf-label">Desempeño</span>
            </div>
          </div>

          <div class="detail-stats">
            <div class="detail-stat">
              <span class="detail-stat-label">Tareas Completadas</span>
              <span class="detail-stat-value">48</span>
            </div>
            <div class="detail-stat">
              <span class="detail-stat-label">Tiempo Promedio</span>
              <span class="detail-stat-value">4.2d</span>
            </div>
            <div class="detail-stat">
              <span class="detail-stat-label">Calidad</span>
              <span class="detail-stat-value">95%</span>
            </div>
            <div class="detail-stat">
              <span class="detail-stat-label">Tendencia</span>
              <span class="detail-stat-value trend-up">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M7 10V4M4 7l3-3 3 3" stroke="#28a745" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Mejora
              </span>
            </div>
          </div>

          <div class="detail-content-grid">
            <!-- Análisis Multidimensional -->
            <div class="detail-section">
              <h4>Análisis Multidimensional</h4>
              <p class="section-subtitle">Métricas de desempeño del colaborador</p>
              
              <svg class="radar-chart" width="100%" height="300" viewBox="0 0 400 300">
                <!-- Pentagon background -->
                <polygon points="200,50 320,115 280,235 120,235 80,115" fill="#f8f9fa" stroke="#e0e0e0" stroke-width="1"/>
                <polygon points="200,90 290,135 265,215 135,215 110,135" fill="#fff" stroke="#e0e0e0" stroke-width="1"/>
                <polygon points="200,130 260,155 250,195 150,195 140,155" fill="#fff" stroke="#e0e0e0" stroke-width="1"/>
                
                <!-- Data polygon -->
                <polygon points="200,70 300,120 270,220 130,220 100,130" fill="rgba(0, 188, 212, 0.3)" stroke="#00bcd4" stroke-width="2"/>
                
                <!-- Axis lines -->
                <line x1="200" y1="150" x2="200" y2="50" stroke="#cbd5e0" stroke-width="1"/>
                <line x1="200" y1="150" x2="320" y2="115" stroke="#cbd5e0" stroke-width="1"/>
                <line x1="200" y1="150" x2="280" y2="235" stroke="#cbd5e0" stroke-width="1"/>
                <line x1="200" y1="150" x2="120" y2="235" stroke="#cbd5e0" stroke-width="1"/>
                <line x1="200" y1="150" x2="80" y2="115" stroke="#cbd5e0" stroke-width="1"/>
                
                <!-- Points -->
                <circle cx="200" cy="70" r="4" fill="#00bcd4"/>
                <circle cx="300" cy="120" r="4" fill="#00bcd4"/>
                <circle cx="270" cy="220" r="4" fill="#00bcd4"/>
                <circle cx="130" cy="220" r="4" fill="#00bcd4"/>
                <circle cx="100" cy="130" r="4" fill="#00bcd4"/>
                
                <!-- Labels -->
                <text x="200" y="40" text-anchor="middle" font-size="12" fill="#495057" font-weight="600">Productividad</text>
                <text x="330" y="120" text-anchor="start" font-size="12" fill="#495057" font-weight="600">Calidad</text>
                <text x="290" y="255" text-anchor="middle" font-size="12" fill="#495057" font-weight="600">Puntualidad</text>
                <text x="110" y="255" text-anchor="middle" font-size="12" fill="#495057" font-weight="600">Colaboración</text>
                <text x="50" y="120" text-anchor="end" font-size="12" fill="#495057" font-weight="600">Innovación</text>
                
                <!-- Values -->
                <text x="200" y="85" text-anchor="middle" font-size="11" fill="#00bcd4" font-weight="600">90</text>
                <text x="285" y="120" text-anchor="start" font-size="11" fill="#00bcd4" font-weight="600">95</text>
                <text x="270" y="210" text-anchor="middle" font-size="11" fill="#00bcd4" font-weight="600">88</text>
                <text x="130" y="210" text-anchor="middle" font-size="11" fill="#00bcd4" font-weight="600">85</text>
                <text x="115" y="130" text-anchor="end" font-size="11" fill="#00bcd4" font-weight="600">82</text>
              </svg>
              
              <div class="legend-note">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <rect width="16" height="16" rx="2" fill="rgba(0, 188, 212, 0.3)"/>
                </svg>
                <span>Desempeño</span>
              </div>
            </div>

            <!-- Predicción de IA -->
            <div class="detail-section">
              <h4>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                  <circle cx="10" cy="10" r="8" fill="#00bcd4"/>
                  <path d="M10 6v4M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Predicción de IA
              </h4>
              <p class="section-subtitle">Análisis de riesgo y recomendaciones</p>

              <div class="prediction-card">
                <div class="prediction-label">Clasificación de Desempeño</div>
                <div class="prediction-result">
                  <span class="prediction-badge success">Excelente</span>
                  <span class="prediction-rank">Top 10%</span>
                </div>
                <div class="prediction-bar">
                  <div class="prediction-fill" style="width: 92%"></div>
                </div>
              </div>

              <div class="prediction-card">
                <div class="prediction-label">Probabilidad de Renuncia</div>
                <div class="prediction-result">
                  <span class="prediction-badge low-risk">Baja</span>
                  <span class="prediction-rank">5-10%</span>
                </div>
                <div class="prediction-bar">
                  <div class="prediction-fill low-risk" style="width: 8%"></div>
                </div>
              </div>

              <div class="recommendations-box">
                <h5>Recomendaciones</h5>
                <ul class="recommendations-list">
                  <li>• Asignar proyectos de alto impacto</li>
                  <li>• Considerar para posiciones de liderazgo</li>
                  <li>• Mantener motivación con desafíos técnicos</li>
                </ul>
              </div>
            </div>
          </div>
        `;

        detailPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
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
