const API_URL = 'http://127.0.0.1:5000/api';

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

    if (!response.ok) {
      throw new Error('Error al obtener tareas');
    }

    return response.json();
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

    if (!response.ok) {
      throw new Error('Error al obtener estadísticas');
    }

    return response.json();
  }

  // Areas endpoints
  async getAreas(status?: string) {
    const url = status ? `${API_URL}/areas?status=${status}` : `${API_URL}/areas`;
    
    const response = await fetch(url, {
      mode: 'cors',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Error al obtener áreas');
    }

    return response.json();
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

    if (!response.ok) {
      throw new Error('Error al obtener usuarios');
    }

    return response.json();
  }
}

export const api = new ApiService();
