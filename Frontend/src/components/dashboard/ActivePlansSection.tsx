import React from 'react';
import { PlanCard } from './PlanCard';

interface ActivePlan {
  emoji: string;
  title: string;
  progress: number;
  daysCompleted: number;
  totalDays: number;
  stepsToday: number;
  isActive: boolean;
}

const defaultActivePlans: ActivePlan[] = [
  {
    emoji: '💪',
    title: 'Fitness',
    progress: 43,
    daysCompleted: 3,
    totalDays: 7,
    stepsToday: 2,
    isActive: true,
  },
  {
    emoji: '🧠',
    title: 'Mindset',
    progress: 28,
    daysCompleted: 2,
    totalDays: 7,
    stepsToday: 3,
    isActive: true,
  },
  {
    emoji: '📚',
    title: 'Skills',
    progress: 0,
    daysCompleted: 0,
    totalDays: 7,
    stepsToday: 0,
    isActive: false,
  },
];

interface ActivePlansSectionProps {
  plans?: ActivePlan[];
  onPlanClick?: (title: string) => void;
}

export const ActivePlansSection: React.FC<ActivePlansSectionProps> = ({
  plans = defaultActivePlans,
  onPlanClick,
}) => {
  return (
    <div>
      <h3 className="mb-4 text-lg font-bold text-white">My active plans</h3>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
        {plans.map((plan) => (
          <PlanCard
            key={plan.title}
            {...plan}
            onContinue={() => onPlanClick?.(plan.title)}
          />
        ))}
      </div>
    </div>
  );
};
