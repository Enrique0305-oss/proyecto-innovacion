import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function IntelligentVisualizationPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('visualizacion')}
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
          <div class="module-header">
            <div class="module-icon">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <rect x="8" y="8" width="10" height="10" stroke="white" stroke-width="2"/>
                <rect x="22" y="8" width="10" height="10" stroke="white" stroke-width="2"/>
                <rect x="22" y="22" width="10" height="10" stroke="white" stroke-width="2"/>
                <rect x="8" y="22" width="10" height="10" stroke="white" stroke-width="2"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Panel de Visualización Inteligente</h2>
              <p class="module-description">Dashboard avanzado con análisis multidimensional</p>
            </div>
          </div>

          <!-- Métricas Principales -->
          <div class="metrics-grid">
            <div class="metric-card">
              <div class="metric-icon blue">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </div>
              <div class="metric-content">
                <div class="metric-label">Eficiencia Global</div>
                <div class="metric-value">83.4%</div>
                <div class="metric-change positive">+4.2% vs mes anterior</div>
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon cyan">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="7" height="7"/>
                  <rect x="14" y="3" width="7" height="7"/>
                  <rect x="14" y="14" width="7" height="7"/>
                  <rect x="3" y="14" width="7" height="7"/>
                </svg>
              </div>
              <div class="metric-content">
                <div class="metric-label">Tareas Totales</div>
                <div class="metric-value">608</div>
                <div class="metric-change neutral">Último trimestre</div>
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon orange">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <div class="metric-content">
                <div class="metric-label">Tiempo Promedio</div>
                <div class="metric-value">4.9 días</div>
                <div class="metric-change positive">-8% optimización</div>
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon red">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              </div>
              <div class="metric-content">
                <div class="metric-label">Anomalías</div>
                <div class="metric-value">3</div>
                <div class="metric-change neutral">Detectadas esta semana</div>
              </div>
            </div>
          </div>

          <!-- Tabs de Visualización -->
          <div class="visualization-tabs">
            <button class="tab-btn active" data-tab="comparacion">Comparación</button>
            <button class="tab-btn" data-tab="historico">Histórico</button>
            <button class="tab-btn" data-tab="rankings">Rankings</button>
            <button class="tab-btn" data-tab="heatmap">Heatmap</button>
            <button class="tab-btn" data-tab="anomalias">Anomalías</button>
          </div>

          <!-- Tab: Comparación -->
          <div class="tab-content active" id="comparacion">
            <div class="charts-row">
              <div class="chart-card">
                <h3>Eficiencia por Área</h3>
                <p class="chart-subtitle">Comparación de rendimiento entre departamentos</p>
                <div class="bar-chart">
                  ${generateBarChart()}
                </div>
              </div>

              <div class="chart-card">
                <h3>Métricas Globales</h3>
                <p class="chart-subtitle">Análisis multidimensional del sistema</p>
                <div class="radar-chart">
                  ${generateRadarChart()}
                </div>
              </div>
            </div>

            <!-- Detalle por Área -->
            <div class="visualization-card">
              <h3>Comparación Detallada por Área</h3>
              <p class="card-subtitle">Métricas clave de rendimiento</p>

              <div class="areas-table">
                ${generateAreaRow('TI', '145', '4.2d', 'Excelente', '88', 'success')}
                ${generateAreaRow('Marketing', '120', '3.8d', 'Excelente', '90', 'success')}
                ${generateAreaRow('Operaciones', '180', '6.5d', 'Mejora', '72', 'danger')}
                ${generateAreaRow('Ventas', '95', '4.8d', 'Excelente', '85', 'success')}
                ${generateAreaRow('RRHH', '68', '5.1d', 'Bueno', '82', 'warning')}
              </div>
            </div>
          </div>

          <!-- Tab: Histórico -->
          <div class="tab-content" id="historico">
            <div class="chart-card full-width">
              <h3>Productividad Histórica</h3>
              <p class="chart-subtitle">Evolución de eficiencia por área (últimos 6 meses)</p>
              <div class="line-chart">
                ${generateLineChart()}
              </div>
            </div>

            <div class="chart-card full-width" style="margin-top: 20px;">
              <h3>Tendencias de Crecimiento</h3>
              <p class="chart-subtitle">Áreas de mejora acumulada</p>
              <div class="area-chart">
                ${generateAreaStackedChart()}
              </div>
            </div>
          </div>

          <!-- Tab: Rankings -->
          <div class="tab-content" id="rankings">
            <div class="rankings-container">
              <!-- Columna Izquierda: Tareas Más Demoradas -->
              <div class="ranking-section">
                <div class="ranking-header">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f44336" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  <div>
                    <h3>Tareas Más Demoradas</h3>
                    <p>Top 5 tareas con mayor retraso</p>
                  </div>
                </div>
                
                <div class="ranking-list">
                  ${generateDelayedTaskItem(1, 'Auditoría Procesos', 'Operaciones', '+4.5d', 'alto', '#005a9c')}
                  ${generateDelayedTaskItem(2, 'Migración Sistema', 'TI', '+3.2d', 'critico', '#005a9c')}
                  ${generateDelayedTaskItem(3, 'Campaña Redes', 'Marketing', '+2.8d', 'medio', '#005a9c')}
                  ${generateDelayedTaskItem(4, 'Onboarding Personal', 'RRHH', '+2.1d', 'bajo', '#005a9c')}
                  ${generateDelayedTaskItem(5, 'Cierre Trimestre', 'Ventas', '+1.9d', 'medio', '#005a9c')}
                </div>

                <div class="chart-card" style="margin-top: 20px;">
                  <h4>Distribución de Tareas por Impacto</h4>
                  <div class="horizontal-bar-chart">
                    ${generateHorizontalBarChart()}
                  </div>
                </div>
              </div>

              <!-- Columna Derecha: Empleados Más Eficientes -->
              <div class="ranking-section">
                <div class="ranking-header">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ff9800" stroke-width="2">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  <div>
                    <h3>Empleados Más Eficientes</h3>
                    <p>Top 5 colaboradores destacados</p>
                  </div>
                </div>
                
                <div class="ranking-list">
                  ${generateEmployeeItem(1, 'María Rodríguez', 'Marketing', '95%', 48, '#ff9800')}
                  ${generateEmployeeItem(2, 'Luis García', 'TI', '92%', 47, '#9e9e9e')}
                  ${generateEmployeeItem(3, 'Ana Fernández', 'Ventas', '90%', 41, '#cd7f32')}
                  ${generateEmployeeItem(4, 'Carlos Méndez', 'Operaciones', '88%', 52, '#005a9c')}
                  ${generateEmployeeItem(5, 'Pedro Sánchez', 'RRHH', '87%', 35, '#005a9c')}
                </div>
              </div>
            </div>
          </div>

          <!-- Tab: Heatmap -->
          <div class="tab-content" id="heatmap">
            <div class="chart-card full-width">
              <h3>Mapa de Calor de Eficiencia Semanal</h3>
              <p class="chart-subtitle">Rendimiento por área y día de la semana</p>
              
              <div class="heatmap-container">
                <div class="heatmap-table">
                  <div class="heatmap-header">
                    <div class="heatmap-cell header-cell">Área</div>
                    <div class="heatmap-cell header-cell">Lunes</div>
                    <div class="heatmap-cell header-cell">Martes</div>
                    <div class="heatmap-cell header-cell">Miércoles</div>
                    <div class="heatmap-cell header-cell">Jueves</div>
                    <div class="heatmap-cell header-cell">Viernes</div>
                  </div>
                  
                  ${generateHeatmapRow('TI', [92, 88, 90, 85, 78])}
                  ${generateHeatmapRow('Marketing', [88, 91, 93, 89, 82])}
                  ${generateHeatmapRow('Operaciones', [70, 72, 75, 71, 68])}
                  ${generateHeatmapRow('Ventas', [85, 87, 86, 88, 80])}
                  ${generateHeatmapRow('RRHH', [80, 82, 84, 83, 79])}
                </div>
              </div>
            </div>
          </div>

          <!-- Tab: Anomalías -->
          <div class="tab-content" id="anomalias">
            <div class="anomalies-section">
              <div class="anomalies-header">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#f44336" stroke-width="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                <div>
                  <h3>Detección de Anomalías</h3>
                  <p>Patrones inusuales detectados por el sistema de IA</p>
                </div>
              </div>

              <div class="anomalies-list">
                ${generateAnomalyItem('alto', 'Pico de demoras', 'Operaciones', 'Incremento inusual de 35% en tiempo de procesamiento')}
                ${generateAnomalyItem('medio', 'Baja productividad', 'Ventas', 'Reducción del 15% vs promedio histórico')}
                ${generateAnomalyItem('medio', 'Sobrecarga', 'TI', 'Asignación de tareas supera capacidad en 20%')}
              </div>

              <div class="recommendations-section">
                <h3>Recomendaciones de Acción</h3>
                <p class="section-subtitle">Acciones sugeridas para mitigar anomalías</p>

                <div class="recommendations-list">
                  ${generateRecommendationItem(1, 'Operaciones', 'Revisar carga de trabajo y considerar redistribución de tareas')}
                  ${generateRecommendationItem(2, 'Ventas', 'Implementar programa de capacitación para recuperar productividad')}
                  ${generateRecommendationItem(3, 'TI', 'Contratar personal temporal o reasignar recursos de otras áreas')}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

function generateBarChart(): string {
  const areas = [
    { name: 'TI', value: 88 },
    { name: 'Marketing', value: 92 },
    { name: 'Operaciones', value: 72 },
    { name: 'Ventas', value: 85 },
    { name: 'RRHH', value: 78 }
  ];

  return `
    <svg class="chart-svg" viewBox="0 0 500 300">
      <g class="bars">
        ${areas.map((area, i) => `
          <rect x="${50 + i * 90}" y="${280 - area.value * 2.5}" width="60" height="${area.value * 2.5}" 
                fill="#005a9c" rx="3"/>
          <text x="${80 + i * 90}" y="${295}" text-anchor="middle" font-size="12" fill="#666">
            ${area.name}
          </text>
          <text x="${80 + i * 90}" y="${275 - area.value * 2.5}" text-anchor="middle" font-size="14" 
                font-weight="600" fill="#005a9c">
            ${area.value}
          </text>
        `).join('')}
      </g>
      
      <!-- Grid lines -->
      <g class="grid" stroke="#e0e0e0" stroke-width="1">
        <line x1="40" y1="30" x2="40" y2="280"/>
        <line x1="40" y1="280" x2="490" y2="280"/>
        ${[0, 25, 50, 75, 100].map(val => `
          <line x1="35" y1="${280 - val * 2.5}" x2="490" y2="${280 - val * 2.5}" stroke-dasharray="2,2"/>
          <text x="25" y="${285 - val * 2.5}" font-size="10" fill="#999" text-anchor="end">${val}</text>
        `).join('')}
      </g>
    </svg>
  `;
}

function generateLineChart(): string {
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
  const areas = [
    { name: 'Marketing', color: '#00bcd4', values: [82, 84, 83, 85, 87, 89] },
    { name: 'Operaciones', color: '#ff9800', values: [68, 70, 69, 71, 72, 73] },
    { name: 'RRHH', color: '#9c27b0', values: [75, 77, 76, 78, 79, 80] },
    { name: 'TI', color: '#2196f3', values: [86, 88, 87, 89, 90, 91] },
    { name: 'Ventas', color: '#4caf50', values: [81, 83, 82, 84, 85, 86] }
  ];

  const width = 1200;
  const height = 400;
  const padding = { top: 20, right: 150, bottom: 50, left: 60 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  
  const xStep = chartWidth / (months.length - 1);
  const maxValue = 100;
  const yScale = chartHeight / maxValue;

  return `
    <svg class="chart-svg" viewBox="0 0 ${width} ${height}">
      <!-- Grid lines -->
      <g class="grid" stroke="#e0e0e0" stroke-width="1">
        ${[0, 25, 50, 75, 100].map(val => `
          <line x1="${padding.left}" y1="${padding.top + chartHeight - val * yScale}" 
                x2="${padding.left + chartWidth}" y2="${padding.top + chartHeight - val * yScale}" 
                stroke-dasharray="4,4"/>
          <text x="${padding.left - 10}" y="${padding.top + chartHeight - val * yScale + 4}" 
                font-size="12" fill="#999" text-anchor="end">${val}</text>
        `).join('')}
      </g>
      
      <!-- X axis labels -->
      <g class="x-labels" font-size="12" fill="#666">
        ${months.map((month, i) => `
          <text x="${padding.left + i * xStep}" y="${height - padding.bottom + 20}" text-anchor="middle">
            ${month}
          </text>
        `).join('')}
      </g>
      
      <!-- Lines for each area -->
      ${areas.map(area => {
        const points = area.values.map((val, i) => 
          `${padding.left + i * xStep},${padding.top + chartHeight - val * yScale}`
        ).join(' ');
        
        return `
          <g class="line-group">
            <polyline points="${points}" fill="none" stroke="${area.color}" stroke-width="2.5"/>
            ${area.values.map((val, i) => `
              <circle cx="${padding.left + i * xStep}" cy="${padding.top + chartHeight - val * yScale}" 
                      r="4" fill="${area.color}"/>
            `).join('')}
          </g>
        `;
      }).join('')}
      
      <!-- Legend -->
      <g class="legend" font-size="13">
        ${areas.map((area, i) => `
          <g transform="translate(${width - padding.right + 20}, ${padding.top + i * 25})">
            <line x1="0" y1="0" x2="20" y2="0" stroke="${area.color}" stroke-width="2.5"/>
            <circle cx="10" cy="0" r="4" fill="${area.color}"/>
            <text x="30" y="4" fill="#666">${area.name}</text>
          </g>
        `).join('')}
      </g>
    </svg>
  `;
}

function generateAreaStackedChart(): string {
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
  const width = 1200;
  const height = 400;
  const padding = { top: 20, right: 150, bottom: 50, left: 60 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  
  const xStep = chartWidth / (months.length - 1);
  const maxValue = 260;
  const yScale = chartHeight / maxValue;

  // Data acumulada por área
  const areas = [
    { name: 'TI', color: '#2196f3', values: [65, 68, 70, 75, 78, 82] },
    { name: 'Marketing', color: '#00bcd4', values: [60, 62, 65, 68, 70, 72] },
    { name: 'Operaciones', color: '#ff9800', values: [50, 52, 55, 58, 62, 65] },
    { name: 'Ventas', color: '#4caf50', values: [45, 48, 50, 52, 55, 58] },
    { name: 'RRHH', color: '#9c27b0', values: [40, 42, 45, 48, 50, 53] }
  ];

  // Calcular puntos acumulados de abajo hacia arriba
  const stackedAreas = areas.map((area, areaIndex) => {
    const baseValues = months.map((_, monthIndex) => {
      let sum = 0;
      for (let i = areas.length - 1; i > areaIndex; i--) {
        sum += areas[i].values[monthIndex];
      }
      return sum;
    });
    
    const topValues = months.map((_, monthIndex) => {
      return baseValues[monthIndex] + area.values[monthIndex];
    });

    return { ...area, baseValues, topValues };
  });

  return `
    <svg class="chart-svg" viewBox="0 0 ${width} ${height}">
      <!-- Grid lines -->
      <g class="grid" stroke="#e0e0e0" stroke-width="1">
        ${[0, 65, 130, 195, 260].map(val => `
          <line x1="${padding.left}" y1="${padding.top + chartHeight - val * yScale}" 
                x2="${padding.left + chartWidth}" y2="${padding.top + chartHeight - val * yScale}" 
                stroke-dasharray="4,4"/>
          <text x="${padding.left - 10}" y="${padding.top + chartHeight - val * yScale + 4}" 
                font-size="12" fill="#999" text-anchor="end">${val}</text>
        `).join('')}
      </g>
      
      <!-- X axis labels -->
      <g class="x-labels" font-size="12" fill="#666">
        ${months.map((month, i) => `
          <text x="${padding.left + i * xStep}" y="${height - padding.bottom + 20}" text-anchor="middle">
            ${month}
          </text>
        `).join('')}
      </g>
      
      <!-- Stacked areas (reverse order for proper rendering) -->
      ${stackedAreas.reverse().map(area => {
        const topPoints = area.topValues.map((val, i) => 
          `${padding.left + i * xStep},${padding.top + chartHeight - val * yScale}`
        );
        const bottomPoints = area.baseValues.map((val, i) => 
          `${padding.left + i * xStep},${padding.top + chartHeight - val * yScale}`
        ).reverse();
        
        const pathData = `M ${topPoints.join(' L ')} L ${bottomPoints.join(' L ')} Z`;
        
        return `
          <path d="${pathData}" fill="${area.color}" opacity="0.7"/>
        `;
      }).join('')}
      
      <!-- Legend -->
      <g class="legend" font-size="13">
        ${areas.map((area, i) => `
          <g transform="translate(${width - padding.right + 20}, ${padding.top + i * 25})">
            <rect x="0" y="-8" width="20" height="16" fill="${area.color}" opacity="0.7"/>
            <text x="30" y="4" fill="#666">${area.name}</text>
          </g>
        `).join('')}
      </g>
    </svg>
  `;
}

function generateRadarChart(): string {
  const metrics = ['Velocidad', 'Calidad', 'Eficiencia', 'Colaboración', 'Innovación'];
  const values = [85, 90, 88, 78, 82];
  const centerX = 150;
  const centerY = 150;
  const radius = 100;
  
  const points = values.map((val, i) => {
    const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
    const r = (val / 100) * radius;
    return `${centerX + r * Math.cos(angle)},${centerY + r * Math.sin(angle)}`;
  }).join(' ');

  return `
    <svg class="radar-svg" viewBox="0 0 300 300">
      <!-- Background circles -->
      <g class="grid" fill="none" stroke="#e0e0e0">
        ${[20, 40, 60, 80, 100].map(pct => `
          <circle cx="${centerX}" cy="${centerY}" r="${radius * pct / 100}"/>
        `).join('')}
      </g>
      
      <!-- Axes -->
      <g class="axes" stroke="#ccc" stroke-width="1">
        ${metrics.map((_, i) => {
          const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
          return `<line x1="${centerX}" y1="${centerY}" 
                       x2="${centerX + radius * Math.cos(angle)}" 
                       y2="${centerY + radius * Math.sin(angle)}"/>`;
        }).join('')}
      </g>
      
      <!-- Data polygon -->
      <polygon points="${points}" fill="rgba(0, 188, 212, 0.3)" stroke="#00bcd4" stroke-width="2"/>
      
      <!-- Labels -->
      <g class="labels" font-size="11" fill="#666" text-anchor="middle">
        ${metrics.map((metric, i) => {
          const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
          const labelRadius = radius + 20;
          return `<text x="${centerX + labelRadius * Math.cos(angle)}" 
                       y="${centerY + labelRadius * Math.sin(angle) + 4}">
                    ${metric}
                  </text>`;
        }).join('')}
      </g>
      
      <!-- Value dots -->
      ${values.map((val, i) => {
        const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
        const r = (val / 100) * radius;
        return `<circle cx="${centerX + r * Math.cos(angle)}" 
                       cy="${centerY + r * Math.sin(angle)}" 
                       r="4" fill="#00bcd4"/>`;
      }).join('')}
    </svg>
  `;
}

function generateAreaRow(
  area: string,
  tasks: string,
  avgTime: string,
  performance: string,
  efficiency: string,
  efficiencyType: 'success' | 'warning' | 'danger'
): string {
  return `
    <div class="area-row">
      <div class="area-name">${area}</div>
      <div class="area-metrics">
        <div class="metric">
          <span class="metric-label">Tareas</span>
          <span class="metric-value">${tasks}</span>
        </div>
        <div class="metric">
          <span class="metric-label">Tiempo Prom.</span>
          <span class="metric-value">${avgTime}</span>
        </div>
        <div class="metric">
          <span class="metric-label">Desempeño</span>
          <span class="metric-value performance">${performance === 'Excelente' ? '⚡' : '⚠️'} ${performance}</span>
        </div>
      </div>
      <div class="area-efficiency">
        <span class="efficiency-badge ${efficiencyType}">${efficiency}% eficiencia</span>
      </div>
    </div>
  `;
}

function generateDelayedTaskItem(
  rank: number,
  taskName: string,
  area: string,
  delay: string,
  priority: string,
  badgeColor: string
): string {
  const priorityColors: { [key: string]: { bg: string; text: string } } = {
    'critico': { bg: '#f8d7da', text: '#721c24' },
    'alto': { bg: '#fff3cd', text: '#856404' },
    'medio': { bg: '#fff3cd', text: '#856404' },
    'bajo': { bg: '#d4edda', text: '#155724' }
  };
  
  const priorityLabels: { [key: string]: string } = {
    'critico': 'crítico',
    'alto': 'alto',
    'medio': 'medio',
    'bajo': 'bajo'
  };

  const color = priorityColors[priority];

  return `
    <div class="ranking-item">
      <div class="rank-badge" style="background: ${badgeColor};">#${rank}</div>
      <div class="ranking-info">
        <div class="ranking-title">${taskName}</div>
        <div class="ranking-subtitle">${area}</div>
      </div>
      <div class="ranking-stats">
        <div class="delay-badge" style="color: ${delay.includes('+') ? '#f44336' : '#4caf50'};">
          ${delay}
        </div>
        <div class="priority-badge" style="background: ${color.bg}; color: ${color.text};">
          ${priorityLabels[priority]}
        </div>
      </div>
    </div>
  `;
}

function generateEmployeeItem(
  rank: number,
  name: string,
  area: string,
  efficiency: string,
  tasks: number,
  medalColor: string
): string {
  return `
    <div class="ranking-item">
      <div class="rank-badge medal" style="background: ${medalColor};">${rank}</div>
      <div class="ranking-info">
        <div class="ranking-title">${name}</div>
        <div class="ranking-subtitle">${area}</div>
      </div>
      <div class="ranking-stats">
        <div class="efficiency-stat" style="color: #4caf50; font-weight: 700; font-size: 18px;">
          ${efficiency}
        </div>
        <div class="tasks-stat" style="color: #666; font-size: 13px;">
          ${tasks} tareas
        </div>
      </div>
    </div>
  `;
}

function generateHorizontalBarChart(): string {
  const tasks = [
    { name: 'Auditoría Procesos', value: 4.5 },
    { name: 'Migración Sistema', value: 3.8 },
    { name: 'Campaña Redes', value: 3.2 },
    { name: 'Onboarding Personal', value: 2.5 },
    { name: 'Cierre Trimestre', value: 1.8 }
  ];

  const maxValue = 8;
  
  return `
    <svg class="chart-svg" viewBox="0 0 900 250" style="width: 100%; height: 250px;">
      <g class="bars">
        ${tasks.map((task, i) => {
          const barWidth = (task.value / maxValue) * 700;
          return `
            <g transform="translate(0, ${i * 50})">
              <text x="0" y="20" font-size="13" fill="#666" text-anchor="start">
                ${task.name}
              </text>
              <rect x="200" y="5" width="${barWidth}" height="28" fill="#00bcd4" rx="4"/>
              <text x="${210 + barWidth}" y="25" font-size="12" fill="#666" font-weight="600">
                ${task.value}
              </text>
            </g>
          `;
        }).join('')}
      </g>
      
      <!-- Grid lines -->
      <g class="grid" stroke="#e0e0e0" stroke-width="1">
        ${[0, 2, 4, 6, 8].map(val => {
          const x = 200 + (val / maxValue) * 700;
          return `
            <line x1="${x}" y1="0" x2="${x}" y2="250" stroke-dasharray="2,2"/>
            <text x="${x}" y="245" font-size="10" fill="#999" text-anchor="middle">${val}</text>
          `;
        }).join('')}
      </g>
    </svg>
  `;
}

function generateHeatmapRow(area: string, values: number[]): string {
  const getHeatColor = (value: number): string => {
    if (value >= 90) return '#4caf50'; // Verde - Excelente
    if (value >= 85) return '#8bc34a'; // Verde claro - Muy bueno
    if (value >= 80) return '#ff9800'; // Naranja - Bueno
    if (value >= 75) return '#ff9800'; // Naranja - Regular
    if (value >= 70) return '#f44336'; // Rojo claro - Bajo
    return '#f44336'; // Rojo - Muy bajo
  };

  return `
    <div class="heatmap-row">
      <div class="heatmap-cell area-cell">${area}</div>
      ${values.map(value => `
        <div class="heatmap-cell value-cell" style="background-color: ${getHeatColor(value)};">
          ${value}%
        </div>
      `).join('')}
    </div>
  `;
}

function generateAnomalyItem(severity: string, title: string, area: string, description: string): string {
  const severityConfig: { [key: string]: { border: string; bg: string; badge: string; badgeText: string } } = {
    'alto': { 
      border: '#f44336', 
      bg: '#ffebee', 
      badge: '#fff3cd', 
      badgeText: '#856404' 
    },
    'medio': { 
      border: '#ff9800', 
      bg: '#fff3e0', 
      badge: '#fff3cd', 
      badgeText: '#856404' 
    },
    'bajo': { 
      border: '#4caf50', 
      bg: '#e8f5e9', 
      badge: '#d4edda', 
      badgeText: '#155724' 
    }
  };

  const config = severityConfig[severity];

  return `
    <div class="anomaly-card" style="border-left: 4px solid ${config.border}; background: ${config.bg};">
      <div class="anomaly-header">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="${config.border}" stroke-width="2">
          <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <div class="anomaly-info">
          <div class="anomaly-title">${title}</div>
          <div class="anomaly-badges">
            <span class="severity-badge" style="background: ${config.badge}; color: ${config.badgeText};">${severity}</span>
            <span class="area-badge">${area}</span>
          </div>
        </div>
      </div>
      <div class="anomaly-description">${description}</div>
    </div>
  `;
}

function generateRecommendationItem(number: number, area: string, description: string): string {
  return `
    <div class="recommendation-item">
      <div class="recommendation-number">${number}</div>
      <div class="recommendation-content">
        <span class="recommendation-area">${area}:</span>
        <span class="recommendation-text">${description}</span>
      </div>
    </div>
  `;
}

export function initIntelligentVisualization(): void {
  // Initialize AI Assistant
  initAIAssistant();

  // Tabs functionality
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const tabName = button.getAttribute('data-tab');
      
      // Remove active class from all buttons and contents
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));
      
      // Add active class to clicked button
      button.classList.add('active');
      
      // Show corresponding content
      const targetContent = document.getElementById(tabName || 'comparacion');
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });

  // Mobile menu
  const mobileToggle = document.querySelector('.btn-mobile-menu');
  const sidebar = document.querySelector('.sidebar');
  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-active');
    });
  }

  // AI Assistant button
  const aiButton = document.querySelector('.btn-ai-assistant');
  if (aiButton) {
    aiButton.addEventListener('click', () => {
      const assistant = document.getElementById('aiAssistant');
      if (assistant) {
        assistant.classList.add('active');
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
