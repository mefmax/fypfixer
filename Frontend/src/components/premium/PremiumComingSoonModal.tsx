import React, { useState } from 'react';
import { X, Bell, Check } from 'lucide-react';

interface Category {
  name: string;
  emoji: string;
  price: number;
  description: string;
  id: number;
}

interface PremiumModalProps {
  category: Category;
  onClose: () => void;
  onJoinWaitlist: () => Promise<void>;
  isOnWaitlist: boolean;
}

export const PremiumComingSoonModal: React.FC<PremiumModalProps> = ({
  category,
  onClose,
  onJoinWaitlist,
  isOnWaitlist
}) => {
  const [loading, setLoading] = useState(false);
  const [joined, setJoined] = useState(isOnWaitlist);

  const handleJoin = async () => {
    setLoading(true);
    try {
      await onJoinWaitlist();
      setJoined(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4">
      <div className="w-full max-w-md bg-gradient-to-b from-slate-900 to-slate-800 rounded-2xl border border-white/10 p-6 relative">

        {/* Close */}
        <button onClick={onClose} className="absolute top-4 right-4 text-white/40 hover:text-white">
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="text-center mb-6">
          <span className="text-5xl mb-3 block">{category.emoji}</span>
          <h2 className="text-xl font-bold text-white">{category.name}</h2>
          <p className="text-white/60 text-sm mt-1">{category.description}</p>
        </div>

        {/* Price Badge */}
        <div className="bg-gradient-to-r from-orange-500/20 to-pink-500/20 border border-orange-500/30 rounded-xl p-4 text-center mb-6">
          <p className="text-white/60 text-sm">Coming Soon</p>
          <p className="text-2xl font-bold text-white">
            ${category.price}
            <span className="text-sm font-normal text-white/60"> for 14 days</span>
          </p>
        </div>

        {/* Benefits */}
        <div className="space-y-2 mb-6">
          <div className="flex items-center gap-2 text-white/80 text-sm">
            <Check className="w-4 h-4 text-green-400" />
            <span>Curated {category.name.toLowerCase()} creators</span>
          </div>
          <div className="flex items-center gap-2 text-white/80 text-sm">
            <Check className="w-4 h-4 text-green-400" />
            <span>14 days of personalized plans</span>
          </div>
          <div className="flex items-center gap-2 text-white/80 text-sm">
            <Check className="w-4 h-4 text-green-400" />
            <span>Early supporters get 20% off</span>
          </div>
        </div>

        {/* CTA */}
        {joined ? (
          <div className="bg-green-500/20 border border-green-500/30 rounded-xl p-4 text-center">
            <Check className="w-6 h-6 text-green-400 mx-auto mb-2" />
            <p className="text-white font-medium">You're on the list!</p>
            <p className="text-white/60 text-sm">We'll notify you when it's ready.</p>
          </div>
        ) : (
          <button
            onClick={handleJoin}
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-orange-500 to-pink-500 text-white font-semibold rounded-xl hover:opacity-90 transition flex items-center justify-center gap-2"
          >
            <Bell className="w-5 h-5" />
            {loading ? 'Joining...' : 'Notify Me When Available'}
          </button>
        )}
      </div>
    </div>
  );
};
