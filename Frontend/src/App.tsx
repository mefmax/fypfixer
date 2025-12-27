import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from './store/authStore';
import { LoginPage } from './pages/auth/LoginPage';
import { TikTokCallback } from './pages/auth/callback/TikTokCallback';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { AdminDashboardPage } from './pages/admin/DashboardPage';
import { GoalsOnboardingPage } from './pages/onboarding/GoalsOnboardingPage';
import { PlanPreviewPage } from './pages/onboarding/PlanPreviewPage';
import { TermsPage, PrivacyPage } from './pages/legal';
import { VideoModal } from './components/video/VideoModal';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import { loadAppConfig, validateStoredCategory } from './lib/appConfig';
import { categoriesApi } from './api/categories.api';
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
    return <Navigate to="/login" replace />;
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
  // Load app config and validate stored data on startup
  useEffect(() => {
    const init = async () => {
      try {
        await loadAppConfig();
        // Validate stored category against available categories
        const response = await categoriesApi.getCategories();
        if (response.success && response.data?.categories) {
          const validCodes = response.data.categories.map((c) => c.code);
          await validateStoredCategory(validCodes);
        }
      } catch (err) {
        logger.error('Failed to initialize app:', err);
      }
    };
    init();
  }, []);

  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
          {/* Login page - main entry point */}
          <Route
            path="/"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path="/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />

          {/* TikTok OAuth callback */}
          <Route path="/auth/tiktok/callback" element={<TikTokCallback />} />

          {/* Onboarding routes */}
          <Route path="/onboarding" element={<GoalsOnboardingPage />} />
          <Route path="/onboarding/goals" element={<GoalsOnboardingPage />} />
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
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/terms" element={<TermsPage />} />

          {/* Admin Dashboard */}
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute>
                <AdminDashboardPage />
              </ProtectedRoute>
            }
          />

            {/* Catch all - redirect to login */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>

          {/* Global components */}
          <VideoModal />
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
