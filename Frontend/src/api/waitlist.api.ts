import apiClient from '../lib/axios';
import type { ApiResponse } from '../types/api.types';

interface JoinWaitlistResponse {
  message: string;
  category: string;
  position?: number;
}

export const waitlistApi = {
  joinWaitlist: async (categoryId: number): Promise<ApiResponse<JoinWaitlistResponse>> => {
    const response = await apiClient.post<ApiResponse<JoinWaitlistResponse>>('/waitlist/join', {
      category_id: categoryId,
    });
    return response.data;
  },

  leaveWaitlist: async (categoryId: number): Promise<ApiResponse<{ message: string }>> => {
    const response = await apiClient.post<ApiResponse<{ message: string }>>('/waitlist/leave', {
      category_id: categoryId,
    });
    return response.data;
  },
};
