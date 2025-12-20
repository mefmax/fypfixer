import apiClient from '../lib/axios';
import type { ApiResponse } from '../types/api.types';

export interface UserPreferences {
  hasCompletedOnboarding: boolean;
  selectedGoals: string[];
  preferredCategory: string;
  language: string;
}

export const preferencesApi = {
  get: async (): Promise<ApiResponse<UserPreferences>> => {
    const response = await apiClient.get('/preferences');
    return response.data;
  },

  update: async (data: Partial<UserPreferences>): Promise<ApiResponse<UserPreferences>> => {
    const response = await apiClient.put('/preferences', data);
    return response.data;
  },

  completeOnboarding: async (goals: string[], category: string): Promise<ApiResponse<{ redirectTo: string }>> => {
    const response = await apiClient.post('/preferences/complete-onboarding', {
      goals,
      category,
    });
    return response.data;
  },
};
