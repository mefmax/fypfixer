/**
 * Application Configuration Service
 *
 * Fetches and caches application settings from backend.
 * Provides fallback defaults if backend is unavailable.
 */

import apiClient from './axios';
import { logger } from './logger';

export interface AppConfig {
  defaultCategoryCode: string | null;
  maxFreeCategories: number;
  premiumAccessDays: number;
  actionsPerPlan: number;
}

// Default fallback values
const DEFAULTS: AppConfig = {
  defaultCategoryCode: null, // Will be determined from categories
  maxFreeCategories: 3,
  premiumAccessDays: 14,
  actionsPerPlan: 5,
};

// Cached config
let cachedConfig: AppConfig | null = null;
let configPromise: Promise<AppConfig> | null = null;

/**
 * Load app config from backend (cached).
 * Returns cached value if already loaded.
 */
export async function loadAppConfig(): Promise<AppConfig> {
  // Return cached if available
  if (cachedConfig) {
    return cachedConfig;
  }

  // Return in-flight promise if loading
  if (configPromise) {
    return configPromise;
  }

  // Start loading
  configPromise = fetchConfig();
  cachedConfig = await configPromise;
  configPromise = null;

  return cachedConfig;
}

async function fetchConfig(): Promise<AppConfig> {
  try {
    const response = await apiClient.get('/config/defaults');
    if (response.data?.success && response.data?.data) {
      return {
        defaultCategoryCode: response.data.data.defaultCategoryCode || null,
        maxFreeCategories: response.data.data.maxFreeCategories || DEFAULTS.maxFreeCategories,
        premiumAccessDays: response.data.data.premiumAccessDays || DEFAULTS.premiumAccessDays,
        actionsPerPlan: response.data.data.actionsPerPlan || DEFAULTS.actionsPerPlan,
      };
    }
  } catch (error) {
    logger.warn('Failed to load app config, using defaults:', error);
  }

  return DEFAULTS;
}

/**
 * Get current config (sync).
 * Returns cached config or defaults if not yet loaded.
 */
export function getAppConfig(): AppConfig {
  return cachedConfig || DEFAULTS;
}

/**
 * Get default category code.
 * Falls back to 'fitness' if not configured.
 */
export function getDefaultCategoryCode(): string {
  const config = getAppConfig();
  return config.defaultCategoryCode || 'fitness';
}

/**
 * Get max free categories limit.
 */
export function getMaxFreeCategories(): number {
  return getAppConfig().maxFreeCategories;
}

/**
 * Refresh config from backend.
 */
export async function refreshAppConfig(): Promise<AppConfig> {
  cachedConfig = null;
  return loadAppConfig();
}
