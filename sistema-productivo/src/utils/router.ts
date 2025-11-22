import { LoginPage, initLogin } from '../pages/Login';
import { DashboardPage, initDashboard } from '../pages/Dashboard';
import { TasksPage, initTasks } from '../pages/Tasks';
import { RiskClassificationPage, initRiskClassification } from '../pages/RiskClassification';
import { DurationPredictionPage, initDurationPrediction } from '../pages/DurationPrediction';

type Route = {
  path: string;
  render: () => string;
  init?: () => void;
  requiresAuth?: boolean;
};

const routes: Route[] = [
  {
    path: 'login',
    render: LoginPage,
    init: initLogin,
    requiresAuth: false
  },
  {
    path: 'dashboard',
    render: DashboardPage,
    init: initDashboard,
    requiresAuth: true
  },
  {
    path: 'tareas',
    render: TasksPage,
    init: initTasks,
    requiresAuth: true
  },
  {
    path: 'riesgo',
    render: RiskClassificationPage,
    init: initRiskClassification,
    requiresAuth: true
  },
  {
    path: 'duracion',
    render: DurationPredictionPage,
    init: initDurationPrediction,
    requiresAuth: true
  }
];

function isAuthenticated(): boolean {
  return localStorage.getItem('isAuthenticated') === 'true';
}

function getRoute(path: string): Route | undefined {
  return routes.find(route => route.path === path);
}

function getCurrentPath(): string {
  const hash = window.location.hash.slice(1);
  return hash || (isAuthenticated() ? 'dashboard' : 'login');
}

export function navigateTo(path: string) {
  window.location.hash = `#${path}`;
}

export function initRouter() {
  function handleRoute() {
    const path = getCurrentPath();
    const route = getRoute(path);

    if (!route) {
      navigateTo(isAuthenticated() ? 'dashboard' : 'login');
      return;
    }

    // Verificar autenticación
    if (route.requiresAuth && !isAuthenticated()) {
      navigateTo('login');
      return;
    }

    if (!route.requiresAuth && isAuthenticated() && path === 'login') {
      navigateTo('dashboard');
      return;
    }

    // Renderizar la página
    const app = document.querySelector<HTMLDivElement>('#app');
    if (app) {
      app.innerHTML = route.render();
      
      // Inicializar eventos de la página
      if (route.init) {
        route.init();
      }
    }
  }

  // Escuchar cambios en el hash
  window.addEventListener('hashchange', handleRoute);
  
  // Cargar la ruta inicial
  handleRoute();
}
