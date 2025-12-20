import React from 'react';
import type { DailyActionPlan } from '../../types/action.types';
import { ProgressTracker } from '../plan/ProgressTracker';
import { ActionList } from './ActionList';

interface DailyPlanViewProps {
  plan: DailyActionPlan;
  onComplete: (actionId: string) => Promise<void>;
  onUncomplete?: (actionId: string) => Promise<void>;
  onOpenTikTok: (url: string) => void;
  onChangeCategory?: () => void;
}

export const DailyPlanView: React.FC<DailyPlanViewProps> = ({
  plan,
  onComplete,
  onUncomplete,
  onOpenTikTok,
  onChangeCategory,
}) => {
  const positiveActions = plan.actions.filter((a) => a.category === 'positive');
  const negativeActions = plan.actions.filter((a) => a.category === 'negative');

  const completedCount = plan.actions.filter((a) => a.completed).length;
  const totalCount = plan.actions.length;

  return (
    <div className="space-y-6">
      {/* Hero */}
      <div className="text-center">
        <h1 className="text-2xl font-bold text-white mb-2">
          Your TikTok plan for today
        </h1>
        <p className="text-white/60">
          {totalCount} actions to retrain your FYP
        </p>
        {onChangeCategory && (
          <button
            onClick={onChangeCategory}
            className="mt-2 text-teal-400 text-sm hover:underline"
          >
            {plan.categoryName} — change
          </button>
        )}
      </div>

      {/* Motivation message from AI */}
      {plan.motivation && (
        <div className="text-center p-4 rounded-xl bg-gradient-to-r from-primary/20 to-secondary/20 border border-primary/30">
          <p className="text-lg text-white font-medium">{plan.motivation}</p>
        </div>
      )}

      {/* Progress */}
      <ProgressTracker total={totalCount} completed={completedCount} />

      {/* Positive actions */}
      <ActionList
        title="✅ Add to your feed"
        actions={positiveActions}
        onComplete={onComplete}
        onUncomplete={onUncomplete}
        onOpenTikTok={onOpenTikTok}
      />

      {/* Negative actions */}
      <ActionList
        title="🚫 Remove from your feed"
        actions={negativeActions}
        onComplete={onComplete}
        onUncomplete={onUncomplete}
      />

      {/* Footer motivation */}
      <div className="text-center py-4 border-t border-white/10">
        <p className="text-white/40 text-sm">
          Follow the plan for 7 days — and TikTok will start showing what truly matters to you
        </p>
      </div>
    </div>
  );
};
