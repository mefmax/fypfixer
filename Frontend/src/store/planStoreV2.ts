/**
 * Plan Store V2 - Zustand store for Plan v2.0 state
 *
 * Manages the new 3-step plan structure:
 * 1. CLEAR (Detox) - Block toxic creators
 * 2. WATCH - Watch curated videos
 * 3. REINFORCE - Rewatch favorite + Share
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { PlanV2, StepType, SignalType, SignalsState, StepsCompleted } from '../types/planV2.types';
import { plansV2Api } from '../api/plansV2.api';
import { logger } from '../lib/logger';

interface PlanV2State {
  // Current plan
  plan: PlanV2 | null;
  isLoading: boolean;
  error: string | null;

  // Step completion
  currentStep: StepType;
  stepsCompleted: StepsCompleted;

  // Signals collected (algorithm training)
  signals: SignalsState;

  // Actions
  fetchPlan: (category: string) => Promise<void>;
  completeStep: (step: 'clear' | 'watch' | 'reinforce') => void;
  addSignal: (type: SignalType, count?: number) => void;
  resetPlan: () => void;

  // Block actions
  blockCreator: (creatorUsername: string, reason?: string) => Promise<boolean>;
  blockAllCreators: () => Promise<number>;
}

const initialSignals: SignalsState = {
  blocks: 0,
  watchesFull: 0,
  likes: 0,
  follows: 0,
  shares: 0,
};

const initialStepsCompleted: StepsCompleted = {
  clear: false,
  watch: false,
  reinforce: false,
};

// Helper to determine next step
const getNextStep = (stepsCompleted: StepsCompleted): StepType => {
  if (!stepsCompleted.clear) return 'clear';
  if (!stepsCompleted.watch) return 'watch';
  if (!stepsCompleted.reinforce) return 'reinforce';
  return 'complete';
};

export const usePlanStoreV2 = create<PlanV2State>()(
  persist(
    (set, get) => ({
      // Initial state
      plan: null,
      isLoading: false,
      error: null,
      currentStep: 'clear',
      stepsCompleted: { ...initialStepsCompleted },
      signals: { ...initialSignals },

      // Fetch plan from API
      fetchPlan: async (category: string) => {
        set({ isLoading: true, error: null });

        try {
          const response = await plansV2Api.generatePlan(category);

          if (response.success && response.data) {
            const plan = response.data.plan;

            // Initialize step completion from plan data
            const stepsCompleted: StepsCompleted = {
              clear: plan.steps.clear.completed,
              watch: plan.steps.watch.completed,
              reinforce: plan.steps.reinforce.completed,
            };

            set({
              plan,
              isLoading: false,
              stepsCompleted,
              currentStep: getNextStep(stepsCompleted),
            });

            logger.debug('Plan V2 loaded:', {
              planId: plan.plan_id,
              day: plan.day_of_challenge,
            });
          } else {
            set({ error: 'Failed to load plan', isLoading: false });
          }
        } catch (error: any) {
          logger.error('Failed to fetch plan V2:', error);
          const message = error.response?.data?.error?.message || 'Failed to load plan';
          set({ error: message, isLoading: false });
        }
      },

      // Mark a step as completed
      completeStep: (step: 'clear' | 'watch' | 'reinforce') => {
        const { stepsCompleted, plan } = get();

        const newStepsCompleted = {
          ...stepsCompleted,
          [step]: true,
        };

        // Update plan's step completion
        if (plan) {
          plan.steps[step].completed = true;
        }

        set({
          stepsCompleted: newStepsCompleted,
          currentStep: getNextStep(newStepsCompleted),
        });

        logger.debug(`Step ${step} completed`);
      },

      // Add signal (algorithm training action)
      addSignal: (type: SignalType, count = 1) => {
        const { signals } = get();

        set({
          signals: {
            ...signals,
            [type]: signals[type] + count,
          },
        });

        logger.debug(`Signal added: ${type} +${count}`);
      },

      // Reset plan state
      resetPlan: () => {
        set({
          plan: null,
          error: null,
          currentStep: 'clear',
          stepsCompleted: { ...initialStepsCompleted },
          signals: { ...initialSignals },
        });
      },

      // Block a single creator
      blockCreator: async (creatorUsername: string, reason?: string) => {
        try {
          const response = await plansV2Api.blockCreator(creatorUsername, reason);

          if (response.success && response.data.blocked) {
            // Add signal for blocking
            get().addSignal('blocks');
            return true;
          }

          return false;
        } catch (error) {
          logger.error('Failed to block creator:', error);
          return false;
        }
      },

      // Block all toxic creators in the plan
      blockAllCreators: async () => {
        const { plan } = get();
        if (!plan) return 0;

        const toxicCreators = plan.steps.clear.toxic_creators;
        let blockedCount = 0;

        for (const creator of toxicCreators) {
          const success = await get().blockCreator(creator.creator_name, creator.reason);
          if (success) blockedCount++;
        }

        return blockedCount;
      },
    }),
    {
      name: 'plan-v2-storage',
      partialize: (state) => ({
        // Only persist signals for session continuity
        signals: state.signals,
        stepsCompleted: state.stepsCompleted,
      }),
    }
  )
);
