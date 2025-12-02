import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { api } from '../utils/api';

export function RiskClassificationPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('riesgo')}
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
                  <label>Tiempo Estimado (días)</label>
                  <input type="number" id="estimatedTime" placeholder="Ej: 10" min="1" />
                </div>

                <div class="form-group">
                  <label>Número de Asignados</label>
                  <input type="number" id="assigneesCount" placeholder="Ej: 3" min="0" value="1" />
                </div>

                <div class="form-group">
                  <label>Dependencias</label>
                  <input type="number" id="dependencies" placeholder="Ej: 2" min="0" value="0" />
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

export function initRiskClassification() {
  initAIAssistant();

  const form = document.getElementById('riskForm') as HTMLFormElement;
  const resultCard = document.getElementById('riskResult');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const taskName = (document.getElementById('taskName') as HTMLInputElement)?.value;
      const taskArea = (document.getElementById('taskArea') as HTMLSelectElement)?.value;
      const taskComplexity = (document.getElementById('taskComplexity') as HTMLSelectElement)?.value;
      const taskPriority = (document.getElementById('taskPriority') as HTMLSelectElement)?.value;
      const taskType = (document.getElementById('taskType') as HTMLSelectElement)?.value;
      const estimatedTime = (document.getElementById('estimatedTime') as HTMLInputElement)?.value;
      const assigneesCount = (document.getElementById('assigneesCount') as HTMLInputElement)?.value;
      const dependencies = (document.getElementById('dependencies') as HTMLInputElement)?.value;

      if (!taskArea || !taskComplexity || !taskPriority || !taskType || !estimatedTime) {
        alert('Por favor complete todos los campos requeridos');
        return;
      }

      try {
        const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculando...';

        const response = await fetch('http://127.0.0.1:5000/api/ml/prediccion-riesgo', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            area: taskArea,
            complexity_level: taskComplexity,
            priority: taskPriority,
            task_type: taskType,
            duration_est: parseInt(estimatedTime),
            assignees_count: parseInt(assigneesCount) || 1,
            dependencies: parseInt(dependencies) || 0
          })
        });

        if (!response.ok) {
          throw new Error('Error al calcular riesgo');
        }

        const data = await response.json();
        
        console.log('Respuesta del modelo:', data); // Debug
        
        // MODELO BINARIO: Solo 2 clases (BAJO_RIESGO y ALTO_RIESGO)
        const probabilities = data.probabilities || {};
        
        const probBajo = probabilities['BAJO_RIESGO'] || 0;
        const probAlto = probabilities['ALTO_RIESGO'] || 0;
        
        // Mapear risk_level del backend a formato del frontend
        const riskLevelMap: any = {
          'bajo_riesgo': 'low',
          'alto_riesgo': 'high'
        };
        
        const riskLevel = data.risk_level?.toLowerCase() || 'bajo_riesgo';
        const riskClass = riskLevelMap[riskLevel] || 'low';
        
        // La confianza es la probabilidad de la clase predicha
        const riskProbability = riskLevel.includes('alto') ? probAlto : probBajo;
        
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
            <div class="risk-level risk-${riskClass}">
              RIESGO ${data.risk_level?.toUpperCase() || 'MEDIO'}
            </div>
            <div class="risk-probability">Confianza: ${(riskProbability * 100).toFixed(1)}%</div>
          </div>

          <div class="risk-distribution">
            <div class="risk-bar-item">
              <span class="risk-bar-label">${(probBajo * 100).toFixed(1)}%</span>
              <div class="risk-bar">
                <div class="risk-bar-fill risk-low" style="width: ${(probBajo * 100).toFixed(0)}%"></div>
              </div>
              <span class="risk-badge-small risk-low">Bajo Riesgo</span>
            </div>
            <div class="risk-bar-item">
              <span class="risk-bar-label">${(probAlto * 100).toFixed(1)}%</span>
              <div class="risk-bar">
                <div class="risk-bar-fill risk-high" style="width: ${(probAlto * 100).toFixed(0)}%"></div>
              </div>
              <span class="risk-badge-small risk-high">Alto Riesgo</span>
            </div>
          </div>
            </div>
            <div class="risk-bar-item">
              <span class="risk-bar-label">${(probAlto * 100).toFixed(1)}%</span>
              <div class="risk-bar">
                <div class="risk-bar-fill risk-high" style="width: ${(probAlto * 100).toFixed(0)}%"></div>
              </div>
              <span class="risk-badge-small risk-high">Alto Riesgo</span>
            </div>
          </div>

          <div class="shap-section">
            <h4>Factores de Riesgo Identificados</h4>
            <p class="shap-subtitle">Razones por las que el modelo asignó este nivel de riesgo</p>
            
            ${(data.risk_factors || []).map((factor: string) => `
              <div class="shap-item">
                <div class="shap-label">
                  <span>${factor}</span>
                </div>
              </div>
            `).join('')}
            </div>

          </div>

          <div class="interpretation-section">
            <h4>⭐ Interpretación Automática</h4>
            
            ${(data.recommendations || []).map((rec: string, idx: number) => {
              const colors = ['#4caf50', '#ff9800', '#f44336'];
              const icons = ['✓', '⚠', '✗'];
              const color = colors[Math.min(idx, 2)];
              const icon = icons[Math.min(idx, 2)];
              
              return `
                <div class="interpretation-item" style="border-left-color: ${color}">
                  <span style="color: ${color}">${icon}</span>
                  <p>${rec}</p>
                </div>
              `;
            }).join('')}
          </div>
        `;
        }

        submitBtn.disabled = false;
        submitBtn.textContent = 'Calcular Riesgo';
        
      } catch (error: any) {
        console.error('Error:', error);
        alert('Error: ' + error.message);
        
        const submitBtn = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Calcular Riesgo';
        }
      }
    });
  }
}
