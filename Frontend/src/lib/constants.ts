export const APP_NAME = 'FYPGlow';

export const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'ru', name: 'Русский' },
  { code: 'es', name: 'Español' },
] as const;

export const STORAGE_KEYS = {
  AUTH: 'auth-storage',
  UI: 'ui-storage',
  CATEGORY: 'fypfixer_category',
} as const;

// ===== UI TIMEOUTS =====

export const UI_TIMEOUTS = {
  TOAST_AUTO_CLOSE: 5000,
  DEBOUNCE: 300,
  API_TIMEOUT: 30000,
} as const;

// ===== LIMITS =====

export const LIMITS = {
  MIN_GOALS: 1,
  MAX_GOALS: 3,
  MAX_ACTIONS: 8,
  MIN_ACTIONS: 3,
} as const;

// ===== API =====

export const API = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
} as const;
