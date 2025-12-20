import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, LoginData, RegisterData } from '../types/auth.types';
import { authApi } from '../api/auth.api';
import { logger } from '../lib/logger';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  hasCompletedOnboarding: boolean;

  // Actions
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
  setUser: (user: User | null) => void;
  checkOnboardingStatus: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
      hasCompletedOnboarding: false,

      login: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.login({ email: data.email, password: data.password });

          localStorage.setItem('access_token', response.data.token);
          localStorage.setItem('refresh_token', response.data.refresh_token);

          set({
            user: response.data.user,
            isAuthenticated: true,
            isLoading: false,
          });

          // Check onboarding status after login
          const { checkOnboardingStatus } = get();
          await checkOnboardingStatus();
        } catch (error: any) {
          const message = error.response?.data?.error?.message || 'Login failed';
          set({ error: message, isLoading: false });
          throw new Error(message);
        }
      },

      register: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.register({
            email: data.email,
            password: data.password,
            language: data.language || 'en'
          });

          localStorage.setItem('access_token', response.data.token);
          localStorage.setItem('refresh_token', response.data.refresh_token);

          set({
            user: response.data.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          const message = error.response?.data?.error?.message || 'Registration failed';
          set({ error: message, isLoading: false });
          throw new Error(message);
        }
      },

      logout: async () => {
        try {
          await authApi.logout();
        } catch {
          // Ignore logout errors
        }

        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        set({
          user: null,
          isAuthenticated: false,
        });
      },

      clearError: () => set({ error: null }),

      setUser: (user) => set({ user, isAuthenticated: !!user }),

      checkOnboardingStatus: async () => {
        const { isAuthenticated } = get();
        if (!isAuthenticated) {
          set({ hasCompletedOnboarding: false });
          return;
        }

        try {
          const { preferencesApi } = await import('../api/preferences.api');
          const response = await preferencesApi.get();
          if (response.success && response.data) {
            set({ hasCompletedOnboarding: response.data.hasCompletedOnboarding });
          }
        } catch (error) {
          logger.error('Failed to check onboarding status:', error);
          // Assume completed to avoid blocking users
          set({ hasCompletedOnboarding: true });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        hasCompletedOnboarding: state.hasCompletedOnboarding,
      }),
    }
  )
);
