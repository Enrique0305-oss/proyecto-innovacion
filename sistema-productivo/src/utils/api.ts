// Configuración centralizada de la API
export const API_URL = 'http://127.0.0.1:5000/api';

interface LoginResponse {
  access_token: string;
  user: {
    id: number;
    email: string;
    full_name: string;
    role: {
      id: number;
      name: string;
      permissions: string[];
    };
  };
}

interface ApiError {
  error: string;
  message?: string;
}

class ApiService {
  private handleUnauthorized(): void {
    // Limpiar sesión y redirigir al login
    this.logout();
    window.location.hash = '#login';
  }

  private async handleResponse(response: Response): Promise<any> {
    // Si es 401, redirigir al login
    if (response.status === 401) {
      this.handleUnauthorized();
      throw new Error('Sesión expirada. Por favor, inicia sesión nuevamente.');
    }

    if (!response.ok) {
      let errorMessage = 'Error en la solicitud';
      try {
        const error: ApiError = await response.json();
        errorMessage = error.error || error.message || errorMessage;
      } catch {
        errorMessage = `Error ${response.status}: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al iniciar sesión');
    }

    const data: LoginResponse = await response.json();
    
    // Guardar token y datos de usuario
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    localStorage.setItem('isAuthenticated', 'true');
    
    return data;
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    localStorage.removeItem('isAuthenticated');
  }

  getUser(): any {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  // Tasks endpoints
  async getTasks(filters?: any) {
    const params = new URLSearchParams(filters).toString();
    const url = params ? `${API_URL}/tasks?${params}` : `${API_URL}/tasks`;
    
    const response = await fetch(url, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    return this.handleResponse(response);
  }

  async createTask(task: any) {
    const response = await fetch(`${API_URL}/tasks`, {
      method: 'POST',
      mode: 'cors',
      headers: this.getHeaders(),
      body: JSON.stringify(task),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al crear tarea');
    }

    return response.json();
  }

  async updateTask(id: number, task: any) {
    const response = await fetch(`${API_URL}/tasks/${id}`, {
      method: 'PUT',
      mode: 'cors',
      headers: this.getHeaders(),
      body: JSON.stringify(task),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al actualizar tarea');
    }

    return response.json();
  }

  async deleteTask(id: number) {
    const response = await fetch(`${API_URL}/tasks/${id}`, {
      method: 'DELETE',
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Error al eliminar tarea');
    }

    return response.json();
  }

  async getTaskStats() {
    const response = await fetch(`${API_URL}/tasks/stats`, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    return this.handleResponse(response);
  }

  // People endpoints
  async getPeople(filters?: any) {
    const params = filters ? new URLSearchParams(filters).toString() : '';
    const url = params ? `${API_URL}/persons?${params}` : `${API_URL}/persons`;
    
    const response = await fetch(url, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    return this.handleResponse(response);
  }

  // Areas endpoints
  async getAreas(status?: string) {
    const url = status ? `${API_URL}/areas?status=${status}` : `${API_URL}/areas`;
    
    const response = await fetch(url, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    return this.handleResponse(response);
  }

  async createArea(area: any) {
    const response = await fetch(`${API_URL}/areas`, {
      method: 'POST',
      mode: 'cors',
      headers: this.getHeaders(),
      body: JSON.stringify(area),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al crear área');
    }

    return response.json();
  }

  async updateArea(id: number, area: any) {
    const response = await fetch(`${API_URL}/areas/${id}`, {
      method: 'PUT',
      mode: 'cors',
      headers: this.getHeaders(),
      body: JSON.stringify(area),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al actualizar área');
    }

    return response.json();
  }

  async deleteArea(id: number) {
    const response = await fetch(`${API_URL}/areas/${id}`, {
      method: 'DELETE',
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al eliminar área');
    }

    return response.json();
  }

  // Users endpoints
  async getUsers(filters?: any) {
    const params = new URLSearchParams(filters).toString();
    const url = params ? `${API_URL}/users?${params}` : `${API_URL}/users`;
    
    const response = await fetch(url, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    return this.handleResponse(response);
  }

  async updateUser(id: number, userData: any) {
    const response = await fetch(`${API_URL}/users/${id}`, {
      method: 'PUT',
      mode: 'cors',
      headers: this.getHeaders(),
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al actualizar usuario');
    }

    return response.json();
  }

  async deleteUser(id: number) {
    const response = await fetch(`${API_URL}/users/${id}`, {
      method: 'DELETE',
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al eliminar usuario');
    }

    return response.json();
  }

  // Roles endpoints
  async getRoles() {
    const response = await fetch(`${API_URL}/users/roles`, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    return this.handleResponse(response);
  }

  // ============================================================================
  // ML Endpoints - Machine Learning
  // ============================================================================

  /**
   * Predecir riesgo de una tarea usando modelo CatBoost
   */
  async predictRisk(taskData: {
    complexity_level: string;
    priority: string;
    area: string;
    task_type: string;
    duration_est: number;
    assignees_count: number;
    dependencies: number;
  }) {
    const response = await fetch(`${API_URL}/ml/prediccion-riesgo`, {
      method: 'POST',
      mode: 'cors',
      headers: this.getHeaders(),
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al predecir riesgo');
    }

    return response.json();
  }

  /**
   * Obtener información del modelo actual
   */
  async getModelInfo() {
    const response = await fetch(`${API_URL}/ml/model/info`, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al obtener info del modelo');
    }

    return response.json();
  }

  /**
   * Reentrenar modelo (solo super_admin)
   */
  async retrainModel(config?: {
    use_optuna?: boolean;
    n_trials?: number;
  }) {
    const response = await fetch(`${API_URL}/ml/model/train`, {
      method: 'POST',
      mode: 'cors',
      headers: this.getHeaders(),
      body: JSON.stringify(config || {}),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al reentrenar modelo');
    }

    return response.json();
  }

  /**
   * Obtener métricas del modelo
   */
  async getModelMetrics() {
    const response = await fetch(`${API_URL}/ml/model/metrics`, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al obtener métricas');
    }

    return response.json();
  }

  /**
   * Obtener URL de imagen de métrica
   */
  getMetricImageUrl(type: 'confusion_matrix' | 'feature_importance'): string {
    const token = localStorage.getItem('access_token');
    return `${API_URL}/ml/model/metrics/image/${type}?token=${token}`;
  }

  /**
   * Obtener configuración del modelo
   */
  async getModelConfig() {
    const response = await fetch(`${API_URL}/ml/model/config`, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al obtener configuración');
    }

    return response.json();
  }

  /**
   * Vista previa de datos de entrenamiento (solo super_admin)
   */
  async getTrainingDataPreview(limit: number = 10) {
    const response = await fetch(`${API_URL}/ml/data/preview?limit=${limit}`, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error || 'Error al obtener datos');
    }

    return response.json();
  }
}

export const api = new ApiService();

// Exportar función helper para obtener headers de autenticación
export function getAuthHeaders(): HeadersInit {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  const token = localStorage.getItem('access_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
}
