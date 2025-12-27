/**
 * PKCE utilities for TikTok OAuth 2.0
 * Auto-detects platform: Desktop (HEX) vs Web (Base64URL)
 */
import { logger } from './logger';

export type TikTokPlatform = 'web' | 'desktop';

export function detectPlatform(): TikTokPlatform {
  const isDev = import.meta.env.DEV;
  const isLocalhost = typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' ||
     window.location.hostname === '127.0.0.1');

  return (isDev || isLocalhost) ? 'desktop' : 'web';
}

function generateRandomBytes(length: number): Uint8Array {
  const array = new Uint8Array(length);
  crypto.getRandomValues(array);
  return array;
}

function base64UrlEncode(buffer: ArrayBuffer | Uint8Array): string {
  const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function arrayBufferToHex(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
}

export function generateCodeVerifier(): string {
  return base64UrlEncode(generateRandomBytes(48));
}

export function generateState(): string {
  return base64UrlEncode(generateRandomBytes(32));
}

export async function generateCodeChallenge(
  codeVerifier: string,
  platform?: TikTokPlatform
): Promise<string> {
  const targetPlatform = platform || detectPlatform();
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest('SHA-256', data);

  const challenge = targetPlatform === 'desktop'
    ? arrayBufferToHex(digest)      // HEX для Desktop
    : base64UrlEncode(digest);      // Base64URL для Web

  logger.debug(`[PKCE] Platform: ${targetPlatform}, Challenge length: ${challenge.length}`);
  return challenge;
}

export function storePKCEData(state: string, codeVerifier: string): void {
  localStorage.setItem('oauth_state', state);
  localStorage.setItem('oauth_code_verifier', codeVerifier);
  localStorage.setItem('oauth_timestamp', Date.now().toString());
}

export function retrievePKCEData(): { state: string | null; codeVerifier: string | null } {
  const state = localStorage.getItem('oauth_state');
  const codeVerifier = localStorage.getItem('oauth_code_verifier');
  localStorage.removeItem('oauth_state');
  localStorage.removeItem('oauth_code_verifier');
  localStorage.removeItem('oauth_timestamp');
  return { state, codeVerifier };
}

export async function generatePKCEPair() {
  const platform = detectPlatform();
  const state = generateState();
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier, platform);
  return { state, codeVerifier, codeChallenge, platform };
}
