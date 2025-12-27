import React from 'react';
import clsx from 'clsx';

interface ProgressBarProps {
  label: string;
  percent: number;
  loading?: boolean;
  color?: 'teal' | 'amber' | 'rose';
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  label,
  percent,
  loading = false,
  color = 'teal',
}) => {
  const colorClasses = {
    teal: 'bg-teal-500',
    amber: 'bg-amber-500',
    rose: 'bg-rose-500',
  };

  if (loading) {
    return (
      <div className="flex items-center gap-3">
        <span className="w-24 text-sm text-slate-400">{label}</span>
        <div className="flex-1 h-4 bg-slate-700/50 rounded animate-pulse" />
        <span className="w-12" />
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <span className="w-24 text-sm text-slate-400">{label}</span>
      <div className="flex-1 h-4 bg-slate-700/30 rounded-full overflow-hidden">
        <div
          className={clsx('h-full rounded-full transition-all duration-500', colorClasses[color])}
          style={{ width: `${Math.min(percent, 100)}%` }}
        />
      </div>
      <span className="w-12 text-right text-sm font-medium text-white">{percent}%</span>
    </div>
  );
};
