import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { API_URL } from '../utils/api';

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
              <p class="module-description">Modelo CatBoost Numeric Only - R² = 0.9742 (97.4% varianza explicada)</p>
            </div>
          </div>

          <div class="risk-container">
            <!-- Formulario -->
            <div class="risk-form-card">
              <h3>Predicción de Duración</h3>
              <p class="form-subtitle">Ingrese los datos de la tarea para estimar la duración real</p>

              <form id="durationForm">
                <div class="form-group">
                  <label>Nombre de la Tarea</label>
                  <input type="text" id="taskName" placeholder="Ej: Implementación Sistema CRM" style="width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px;" />
                </div>

                <div class="form-group">
                  <label>Área</label>
                  <select id="taskArea" style="width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px;">
                    <option value="">Cargando áreas...</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Complejidad de la Tarea</label>
                  <select id="taskComplexity" required style="width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px;">
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
                    style="width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px;"
                  />
                </div>

                <div class="form-group">
                  <label>Asignar a Persona</label>
                  <select id="personId" style="width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px;">
                    <option value="">Sin asignar</option>
                  </select>
                </div>

                <button type="submit" class="btn-calculate">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  Predecir Duración
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
                <h3>Ingrese los datos de la tarea</h3>
                <p>El sistema predecirá la duración real utilizando inteligencia artificial</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

async function loadAreasForSelector() {
  try {
    const response = await fetch(`${API_URL}/areas?status=active`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      const areaSelect = document.getElementById('taskArea') as HTMLSelectElement;
      
      if (areaSelect && data.areas) {
        // Limpiar opciones existentes excepto la primera
        areaSelect.innerHTML = '<option value="">Seleccionar área</option>';
        
        data.areas.forEach((area: any) => {
          const option = document.createElement('option');
          option.value = area.name;
          option.textContent = area.name;
          areaSelect.appendChild(option);
        });
      }
    }
  } catch (error) {
    console.error('Error cargando áreas:', error);
  }
}

async function loadPersonsForSelector() {
  try {
    const response = await fetch(`${API_URL}/users`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      const personSelect = document.getElementById('personId') as HTMLSelectElement;
      
      if (personSelect && data.users) {
        data.users.forEach((user: any) => {
          const option = document.createElement('option');
          option.value = user.id;
          const exp = user.experience_years || 0;
          const perf = user.performance_index || 50;
          option.textContent = `${user.full_name} - ${exp} años exp, ${perf.toFixed(0)}% perf`;
          personSelect.appendChild(option);
        });
      }
    }
  } catch (error) {
    console.error('Error cargando personas:', error);
  }
}

function displayResults(
  estimatedTime: string,
  predictedDuration: number,
  difference: number,
  percentDiff: string,
  confidenceInterval: any,
  factors: string[],
  mode: string,
  resultCard: HTMLElement | null,
  taskName?: string,
  taskArea?: string
) {
  if (!resultCard) return;
  
  const minDuration = confidenceInterval.min || predictedDuration * 0.8;
  const maxDuration = confidenceInterval.max || predictedDuration * 1.2;
  const meanDuration = confidenceInterval.mean || predictedDuration;
  
  resultCard.innerHTML = `
    <div class="duration-results" style="padding: 20px;">
      ${taskName || taskArea ? `
      <div style="background: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 4px solid #00bcd4; margin-bottom: 20px;">
        ${taskName ? `<div style="font-size: 16px; font-weight: 600; color: #00838f; margin-bottom: 5px;"> ${taskName}</div>` : ''}
        ${taskArea ? `<div style="font-size: 14px; color: #0097a7;"> Área: <strong>${taskArea}</strong></div>` : ''}
      </div>
      ` : ''}
      <!-- Cards de Resultado -->
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
        <!-- Estimación Inicial -->
        <div style="background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #dee2e6;">
          <h4 style="margin: 0 0 10px 0; color: #6c757d; font-size: 14px; font-weight: 500;">Estimación Inicial</h4>
          <div style="font-size: 32px; font-weight: 700; color: #495057; margin: 10px 0;">${estimatedTime} días</div>
          <p style="margin: 0; color: #6c757d; font-size: 13px;">Tiempo planificado</p>
        </div>

        <!-- Predicción IA -->
        <div style="background: linear-gradient(135deg, rgba(0, 188, 212, 0.1) 0%, rgba(0, 188, 212, 0.2) 100%); padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #00bcd4;">
          <h4 style="margin: 0 0 10px 0; color: #00bcd4; font-size: 14px; font-weight: 600;">Predicción IA (CatBoost)</h4>
          <div style="font-size: 36px; font-weight: 700; color: #00bcd4; margin: 10px 0;">${Math.round(predictedDuration)} ${Math.round(predictedDuration) === 1 ? 'día' : 'días'}</div>
          <p style="margin: 0; color: #00838f; font-size: 13px;">Duración estimada real</p>
        </div>

        <!-- Diferencia -->
        <div style="background: ${difference > 0 ? 'rgba(255, 152, 0, 0.1)' : 'rgba(76, 175, 80, 0.1)'}; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid ${difference > 0 ? '#ff9800' : '#4caf50'};">
          <h4 style="margin: 0 0 10px 0; color: ${difference > 0 ? '#ff9800' : '#4caf50'}; font-size: 14px; font-weight: 500;">Diferencia</h4>
          <div style="font-size: 32px; font-weight: 700; color: ${difference > 0 ? '#ff9800' : '#4caf50'}; margin: 10px 0;">${difference > 0 ? '+' : ''}${Math.round(difference)} ${Math.abs(Math.round(difference)) === 1 ? 'día' : 'días'}</div>
          <p style="margin: 0; color: ${difference > 0 ? '#e65100' : '#2e7d32'}; font-size: 13px;">(${percentDiff}% ${difference > 0 ? 'más tiempo' : 'menos tiempo'})</p>
        </div>
      </div>

      <!-- Intervalo de Confianza -->
      <div style="background: #fff; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #e0e0e0;">
        <h4 style="margin: 0 0 8px 0; color: #495057; font-size: 16px;"> Intervalo de Confianza (80%)</h4>
        <p style="margin: 0 0 20px 0; color: #6c757d; font-size: 14px;">Rango esperado de duración según modelo CatBoost</p>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px;">
          <span><strong>Mínimo:</strong> ${Math.round(minDuration)} ${Math.round(minDuration) === 1 ? 'día' : 'días'}</span>
          <span><strong>Promedio:</strong> ${Math.round(meanDuration)} ${Math.round(meanDuration) === 1 ? 'día' : 'días'}</span>
          <span><strong>Máximo:</strong> ${Math.round(maxDuration)} ${Math.round(maxDuration) === 1 ? 'día' : 'días'}</span>
        </div>
        
        <div style="height: 30px; background: linear-gradient(90deg, #4caf50 0%, #00bcd4 50%, #ff9800 100%); border-radius: 15px; position: relative;">
          <div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 4px; height: 40px; background: #fff; border-radius: 2px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>
        </div>

        <div style="margin-top: 20px; padding: 15px; background: rgba(33, 150, 243, 0.1); border-radius: 8px; border-left: 4px solid #2196f3;">
          <p style="margin: 0; color: #1565c0; font-size: 14px;">
             Con 80% de confianza, la tarea tomará entre <strong>${Math.round(minDuration)} y ${Math.round(maxDuration)} días</strong>. Se recomienda planificar con <strong>${Math.round(meanDuration)} ${Math.round(meanDuration) === 1 ? 'día' : 'días'}</strong>.
          </p>
        </div>
      </div>

      ${factors.length > 0 ? `
      <div style="background: #fff; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #e0e0e0;">
        <h4 style="margin: 0 0 15px 0; color: #495057; font-size: 16px;"> Factores que Afectan la Duración</h4>
        <ul style="margin: 0; padding: 0 0 0 20px; color: #6c757d; font-size: 14px; line-height: 2;">
          ${factors.map(factor => `<li>${factor}</li>`).join('')}
        </ul>
      </div>
      ` : ''}

      <!-- Información del Modelo -->
      <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #e0e0e0;">
        <h4 style="margin: 0 0 10px 0; color: #495057; font-size: 15px;"> Información del Modelo</h4>
        <p style="margin: 0; color: #6c757d; font-size: 14px; line-height: 1.6;">
          ${mode === 'personalizado' ? 'Predicción personalizada basada en las métricas del colaborador seleccionado.' : 'Predicción genérica basada en datos históricos del sistema.'}
        </p>
      </div>

      <!-- Recomendaciones -->
      <div style="background: #fff; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0;">
        <h4 style="margin: 0 0 20px 0; color: #495057; font-size: 16px;"> Recomendaciones</h4>
        
        <div style="display: flex; gap: 15px; margin-bottom: 15px; padding: 15px; background: rgba(0, 188, 212, 0.05); border-left: 4px solid #00bcd4; border-radius: 4px;">
          <div style="background: #00bcd4; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">1</div>
          <p style="margin: 0; color: #495057; font-size: 14px;"><strong>Ajustar cronograma:</strong> Considerar ${Math.round(meanDuration)} ${Math.round(meanDuration) === 1 ? 'día' : 'días'} en lugar de ${estimatedTime} días${difference > 2 ? ' <span style="color: #ff9800;">(diferencia significativa)</span>' : ''}.</p>
        </div>

        ${difference > 3 ? `
        <div style="display: flex; gap: 15px; margin-bottom: 15px; padding: 15px; background: rgba(255, 152, 0, 0.05); border-left: 4px solid #ff9800; border-radius: 4px;">
          <div style="background: #ff9800; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">2</div>
          <p style="margin: 0; color: #495057; font-size: 14px;"><strong>Recursos adicionales:</strong> La predicción es ${percentDiff}% mayor. Considera asignar más personas o reducir alcance.</p>
        </div>
        ` : ''}

        <div style="display: flex; gap: 15px; margin-bottom: ${mode === 'genérico' ? '15px' : '0'}; padding: 15px; background: rgba(33, 150, 243, 0.05); border-left: 4px solid #2196f3; border-radius: 4px;">
          <div style="background: #2196f3; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">${difference > 3 ? '3' : '2'}</div>
          <p style="margin: 0; color: #495057; font-size: 14px;"><strong>Monitoreo:</strong> Establecer checkpoints cada ${Math.ceil(meanDuration / 3)} ${Math.ceil(meanDuration / 3) === 1 ? 'día' : 'días'} para validar el progreso real.</p>
        </div>

        ${mode === 'genérico' ? `
        <div style="display: flex; gap: 15px; padding: 15px; background: rgba(76, 175, 80, 0.05); border-left: 4px solid #4caf50; border-radius: 4px;">
          <div style="background: #4caf50; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">${difference > 3 ? '4' : '3'}</div>
          <p style="margin: 0; color: #495057; font-size: 14px;"><strong>Mejora de predicción:</strong> Selecciona una persona específica arriba para obtener estimación personalizada basada en experiencia y rendimiento real.</p>
        </div>
        ` : ''}
      </div>
    </div>
  `;

  // Scroll al resultado
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

export function initDurationPrediction() {
  initAIAssistant();

  const form = document.getElementById('durationForm') as HTMLFormElement;
  const resultCard = document.getElementById('durationResult');

  // Cargar áreas y personas para los selectores
  loadAreasForSelector();
  loadPersonsForSelector();

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const taskName = (document.getElementById('taskName') as HTMLInputElement)?.value;
      const taskArea = (document.getElementById('taskArea') as HTMLSelectElement)?.value;
      const taskComplexity = (document.getElementById('taskComplexity') as HTMLSelectElement)?.value;
      const estimatedTime = (document.getElementById('estimatedTime') as HTMLInputElement)?.value;
      const personId = (document.getElementById('personId') as HTMLSelectElement)?.value;

      if (!taskComplexity || !estimatedTime) {
        alert('Por favor complete los campos requeridos (Complejidad y Duración Estimada)');
        return;
      }

      try {
        const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Prediciendo con IA...';

        // Preparar datos según modelo numeric_only
        const requestData: any = {
          complexity_level: taskComplexity,
          duration_est_days: parseFloat(estimatedTime)
        };

        // Si se seleccionó persona, agregar person_id para modo personalizado
        if (personId) {
          requestData.person_id = parseInt(personId);
        }

        console.log('📤 Enviando solicitud:', requestData);

        const response = await fetch(`${API_URL}/ml/tiempo-real`, {
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
          throw new Error(errorData.details || errorData.error || 'Error al estimar duración');
        }

        const data = await response.json();
        console.log('📊 Respuesta del modelo:', data);
        
        // Extraer datos de la respuesta
        const predictedDuration = data.predicted_duration_days || data.duration;
        const confidenceInterval = data.confidence_interval || {
          min: predictedDuration * 0.8,
          max: predictedDuration * 1.2,
          mean: predictedDuration
        };
        const factors = data.factors || [];
        const mode = requestData.person_id ? 'personalizado' : 'genérico';
        
        const difference = predictedDuration - parseFloat(estimatedTime);
        const percentDiff = ((difference / parseFloat(estimatedTime)) * 100).toFixed(1);
        
        displayResults(estimatedTime, predictedDuration, difference, percentDiff, confidenceInterval, factors, mode, resultCard, taskName, taskArea);
      
      } catch (error) {
        console.error('❌ Error completo:', error);
        if (resultCard) {
          resultCard.innerHTML = `
            <div style="text-align: center; padding: 40px;">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                <circle cx="30" cy="30" r="25" stroke="#f44336" stroke-width="2"/>
                <path d="M30 20v12M30 38v2" stroke="#f44336" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <h3 style="color: #f44336; margin: 20px 0 10px 0;">Error al predecir duración</h3>
              <p style="color: #6c757d; margin: 0;">${(error as Error).message}</p>
              <button class="btn-calculate" style="margin-top: 20px;" onclick="location.reload()">
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
              <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Predecir Duración Real con IA
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
