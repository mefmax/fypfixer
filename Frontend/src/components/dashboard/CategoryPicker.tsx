import React, { useEffect, useState } from 'react';
import { X, Check, Loader2, Lock } from 'lucide-react';
import { clsx } from 'clsx';
import { plansApi } from '../../api/plans.api';
import { waitlistApi } from '../../api/waitlist.api';
import { PremiumComingSoonModal } from '../premium/PremiumComingSoonModal';
import type { Category as CategoryType } from '../../types/plan.types';

interface CategoryPickerProps {
  isOpen: boolean;
  currentCategory: string;
  onSelect: (categoryCode: string) => void;
  onClose: () => void;
}

export const CategoryPicker: React.FC<CategoryPickerProps> = ({
  isOpen,
  currentCategory,
  onSelect,
  onClose,
}) => {
  const [categories, setCategories] = useState<CategoryType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedCode, setSelectedCode] = useState(currentCategory);
  const [premiumModalCategory, setPremiumModalCategory] = useState<CategoryType | null>(null);

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
        setCategories(response.data.categories);
      }
    } catch (error) {
      console.error('Failed to load categories:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCategoryClick = (cat: CategoryType) => {
    if (cat.is_premium && cat.coming_soon) {
      // Show premium modal
      setPremiumModalCategory(cat);
    } else {
      // Select category
      setSelectedCode(cat.slug || cat.code || '');
    }
  };

  const handleSelect = () => {
    onSelect(selectedCode);
    onClose();
  };

  const handleJoinWaitlist = async () => {
    if (!premiumModalCategory) return;

    try {
      await waitlistApi.joinWaitlist(premiumModalCategory.id);
      // Reload categories to update waitlist status
      await loadCategories();
    } catch (error) {
      console.error('Failed to join waitlist:', error);
      throw error;
    }
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
          <h2 className="text-xl font-bold text-white">Choose Your Goal</h2>
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
              {categories.map((cat) => {
                const categorySlug = cat.slug || cat.code || '';
                const isSelected = selectedCode === categorySlug;
                const isPremium = cat.is_premium && cat.coming_soon;

                return (
                  <button
                    key={cat.id}
                    onClick={() => handleCategoryClick(cat)}
                    className={clsx(
                      'w-full p-4 rounded-xl border-2 text-left transition-all relative',
                      isSelected && !isPremium
                        ? 'border-primary bg-primary/10'
                        : isPremium
                        ? 'border-orange-500/30 hover:border-orange-500/50 bg-gradient-to-br from-orange-500/10 to-pink-500/10'
                        : 'border-white/10 hover:border-white/20 bg-white/5'
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{cat.emoji || cat.icon}</span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-semibold text-white">{cat.name}</span>
                          {isPremium && (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-gradient-to-r from-orange-500 to-pink-500 text-white text-xs font-semibold rounded-full">
                              <Lock className="w-3 h-3" />
                              Coming Soon
                            </span>
                          )}
                          {cat.on_waitlist && (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-500/20 border border-green-500/30 text-green-400 text-xs font-semibold rounded-full">
                              <Check className="w-3 h-3" />
                              On Waitlist
                            </span>
                          )}
                          {isSelected && !isPremium && (
                            <Check className="w-4 h-4 text-primary" />
                          )}
                        </div>
                        <p className="text-sm text-white/60 mt-1">{cat.description}</p>
                      </div>
                    </div>
                  </button>
                );
              })}
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
            Apply
          </button>
        </div>
      </div>

      {/* Premium Coming Soon Modal */}
      {premiumModalCategory && (
        <PremiumComingSoonModal
          category={{
            name: premiumModalCategory.name,
            emoji: premiumModalCategory.emoji,
            price: premiumModalCategory.price,
            description: premiumModalCategory.description,
            id: premiumModalCategory.id,
          }}
          onClose={() => setPremiumModalCategory(null)}
          onJoinWaitlist={handleJoinWaitlist}
          isOnWaitlist={premiumModalCategory.on_waitlist}
        />
      )}
    </div>
  );
};
