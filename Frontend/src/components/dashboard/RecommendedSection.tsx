import React from 'react';
import { RecommendedCategoryCard } from './RecommendedCategoryCard';

interface RecommendedCategory {
  emoji: string;
  name: string;
}

const defaultRecommendedCategories: RecommendedCategory[] = [
  { emoji: '💰', name: 'Finance' },
  { emoji: '✅', name: 'Habits' },
  { emoji: '⚡', name: 'Productivity' },
  { emoji: '😴', name: 'Sleep' },
  { emoji: '🔥', name: 'Motivation' },
];

interface RecommendedSectionProps {
  categories?: RecommendedCategory[];
  onAddCategory?: (name: string) => void;
}

export const RecommendedSection: React.FC<RecommendedSectionProps> = ({
  categories = defaultRecommendedCategories,
  onAddCategory,
}) => {
  return (
    <div className="mt-8">
      <h3 className="mb-4 text-lg font-bold text-white">Recommended for you</h3>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
        {categories.map((category) => (
          <RecommendedCategoryCard key={category.name} {...category} onAdd={onAddCategory} />
        ))}
      </div>
    </div>
  );
};
