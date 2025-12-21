/**
 * PKCE (Proof Key for Code Exchange) utilities for OAuth 2.0
 * RFC 7636 compliant implementation for browser-side OAuth
 */

// Generate cryptographically secure random bytes
function generateRandomBytes(length: number): Uint8Array {
  const array = new Uint8Array(length);
  crypto.getRandomValues(array);
  return array;
}

// Base64 URL encode (RFC 4648)
function base64UrlEncode(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

// Generate code_verifier (64 characters - some providers need longer)
export function generateCodeVerifier(): string {
  const randomBytes = generateRandomBytes(48); // 48 bytes = 64 chars in base64url
  return base64UrlEncode(randomBytes);
}

// Generate code_challenge from code_verifier using S256 method
export async function generateCodeChallenge(codeVerifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return base64UrlEncode(digest);
}

// Generate state token for CSRF protection
export function generateState(): string {
  const randomBytes = generateRandomBytes(32);
  return base64UrlEncode(randomBytes);
}

// Storage keys
const STORAGE_KEY_STATE = 'oauth_state';
const STORAGE_KEY_VERIFIER = 'oauth_code_verifier';

// Store PKCE data in localStorage (more reliable than sessionStorage for redirects)
export function storePKCEData(state: string, codeVerifier: string): void {
  localStorage.setItem(STORAGE_KEY_STATE, state);
  localStorage.setItem(STORAGE_KEY_VERIFIER, codeVerifier);
  console.log('[PKCE] Stored state and verifier in localStorage');
}

// Retrieve and clear PKCE data from localStorage
export function retrievePKCEData(): { state: string | null; codeVerifier: string | null } {
  const state = localStorage.getItem(STORAGE_KEY_STATE);
  const codeVerifier = localStorage.getItem(STORAGE_KEY_VERIFIER);

  console.log('[PKCE] Retrieved from localStorage:', {
    hasState: !!state,
    hasVerifier: !!codeVerifier,
  });

  // Clear after retrieval (one-time use)
  localStorage.removeItem(STORAGE_KEY_STATE);
  localStorage.removeItem(STORAGE_KEY_VERIFIER);

  return { state, codeVerifier };
}

// Generate full PKCE pair
export async function generatePKCEPair(): Promise<{
  state: string;
  codeVerifier: string;
  codeChallenge: string;
}> {
  const state = generateState();
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);

  // Save debug info to localStorage (no alert to avoid interrupting flow)
  localStorage.setItem('pkce_debug', JSON.stringify({
    verifier: codeVerifier,
    challenge: codeChallenge,
    verifierLength: codeVerifier.length,
    challengeLength: codeChallenge.length,
    timestamp: new Date().toISOString(),
  }));

  return { state, codeVerifier, codeChallenge };
}
