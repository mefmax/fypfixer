export const APP_NAME = 'FYPFixer';

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
