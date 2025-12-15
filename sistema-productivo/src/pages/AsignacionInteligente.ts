import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { API_URL } from '../utils/api';

export function AsignacionInteligentePage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('asignacion')}
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
            <div class="module-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <path d="M16 4l3 9h9l-7 6 3 9-8-6-8 6 3-9-7-6h9l3-9z" fill="white"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Asignación Inteligente de Tareas</h2>
              <p class="module-description">Combina Riesgo + Recomendación + Duración en un solo análisis</p>
            </div>
          </div>

          <div class="assignment-container">
            <!-- Formulario -->
            <div class="assignment-form-card">
              <h3>Datos de la Tarea</h3>
              <p class="form-subtitle">Ingrese las características para obtener recomendaciones inteligentes</p>

              <form id="assignmentForm">
                <div class="form-group">
                  <label>Complejidad de la Tarea</label>
                  <select id="taskComplexity" required>
                    <option value="">Seleccionar complejidad</option>
                    <option value="Baja">Baja</option>
                    <option value="Media">Media</option>
                    <option value="Alta">Alta</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Duración Estimada Inicial (días)</label>
                  <input 
                    type="number" 
                    id="estimatedTime" 
                    placeholder="Ej: 10" 
                    min="1" 
                    max="90"
                    step="0.5"
                    required 
                  />
                </div>

                <div class="form-group">
                  <label>Número de Personas a Asignar</label>
                  <input 
                    type="number" 
                    id="assigneesCount" 
                    placeholder="Ej: 1" 
                    min="1" 
                    max="10"
                    value="1"
                  />
                </div>

                <div class="form-group">
                  <label>Dependencias de Tareas</label>
                  <input 
                    type="number" 
                    id="dependencies" 
                    placeholder="Número de dependencias" 
                    min="0" 
                    max="20"
                    value="0"
                  />
                </div>

                <div class="form-group">
                  <label>Área</label>
                  <select id="taskArea">
                    <option value="">Todas las áreas</option>
                    <!-- Se cargan dinámicamente desde la BD -->
                  </select>
                </div>

                <div class="form-group">
                  <label>Tipo de Tarea</label>
                  <select id="taskType">
                    <option value="">Sin especificar</option>
                    <option value="desarrollo">Desarrollo</option>
                    <option value="bug">Corrección de Bug</option>
                    <option value="feature">Nueva Funcionalidad</option>
                    <option value="refactor">Refactorización</option>
                    <option value="testing">Testing</option>
                    <option value="documentacion">Documentación</option>
                  </select>
                </div>

                <button type="submit" class="btn-analyze">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
                  </svg>
                  Analizar con IA
                </button>
              </form>
            </div>

            <!-- Resultados -->
            <div class="assignment-result-card" id="assignmentResult">
              <div class="result-empty">
                <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                  <path d="M40 10l6 18h18l-14 12 6 18-16-12-16 12 6-18-14-12h18l6-18z" stroke="#cbd5e0" stroke-width="3"/>
                </svg>
                <h3>Ingrese los datos de la tarea</h3>
                <p>El sistema analizará riesgo, recomendará personas y estimará duración para cada candidato</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

function displayResults(risk: any, recommendations: any[], resultCard: HTMLElement | null) {
  if (!resultCard) return;
  
  // Normalizar y validar riskLevel
  let riskLevelRaw = (risk.level || 'MEDIO').toString().toUpperCase();
  const validLevels = ['BAJO', 'MEDIO', 'ALTO'];
  const riskLevel = (validLevels.includes(riskLevelRaw) ? riskLevelRaw : 'MEDIO') as 'BAJO' | 'MEDIO' | 'ALTO';
  
  const riskProbability = risk.probability || 50;
  const riskFactors = risk.factors || [];
  
  const riskColors: Record<'BAJO' | 'MEDIO' | 'ALTO', { bg: string; border: string; text: string }> = {
    'BAJO': { bg: '#e8f5e9', border: '#4caf50', text: '#2e7d32' },
    'MEDIO': { bg: '#fff3e0', border: '#ff9800', text: '#e65100' },
    'ALTO': { bg: '#ffebee', border: '#f44336', text: '#c62828' }
  };
  
  const colors = riskColors[riskLevel];
  
  resultCard.innerHTML = `
    <div class="assignment-results">
      <!-- Análisis de Riesgo -->
      <div style="background: ${colors.bg}; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 2px solid ${colors.border};">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
          <div style="width: 50px; height: 50px; background: ${colors.border}; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7v6c0 5.5 3.8 10.7 10 12 6.2-1.3 10-6.5 10-12V7l-10-5z" fill="white"/>
            </svg>
          </div>
          <div>
            <h3 style="margin: 0 0 5px 0; color: ${colors.text}; font-size: 20px;">Nivel de Riesgo: ${riskLevel}</h3>
            <p style="margin: 0; color: ${colors.text}; font-size: 14px;">Probabilidad: ${riskProbability.toFixed(0)}%</p>
          </div>
        </div>
        
        ${riskFactors.length > 0 ? `
        <div style="background: rgba(255,255,255,0.6); padding: 15px; border-radius: 8px;">
          <strong style="color: ${colors.text}; font-size: 14px; display: block; margin-bottom: 10px;">Factores de riesgo:</strong>
          <ul style="margin: 0; padding: 0 0 0 20px; color: ${colors.text}; font-size: 13px; line-height: 1.8;">
            ${riskFactors.map((f: string) => `<li>${f}</li>`).join('')}
          </ul>
        </div>
        ` : ''}
      </div>

      <!-- Resumen Ejecutivo -->
      ${recommendations.length > 0 ? `
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;">
          <div style="font-size: 12px; opacity: 0.9; margin-bottom: 5px;">MEJOR CANDIDATO</div>
          <div style="font-size: 20px; font-weight: 700; margin-bottom: 5px;">${recommendations[0].person_name}</div>
          <div style="font-size: 14px; opacity: 0.9;">${recommendations[0].score.toFixed(0)}% Match</div>
        </div>
        <div style="background: linear-gradient(135deg, #00bcd4 0%, #00838f 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;">
          <div style="font-size: 12px; opacity: 0.9; margin-bottom: 5px;">DURACIÓN ESTIMADA</div>
          <div style="font-size: 24px; font-weight: 700; margin-bottom: 5px;">${recommendations[0].predicted_duration_days ? recommendations[0].predicted_duration_days.toFixed(1) : 'N/A'}</div>
          <div style="font-size: 14px; opacity: 0.9;">días</div>
        </div>
        <div style="background: linear-gradient(135deg, ${riskLevel === 'ALTO' ? '#f44336 0%, #c62828' : riskLevel === 'MEDIO' ? '#ff9800 0%, #e65100' : '#4caf50 0%, #2e7d32'} 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;">
          <div style="font-size: 12px; opacity: 0.9; margin-bottom: 5px;">NIVEL DE RIESGO</div>
          <div style="font-size: 24px; font-weight: 700; margin-bottom: 5px;">${riskLevel}</div>
          <div style="font-size: 14px; opacity: 0.9;">${riskProbability.toFixed(0)}% probabilidad</div>
        </div>
      </div>
      ` : ''}

      <!-- Tabla de Recomendaciones -->
      <h3 style="margin: 0 0 20px 0; color: #495057; font-size: 18px;">🎯 Candidatos Recomendados (${recommendations.length})</h3>
      
      ${recommendations.length > 0 ? `
      <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden;">
          <thead>
            <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
              <th style="padding: 15px; text-align: left; font-weight: 600;">Persona</th>
              <th style="padding: 15px; text-align: center; font-weight: 600;">Score</th>
              <th style="padding: 15px; text-align: center; font-weight: 600;">Duración Est.</th>
              <th style="padding: 15px; text-align: center; font-weight: 600;">Experiencia</th>
              <th style="padding: 15px; text-align: center; font-weight: 600;">Carga</th>
              <th style="padding: 15px; text-align: left; font-weight: 600;">Observaciones</th>
            </tr>
          </thead>
          <tbody>
            ${recommendations.map((rec, index) => `
              <tr style="border-bottom: 1px solid #e0e0e0; ${index === 0 ? 'background: rgba(102, 126, 234, 0.05);' : ''}">
                <td style="padding: 15px;">
                  <div style="display: flex; align-items: center; gap: 10px;">
                    ${index === 0 ? '<span style="font-size: 20px;">⭐</span>' : ''}
                    <strong style="color: #495057;">${rec.person_name}</strong>
                  </div>
                </td>
                <td style="padding: 15px; text-align: center;">
                  <span style="display: inline-block; padding: 5px 12px; background: ${rec.score >= 90 ? '#4caf50' : rec.score >= 75 ? '#ff9800' : '#9e9e9e'}; color: white; border-radius: 20px; font-weight: 600; font-size: 14px;">
                    ${rec.score.toFixed(0)}%
                  </span>
                </td>
                <td style="padding: 15px; text-align: center;">
                  <strong style="color: #667eea; font-size: 16px;">
                    ${rec.predicted_duration_days ? rec.predicted_duration_days.toFixed(1) + ' días' : 'N/A'}
                  </strong>
                </td>
                <td style="padding: 15px; text-align: center; color: #6c757d;">
                  ${rec.experience_years} años
                </td>
                <td style="padding: 15px; text-align: center;">
                  <span style="color: ${rec.current_load > 5 ? '#f44336' : rec.current_load > 3 ? '#ff9800' : '#4caf50'}; font-weight: 600;">
                    ${rec.current_load} tareas
                  </span>
                </td>
                <td style="padding: 15px;">
                  ${rec.observations.length > 0 ? rec.observations.join('<br>') : '-'}
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>

      <!-- Recomendaciones -->
      <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;">
        <h4 style="margin: 0 0 15px 0; color: #495057; font-size: 16px;">💡 Recomendaciones</h4>
        
        ${recommendations[0] ? `
        <div style="background: white; padding: 15px; border-radius: 6px; margin-bottom: 10px;">
          <strong style="color: #667eea;">✅ Mejor candidato:</strong> 
          <span style="color: #495057;">${recommendations[0].person_name} (${recommendations[0].score.toFixed(0)}% match, ${recommendations[0].predicted_duration_days ? recommendations[0].predicted_duration_days.toFixed(1) + ' días estimados' : 'duración N/A'})</span>
        </div>
        ` : ''}
        
        ${riskLevel === 'ALTO' ? `
        <div style="background: white; padding: 15px; border-radius: 6px; margin-bottom: 10px;">
          <strong style="color: #f44336;">⚠️ Riesgo alto:</strong> 
          <span style="color: #495057;">Asignar seguimiento diario y considerar pair programming</span>
        </div>
        ` : ''}
        
        ${recommendations.filter(r => r.current_load > 5).length > 0 ? `
        <div style="background: white; padding: 15px; border-radius: 6px;">
          <strong style="color: #ff9800;">⚠️ Carga alta:</strong> 
          <span style="color: #495057;">Algunos candidatos tienen sobrecarga. Considerar redistribuir tareas.</span>
        </div>
        ` : ''}
      </div>
      ` : `
      <div style="text-align: center; padding: 40px; background: #f8f9fa; border-radius: 8px;">
        <p style="color: #6c757d; margin: 0;">No se encontraron candidatos disponibles</p>
      </div>
      `}
    </div>
  `;

  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function loadAreasForForm() {
  try {
    const response = await fetch(`${API_URL}/areas`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      const areas = data.areas || [];
      
      // Filtrar solo áreas activas
      const activeAreas = areas.filter((area: any) => area.status === 'active');
      
      const taskAreaSelect = document.getElementById('taskArea') as HTMLSelectElement;
      if (taskAreaSelect) {
        // Mantener la opción "Todas las áreas"
        taskAreaSelect.innerHTML = '<option value="">Todas las áreas</option>';
        activeAreas.forEach((area: any) => {
          const option = document.createElement('option');
          option.value = area.name;
          option.textContent = area.name;
          taskAreaSelect.appendChild(option);
        });
      }
    }
  } catch (error) {
    console.error('Error al cargar áreas:', error);
  }
}

export function initAsignacionInteligente() {
  initAIAssistant();

  // Cargar áreas desde la BD
  loadAreasForForm();

  const form = document.getElementById('assignmentForm') as HTMLFormElement;
  const resultCard = document.getElementById('assignmentResult');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const taskComplexity = (document.getElementById('taskComplexity') as HTMLSelectElement)?.value;
      const estimatedTime = (document.getElementById('estimatedTime') as HTMLInputElement)?.value;
      const assigneesCount = (document.getElementById('assigneesCount') as HTMLInputElement)?.value;
      const dependencies = (document.getElementById('dependencies') as HTMLInputElement)?.value;
      const taskArea = (document.getElementById('taskArea') as HTMLSelectElement)?.value;
      const taskType = (document.getElementById('taskType') as HTMLSelectElement)?.value;

      if (!taskComplexity || !estimatedTime) {
        alert('Por favor complete los campos requeridos');
        return;
      }

      try {
        const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="animation: spin 1s linear infinite;">
            <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="2" stroke-dasharray="40" stroke-dashoffset="10"/>
          </svg>
          Analizando...
        `;

        const requestData: any = {
          complexity_level: taskComplexity,
          duration_est_days: parseFloat(estimatedTime),
          assignees_count: parseInt(assigneesCount || '1'),
          dependencies: parseInt(dependencies || '0'),
          top_n: 5
        };

        if (taskArea) {
          requestData.area = taskArea;
        }
        
        if (taskType) {
          requestData.task_type = taskType;
        }

        console.log('📤 Enviando solicitud:', requestData);

        const response = await fetch(`${API_URL}/ml/asignacion-inteligente`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify(requestData)
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error('❌ Error del servidor:', errorData);
          throw new Error(errorData.details || errorData.error || 'Error en análisis');
        }

        const data = await response.json();
        console.log('📊 Respuesta:', data);
        
        displayResults(data.risk, data.recommendations, resultCard);
      
      } catch (error) {
        console.error('❌ Error:', error);
        if (resultCard) {
          resultCard.innerHTML = `
            <div style="text-align: center; padding: 40px;">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                <circle cx="30" cy="30" r="25" stroke="#f44336" stroke-width="2"/>
                <path d="M30 20v12M30 38v2" stroke="#f44336" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <h3 style="color: #f44336; margin: 20px 0 10px 0;">Error en el análisis</h3>
              <p style="color: #6c757d; margin: 0;">${(error as Error).message}</p>
              <button class="btn-analyze" style="margin-top: 20px;" onclick="location.reload()">
                Reintentar
              </button>
            </div>
          `;
        }
      } finally {
        const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
            </svg>
            Analizar con IA
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
      localStorage.removeItem('access_token');
      window.location.hash = '#login';
    });
  }
}
