/**
 * User category subscription types for multi-category selection feature.
 *
 * Business rules:
 * - FREE categories: max 3, no expiration
 * - PREMIUM categories: unlimited, 14 days from purchase
 * - Expired premium categories become inactive (greyed out)
 */

import { Category } from './plan.types';

export interface UserCategory {
  id: number;
  categoryId: number;
  isActive: boolean;
  isPremium: boolean;
  purchasedAt: string | null;
  expiresAt: string | null;
  daysRemaining: number | null;
  isExpired: boolean;
  category: Category;
}

export interface CategoryStats {
  freeActive: number;
  freeLimit: number;
  freeRemaining: number;
  premiumActive: number;
  premiumExpired: number;
  totalActive: number;
}

export interface UserCategoriesResponse {
  categories: UserCategory[];
  stats: CategoryStats;
}

export interface AddCategoryRequest {
  categoryId: number;
  isPurchased?: boolean;
}

export interface RemoveCategoryResponse {
  removed: boolean;
}
