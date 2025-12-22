/**
 * PKCE (Proof Key for Code Exchange) utilities for TikTok OAuth 2.0
 *
 * IMPORTANT: TikTok uses HEX encoding for code_challenge instead of standard
 * Base64URL encoding specified in RFC 7636. This implementation is
 * TikTok-specific and may not work with other OAuth providers.
 *
 * @see https://developers.tiktok.com/doc/login-kit-desktop/
 * @see docs/TIKTOK_OAUTH_PKCE_LESSONS_LEARNED.md
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

// Convert ArrayBuffer to hex string
function arrayBufferToHex(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  return Array.from(bytes)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

// Generate code_challenge from code_verifier using S256 method
// TikTok requires HEX encoding (not base64url like standard RFC 7636!)
export async function generateCodeChallenge(codeVerifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  // TikTok uses HEX encoding, not base64url!
  return arrayBufferToHex(digest);
}

// Generate state token for CSRF protection
export function generateState(): string {
  const randomBytes = generateRandomBytes(32);
  return base64UrlEncode(randomBytes);
}

// Storage keys
const STORAGE_KEY_STATE = 'oauth_state';
const STORAGE_KEY_VERIFIER = 'oauth_code_verifier';
const STORAGE_KEY_TIMESTAMP = 'oauth_timestamp';

// Check if PKCE data exists and is fresh (within last 60 seconds)
export function hasFreshPKCEData(): boolean {
  const timestamp = localStorage.getItem(STORAGE_KEY_TIMESTAMP);
  if (!timestamp) return false;

  const age = Date.now() - parseInt(timestamp, 10);
  return age < 60000; // 60 seconds
}

// Store PKCE data in localStorage (more reliable than sessionStorage for redirects)
export function storePKCEData(state: string, codeVerifier: string): void {
  localStorage.setItem(STORAGE_KEY_STATE, state);
  localStorage.setItem(STORAGE_KEY_VERIFIER, codeVerifier);
  localStorage.setItem(STORAGE_KEY_TIMESTAMP, Date.now().toString());
}

// Retrieve and clear PKCE data from localStorage
export function retrievePKCEData(): { state: string | null; codeVerifier: string | null } {
  const state = localStorage.getItem(STORAGE_KEY_STATE);
  const codeVerifier = localStorage.getItem(STORAGE_KEY_VERIFIER);

  // Clear after retrieval (one-time use)
  localStorage.removeItem(STORAGE_KEY_STATE);
  localStorage.removeItem(STORAGE_KEY_VERIFIER);
  localStorage.removeItem(STORAGE_KEY_TIMESTAMP);

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

  return { state, codeVerifier, codeChallenge };
}
