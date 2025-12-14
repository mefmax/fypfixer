import { apiClient } from '../lib/axios';
import type { Plan, Category } from '../types/plan.types';

export const plansApi = {
  getPlans: async (params?: { category?: string; language?: string }) => {
    const response = await apiClient.get<{ plans: Plan[] }>('/api/plans', { params });
    return response.data;
  },

  getPlan: async (planId: string) => {
    const response = await apiClient.get<Plan>(`/api/plans/${planId}`);
    return response.data;
  },

  completeStep: async (planId: string, stepId: string) => {
    const response = await apiClient.post(`/api/plans/${planId}/steps/${stepId}/complete`, {
      completed_at: new Date().toISOString(),
    });
    return response.data;
  },
};

export const categoriesApi = {
  getCategories: async () => {
    const response = await apiClient.get<Category[]>('/api/categories');
    return response.data;
  },
};
