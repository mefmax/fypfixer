import React from 'react';
import { clsx } from 'clsx';
import type { StepItem } from '../../types/plan.types';
import { useUIStore } from '../../store/uiStore';

interface VideoCardProps {
  video: StepItem;
  isCompleted?: boolean;
  onComplete?: () => void;
}

export const VideoCard: React.FC<VideoCardProps> = ({
  video,
  isCompleted = false,
  onComplete
}) => {
  const { openVideoModal } = useUIStore();

  const handleClick = () => {
    openVideoModal(video);
  };

  return (
    <div
      onClick={handleClick}
      className={clsx(
        'relative rounded-xl overflow-hidden cursor-pointer',
        'bg-gradient-to-br from-primary/30 to-background',
        'border border-primary/40 hover:border-primary/60',
        'transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-primary/20',
        isCompleted && 'opacity-60'
      )}
    >
      {/* Thumbnail */}
      <div className="relative aspect-[9/16]">
        <img
          src={video.thumbnail_url || '/placeholder-video.jpg'}
          alt={video.title}
          className="w-full h-full object-cover"
        />

        {/* Play overlay */}
        <div className="absolute inset-0 flex items-center justify-center bg-black/20">
          <div className="w-14 h-14 rounded-full bg-black/70 flex items-center justify-center backdrop-blur-sm">
            <span className="text-white text-xl ml-1">▶</span>
          </div>
        </div>

        {/* Completed badge */}
        {isCompleted && (
          <div className="absolute top-3 left-3 px-2 py-1 bg-green-500/90 rounded-full">
            <span className="text-xs text-white font-medium">✓ Watched</span>
          </div>
        )}

        {/* Checkbox */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onComplete?.();
          }}
          className={clsx(
            'absolute top-3 right-3 w-6 h-6 rounded-md border-2',
            'flex items-center justify-center transition-all',
            isCompleted
              ? 'bg-green-500 border-green-500 text-white'
              : 'border-white/50 bg-black/30 hover:border-white'
          )}
        >
          {isCompleted && '✓'}
        </button>
      </div>

      {/* Meta */}
      <div className="p-4 bg-black/40">
        <h4 className="text-sm font-semibold text-white line-clamp-2 mb-1">
          {video.title}
        </h4>
        <p className="text-xs text-gray-400">
          {video.creator_username}
        </p>
        {video.reason_text && (
          <p className="text-xs text-gray-500 mt-2 line-clamp-2 italic">
            {video.reason_text}
          </p>
        )}
      </div>
    </div>
  );
};
