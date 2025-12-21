import apiClient from '../lib/axios';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  TikTokAuthUrlResponse,
  OAuthCallbackResponse,
} from '../types/auth.types';

export const authApi = {
  // OAuth Methods
  getTikTokAuthUrl: async (): Promise<TikTokAuthUrlResponse> => {
    const response = await apiClient.get<TikTokAuthUrlResponse>('/auth/oauth/tiktok/url');
    return response.data;
  },

  handleTikTokCallback: async (code: string, state: string): Promise<OAuthCallbackResponse> => {
    const url = '/auth/oauth/tiktok/callback?code=' + encodeURIComponent(code) + '&state=' + encodeURIComponent(state);
    const response = await apiClient.get<OAuthCallbackResponse>(url);
    return response.data;
  },

  // Legacy email/password methods (deprecated)
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/register', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout');
  },

  getProfile: async () => {
    const response = await apiClient.get('/user');
    return response.data;
  },
};
