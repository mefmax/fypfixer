import apiClient from '../lib/axios';
import type { Plan, Category } from '../types/plan.types';
import type { ApiResponse } from '../types/api.types';
import type { DailyActionPlan, CompleteActionResponse } from '../types/action.types';

export const plansApi = {
  getDailyPlan: async (category: string, lang = 'en'): Promise<ApiResponse<Plan>> => {
    const response = await apiClient.get<ApiResponse<Plan>>('/plan', {
      params: { category, lang },
    });
    return response.data;
  },

  getDailyActions: async (category: string, lang = 'en'): Promise<ApiResponse<DailyActionPlan>> => {
    const response = await apiClient.get<ApiResponse<DailyActionPlan>>('/v1/plans/today', {
      params: { category, language: lang },
    });
    return response.data;
  },

  generateNewPlan: async (category: string, lang = 'en'): Promise<ApiResponse<DailyActionPlan>> => {
    const response = await apiClient.post<ApiResponse<DailyActionPlan>>('/v1/plans/generate', {
      category,
      language: lang,
      forceRegenerate: true,
    });
    return response.data;
  },

  getPlans: async (params?: { category?: string; language?: string; limit?: number; offset?: number }) => {
    const response = await apiClient.get('/plans', { params });
    return response.data;
  },

  completeStep: async (planId: number, stepId: number): Promise<ApiResponse<{ step_id: number; completed: boolean }>> => {
    const response = await apiClient.post(`/plans/${planId}/steps/${stepId}/complete`);
    return response.data;
  },

  completeAction: async (actionId: string): Promise<ApiResponse<CompleteActionResponse>> => {
    const response = await apiClient.post<ApiResponse<CompleteActionResponse>>(`/actions/${actionId}/complete`);
    return response.data;
  },

  getCategories: async (language = 'en'): Promise<ApiResponse<{ categories: Category[] }>> => {
    const response = await apiClient.get('/categories', {
      params: { language },
    });
    return response.data;
  },
};
