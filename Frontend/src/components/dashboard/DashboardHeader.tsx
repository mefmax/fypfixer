import React from 'react';
import { Film } from 'lucide-react';
import { Card } from '../common/Card';

interface DashboardHeaderProps {
  weekNumber?: number;
  dayNumber?: number;
  streak?: number;
  xp?: number;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  weekNumber = 1,
  dayNumber = 1,
  streak = 1,
  xp = 0,
}) => {
  const weekProgress = (dayNumber / 7) * 100;

  return (
    <header className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      {/* Left: Logo & Title */}
      <div>
        <div className="flex items-center gap-2">
          <Film className="h-6 w-6 text-teal-400" />
          <span className="text-xl font-semibold text-white">FYPGlow</span>
        </div>
        <p className="mt-1 text-sm text-slate-400">Your daily personal growth companion</p>
      </div>

      {/* Right: Weekly Progress Badge */}
      <Card className="border-teal-500/30 bg-slate-900/80 px-4 py-3">
        <div className="flex items-center gap-4">
          <div>
            <p className="text-sm font-medium text-white">
              Week {weekNumber} / 4 · Day {dayNumber} / 7
            </p>
            {/* Progress Bar */}
            <div className="mt-2 h-1.5 w-32 overflow-hidden rounded-full bg-slate-700">
              <div
                className="h-full rounded-full bg-gradient-to-r from-teal-500 to-teal-400"
                style={{ width: `${weekProgress}%` }}
              />
            </div>
          </div>
          <div className="border-l border-slate-700 pl-4">
            <p className="text-xs text-slate-500">Streak</p>
            <p className="text-sm font-medium text-teal-400">{streak} day{streak !== 1 ? 's' : ''}</p>
          </div>
          <div className="border-l border-slate-700 pl-4">
            <p className="text-xs text-slate-500">XP</p>
            <p className="text-sm font-medium text-orange-400">{xp} XP</p>
          </div>
        </div>
      </Card>
    </header>
  );
};
