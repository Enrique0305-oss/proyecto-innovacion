import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { API_URL } from '../utils/api';

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
              <p class="module-description">Modelo 5: Process Mining con IA - Análisis predictivo de cadenas críticas</p>
            </div>
          </div>

          <!-- Filtros y controles -->
          <div class="control-panel">
            <div class="control-row">
              <div class="form-group">
                <label>Proyecto</label>
                <select id="projectFilter">
                  <option value="">Todos los proyectos</option>
                </select>
              </div>
              <div class="control-buttons">
                <button class="btn-execute" id="loadAnalysisBtn">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M5 3l12 7-12 7V3z" fill="currentColor"/>
                  </svg>
                  Cargar Análisis
                </button>
                <button class="btn-export" id="exportBtn">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 3v10M7 10l3 3 3-3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M4 14v2a2 2 0 002 2h8a2 2 0 002-2v-2" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  Exportar CSV
                </button>
              </div>
            </div>
          </div>

          <!-- Tabs -->
          <div class="simulation-tabs">
            <button class="tab-btn active" data-tab="summary">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <rect x="2" y="2" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
                <rect x="10" y="2" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
                <rect x="2" y="10" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
                <rect x="10" y="10" width="6" height="6" rx="1" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              Resumen
            </button>
            <button class="tab-btn" data-tab="critical">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 2l2 5h5l-4 3.5 1.5 5.5-4.5-3.5-4.5 3.5 1.5-5.5-4-3.5h5l2-5z" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              Cadena Crítica
            </button>
            <button class="tab-btn" data-tab="domino">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <circle cx="4" cy="9" r="2.5" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="9" cy="9" r="2.5" stroke="currentColor" stroke-width="1.5"/>
                <circle cx="14" cy="9" r="2.5" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              Efecto Dominó
            </button>
            <button class="tab-btn" data-tab="whatif">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 2v14M2 9h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              Optimización What-If
            </button>
            <button class="tab-btn" data-tab="mining">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M2 16h14M4 12h10M6 8h6M8 4h2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              Process Mining
            </button>
          </div>

          <!-- Tab Content -->
          
          <!-- TAB 1: RESUMEN -->
          <div class="tab-content active" id="summaryTab">
            <div class="summary-grid">
              <div class="metric-card">
                <div class="metric-icon" style="background: rgba(0, 114, 198, 0.1);">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M9 11l3 3L22 4" stroke="#0072c6" stroke-width="2" stroke-linecap="round"/>
                    <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" stroke="#0072c6" stroke-width="2"/>
                  </svg>
                </div>
                <div class="metric-content">
                  <h4>Total Eventos</h4>
                  <p class="metric-value" id="totalEvents">-</p>
                  <span class="metric-label">Tareas procesadas</span>
                </div>
              </div>

              <div class="metric-card">
                <div class="metric-icon" style="background: rgba(40, 167, 69, 0.1);">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 11a4 4 0 100-8 4 4 0 000 8z" stroke="#28a745" stroke-width="2"/>
                  </svg>
                </div>
                <div class="metric-content">
                  <h4>Proyectos</h4>
                  <p class="metric-value" id="totalCases">-</p>
                  <span class="metric-label">Casos analizados</span>
                </div>
              </div>

              <div class="metric-card">
                <div class="metric-icon" style="background: rgba(255, 193, 7, 0.1);">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="#ffc107" stroke-width="2"/>
                    <path d="M12 6v6l4 2" stroke="#ffc107" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </div>
                <div class="metric-content">
                  <h4>Throughput Promedio</h4>
                  <p class="metric-value" id="avgThroughput">-</p>
                  <span class="metric-label">Días por proyecto</span>
                </div>
              </div>

              <div class="metric-card">
                <div class="metric-icon" style="background: rgba(220, 53, 69, 0.1);">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M12 9v4M12 17h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="#dc3545" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </div>
                <div class="metric-content">
                  <h4>Accuracy Predictor</h4>
                  <p class="metric-value" id="modelAccuracy">88%</p>
                  <span class="metric-label">Modelo cadena crítica</span>
                </div>
              </div>
            </div>

            <div class="models-info">
              <h3>Modelos de IA Cargados</h3>
              <div class="models-grid">
                <div class="model-status">
                  <span class="status-indicator loaded"></span>
                  <div>
                    <strong>Predictor de Cadenas Críticas</strong>
                    <p>RandomForestClassifier - Accuracy: 88%</p>
                  </div>
                </div>
                <div class="model-status">
                  <span class="status-indicator loaded"></span>
                  <div>
                    <strong>Simulador de Efecto Dominó</strong>
                    <p>RandomForestRegressor - MAE: 2.3 tareas</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 2: CADENA CRÍTICA -->
          <div class="tab-content" id="criticalTab">
            <div class="section-header">
              <h3>🔗 Predictor de Cadenas Críticas</h3>
              <p class="section-subtitle">Identifica tareas "single point of failure" con alta centralidad</p>
            </div>

            <div class="metrics-row">
              <div class="metric-small">
                <span class="label">Accuracy</span>
                <span class="value" id="criticalAccuracy">88%</span>
              </div>
              <div class="metric-small">
                <span class="label">Precision</span>
                <span class="value" id="criticalPrecision">82%</span>
              </div>
              <div class="metric-small">
                <span class="label">Tareas Críticas</span>
                <span class="value critical" id="criticalCount">0</span>
              </div>
              <div class="metric-small">
                <span class="label">Analizadas</span>
                <span class="value" id="totalAnalyzed">0</span>
              </div>
            </div>

            <div class="visualization-section">
              <h4>Grafo de Dependencias</h4>
              <div class="graph-container" id="criticalGraph">
                <p class="placeholder-text">Cargue un análisis para ver el grafo de dependencias</p>
              </div>
            </div>

            <div class="table-section">
              <h4>Top Tareas Críticas</h4>
              <div class="table-responsive">
                <table class="data-table" id="criticalTasksTable">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Actividad</th>
                      <th>Probabilidad Crítica</th>
                      <th>Betweenness</th>
                      <th>Delay Ratio</th>
                      <th>In/Out Degree</th>
                      <th>Riesgo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colspan="7" class="no-data">No hay datos disponibles</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- TAB 3: EFECTO DOMINÓ -->
          <div class="tab-content" id="dominoTab">
            <div class="section-header">
              <h3>📊 Simulador de Efecto Dominó</h3>
              <p class="section-subtitle">Predice impacto en cadena si una tarea se retrasa</p>
            </div>

            <div class="metrics-row">
              <div class="metric-small">
                <span class="label">MAE</span>
                <span class="value" id="dominoMAE">2.3</span>
              </div>
              <div class="metric-small">
                <span class="label">R²</span>
                <span class="value" id="dominoR2">0.68</span>
              </div>
              <div class="metric-small">
                <span class="label">Impacto Promedio</span>
                <span class="value" id="avgImpact">-</span>
              </div>
              <div class="metric-small">
                <span class="label">Impacto Máximo</span>
                <span class="value critical" id="maxImpact">-</span>
              </div>
            </div>

            <div class="heatmap-section">
              <h4>Mapa de Calor de Impacto</h4>
              <div id="dominoHeatmap" class="heatmap-container">
                <p class="placeholder-text">Cargue un análisis para ver el mapa de calor</p>
              </div>
            </div>

            <div class="table-section">
              <h4>Top Tareas con Mayor Impacto</h4>
              <div class="table-responsive">
                <table class="data-table" id="dominoTasksTable">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Actividad</th>
                      <th>Impacto Predicho</th>
                      <th>Delay Ratio</th>
                      <th>Betweenness</th>
                      <th>Nivel</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colspan="6" class="no-data">No hay datos disponibles</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- TAB 4: WHAT-IF -->
          <div class="tab-content" id="whatifTab">
            <div class="section-header">
              <h3>🎲 Optimización What-If (Monte Carlo)</h3>
              <p class="section-subtitle">Simulación de 100 escenarios alternativos</p>
            </div>

            <div class="whatif-baseline">
              <div class="baseline-card">
                <h4>Escenario Base</h4>
                <p class="baseline-value" id="baselineThroughput">-</p>
                <span class="baseline-label">Días de throughput</span>
              </div>
              <div class="baseline-card highlight">
                <h4>Mejor Mejora</h4>
                <p class="baseline-value success" id="bestImprovement">-</p>
                <span class="baseline-label">% de optimización</span>
              </div>
            </div>

            <div class="table-section">
              <h4>Top 10 Escenarios Optimizados</h4>
              <div class="table-responsive">
                <table class="data-table" id="scenariosTable">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Resource Boost</th>
                      <th>Throughput Simulado</th>
                      <th>Mejora %</th>
                      <th>Acción</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colspan="5" class="no-data">No hay datos disponibles</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- TAB 5: PROCESS MINING -->
          <div class="tab-content" id="miningTab">
            <div class="section-header">
              <h3>📈 Process Mining Tradicional (PM4Py)</h3>
              <p class="section-subtitle">Análisis de flujos reales de ejecución</p>
            </div>

            <div class="process-flow-section" id="processMapContainer">
              <h4>Mapa de Proceso BPMN</h4>
              <div class="process-steps-grid">
                <p class="placeholder-text">Cargue un análisis para ver el mapa de proceso</p>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  `;
}

export function initProcessSimulation() {
  initAIAssistant();

  let currentProject: string | null = null;

  // Cargar proyectos
  loadProjects();

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

  // Cambio de proyecto
  const projectFilter = document.getElementById('projectFilter') as HTMLSelectElement;
  if (projectFilter) {
    projectFilter.addEventListener('change', () => {
      currentProject = projectFilter.value || null;
    });
  }

  // Cargar análisis
  const loadBtn = document.getElementById('loadAnalysisBtn');
  if (loadBtn) {
    loadBtn.addEventListener('click', loadAllAnalysis);
  }

  // Exportar
  const exportBtn = document.getElementById('exportBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', showExportMenu);
  }

  // FUNCIONES
  async function loadProjects() {
    try {
      const token = localStorage.getItem('token');
      console.log('Cargando proyectos desde:', `${API_URL}/projects`);
      
      const response = await fetch(`${API_URL}/projects`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('Respuesta de proyectos:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('Datos recibidos:', data);
        
        // El endpoint devuelve { status: 'success', projects: [...] }
        const projects = data.projects || data;
        
        const select = document.getElementById('projectFilter') as HTMLSelectElement;
        
        if (select) {
          select.innerHTML = '<option value="">Todos los proyectos</option>';
          
          if (Array.isArray(projects) && projects.length > 0) {
            projects.forEach((p: any) => {
              const option = document.createElement('option');
              option.value = p.project_id || p.id;
              option.textContent = p.name || p.title || p.project_id;
              select.appendChild(option);
            });
            console.log(`✅ ${projects.length} proyectos cargados en el dropdown`);
          } else {
            console.warn('No se encontraron proyectos');
          }
        }
      } else {
        const errorText = await response.text();
        console.error('Error al cargar proyectos:', response.status, errorText);
      }
    } catch (error) {
      console.error('Error cargando proyectos:', error);
    }
  }

  async function loadAllAnalysis() {
    const loadBtn = document.getElementById('loadAnalysisBtn') as HTMLButtonElement;
    if (loadBtn) {
      loadBtn.disabled = true;
      loadBtn.textContent = 'Cargando...';
    }

    try {
      await Promise.all([
        loadSummary(),
        loadCriticalChain(),
        loadDominoEffect(),
        loadWhatIf()
      ]);

      alert('Análisis cargado correctamente');
    } catch (error) {
      console.error('Error cargando análisis:', error);
      alert('Error al cargar análisis');
    } finally {
      if (loadBtn) {
        loadBtn.disabled = false;
        loadBtn.textContent = 'Cargar Análisis';
      }
    }
  }

  async function loadSummary() {
    const token = localStorage.getItem('token');
    const url = currentProject 
      ? `${API_URL}/ml/process-mining/summary/${currentProject}`
      : `${API_URL}/ml/process-mining/summary`;

    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
      const data = await response.json();
      renderSummary(data);
    }
  }

  async function loadCriticalChain() {
    const token = localStorage.getItem('token');
    const url = currentProject
      ? `${API_URL}/ml/process-mining/critical-chain/${currentProject}`
      : `${API_URL}/ml/process-mining/critical-chain`;

    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
      const data = await response.json();
      renderCriticalChain(data);
    }
  }

  async function loadDominoEffect() {
    const token = localStorage.getItem('token');
    const url = currentProject
      ? `${API_URL}/ml/process-mining/domino-effect/${currentProject}`
      : `${API_URL}/ml/process-mining/domino-effect`;

    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
      const data = await response.json();
      renderDominoEffect(data);
    }
  }

  async function loadWhatIf() {
    const token = localStorage.getItem('token');
    const url = currentProject
      ? `${API_URL}/ml/process-mining/what-if/${currentProject}`
      : `${API_URL}/ml/process-mining/what-if`;

    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
      const data = await response.json();
      renderWhatIf(data);
    }
  }

  function renderSummary(data: any) {
    const stats = data.statistics || {};
    
    document.getElementById('totalEvents')!.textContent = 
      (stats.total_events || 0).toLocaleString();
    document.getElementById('totalCases')!.textContent = 
      (stats.total_cases || 0).toLocaleString();
    document.getElementById('avgThroughput')!.textContent = 
      `${(stats.avg_throughput_days || 0).toFixed(0)} días`;
    
    const models = data.ai_models || {};
    const criticalModel = models.critical_chain_predictor || {};
    
    document.getElementById('modelAccuracy')!.textContent = 
      `${((criticalModel.accuracy || 0.88) * 100).toFixed(0)}%`;
  }

  function renderCriticalChain(data: any) {
    const metrics = data.metrics || {};
    
    document.getElementById('criticalAccuracy')!.textContent = 
      `${(metrics.accuracy * 100).toFixed(0)}%`;
    document.getElementById('criticalPrecision')!.textContent = 
      `${(metrics.precision * 100).toFixed(0)}%`;
    document.getElementById('criticalCount')!.textContent = 
      metrics.critical_count || 0;
    document.getElementById('totalAnalyzed')!.textContent = 
      metrics.total_analyzed || 0;

    // Tabla
    const tbody = document.querySelector('#criticalTasksTable tbody');
    if (tbody && data.tasks && data.tasks.length > 0) {
      tbody.innerHTML = data.tasks.map((task: any) => `
        <tr>
          <td>${task.task_id}</td>
          <td title="${task.activity}">${task.activity.substring(0, 40)}...</td>
          <td>
            <span class="probability-badge ${task.critical_probability > 0.7 ? 'high' : task.critical_probability > 0.4 ? 'medium' : 'low'}">
              ${(task.critical_probability * 100).toFixed(1)}%
            </span>
          </td>
          <td>${task.betweenness.toFixed(3)}</td>
          <td>${task.delay_ratio.toFixed(2)}</td>
          <td>${task.in_degree}/${task.out_degree}</td>
          <td><span class="risk-badge ${task.risk_level.toLowerCase()}">${task.risk_level}</span></td>
        </tr>
      `).join('');
    }

    // Grafo
    const graphContainer = document.getElementById('criticalGraph');
    if (graphContainer && data.graph) {
      graphContainer.innerHTML = `
        <div class="graph-info">
          <p><strong>Nodos:</strong> ${data.graph.nodes.length}</p>
          <p><strong>Conexiones:</strong> ${data.graph.edges.length}</p>
          <p class="info-text">Grafo construido desde web_task_dependencies</p>
        </div>
      `;
    }
  }

  function renderDominoEffect(data: any) {
    const metrics = data.metrics || {};
    
    document.getElementById('dominoMAE')!.textContent = 
      (metrics.mae || 2.3).toFixed(1);
    document.getElementById('dominoR2')!.textContent = 
      (metrics.r2 || 0.68).toFixed(2);
    document.getElementById('avgImpact')!.textContent = 
      `${(metrics.avg_impact || 0).toFixed(1)} tareas`;
    document.getElementById('maxImpact')!.textContent = 
      `${(metrics.max_impact || 0).toFixed(0)} tareas`;

    // Tabla
    const tbody = document.querySelector('#dominoTasksTable tbody');
    if (tbody && data.tasks && data.tasks.length > 0) {
      tbody.innerHTML = data.tasks.map((task: any) => `
        <tr>
          <td>${task.task_id}</td>
          <td title="${task.activity}">${task.activity.substring(0, 40)}...</td>
          <td><strong>${task.predicted_impact.toFixed(1)}</strong> tareas</td>
          <td>${task.delay_ratio.toFixed(2)}</td>
          <td>${task.betweenness.toFixed(3)}</td>
          <td><span class="impact-badge ${task.impact_level.toLowerCase()}">${task.impact_level}</span></td>
        </tr>
      `).join('');
    }

    // Heatmap
    const heatmapContainer = document.getElementById('dominoHeatmap');
    if (heatmapContainer && data.heatmap) {
      heatmapContainer.innerHTML = data.heatmap.map((item: any) => `
        <div class="heatmap-row">
          <div class="heatmap-label">${item.activity}</div>
          <div class="heatmap-bar">
            <div class="heatmap-fill" style="width: ${Math.min(item.impact_score * 5, 100)}%; background: ${item.color}"></div>
          </div>
          <div class="heatmap-value">${item.impact_score.toFixed(1)}</div>
        </div>
      `).join('');
    }
  }

  function renderWhatIf(data: any) {
    const baseline = data.baseline || {};
    
    document.getElementById('baselineThroughput')!.textContent = 
      `${(baseline.throughput_days || 0).toFixed(0)} días`;
    document.getElementById('bestImprovement')!.textContent = 
      `${(baseline.best_improvement || 0).toFixed(1)}%`;

    // Tabla
    const tbody = document.querySelector('#scenariosTable tbody');
    if (tbody && data.scenarios && data.scenarios.length > 0) {
      tbody.innerHTML = data.scenarios.map((scenario: any, index: number) => `
        <tr>
          <td>${index + 1}</td>
          <td>${(scenario.resource_boost * 100).toFixed(1)}%</td>
          <td>${scenario.simulated_throughput.toFixed(1)} días</td>
          <td><span class="${scenario.improvement_pct > 0 ? 'success' : ''}">${scenario.improvement_pct.toFixed(2)}%</span></td>
          <td><button class="btn-view-scenario">Ver</button></td>
        </tr>
      `).join('');
    }
  }

  function showExportMenu() {
    const confirmed = confirm('¿Desea exportar los datos de análisis en formato CSV?');
    if (confirmed) {
      window.open(`${API_URL}/ml/process-mining/export/task_risk`, '_blank');
    }
  }
}
