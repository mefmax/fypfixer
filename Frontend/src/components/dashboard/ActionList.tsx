import React from 'react';
import type { PlanAction } from '../../types/action.types';
import { ActionCard } from './ActionCard';

interface ActionListProps {
  title: string;
  actions: PlanAction[];
  onComplete: (actionId: string) => Promise<void>;
  onOpenTikTok?: (url: string) => void;
}

export const ActionList: React.FC<ActionListProps> = ({
  title,
  actions,
  onComplete,
  onOpenTikTok,
}) => {
  if (actions.length === 0) return null;

  return (
    <div className="space-y-3">
      {/* Section header */}
      <h3 className="text-white/80 font-medium flex items-center gap-2">
        <span>{title}</span>
        <span className="text-white/40 text-sm">({actions.length})</span>
      </h3>

      {/* Action cards */}
      <div className="space-y-3">
        {actions.map((action) => (
          <ActionCard
            key={action.id}
            action={action}
            onComplete={onComplete}
            onOpenTikTok={onOpenTikTok}
          />
        ))}
      </div>
    </div>
  );
};
