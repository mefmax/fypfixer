/**
 * WatchStep Component - Mindful Watching step
 *
 * Displays 4 curated videos for the user to watch.
 * Tracks watch completion, likes, and follows.
 * Part of the Plan V2 3-step flow.
 */
import React, { useState, useCallback } from 'react';
import { clsx } from 'clsx';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../common/Card';
import { Button } from '../common/Button';
import { usePlanStoreV2 } from '../../store/planStoreV2';
import { plansV2Api } from '../../api/plansV2.api';
import type { CuratedVideo } from '../../types/planV2.types';
import { logger } from '../../lib/logger';

interface VideoCardProps {
  video: CuratedVideo;
  onOpenTikTok: () => void;
}

const VideoCard: React.FC<VideoCardProps> = ({ video, onOpenTikTok }) => {
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div
      className="relative rounded-xl overflow-hidden bg-black cursor-pointer group"
      onClick={onOpenTikTok}
    >
      {/* Thumbnail */}
      {video.thumbnail_url ? (
        <img
          src={video.thumbnail_url}
          alt={video.creator_name}
          className="w-full aspect-[9/16] object-cover"
        />
      ) : (
        <div className="w-full aspect-[9/16] bg-gray-800 flex items-center justify-center">
          <svg className="w-16 h-16 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      )}

      {/* Play overlay */}
      <div className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center">
          <svg className="w-8 h-8 text-black ml-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
      </div>

      {/* Creator info overlay */}
      <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent">
        <p className="text-white font-medium">{video.creator_name}</p>
        {video.creator_display_name && video.creator_display_name !== video.creator_name && (
          <p className="text-gray-300 text-sm">{video.creator_display_name}</p>
        )}
        <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
          {video.duration_seconds && (
            <span>{formatDuration(video.duration_seconds)}</span>
          )}
          {video.views && (
            <span>{video.views.toLocaleString()} views</span>
          )}
        </div>
      </div>

      {/* TikTok logo */}
      <div className="absolute top-3 right-3">
        <svg className="w-6 h-6 text-white drop-shadow-lg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1-.1z" />
        </svg>
      </div>
    </div>
  );
};

interface ProgressDotsProps {
  total: number;
  current: number;
  completed: boolean[];
}

const ProgressDots: React.FC<ProgressDotsProps> = ({ total, current, completed }) => {
  return (
    <div className="flex items-center justify-center gap-2">
      {Array.from({ length: total }).map((_, i) => (
        <div
          key={i}
          className={clsx(
            'w-2.5 h-2.5 rounded-full transition-all duration-300',
            completed[i]
              ? 'bg-green-500'
              : i === current
              ? 'bg-primary w-3 h-3'
              : 'bg-gray-600'
          )}
        />
      ))}
    </div>
  );
};

interface WatchStepProps {
  onComplete?: () => void;
}

export const WatchStep: React.FC<WatchStepProps> = ({ onComplete }) => {
  const { plan, completeStep, addSignal, signals } = usePlanStoreV2();

  const videos = plan?.steps.watch.videos || [];
  const totalVideos = videos.length;

  const [currentIndex, setCurrentIndex] = useState(0);
  const [watchedFull, setWatchedFull] = useState<boolean[]>(new Array(totalVideos).fill(false));
  const [liked, setLiked] = useState<boolean[]>(new Array(totalVideos).fill(false));
  const [followed, setFollowed] = useState<boolean[]>(new Array(totalVideos).fill(false));
  const [isProcessing, setIsProcessing] = useState(false);

  const currentVideo = videos[currentIndex];
  const allCompleted = currentIndex >= totalVideos;

  // Open TikTok video
  const handleOpenTikTok = useCallback(() => {
    if (currentVideo?.video_url) {
      window.open(currentVideo.video_url, '_blank', 'noopener,noreferrer');
    }
  }, [currentVideo]);

  // Move to next video or complete step
  const advanceToNext = useCallback(() => {
    if (currentIndex < totalVideos - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      // All videos done - complete step
      completeStep('watch');
      onComplete?.();
    }
  }, [currentIndex, totalVideos, completeStep, onComplete]);

  // Handle YES (watched full)
  const handleWatchedFull = async () => {
    setIsProcessing(true);

    try {
      // Mark as watched
      const newWatched = [...watchedFull];
      newWatched[currentIndex] = true;
      setWatchedFull(newWatched);

      // Add signal
      addSignal('watchesFull');

      // Small delay for UX
      await new Promise((resolve) => setTimeout(resolve, 300));

      advanceToNext();
    } finally {
      setIsProcessing(false);
    }
  };

  // Handle SKIP
  const handleSkip = () => {
    advanceToNext();
  };

  // Handle Like
  const handleLike = async () => {
    if (liked[currentIndex] || !currentVideo) return;

    try {
      // Add to favorites via API
      await plansV2Api.addFavorite(currentVideo.video_id);

      const newLiked = [...liked];
      newLiked[currentIndex] = true;
      setLiked(newLiked);

      addSignal('likes');
    } catch (error) {
      logger.error('Failed to like video:', error);
    }
  };

  // Handle Follow
  const handleFollow = async () => {
    if (followed[currentIndex]) return;

    // For now, just track locally (no backend endpoint for follows yet)
    const newFollowed = [...followed];
    newFollowed[currentIndex] = true;
    setFollowed(newFollowed);

    addSignal('follows');
  };

  // Empty state
  if (videos.length === 0) {
    return (
      <Card className="text-center">
        <CardHeader>
          <CardTitle className="flex items-center justify-center gap-2">
            <span className="text-2xl">📭</span>
            No Videos Available
          </CardTitle>
          <CardDescription>
            We couldn't find any curated videos for you right now. Try again later!
          </CardDescription>
        </CardHeader>
        <CardFooter className="justify-center">
          <Button onClick={() => { completeStep('watch'); onComplete?.(); }}>
            Continue to Reinforce Step
          </Button>
        </CardFooter>
      </Card>
    );
  }

  // Completed state
  if (allCompleted) {
    const watchCount = watchedFull.filter(Boolean).length;
    const likeCount = liked.filter(Boolean).length;
    const followCount = followed.filter(Boolean).length;

    return (
      <Card className="text-center">
        <CardHeader>
          <CardTitle className="flex items-center justify-center gap-2">
            <span className="text-2xl">🎉</span>
            Watch Step Complete!
          </CardTitle>
          <CardDescription>
            Great job training your algorithm with positive content
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center gap-6 py-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-400">{watchCount}</p>
              <p className="text-xs text-gray-400">Full Watches</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-pink-400">{likeCount}</p>
              <p className="text-xs text-gray-400">Likes</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-400">{followCount}</p>
              <p className="text-xs text-gray-400">Follows</p>
            </div>
          </div>
        </CardContent>
        <CardFooter className="justify-center">
          <Button onClick={onComplete}>
            Continue to Reinforce Step
          </Button>
        </CardFooter>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <span className="text-2xl">👀</span>
            Mindful Watching
          </CardTitle>
          <span className="text-sm text-gray-400">
            Video {currentIndex + 1} of {totalVideos}
          </span>
        </div>
        <CardDescription>
          Watch these inspiring videos to train your algorithm
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Video Card */}
        {currentVideo && (
          <VideoCard video={currentVideo} onOpenTikTok={handleOpenTikTok} />
        )}

        {/* Watch confirmation */}
        <div className="text-center py-2">
          <p className="text-gray-300 mb-4">Did you watch the full video?</p>
          <div className="flex gap-3 justify-center">
            <Button
              variant="primary"
              onClick={handleWatchedFull}
              disabled={isProcessing}
              className="min-w-[120px]"
            >
              {isProcessing ? (
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  YES
                </>
              )}
            </Button>
            <Button
              variant="secondary"
              onClick={handleSkip}
              disabled={isProcessing}
              className="min-w-[120px]"
            >
              SKIP
            </Button>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-white/10 pt-4">
          <p className="text-xs text-gray-500 text-center mb-3">Optional actions:</p>
          <div className="flex gap-3 justify-center">
            <Button
              variant={liked[currentIndex] ? 'primary' : 'ghost'}
              size="sm"
              onClick={handleLike}
              disabled={liked[currentIndex]}
              className={clsx(
                'min-w-[100px]',
                liked[currentIndex] && 'bg-pink-500/20 text-pink-400'
              )}
            >
              {liked[currentIndex] ? (
                <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
              ) : (
                <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              )}
              Like
            </Button>
            <Button
              variant={followed[currentIndex] ? 'primary' : 'ghost'}
              size="sm"
              onClick={handleFollow}
              disabled={followed[currentIndex]}
              className={clsx(
                'min-w-[100px]',
                followed[currentIndex] && 'bg-blue-500/20 text-blue-400'
              )}
            >
              {followed[currentIndex] ? (
                <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
                </svg>
              ) : (
                <svg className="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              )}
              Follow
            </Button>
          </div>
        </div>

        {/* Progress dots */}
        <div className="pt-2">
          <ProgressDots
            total={totalVideos}
            current={currentIndex}
            completed={watchedFull}
          />
        </div>
      </CardContent>

      <CardFooter className="justify-center">
        {/* Signal counter */}
        <p className="text-xs text-gray-500">
          +{signals.watchesFull + signals.likes + signals.follows} signals this session
        </p>
      </CardFooter>
    </Card>
  );
};

export default WatchStep;
