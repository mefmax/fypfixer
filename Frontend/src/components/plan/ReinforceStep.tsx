/**
 * ReinforceStep Component - Reinforce step
 *
 * Displays favorite video for rewatching and share button (Day 3+).
 * Tracks rewatch completion and shares.
 * Part of the Plan V2 3-step flow.
 */
import React, { useState } from 'react';
import { clsx } from 'clsx';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../common/Card';
import { Button } from '../common/Button';
import { usePlanStoreV2 } from '../../store/planStoreV2';
import type { FavoriteVideo } from '../../types/planV2.types';

interface FavoriteVideoCardProps {
  video: FavoriteVideo;
  onOpenTikTok: () => void;
}

const FavoriteVideoCard: React.FC<FavoriteVideoCardProps> = ({ video, onOpenTikTok }) => {
  return (
    <div
      className="relative rounded-xl overflow-hidden bg-black cursor-pointer group"
      onClick={onOpenTikTok}
    >
      {/* Thumbnail */}
      {video.thumbnail_url ? (
        <img
          src={video.thumbnail_url}
          alt={video.creator_name || 'Favorite video'}
          className="w-full aspect-[9/16] object-cover max-h-[400px]"
        />
      ) : (
        <div className="w-full aspect-[9/16] max-h-[400px] bg-gray-800 flex items-center justify-center">
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

      {/* Favorite badge */}
      <div className="absolute top-3 left-3">
        <span className="px-2 py-1 rounded-full bg-pink-500/80 text-white text-xs font-medium flex items-center gap-1">
          <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
          </svg>
          Favorite
        </span>
      </div>

      {/* Creator info overlay */}
      <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent">
        <p className="text-white font-medium">{video.creator_name || 'Unknown creator'}</p>
        {video.creator_display_name && video.creator_display_name !== video.creator_name && (
          <p className="text-gray-300 text-sm">{video.creator_display_name}</p>
        )}
        {video.description && (
          <p className="text-gray-400 text-xs mt-1 line-clamp-2">{video.description}</p>
        )}
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

interface ReinforceStepProps {
  onComplete?: () => void;
  onShare?: () => void;
}

export const ReinforceStep: React.FC<ReinforceStepProps> = ({ onComplete, onShare }) => {
  const { plan, completeStep, addSignal, signals } = usePlanStoreV2();

  const favoriteVideo = plan?.steps.reinforce.favorite_video;
  const showShare = plan?.steps.reinforce.show_share ?? false;
  const dayOfChallenge = plan?.day_of_challenge ?? 1;

  const [rewatched, setRewatched] = useState(false);
  const [shared, setShared] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Open TikTok video
  const handleOpenTikTok = () => {
    if (favoriteVideo?.video_url) {
      window.open(favoriteVideo.video_url, '_blank', 'noopener,noreferrer');
    }
  };

  // Handle rewatch confirmation
  const handleRewatched = async () => {
    setIsProcessing(true);

    try {
      setRewatched(true);
      addSignal('watchesFull');

      // Small delay for UX
      await new Promise((resolve) => setTimeout(resolve, 300));

      // If no share button or already shared, complete step
      if (!showShare || shared) {
        handleComplete();
      }
    } finally {
      setIsProcessing(false);
    }
  };

  // Handle share
  const handleShare = () => {
    setShared(true);
    addSignal('shares');
    onShare?.();
  };

  // Complete step
  const handleComplete = () => {
    completeStep('reinforce');
    onComplete?.();
  };

  // Skip step
  const handleSkip = () => {
    handleComplete();
  };

  // Empty state - no favorite video
  if (!favoriteVideo) {
    return (
      <Card className="text-center">
        <CardHeader>
          <CardTitle className="flex items-center justify-center gap-2">
            <span className="text-2xl">📭</span>
            No Favorite Video Yet
          </CardTitle>
          <CardDescription>
            Like some videos in the Watch step to build your favorites collection!
          </CardDescription>
        </CardHeader>
        <CardFooter className="justify-center">
          <Button onClick={handleComplete}>
            Complete Today's Plan
          </Button>
        </CardFooter>
      </Card>
    );
  }

  // Completed state
  const allDone = rewatched && (!showShare || shared);

  if (allDone) {
    return (
      <Card className="text-center">
        <CardHeader>
          <CardTitle className="flex items-center justify-center gap-2">
            <span className="text-2xl">🎉</span>
            Day {dayOfChallenge} Complete!
          </CardTitle>
          <CardDescription>
            Amazing work! Your algorithm is getting better every day.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center gap-6 py-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-400">{signals.watchesFull}</p>
              <p className="text-xs text-gray-400">Watches</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-pink-400">{signals.likes}</p>
              <p className="text-xs text-gray-400">Likes</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-400">{signals.shares}</p>
              <p className="text-xs text-gray-400">Shares</p>
            </div>
          </div>
        </CardContent>
        <CardFooter className="justify-center">
          <Button onClick={handleComplete}>
            Finish Day {dayOfChallenge}
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
            <span className="text-2xl">💪</span>
            Reinforce
          </CardTitle>
          <span className="text-sm text-gray-400">
            Day {dayOfChallenge} of 7
          </span>
        </div>
        <CardDescription>
          Rewatch your favorite video to strengthen the positive signals
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Favorite Video Card */}
        <FavoriteVideoCard video={favoriteVideo} onOpenTikTok={handleOpenTikTok} />

        {/* Rewatch confirmation */}
        {!rewatched && (
          <div className="text-center py-2">
            <p className="text-gray-300 mb-4">Did you rewatch your favorite video?</p>
            <div className="flex gap-3 justify-center">
              <Button
                variant="primary"
                onClick={handleRewatched}
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
        )}

        {/* Share section (Day 3+) */}
        {rewatched && showShare && !shared && (
          <div className="border-t border-white/10 pt-4">
            <div className="text-center">
              <p className="text-gray-300 mb-2">Share with a friend to boost your progress!</p>
              <p className="text-xs text-gray-500 mb-4">
                Sharing unlocks bonus rewards and helps friends discover great content
              </p>
              <div className="flex gap-3 justify-center">
                <Button
                  variant="primary"
                  onClick={handleShare}
                  className="min-w-[140px]"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                  </svg>
                  Share Now
                </Button>
                <Button
                  variant="ghost"
                  onClick={handleComplete}
                  className="min-w-[100px]"
                >
                  Skip
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Rewatched badge */}
        {rewatched && (
          <div className="flex items-center justify-center gap-2 py-2">
            <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-sm flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Rewatched
            </span>
            {shared && (
              <span className="px-3 py-1 rounded-full bg-purple-500/20 text-purple-400 text-sm flex items-center gap-1">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
                Shared
              </span>
            )}
          </div>
        )}
      </CardContent>

      <CardFooter className="flex flex-col gap-2">
        {/* Complete button (shown when rewatch done but no share required) */}
        {rewatched && !showShare && (
          <Button variant="primary" fullWidth onClick={handleComplete}>
            Complete Day {dayOfChallenge}
          </Button>
        )}

        {/* Signal counter */}
        <p className="text-xs text-gray-500 text-center">
          +{signals.watchesFull + signals.shares} signals today
        </p>
      </CardFooter>
    </Card>
  );
};

export default ReinforceStep;
