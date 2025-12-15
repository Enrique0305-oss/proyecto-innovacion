import { API_URL, getAuthHeaders } from '../utils/api';

interface TrainingSchedule {
    id?: number;
    model_type: string;
    scheduled_date: string;
    scheduled_time: string;
    status: string;
    parameters?: string;
    last_execution?: string;
    execution_result?: string;
    created_by?: number;
    created_at?: string;
    updated_at?: string;
    is_recurring: boolean;
    recurrence_pattern?: string;
}

interface ModelType {
    value: string;
    label: string;
}

let schedules: TrainingSchedule[] = [];
let modelTypes: ModelType[] = [];
let currentEditingSchedule: TrainingSchedule | null = null;

export function RetrainIA() {
    const container = document.createElement('div');
    container.className = 'retrain-ia-container';
    container.innerHTML = `
        <div class="retrain-ia-header">
            <h1>🤖 Reentrenamiento de IA</h1>
            <button id="btnNewSchedule" class="btn btn-primary">
                <i class="fas fa-plus"></i> Programar Reentrenamiento
            </button>
        </div>

        <div class="filters-section">
            <div class="filter-group">
                <label for="filterModel">Modelo:</label>
                <select id="filterModel" class="form-control">
                    <option value="">Todos los modelos</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="filterStatus">Estado:</label>
                <select id="filterStatus" class="form-control">
                    <option value="">Todos los estados</option>
                    <option value="programado">Programado</option>
                    <option value="ejecutando">Ejecutando</option>
                    <option value="completado">Completado</option>
                    <option value="fallido">Fallido</option>
                </select>
            </div>
            <button id="btnApplyFilters" class="btn btn-secondary">Aplicar Filtros</button>
        </div>

        <div class="schedules-grid" id="schedulesGrid">
            <div class="loading">Cargando programaciones...</div>
        </div>

        <!-- Modal para crear/editar programación -->
        <div id="scheduleModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 id="modalTitle">Nueva Programación</h2>
                    <span class="close">&times;</span>
                </div>
                <div class="modal-body">
                    <form id="scheduleForm">
                        <div class="form-group">
                            <label for="modelType">Modelo *</label>
                            <select id="modelType" class="form-control" required>
                                <option value="">Seleccionar modelo</option>
                            </select>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label for="scheduledDate">Fecha *</label>
                                <input type="date" id="scheduledDate" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label for="scheduledTime">Hora *</label>
                                <input type="time" id="scheduledTime" class="form-control" required>
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="isRecurring">
                                Reentrenamiento Recurrente
                            </label>
                        </div>

                        <div class="form-group" id="recurrenceGroup" style="display: none;">
                            <label for="recurrencePattern">Patrón de Recurrencia</label>
                            <select id="recurrencePattern" class="form-control">
                                <option value="">Seleccionar patrón</option>
                                <option value="daily">Diario</option>
                                <option value="weekly">Semanal</option>
                                <option value="monthly">Mensual</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="parameters">Parámetros (JSON)</label>
                            <textarea id="parameters" class="form-control" rows="4" 
                                placeholder='{"epochs": 100, "batch_size": 32}'></textarea>
                            <small class="form-text">Opcional: parámetros adicionales en formato JSON</small>
                        </div>

                        <div class="modal-actions">
                            <button type="button" class="btn btn-secondary" id="btnCancelSchedule">Cancelar</button>
                            <button type="submit" class="btn btn-primary">Guardar Programación</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;

    // Event listeners
    setTimeout(() => {
        setupEventListeners();
        loadModelTypes();
        loadSchedules();
    }, 0);

    return container;
}

function setupEventListeners() {
    const btnNewSchedule = document.getElementById('btnNewSchedule');
    const modal = document.getElementById('scheduleModal');
    const closeBtn = modal?.querySelector('.close');
    const scheduleForm = document.getElementById('scheduleForm') as HTMLFormElement;
    const btnCancel = document.getElementById('btnCancelSchedule');
    const isRecurringCheckbox = document.getElementById('isRecurring') as HTMLInputElement;
    const btnApplyFilters = document.getElementById('btnApplyFilters');

    btnNewSchedule?.addEventListener('click', openNewScheduleModal);
    closeBtn?.addEventListener('click', closeModal);
    btnCancel?.addEventListener('click', closeModal);
    scheduleForm?.addEventListener('submit', handleSubmitSchedule);
    btnApplyFilters?.addEventListener('click', applyFilters);

    isRecurringCheckbox?.addEventListener('change', (e) => {
        const recurrenceGroup = document.getElementById('recurrenceGroup');
        if (recurrenceGroup) {
            recurrenceGroup.style.display = (e.target as HTMLInputElement).checked ? 'block' : 'none';
        }
    });

    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });
}

async function loadModelTypes() {
    try {
        const response = await fetch(`${API_URL}/training-schedules/model-types`, {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            modelTypes = await response.json();
            populateModelTypeSelects();
        }
    } catch (error) {
        console.error('Error al cargar tipos de modelos:', error);
    }
}

function populateModelTypeSelects() {
    const modelTypeSelect = document.getElementById('modelType') as HTMLSelectElement;
    const filterModelSelect = document.getElementById('filterModel') as HTMLSelectElement;

    modelTypes.forEach(modelType => {
        const option1 = document.createElement('option');
        option1.value = modelType.value;
        option1.textContent = modelType.label;
        modelTypeSelect?.appendChild(option1);

        const option2 = document.createElement('option');
        option2.value = modelType.value;
        option2.textContent = modelType.label;
        filterModelSelect?.appendChild(option2);
    });
}

async function loadSchedules() {
    const grid = document.getElementById('schedulesGrid');
    if (!grid) return;

    grid.innerHTML = '<div class="loading">Cargando programaciones...</div>';

    try {
        const response = await fetch(`${API_URL}/training-schedules`, {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            schedules = await response.json();
            renderSchedules(schedules);
        } else {
            grid.innerHTML = '<div class="error">Error al cargar programaciones</div>';
        }
    } catch (error) {
        console.error('Error:', error);
        grid.innerHTML = '<div class="error">Error de conexión</div>';
    }
}

function renderSchedules(schedulesToRender: TrainingSchedule[]) {
    const grid = document.getElementById('schedulesGrid');
    if (!grid) return;

    if (schedulesToRender.length === 0) {
        grid.innerHTML = '<div class="empty-state">No hay programaciones registradas</div>';
        return;
    }

    grid.innerHTML = schedulesToRender.map(schedule => {
        const modelType = modelTypes.find(mt => mt.value === schedule.model_type);
        const statusClass = `status-${schedule.status}`;
        const statusIcon = getStatusIcon(schedule.status);

        return `
            <div class="schedule-card ${statusClass}">
                <div class="schedule-header">
                    <h3>${modelType?.label || schedule.model_type}</h3>
                    <span class="status-badge ${statusClass}">
                        ${statusIcon} ${schedule.status}
                    </span>
                </div>
                <div class="schedule-body">
                    <div class="schedule-info">
                        <i class="fas fa-calendar"></i>
                        <span>${formatDate(schedule.scheduled_date)}</span>
                    </div>
                    <div class="schedule-info">
                        <i class="fas fa-clock"></i>
                        <span>${schedule.scheduled_time}</span>
                    </div>
                    ${schedule.is_recurring ? `
                        <div class="schedule-info recurring">
                            <i class="fas fa-sync-alt"></i>
                            <span>Recurrente: ${formatRecurrence(schedule.recurrence_pattern)}</span>
                        </div>
                    ` : ''}
                    ${schedule.last_execution ? `
                        <div class="schedule-info">
                            <i class="fas fa-history"></i>
                            <span>Última ejecución: ${formatDateTime(schedule.last_execution)}</span>
                        </div>
                    ` : ''}
                    ${schedule.execution_result ? `
                        <div class="execution-result">
                            <strong>Resultado:</strong>
                            <p>${schedule.execution_result}</p>
                        </div>
                    ` : ''}
                </div>
                <div class="schedule-actions">
                    <button class="btn-icon" onclick="window.editSchedule(${schedule.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-icon" onclick="window.executeSchedule(${schedule.id})" 
                        title="Ejecutar ahora" ${schedule.status === 'ejecutando' ? 'disabled' : ''}>
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="btn-icon btn-danger" onclick="window.deleteSchedule(${schedule.id})" title="Eliminar">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function getStatusIcon(status: string): string {
    const icons: { [key: string]: string } = {
        'programado': '📅',
        'ejecutando': '⚙️',
        'completado': '✅',
        'fallido': '❌'
    };
    return icons[status] || '❓';
}

function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
}

function formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES');
}

function formatRecurrence(pattern?: string): string {
    const patterns: { [key: string]: string } = {
        'daily': 'Diario',
        'weekly': 'Semanal',
        'monthly': 'Mensual'
    };
    return patterns[pattern || ''] || pattern || '';
}

function openNewScheduleModal() {
    currentEditingSchedule = null;
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('scheduleForm') as HTMLFormElement;
    
    if (modalTitle) modalTitle.textContent = 'Nueva Programación';
    form?.reset();
    
    // Establecer fecha mínima como hoy
    const dateInput = document.getElementById('scheduledDate') as HTMLInputElement;
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;
    }
    
    const modal = document.getElementById('scheduleModal');
    if (modal) modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('scheduleModal');
    if (modal) modal.style.display = 'none';
    currentEditingSchedule = null;
}

async function handleSubmitSchedule(e: Event) {
    e.preventDefault();
    
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);
    
    const scheduleData: any = {
        model_type: (document.getElementById('modelType') as HTMLSelectElement).value,
        scheduled_date: (document.getElementById('scheduledDate') as HTMLInputElement).value,
        scheduled_time: (document.getElementById('scheduledTime') as HTMLInputElement).value,
        is_recurring: (document.getElementById('isRecurring') as HTMLInputElement).checked,
        recurrence_pattern: (document.getElementById('recurrencePattern') as HTMLSelectElement).value || null,
        parameters: (document.getElementById('parameters') as HTMLTextAreaElement).value || null
    };

    // Validar JSON de parámetros si se proporcionó
    if (scheduleData.parameters) {
        try {
            JSON.parse(scheduleData.parameters);
        } catch (error) {
            alert('El formato de parámetros JSON no es válido');
            return;
        }
    }

    try {
        const url = currentEditingSchedule 
            ? `${API_URL}/training-schedules/${currentEditingSchedule.id}`
            : `${API_URL}/training-schedules`;
        
        const method = currentEditingSchedule ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method,
            headers: {
                ...getAuthHeaders(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(scheduleData)
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message || 'Programación guardada exitosamente');
            closeModal();
            loadSchedules();
        } else {
            alert(data.error || 'Error al guardar la programación');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión al guardar la programación');
    }
}

// Funciones globales para los botones
(window as any).editSchedule = async function(scheduleId: number) {
    const schedule = schedules.find(s => s.id === scheduleId);
    if (!schedule) return;

    currentEditingSchedule = schedule;
    const modalTitle = document.getElementById('modalTitle');
    if (modalTitle) modalTitle.textContent = 'Editar Programación';

    // Llenar el formulario con los datos
    (document.getElementById('modelType') as HTMLSelectElement).value = schedule.model_type;
    (document.getElementById('scheduledDate') as HTMLInputElement).value = schedule.scheduled_date;
    (document.getElementById('scheduledTime') as HTMLInputElement).value = schedule.scheduled_time;
    (document.getElementById('isRecurring') as HTMLInputElement).checked = schedule.is_recurring;
    
    const recurrenceGroup = document.getElementById('recurrenceGroup');
    if (recurrenceGroup) {
        recurrenceGroup.style.display = schedule.is_recurring ? 'block' : 'none';
    }
    
    if (schedule.recurrence_pattern) {
        (document.getElementById('recurrencePattern') as HTMLSelectElement).value = schedule.recurrence_pattern;
    }
    
    if (schedule.parameters) {
        (document.getElementById('parameters') as HTMLTextAreaElement).value = schedule.parameters;
    }

    const modal = document.getElementById('scheduleModal');
    if (modal) modal.style.display = 'block';
};

(window as any).executeSchedule = async function(scheduleId: number) {
    if (!confirm('¿Deseas ejecutar este reentrenamiento ahora?')) return;

    try {
        const response = await fetch(`${API_URL}/training-schedules/${scheduleId}/execute`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message || 'Ejecución iniciada');
            loadSchedules();
        } else {
            alert(data.error || 'Error al ejecutar');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
};

(window as any).deleteSchedule = async function(scheduleId: number) {
    if (!confirm('¿Estás seguro de eliminar esta programación?')) return;

    try {
        const response = await fetch(`${API_URL}/training-schedules/${scheduleId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message || 'Programación eliminada');
            loadSchedules();
        } else {
            alert(data.error || 'Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
};

function applyFilters() {
    const filterModel = (document.getElementById('filterModel') as HTMLSelectElement).value;
    const filterStatus = (document.getElementById('filterStatus') as HTMLSelectElement).value;

    let filtered = schedules;

    if (filterModel) {
        filtered = filtered.filter(s => s.model_type === filterModel);
    }

    if (filterStatus) {
        filtered = filtered.filter(s => s.status === filterStatus);
    }

    renderSchedules(filtered);
}
