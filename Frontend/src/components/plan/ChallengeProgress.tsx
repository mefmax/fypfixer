/**
 * ChallengeProgress Component - Shows "Day X of 7" progress
 *
 * Displays the user's progress through the 7-day challenge
 * with visual day indicators and signal counts.
 */
import React from 'react';
import { clsx } from 'clsx';
import type { SignalsState } from '../../types/planV2.types';

interface DayIndicatorProps {
  day: number;
  isCurrent: boolean;
  isCompleted: boolean;
}

const DayIndicator: React.FC<DayIndicatorProps> = ({ day, isCurrent, isCompleted }) => {
  return (
    <div
      className={clsx(
        'w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium transition-all',
        isCompleted
          ? 'bg-green-500 text-white'
          : isCurrent
          ? 'bg-primary text-white ring-2 ring-primary/50 ring-offset-2 ring-offset-gray-900'
          : 'bg-gray-700 text-gray-500'
      )}
    >
      {isCompleted ? (
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
      ) : (
        day
      )}
    </div>
  );
};

interface ChallengeProgressProps {
  currentDay: number;
  totalDays?: number;
  signals?: SignalsState;
  compact?: boolean;
}

export const ChallengeProgress: React.FC<ChallengeProgressProps> = ({
  currentDay,
  totalDays = 7,
  signals,
  compact = false,
}) => {
  const progressPercent = Math.round(((currentDay - 1) / totalDays) * 100);
  const totalSignals = signals
    ? signals.blocks + signals.watchesFull + signals.likes + signals.follows + signals.shares
    : 0;

  if (compact) {
    return (
      <div className="bg-white/5 rounded-xl p-4">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="text-lg font-semibold text-white">
              Day {currentDay} of {totalDays}
            </h3>
            <p className="text-sm text-gray-400">7-Day Challenge</p>
          </div>
          {signals && totalSignals > 0 && (
            <div className="text-right">
              <p className="text-lg font-semibold text-primary">+{totalSignals}</p>
              <p className="text-xs text-gray-500">signals today</p>
            </div>
          )}
        </div>

        {/* Progress bar */}
        <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white/5 rounded-xl p-6">
      {/* Header */}
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-1">
          Day {currentDay} of {totalDays}
        </h2>
        <p className="text-gray-400">
          {currentDay === 1
            ? "Let's start your journey!"
            : currentDay === totalDays
            ? 'Final day - finish strong!'
            : `${totalDays - currentDay} days remaining`}
        </p>
      </div>

      {/* Day indicators */}
      <div className="flex justify-center items-center gap-2 mb-6">
        {Array.from({ length: totalDays }).map((_, index) => {
          const day = index + 1;
          return (
            <React.Fragment key={day}>
              <DayIndicator
                day={day}
                isCurrent={day === currentDay}
                isCompleted={day < currentDay}
              />
              {day < totalDays && (
                <div
                  className={clsx(
                    'w-4 h-0.5',
                    day < currentDay ? 'bg-green-500' : 'bg-gray-700'
                  )}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Progress bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-400">Progress</span>
          <span className="text-white font-medium">{progressPercent}%</span>
        </div>
        <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-primary via-secondary to-green-400 transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Signal stats */}
      {signals && (
        <div className="grid grid-cols-5 gap-2">
          <div className="bg-white/5 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-red-400">{signals.blocks}</p>
            <p className="text-xs text-gray-500">Blocks</p>
          </div>
          <div className="bg-white/5 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-green-400">{signals.watchesFull}</p>
            <p className="text-xs text-gray-500">Watches</p>
          </div>
          <div className="bg-white/5 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-pink-400">{signals.likes}</p>
            <p className="text-xs text-gray-500">Likes</p>
          </div>
          <div className="bg-white/5 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-blue-400">{signals.follows}</p>
            <p className="text-xs text-gray-500">Follows</p>
          </div>
          <div className="bg-white/5 rounded-lg p-3 text-center">
            <p className="text-lg font-bold text-purple-400">{signals.shares}</p>
            <p className="text-xs text-gray-500">Shares</p>
          </div>
        </div>
      )}

      {/* Motivational message */}
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-400">
          {currentDay <= 2 && "Building momentum - keep going!"}
          {currentDay === 3 && "Day 3 unlocked! Share with friends now."}
          {currentDay === 4 && "Halfway there! Your algorithm is improving."}
          {currentDay >= 5 && currentDay < 7 && "Almost there! Stay consistent."}
          {currentDay === 7 && "Final day! Complete the challenge!"}
        </p>
      </div>
    </div>
  );
};

export default ChallengeProgress;
