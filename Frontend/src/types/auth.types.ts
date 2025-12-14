export interface User {
  id: string;
  email: string;
  language: 'en' | 'ru' | 'es';
  created_at: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  language: 'en' | 'ru' | 'es';
}

export interface AuthResponse {
  user_id: string;
  token: string;
  email: string;
  language: string;
}
