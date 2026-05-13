import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
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

          {/* Auth routes render pages that already include AuthLayout */}
          {authRoutes.map((route) => (
            <Route
              key={route.path}
              path={route.path}
              element={route.element}
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