import React from 'react';
import { Check } from 'lucide-react';
import { clsx } from 'clsx';

export interface ChecklistItemData {
  id: string;
  icon: string;
  title: string;
  description: string;
  duration: string;
}

interface ChecklistItemProps extends ChecklistItemData {
  isCompleted: boolean;
  onToggle: (id: string) => void;
}

export const ChecklistItem: React.FC<ChecklistItemProps> = ({
  id,
  icon,
  title,
  description,
  duration,
  isCompleted,
  onToggle,
}) => {
  return (
    <button
      onClick={() => onToggle(id)}
      className={clsx(
        'group flex w-full items-center gap-3 rounded-xl border p-3 text-left transition-all duration-200 min-h-[64px] cursor-pointer',
        'focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900',
        isCompleted
          ? 'border-teal-500/40 bg-teal-500/10'
          : 'border-slate-700 bg-slate-800/30 hover:border-teal-500/50 hover:bg-slate-800/60 hover:-translate-y-0.5 hover:shadow-md hover:shadow-teal-500/10 active:translate-y-0 active:bg-slate-800/80'
      )}
    >
      {/* Check Circle */}
      <div
        className={clsx(
          'flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 transition-all duration-200',
          isCompleted ? 'border-teal-500 bg-teal-500' : 'border-slate-600 group-hover:border-teal-500/50'
        )}
      >
        {isCompleted && <Check className="h-3 w-3 stroke-[3] text-slate-900" />}
      </div>

      {/* Icon */}
      <span className={clsx('text-lg transition-opacity', isCompleted && 'opacity-70')}>{icon}</span>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <h4
          className={clsx('font-medium text-sm transition-all', isCompleted ? 'text-slate-300 opacity-80' : 'text-white')}
        >
          {title}
        </h4>
        <p
          className={clsx(
            'text-xs transition-all leading-relaxed line-clamp-1',
            isCompleted ? 'text-slate-500 opacity-80' : 'text-slate-400'
          )}
        >
          {description}
        </p>
      </div>

      {/* Time Badge & Done Badge */}
      <div className="flex shrink-0 items-center gap-2">
        {isCompleted && (
          <span className="rounded-full border border-teal-500/50 bg-teal-500/10 px-2 py-0.5 text-[10px] font-medium text-teal-400">
            Done
          </span>
        )}
        <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-300">{duration}</span>
      </div>
    </button>
  );
};
