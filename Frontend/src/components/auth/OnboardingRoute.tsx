import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

interface OnboardingRouteProps {
  children: React.ReactNode;
}

export const OnboardingRoute: React.FC<OnboardingRouteProps> = ({ children }) => {
  const { isAuthenticated, hasCompletedOnboarding } = useAuthStore();

  // Not logged in - go to login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Logged in but hasn't done onboarding - go to onboarding
  if (!hasCompletedOnboarding) {
    return <Navigate to="/onboarding" replace />;
  }

  // All good - show the page
  return <>{children}</>;
};
