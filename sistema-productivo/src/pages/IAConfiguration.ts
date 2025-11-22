import { Sidebar } from '../components/Sidebar';
import { AIAssistant, initAIAssistant } from '../components/AIAssistant';

export function IAConfigurationPage(): string {
  return `
    <div class="dashboard-layout">
      ${Sidebar('configuracion-ia')}
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
          <div class="config-header">
            <div class="module-icon config">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="white" stroke-width="2">
                <circle cx="20" cy="20" r="3"/>
                <path d="M20 12v-4M20 32v-4M28 20h4M8 20H4M26.8 13.2l2.8-2.8M10.4 29.6l2.8-2.8M26.8 26.8l2.8 2.8M10.4 10.4l2.8 2.8"/>
              </svg>
            </div>
            <div class="module-info">
              <h2 class="module-title">Configuración de IA</h2>
              <p class="module-description">Gestión de modelos y datasets del sistema</p>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-label">Modelos Activos</div>
              <div class="stat-value">4</div>
              <div class="stat-description">De 5 totales</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Precisión Promedio</div>
              <div class="stat-value">91%</div>
              <div class="stat-description">Todos los modelos</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Total Muestras</div>
              <div class="stat-value">6,536</div>
              <div class="stat-description">Entrenamiento</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Datasets</div>
              <div class="stat-value">4</div>
              <div class="stat-description">Archivos cargados</div>
            </div>
          </div>

          <!-- AI Models Section -->
          <div class="models-section">
            <div class="section-header">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6M12 17v6M23 12h-6M7 12H1M18.4 5.6l-4.2 4.2M9.8 14.2l-4.2 4.2M18.4 18.4l-4.2-4.2M9.8 9.8L5.6 5.6"/>
              </svg>
              <h3>Modelos de IA</h3>
              <p>Estado y configuración de los modelos de machine learning</p>
            </div>

            <div class="models-list">
              ${generateModelCard('Clasificación de Riesgo', 'Activo', 'Clasificación Multiclase', 'Random Forest', 94, '2024-11-15', 1250)}
              ${generateModelCard('Predicción de Duración', 'Activo', 'Regresión', 'CatBoost Regressor', 92, '2024-11-10', 980)}
              ${generateModelCard('Recomendación Persona-Tarea', 'Activo', 'Sistema de Recomendación', 'Collaborative Filtering', 89, '2024-11-12', 2100)}
              ${generateModelCard('Desempeño Colaborador', 'Activo', 'Clasificación Multiclase', 'XGBoost', 91, '2024-11-08', 756)}
              ${generateModelCard('Simulación de Flujo', 'Entrenando', 'Process Mining', 'LSTM + Process Mining', 88, '2024-11-01', 1450)}
            </div>
          </div>

          <!-- Datasets Section -->
          <div class="datasets-section">
            <div class="section-header">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" stroke-width="2">
                <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                <polyline points="13 2 13 9 20 9"/>
              </svg>
              <h3>Datasets</h3>
              <p>Archivos de datos para entrenamiento de modelos</p>
            </div>
            <button class="btn-primary" id="btnUploadDataset">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              Subir Dataset
            </button>

            <div class="datasets-list">
              ${generateDatasetCard('tareas_historicas.csv', '2.4 MB', 1250, '2024-11-15')}
              ${generateDatasetCard('colaboradores_performance.csv', '856 KB', 756, '2024-11-10')}
              ${generateDatasetCard('procesos_flujo.csv', '1.8 MB', 1450, '2024-11-01')}
              ${generateDatasetCard('asignaciones_tareas.csv', '3.2 MB', 2100, '2024-11-12')}
            </div>

            <!-- Upload Section -->
            <div class="upload-section">
              <h4>Cargar Nuevo Dataset</h4>
              <p class="upload-description">Sube archivos CSV o Excel para entrenar modelos</p>

              <div class="file-upload">
                <div class="upload-box" id="uploadBox">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                  </svg>
                  <p class="upload-text">Seleccionar archivo <span>Sin archivos seleccionados</span></p>
                  <input type="file" id="fileInput" accept=".csv,.xlsx,.xls" hidden>
                  <button class="btn-upload" id="btnSelectFile">Cargar</button>
                </div>
              </div>

              <div class="dataset-requirements">
                <h5>Requisitos del Dataset</h5>
                <ul>
                  <li>Formato: CSV o Excel (.xlsx)</li>
                  <li>Tamaño máximo: 10 MB</li>
                  <li>Debe incluir encabezados de columna</li>
                  <li>Datos limpios sin valores nulos críticos</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- System Status -->
          <div class="system-status">
            <div class="status-header">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
              <h3>Estado del Sistema</h3>
            </div>

            <div class="status-grid">
              <div class="status-card success">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <div class="status-label">API Activa</div>
              </div>
              <div class="status-card success">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <div class="status-label">Modelos OK</div>
              </div>
              <div class="status-card success">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <div class="status-label">DB Conectada</div>
              </div>
              <div class="status-card success">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <div class="status-label">Cache Activo</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;
}

function generateModelCard(
  name: string,
  status: string,
  type: string,
  algorithm: string,
  precision: number,
  lastTrained: string,
  samples: number
): string {
  const isActive = status === 'Activo';
  const statusColor = isActive ? '#4caf50' : '#ff9800';
  const statusBg = isActive ? '#4caf50' : '#ff9800';
  const precisionColor = precision >= 90 ? '#4caf50' : precision >= 85 ? '#00bcd4' : '#ff9800';

  return `
    <div class="model-card">
      <div class="model-header">
        <div class="model-title">
          <h4>${name}</h4>
          <span class="status-badge" style="background: ${statusBg};">
            ${isActive ? '✓' : '⟳'} ${status}
          </span>
        </div>
        <div class="model-actions">
          <button class="btn-icon-sm" title="Reentrenar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 4 23 10 17 10"/>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
            </svg>
            Reentrenar
          </button>
          <button class="btn-icon-sm" title="Métricas">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
            Métricas
          </button>
        </div>
      </div>

      <div class="model-info">
        <div class="info-row">
          <span class="info-label">Tipo:</span>
          <span class="info-value">${type}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Algoritmo:</span>
          <span class="info-value">${algorithm}</span>
        </div>
      </div>

      <div class="model-metrics">
        <div class="metric-item">
          <div class="metric-header">
            <span>Precisión</span>
            <span class="metric-value" style="color: ${precisionColor};">${precision}%</span>
          </div>
          <div class="metric-bar">
            <div class="metric-fill" style="width: ${precision}%; background: ${precisionColor};"></div>
          </div>
        </div>

        <div class="model-details">
          <div class="detail-item">
            <span class="detail-label">Último Entrenamiento</span>
            <span class="detail-value">${lastTrained}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Muestras</span>
            <span class="detail-value">${samples.toLocaleString()}</span>
          </div>
        </div>
      </div>

      ${!isActive ? '<div class="training-notice"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ff9800" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg> Modelo en proceso de reentrenamiento...</div>' : ''}
    </div>
  `;
}

function generateDatasetCard(
  filename: string,
  size: string,
  records: number,
  uploaded: string
): string {
  return `
    <div class="dataset-card">
      <div class="dataset-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" stroke-width="2">
          <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
          <polyline points="13 2 13 9 20 9"/>
        </svg>
      </div>
      <div class="dataset-info">
        <h5>${filename}</h5>
        <p>${size} • ${records.toLocaleString()} registros • Cargado: ${uploaded}</p>
      </div>
      <div class="dataset-actions">
        <button class="btn-text">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          Descargar
        </button>
        <button class="btn-text">Ver Detalles</button>
      </div>
    </div>
  `;
}

export function initIAConfiguration(): void {
  // Initialize AI Assistant
  initAIAssistant();

  // File upload
  const btnSelectFile = document.getElementById('btnSelectFile');
  const fileInput = document.getElementById('fileInput') as HTMLInputElement;
  const uploadBox = document.getElementById('uploadBox');
  const uploadText = uploadBox?.querySelector('.upload-text span');

  btnSelectFile?.addEventListener('click', () => {
    fileInput?.click();
  });

  fileInput?.addEventListener('change', (e) => {
    const files = (e.target as HTMLInputElement).files;
    if (files && files.length > 0) {
      const file = files[0];
      if (uploadText) {
        uploadText.textContent = file.name;
      }
      console.log('Archivo seleccionado:', file.name);
      // Here you would handle the file upload
      alert(`Archivo "${file.name}" listo para cargar`);
    }
  });

  // Upload dataset button
  const btnUploadDataset = document.getElementById('btnUploadDataset');
  btnUploadDataset?.addEventListener('click', () => {
    const uploadSection = document.querySelector('.upload-section');
    uploadSection?.scrollIntoView({ behavior: 'smooth' });
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
