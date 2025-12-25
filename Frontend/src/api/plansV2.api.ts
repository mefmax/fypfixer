/**
 * Plans V2 API - New plan structure with Clear/Watch/Reinforce steps
 */
import apiClient from '../lib/axios';
import type { PlanV2, ToxicCreator } from '../types/planV2.types';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: { code: string; message: string };
}

export const plansV2Api = {
  /**
   * Generate a new plan v2.0
   */
  generatePlan: async (category: string): Promise<ApiResponse<{ plan: PlanV2 }>> => {
    const response = await apiClient.post('/v2/plan/generate', { category });
    return response.data;
  },

  /**
   * Get toxic creators for the Clear step
   */
  getToxicCreators: async (category?: number, limit = 5): Promise<ApiResponse<{ toxic_creators: ToxicCreator[]; count: number }>> => {
    const params = new URLSearchParams();
    if (category) params.append('category', String(category));
    params.append('limit', String(limit));

    const response = await apiClient.get(`/v2/toxic-creators?${params}`);
    return response.data;
  },

  /**
   * Block a creator
   */
  blockCreator: async (creatorUsername: string, reason?: string): Promise<ApiResponse<{ blocked: boolean; creator_username: string }>> => {
    const response = await apiClient.post('/v2/toxic-creators/block', {
      creator_username: creatorUsername,
      reason,
    });
    return response.data;
  },

  /**
   * Unblock a creator
   */
  unblockCreator: async (creatorUsername: string): Promise<ApiResponse<{ unblocked: boolean }>> => {
    const response = await apiClient.post('/v2/toxic-creators/unblock', {
      creator_username: creatorUsername,
    });
    return response.data;
  },

  /**
   * Get curated videos for Watch step
   */
  getCuratedVideos: async (category?: number, count = 4): Promise<ApiResponse<{ videos: any[]; count: number }>> => {
    const params = new URLSearchParams();
    if (category) params.append('category', String(category));
    params.append('count', String(count));

    const response = await apiClient.get(`/v2/curated-videos?${params}`);
    return response.data;
  },

  /**
   * Get user's favorites
   */
  getFavorites: async (limit = 10): Promise<ApiResponse<{ favorites: any[]; count: number }>> => {
    const response = await apiClient.get(`/v2/favorites?limit=${limit}`);
    return response.data;
  },

  /**
   * Add video to favorites
   */
  addFavorite: async (videoId: string): Promise<ApiResponse<{ added: boolean; video_id: string }>> => {
    const response = await apiClient.post('/v2/favorites', { video_id: videoId });
    return response.data;
  },

  /**
   * Remove video from favorites
   */
  removeFavorite: async (videoId: string): Promise<ApiResponse<{ removed: boolean }>> => {
    const response = await apiClient.delete('/v2/favorites', { data: { video_id: videoId } });
    return response.data;
  },

  /**
   * Get random favorite for Reinforce step
   */
  getRandomFavorite: async (): Promise<ApiResponse<{ video: any | null }>> => {
    const response = await apiClient.get('/v2/favorites/random');
    return response.data;
  },
};
