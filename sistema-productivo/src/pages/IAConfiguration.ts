/**
 * Configuración de IA - Gestión de reentrenamiento de modelos
 */
import '../styles/ia-configuration.css';
import { Sidebar, initSidebar } from '../components/Sidebar';
import { API_URL } from '../utils/api';

let models: any[] = [];
let selectedModel: any = null;

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
                        <button class="tab-btn" data-view="retrain">Reentrenar Modelos</button>
                    </div>

                    <div class="ia-config-content">
                        <div id="models-view" class="view-section active"></div>
                        <div id="retrain-view" class="view-section"></div>
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
        btn.addEventListener('click', async () => {
            const view = btn.getAttribute('data-view');
            await switchView(view as string);
        });
    });
    
    // Inicializar vista de modelos
    renderModelsView();
}

async function switchView(view: string) {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    container.querySelector(`[data-view="${view}"]`)?.classList.add('active');
    
    container.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
    container.querySelector(`#${view}-view`)?.classList.add('active');

    switch(view) {
        case 'models': renderModelsView(); break;
        case 'retrain': await renderRetrainView(); break;
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
                <button class="btn btn-primary btn-sm" onclick="window.iaConfig.retrain('${m.type}', '${m.name}')">
                    Reentrenar Modelo
                </button>
            </div>
        </div>
    `).join('');
}

// RETRAIN VIEW
async function renderRetrainView() {
    const container = document.querySelector('.ia-config-container');
    if (!container) return;
    
    const view = container.querySelector('#retrain-view');
    if (!view) return;
    
    const today = new Date().toISOString().split('T')[0];
    
    // Renderizar estructura inicial
    view.innerHTML = `
        <h3>Reentrenamiento de Modelos</h3>
        <p class="description">Ejecuta el entrenamiento inmediatamente y programa entrenamientos automáticos futuros.</p>
        
        <div class="form-group">
            <label>Modelo a entrenar:</label>
            <select id="model-select" class="form-control">
                <option value="">Cargando modelos...</option>
            </select>
        </div>
        
        <div id="retrain-config" style="display:none;">
            <div class="form-group">
                <label>Día de entrenamiento:</label>
                <input type="date" id="training-date" class="form-control" value="${today}">
                <small class="help-text">Si seleccionas hoy: entrena inmediatamente. Si seleccionas una fecha futura: solo programa. Los entrenamientos se repetirán en este día del mes según la frecuencia.</small>
            </div>
            
            <div class="form-group">
                <label>Frecuencia de reentrenamiento automático:</label>
                <select id="frequency-select" class="form-control">
                    <option value="quarterly">Cada 3 meses</option>
                    <option value="biannual">Cada 6 meses</option>
                    <option value="annual">Cada año</option>
                </select>
                <small id="frequency-hint" class="help-text"></small>
            </div>
            
            <button id="start-train-btn" class="btn btn-primary btn-lg">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px;">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
                Ejecutar Entrenamiento
            </button>
            
            <div class="history-section">
                <h4>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 8px; vertical-align: middle;">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                        <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
                    </svg>
                    Historial de Entrenamientos
                </h4>
                <div id="model-history-list"></div>
            </div>
        </div>
        
        <div id="training-result" style="display:none;"></div>
    `;

    // Event listeners
    view.querySelector('#model-select')?.addEventListener('change', (e: any) => {
        if (e.target.value) {
            const option = e.target.options[e.target.selectedIndex];
            selectedModel = {
                type: e.target.value,
                name: option.dataset.name
            };
            const config = view.querySelector('#retrain-config') as HTMLElement;
            if (config) config.style.display = 'block';
            updateFrequencyHint();
            loadModelHistory(selectedModel.type);
        }
    });
    
    view.querySelector('#training-date')?.addEventListener('change', updateFrequencyHint);
    view.querySelector('#frequency-select')?.addEventListener('change', updateFrequencyHint);
    view.querySelector('#start-train-btn')?.addEventListener('click', executeTraining);
    
    // Cargar modelos si no están cargados
    if (models.length === 0) {
        await loadModels();
    }
    
    // Actualizar dropdown con modelos
    const modelSelect = view.querySelector('#model-select') as HTMLSelectElement;
    if (modelSelect) {
        if (models.length > 0) {
            modelSelect.innerHTML = `
                <option value="">-- Selecciona un modelo --</option>
                ${models.map(m => `<option value="${m.type}" data-name="${m.name}">${m.name}</option>`).join('')}
            `;
        } else {
            modelSelect.innerHTML = '<option value="">Error al cargar modelos</option>';
        }
    }
}

function updateFrequencyHint() {
    const dateInput = document.querySelector('#training-date') as HTMLInputElement;
    const frequencySelect = document.querySelector('#frequency-select') as HTMLSelectElement;
    const hint = document.querySelector('#frequency-hint');
    
    if (!dateInput || !frequencySelect || !hint) return;
    
    const selectedDate = new Date(dateInput.value);
    const day = selectedDate.getDate();
    const monthName = selectedDate.toLocaleDateString('es', {month: 'long'});
    const frequency = frequencySelect.value;
    
    const calendarIcon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 4px; vertical-align: middle;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>';
    
    const hints: Record<string, string> = {
        'quarterly': `${calendarIcon}El modelo se reentrenará automáticamente el día ${day} de cada 3 meses (ej: ${day}/02, ${day}/05, ${day}/08, ${day}/11)`,
        'biannual': `${calendarIcon}El modelo se reentrenará automáticamente el día ${day} de cada 6 meses (ej: ${day}/02, ${day}/08)`,
        'annual': `${calendarIcon}El modelo se reentrenará automáticamente el día ${day} de ${monthName} cada año`
    };
    
    if (hint instanceof HTMLElement) {
        hint.innerHTML = hints[frequency] || '';
    }
}

async function executeTraining() {
    const modelType = selectedModel?.type;
    const modelName = selectedModel?.name;
    const trainingDate = (document.querySelector('#training-date') as HTMLInputElement)?.value;
    const frequency = (document.querySelector('#frequency-select') as HTMLSelectElement)?.value;
    
    if (!modelType || !trainingDate || !frequency) {
        alert('Por favor completa todos los campos');
        return;
    }
    
    const btn = document.querySelector('#start-train-btn') as HTMLButtonElement;
    const resultDiv = document.querySelector('#training-result') as HTMLElement;
    
    // Determinar si es hoy o futuro
    const selectedDate = new Date(trainingDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    selectedDate.setHours(0, 0, 0, 0);
    
    const isToday = selectedDate <= today;
    
    // Confirmar acción con mensaje apropiado
    let confirmMsg = '';
    if (isToday) {
        confirmMsg = `¿Iniciar entrenamiento del modelo "${modelName}" AHORA?\n\nEl entrenamiento se ejecutará inmediatamente (puede tardar varios minutos).\nLuego se programarán entrenamientos automáticos según la frecuencia seleccionada.`;
    } else {
        const dateStr = selectedDate.toLocaleDateString('es', { day: 'numeric', month: 'long', year: 'numeric' });
        confirmMsg = `¿Programar entrenamiento del modelo "${modelName}"?\n\nEl primer entrenamiento se ejecutará el ${dateStr}.\nLuego se repetirá automáticamente según la frecuencia seleccionada.\n\nNOTA: No se entrenará ahora, solo se programará.`;
    }
    
    if (!window.confirm(confirmMsg)) return;
    
    // Deshabilitar botón
    btn.disabled = true;
    resultDiv.style.display = 'block';
    
    if (isToday) {
        btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinning" style="margin-right: 6px;">
                <path d="M21 12a9 9 0 11-6.219-8.56"/>
            </svg>
            Entrenando modelo (puede tardar varios minutos)...
        `;
        resultDiv.innerHTML = `
            <div class="alert info">
                <div class="loading-spinner"></div>
                <p><strong>Ejecutando entrenamiento...</strong></p>
                <p>El modelo está siendo entrenado con los datos más recientes de la base de datos.</p>
                <p>Esto puede tardar entre 5 y 15 minutos dependiendo del modelo.</p>
                <p>Por favor, no cierres esta ventana.</p>
            </div>
        `;
    } else {
        btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinning" style="margin-right: 6px;">
                <path d="M21 12a9 9 0 11-6.219-8.56"/>
            </svg>
            Programando entrenamiento...
        `;
        resultDiv.innerHTML = `
            <div class="alert info">
                <div class="loading-spinner"></div>
                <p><strong>Programando entrenamiento futuro...</strong></p>
                <p>El modelo se entrenará automáticamente en la fecha programada.</p>
            </div>
        `;
    }
    
    try {
        const response = await fetch(`${API_URL}/ml/training/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                model_type: modelType,
                training_date: trainingDate,
                frequency: frequency
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Diferenciar entre ejecución inmediata y programación futura
            if (data.executed_now) {
                // Se ejecutó ahora
                resultDiv.innerHTML = `
                    <div class="alert success">
                        <h4>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px; vertical-align: middle;">
                                <polyline points="20 6 9 17 4 12"/>
                            </svg>
                            Entrenamiento Completado Exitosamente
                        </h4>
                        <p><strong>Modelo:</strong> ${modelName}</p>
                        <p><strong>Estado:</strong> ${data.message}</p>
                        <p><strong>Próxima ejecución automática:</strong> ${data.next_execution}</p>
                        <p><strong>ID del job programado:</strong> ${data.scheduled_job_id}</p>
                    </div>
                `;
            } else {
                // Solo se programó
                resultDiv.innerHTML = `
                    <div class="alert success">
                        <h4>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px; vertical-align: middle;">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                                <line x1="16" y1="2" x2="16" y2="6"/>
                                <line x1="8" y1="2" x2="8" y2="6"/>
                                <line x1="3" y1="10" x2="21" y2="10"/>
                            </svg>
                            Entrenamiento Programado
                        </h4>
                        <p><strong>Modelo:</strong> ${modelName}</p>
                        <p><strong>Estado:</strong> ${data.message}</p>
                        <p><strong>Primera ejecución:</strong> ${data.next_run || 'Programado'}</p>
                        <p><strong>Frecuencia:</strong> ${data.next_execution}</p>
                        <p><strong>ID del job:</strong> ${data.scheduled_job_id}</p>
                        <p class="help-text">El entrenamiento se ejecutará automáticamente en la fecha programada.</p>
                    </div>
                `;
            }
            
            // Solo recargar y cambiar vista si se ejecutó ahora
            if (data.executed_now) {
                // Recargar modelos para actualizar métricas
                await loadModels();
                
                // Recargar historial del modelo
                loadModelHistory(modelType);
                
                // Cambiar a vista de modelos después de 5 segundos
                setTimeout(async () => {
                    await switchView('models');
                }, 5000);
            } else {
                // Solo recargar historial si fue programado
                loadModelHistory(modelType);
                
                // Ocultar mensaje después de 8 segundos
                setTimeout(() => {
                    resultDiv.style.display = 'none';
                }, 8000);
            }
        } else {
            resultDiv.innerHTML = `
                <div class="alert error">
                    <h4>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px; vertical-align: middle;">
                            <circle cx="12" cy="12" r="10"/>
                            <line x1="15" y1="9" x2="9" y2="15"/>
                            <line x1="9" y1="9" x2="15" y2="15"/>
                        </svg>
                        Error en el Entrenamiento
                    </h4>
                    <p>${data.error || data.message}</p>
                    <p>Por favor, revisa los logs del backend para más detalles.</p>
                </div>
            `;
        }
    } catch (err: any) {
        resultDiv.innerHTML = `
            <div class="alert error">
                <h4>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px; vertical-align: middle;">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                    Error de Conexión
                </h4>
                <p>No se pudo conectar con el servidor.</p>
                <p>${err.message || err}</p>
            </div>
        `;
    } finally {
        btn.disabled = false;
        btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px;">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            Ejecutar Entrenamiento
        `;
    }
}

// ============================================================================
// HISTORIAL DE ENTRENAMIENTOS
// ============================================================================

async function loadModelHistory(modelType: string) {
    const historyList = document.querySelector('#model-history-list');
    if (!historyList) return;
    
    historyList.innerHTML = `
        <div class="loading">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinning" style="margin-right: 6px;">
                <path d="M21 12a9 9 0 11-6.219-8.56"/>
            </svg>
            Cargando historial...
        </div>
    `;
    
    try {
        const response = await fetch(`${API_URL}/ml/training/jobs?model_type=${modelType}&limit=10`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        if (!response.ok) {
            throw new Error('Error al cargar historial');
        }
        
        const jobs = await response.json();
        displayModelHistory(jobs);
    } catch (err) {
        console.error('Error loading model history:', err);
        historyList.innerHTML = '<div class="alert error">Error al cargar historial de entrenamientos</div>';
    }
}

function displayModelHistory(jobs: any[]) {
    const historyList = document.querySelector('#model-history-list');
    if (!historyList) return;
    
    if (jobs.length === 0) {
        historyList.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 8px; opacity: 0.4;">
                    <path d="M9 11l3 3L22 4"/>
                    <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
                </svg>
                <p>No hay entrenamientos registrados para este modelo</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = `
        <table class="history-table">
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Estado</th>
                    <th>Duración</th>
                    <th>Resultado</th>
                </tr>
            </thead>
            <tbody>
                ${jobs.map(job => {
                    const date = new Date(job.created_at);
                    const dateStr = date.toLocaleDateString('es', { 
                        year: 'numeric', 
                        month: 'short', 
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                    
                    const statusClass = job.status === 'completed' ? 'success' : 
                                       job.status === 'failed' ? 'error' : 
                                       job.status === 'running' ? 'running' : 'pending';
                    
                    const statusIcon = job.status === 'completed' ? 
                        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>' : 
                                      job.status === 'failed' ? 
                        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>' : 
                                      job.status === 'running' ? 
                        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinning"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>' : 
                        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';
                    
                    const duration = job.duration_seconds ? 
                        `${Math.floor(job.duration_seconds / 60)}m ${job.duration_seconds % 60}s` : 
                        '-';
                    
                    const result = job.status === 'completed' ? 
                        (job.metrics?.comparison?.reason || 'Completado') :
                        job.status === 'failed' ? 
                        (job.error_message || 'Error desconocido') : 
                        '-';
                    
                    return `
                        <tr class="history-row status-${statusClass}">
                            <td>${dateStr}</td>
                            <td><span class="status-badge ${statusClass}">${statusIcon} <span style="margin-left: 4px;">${job.status}</span></span></td>
                            <td>${duration}</td>
                            <td class="result-cell">${result}</td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
    `;
}

// ============================================================================
// FUNCIONES GLOBALES
// ============================================================================

// Función global para acceso desde HTML
(window as any).iaConfig = {
    retrain: async (modelType: string, modelName: string) => {
        selectedModel = { type: modelType, name: modelName };
        await switchView('retrain');
        
        // Pre-seleccionar modelo
        setTimeout(() => {
            const select = document.querySelector('#model-select') as HTMLSelectElement;
            const config = document.querySelector('#retrain-config') as HTMLElement;
            if (select && config) {
                select.value = modelType;
                config.style.display = 'block';
                updateFrequencyHint();
                loadModelHistory(modelType);
            }
        }, 100);
    }
};
