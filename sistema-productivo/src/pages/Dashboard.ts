import { Sidebar, initSidebar } from '../components/Sidebar';
import { MetricCard } from '../components/MetricCard';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function DashboardPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('dashboard')}
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
          <!-- Métricas principales -->
          <div class="metrics-grid">
            ${MetricCard({
              title: 'Tasa de Completación',
              value: '<span id="completionRate">--%</span>',
              change: '<span id="completionChange">--</span>',
              subtitle: 'tareas completadas',
              icon: 'efficiency',
              changeType: 'positive'
            })}
            ${MetricCard({
              title: 'Total de Tareas',
              value: '<span id="totalTasks">--</span>',
              change: '<span id="activeChange">-- activas</span>',
              subtitle: 'en el sistema',
              icon: 'time',
              changeType: 'positive'
            })}
            ${MetricCard({
              title: 'Tareas Retrasadas',
              value: '<span id="delayedTasks">--</span>',
              change: '<span id="delayedChange">--</span>',
              subtitle: 'requieren atención',
              icon: 'warning',
              changeType: 'negative'
            })}
            ${MetricCard({
              title: 'En Progreso',
              value: '<span id="inProgressTasks">--</span>',
              change: '<span id="progressChange">--</span>',
              subtitle: 'tareas activas',
              icon: 'prediction',
              changeType: 'positive'
            })}
          </div>

          <!-- Gráficos -->
          <div class="charts-grid">
            <!-- Productividad por Área -->
            <div class="chart-card">
              <div class="chart-header">
                <h3>Tareas por Área</h3>
                <p class="chart-subtitle">Distribución de tareas por área</p>
              </div>
              <div class="chart-content">
                <div class="bar-chart" id="areaChart">
                  <p style="text-align: center; padding: 40px;">Cargando datos...</p>
                </div>
              </div>
            </div>

            <!-- Estado de Tareas -->
            <div class="chart-card">
              <div class="chart-header">
                <h3>Estado de Tareas</h3>
                <p class="chart-subtitle">Distribución actual</p>
              </div>
              <div class="chart-content">
                <div class="donut-chart" id="statusDonutContainer">
                  <svg width="200" height="200" viewBox="0 0 200 200" id="statusDonut">
                    <!-- Se generará dinámicamente -->
                  </svg>
                  <div class="donut-center">
                    <div class="donut-total" id="donutTotal">--</div>
                  </div>
                </div>
                <div class="donut-legend" id="statusLegend">
                  <div class="legend-item">
                    <span class="legend-color" style="background: #28a745"></span>
                    <span class="legend-label">Completadas: <span id="completedCount">--</span></span>
                  </div>
                  <div class="legend-item">
                    <span class="legend-color" style="background: #007bff"></span>
                    <span class="legend-label">En Progreso: <span id="inProgressCount">--</span></span>
                  </div>
                  <div class="legend-item">
                    <span class="legend-color" style="background: #ffc107"></span>
                    <span class="legend-label">Pendientes: <span id="pendingCount">--</span></span>
                  </div>
                  <div class="legend-item">
                    <span class="legend-color" style="background: #dc3545"></span>
                    <span class="legend-label">Retrasadas: <span id="delayedCount">--</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tendencia e Insights -->
          <div class="charts-grid-2">
            <!-- Tendencia de Eficiencia -->
            <div class="chart-card">
              <div class="chart-header">
                <h3>Tendencia de Eficiencia</h3>
                <p class="chart-subtitle">Evolución últimos 6 meses</p>
              </div>
              <div class="chart-content">
                <svg class="line-chart" width="100%" height="200" viewBox="0 0 600 200">
                  <polyline points="50,150 150,130 250,120 350,125 450,115 550,110" fill="none" stroke="#00bcd4" stroke-width="3"/>
                  <circle cx="50" cy="150" r="4" fill="#00bcd4"/>
                  <circle cx="150" cy="130" r="4" fill="#00bcd4"/>
                  <circle cx="250" cy="120" r="4" fill="#00bcd4"/>
                  <circle cx="350" cy="125" r="4" fill="#00bcd4"/>
                  <circle cx="450" cy="115" r="4" fill="#00bcd4"/>
                  <circle cx="550" cy="110" r="4" fill="#00bcd4"/>
                  <text x="50" y="185" text-anchor="middle" font-size="12" fill="#6c757d">Ene</text>
                  <text x="150" y="185" text-anchor="middle" font-size="12" fill="#6c757d">Feb</text>
                  <text x="250" y="185" text-anchor="middle" font-size="12" fill="#6c757d">Mar</text>
                  <text x="350" y="185" text-anchor="middle" font-size="12" fill="#6c757d">Abr</text>
                  <text x="450" y="185" text-anchor="middle" font-size="12" fill="#6c757d">May</text>
                  <text x="550" y="185" text-anchor="middle" font-size="12" fill="#6c757d">Jun</text>
                </svg>
              </div>
            </div>

            <!-- Insights de IA -->
            <div class="chart-card insights-card">
              <div class="chart-header">
                <h3>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="#00bcd4"/>
                  </svg>
                  Insights de IA
                </h3>
                <p class="chart-subtitle">Predicciones y recomendaciones automáticas</p>
              </div>
              <div class="insights-list">
                <div class="insight-item warning">
                  <div class="insight-icon"></div>
                  <div class="insight-content">
                    <div class="insight-title">Predicción de Riesgo</div>
                    <div class="insight-text">3 tareas con alto riesgo de retraso detectadas</div>
                  </div>
                </div>
                <div class="insight-item success">
                  <div class="insight-icon"></div>
                  <div class="insight-content">
                    <div class="insight-title">Oportunidad de Mejora</div>
                    <div class="insight-text">Reasignar tareas en Operaciones podría aumentar 15% la eficiencia</div>
                  </div>
                </div>
                <div class="insight-item danger">
                  <div class="insight-icon"></div>
                  <div class="insight-content">
                    <div class="insight-title">Cuello de Botella</div>
                    <div class="insight-text">Proceso de aprobación identificado como punto crítico</div>
                  </div>
                </div>
                <div class="insight-item info">
                  <div class="insight-icon"></div>
                  <div class="insight-content">
                    <div class="insight-title">Recomendación Activa</div>
                    <div class="insight-text">Luis García ideal para 5 tareas prioritarias</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tareas Críticas -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>Tareas Recientes</h3>
              <p class="chart-subtitle">Últimas tareas del sistema</p>
            </div>
            <div class="tasks-list" id="recentTasksList">
              <p style="text-align: center; padding: 40px;">Cargando tareas...</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

export async function initDashboard() {
  initSidebar();
  initAIAssistant();
  
  // Cargar estadísticas del backend
  await loadDashboardData();
}

async function loadDashboardData() {
  try {
    const { api } = await import('../utils/api');
    
    // Obtener estadísticas
    const stats = await api.getTaskStats();
    console.log('📊 Estadísticas cargadas:', stats);
    
    // Actualizar métricas principales
    const completionRateEl = document.getElementById('completionRate');
    const totalTasksEl = document.getElementById('totalTasks');
    const delayedTasksEl = document.getElementById('delayedTasks');
    const inProgressTasksEl = document.getElementById('inProgressTasks');
    const activeChangeEl = document.getElementById('activeChange');
    const delayedChangeEl = document.getElementById('delayedChange');
    const progressChangeEl = document.getElementById('progressChange');
    
    if (completionRateEl) completionRateEl.textContent = `${stats.completion_rate}%`;
    if (totalTasksEl) totalTasksEl.textContent = stats.total_tasks.toString();
    if (delayedTasksEl) delayedTasksEl.textContent = stats.delayed.toString();
    if (inProgressTasksEl) inProgressTasksEl.textContent = stats.in_progress.toString();
    if (activeChangeEl) activeChangeEl.textContent = `${stats.in_progress + stats.pending} activas`;
    if (delayedChangeEl) delayedChangeEl.textContent = stats.delayed > 0 ? 'Atención requerida' : 'Todo al día';
    if (progressChangeEl) progressChangeEl.textContent = `${stats.pending} pendientes`;
    
    // Actualizar contadores en leyenda del donut
    const completedCountEl = document.getElementById('completedCount');
    const inProgressCountEl = document.getElementById('inProgressCount');
    const pendingCountEl = document.getElementById('pendingCount');
    const delayedCountEl = document.getElementById('delayedCount');
    const donutTotalEl = document.getElementById('donutTotal');
    
    if (completedCountEl) completedCountEl.textContent = stats.completed.toString();
    if (inProgressCountEl) inProgressCountEl.textContent = stats.in_progress.toString();
    if (pendingCountEl) pendingCountEl.textContent = stats.pending.toString();
    if (delayedCountEl) delayedCountEl.textContent = stats.delayed.toString();
    if (donutTotalEl) donutTotalEl.textContent = `${stats.total_tasks}`;
    
    // Generar gráfico de dona
    generateDonutChart(stats);
    
    // Renderizar gráfico de áreas
    renderAreaChart(stats.tasks_by_area || []);
    
    // Obtener y mostrar tareas recientes
    const tasksResponse = await api.getTasks({ per_page: 5 });
    renderRecentTasks(tasksResponse.tasks || []);
    
  } catch (error) {
    console.error('Error al cargar datos del dashboard:', error);
  }
}

function generateDonutChart(stats: any) {
  const svg = document.getElementById('statusDonut');
  if (!svg) return;
  
  const total = stats.total_tasks;
  if (total === 0) {
    svg.innerHTML = '<text x="100" y="100" text-anchor="middle" font-size="14" fill="#6c757d">Sin datos</text>';
    return;
  }
  
  const circumference = 2 * Math.PI * 60; // radio = 60
  const completed = stats.completed;
  const inProgress = stats.in_progress;
  const pending = stats.pending;
  const delayed = stats.delayed;
  
  const completedDash = (completed / total) * circumference;
  const inProgressDash = (inProgress / total) * circumference;
  const pendingDash = (pending / total) * circumference;
  const delayedDash = (delayed / total) * circumference;
  
  let offset = 0;
  
  svg.innerHTML = `
    ${completed > 0 ? `<circle cx="100" cy="100" r="60" fill="none" stroke="#28a745" stroke-width="40" 
      stroke-dasharray="${completedDash} ${circumference}" 
      stroke-dashoffset="${offset}" 
      transform="rotate(-90 100 100)"/>` : ''}
    ${inProgress > 0 ? `<circle cx="100" cy="100" r="60" fill="none" stroke="#007bff" stroke-width="40" 
      stroke-dasharray="${inProgressDash} ${circumference}" 
      stroke-dashoffset="${offset -= completedDash}" 
      transform="rotate(-90 100 100)"/>` : ''}
    ${pending > 0 ? `<circle cx="100" cy="100" r="60" fill="none" stroke="#ffc107" stroke-width="40" 
      stroke-dasharray="${pendingDash} ${circumference}" 
      stroke-dashoffset="${offset -= inProgressDash}" 
      transform="rotate(-90 100 100)"/>` : ''}
    ${delayed > 0 ? `<circle cx="100" cy="100" r="60" fill="none" stroke="#dc3545" stroke-width="40" 
      stroke-dasharray="${delayedDash} ${circumference}" 
      stroke-dashoffset="${offset -= pendingDash}" 
      transform="rotate(-90 100 100)"/>` : ''}
  `;
}

function renderAreaChart(areas: any[]) {
  const container = document.getElementById('areaChart');
  if (!container) return;
  
  if (areas.length === 0) {
    container.innerHTML = '<p style="text-align: center; padding: 40px;">No hay datos por área</p>';
    return;
  }
  
  // Encontrar el máximo para calcular porcentajes
  const maxCount = Math.max(...areas.map(a => a.count));
  
  container.innerHTML = areas.map(area => {
    const percentage = maxCount > 0 ? (area.count / maxCount * 100) : 0;
    return `
      <div class="bar-item">
        <div class="bar-label">${area.area}</div>
        <div class="bar-container">
          <div class="bar-fill" style="--target-width: ${percentage}%"></div>
        </div>
        <div class="bar-value">${area.count}</div>
      </div>
    `;
  }).join('');
}

function renderRecentTasks(tasks: any[]) {
  const container = document.getElementById('recentTasksList');
  if (!container) return;
  
  if (tasks.length === 0) {
    container.innerHTML = '<p style="text-align: center; padding: 40px;">No hay tareas registradas</p>';
    return;
  }
  
  const getPriorityClass = (priority: string) => {
    const map: any = { 'alta': 'high', 'media': 'medium', 'baja': 'low' };
    return map[priority] || 'low';
  };
  
  const getPriorityText = (priority: string) => {
    const map: any = { 'alta': 'Alto', 'media': 'Medio', 'baja': 'Bajo' };
    return map[priority] || priority;
  };
  
  const getProgress = (status: string) => {
    const map: any = {
      'pendiente': 0,
      'en_progreso': 50,
      'completada': 100,
      'retrasada': 30
    };
    return map[status] || 0;
  };
  
  container.innerHTML = tasks.map(task => {
    const progress = getProgress(task.status);
    return `
      <div class="task-item">
        <div class="task-info">
          <div class="task-id">T-${String(task.id).padStart(3, '0')}</div>
          <div class="task-title">${task.title}</div>
          <div class="task-area">${task.area || 'Sin área'}</div>
          <div class="task-priority ${getPriorityClass(task.priority)}">${getPriorityText(task.priority)}</div>
        </div>
        <div class="task-progress">
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${progress}%"></div>
          </div>
          <div class="progress-value">${progress}%</div>
        </div>
      </div>
    `;
  }).join('');
}
