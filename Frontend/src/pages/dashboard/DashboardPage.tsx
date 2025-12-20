import React, { useEffect, useState, useCallback } from 'react';
import { Header } from '../../components/layout/Header';
import { DailyPlanView } from '../../components/dashboard/DailyPlanView';
import { StreakDisplay } from '../../components/dashboard/StreakDisplay';
import { CategoryPicker } from '../../components/dashboard/CategoryPicker';
import { Toast } from '../../components/ui/Toast';
import { usePlanStore } from '../../store/planStore';
import { userApi, type StreakInfo } from '../../api/user.api';
import { useAuthStore } from '../../store/authStore';
import { STORAGE_KEYS } from '../../lib/constants';

export const DashboardPage: React.FC = () => {
  const { plan, isLoading, error, fetchPlan, completeAction, uncompleteAction } = usePlanStore();
  const { isAuthenticated } = useAuthStore();

  const [showErrorToast, setShowErrorToast] = useState(false);
  const [showCategoryPicker, setShowCategoryPicker] = useState(false);
  const [streakInfo, setStreakInfo] = useState<StreakInfo | null>(null);
  const [xpToast, setXpToast] = useState<{ show: boolean; amount: number }>({
    show: false,
    amount: 0,
  });

  // Get saved category or default
  const [currentCategory, setCurrentCategory] = useState(() => {
    return localStorage.getItem(STORAGE_KEYS.CATEGORY) || 'personal_growth';
  });

  // Load plan on mount and category change
  useEffect(() => {
    fetchPlan(currentCategory, 'en');
  }, [fetchPlan, currentCategory]);

  // Load streak info if authenticated
  useEffect(() => {
    if (isAuthenticated) {
      loadStreakInfo();
    }
  }, [isAuthenticated]);

  const loadStreakInfo = useCallback(async () => {
    try {
      const response = await userApi.getStreak();
      if (response.success && response.data) {
        setStreakInfo(response.data);
      }
    } catch (error) {
      console.error('Failed to load streak info:', error);
    }
  }, []);

  // Show toast when error occurs
  useEffect(() => {
    if (error && plan) {
      setShowErrorToast(true);
    }
  }, [error, plan]);

  const handleOpenTikTok = (url: string) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const handleChangeCategory = () => {
    setShowCategoryPicker(true);
  };

  const handleCategorySelect = (categoryCode: string) => {
    setCurrentCategory(categoryCode);
    localStorage.setItem(STORAGE_KEYS.CATEGORY, categoryCode);
    // Plan will reload via useEffect
  };

  const handleCompleteAction = async (actionId: string) => {
    const result = await completeAction(actionId);

    // Show XP toast if earned
    if (result?.xpEarned) {
      setXpToast({ show: true, amount: result.xpEarned });
      // Refresh streak info
      if (isAuthenticated) {
        loadStreakInfo();
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-background-secondary">
      <Header />

      <main className="max-w-lg mx-auto px-4 py-6 space-y-6">
        {/* Streak Display (only if authenticated and has data) */}
        {isAuthenticated && streakInfo && (
          <StreakDisplay
            currentStreak={streakInfo.currentStreak}
            longestStreak={streakInfo.longestStreak}
            totalXp={streakInfo.totalXp}
            level={streakInfo.level}
            nextMilestone={streakInfo.nextMilestone ?? undefined}
          />
        )}

        {/* Loading */}
        {isLoading && (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="animate-spin w-10 h-10 border-4 border-primary border-t-transparent rounded-full mb-4" />
            <p className="text-white/60">Generating your plan...</p>
          </div>
        )}

        {/* Error - only show if plan failed to load */}
        {error && !plan && (
          <div className="p-4 rounded-xl bg-red-500/20 border border-red-500/50 text-red-400 text-center">
            {error}
            <button
              onClick={() => fetchPlan(currentCategory, 'en')}
              className="block mx-auto mt-3 text-sm underline hover:no-underline"
            >
              Try again
            </button>
          </div>
        )}

        {/* Plan */}
        {plan && !isLoading && (
          <DailyPlanView
            plan={plan}
            onComplete={handleCompleteAction}
            onUncomplete={async (actionId) => {
              await uncompleteAction(actionId);
            }}
            onOpenTikTok={handleOpenTikTok}
            onChangeCategory={handleChangeCategory}
          />
        )}
      </main>

      {/* Category Picker Modal */}
      <CategoryPicker
        isOpen={showCategoryPicker}
        currentCategory={currentCategory}
        onSelect={handleCategorySelect}
        onClose={() => setShowCategoryPicker(false)}
      />

      {/* Error Toast */}
      {showErrorToast && error && (
        <Toast
          message={error}
          type="error"
          onClose={() => setShowErrorToast(false)}
        />
      )}

      {/* XP Earned Toast */}
      {xpToast.show && (
        <Toast
          message={`+${xpToast.amount} XP!`}
          type="success"
          onClose={() => setXpToast({ show: false, amount: 0 })}
        />
      )}
    </div>
  );
};
