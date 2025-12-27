/**
 * DailyPlanViewV2 Component - Container for the 3-step daily plan
 *
 * Orchestrates the flow between:
 * 1. CLEAR (Detox) - Block toxic creators
 * 2. WATCH - Watch curated videos
 * 3. REINFORCE - Rewatch favorite + Share
 */
import React, { useState, useEffect } from 'react';
import { clsx } from 'clsx';
import { usePlanStoreV2 } from '../../store/planStoreV2';
import { ClearStep } from './ClearStep';
import { WatchStep } from './WatchStep';
import { ReinforceStep } from './ReinforceStep';
import { ShareModal } from './ShareModal';
import { ChallengeProgress } from './ChallengeProgress';
import { Button } from '../common/Button';


interface StepIndicatorProps {
  step: 1 | 2 | 3;
  label: string;
  icon: React.ReactNode;
  isActive: boolean;
  isCompleted: boolean;
}

const StepIndicator: React.FC<StepIndicatorProps> = ({
  step: _step,
  label,
  icon,
  isActive,
  isCompleted,
}) => {
  return (
    <div className="flex flex-col items-center">
      <div
        className={clsx(
          'w-10 h-10 rounded-full flex items-center justify-center transition-all',
          isCompleted
            ? 'bg-green-500 text-white'
            : isActive
            ? 'bg-primary text-white ring-2 ring-primary/50'
            : 'bg-gray-700 text-gray-400'
        )}
      >
        {isCompleted ? (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        ) : (
          icon
        )}
      </div>
      <span
        className={clsx(
          'mt-2 text-xs font-medium',
          isActive ? 'text-white' : 'text-gray-500'
        )}
      >
        {label}
      </span>
    </div>
  );
};

interface StepConnectorProps {
  isCompleted: boolean;
}

const StepConnector: React.FC<StepConnectorProps> = ({ isCompleted }) => {
  return (
    <div className="flex-1 h-0.5 mx-2 mt-5">
      <div
        className={clsx(
          'h-full transition-all duration-300',
          isCompleted ? 'bg-green-500' : 'bg-gray-700'
        )}
      />
    </div>
  );
};

interface DailyPlanViewV2Props {
  category?: string;
  onPlanComplete?: () => void;
}

export const DailyPlanViewV2: React.FC<DailyPlanViewV2Props> = ({
  category = 'fitness',
  onPlanComplete,
}) => {
  const {
    plan,
    isLoading,
    error,
    currentStep,
    stepsCompleted,
    signals,
    fetchPlan,
    resetPlan,
  } = usePlanStoreV2();

  const [isShareModalOpen, setIsShareModalOpen] = useState(false);

  // Fetch plan on mount
  useEffect(() => {
    if (!plan) {
      fetchPlan(category);
    }
  }, [plan, category, fetchPlan]);

  // Handle step completion
  const handleClearComplete = () => {
    // Auto-advance to watch step
  };

  const handleWatchComplete = () => {
    // Auto-advance to reinforce step
  };

  const handleReinforceComplete = () => {
    onPlanComplete?.();
  };

  const handleShare = () => {
    setIsShareModalOpen(true);
  };

  const handleShareComplete = () => {
    // Track share completion
  };

  const handleRetry = () => {
    resetPlan();
    fetchPlan(category);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-gray-400">Loading your daily plan...</p>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center">
          <svg className="w-8 h-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-white mb-2">Failed to load plan</h3>
        <p className="text-gray-400 mb-4">{error}</p>
        <Button onClick={handleRetry}>Try Again</Button>
      </div>
    );
  }

  // No plan state
  if (!plan) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">No plan available</p>
        <Button onClick={() => fetchPlan(category)} className="mt-4">
          Generate Plan
        </Button>
      </div>
    );
  }

  // All steps complete
  if (currentStep === 'complete') {
    return (
      <div className="space-y-6">
        <ChallengeProgress
          currentDay={plan.day_of_challenge}
          totalDays={7}
          signals={signals}
        />

        <div className="text-center py-8">
          <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center">
            <svg className="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">
            Day {plan.day_of_challenge} Complete!
          </h2>
          <p className="text-gray-400 mb-6">
            Amazing work! Come back tomorrow to continue your journey.
          </p>

          {/* Stats summary */}
          <div className="grid grid-cols-3 gap-4 max-w-sm mx-auto mb-6">
            <div className="bg-white/5 rounded-xl p-4">
              <p className="text-2xl font-bold text-green-400">{signals.blocks}</p>
              <p className="text-xs text-gray-500">Blocked</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className="text-2xl font-bold text-blue-400">{signals.watchesFull}</p>
              <p className="text-xs text-gray-500">Watched</p>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <p className="text-2xl font-bold text-purple-400">{signals.shares}</p>
              <p className="text-xs text-gray-500">Shared</p>
            </div>
          </div>

          <Button onClick={onPlanComplete}>
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  // Get step number from current step
  

  return (
    <div className="space-y-6">
      {/* Challenge progress */}
      <ChallengeProgress
        currentDay={plan.day_of_challenge}
        totalDays={7}
        signals={signals}
        compact
      />

      {/* Step indicators */}
      <div className="flex items-start justify-center px-4">
        <StepIndicator
          step={1}
          label="Clear"
          icon={<span className="text-lg">🧹</span>}
          isActive={currentStep === 'clear'}
          isCompleted={stepsCompleted.clear}
        />
        <StepConnector isCompleted={stepsCompleted.clear} />
        <StepIndicator
          step={2}
          label="Watch"
          icon={<span className="text-lg">👀</span>}
          isActive={currentStep === 'watch'}
          isCompleted={stepsCompleted.watch}
        />
        <StepConnector isCompleted={stepsCompleted.watch} />
        <StepIndicator
          step={3}
          label="Reinforce"
          icon={<span className="text-lg">💪</span>}
          isActive={currentStep === 'reinforce'}
          isCompleted={stepsCompleted.reinforce}
        />
      </div>

      {/* Current step content */}
      <div className="mt-6">
        {currentStep === 'clear' && (
          <ClearStep onComplete={handleClearComplete} />
        )}
        {currentStep === 'watch' && (
          <WatchStep onComplete={handleWatchComplete} />
        )}
        {currentStep === 'reinforce' && (
          <ReinforceStep
            onComplete={handleReinforceComplete}
            onShare={handleShare}
          />
        )}
      </div>

      {/* Share Modal */}
      <ShareModal
        isOpen={isShareModalOpen}
        onClose={() => setIsShareModalOpen(false)}
        onShareComplete={handleShareComplete}
      />
    </div>
  );
};

export default DailyPlanViewV2;
