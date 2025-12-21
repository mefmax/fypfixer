import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Check,
  ClipboardList,
  TrendingUp,
  Sparkles,
  Brain,
  Clock,
  Heart,
  Ban,
  Zap,
  Target,
  Volume2,
  Film,
} from 'lucide-react';
import { clsx } from 'clsx';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { useAuthStore } from '../../store/authStore';
import { preferencesApi } from '../../api/preferences.api';
import { logger } from '../../lib/logger';

interface Goal {
  id: string;
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  category: 'more' | 'less';
}

const goals: Goal[] = [
  {
    id: 'more-educational',
    icon: Brain,
    title: 'More educational content',
    description: 'Learn new skills, facts, and insights',
    category: 'more',
  },
  {
    id: 'less-doomscroll',
    icon: Clock,
    title: 'Less doomscrolling',
    description: 'Break the endless scroll habit',
    category: 'less',
  },
  {
    id: 'more-inspiration',
    icon: Sparkles,
    title: 'More creative inspiration',
    description: 'Fuel your creativity with fresh ideas',
    category: 'more',
  },
  {
    id: 'less-negativity',
    icon: Ban,
    title: 'Less negativity',
    description: 'Filter out toxic or draining content',
    category: 'less',
  },
  {
    id: 'more-motivation',
    icon: Zap,
    title: 'More motivation',
    description: 'Content that energizes and inspires action',
    category: 'more',
  },
  {
    id: 'niche-focus',
    icon: Target,
    title: 'Focus on my niche',
    description: 'Train the algorithm for your interests',
    category: 'more',
  },
  {
    id: 'less-noise',
    icon: Volume2,
    title: 'Less random noise',
    description: 'Cut down on irrelevant recommendations',
    category: 'less',
  },
  {
    id: 'more-wellness',
    icon: Heart,
    title: 'More wellness content',
    description: 'Mental health, fitness, and self-care',
    category: 'more',
  },
];

const howItWorks = [
  {
    icon: Check,
    title: 'Pick your goals',
    description: 'Tell us what you want more or less of in your FYP.',
  },
  {
    icon: ClipboardList,
    title: 'Get a plan',
    description: 'We generate a personalized action plan for your feed.',
  },
  {
    icon: TrendingUp,
    title: 'Follow daily steps',
    description: 'Complete simple manual actions and track progress.',
  },
];

export const GoalsOnboardingPage: React.FC = () => {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [selectedGoals, setSelectedGoals] = useState<string[]>([]);

  const toggleGoal = (goalId: string) => {
    setSelectedGoals((prev) => {
      if (prev.includes(goalId)) {
        return prev.filter((id) => id !== goalId);
      }
      if (prev.length >= 3) {
        return prev;
      }
      return [...prev, goalId];
    });
  };

  const canContinue = selectedGoals.length >= 1 && selectedGoals.length <= 3;

  // Helper to map goals to category
  const determineCategoryFromGoals = (goalIds: string[]): string => {
    const goalToCategory: Record<string, string> = {
      'more-educational': 'books',
      'more-inspiration': 'art',
      'more-motivation': 'fitness',
      'more-wellness': 'wellness',
      'niche-focus': 'fitness',
      'less-doomscroll': 'fitness',
      'less-negativity': 'wellness',
      'less-noise': 'fitness',
    };

    const categories = goalIds.map(id => goalToCategory[id] || 'fitness');
    const counts = categories.reduce((acc, cat) => {
      acc[cat] = (acc[cat] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || 'fitness';
  };

  const handleContinue = async () => {
    if (!canContinue) return;

    // Store in localStorage for PlanPreviewPage
    const selectedGoalObjects = goals.filter((g) => selectedGoals.includes(g.id));
    localStorage.setItem('selectedGoals', JSON.stringify(selectedGoalObjects));
    localStorage.setItem('fypfixer_category', determineCategoryFromGoals(selectedGoals));

    // If authenticated, save to backend too
    if (user) {
      try {
        await preferencesApi.update({
          selectedGoals,
          preferredCategory: determineCategoryFromGoals(selectedGoals),
        });
      } catch (error) {
        logger.error('Failed to save preferences:', error);
        // Continue anyway - localStorage is backup
      }
    }

    navigate('/onboarding/plan-preview');
  };

  const handleSkip = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900">
      <div className="mx-auto max-w-[960px] px-4 py-8 sm:px-6 lg:px-8">
        {/* Header Section */}
        <div className="mb-10 text-center">
          {/* Logo */}
          <div className="mb-6 flex items-center justify-center gap-2">
            <Film className="h-7 w-7 text-teal-400" />
            <span className="text-xl font-semibold text-white">FYPGlow</span>
          </div>

          {/* Welcome Text */}
          <h1 className="mb-2 text-3xl font-bold text-white sm:text-4xl">Welcome to FYPGlow</h1>
          {user?.display_name ? (
            <p className="mb-4 text-lg text-slate-300">Nice to meet you, {user.display_name} 👋</p>
          ) : (
            <p className="mb-4 text-lg text-slate-300">Let's retrain your TikTok feed the right way.</p>
          )}
          <p className="mx-auto max-w-xl text-slate-400">
            Tell us what you want to glow up in your FYP and we'll build a step-by-step action plan tailored to you.
          </p>
        </div>

        {/* How It Works Section */}
        <div className="mb-10">
          <p className="mb-4 text-center text-xs font-semibold uppercase tracking-wider text-teal-400">
            How FYPGlow works
          </p>
          <div className="grid gap-4 sm:grid-cols-3">
            {howItWorks.map((step, index) => {
              const IconComponent = step.icon;
              return (
                <Card key={index} className="border-slate-800 bg-slate-900/50 p-4 text-center">
                  <div className="mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-teal-500/10">
                    <IconComponent className="h-5 w-5 text-teal-400" />
                  </div>
                  <h3 className="mb-1 font-semibold text-white">{step.title}</h3>
                  <p className="text-sm text-slate-400">{step.description}</p>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Goal Selection Section */}
        <div className="mb-8">
          <h2 className="mb-2 text-center text-xl font-semibold text-white sm:text-2xl">
            What's your main goal with TikTok?
          </h2>
          <p className="mb-6 text-center text-sm text-slate-400">
            Choose 1–3 goals that matter most to you. You can always change these later.
          </p>

          <div className="grid gap-3 sm:grid-cols-2">
            {goals.map((goal) => {
              const isSelected = selectedGoals.includes(goal.id);
              const isDisabled = !isSelected && selectedGoals.length >= 3;
              const IconComponent = goal.icon;

              return (
                <button
                  key={goal.id}
                  onClick={() => toggleGoal(goal.id)}
                  disabled={isDisabled}
                  className={clsx(
                    'group relative flex items-start gap-4 rounded-xl border p-4 text-left transition-all',
                    isSelected
                      ? 'border-orange-500 bg-orange-500/10'
                      : 'border-slate-700 bg-slate-800/50 hover:border-slate-600 hover:bg-slate-800',
                    isDisabled && 'cursor-not-allowed opacity-50'
                  )}
                >
                  {/* Selection indicator */}
                  <div
                    className={clsx(
                      'flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 transition-all',
                      isSelected ? 'border-orange-500 bg-orange-500' : 'border-slate-600'
                    )}
                  >
                    {isSelected && <Check className="h-3 w-3 text-white" />}
                  </div>

                  {/* Icon */}
                  <div
                    className={clsx(
                      'flex h-10 w-10 shrink-0 items-center justify-center rounded-lg transition-colors',
                      isSelected ? 'bg-orange-500/20' : 'bg-slate-700/50',
                      goal.category === 'more' ? 'text-teal-400' : 'text-orange-400'
                    )}
                  >
                    <IconComponent className="h-5 w-5" />
                  </div>

                  {/* Content */}
                  <div className="flex-1">
                    <h3 className="font-medium text-white">{goal.title}</h3>
                    <p className="text-sm text-slate-400">{goal.description}</p>
                  </div>

                  {/* Category badge */}
                  <span
                    className={clsx(
                      'absolute right-3 top-3 rounded-full px-2 py-0.5 text-xs font-medium',
                      goal.category === 'more'
                        ? 'bg-teal-500/10 text-teal-400'
                        : 'bg-orange-500/10 text-orange-400'
                    )}
                  >
                    {goal.category === 'more' ? 'More' : 'Less'}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Selection Counter */}
        <div className="mb-6 text-center">
          <p className="text-sm text-slate-400">
            {selectedGoals.length === 0 && 'Select at least 1 goal to continue'}
            {selectedGoals.length === 1 && '1 goal selected — you can pick up to 2 more'}
            {selectedGoals.length === 2 && '2 goals selected — you can pick 1 more'}
            {selectedGoals.length === 3 && '3 goals selected — maximum reached'}
          </p>
        </div>

        {/* CTA Button */}
        <div className="flex justify-center">
          <Button
            size="lg"
            disabled={!canContinue}
            onClick={handleContinue}
            className={clsx(
              'min-w-[200px] text-base font-semibold transition-all',
              canContinue
                ? 'bg-orange-500 text-white hover:bg-orange-600'
                : 'bg-slate-700 text-slate-400 cursor-not-allowed'
            )}
          >
            Continue to My Plan →
          </Button>
        </div>

        {/* Skip Link */}
        <div className="mt-4 text-center">
          <button
            onClick={handleSkip}
            className="text-sm text-slate-500 underline-offset-2 hover:text-slate-400 hover:underline"
          >
            Skip for now
          </button>
        </div>
      </div>
    </div>
  );
};
