/**
 * Admin Metrics Hooks - React Query hooks for dashboard data
 */
import { useQuery } from '@tanstack/react-query';
import { adminMetricsApi } from '../api/adminMetrics.api';

const REFRESH_INTERVAL = 30000; // 30 seconds

/**
 * Hook for user overview metrics (DAU, new today, total users)
 */
export function useOverviewMetrics() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'overview'],
    queryFn: async () => {
      const response = await adminMetricsApi.getOverview();
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to fetch overview');
      }
      return response.data;
    },
    refetchInterval: REFRESH_INTERVAL,
  });
}

/**
 * Hook for challenge funnel metrics (D0 -> D7 completion)
 */
export function useChallengeMetrics() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'challenge'],
    queryFn: async () => {
      const response = await adminMetricsApi.getChallenge();
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to fetch challenge');
      }
      return response.data;
    },
    refetchInterval: REFRESH_INTERVAL,
  });
}

/**
 * Hook for plan performance metrics (step completion, signals)
 */
export function usePlansMetrics() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'plans'],
    queryFn: async () => {
      const response = await adminMetricsApi.getPlans();
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to fetch plans');
      }
      return response.data;
    },
    refetchInterval: REFRESH_INTERVAL,
  });
}

/**
 * Hook for system health metrics (latency, errors, AI cost)
 */
export function useSystemMetrics() {
  return useQuery({
    queryKey: ['admin', 'metrics', 'system'],
    queryFn: async () => {
      const response = await adminMetricsApi.getSystem();
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to fetch system');
      }
      return response.data;
    },
    refetchInterval: REFRESH_INTERVAL,
  });
}
