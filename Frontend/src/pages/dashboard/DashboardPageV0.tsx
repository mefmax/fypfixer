import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { plansApi } from '../../api/plans.api';
import { useAuthStore } from '../../store/authStore';
import { DashboardHeader } from '../../components/dashboard/DashboardHeader';
import { TodayProgressCard } from '../../components/dashboard/TodayProgressCard';
import { NextVideoCard } from '../../components/dashboard/NextVideoCard';
import { TodayChecklist } from '../../components/dashboard/TodayChecklist';
import { ActivePlansSection } from '../../components/dashboard/ActivePlansSection';
import { RecommendedSection } from '../../components/dashboard/RecommendedSection';

/**
 * New Dashboard Page with V0 Design
 * This implements the full V0 dashboard layout with all components
 */
export const DashboardPageV0: React.FC = () => {
  const { user } = useAuthStore();
  const [completedItems, setCompletedItems] = useState<string[]>([]);
  const [completedVideos, setCompletedVideos] = useState<number[]>([]);

  // Fetch daily plan
  const { data, isLoading } = useQuery({
    queryKey: ['dailyPlan', 'personal_growth', user?.language || 'en'],
    queryFn: () => plansApi.getDailyPlan('personal_growth', user?.language || 'en'),
  });

  // Complete step mutation
  const completeMutation = useMutation({
    mutationFn: ({ planId, stepId }: { planId: number; stepId: number }) =>
      plansApi.completeStep(planId, stepId),
    onSuccess: (_, variables) => {
      setCompletedVideos((prev) => [...prev, variables.stepId]);
    },
  });

  const plan = data?.data;
  const firstVideo = plan?.steps?.[0]?.items?.[0] || null;
  const totalVideos = plan?.steps.reduce((acc, step) => acc + step.items.length, 0) || 4;
  const videosWatched = completedVideos.length;

  const toggleChecklistItem = (itemId: string) => {
    setCompletedItems((prev) =>
      prev.includes(itemId) ? prev.filter((id) => id !== itemId) : [...prev, itemId]
    );
  };

  const handleOpenInTikTok = () => {
    if (firstVideo?.video_url) {
      window.open(firstVideo.video_url, '_blank');
    }
  };

  const handleMarkWatched = () => {
    if (plan && firstVideo) {
      completeMutation.mutate({ planId: plan.id, stepId: firstVideo.id });
    }
  };

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 flex items-center justify-center">
        <div className="animate-spin w-12 h-12 border-4 border-teal-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900">
      <div className="mx-auto max-w-[1200px] px-4 py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <DashboardHeader weekNumber={1} dayNumber={1} streak={1} xp={0} />

        {/* Main Content Grid */}
        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          {/* Left Column */}
          <div className="space-y-6">
            <TodayProgressCard
              videosWatched={videosWatched}
              totalVideos={totalVideos}
              timeSpent={0}
              streakDay={1}
              xpEarned={0}
            />
            <NextVideoCard
              video={firstVideo}
              videoNumber={1}
              totalVideos={totalVideos}
              onOpenInTikTok={handleOpenInTikTok}
              onMarkWatched={handleMarkWatched}
            />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <TodayChecklist completedItems={completedItems} onToggleItem={toggleChecklistItem} />
            <ActivePlansSection />
          </div>
        </div>

        {/* Recommended Section - Full Width */}
        <RecommendedSection />

        {/* Footer Microcopy */}
        <div className="mt-10 pb-8 text-center">
          <p className="text-xs text-slate-500">
            You're always in control. FYPFixer only suggests manual actions — you decide what to do in TikTok.
          </p>
        </div>
      </div>
    </div>
  );
};
