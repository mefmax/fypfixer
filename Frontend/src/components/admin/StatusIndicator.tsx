import React from 'react';
import clsx from 'clsx';

type Status = 'ok' | 'warning' | 'error';

interface StatusIndicatorProps {
  label: string;
  value: string | number;
  status: Status;
  loading?: boolean;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  label,
  value,
  status,
  loading = false,
}) => {
  const statusColors = {
    ok: 'bg-green-500',
    warning: 'bg-amber-500',
    error: 'bg-red-500',
  };

  if (loading) {
    return (
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-slate-600 animate-pulse" />
        <span className="text-sm text-slate-400">{label}:</span>
        <div className="w-12 h-4 bg-slate-700/50 rounded animate-pulse" />
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <div className={clsx('w-2 h-2 rounded-full', statusColors[status])} />
      <span className="text-sm text-slate-400">{label}:</span>
      <span className="text-sm font-medium text-white">{value}</span>
    </div>
  );
};
