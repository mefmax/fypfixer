import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from './store/authStore';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { GoalsOnboardingPage } from './pages/onboarding/GoalsOnboardingPage';
import { PlanPreviewPage } from './pages/onboarding/PlanPreviewPage';
import { VideoModal } from './components/video/VideoModal';
import { loadAppConfig } from './lib/appConfig';
import { logger } from './lib/logger';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

// Protected Route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  return <>{children}</>;
};

// Public Route wrapper (redirect to dashboard if authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

function App() {
  // Load app config on startup (async, non-blocking)
  useEffect(() => {
    loadAppConfig().catch((err) => logger.error('Failed to load app config:', err));
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Landing page - redirect to dashboard if authenticated */}
          <Route
            path="/"
            element={
              <PublicRoute>
                <LandingPage />
              </PublicRoute>
            }
          />

          {/* Auth routes */}
          <Route
            path="/auth/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path="/auth/register"
            element={
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            }
          />
          {/* Legacy routes for backward compatibility */}
          <Route path="/login" element={<Navigate to="/auth/login" replace />} />
          <Route path="/register" element={<Navigate to="/auth/register" replace />} />

          {/* Onboarding routes */}
          <Route
            path="/onboarding/goals"
            element={
              <ProtectedRoute>
                <GoalsOnboardingPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/onboarding/plan-preview"
            element={
              <ProtectedRoute>
                <PlanPreviewPage />
              </ProtectedRoute>
            }
          />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />

          {/* Privacy and Terms */}
          <Route
            path="/privacy"
            element={
              <div className="min-h-screen bg-gradient-to-b from-[#0a0e27] to-[#1a1f3a] flex items-center justify-center p-6">
                <div className="text-center text-white">
                  <h1 className="text-3xl font-bold mb-4">Privacy Policy</h1>
                  <p className="text-[#B0B0B0]">Coming soon...</p>
                </div>
              </div>
            }
          />
          <Route
            path="/terms"
            element={
              <div className="min-h-screen bg-gradient-to-b from-[#0a0e27] to-[#1a1f3a] flex items-center justify-center p-6">
                <div className="text-center text-white">
                  <h1 className="text-3xl font-bold mb-4">Terms of Service</h1>
                  <p className="text-[#B0B0B0]">Coming soon...</p>
                </div>
              </div>
            }
          />

          {/* Catch all - redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Global components */}
        <VideoModal />
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
