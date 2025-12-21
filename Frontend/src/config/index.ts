/**
 * Application Configuration
 *
 * All configurable values should come from environment variables.
 * No hardcoded URLs or API keys.
 */

export const config = {
  // API base URL (without /api suffix for OAuth endpoints that need full path control)
  apiBaseUrl: import.meta.env.VITE_API_URL?.replace(/\/api$/, '') || 'http://localhost:8000',

  // API URL with /api prefix (for existing api client compatibility)
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
};
