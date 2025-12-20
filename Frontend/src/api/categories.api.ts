/**
 * Categories API - manages user category subscriptions.
 *
 * Endpoints:
 * - GET  /user/categories - get user's categories
 * - POST /user/categories - add category
 * - DELETE /user/categories/:id - remove category
 * - GET  /user/categories/stats - get stats
 */

import apiClient from '../lib/axios';
import type { ApiResponse } from '../types/api.types';
import type {
  UserCategoriesResponse,
  UserCategory,
  RemoveCategoryResponse,
  CategoryStats,
} from '../types/category.types';

interface Category {
  id: number;
  code: string;
  name: string;
  is_premium: boolean;
}

interface CategoriesListResponse {
  categories: Category[];
}

export const categoriesApi = {
  /**
   * Get all available categories (public endpoint).
   */
  getCategories: async (): Promise<ApiResponse<CategoriesListResponse>> => {
    const response = await apiClient.get('/categories');
    return response.data;
  },

  /**
   * Get user's category subscriptions.
   * @param includeInactive - include inactive/expired categories
   */
  getMyCategories: async (includeInactive = false): Promise<ApiResponse<UserCategoriesResponse>> => {
    const response = await apiClient.get('/user/categories', {
      params: { include_inactive: includeInactive },
    });
    return response.data;
  },

  /**
   * Add a category to user's list.
   * @param categoryId - category ID to add
   * @param isPurchased - true if this is a premium purchase
   */
  addCategory: async (categoryId: number, isPurchased = false): Promise<ApiResponse<UserCategory>> => {
    const response = await apiClient.post('/user/categories', {
      categoryId,
      isPurchased,
    });
    return response.data;
  },

  /**
   * Remove a category from user's list.
   * @param categoryId - category ID to remove
   */
  removeCategory: async (categoryId: number): Promise<ApiResponse<RemoveCategoryResponse>> => {
    const response = await apiClient.delete(`/user/categories/${categoryId}`);
    return response.data;
  },

  /**
   * Get category subscription stats.
   */
  getStats: async (): Promise<ApiResponse<CategoryStats>> => {
    const response = await apiClient.get('/user/categories/stats');
    return response.data;
  },
};
