import React, { useEffect, useState } from 'react';
import { X, Check, Loader2, Lock, Clock, Plus, Minus } from 'lucide-react';
import { clsx } from 'clsx';
import { plansApi } from '../../api/plans.api';
import { waitlistApi } from '../../api/waitlist.api';
import { PremiumComingSoonModal } from '../premium/PremiumComingSoonModal';
import type { Category as CategoryType, UserCategory, CategoryStats } from '../../types/plan.types';

interface CategoryPickerProps {
  isOpen: boolean;
  onClose: () => void;
  onCategoriesChanged?: () => void; // Callback when categories change
}

export const CategoryPicker: React.FC<CategoryPickerProps> = ({
  isOpen,
  onClose,
  onCategoriesChanged,
}) => {
  // All available categories
  const [allCategories, setAllCategories] = useState<CategoryType[]>([]);
  // User's selected category IDs
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  // User's category details (with expiry info)
  const [userCategories, setUserCategories] = useState<UserCategory[]>([]);
  // Stats
  const [stats, setStats] = useState<CategoryStats | null>(null);

  const [isLoading, setIsLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [premiumModalCategory, setPremiumModalCategory] = useState<CategoryType | null>(null);

  // Load data when modal opens
  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Load all categories
      const categoriesRes = await plansApi.getCategories('en');
      if (categoriesRes.success && categoriesRes.data?.categories) {
        setAllCategories(categoriesRes.data.categories);
      }

      // Load user's selected categories
      const userCatsRes = await plansApi.getUserCategories(true); // include inactive
      if (userCatsRes.success && userCatsRes.data) {
        setUserCategories(userCatsRes.data.categories);
        setStats(userCatsRes.data.stats);

        // Build selected IDs set (only active ones)
        const activeIds = new Set(
          userCatsRes.data.categories
            .filter(uc => uc.isActive)
            .map(uc => uc.categoryId)
        );
        setSelectedIds(activeIds);
      }
    } catch (err) {
      console.error('Failed to load categories:', err);
      setError('Failed to load categories');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCategoryToggle = async (category: CategoryType) => {
    const categoryId = category.id;
    const isSelected = selectedIds.has(categoryId);

    // Check if premium and not purchased
    if (category.is_premium && category.coming_soon && !isSelected) {
      // Show premium modal
      setPremiumModalCategory(category);
      return;
    }

    // Check if trying to add 4th free category
    if (!isSelected && !category.is_premium && stats && stats.freeRemaining <= 0) {
      setError('Maximum 3 free categories. Remove one to add another.');
      setTimeout(() => setError(null), 3000);
      return;
    }

    setActionLoading(categoryId);
    setError(null);

    try {
      if (isSelected) {
        // Remove category
        await plansApi.removeUserCategory(categoryId);
        setSelectedIds(prev => {
          const next = new Set(prev);
          next.delete(categoryId);
          return next;
        });
      } else {
        // Add category
        await plansApi.addUserCategory(categoryId, false);
        setSelectedIds(prev => new Set(prev).add(categoryId));
      }

      // Reload stats
      const userCatsRes = await plansApi.getUserCategories(true);
      if (userCatsRes.success && userCatsRes.data) {
        setUserCategories(userCatsRes.data.categories);
        setStats(userCatsRes.data.stats);
      }

      // Notify parent
      onCategoriesChanged?.();
    } catch (err: any) {
      console.error('Failed to update category:', err);
      setError(err.response?.data?.error?.message || 'Failed to update');
      setTimeout(() => setError(null), 3000);
    } finally {
      setActionLoading(null);
    }
  };

  const handleJoinWaitlist = async () => {
    if (!premiumModalCategory) return;
    try {
      await waitlistApi.joinWaitlist(premiumModalCategory.id);
      await loadData(); // Reload to update waitlist status
    } catch (err) {
      console.error('Failed to join waitlist:', err);
      throw err;
    }
  };

  const getUserCategoryInfo = (categoryId: number): UserCategory | undefined => {
    return userCategories.find(uc => uc.categoryId === categoryId);
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
      <div className="relative w-full max-w-md bg-background-secondary rounded-2xl border border-white/10 shadow-2xl max-h-[85vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/10 flex-shrink-0">
          <div>
            <h2 className="text-xl font-bold text-white">Your Categories</h2>
            {stats && (
              <p className="text-sm text-white/60 mt-1">
                {stats.freeActive}/{stats.freeLimit} free • {stats.premiumActive} premium
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5 text-white/60" />
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="mx-4 mt-4 p-3 rounded-lg bg-red-500/20 border border-red-500/50 text-red-400 text-sm">
            {error}
          </div>
        )}

        {/* Content */}
        <div className="p-4 overflow-y-auto flex-1">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-8 h-8 text-primary animate-spin" />
            </div>
          ) : (
            <div className="space-y-2">
              {/* FREE Categories Section */}
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-white/40 uppercase tracking-wider mb-2">
                  Free Categories ({stats?.freeRemaining || 0} remaining)
                </h3>
                <div className="space-y-2">
                  {allCategories.filter(c => !c.is_premium).map((cat) => (
                    <CategoryRow
                      key={cat.id}
                      category={cat}
                      isSelected={selectedIds.has(cat.id)}
                      isLoading={actionLoading === cat.id}
                      userCategoryInfo={getUserCategoryInfo(cat.id)}
                      onToggle={() => handleCategoryToggle(cat)}
                      disabled={!selectedIds.has(cat.id) && stats?.freeRemaining === 0}
                    />
                  ))}
                </div>
              </div>

              {/* PREMIUM Categories Section */}
              <div>
                <h3 className="text-sm font-semibold text-white/40 uppercase tracking-wider mb-2">
                  Premium Categories
                </h3>
                <div className="space-y-2">
                  {allCategories.filter(c => c.is_premium).map((cat) => {
                    const userCatInfo = getUserCategoryInfo(cat.id);
                    const isExpired = userCatInfo?.isExpired;
                    const isActive = selectedIds.has(cat.id) && !isExpired;

                    return (
                      <CategoryRow
                        key={cat.id}
                        category={cat}
                        isSelected={isActive}
                        isLoading={actionLoading === cat.id}
                        userCategoryInfo={userCatInfo}
                        onToggle={() => handleCategoryToggle(cat)}
                        isPremiumLocked={cat.coming_soon && !userCatInfo}
                        isExpired={isExpired}
                      />
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-white/10 flex-shrink-0">
          <button
            onClick={onClose}
            className={clsx(
              'w-full py-3 rounded-xl font-semibold transition-all',
              'bg-gradient-to-r from-primary to-secondary text-white',
              'hover:opacity-90'
            )}
          >
            Done
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

// Sub-component for category row
interface CategoryRowProps {
  category: CategoryType;
  isSelected: boolean;
  isLoading: boolean;
  userCategoryInfo?: UserCategory;
  onToggle: () => void;
  disabled?: boolean;
  isPremiumLocked?: boolean;
  isExpired?: boolean;
}

const CategoryRow: React.FC<CategoryRowProps> = ({
  category,
  isSelected,
  isLoading,
  userCategoryInfo,
  onToggle,
  disabled,
  isPremiumLocked,
  isExpired,
}) => {
  const daysRemaining = userCategoryInfo?.daysRemaining;

  return (
    <button
      onClick={onToggle}
      disabled={isLoading || disabled}
      className={clsx(
        'w-full p-4 rounded-xl border-2 text-left transition-all relative',
        isExpired
          ? 'border-white/5 bg-white/[0.02] opacity-50'
          : isSelected
            ? 'border-primary bg-primary/10'
            : isPremiumLocked
              ? 'border-orange-500/30 hover:border-orange-500/50 bg-gradient-to-br from-orange-500/10 to-pink-500/10'
              : disabled
                ? 'border-white/5 bg-white/[0.02] opacity-50 cursor-not-allowed'
                : 'border-white/10 hover:border-white/20 bg-white/5',
      )}
    >
      <div className="flex items-center gap-3">
        {/* Checkbox */}
        <div
          className={clsx(
            'w-6 h-6 rounded-md border-2 flex items-center justify-center flex-shrink-0 transition-all',
            isSelected && !isExpired
              ? 'bg-primary border-primary'
              : isExpired
                ? 'border-white/10'
                : 'border-white/30'
          )}
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 text-white animate-spin" />
          ) : isSelected && !isExpired ? (
            <Check className="w-4 h-4 text-white" />
          ) : null}
        </div>

        {/* Emoji */}
        <span className="text-2xl">{category.emoji || category.icon}</span>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={clsx(
              'font-semibold',
              isExpired ? 'text-white/40' : 'text-white'
            )}>
              {category.name}
            </span>

            {/* Badges */}
            {isPremiumLocked && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-gradient-to-r from-orange-500 to-pink-500 text-white text-xs font-semibold rounded-full">
                <Lock className="w-3 h-3" />
                ${category.price}
              </span>
            )}

            {isExpired && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-red-500/20 border border-red-500/30 text-red-400 text-xs font-semibold rounded-full">
                Expired
              </span>
            )}

            {daysRemaining !== null && daysRemaining !== undefined && !isExpired && isSelected && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-blue-500/20 border border-blue-500/30 text-blue-400 text-xs font-semibold rounded-full">
                <Clock className="w-3 h-3" />
                {daysRemaining}d left
              </span>
            )}

            {category.on_waitlist && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-500/20 border border-green-500/30 text-green-400 text-xs font-semibold rounded-full">
                <Check className="w-3 h-3" />
                Waitlist
              </span>
            )}
          </div>

          {category.description && (
            <p className={clsx(
              'text-sm mt-1 truncate',
              isExpired ? 'text-white/30' : 'text-white/60'
            )}>
              {category.description}
            </p>
          )}
        </div>

        {/* Action indicator */}
        <div className="flex-shrink-0">
          {!isLoading && !isPremiumLocked && !isExpired && (
            isSelected ? (
              <Minus className="w-5 h-5 text-white/40" />
            ) : !disabled ? (
              <Plus className="w-5 h-5 text-white/40" />
            ) : null
          )}
        </div>
      </div>
    </button>
  );
};
