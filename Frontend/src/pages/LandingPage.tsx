import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.svg';
import { logger } from '../lib/logger';

interface LandingPageProps {
  className?: string;
}

export function LandingPage({ className = '' }: LandingPageProps) {
  const [input, setInput] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Handle form submission - navigate to register with interests
    if (input.trim()) {
      logger.debug('User interests:', input);
      // Store interests in localStorage or pass as state
      localStorage.setItem('userInterests', input);
      navigate('/auth/register');
    }
  };

  return (
    <main className={`min-h-screen bg-gradient-to-b from-[#0a0e27] to-[#1a1f3a] flex flex-col items-center justify-between p-6 ${className}`}>
      <div className="w-full max-w-[500px] flex-1 flex flex-col justify-center gap-12">
        {/* Header */}
        <header className="text-center">
          <h1 className="text-2xl font-bold text-white flex items-center justify-center gap-2">
            <img src={logo} alt="FYPGlow" className="w-8 h-8" />
            FYPGlow
          </h1>
        </header>

        {/* Hero Section */}
        <section className="text-center space-y-4">
          <h2 className="text-4xl font-bold text-white leading-tight">
            <span className="bg-gradient-to-r from-[#208E9F] to-[#FF6B35] bg-clip-text text-transparent">
              Glow up your life. Detox your feed.
            </span>
          </h2>
          <p className="text-base text-[#B0B0B0]">Get a daily plan to transform your For You page.</p>
        </section>

        {/* Input Section */}
        <section className="space-y-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="interests" className="text-sm text-white block text-left">
                What do you want to see?
              </label>
              <input
                id="interests"
                type="text"
                placeholder="personal growth, fitness, education..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="w-full h-14 px-4 bg-white/[0.04] border border-white/[0.12] rounded-xl text-sm text-white placeholder:text-white/40 focus:outline-none focus:border-[#208E9F] transition-colors"
                aria-label="Enter your interests"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full h-14 bg-gradient-to-br from-[#FF6B35] to-[#FF9F0A] text-white text-base font-bold rounded-xl shadow-[0px_0px_16px_rgba(255,107,53,0.4)] hover:shadow-[0px_0px_24px_rgba(255,107,53,0.6)] transition-shadow active:scale-[0.98] transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={!input.trim()}
            >
              Get Plan
            </button>
          </form>

          {/* Safety Message */}
          <div className="bg-[rgba(255,45,85,0.1)] border border-[rgba(255,45,85,0.3)] rounded-lg p-3">
            <p className="text-xs text-[#E0E0E0] leading-relaxed">
              <span role="img" aria-label="shield">🛡️</span> Safe: We never log in, use bots, or auto-like. Just a simple checklist for you.
            </p>
          </div>

          {/* Auth Links */}
          <div className="flex items-center justify-center gap-4 pt-2">
            <Link
              to="/auth/login"
              className="text-sm text-[#208E9F] hover:underline transition-colors"
            >
              Already have an account? Log in
            </Link>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="w-full max-w-[500px] text-center space-y-2 py-6">
        <p className="text-xs text-[#707070]">
          Made with <span role="img" aria-label="heart">❤️</span> for TikTok creators
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link to="/privacy" className="text-xs text-[#208E9F] hover:underline transition-colors">
            Privacy
          </Link>
          <Link to="/terms" className="text-xs text-[#208E9F] hover:underline transition-colors">
            Terms
          </Link>
        </div>
      </footer>
    </main>
  );
}
