import React from 'react';
import { clsx } from 'clsx';

interface ProgressTrackerProps {
  total: number;
  completed: number;
}

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({ total, completed }) => {
  const percentage = total > 0 ? (completed / total) * 100 : 0;

  return (
    <div className="bg-white/5 border border-primary/20 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-white">Daily Progress</h3>
        <span className="text-xs text-gray-400">
          {completed}/{total} completed
        </span>
      </div>

      {/* Checkboxes */}
      <div className="flex gap-2 mb-3">
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            className={clsx(
              'w-6 h-6 rounded-md border-2 flex items-center justify-center transition-all',
              i < completed
                ? 'bg-green-500 border-green-500 text-white'
                : 'border-gray-600 bg-transparent'
            )}
          >
            {i < completed && '✓'}
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-primary to-green-500 rounded-full transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Motivation text */}
      <p className="text-xs text-gray-500 mt-3">
        {completed === 0 && "Ready to start? Let's go! 💪"}
        {completed > 0 && completed < total && "Great progress! Keep going! 🔥"}
        {completed === total && "Amazing! Day complete! 🎉"}
      </p>
    </div>
  );
};
