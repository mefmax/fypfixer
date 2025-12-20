import apiClient from '../lib/axios';
import type { ApiResponse } from '../types/api.types';

export interface UserStats {
  streak: {
    currentStreak: number;
    longestStreak: number;
    lastActiveDate: string | null;
    nextMilestone: number | null;
  };
  gamification: {
    level: string;
    xp: number;
    actionsCompleted: number;
    plansCompleted: number;
  };
}

export interface StreakInfo {
  currentStreak: number;
  longestStreak: number;
  nextMilestone: number | null;
  totalXp: number;
  level: string;
}

export const userApi = {
  getStats: async (): Promise<ApiResponse<UserStats>> => {
    const response = await apiClient.get<ApiResponse<UserStats>>('/user/stats');
    return response.data;
  },

  getStreak: async (): Promise<ApiResponse<StreakInfo>> => {
    const response = await apiClient.get<ApiResponse<StreakInfo>>('/user/streak');
    return response.data;
  },
};
