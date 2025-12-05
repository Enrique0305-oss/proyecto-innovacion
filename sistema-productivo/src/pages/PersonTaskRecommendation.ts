import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { api } from '../utils/api';

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
                    <option value="IT">IT</option>
                    <option value="Engineering">Engineering</option>
                    <option value="Operations">Operations</option>
                    <option value="Ventas">Ventas</option>
                    <option value="Gerencia">Gerencia</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Tipo de Tarea</label>
                  <select id="taskType">
                    <option value="">Seleccionar tipo</option>
                    <option value="Desarrollo">Desarrollo</option>
                    <option value="Diseño">Diseño</option>
                    <option value="Análisis">Análisis</option>
                    <option value="Testing">Testing</option>
                    <option value="Documentación">Documentación</option>
                    <option value="Soporte">Soporte</option>
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
                  <label>Duración Estimada (días)</label>
                  <input type="number" id="estimatedDuration" placeholder="Ej: 10" min="1" />
                </div>

                <div class="form-group">
                  <label>Prioridad</label>
                  <select id="taskPriority">
                    <option value="">Seleccionar prioridad</option>
                    <option value="Baja">Baja</option>
                    <option value="Media">Media</option>
                    <option value="Alta">Alta</option>
                    <option value="Crítica">Crítica</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Habilidades Deseadas</label>
                  <input type="text" id="skills" placeholder="Python, React, SQL..." />
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
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      // Capturar valores del formulario
      const taskName = (document.getElementById('taskName') as HTMLInputElement)?.value;
      const taskArea = (document.getElementById('taskArea') as HTMLSelectElement)?.value;
      const taskType = (document.getElementById('taskType') as HTMLSelectElement)?.value;
      const taskComplexity = (document.getElementById('taskComplexity') as HTMLSelectElement)?.value;
      const estimatedDuration = (document.getElementById('estimatedDuration') as HTMLInputElement)?.value;
      const taskPriority = (document.getElementById('taskPriority') as HTMLSelectElement)?.value;
      const skills = (document.getElementById('skills') as HTMLInputElement)?.value;

      // Validación
      if (!taskArea || !taskType || !taskComplexity || !estimatedDuration || !taskPriority) {
        alert('Por favor complete todos los campos requeridos');
        return;
      }

      try {
        const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Buscando colaborador...';

        // Llamada al API
        const response = await fetch('http://127.0.0.1:5000/api/ml/recomendar-persona', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            area: taskArea,
            task_type: taskType,
            complexity_level: taskComplexity,
            duration_est: parseInt(estimatedDuration),
            priority: taskPriority,
            skills_required: skills ? skills.split(',').map(s => s.trim()) : [],
            top_n: 5
          })
        });

        console.log('Response status:', response.status);

        if (response.status === 401) {
          alert('Sesión expirada. Por favor inicia sesión nuevamente.');
          localStorage.removeItem('access_token');
          localStorage.removeItem('isAuthenticated');
          window.location.hash = '#/login';
          return;
        }

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error('Error response:', errorData);
          throw new Error(errorData.error || 'Error al obtener recomendaciones');
        }

        const data = await response.json();
        
        console.log('Recomendaciones del modelo:', data); // Debug

        submitBtn.disabled = false;
        submitBtn.innerHTML = `
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5"/>
            <path d="M5 17c0-2.8 2.2-5 5-5s5 2.2 5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Recomendar Colaborador
        `;

        // Mostrar resultados (por ahora simulado, luego usaremos los datos reales)
        displayRecommendations(data, resultCard, skills);

      } catch (error: any) {
        console.error('Error:', error);
        alert('Error: ' + error.message);
        
        const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5"/>
              <path d="M5 17c0-2.8 2.2-5 5-5s5 2.2 5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Recomendar Colaborador
          `;
        }
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

function displayRecommendations(data: any, resultCard: HTMLElement | null, skills: string) {
  if (!resultCard) return;

  console.log('📊 Datos recibidos del backend:', data);

  const recommendations = data.recommendations || [];
  
  if (recommendations.length === 0) {
    resultCard.innerHTML = `
      <div class="result-empty">
        <h3>No se encontraron candidatos</h3>
        <p>${data.message || 'No hay colaboradores disponibles para esta tarea'}</p>
      </div>
    `;
    return;
  }

  // Primera recomendación (principal)
  const top = recommendations[0];
  const topInitials = top.name.split(' ').map((n: string) => n[0]).join('').toUpperCase().substring(0, 2);
  
  // Otras recomendaciones (del 2 en adelante)
  const others = recommendations.slice(1);

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
        <div class="person-avatar">${topInitials}</div>
        <div class="person-info">
          <div class="person-name">
            ${top.name}
            <span class="person-badge">${top.area}</span>
          </div>
          <div class="person-label">Compatibilidad</div>
          <div class="compatibility-metrics">
            <div class="metric-item">
              <span class="metric-label">Probabilidad de Éxito</span>
              <div class="metric-bar">
                <div class="metric-fill" style="width: ${top.score_percentage}%"></div>
              </div>
              <span class="metric-value">${top.score_percentage}%</span>
            </div>
          </div>
          <div class="person-skills">
            ${(top.skills || []).map((skill: string) => `<span class="skill-tag">${skill}</span>`).join('')}
          </div>
          <div class="person-stats">
            <div class="stat-item">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <rect x="3" y="3" width="10" height="10" rx="1" stroke="currentColor" stroke-width="1.5"/>
                <path d="M6 8l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>Disponibilidad</span>
              <strong class="status-badge ${top.availability === 'Alta' ? 'success' : (top.availability === 'Media' ? 'warning' : 'danger')}">${top.availability}</strong>
            </div>
            <div class="stat-item">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M14 11l-5-5-2 2-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>Desempeño</span>
              <strong>${top.performance_index}%</strong>
            </div>
            <div class="stat-item">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
                <path d="M8 5v3l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>Experiencia</span>
              <strong>${top.experience_years} años</strong>
            </div>
            <div class="stat-item">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
                <path d="M8 5v3M8 11v1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span>Carga actual</span>
              <strong>${top.current_workload} tareas</strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    ${others.length > 0 ? `
    <!-- Otras Recomendaciones -->
    <div class="other-recommendations">
      <h4>Otras Recomendaciones</h4>
      <p class="section-subtitle">Colaboradores alternativos ordenados por compatibilidad</p>

      ${others.map((person: any, index: number) => {
        const initials = person.name.split(' ').map((n: string) => n[0]).join('').toUpperCase().substring(0, 2);
        return `
        <div class="person-card">
          <div class="person-number">#${index + 2}</div>
          <div class="person-avatar alt">${initials}</div>
          <div class="person-info">
            <div class="person-name">
              ${person.name}
              <span class="person-badge">${person.area}</span>
              <span class="person-badge ${person.availability === 'Alta' ? 'green' : (person.availability === 'Media' ? 'orange' : 'red')}">${person.availability}</span>
            </div>
            <div class="person-label">Compatibilidad</div>
            <div class="simple-metrics">
              <div class="simple-metric">
                <div class="simple-bar">
                  <div class="simple-fill" style="width: ${person.score_percentage}%"></div>
                </div>
                <span>${person.score_percentage}%</span>
              </div>
              <div class="simple-metric">
                <span class="simple-label">Desempeño</span>
                <strong>${person.performance_index}%</strong>
                <strong>${person.experience_years} años exp.</strong>
              </div>
              <div class="simple-metric">
                <span class="simple-label">Carga</span>
                <strong>${person.current_workload} tareas</strong>
              </div>
            </div>
            <div class="person-skills">
              ${(person.skills || []).slice(0, 3).map((skill: string) => `<span class="skill-tag">${skill}</span>`).join('')}
              ${(person.skills || []).length > 3 ? `<span class="skill-tag extra">+${(person.skills || []).length - 3}</span>` : ''}
            </div>
          </div>
        </div>
        `;
      }).join('')}
    </div>
    ` : ''}

    <!-- Análisis de IA -->
    <div class="ai-analysis">
      <h4>
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
          <circle cx="10" cy="10" r="8" fill="#00bcd4"/>
          <path d="M10 6v4M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
        Análisis de IA
      </h4>

      ${(top.reasons || []).map((reason: string, idx: number) => {
        const isPositive = reason.includes('Alto') || reason.includes('Excelente') || reason.includes('Buena') || reason.includes('Disponibilidad');
        const isWarning = reason.includes('⚠️') || reason.includes('Alta carga');
        const type = isWarning ? 'warning' : (isPositive ? 'success' : 'info');
        const icon = isWarning ? 
          '<path d="M10 2l8 14H2l8-14z" fill="#ffc107"/><path d="M10 8v3M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>' :
          (isPositive ? 
            '<circle cx="10" cy="10" r="8" fill="#28a745"/><path d="M6 10l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' :
            '<circle cx="10" cy="10" r="8" fill="#0072c6"/><path d="M10 6v4M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>');
        
        return `
        <div class="analysis-item ${type}">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            ${icon}
          </svg>
          <p>${reason}</p>
        </div>
        `;
      }).join('')}
      
      <div class="analysis-item info">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <circle cx="10" cy="10" r="8" fill="#0072c6"/>
          <path d="M10 6v4M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <p>Total de ${data.total_candidates} candidatos evaluados por el modelo CatBoost.</p>
      </div>
    </div>
  `;

  // Scroll al resultado
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
