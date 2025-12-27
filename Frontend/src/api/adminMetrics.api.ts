/**
 * Admin Metrics API - Dashboard metrics for admin users
 */
import apiClient from '../lib/axios';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: { code: string; message: string };
}

export interface OverviewMetrics {
  dau: number;
  new_today: number;
  total_users: number;
}

export interface FunnelDay {
  day: number;
  count: number;
  percent: number;
}

export interface ChallengeMetrics {
  funnel: FunnelDay[];
  d7_completion_rate: number;
}

export interface PlansMetrics {
  step_completion: {
    clear: number;
    watch: number;
    reinforce: number;
  };
  avg_duration_seconds: number;
  signals: {
    blocks: number;
    watches_full: number;
    likes: number;
    follows: number;
    shares: number;
  };
}

export interface SystemMetrics {
  api_latency_p95_ms: number;
  error_rate_percent: number;
  ai_cost_today_usd: number;
  status: 'operational' | 'degraded' | 'outage';
}

export const adminMetricsApi = {
  /**
   * Get user overview metrics (DAU, new today, total)
   */
  getOverview: async (): Promise<ApiResponse<OverviewMetrics>> => {
    const response = await apiClient.get('/admin/metrics/overview');
    return response.data;
  },

  /**
   * Get challenge funnel metrics (D0 -> D7)
   */
  getChallenge: async (): Promise<ApiResponse<ChallengeMetrics>> => {
    const response = await apiClient.get('/admin/metrics/challenge');
    return response.data;
  },

  /**
   * Get plan performance metrics (step completion, signals)
   */
  getPlans: async (): Promise<ApiResponse<PlansMetrics>> => {
    const response = await apiClient.get('/admin/metrics/plans');
    return response.data;
  },

  /**
   * Get system health metrics (latency, errors, AI cost)
   */
  getSystem: async (): Promise<ApiResponse<SystemMetrics>> => {
    const response = await apiClient.get('/admin/metrics/system');
    return response.data;
  },
};
