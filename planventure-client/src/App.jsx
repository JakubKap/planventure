import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import AuthLayout from './layouts/AuthLayout';
import ProtectedRoute from './components/routing/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import { homeRoutes, authRoutes, protectedRoutes } from './routes/routes';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Home routes with MainLayout */}
          {homeRoutes.map((route) => (
            <Route
              key={route.path}
              path={route.path}
              element={
                <MainLayout>
                  {route.element}
                </MainLayout>
              }
            />
          ))}

          {/* Auth routes with AuthLayout */}
          {authRoutes.map((route) => (
            <Route
              key={route.path}
              path={route.path}
              element={
                <AuthLayout>
                  {route.element}
                </AuthLayout>
              }
            />
          ))}

          {/* Protected routes with DashboardLayout (already included in route elements) */}
          {protectedRoutes.map((route) => (
            <Route
              key={route.path}
              path={route.path}
              element={
                <ProtectedRoute>
                  {route.element}
                </ProtectedRoute>
              }
            />
          ))}
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;