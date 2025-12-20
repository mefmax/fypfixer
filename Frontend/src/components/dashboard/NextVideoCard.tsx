import React from 'react';
import { Play, ExternalLink, Check, SkipForward } from 'lucide-react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import type { StepItem } from '../../types/plan.types';

interface NextVideoCardProps {
  video?: StepItem | null;
  videoNumber?: number;
  totalVideos?: number;
  onOpenInTikTok?: () => void;
  onMarkWatched?: () => void;
  onSkip?: () => void;
}

export const NextVideoCard: React.FC<NextVideoCardProps> = ({
  video,
  videoNumber = 1,
  totalVideos = 4,
  onOpenInTikTok,
  onMarkWatched,
  onSkip,
}) => {
  // Default placeholder if no video provided
  const displayVideo = video || {
    title: 'Loading next video...',
    creator_username: '@creator_handle',
    thumbnail_url: '',
    reason_text: 'Short, high-signal content that matches your goals.',
  };

  return (
    <Card className="border-teal-500/30 bg-slate-900/80 p-5 shadow-lg shadow-teal-500/5">
      <div className="flex flex-col gap-5 lg:flex-row">
        {/* Video Thumbnail */}
        <div className="relative aspect-[9/16] w-full max-w-[180px] shrink-0 self-center overflow-hidden rounded-xl bg-gradient-to-b from-slate-800 to-slate-900 lg:self-start">
          {/* Badge */}
          <div className="absolute left-2 top-2 rounded-full bg-slate-900/90 px-2 py-0.5 text-[10px] font-medium text-slate-300">
            Video {videoNumber} / {totalVideos} for today
          </div>

          {displayVideo.thumbnail_url && (
            <img
              src={displayVideo.thumbnail_url}
              alt={displayVideo.title}
              className="h-full w-full object-cover"
            />
          )}

          {/* Play Button */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="flex h-14 w-14 items-center justify-center rounded-full bg-orange-500/90 shadow-lg shadow-orange-500/30">
              <Play className="ml-1 h-6 w-6 fill-white text-white" />
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex flex-1 flex-col">
          <h3 className="text-lg font-bold text-white">Your next video</h3>
          <p className="mb-3 text-sm text-slate-400">Handpicked from your target topics</p>

          {/* Meta Info */}
          <div className="mb-3 flex flex-wrap items-center gap-2 text-xs text-slate-500">
            <span>From: {displayVideo.creator_username}</span>
            <span className="h-1 w-1 rounded-full bg-slate-600" />
            <span>Approx. length: 30–60 sec</span>
          </div>

          {/* Description */}
          <p className="mb-4 text-sm leading-relaxed text-slate-300">
            {displayVideo.reason_text}
          </p>

          {/* Buttons */}
          <div className="mt-auto flex flex-wrap gap-2">
            <Button
              onClick={onOpenInTikTok}
              className="gap-2 bg-orange-500 font-semibold text-white shadow-lg shadow-orange-500/25 hover:bg-orange-600 hover:shadow-orange-500/40"
            >
              <ExternalLink className="h-4 w-4" />
              Open in TikTok
            </Button>
            <Button
              onClick={onMarkWatched}
              variant="outline"
              className="gap-2 border-slate-700 bg-transparent text-slate-300 hover:bg-slate-800 hover:text-white"
            >
              <Check className="h-4 w-4" />
              Mark as watched
            </Button>
            <Button
              onClick={onSkip}
              variant="ghost"
              className="gap-2 text-slate-400 hover:bg-slate-800 hover:text-slate-300"
            >
              <SkipForward className="h-4 w-4" />
              Skip
            </Button>
          </div>

          {/* Disclaimer */}
          <p className="mt-4 text-[10px] text-slate-500">
            FYPFixer never automates actions. You open and interact with videos manually in the TikTok app.
          </p>
        </div>
      </div>
    </Card>
  );
};
