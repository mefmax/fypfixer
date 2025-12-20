import React from 'react';
import { clsx } from 'clsx';
import { Card } from '../common/Card';
import { Button } from '../common/Button';

interface PlanCardProps {
  emoji: string;
  title: string;
  progress: number;
  daysCompleted: number;
  totalDays: number;
  stepsToday: number;
  isActive?: boolean;
  onContinue?: () => void;
}

export const PlanCard: React.FC<PlanCardProps> = ({
  emoji,
  title,
  progress,
  daysCompleted,
  totalDays,
  stepsToday,
  isActive = true,
  onContinue,
}) => {
  return (
    <Card
      className={clsx(
        'group border-slate-700 bg-slate-900/60 p-4 transition-all duration-200',
        'hover:border-teal-500/50 hover:-translate-y-0.5 hover:shadow-md hover:shadow-teal-500/10'
      )}
    >
      {/* Header */}
      <div className="mb-3 flex items-center gap-2">
        <span className="text-2xl">{emoji}</span>
        <h4 className="font-semibold text-white">{title}</h4>
      </div>

      {/* Progress */}
      <p className="mb-2 text-xs text-slate-400">
        {daysCompleted} / {totalDays} days completed
      </p>
      <div className="mb-3 h-1.5 overflow-hidden rounded-full bg-slate-700">
        <div
          className="h-full rounded-full bg-gradient-to-r from-teal-600 to-teal-500 transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Stats Row */}
      <div className="mb-4 flex items-center justify-between text-xs">
        <span className="text-slate-400">{progress}% complete</span>
        <span className="text-teal-400">+{stepsToday} steps today</span>
      </div>

      {/* Button */}
      <Button
        size="sm"
        onClick={onContinue}
        className={clsx(
          'w-full',
          isActive ? 'bg-slate-800 text-white hover:bg-slate-700' : 'bg-orange-500 text-white hover:bg-orange-600'
        )}
      >
        {isActive ? 'Continue plan' : 'Start plan'}
      </Button>
    </Card>
  );
};
