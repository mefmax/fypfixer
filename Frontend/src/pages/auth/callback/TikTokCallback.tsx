import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authApi } from '../../../api/auth.api';
import { useAuthStore } from '../../../store/authStore';
import { logger } from '../../../lib/logger';

export const TikTokCallback: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [error, setError] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(true);
  const { setUser, checkOnboardingStatus } = useAuthStore();

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const errorParam = searchParams.get('error');
      const errorDescription = searchParams.get('error_description');

      // Handle TikTok errors
      if (errorParam) {
        logger.error('TikTok OAuth error:', errorParam, errorDescription);
        setError(errorDescription || 'TikTok authentication was cancelled or failed');
        setIsProcessing(false);
        return;
      }

      // Validate required params
      if (!code || !state) {
        logger.error('Missing OAuth parameters:', { code: !!code, state: !!state });
        setError('Invalid callback - missing authorization code');
        setIsProcessing(false);
        return;
      }

      try {
        // Exchange code for tokens
        const response = await authApi.handleTikTokCallback(code, state);

        if (response.success && response.data) {
          // Store tokens
          localStorage.setItem('access_token', response.data.access_token);
          if (response.data.refresh_token) {
            localStorage.setItem('refresh_token', response.data.refresh_token);
          }

          // Store user info in auth store
          const user = {
            id: response.data.user.id,
            client_id: '',
            email: null,
            display_name: response.data.user.display_name,
            avatar_url: response.data.user.avatar_url,
            oauth_provider: response.data.user.oauth_provider,
            language: 'en',
            is_premium: response.data.user.is_premium,
            created_at: null,
          };
          setUser(user);

          // Check onboarding status
          await checkOnboardingStatus();

          // Redirect based on onboarding status
          const { hasCompletedOnboarding } = useAuthStore.getState();
          if (hasCompletedOnboarding) {
            navigate('/dashboard', { replace: true });
          } else {
            navigate('/onboarding', { replace: true });
          }
        } else {
          throw new Error('Invalid response from server');
        }
      } catch (err: any) {
        logger.error('OAuth callback failed:', err);
        const message = err.response?.data?.error?.message || 'Authentication failed. Please try again.';
        setError(message);
        setIsProcessing(false);
      }
    };

    handleCallback();
  }, [searchParams, navigate, setUser, checkOnboardingStatus]);

  const handleRetry = () => {
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-gradient-to-b from-[#0a0e27] to-[#1a1f3a]">
      <div className="w-full max-w-md text-center">
        {isProcessing ? (
          <>
            {/* Loading spinner */}
            <div className="w-16 h-16 mx-auto mb-6 border-4 border-primary border-t-transparent rounded-full animate-spin" />
            <h2 className="text-xl font-semibold text-white mb-2">
              Connecting your TikTok account...
            </h2>
            <p className="text-gray-400">
              Please wait while we complete the authentication
            </p>
          </>
        ) : (
          <>
            {/* Error state */}
            <div className="w-16 h-16 mx-auto mb-6 bg-red-500/20 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-white mb-2">
              Authentication Failed
            </h2>
            <p className="text-red-400 mb-6">
              {error}
            </p>
            <button
              onClick={handleRetry}
              className="px-6 py-3 bg-primary hover:bg-primary/80 text-white font-semibold rounded-xl transition-colors"
            >
              Try Again
            </button>
          </>
        )}
      </div>
    </div>
  );
};
