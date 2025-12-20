import React, { useEffect, useState } from 'react';
import { X, Check, Loader2 } from 'lucide-react';
import { clsx } from 'clsx';
import { plansApi } from '../../api/plans.api';

interface Category {
  code: string;
  name: string;
  description?: string;
  icon: string;
}

// Category descriptions mapping
const CATEGORY_DESCRIPTIONS: Record<string, string> = {
  personal_growth: 'Motivation, habits, mindset',
  wellness: 'Health, fitness, mental health',
  productivity: 'Focus, time management',
  creativity: 'Art, music, design',
  learning: 'Education, skills, knowledge',
  fitness: 'Exercise, sports, workouts',
  mindfulness: 'Meditation, awareness',
  finance: 'Money, investing, budgeting',
};

interface CategoryPickerProps {
  isOpen: boolean;
  currentCategory: string;
  onSelect: (categoryCode: string) => void;
  onClose: () => void;
}

// Category icons mapping
const CATEGORY_ICONS: Record<string, string> = {
  personal_growth: '🚀',
  wellness: '🧘',
  productivity: '⚡',
  creativity: '🎨',
  learning: '📚',
  fitness: '💪',
  mindfulness: '🧠',
  finance: '💰',
};

export const CategoryPicker: React.FC<CategoryPickerProps> = ({
  isOpen,
  currentCategory,
  onSelect,
  onClose,
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedCode, setSelectedCode] = useState(currentCategory);

  useEffect(() => {
    if (isOpen) {
      loadCategories();
      setSelectedCode(currentCategory);
    }
  }, [isOpen, currentCategory]);

  const loadCategories = async () => {
    setIsLoading(true);
    try {
      const response = await plansApi.getCategories('en');
      if (response.success && response.data?.categories) {
        setCategories(response.data.categories.map(cat => ({
          code: cat.code,
          name: cat.name,
          description: CATEGORY_DESCRIPTIONS[cat.code] || '',
          icon: CATEGORY_ICONS[cat.code] || '📌',
        })));
      }
    } catch (error) {
      console.error('Failed to load categories:', error);
      // Fallback categories
      setCategories([
        { code: 'personal_growth', name: 'Personal Growth', description: 'Motivation, habits, mindset', icon: '🚀' },
        { code: 'wellness', name: 'Wellness', description: 'Health, fitness, mental health', icon: '🧘' },
        { code: 'productivity', name: 'Productivity', description: 'Focus, time management', icon: '⚡' },
        { code: 'creativity', name: 'Creativity', description: 'Art, music, design', icon: '🎨' },
        { code: 'learning', name: 'Learning', description: 'Education, skills, knowledge', icon: '📚' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelect = () => {
    onSelect(selectedCode);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-md bg-background-secondary rounded-2xl border border-white/10 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/10">
          <h2 className="text-xl font-bold text-white">Выбери цель</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5 text-white/60" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 max-h-[60vh] overflow-y-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-8 h-8 text-primary animate-spin" />
            </div>
          ) : (
            <div className="space-y-2">
              {categories.map((cat) => (
                <button
                  key={cat.code}
                  onClick={() => setSelectedCode(cat.code)}
                  className={clsx(
                    'w-full p-4 rounded-xl border-2 text-left transition-all',
                    selectedCode === cat.code
                      ? 'border-primary bg-primary/10'
                      : 'border-white/10 hover:border-white/20 bg-white/5'
                  )}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{cat.icon}</span>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-white">{cat.name}</span>
                        {selectedCode === cat.code && (
                          <Check className="w-4 h-4 text-primary" />
                        )}
                      </div>
                      <p className="text-sm text-white/60">{cat.description}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-white/10">
          <button
            onClick={handleSelect}
            disabled={isLoading}
            className={clsx(
              'w-full py-3 rounded-xl font-semibold transition-all',
              'bg-gradient-to-r from-primary to-secondary text-white',
              'hover:opacity-90 disabled:opacity-50'
            )}
          >
            Применить
          </button>
        </div>
      </div>
    </div>
  );
};
