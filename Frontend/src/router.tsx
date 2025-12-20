import { createBrowserRouter, Navigate } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { OnboardingRoute } from './components/auth/OnboardingRoute';
import { GoalsOnboardingPage } from './pages/onboarding/GoalsOnboardingPage';
import { PlanPreviewPage } from './pages/onboarding/PlanPreviewPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <LandingPage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
  {
    path: '/onboarding',
    element: <GoalsOnboardingPage />,
  },
  {
    path: '/onboarding/plan-preview',
    element: <PlanPreviewPage />,
  },
  {
    path: '/dashboard',
    element: (
      <OnboardingRoute>
        <DashboardPage />
      </OnboardingRoute>
    ),
  },
  {
    path: '/privacy',
    element: (
      <div className="min-h-screen bg-gradient-to-b from-[#0a0e27] to-[#1a1f3a] flex items-center justify-center p-6">
        <div className="text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Privacy Policy</h1>
          <p className="text-[#B0B0B0]">Coming soon...</p>
        </div>
      </div>
    ),
  },
  {
    path: '/terms',
    element: (
      <div className="min-h-screen bg-gradient-to-b from-[#0a0e27] to-[#1a1f3a] flex items-center justify-center p-6">
        <div className="text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Terms of Service</h1>
          <p className="text-[#B0B0B0]">Coming soon...</p>
        </div>
      </div>
    ),
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
]);
