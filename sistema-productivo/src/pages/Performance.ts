import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';
import { API_URL } from '../utils/api';

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
                <tbody id="collaboratorsTableBody">
                  <!-- Se llenará dinámicamente -->
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
  loadCollaborators();

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

async function loadCollaborators(): Promise<void> {
  try {
    const response = await fetch(`${API_URL}/users`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (!response.ok) throw new Error('Error al cargar colaboradores');

    const data = await response.json();
    console.log('📊 Datos recibidos del backend:', data);
    console.log('📊 Total de usuarios:', data.users?.length || 0);
    
    const tbody = document.getElementById('collaboratorsTableBody');
    
    if (tbody && data.users) {
      tbody.innerHTML = data.users.map((user: any) => {
        const initials = (user.full_name || 'NN').substring(0, 2).toUpperCase();
        const performance = user.performance_index || 75;
        
        let perfClass = 'medium';
        let perfIcon = '<path d="M7 4v6M4 7h6" stroke="#ff9800" stroke-width="1.5" stroke-linecap="round"/>';
        
        if (performance >= 85) {
          perfClass = 'high';
          perfIcon = '<path d="M7 10V4M4 7l3-3 3 3" stroke="#28a745" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>';
        } else if (performance < 70) {
          perfClass = 'low';
          perfIcon = '<path d="M7 4V10M10 7L7 10 4 7" stroke="#dc3545" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>';
        }
        
        return `
          <tr>
            <td>
              <div class="collab-info">
                <div class="collab-avatar">${initials}</div>
                <span>${user.full_name || 'Usuario'}</span>
              </div>
            </td>
            <td><span class="area-badge">${user.area || 'Sin área'}</span></td>
            <td>
              <div class="performance-indicator">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  ${perfIcon}
                </svg>
                <span class="perf-value ${perfClass}">${performance}%</span>
              </div>
            </td>
            <td>
              <button class="btn-predict" data-user-id="${user.id}">Predecir</button>
            </td>
          </tr>
        `;
      }).join('');
      
      // Agregar event listeners a los botones
      attachPredictButtons();
    } else {
      console.warn('⚠️ No se encontraron colaboradores o tbody no existe');
      if (tbody) {
        tbody.innerHTML = `
          <tr>
            <td colspan="4" style="text-align: center; padding: 40px; color: #6c757d;">
              No hay colaboradores disponibles
            </td>
          </tr>
        `;
      }
    }
  } catch (error) {
    console.error('Error cargando colaboradores:', error);
    const tbody = document.getElementById('collaboratorsTableBody');
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="4" style="text-align: center; padding: 40px; color: #dc3545;">
            Error al cargar colaboradores: ${error}
          </td>
        </tr>
      `;
    }
  }
}

function attachPredictButtons(): void {
  const predictButtons = document.querySelectorAll('.btn-predict');
  
  predictButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      const target = e.target as HTMLElement;
      const userId = target.getAttribute('data-user-id');
      
      if (userId) {
        await performHybridAnalysis(userId);
      }
    });
  });
}

async function performHybridAnalysis(userId: string): Promise<void> {
  const detailPanel = document.getElementById('detailPanel');
  if (!detailPanel) return;
  
  try {
    // Mostrar loading
    detailPanel.style.display = 'block';
    detailPanel.innerHTML = `
      <div style="text-align: center; padding: 60px;">
        <div style="display: inline-block; width: 50px; height: 50px; border: 4px solid #f3f3f3; border-top: 4px solid #00bcd4; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        <p style="margin-top: 20px; color: #6c757d;">Analizando desempeño...</p>
      </div>
    `;
    
    const response = await fetch(`${API_URL}/ml/analisis-desempeno`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({ user_id: userId })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Error en el análisis');
    }

    const result = await response.json();
    displayHybridResults(userId, result);
    
  } catch (error: any) {
    console.error('Error:', error);
    alert(`Error: ${error.message}`);
    if (detailPanel) {
      detailPanel.style.display = 'none';
    }
  }
}

function displayHybridResults(userId: string, data: any): void {
  const detailPanel = document.getElementById('detailPanel');
  if (!detailPanel) return;
  
  const { metricas, prediccion, recomendaciones } = data;
  
  // Determinar color y badge según clase predicha
  const claseBadges: { [key: string]: { label: string, color: string, emoji: string } } = {
    'high_performer': { label: 'Alto Desempeño', color: '#28a745', emoji: '⭐' },
    'at_risk': { label: 'En Riesgo', color: '#ff9800', emoji: '⚠️' },
    'resignation_risk': { label: 'Riesgo de Renuncia', color: '#dc3545', emoji: '🚨' }
  };
  
  const claseInfo = claseBadges[prediccion.clase] || { label: 'Desconocido', color: '#6c757d', emoji: '❓' };
  
  // Obtener info del usuario desde los datos o localStorage
  const userName = data.user_name || `Usuario ${userId}`;
  const initials = userName.substring(0, 2).toUpperCase();
  
  detailPanel.innerHTML = `
    <div class="detail-header">
      <div class="detail-person">
        <div class="detail-avatar">${initials}</div>
        <div class="detail-person-info">
          <h3>${userName}</h3>
          <div class="detail-badges">
            <span class="performance-badge" style="background: ${claseInfo.color};">
              ${claseInfo.emoji} ${claseInfo.label}
            </span>
          </div>
        </div>
      </div>
      <div class="detail-performance">
        <span class="detail-perf-value">${metricas.rendimiento}%</span>
        <span class="detail-perf-label">Desempeño</span>
      </div>
    </div>

    <div class="detail-stats">
      <div class="detail-stat">
        <span class="detail-stat-label">Tareas Completadas</span>
        <span class="detail-stat-value">${metricas.tareas_completadas} / ${metricas.tareas_totales}</span>
      </div>
      <div class="detail-stat">
        <span class="detail-stat-label">Tiempo Promedio</span>
        <span class="detail-stat-value">${metricas.tiempo_promedio}d</span>
      </div>
      <div class="detail-stat">
        <span class="detail-stat-label">Calidad</span>
        <span class="detail-stat-value">${metricas.calidad}%</span>
      </div>
      <div class="detail-stat">
        <span class="detail-stat-label">Carga Actual</span>
        <span class="detail-stat-value">${metricas.carga_actual}%</span>
      </div>
    </div>

    <div class="detail-content-grid">
      <!-- CAPA 1: Métricas SQL -->
      <div class="detail-section">
        <h4>📊 CAPA 1: Métricas (SQL + Agregación)</h4>
        <p class="section-subtitle">Datos calculados desde la base de datos</p>
        
        <div style="display: flex; flex-direction: column; gap: 20px; margin-top: 20px;">
          <!-- Rendimiento -->
          <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="font-size: 13px; font-weight: 600; color: #495057;">Rendimiento</span>
              <span style="font-size: 13px; font-weight: 700; color: ${metricas.rendimiento >= 80 ? '#28a745' : metricas.rendimiento >= 60 ? '#ffc107' : '#dc3545'};">
                ${metricas.rendimiento}%
              </span>
            </div>
            <div style="background: #e9ecef; height: 12px; border-radius: 6px; overflow: hidden;">
              <div style="background: ${metricas.rendimiento >= 80 ? '#28a745' : metricas.rendimiento >= 60 ? '#ffc107' : '#dc3545'}; 
                          width: ${metricas.rendimiento}%; height: 100%; border-radius: 6px; transition: width 0.3s ease;"></div>
            </div>
          </div>

          <!-- Calidad -->
          <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="font-size: 13px; font-weight: 600; color: #495057;">Calidad</span>
              <span style="font-size: 13px; font-weight: 700; color: ${metricas.calidad >= 95 ? '#28a745' : metricas.calidad >= 85 ? '#ffc107' : '#dc3545'};">
                ${metricas.calidad}%
              </span>
            </div>
            <div style="background: #e9ecef; height: 12px; border-radius: 6px; overflow: hidden;">
              <div style="background: ${metricas.calidad >= 95 ? '#28a745' : metricas.calidad >= 85 ? '#ffc107' : '#dc3545'}; 
                          width: ${metricas.calidad}%; height: 100%; border-radius: 6px; transition: width 0.3s ease;"></div>
            </div>
          </div>

          <!-- Tasa de Retrabajos (invertida) -->
          <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="font-size: 13px; font-weight: 600; color: #495057;">Tasa de Retrabajos</span>
              <span style="font-size: 13px; font-weight: 700; color: ${metricas.tasa_retrabajos < 10 ? '#28a745' : metricas.tasa_retrabajos < 20 ? '#ffc107' : '#dc3545'};">
                ${metricas.tasa_retrabajos}%
              </span>
            </div>
            <div style="background: #e9ecef; height: 12px; border-radius: 6px; overflow: hidden;">
              <div style="background: ${metricas.tasa_retrabajos < 10 ? '#28a745' : metricas.tasa_retrabajos < 20 ? '#ffc107' : '#dc3545'}; 
                          width: ${metricas.tasa_retrabajos}%; height: 100%; border-radius: 6px; transition: width 0.3s ease;"></div>
            </div>
          </div>

          <!-- Carga Actual -->
          <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="font-size: 13px; font-weight: 600; color: #495057;">Carga Actual</span>
              <span style="font-size: 13px; font-weight: 700; color: ${metricas.carga_actual < 70 ? '#28a745' : metricas.carga_actual < 90 ? '#ffc107' : '#dc3545'};">
                ${metricas.carga_actual}%
              </span>
            </div>
            <div style="background: #e9ecef; height: 12px; border-radius: 6px; overflow: hidden;">
              <div style="background: ${metricas.carga_actual < 70 ? '#28a745' : metricas.carga_actual < 90 ? '#ffc107' : '#dc3545'}; 
                          width: ${Math.min(metricas.carga_actual, 100)}%; height: 100%; border-radius: 6px; transition: width 0.3s ease;"></div>
            </div>
          </div>

          <!-- Tareas completadas -->
          <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #00bcd4;">
            <div style="font-size: 12px; color: #6c757d; margin-bottom: 4px;">Tareas Completadas</div>
            <div style="font-size: 20px; font-weight: 700; color: #495057;">
              ${metricas.tareas_completadas} <span style="font-size: 14px; color: #6c757d;">/ ${metricas.tareas_totales}</span>
            </div>
          </div>

          <!-- Tiempo Promedio -->
          <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #9c27b0;">
            <div style="font-size: 12px; color: #6c757d; margin-bottom: 4px;">Tiempo Promedio</div>
            <div style="font-size: 20px; font-weight: 700; color: #495057;">
              ${metricas.tiempo_promedio} <span style="font-size: 14px; color: #6c757d;">días</span>
            </div>
          </div>
        </div>
      </div>

      <!-- CAPA 2: Predicción ML -->
      <div class="detail-section">
        <h4>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
            <circle cx="10" cy="10" r="8" fill="#00bcd4"/>
            <path d="M10 6v4M10 13v1" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          🤖 CAPA 2: Predicción ML (CatBoost)
        </h4>
        <p class="section-subtitle">Modelo XGBoost con AUC-ROC: 1.0</p>

        <div class="prediction-card" style="background: ${claseInfo.color}; color: white; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
          <div class="prediction-label" style="font-size: 14px; opacity: 0.9;">Clasificación Predicha</div>
          <div class="prediction-result" style="font-size: 28px; font-weight: 700; margin: 10px 0;">
            ${claseInfo.emoji} ${claseInfo.label}
          </div>
          <div style="font-size: 16px; opacity: 0.95;">
            Probabilidad de Renuncia: ${prediccion.probabilidad_renuncia}%
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px;">
          <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; text-align: center;">
            <div style="font-size: 11px; color: #6c757d; margin-bottom: 5px;">⚠️ En Riesgo</div>
            <div style="font-size: 20px; font-weight: 700; color: #ff9800;">${prediccion.probabilidades.at_risk}%</div>
          </div>
          <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; text-align: center;">
            <div style="font-size: 11px; color: #6c757d; margin-bottom: 5px;">⭐ Alto Desemp.</div>
            <div style="font-size: 20px; font-weight: 700; color: #28a745;">${prediccion.probabilidades.high_performer}%</div>
          </div>
          <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; text-align: center;">
            <div style="font-size: 11px; color: #6c757d; margin-bottom: 5px;">🚨 Riesgo Renuncia</div>
            <div style="font-size: 20px; font-weight: 700; color: #dc3545;">${prediccion.probabilidades.resignation_risk}%</div>
          </div>
        </div>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
          <h5 style="margin: 0 0 10px 0; font-size: 14px; color: #495057;">Factores Contribuyentes</h5>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${prediccion.factores.map((f: any) => `
              <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: white; border-radius: 4px;">
                <span style="font-size: 13px; color: #495057;">${f.factor}</span>
                <div style="display: flex; gap: 10px; align-items: center;">
                  <span style="font-size: 13px; font-weight: 600; color: #00bcd4;">${f.value}</span>
                  <span style="font-size: 11px; padding: 2px 8px; border-radius: 12px; background: ${
                    f.impact === 'crítico' || f.impact === 'alto' ? '#dc3545' : 
                    f.impact === 'medio' ? '#ffc107' : '#28a745'
                  }; color: white;">${f.impact}</span>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    </div>

    <!-- CAPA 3: Motor de Reglas -->
    <div class="detail-section" style="grid-column: 1 / -1;">
      <h4>⚙️ CAPA 3: Motor de Recomendaciones (Rule-Based System)</h4>
      <p class="section-subtitle">Acciones sugeridas según reglas de negocio</p>

      ${recomendaciones.length === 0 ? `
        <div style="text-align: center; padding: 40px; background: #f8f9fa; border-radius: 8px;">
          <div style="font-size: 48px;">✓</div>
          <p style="color: #6c757d; margin: 10px 0 0 0;">No se requieren acciones especiales en este momento</p>
        </div>
      ` : `
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; margin-top: 20px;">
          ${recomendaciones.map((rec: any) => {
            const priorityColors: { [key: string]: string } = {
              'crítica': '#dc3545',
              'alta': '#ff9800',
              'media': '#ffc107',
              'baja': '#28a745'
            };
            const color = priorityColors[rec.prioridad] || '#6c757d';
            
            return `
              <div style="background: white; border-left: 4px solid ${color}; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                  <div style="display: flex; gap: 10px; align-items: center;">
                    <span style="font-size: 24px;">${rec.icono}</span>
                    <h5 style="margin: 0; font-size: 15px; color: #212529; font-weight: 600;">${rec.titulo}</h5>
                  </div>
                  <span style="font-size: 10px; padding: 4px 10px; border-radius: 12px; background: ${color}; color: white; text-transform: uppercase; font-weight: 600;">
                    ${rec.prioridad}
                  </span>
                </div>
                <p style="margin: 0; font-size: 13px; color: #6c757d; line-height: 1.5;">
                  ${rec.descripcion}
                </p>
              </div>
            `;
          }).join('')}
        </div>
      `}
    </div>
  `;

  detailPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
