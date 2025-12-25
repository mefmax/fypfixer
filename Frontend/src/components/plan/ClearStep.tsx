/**
 * ClearStep Component - Digital Detox step
 *
 * Displays toxic creators and allows user to block them.
 * Part of the Plan V2 3-step flow.
 */
import React, { useState } from 'react';
import { clsx } from 'clsx';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../common/Card';
import { Button } from '../common/Button';
import { usePlanStoreV2 } from '../../store/planStoreV2';
import type { ToxicCreator } from '../../types/planV2.types';

interface CreatorItemProps {
  creator: ToxicCreator;
  onBlock: (username: string) => Promise<void>;
  isBlocking: boolean;
  isBlocked: boolean;
}

const CreatorItem: React.FC<CreatorItemProps> = ({ creator, onBlock, isBlocking, isBlocked }) => {
  const completionPercent = Math.round(creator.completion_rate * 100);

  return (
    <div
      className={clsx(
        'flex items-center justify-between p-4 rounded-xl border transition-all duration-200',
        isBlocked
          ? 'border-green-500/30 bg-green-500/10'
          : 'border-white/10 bg-white/5 hover:bg-white/10'
      )}
    >
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="text-white font-medium">{creator.creator_name}</span>
          {isBlocked && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-green-500/20 text-green-400">
              Blocked
            </span>
          )}
        </div>
        <p className="text-sm text-gray-400 mt-1">
          {creator.reason || `Low engagement - ${completionPercent}%`}
        </p>
        <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
          <span>{creator.view_count} views</span>
          <span>{completionPercent}% completion</span>
        </div>
      </div>

      <Button
        variant={isBlocked ? 'ghost' : 'secondary'}
        size="sm"
        onClick={() => onBlock(creator.creator_name)}
        disabled={isBlocking || isBlocked}
        className={clsx(
          'ml-4 min-w-[80px]',
          isBlocked && 'opacity-50'
        )}
      >
        {isBlocking ? (
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : isBlocked ? (
          <svg className="h-4 w-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        ) : (
          <span className="flex items-center gap-1">
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
            </svg>
            Block
          </span>
        )}
      </Button>
    </div>
  );
};

interface ClearStepProps {
  onComplete?: () => void;
}

export const ClearStep: React.FC<ClearStepProps> = ({ onComplete }) => {
  const { plan, completeStep, blockCreator, blockAllCreators, signals } = usePlanStoreV2();
  const [blockedUsernames, setBlockedUsernames] = useState<Set<string>>(new Set());
  const [blockingUsername, setBlockingUsername] = useState<string | null>(null);
  const [isBlockingAll, setIsBlockingAll] = useState(false);

  const toxicCreators = plan?.steps.clear.toxic_creators || [];
  const remainingCount = toxicCreators.length - blockedUsernames.size;
  const allBlocked = remainingCount === 0 && toxicCreators.length > 0;

  const handleBlockCreator = async (username: string) => {
    setBlockingUsername(username);

    try {
      const success = await blockCreator(username);
      if (success) {
        setBlockedUsernames((prev) => new Set([...prev, username]));
      }
    } finally {
      setBlockingUsername(null);
    }
  };

  const handleBlockAll = async () => {
    setIsBlockingAll(true);

    try {
      const count = await blockAllCreators();
      // Mark all as blocked
      const allUsernames = toxicCreators.map((c) => c.creator_name);
      setBlockedUsernames(new Set(allUsernames));

      if (count > 0) {
        // Auto-complete step after blocking all
        setTimeout(() => {
          handleComplete();
        }, 500);
      }
    } finally {
      setIsBlockingAll(false);
    }
  };

  const handleComplete = () => {
    completeStep('clear');
    onComplete?.();
  };

  const handleSkip = () => {
    // Complete step without blocking
    handleComplete();
  };

  // Empty state - no toxic creators found
  if (toxicCreators.length === 0) {
    return (
      <Card className="text-center">
        <CardHeader>
          <CardTitle className="flex items-center justify-center gap-2">
            <span className="text-2xl">🎉</span>
            Great News!
          </CardTitle>
          <CardDescription>
            No toxic creators detected in your feed. Your algorithm is looking healthy!
          </CardDescription>
        </CardHeader>
        <CardFooter className="justify-center">
          <Button onClick={handleComplete}>
            Continue to Watch Step
          </Button>
        </CardFooter>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <span className="text-2xl">🧹</span>
          Digital Detox
        </CardTitle>
        <CardDescription>
          Block creators that drain your energy and pollute your algorithm
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-3">
        {toxicCreators.map((creator) => (
          <CreatorItem
            key={creator.creator_id}
            creator={creator}
            onBlock={handleBlockCreator}
            isBlocking={blockingUsername === creator.creator_name}
            isBlocked={blockedUsernames.has(creator.creator_name)}
          />
        ))}
      </CardContent>

      <CardFooter className="flex flex-col gap-3">
        {/* Block All Button */}
        {!allBlocked && (
          <Button
            variant="primary"
            fullWidth
            onClick={handleBlockAll}
            isLoading={isBlockingAll}
            disabled={isBlockingAll || allBlocked}
          >
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
            </svg>
            Block All ({remainingCount})
          </Button>
        )}

        {/* Continue Button (shown when all blocked) */}
        {allBlocked && (
          <Button variant="primary" fullWidth onClick={handleComplete}>
            <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            Continue to Watch Step
          </Button>
        )}

        {/* Skip Link */}
        {!allBlocked && (
          <button
            onClick={handleSkip}
            className="text-sm text-gray-400 hover:text-gray-300 transition-colors"
          >
            Skip for now
          </button>
        )}

        {/* Signal Counter */}
        {signals.blocks > 0 && (
          <p className="text-xs text-gray-500 text-center">
            +{signals.blocks} blocks recorded
          </p>
        )}
      </CardFooter>
    </Card>
  );
};

export default ClearStep;
