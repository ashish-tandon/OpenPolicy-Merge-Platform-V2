// router.tsx
import { createBrowserRouter } from 'react-router-dom';
import App from './src/App';
import Dashboard from './src/pages/Dashboard';
import GovernmentLevels from './src/pages/data/GovernmentLevels';
import ETLManagement from './src/pages/ETLManagement';
import APIGatewayDashboard from './src/pages/APIGatewayDashboard';
import ScrapersDashboard from './src/pages/ScrapersDashboard';
import DatabaseDashboard from './src/pages/DatabaseDashboard';
import UserManagement from './src/pages/UserManagement';
import NotificationSetup from './src/pages/NotificationSetup';
import NotificationStats from './src/pages/NotificationStats';
import UmamiAnalytics from './src/pages/UmamiAnalytics';
import Login from './src/pages/auth/Login';
import ProtectedRoute from './src/components/auth/ProtectedRoute';

export const router = createBrowserRouter([
  {
    path: '/auth/login',
    element: <Login />
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <App />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Dashboard />
      },
      {
        path: 'data',
        children: [
          {
            path: 'government-levels',
            element: <GovernmentLevels />
          }
        ]
      },
      {
        path: 'government',
        children: [
          {
            path: 'levels',
            element: <GovernmentLevels />
          }
        ]
      },
      {
        path: 'parliamentary',
        children: [
          {
            path: 'debates',
            element: <div>Debates Management</div>
          },
          {
            path: 'committees',
            element: <div>Committees Management</div>
          },
          {
            path: 'sessions',
            element: <div>Sessions Management</div>
          }
        ]
      },
      {
        path: 'representatives',
        element: <div>Representatives Management</div>
      },
      {
        path: 'bills',
        element: <div>Bills & Legislation Management</div>
      },
      {
        path: 'votes',
        element: <div>Voting Records Management</div>
      },
      {
        path: 'etl',
        element: <ETLManagement />
      },
      {
        path: 'scrapers',
        element: <ScrapersDashboard />
      },
      {
        path: 'database',
        element: <DatabaseDashboard />
      },
      {
        path: 'api-gateway',
        element: <APIGatewayDashboard />
      },
      {
        path: 'analytics',
        element: <UmamiAnalytics />
      },
      {
        path: 'monitoring',
        element: <div>System Monitoring</div>
      },
      {
        path: 'users',
        element: <UserManagement />
      },
      {
        path: 'admin',
        children: [
          {
            path: 'notifications',
            element: <NotificationSetup />
          },
          {
            path: 'notification-stats',
            element: <NotificationStats />
          }
        ]
      },
      {
        path: 'settings',
        element: <div>System Settings</div>
      }
    ]
  }
]);
