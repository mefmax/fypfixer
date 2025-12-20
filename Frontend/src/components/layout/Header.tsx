import React from 'react';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../common/Button';

export const Header: React.FC = () => {
  const { user, logout } = useAuthStore();

  return (
    <header className="sticky top-0 z-40 bg-background/80 backdrop-blur-lg border-b border-white/10">
      <div className="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          FYPGlow
        </h1>

        <div className="flex items-center gap-3">
          {user?.email && (
            <span className="text-xs text-gray-400 hidden sm:block">
              {user.email}
            </span>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={logout}
          >
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
};
