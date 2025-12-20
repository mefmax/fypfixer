import { create } from 'zustand';
import type { DailyActionPlan } from '../types/action.types';
import { plansApi } from '../api/plans.api';
import { getDefaultCategoryCode } from '../lib/appConfig';
import { logger } from '../lib/logger';

interface PlanState {
  plan: DailyActionPlan | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchPlan: (categoryCode?: string, language?: string) => Promise<void>;
  completeAction: (actionId: string) => Promise<{ success: boolean; xpEarned: number; planCompleted: boolean } | null>;
  uncompleteAction: (actionId: string) => Promise<{ success: boolean } | null>;
  resetPlan: () => void;
}

export const usePlanStore = create<PlanState>((set, get) => ({
  plan: null,
  isLoading: false,
  error: null,

  fetchPlan: async (categoryCode, language = 'en') => {
    // Use default from config if not provided
    const category = categoryCode || getDefaultCategoryCode();
    set({ isLoading: true, error: null });

    try {
      const response = await plansApi.getDailyActions(category, language);

      if (response.success && response.data) {
        // SECURITY: Only log in development
        logger.debug('Plan loaded:', {
          source: response.data.metadata?.source,
          provider: response.data.metadata?.provider,
        });
        set({ plan: response.data, isLoading: false });
      } else {
        set({ error: 'Failed to load plan', isLoading: false });
      }
    } catch (error) {
      logger.error('Failed to fetch plan:', error);
      set({ error: 'Failed to load plan', isLoading: false });
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
      logger.error('Failed to complete action:', error);
      // Revert optimistic update on error
      set({
        plan: originalPlan,
        error: 'Failed to complete action. Please try again.',
      });
      return null;
    }
  },

  uncompleteAction: async (actionId: string) => {
    const { plan } = get();
    if (!plan) return null;

    // Save original state for rollback
    const originalPlan = plan;

    // Optimistic update (immediate UI feedback)
    const updatedActions = plan.actions.map((action) =>
      action.id === actionId
        ? { ...action, completed: false, completedAt: undefined }
        : action
    );

    set({ plan: { ...plan, actions: updatedActions } });

    try {
      // Call backend API
      const response = await plansApi.uncompleteAction(actionId);

      if (response.success) {
        // Update with server response
        const finalActions = plan.actions.map((action) =>
          action.id === actionId
            ? { ...action, completed: false, completedAt: undefined }
            : action
        );

        set({
          plan: { ...plan, actions: finalActions },
          error: null,
        });

        return { success: true };
      }
      return null;
    } catch (error) {
      logger.error('Failed to uncomplete action:', error);
      // Revert optimistic update on error
      set({
        plan: originalPlan,
        error: 'Failed to uncomplete action. Please try again.',
      });
      return null;
    }
  },

  resetPlan: () => {
    set({ plan: null, error: null });
  },
}));
