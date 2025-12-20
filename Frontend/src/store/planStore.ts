import { create } from 'zustand';
import type { DailyActionPlan } from '../types/action.types';
import { plansApi } from '../api/plans.api';

interface PlanState {
  plan: DailyActionPlan | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchPlan: (categoryCode?: string, language?: string) => Promise<void>;
  completeAction: (actionId: string) => Promise<{ success: boolean; xpEarned: number; planCompleted: boolean } | null>;
  resetPlan: () => void;
}

export const usePlanStore = create<PlanState>((set, get) => ({
  plan: null,
  isLoading: false,
  error: null,

  fetchPlan: async (categoryCode = 'personal_growth', language = 'en') => {
    set({ isLoading: true, error: null });

    try {
      const response = await plansApi.getDailyActions(categoryCode, language);

      if (response.success && response.data) {
        // Log AI source for debugging
        console.log('Plan loaded:', {
          source: response.data.metadata?.source,
          provider: response.data.metadata?.provider,
          motivation: response.data.motivation,
        });
        set({ plan: response.data, isLoading: false });
      } else {
        set({ error: 'Не удалось загрузить план', isLoading: false });
      }
    } catch (error) {
      console.error('Failed to fetch plan:', error);
      set({ error: 'Не удалось загрузить план', isLoading: false });
    }
  },

  completeAction: async (actionId: string) => {
    const { plan } = get();
    if (!plan) return null;

    // Save original state for rollback
    const originalPlan = plan;

    // Optimistic update (immediate UI feedback)
    const updatedActions = plan.actions.map((action) =>
      action.id === actionId
        ? { ...action, completed: true, completedAt: new Date().toISOString() }
        : action
    );

    set({ plan: { ...plan, actions: updatedActions } });

    try {
      // Call backend API
      const response = await plansApi.completeAction(actionId);

      if (response.success && response.data) {
        // Update with server response (actual completedAt timestamp)
        const finalActions = plan.actions.map((action) =>
          action.id === actionId
            ? { ...action, completed: true, completedAt: response.data.completedAt }
            : action
        );

        set({
          plan: { ...plan, actions: finalActions },
          error: null,
        });

        // Return result with XP info
        return {
          success: true,
          xpEarned: response.data.xpEarned || 0,
          planCompleted: response.data.planCompleted || false,
        };
      }
      return null;
    } catch (error) {
      console.error('Failed to complete action:', error);
      // Revert optimistic update on error
      set({
        plan: originalPlan,
        error: 'Failed to complete action. Please try again.',
      });
      return null;
    }
  },

  resetPlan: () => {
    set({ plan: null, error: null });
  },
}));
