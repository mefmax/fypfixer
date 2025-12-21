import apiClient from '../lib/axios';
import {
  generatePKCEPair,
  storePKCEData,
  retrievePKCEData,
} from '../lib/pkce';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  TikTokAuthUrlResponse,
  OAuthCallbackResponse,
} from '../types/auth.types';

// TikTok OAuth config (from env or hardcoded for dev)
const TIKTOK_CLIENT_KEY = 'sbawtxexitqtinqhng';
const TIKTOK_AUTH_URL = 'https://www.tiktok.com/v2/auth/authorize/';
const TIKTOK_REDIRECT_URI = 'http://localhost:5173/auth/tiktok/callback';
const TIKTOK_SCOPES = 'user.info.basic,user.info.profile,user.info.stats,video.list';

export const authApi = {
  // OAuth Methods - Frontend-side PKCE generation
  getTikTokAuthUrl: async (): Promise<TikTokAuthUrlResponse> => {
    // Generate PKCE on frontend (solves SameSite cookie issue)
    const { state, codeVerifier, codeChallenge } = await generatePKCEPair();

    // Debug logging - FULL values for debugging PKCE issue
    console.log('[OAuth] Generated PKCE:', {
      state: state.substring(0, 10) + '...',
      verifier: codeVerifier,  // FULL verifier for debugging
      challenge: codeChallenge, // FULL challenge for debugging
      verifierLength: codeVerifier.length,
      challengeLength: codeChallenge.length,
    });

    // Store in sessionStorage for callback
    storePKCEData(state, codeVerifier);

    // Build authorization URL
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

    // Log FULL URL for debugging - check code_challenge in URL
    console.log('[OAuth] FULL TikTok auth URL:', url);
    console.log('[OAuth] code_challenge in URL:', params.get('code_challenge'));

    // Save URL to localStorage for later comparison
    localStorage.setItem('oauth_auth_url', url);

    return {
      success: true,
      data: { url },
    };
  },

  handleTikTokCallback: async (code: string, state: string): Promise<OAuthCallbackResponse> => {
    // Retrieve PKCE data from sessionStorage
    const { state: storedState, codeVerifier } = retrievePKCEData();

    // Debug logging - FULL values to compare with what was sent to TikTok
    const pkceDebug = localStorage.getItem('pkce_debug');
    const savedAuthUrl = localStorage.getItem('oauth_auth_url');

    // Extract code_challenge from saved URL
    let challengeFromUrl = null;
    if (savedAuthUrl) {
      const urlParams = new URL(savedAuthUrl).searchParams;
      challengeFromUrl = urlParams.get('code_challenge');
    }

    console.log('[OAuth] Callback PKCE:', {
      receivedState: state.substring(0, 10) + '...',
      storedState: storedState ? storedState.substring(0, 10) + '...' : 'null',
      stateMatch: storedState === state,
      verifierFromStorage: codeVerifier,  // FULL verifier
      verifierLength: codeVerifier?.length || 0,
      pkceDebugFromGeneration: pkceDebug ? JSON.parse(pkceDebug) : null,
      challengeSentToTikTok: challengeFromUrl,
      savedAuthUrl: savedAuthUrl,
    });

    // Verify state matches (CSRF protection)
    if (!storedState || storedState !== state) {
      console.error('[OAuth] State mismatch!', { received: state, stored: storedState });
      throw new Error('Invalid state - possible CSRF attack or session expired');
    }

    if (!codeVerifier) {
      console.error('[OAuth] Missing code verifier!');
      throw new Error('Missing code verifier - session expired');
    }

    // Send code + code_verifier to backend for token exchange
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
