import React from 'react';
import clsx from 'clsx';

interface FunnelStep {
  day: number;
  count: number;
  percent: number;
}

interface FunnelChartProps {
  data: FunnelStep[];
  loading?: boolean;
}

export const FunnelChart: React.FC<FunnelChartProps> = ({ data, loading = false }) => {
  if (loading) {
    return (
      <div className="space-y-3">
        {[0, 1, 2, 3].map((i) => (
          <div key={i} className="flex items-center gap-3">
            <div className="w-16 h-4 bg-slate-700/50 rounded animate-pulse" />
            <div className="flex-1 h-6 bg-slate-700/50 rounded animate-pulse" />
          </div>
        ))}
      </div>
    );
  }

  const maxCount = Math.max(...data.map((d) => d.count), 1);

  return (
    <div className="space-y-3">
      {data.map((step) => (
        <div key={step.day} className="flex items-center gap-3">
          <span className="w-16 text-sm text-slate-400">
            {step.day === 0 ? 'Start' : `Day ${step.day}`}
          </span>
          <div className="flex-1 h-6 bg-slate-700/30 rounded-full overflow-hidden">
            <div
              className={clsx(
                'h-full rounded-full transition-all duration-500',
                step.day === 0
                  ? 'bg-teal-500'
                  : step.day === 7
                    ? 'bg-amber-500'
                    : 'bg-teal-500/70'
              )}
              style={{ width: `${(step.count / maxCount) * 100}%` }}
            />
          </div>
          <span className="w-12 text-right text-sm font-medium text-white">{step.percent}%</span>
        </div>
      ))}
    </div>
  );
};
