import React, { useState } from 'react';
import { clsx } from 'clsx';
import { Check, ExternalLink, HelpCircle, Loader2 } from 'lucide-react';
import type { PlanAction } from '../../types/action.types';
import { Tooltip } from '../common/Tooltip';

interface ActionCardProps {
  action: PlanAction;
  onComplete: (actionId: string) => Promise<void>;
  onOpenTikTok?: (url: string) => void;
}

export const ActionCard: React.FC<ActionCardProps> = ({
  action,
  onComplete,
  onOpenTikTok,
}) => {
  const { id, type, category, target, completed } = action;
  const isNegative = category === 'negative';
  const [isCompleting, setIsCompleting] = useState(false);

  const handleComplete = async () => {
    if (completed || isCompleting) return;

    setIsCompleting(true);
    try {
      await onComplete(id);
    } finally {
      setIsCompleting(false);
    }
  };

  const handleCTAClick = async () => {
    if (completed || isCompleting) return;

    if (isNegative) {
      await handleComplete();
    } else if (target.tiktokUrl && onOpenTikTok) {
      onOpenTikTok(target.tiktokUrl);
    }
  };

  const getActionLabel = (): string => {
    const labels: Record<string, string> = {
      follow: 'FOLLOW',
      like: 'LIKE',
      save: 'SAVE',
      not_interested: 'NOT INTERESTED',
    };
    return labels[type] || type.toUpperCase();
  };

  const getLabelColor = (): string => {
    const colors: Record<string, string> = {
      follow: 'text-teal-400',
      like: 'text-pink-400',
      save: 'text-yellow-400',
      not_interested: 'text-red-400',
    };
    return colors[type] || 'text-gray-400';
  };

  return (
    <div
      className={clsx(
        'rounded-xl p-4 border transition-all',
        'bg-white/[0.04] border-white/[0.08]',
        completed ? 'opacity-60 border-green-500/30' : 'hover:border-white/20'
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          {/* Checkbox */}
          <button
            onClick={handleComplete}
            disabled={completed || isCompleting}
            className={clsx(
              'w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all',
              completed
                ? 'bg-green-500 border-green-500'
                : 'border-white/30 hover:border-teal-500',
              isCompleting && 'opacity-50 cursor-wait'
            )}
          >
            {isCompleting ? (
              <Loader2 className="w-4 h-4 text-white animate-spin" />
            ) : completed ? (
              <Check className="w-4 h-4 text-white" />
            ) : null}
          </button>

          {/* Action type label */}
          <span className={clsx('text-xs font-bold uppercase tracking-wider', getLabelColor())}>
            {getActionLabel()}
          </span>
        </div>

        {/* Help icon for negative actions */}
        {isNegative && (
          <Tooltip
            content={
              <div className="text-xs">
                <p className="font-medium mb-1">Как сделать в TikTok:</p>
                <ol className="list-decimal list-inside space-y-1 text-gray-300">
                  <li>Открой ленту</li>
                  <li>Найди похожее видео</li>
                  <li>Нажми ⋯</li>
                  <li>Выбери "Not interested"</li>
                </ol>
              </div>
            }
          >
            <HelpCircle className="w-4 h-4 text-white/40 hover:text-white/60 cursor-help" />
          </Tooltip>
        )}

        {/* Completed badge */}
        {completed && (
          <span className="text-xs text-green-400 font-medium flex items-center gap-1">
            <Check className="w-3 h-3" /> Готово
          </span>
        )}
      </div>

      {/* Content */}
      <div className="flex gap-3 mb-4">
        {/* Thumbnail (только для positive) */}
        {!isNegative && target.thumbnailUrl && (
          <div className="w-14 h-14 rounded-lg bg-white/10 overflow-hidden flex-shrink-0">
            <img
              src={target.thumbnailUrl}
              alt={target.name}
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).src = '/placeholder-video.jpg';
              }}
            />
          </div>
        )}

        {/* Info */}
        <div className="flex-1 min-w-0">
          <p className="text-white font-medium truncate">{target.name}</p>
          {target.description && (
            <p className="text-white/60 text-sm truncate">{target.description}</p>
          )}
        </div>
      </div>

      {/* CTA Button */}
      <button
        onClick={handleCTAClick}
        disabled={completed || isCompleting}
        className={clsx(
          'w-full px-4 py-2.5 rounded-lg text-sm font-medium transition-all',
          'flex items-center justify-center gap-2',
          completed
            ? 'bg-green-500/20 text-green-400 cursor-default'
            : isNegative
              ? 'bg-white/10 text-white hover:bg-white/20'
              : 'bg-gradient-to-r from-primary to-secondary text-white hover:opacity-90',
          isCompleting && 'opacity-50 cursor-wait'
        )}
      >
        {isCompleting ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Отправка...
          </>
        ) : completed ? (
          <>
            <Check className="w-4 h-4" />
            Готово
          </>
        ) : isNegative ? (
          'Готово ✓'
        ) : (
          <>
            <ExternalLink className="w-4 h-4" />
            Открыть в TikTok
          </>
        )}
      </button>
    </div>
  );
};
