import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function PersonTaskRecommendationPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('recomendacion')}
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
                <circle cx="12" cy="10" r="4" stroke="white" stroke-width="2"/>
                <path d="M6 22c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="white" stroke-width="2" stroke-linecap="round"/>
                <rect x="20" y="14" width="8" height="8" rx="1" stroke="white" stroke-width="2"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Sistema de Recomendación Persona-Tarea</h2>
              <p class="module-description">Modelo 3: Asignación óptima de colaboradores para cada tarea</p>
            </div>
          </div>

          <div class="risk-container">
            <!-- Formulario -->
            <div class="risk-form-card">
              <h3>Requisitos de la Tarea</h3>
              <p class="form-subtitle">Defina los criterios para la recomendación</p>

              <form id="recommendationForm">
                <div class="form-group">
                  <label>Nombre de la Tarea</label>
                  <input type="text" id="taskName" placeholder="Ej: Desarrollo API REST" />
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
                  <label>Habilidades Requeridas</label>
                  <input type="text" id="skills" placeholder="Python, React, SQL..." />
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
                  <label>Urgencia</label>
                  <select id="urgency">
                    <option value="">Nivel de urgencia</option>
                    <option value="Baja">Baja</option>
                    <option value="Media">Media</option>
                    <option value="Alta">Alta</option>
                    <option value="Crítica">Crítica</option>
                  </select>
                </div>

                <button type="submit" class="btn-calculate">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M5 17c0-2.8 2.2-5 5-5s5 2.2 5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  Recomendar Colaborador
                </button>
              </form>
            </div>

            <!-- Resultado -->
            <div class="risk-result-card" id="recommendationResult">
              <div class="result-empty">
                <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                  <circle cx="40" cy="40" r="20" stroke="#cbd5e0" stroke-width="3"/>
                  <circle cx="40" cy="32" r="8" stroke="#cbd5e0" stroke-width="3"/>
                  <path d="M24 64c0-8.8 7.2-16 16-16s16 7.2 16 16" stroke="#cbd5e0" stroke-width="3" stroke-linecap="round"/>
                </svg>
                <h3>Defina los requisitos de la tarea</h3>
                <p>El sistema recomendará al colaborador más adecuado</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

export function initPersonTaskRecommendation() {
  initAIAssistant();

  const form = document.getElementById('recommendationForm') as HTMLFormElement;
  const resultCard = document.getElementById('recommendationResult');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Simular recomendación
      if (resultCard) {
        resultCard.innerHTML = `
          <!-- Recomendación Principal -->
          <div class="recommendation-main">
            <div class="recommendation-header">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="#ffc107"/>
              </svg>
              <h3>Recomendación Principal</h3>
            </div>
            <p class="recommendation-subtitle">El colaborador más adecuado para esta tarea</p>

            <div class="person-card main-recommendation">
              <div class="person-avatar">LG</div>
              <div class="person-info">
                <div class="person-name">
                  Luis García
                  <span class="person-badge">TI</span>
                </div>
                <div class="person-label">Compatibilidad</div>
                <div class="compatibility-metrics">
                  <div class="metric-item">
                    <span class="metric-label">Probabilidad de Éxito</span>
                    <div class="metric-bar">
                      <div class="metric-fill" style="width: 94%"></div>
                    </div>
                    <span class="metric-value">94%</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-label">Probabilidad de Éxito</span>
                    <div class="metric-bar">
                      <div class="metric-fill success" style="width: 92%"></div>
                    </div>
                    <span class="metric-value">92%</span>
                  </div>
                </div>
                <div class="person-skills">
                  <span class="skill-tag">Python</span>
                  <span class="skill-tag">React</span>
                  <span class="skill-tag">Machine Learning</span>
                  <span class="skill-tag">SQL</span>
                </div>
                <div class="person-stats">
                  <div class="stat-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M8 5v3l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                    <span>Tiempo Estimado</span>
                    <strong>8.5d</strong>
                  </div>
                  <div class="stat-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <rect x="3" y="3" width="10" height="10" rx="1" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M6 8l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                    <span>Disponibilidad</span>
                    <strong class="status-badge success">Alta</strong>
                  </div>
                  <div class="stat-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M8 5v3M8 11v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                    <span>Riesgo</span>
                    <strong class="status-badge low">Riesgo Bajo</strong>
                  </div>
                  <div class="stat-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M14 11l-5-5-2 2-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                    <span>Desempeño Prom.</span>
                    <strong>88%</strong>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Otras Recomendaciones -->
          <div class="other-recommendations">
            <h4>Otras Recomendaciones</h4>
            <p class="section-subtitle">Colaboradores alternativos ordenados por compatibilidad</p>

            <div class="person-card">
              <div class="person-number">#2</div>
              <div class="person-avatar alt">MR</div>
              <div class="person-info">
                <div class="person-name">
                  María Rodríguez
                  <span class="person-badge">TI</span>
                  <span class="person-badge orange">Media</span>
                </div>
                <div class="person-label">Compatibilidad</div>
                <div class="simple-metrics">
                  <div class="simple-metric">
                    <div class="simple-bar">
                      <div class="simple-fill" style="width: 87%"></div>
                    </div>
                    <span>87%</span>
                  </div>
                  <div class="simple-metric">
                    <span class="simple-label">Éxito Estimado</span>
                    <div class="simple-bar">
                      <div class="simple-fill" style="width: 85%"></div>
                    </div>
                    <span>85%</span>
                  </div>
                  <div class="simple-metric">
                    <span class="simple-label">Tiempo</span>
                    <strong>10d</strong>
                    <strong class="status-badge low">Riesgo Bajo</strong>
                  </div>
                </div>
                <div class="person-skills">
                  <span class="skill-tag">JavaScript</span>
                  <span class="skill-tag">Node.js</span>
                  <span class="skill-tag">DevOps</span>
                  <span class="skill-tag extra">+1</span>
                </div>
              </div>
            </div>

            <div class="person-card">
              <div class="person-number">#3</div>
              <div class="person-avatar alt">CM</div>
              <div class="person-info">
                <div class="person-name">
                  Carlos Mendoza
                  <span class="person-badge">TI</span>
                  <span class="person-badge red">Baja</span>
                </div>
                <div class="person-label">Compatibilidad</div>
                <div class="simple-metrics">
                  <div class="simple-metric">
                    <div class="simple-bar">
                      <div class="simple-fill" style="width: 78%"></div>
                    </div>
                    <span>78%</span>
                  </div>
                  <div class="simple-metric">
                    <span class="simple-label">Éxito Estimado</span>
                    <div class="simple-bar">
                      <div class="simple-fill" style="width: 80%"></div>
                    </div>
                    <span>80%</span>
                  </div>
                  <div class="simple-metric">
                    <span class="simple-label">Tiempo</span>
                    <strong>11.5d</strong>
                    <strong class="status-badge medium">Riesgo Medio</strong>
                  </div>
                </div>
                <div class="person-skills">
                  <span class="skill-tag">Java</span>
                  <span class="skill-tag">Spring</span>
                  <span class="skill-tag">Microservicios</span>
                  <span class="skill-tag extra">+1</span>
                </div>
              </div>
            </div>

            <div class="person-card">
              <div class="person-number">#4</div>
              <div class="person-avatar alt">AF</div>
              <div class="person-info">
                <div class="person-name">
                  Ana Fernández
                  <span class="person-badge">TI</span>
                  <span class="person-badge green">Alta</span>
                </div>
                <div class="person-label">Compatibilidad</div>
                <div class="simple-metrics">
                  <div class="simple-metric">
                    <div class="simple-bar">
                      <div class="simple-fill" style="width: 82%"></div>
                    </div>
                    <span>82%</span>
                  </div>
                  <div class="simple-metric">
                    <span class="simple-label">Éxito Estimado</span>
                    <div class="simple-bar">
                      <div class="simple-fill" style="width: 88%"></div>
                    </div>
                    <span>88%</span>
                  </div>
                  <div class="simple-metric">
                    <span class="simple-label">Tiempo</span>
                    <strong>9d</strong>
                    <strong class="status-badge low">Riesgo Bajo</strong>
                  </div>
                </div>
                <div class="person-skills">
                  <span class="skill-tag">React</span>
                  <span class="skill-tag">TypeScript</span>
                  <span class="skill-tag">UI/UX</span>
                  <span class="skill-tag extra">+1</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Análisis de IA -->
          <div class="ai-analysis">
            <h4>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                <circle cx="10" cy="10" r="8" fill="#00bcd4"/>
                <path d="M10 6v4M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Análisis de IA
            </h4>

            <div class="analysis-item success">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="10" cy="10" r="8" fill="#28a745"/>
                <path d="M6 10l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <p>Luis García tiene la mejor combinación de habilidades técnicas y experiencia previa en tareas similares.</p>
            </div>

            <div class="analysis-item info">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="#0072c6"/>
              </svg>
              <p>Su historial muestra un 88% de desempeño promedio con 47 tareas completadas exitosamente.</p>
            </div>

            <div class="analysis-item warning">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 2l8 14H2l8-14z" fill="#ffc107"/>
                <path d="M10 8v3M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <p>Si Luis García no está disponible, considere a María Rodríguez como segunda opción (87% compatibilidad).</p>
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
