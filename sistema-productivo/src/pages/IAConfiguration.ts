/**
 * Configuración de IA - Gestión de reentrenamiento de modelos
 */
import '../styles/ia-configuration.css';
import { Sidebar, initSidebar } from '../components/Sidebar';
import { API_URL } from '../utils/api';

let models: any[] = [];
let jobs: any[] = [];
let schedules: any[] = [];
let selectedModel: any = null;
let pollingInterval: number | null = null;

export function IAConfigurationPage(): string {
    return `
        <div class="dashboard-layout">
            ${Sidebar('configuracion-ia')}
            <main class="dashboard-main">
                <div class="ia-config-container">
                    <div class="ia-config-header">
                        <h1>Configuración de Inteligencia Artificial</h1>
                        <p>Gestiona el reentrenamiento y programación de modelos de Machine Learning</p>
                    </div>

                    <div class="ia-config-tabs">
                        <button class="tab-btn active" data-view="models">Estado de Modelos</button>
                        <button class="tab-btn" data-view="retrain">Reentrenamiento</button>
                        <button class="tab-btn" data-view="schedules">Programaciones</button>
                        <button class="tab-btn" data-view="history">Historial</button>
                    </div>

                    <div class="ia-config-content">
                        <div id="models-view" class="view-section active"></div>
                        <div id="retrain-view" class="view-section"></div>
                        <div id="schedules-view" class="view-section"></div>
                        <div id="history-view" class="view-section"></div>
                    </div>
                </div>
            </main>
        </div>
    `;
}

export function initIAConfiguration() {
    initSidebar();
    
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    // Tab switching
    container.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.getAttribute('data-view');
            switchView(view as string);
        });
    });
    
    // Inicializar vista de modelos
    renderModelsView();
}

function switchView(view: string) {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    container.querySelector(`[data-view="${view}"]`)?.classList.add('active');
    
    container.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
    container.querySelector(`#${view}-view`)?.classList.add('active');

    switch(view) {
        case 'models': renderModelsView(); break;
        case 'retrain': renderRetrainView(); break;
        case 'schedules': renderSchedulesView(); break;
        case 'history': renderHistoryView(); break;
    }
}

// MODELS VIEW
function renderModelsView() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const view = container.querySelector('#models-view');
    if (!view) return;
    
    view.innerHTML = `
        <div class="stats-section">
            <h3>Datos Disponibles</h3>
            <div id="stats-grid"></div>
        </div>
        <div id="models-grid" style="display: grid !important; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)) !important; gap: 20px !important; width: 100% !important;"></div>
    `;
    
    loadModels();
    loadStats();
}

async function loadModels() {
    try {
        const res = await fetch(`${API_URL}/ml/training/models`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        models = await res.json();
        displayModels();
    } catch (err) {
        console.error('Error loading models:', err);
        const container = document.querySelector('.ia-config-container');
        const grid = container?.querySelector('#models-grid');
        if (grid) {
            grid.innerHTML = '<div class="alert error">Error al cargar modelos. Verifica que el backend esté corriendo.</div>';
        }
    }
}

async function loadStats() {
    try {
        const res = await fetch(`${API_URL}/ml/training/data-stats`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const stats = await res.json();
        displayStats(stats);
    } catch (err) {
        console.error('Error loading stats:', err);
        const container = document.querySelector('.ia-config-container');
        const grid = container?.querySelector('#stats-grid');
        if (grid) {
            grid.innerHTML = '<div class="alert error">Error al cargar estadísticas</div>';
        }
    }
}

function displayStats(stats: any) {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const grid = container.querySelector('#stats-grid');
    if (!grid) return;
    
    const tasks = stats.tasks?.with_actual_hours || 0;
    grid.innerHTML = `
        <div class="stat-card">
            <div class="stat-icon"></div>
            <div class="stat-value">${tasks}</div>
            <div class="stat-label">Tareas con horas reales</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"></div>
            <div class="stat-value">${stats.users || 0}</div>
            <div class="stat-label">Usuarios activos</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"></div>
            <div class="stat-value">${stats.predictions || 0}</div>
            <div class="stat-label">Predicciones guardadas</div>
        </div>
    `;
}

function displayModels() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const grid = container.querySelector('#models-grid') as HTMLElement;
    if (!grid) return;
    
    grid.innerHTML = models.map(m => `
        <div class="model-card-horizontal ${m.needs_retraining ? 'needs-training' : ''}">
            <div class="model-main-info">
                <div class="model-title-section">
                    <span class="status-indicator ${m.status}"></span>
                    <div>
                        <h3>${m.name}</h3>
                        <span class="model-type">${m.type}</span>
                    </div>
                </div>
                <span class="version-badge">${m.version}</span>
            </div>
            
            <div class="model-details-row">
                <div class="detail-item">
                    <span class="detail-label">Algoritmo</span>
                    <span class="detail-value">${m.algorithm || 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Precisión</span>
                    <span class="detail-value">${m.precision?.toFixed(2) || 'N/A'}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Muestras</span>
                    <span class="detail-value">${m.samples_count || 0}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Último entrenamiento</span>
                    <span class="detail-value">${m.days_since_training !== null ? `Hace ${m.days_since_training} días` : 'Nunca'}</span>
                </div>
            </div>
            
            <div class="model-actions">
                ${m.needs_retraining ? '<span class="retrain-badge">Reentrenamiento recomendado</span>' : ''}
                <button class="btn btn-primary btn-sm" onclick="window.iaConfig.retrain(${m.id})">
                    Reentrenar Modelo
                </button>
            </div>
        </div>
    `).join('');
}

// RETRAIN VIEW
function renderRetrainView() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const view = container.querySelector('#retrain-view');
    if (!view) return;
    
    view.innerHTML = `
        <h3>Reentrenamiento Manual</h3>
        <div class="form-group">
            <label>Modelo:</label>
            <select id="model-select" class="form-control">
                <option value="">-- Selecciona un modelo --</option>
                ${models.map(m => `<option value="${m.id}">${m.name} (${m.type})</option>`).join('')}
            </select>
        </div>
        <div id="retrain-config" style="display:none;">
            <div class="form-row">
                <div class="form-group">
                    <label>Desde (opcional):</label>
                    <input type="date" id="date-from" class="form-control">
                </div>
                <div class="form-group">
                    <label>Hasta (opcional):</label>
                    <input type="date" id="date-to" class="form-control">
                </div>
            </div>
            <div id="dataset-preview"></div>
            <button id="gen-dataset-btn" class="btn btn-secondary">Generar Dataset</button>
            <button id="start-train-btn" class="btn btn-primary" disabled>Iniciar Entrenamiento</button>
        </div>
        <div id="training-progress" style="display:none;"></div>
    `;

    view.querySelector('#model-select')?.addEventListener('change', (e: any) => {
        if (e.target.value) {
            selectedModel = models.find(m => m.id === parseInt(e.target.value));
            const config = view.querySelector('#retrain-config') as HTMLElement;
            if (config) config.style.display = 'block';
        }
    });

    view.querySelector('#gen-dataset-btn')?.addEventListener('click', generateDataset);
    view.querySelector('#start-train-btn')?.addEventListener('click', startTraining);
}

async function generateDataset() {
    if (!selectedModel) return;
    
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const dateFrom = (container.querySelector('#date-from') as HTMLInputElement)?.value || '';
    const dateTo = (container.querySelector('#date-to') as HTMLInputElement)?.value || '';

    try {
        const res = await fetch(`${API_URL}/ml/training/datasets/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                model_type: selectedModel.type,
                date_from: dateFrom || null,
                date_to: dateTo || null
            })
        });

        const data = await res.json();
        const preview = container.querySelector('#dataset-preview');
        if (preview) {
            preview.innerHTML = `
                <div class="alert success">
                    Dataset generado: ${data.dataset.record_count} registros
                </div>
            `;
        }

        const btn = container.querySelector('#start-train-btn') as HTMLButtonElement;
        if (btn) {
            btn.disabled = false;
            btn.dataset.datasetId = data.dataset.id;
        }
    } catch (err: any) {
        alert('Error: ' + err.message);
    }
}

async function startTraining() {
    if (!selectedModel) return;
    
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const btn = container.querySelector('#start-train-btn') as HTMLButtonElement;
    if (!btn) return;

    try {
        const res = await fetch(`${API_URL}/ml/training/jobs`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                model_id: selectedModel.id,
                dataset_id: btn.dataset.datasetId ? parseInt(btn.dataset.datasetId) : null
            })
        });

        const data = await res.json();
        showProgress(data.job.id);
    } catch (err: any) {
        alert('Error: ' + err.message);
    }
}

function showProgress(jobId: number) {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const progress = container.querySelector('#training-progress') as HTMLElement;
    if (!progress) return;
    
    progress.style.display = 'block';
    progress.innerHTML = `
        <div class="progress-card">
            <h4>Job #${jobId} en progreso</h4>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width:0%"></div>
            </div>
            <div id="progress-info">0% - Inicializando...</div>
            <div id="progress-result"></div>
        </div>
    `;

    pollingInterval = setInterval(async () => {
        try {
            const res = await fetch(`${API_URL}/ml/training/jobs/${jobId}`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
            });
            const job = await res.json();
            
            const fill = container.querySelector('#progress-fill') as HTMLElement;
            const info = container.querySelector('#progress-info');
            if (fill && info) {
                fill.style.width = `${job.progress}%`;
                info.textContent = `${job.progress}% - ${job.current_step || 'Procesando...'}`;
            }

            if (job.status === 'completed' || job.status === 'failed') {
                if (pollingInterval) clearInterval(pollingInterval);
                showResult(job);
            }
        } catch (err) {
            console.error('Polling error:', err);
        }
    }, 2000);
}

function showResult(job: any) {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const result = container.querySelector('#progress-result');
    if (!result) return;
    
    if (job.status === 'completed') {
        const comp = job.metrics?.comparison;
        result.innerHTML = `
            <div class="alert ${comp?.should_replace ? 'success' : 'warning'}">
                ${comp?.reason || 'Completado'}
            </div>
        `;
    } else {
        result.innerHTML = `<div class="alert error">${job.error_message}</div>`;
    }
}

// SCHEDULES VIEW
function renderSchedulesView() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const view = container.querySelector('#schedules-view');
    if (!view) return;
    
    view.innerHTML = `
        <div class="schedules-header">
            <h3>Programaciones</h3>
            <button id="new-schedule-btn" class="btn btn-primary">Nueva Programación</button>
        </div>
        <div id="schedules-list"></div>
        <div id="schedule-modal" class="modal" style="display:none;">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h3>Nueva Programación</h3>
                <div class="form-group">
                    <label>Modelo:</label>
                    <select id="sched-type" class="form-control">
                        <option value="risk">Riesgo</option>
                        <option value="duration">Duración</option>
                        <option value="recommendation">Recomendación</option>
                        <option value="simulation">Simulación</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Frecuencia:</label>
                    <select id="sched-pattern" class="form-control">
                        <option value="daily">Diaria</option>
                        <option value="weekly">Semanal</option>
                        <option value="monthly">Mensual</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Hora:</label>
                    <input type="time" id="sched-time" class="form-control" value="02:00">
                </div>
                <button id="save-sched-btn" class="btn btn-primary">Guardar</button>
            </div>
        </div>
    `;

    loadSchedules();

    view.querySelector('#new-schedule-btn')?.addEventListener('click', () => {
        const modal = view.querySelector('#schedule-modal') as HTMLElement;
        if (modal) modal.style.display = 'flex';
    });
    
    view.querySelector('.close')?.addEventListener('click', () => {
        const modal = view.querySelector('#schedule-modal') as HTMLElement;
        if (modal) modal.style.display = 'none';
    });

    view.querySelector('#save-sched-btn')?.addEventListener('click', saveSchedule);
}

async function loadSchedules() {
    try {
        const res = await fetch(`${API_URL}/ml/training/schedules`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        schedules = await res.json();
        displaySchedules();
    } catch (err) {
        console.error('Error loading schedules:', err);
        const container = document.querySelector('.ia-config-container');
        const list = container?.querySelector('#schedules-list');
        if (list) {
            list.innerHTML = '<div class="alert error">Error al cargar programaciones</div>';
        }
    }
}

function displaySchedules() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const list = container.querySelector('#schedules-list');
    if (!list) return;
    
    if (schedules.length === 0) {
        list.innerHTML = '<div class="empty">No hay programaciones</div>';
        return;
    }
    list.innerHTML = schedules.map(s => `
        <div class="schedule-card">
            <h4>${s.model_type}</h4>
            <p>${s.recurrence_pattern} a las ${s.scheduled_time}</p>
            ${s.last_execution ? `<p>Última ejecución: ${new Date(s.last_execution).toLocaleString()}</p>` : ''}
            <button class="btn btn-sm btn-danger" onclick="window.iaConfig.deleteSched(${s.id})">
                Eliminar
            </button>
        </div>
    `).join('');
}

async function saveSchedule() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const type = (container.querySelector('#sched-type') as HTMLSelectElement)?.value;
    const pattern = (container.querySelector('#sched-pattern') as HTMLSelectElement)?.value;
    const time = (container.querySelector('#sched-time') as HTMLInputElement)?.value;

    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);

    try {
        await fetch(`${API_URL}/ml/training/schedules`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                model_type: type,
                scheduled_date: tomorrow.toISOString().split('T')[0],
                scheduled_time: time,
                is_recurring: true,
                recurrence_pattern: pattern
            })
        });

        const modal = container.querySelector('#schedule-modal') as HTMLElement;
        if (modal) modal.style.display = 'none';
        loadSchedules();
    } catch (err) {
        alert('Error guardando programación');
    }
}

async function deleteSchedule(id: number) {
    if (!confirm('¿Eliminar programación?')) return;
    try {
        await fetch(`${API_URL}/ml/training/schedules/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        loadSchedules();
    } catch (err) {
        alert('Error eliminando');
    }
}

// HISTORY VIEW
function renderHistoryView() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const view = container.querySelector('#history-view');
    if (!view) return;
    
    view.innerHTML = `
        <h3>Historial de Entrenamientos</h3>
        <div id="history-list"></div>
    `;
    loadHistory();
}

async function loadHistory() {
    try {
        const res = await fetch(`${API_URL}/ml/training/jobs?limit=20`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        jobs = await res.json();
        displayHistory();
    } catch (err) {
        console.error('Error loading history:', err);
        const container = document.querySelector('.ia-config-container');
        const list = container?.querySelector('#history-list');
        if (list) {
            list.innerHTML = '<div class="alert error">Error al cargar historial</div>';
        }
    }
}

function displayHistory() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const list = container.querySelector('#history-list');
    if (!list) return;
    
    if (jobs.length === 0) {
        list.innerHTML = '<div class="empty">No hay entrenamientos</div>';
        return;
    }
    list.innerHTML = jobs.map(j => `
        <div class="job-card status-${j.status}">
            <div class="job-header">
                <span>#${j.id}</span>
                <span class="status">${j.status}</span>
            </div>
            <h4>${j.job_name}</h4>
            <p>${new Date(j.created_at).toLocaleString()}</p>
            ${j.duration_seconds ? `<p>Duración: ${j.duration_seconds}s</p>` : ''}
            ${j.error_message ? `<p class="error">${j.error_message}</p>` : ''}
        </div>
    `).join('');
}

// Global functions
(window as any).iaConfig = {
    retrain: (id: number) => {
        selectedModel = models.find(m => m.id === id);
        switchView('retrain');
        const select = document.querySelector('#model-select') as HTMLSelectElement;
        const config = document.querySelector('#retrain-config') as HTMLElement;
        if (select && config) {
            select.value = id.toString();
            config.style.display = 'block';
        }
    },
    deleteSched: deleteSchedule
};
