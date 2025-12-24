/**
 * TikTok OAuth API - auto-detects Dev/Prod environment
 */

import apiClient from '../lib/axios';
import {
  generateState,
  generateCodeVerifier,
  generateCodeChallenge,
  detectPlatform,
  storePKCEData
} from '../lib/pkce';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  TikTokAuthUrlResponse,
  OAuthCallbackResponse,
} from '../types/auth.types';

const TIKTOK_CLIENT_KEY = import.meta.env.VITE_TIKTOK_CLIENT_KEY;
const TIKTOK_AUTH_URL = import.meta.env.VITE_TIKTOK_AUTH_URL || 'https://www.tiktok.com/v2/auth/authorize/';
const TIKTOK_SCOPES = import.meta.env.VITE_TIKTOK_SCOPES || 'user.info.basic';

const REDIRECT_URI_DEV = import.meta.env.VITE_TIKTOK_REDIRECT_URI_DEV || 'http://localhost:5173/auth/tiktok/callback';
const REDIRECT_URI_PROD = import.meta.env.VITE_TIKTOK_REDIRECT_URI_PROD || 'https://fypglow.com/auth/tiktok/callback';

function getRedirectUri(): string {
  const platform = detectPlatform();
  return platform === 'desktop' ? REDIRECT_URI_DEV : REDIRECT_URI_PROD;
}

export const authApi = {
  getTikTokAuthUrl: async (): Promise<TikTokAuthUrlResponse> => {
    const platform = detectPlatform();
    const state = generateState();
    const codeVerifier = generateCodeVerifier();
    const codeChallenge = await generateCodeChallenge(codeVerifier, platform);
    const redirectUri = getRedirectUri();

    storePKCEData(state, codeVerifier);
    localStorage.setItem('oauth_redirect_uri', redirectUri);

    const params = new URLSearchParams({
      client_key: TIKTOK_CLIENT_KEY,
      scope: TIKTOK_SCOPES,
      response_type: 'code',
      redirect_uri: redirectUri,
      state: state,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256',
    });

    return { success: true, data: { url: `${TIKTOK_AUTH_URL}?${params.toString()}` } };
  },

  handleTikTokCallback: async (code: string, state: string): Promise<OAuthCallbackResponse> => {
    const storedState = localStorage.getItem('oauth_state');
    const codeVerifier = localStorage.getItem('oauth_code_verifier');
    const redirectUri = localStorage.getItem('oauth_redirect_uri');

    localStorage.removeItem('oauth_state');
    localStorage.removeItem('oauth_code_verifier');
    localStorage.removeItem('oauth_timestamp');
    localStorage.removeItem('oauth_redirect_uri');

    if (!storedState || storedState !== state) {
      throw new Error('Invalid OAuth state');
    }

    const response = await apiClient.post<OAuthCallbackResponse>('/auth/oauth/tiktok/callback', {
      code,
      code_verifier: codeVerifier,
      redirect_uri: redirectUri,
    });

    return response.data;
  },

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
