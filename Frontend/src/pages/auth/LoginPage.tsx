import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { authApi } from '../../api/auth.api';
import { logger } from '../../lib/logger';

export const LoginPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleTikTokLogin = async () => {
    setError('');
    setIsLoading(true);
    try {
      const response = await authApi.getTikTokAuthUrl();
      if (response.success && response.data?.url) {
        // Redirect to TikTok OAuth
        window.location.href = response.data.url;
      } else {
        setError('Failed to get TikTok authorization URL');
      }
    } catch (err: unknown) {
      logger.error('Failed to get TikTok auth URL:', err);
      const axiosError = err as { response?: { data?: { error?: { message?: string } } } };
      setError(axiosError.response?.data?.error?.message || 'Failed to connect to TikTok. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-gradient-to-b from-[#0a0e27] to-[#1a1f3a]">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            FYPGlow
          </h1>
          <p className="text-gray-400 mt-2">Transform your TikTok scrolling into real progress</p>
        </div>

        {/* OAuth Buttons */}
        <div className="space-y-4">
          {error && (
            <div className="p-4 rounded-xl bg-red-500/20 border border-red-500/50 text-red-400 text-sm">
              {error}
            </div>
          )}

          {/* TikTok Login Button */}
          <button
            onClick={handleTikTokLogin}
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-3 px-6 py-4 bg-black hover:bg-gray-900 
                       text-white font-semibold rounded-xl border border-gray-700 
                       transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                {/* TikTok Icon */}
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
                </svg>
                Continue with TikTok
              </>
            )}
          </button>

          {/* Info text */}
          <p className="text-center text-gray-500 text-sm mt-6">
            By continuing, you agree to our{' '}
            <Link to="/terms" className="text-primary hover:underline">
              Terms of Service
            </Link>{' '}
            and{' '}
            <Link to="/privacy" className="text-primary hover:underline">
              Privacy Policy
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
