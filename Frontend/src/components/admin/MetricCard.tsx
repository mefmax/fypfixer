import React from 'react';
import clsx from 'clsx';

interface MetricCardProps {
  label: string;
  value: number | string;
  subtext?: string;
  loading?: boolean;
  variant?: 'default' | 'highlight';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  subtext,
  loading = false,
  variant = 'default',
}) => {
  return (
    <div
      className={clsx(
        'rounded-xl p-4 text-center',
        variant === 'highlight'
          ? 'bg-teal-500/20 border border-teal-500/30'
          : 'bg-slate-800/50 border border-slate-700/50'
      )}
    >
      <p className="text-xs text-slate-400 uppercase tracking-wide mb-1">{label}</p>
      {loading ? (
        <div className="h-8 bg-slate-700/50 rounded animate-pulse w-16 mx-auto" />
      ) : (
        <p
          className={clsx(
            'text-2xl font-bold',
            variant === 'highlight' ? 'text-teal-400' : 'text-white'
          )}
        >
          {typeof value === 'number' ? value.toLocaleString() : value}
        </p>
      )}
      {subtext && <p className="text-xs text-slate-500 mt-1">{subtext}</p>}
    </div>
  );
};
