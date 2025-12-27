import { createBrowserRouter, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/auth/LoginPage';
import { TikTokCallback } from './pages/auth/callback/TikTokCallback';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { OnboardingRoute } from './components/auth/OnboardingRoute';
import { GoalsOnboardingPage } from './pages/onboarding/GoalsOnboardingPage';
import { PlanPreviewPage } from './pages/onboarding/PlanPreviewPage';
import { TermsPage, PrivacyPage } from './pages/legal';
import { DailyPlanViewV2 } from './components/plan/DailyPlanViewV2';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <LoginPage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/auth/tiktok/callback',
    element: <TikTokCallback />,
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
    path: '/plan',
    element: (
      <OnboardingRoute>
        <DailyPlanViewV2 />
      </OnboardingRoute>
    ),
  },
  {
    path: '/privacy',
    element: <PrivacyPage />,
  },
  {
    path: '/terms',
    element: <TermsPage />,
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
]);
