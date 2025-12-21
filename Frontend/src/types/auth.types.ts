export interface User {
  id: number;
  client_id: string;
  email: string | null;
  display_name: string | null;
  avatar_url: string | null;
  oauth_provider: string | null;
  language: string;
  is_premium: boolean;
  created_at: string | null;
}

// OAuth Response from backend
export interface OAuthUser {
  id: number;
  display_name: string | null;
  avatar_url: string | null;
  oauth_provider: string;
  is_premium: boolean;
}

export interface OAuthCallbackResponse {
  success: boolean;
  data: {
    access_token: string;
    refresh_token: string | null;
    user: OAuthUser;
  };
}

export interface TikTokAuthUrlResponse {
  success: boolean;
  data: {
    url: string;
  };
}

// Legacy email/password types (deprecated, kept for backwards compatibility)
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  language?: string;
}

export interface AuthResponse {
  success: boolean;
  data: {
    user: User;
    token: string;
    refresh_token: string;
  };
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  confirmPassword?: string;
  language?: string;
}
