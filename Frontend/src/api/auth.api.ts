import apiClient from '../lib/axios';
import { generateState, generateCodeVerifier, generateCodeChallenge } from '../lib/pkce';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  TikTokAuthUrlResponse,
  OAuthCallbackResponse,
} from '../types/auth.types';

// TikTok OAuth config from environment
const TIKTOK_CLIENT_KEY = import.meta.env.VITE_TIKTOK_CLIENT_KEY;
const TIKTOK_AUTH_URL = import.meta.env.VITE_TIKTOK_AUTH_URL || 'https://www.tiktok.com/v2/auth/authorize/';
const TIKTOK_REDIRECT_URI = import.meta.env.VITE_TIKTOK_REDIRECT_URI;
const TIKTOK_SCOPES = import.meta.env.VITE_TIKTOK_SCOPES || 'user.info.basic';

export const authApi = {
  // OAuth Methods - PKCE flow with HEX-encoded challenge (TikTok requirement)
  getTikTokAuthUrl: async (): Promise<TikTokAuthUrlResponse> => {
    const state = generateState();
    const codeVerifier = generateCodeVerifier();
    const codeChallenge = await generateCodeChallenge(codeVerifier);

    // Store in localStorage for callback verification
    localStorage.setItem('oauth_state', state);
    localStorage.setItem('oauth_code_verifier', codeVerifier);

    // Build authorization URL with PKCE (TikTok requires HEX-encoded challenge)
    const params = new URLSearchParams({
      client_key: TIKTOK_CLIENT_KEY,
      scope: TIKTOK_SCOPES,
      response_type: 'code',
      redirect_uri: TIKTOK_REDIRECT_URI,
      state: state,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256',
    });

    const url = `${TIKTOK_AUTH_URL}?${params.toString()}`;

    return {
      success: true,
      data: { url },
    };
  },

  handleTikTokCallback: async (code: string, state: string): Promise<OAuthCallbackResponse> => {
    const storedState = localStorage.getItem('oauth_state');
    const codeVerifier = localStorage.getItem('oauth_code_verifier');

    localStorage.removeItem('oauth_state');
    localStorage.removeItem('oauth_code_verifier');

    if (!storedState || storedState !== state) {
      throw new Error('Invalid state');
    }

    // Send code + verifier to backend
    const response = await apiClient.post<OAuthCallbackResponse>('/auth/oauth/tiktok/callback', {
      code,
      code_verifier: codeVerifier,
    });

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
