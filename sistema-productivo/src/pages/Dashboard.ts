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
              title: 'Eficiencia General',
              value: '85%',
              change: '+5.2%',
              subtitle: 'vs. mes anterior',
              icon: 'efficiency',
              changeType: 'positive'
            })}
            ${MetricCard({
              title: 'Tiempo Promedio',
              value: '4.2 días',
              change: '-12%',
              subtitle: 'vs. mes anterior',
              icon: 'time',
              changeType: 'positive'
            })}
            ${MetricCard({
              title: 'Cuellos de Botella',
              value: '3 Detectados',
              change: '+1',
              subtitle: 'requieren atención',
              icon: 'warning',
              changeType: 'negative'
            })}
            ${MetricCard({
              title: 'Predicciones Activas',
              value: '24 Modelos',
              change: '95% precisión',
              subtitle: 'en ejecución',
              icon: 'prediction',
              changeType: 'positive'
            })}
          </div>

          <!-- Gráficos -->
          <div class="charts-grid">
            <!-- Productividad por Área -->
            <div class="chart-card">
              <div class="chart-header">
                <h3>Productividad por Área</h3>
                <p class="chart-subtitle">Puntaje de eficiencia por departamento</p>
              </div>
              <div class="chart-content">
                <div class="bar-chart">
                  <div class="bar-item">
                    <div class="bar-label">Ventas</div>
                    <div class="bar-container">
                      <div class="bar-fill" style="--target-width: 88%"></div>
                    </div>
                    <div class="bar-value">88</div>
                  </div>
                  <div class="bar-item">
                    <div class="bar-label">Operaciones</div>
                    <div class="bar-container">
                      <div class="bar-fill" style="--target-width: 72%"></div>
                    </div>
                    <div class="bar-value">72</div>
                  </div>
                  <div class="bar-item">
                    <div class="bar-label">Soporte</div>
                    <div class="bar-container">
                      <div class="bar-fill" style="--target-width: 78%"></div>
                    </div>
                    <div class="bar-value">78</div>
                  </div>
                  <div class="bar-item">
                    <div class="bar-label">Marketing</div>
                    <div class="bar-container">
                      <div class="bar-fill" style="--target-width: 92%"></div>
                    </div>
                    <div class="bar-value">92</div>
                  </div>
                  <div class="bar-item">
                    <div class="bar-label">TI</div>
                    <div class="bar-container">
                      <div class="bar-fill" style="--target-width: 85%"></div>
                    </div>
                    <div class="bar-value">85</div>
                  </div>
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
                <div class="donut-chart">
                  <svg width="200" height="200" viewBox="0 0 200 200">
                    <circle cx="100" cy="100" r="60" fill="none" stroke="#005a9c" stroke-width="40" stroke-dasharray="283 377" transform="rotate(-90 100 100)"/>
                    <circle cx="100" cy="100" r="60" fill="none" stroke="#00bcd4" stroke-width="40" stroke-dasharray="57 603" stroke-dashoffset="-283" transform="rotate(-90 100 100)"/>
                    <circle cx="100" cy="100" r="60" fill="none" stroke="#ff5252" stroke-width="40" stroke-dasharray="28 632" stroke-dashoffset="-340" transform="rotate(-90 100 100)"/>
                    <circle cx="100" cy="100" r="60" fill="none" stroke="#ffc107" stroke-width="40" stroke-dasharray="9 651" stroke-dashoffset="-368" transform="rotate(-90 100 100)"/>
                  </svg>
                  <div class="donut-center">
                    <div class="donut-total">100%</div>
                  </div>
                </div>
                <div class="donut-legend">
                  <div class="legend-item">
                    <span class="legend-color" style="background: #005a9c"></span>
                    <span class="legend-label">Completadas</span>
                  </div>
                  <div class="legend-item">
                    <span class="legend-color" style="background: #00bcd4"></span>
                    <span class="legend-label">En Progreso</span>
                  </div>
                  <div class="legend-item">
                    <span class="legend-color" style="background: #ff5252"></span>
                    <span class="legend-label">Pendientes</span>
                  </div>
                  <div class="legend-item">
                    <span class="legend-color" style="background: #ffc107"></span>
                    <span class="legend-label">Bloqueadas</span>
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
                  <div class="insight-icon">⚠️</div>
                  <div class="insight-content">
                    <div class="insight-title">Predicción de Riesgo</div>
                    <div class="insight-text">3 tareas con alto riesgo de retraso detectadas</div>
                  </div>
                </div>
                <div class="insight-item success">
                  <div class="insight-icon">📈</div>
                  <div class="insight-content">
                    <div class="insight-title">Oportunidad de Mejora</div>
                    <div class="insight-text">Reasignar tareas en Operaciones podría aumentar 15% la eficiencia</div>
                  </div>
                </div>
                <div class="insight-item danger">
                  <div class="insight-icon">🎯</div>
                  <div class="insight-content">
                    <div class="insight-title">Cuello de Botella</div>
                    <div class="insight-text">Proceso de aprobación identificado como punto crítico</div>
                  </div>
                </div>
                <div class="insight-item info">
                  <div class="insight-icon">✨</div>
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
              <h3>Tareas Críticas en Progreso</h3>
              <p class="chart-subtitle">Requieren seguimiento prioritario</p>
            </div>
            <div class="tasks-list">
              <div class="task-item">
                <div class="task-info">
                  <div class="task-id">T-001</div>
                  <div class="task-title">Implementación CRM</div>
                  <div class="task-area">TI</div>
                  <div class="task-priority high">Bajo</div>
                </div>
                <div class="task-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" style="width: 75%"></div>
                  </div>
                  <div class="progress-value">75%</div>
                </div>
              </div>
              <div class="task-item">
                <div class="task-info">
                  <div class="task-id">T-002</div>
                  <div class="task-title">Campaña Q4</div>
                  <div class="task-area">Marketing</div>
                  <div class="task-priority medium">Medio</div>
                </div>
                <div class="task-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" style="width: 45%"></div>
                  </div>
                  <div class="progress-value">45%</div>
                </div>
              </div>
              <div class="task-item">
                <div class="task-info">
                  <div class="task-id">T-003</div>
                  <div class="task-title">Auditoría Procesos</div>
                  <div class="task-area">Operaciones</div>
                  <div class="task-priority high">Alto</div>
                </div>
                <div class="task-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" style="width: 30%"></div>
                  </div>
                  <div class="progress-value">30%</div>
                </div>
              </div>
              <div class="task-item">
                <div class="task-info">
                  <div class="task-id">T-004</div>
                  <div class="task-title">Capacitación Equipo</div>
                  <div class="task-area">RRHH</div>
                  <div class="task-priority low">Bajo</div>
                </div>
                <div class="task-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" style="width: 90%"></div>
                  </div>
                  <div class="progress-value">90%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

export function initDashboard() {
  initSidebar();
  initAIAssistant();
}
