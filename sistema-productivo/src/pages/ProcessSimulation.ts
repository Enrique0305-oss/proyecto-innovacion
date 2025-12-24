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
          <div class="module-header">
            <div class="module-icon" style="background: rgba(0, 114, 198, 0.2);">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <circle cx="8" cy="16" r="3" stroke="white" stroke-width="2"/>
                <circle cx="24" cy="16" r="3" stroke="white" stroke-width="2"/>
                <path d="M11 16h10" stroke="white" stroke-width="2"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Análisis de Cuellos de Botella con IA</h2>
              <p class="module-description">Modelo CatBoost - Predicción de tareas críticas (99.9% precisión)</p>
            </div>
          </div>

          <div class="control-panel">
            <div class="control-row">
              <button class="btn-execute" id="loadAnalysisBtn">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 2a8 8 0 100 16 8 8 0 000-16z" stroke="currentColor" stroke-width="2"/>
                </svg>
                Analizar Cuellos de Botella
              </button>
            </div>
          </div>

          <div class="metrics-grid">
            <div class="metric-card">
              <span class="metric-label">Accuracy</span>
              <span class="metric-value" id="modelAccuracy">99.9%</span>
            </div>
            <div class="metric-card">
              <span class="metric-label">Bottlenecks Detectados</span>
              <span class="metric-value critical" id="totalBottlenecks">-</span>
            </div>
          </div>

          <div class="table-section">
            <h3>⚠️ Cuellos de Botella</h3>
            <table class="data-table" id="bottlenecksTable">
              <thead>
                <tr>
                  <th>Actividad</th>
                  <th>Probabilidad</th>
                  <th>Riesgo</th>
                </tr>
              </thead>
              <tbody>
                <tr><td colspan="3" class="no-data">Cargue un análisis</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  `;
}

export function initProcessSimulation() {
  const loadBtn = document.getElementById('loadAnalysisBtn');
  initAIAssistant();

  if (loadBtn) {
    loadBtn.addEventListener('click', loadAnalysis);
  }

  async function loadAnalysis() {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/ml/process-mining/analyze`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        renderAnalysis(data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  function renderAnalysis(data: any) {
    const summary = data.summary || {};
    document.getElementById('totalBottlenecks')!.textContent = summary.total_bottlenecks || '0';

    const tbody = document.querySelector('#bottlenecksTable tbody');
    if (tbody && data.bottlenecks) {
      tbody.innerHTML = data.bottlenecks.map((b: any) => `
        <tr>
          <td>${b.activity.substring(0, 60)}</td>
          <td>${(b.bottleneck_probability * 100).toFixed(1)}%</td>
          <td><span class="risk-badge ${b.risk_level.toLowerCase()}">${b.risk_level}</span></td>
        </tr>
      `).join('');
    }
  }
}
