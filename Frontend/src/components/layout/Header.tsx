import React from 'react';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../common/Button';

export const Header: React.FC = () => {
  const { user, logout } = useAuthStore();

  // Get display name: prefer display_name, fallback to email
  const displayName = user?.display_name || user?.email || 'User';

  return (
    <header className="sticky top-0 z-40 bg-background/80 backdrop-blur-lg border-b border-white/10">
      <div className="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          FYPGlow
        </h1>

        <div className="flex items-center gap-3">
          {/* User Avatar and Name */}
          {user && (
            <div className="flex items-center gap-2">
              {user.avatar_url ? (
                <img
                  src={user.avatar_url}
                  alt={displayName}
                  className="w-8 h-8 rounded-full object-cover border border-white/20"
                />
              ) : (
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                  <span className="text-xs font-medium text-primary">
                    {displayName.charAt(0).toUpperCase()}
                  </span>
                </div>
              )}
              <span className="text-xs text-gray-400 hidden sm:block max-w-[100px] truncate">
                {displayName}
              </span>
            </div>
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
