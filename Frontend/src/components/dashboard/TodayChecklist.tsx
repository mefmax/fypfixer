import React from 'react';
import { Link } from 'react-router-dom';
import { Card } from '../common/Card';
import { ChecklistItem, type ChecklistItemData } from './ChecklistItem';

const defaultChecklistItems: ChecklistItemData[] = [
  {
    id: 'clean-up',
    icon: '🧹',
    title: 'Clean up 5 low-value videos',
    description: "Use 'Not interested' on 5 videos that don't match your goals.",
    duration: '~3 min',
  },
  {
    id: 'save-videos',
    icon: '📥',
    title: 'Save 3 great videos',
    description: 'Save or favorite 3 high-quality videos that fit your topics.',
    duration: '~3 min',
  },
  {
    id: 'follow-creators',
    icon: '➕',
    title: 'Follow 2–3 great creators',
    description: "Follow a few creators whose content you'd love to see daily.",
    duration: '~2 min',
  },
];

interface TodayChecklistProps {
  completedItems: string[];
  onToggleItem: (id: string) => void;
  items?: ChecklistItemData[];
}

export const TodayChecklist: React.FC<TodayChecklistProps> = ({
  completedItems,
  onToggleItem,
  items = defaultChecklistItems,
}) => {
  return (
    <Card className="border-slate-700 bg-slate-900/60 p-5">
      <div className="mb-4">
        <h3 className="text-lg font-bold text-white">Today's checklist</h3>
        <p className="text-xs text-slate-400">Complete these steps to stay on track.</p>
      </div>

      <div className="space-y-2">
        {items.map((item) => (
          <ChecklistItem
            key={item.id}
            {...item}
            isCompleted={completedItems.includes(item.id)}
            onToggle={onToggleItem}
          />
        ))}
      </div>

      <div className="mt-4 text-center">
        <Link
          to="/plan/preview"
          className="text-xs text-teal-400 underline-offset-2 hover:text-teal-300 hover:underline"
        >
          View full Day 1 checklist
        </Link>
      </div>
    </Card>
  );
};
