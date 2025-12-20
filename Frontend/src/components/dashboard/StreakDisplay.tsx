import React from 'react';
import { Flame, Trophy, Star, TrendingUp } from 'lucide-react';

interface StreakDisplayProps {
  currentStreak: number;
  longestStreak: number;
  totalXp: number;
  level: string;
  nextMilestone?: number;
}

export const StreakDisplay: React.FC<StreakDisplayProps> = ({
  currentStreak,
  longestStreak,
  totalXp,
  level,
  nextMilestone,
}) => {
  const progressToMilestone = nextMilestone
    ? Math.min((currentStreak / nextMilestone) * 100, 100)
    : 100;

  return (
    <div className="rounded-xl bg-gradient-to-br from-orange-500/20 to-red-500/20 border border-orange-500/30 p-4">
      {/* Main streak */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center">
            <Flame className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-bold text-white">{currentStreak}</span>
              <span className="text-white/60">days</span>
            </div>
            <p className="text-sm text-white/60">Current streak</p>
          </div>
        </div>

        {/* Level badge */}
        <div className="text-right">
          <div className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-white/10">
            <Star className="w-4 h-4 text-yellow-400" />
            <span className="text-sm font-medium text-white">{level}</span>
          </div>
          <p className="text-xs text-white/40 mt-1">{totalXp.toLocaleString()} XP</p>
        </div>
      </div>

      {/* Progress to next milestone */}
      {nextMilestone && (
        <div className="mb-4">
          <div className="flex justify-between text-xs text-white/60 mb-1">
            <span>To {nextMilestone}-day streak</span>
            <span>{nextMilestone - currentStreak} days</span>
          </div>
          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-orange-500 to-red-500 rounded-full transition-all duration-500"
              style={{ width: `${progressToMilestone}%` }}
            />
          </div>
        </div>
      )}

      {/* Stats row */}
      <div className="grid grid-cols-2 gap-3">
        <div className="flex items-center gap-2 p-2 rounded-lg bg-white/5">
          <Trophy className="w-4 h-4 text-yellow-400" />
          <div>
            <p className="text-xs text-white/60">Record</p>
            <p className="text-sm font-semibold text-white">{longestStreak} days</p>
          </div>
        </div>
        <div className="flex items-center gap-2 p-2 rounded-lg bg-white/5">
          <TrendingUp className="w-4 h-4 text-green-400" />
          <div>
            <p className="text-xs text-white/60">Total XP</p>
            <p className="text-sm font-semibold text-white">{totalXp.toLocaleString()}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
