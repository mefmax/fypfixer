import React from 'react';
import { RefreshCw, Users, Trophy, ClipboardList, Settings } from 'lucide-react';
import { MetricCard, FunnelChart, ProgressBar, StatusIndicator } from '../../components/admin';
import {
  useOverviewMetrics,
  useChallengeMetrics,
  usePlansMetrics,
  useSystemMetrics,
} from '../../hooks/useAdminMetrics';

export const AdminDashboardPage: React.FC = () => {
  const { data: overview, isLoading: overviewLoading, dataUpdatedAt } = useOverviewMetrics();
  const { data: challenge, isLoading: challengeLoading } = useChallengeMetrics();
  const { data: plans, isLoading: plansLoading } = usePlansMetrics();
  const { data: system, isLoading: systemLoading } = useSystemMetrics();

  // Format last updated time
  const lastUpdated = dataUpdatedAt
    ? `${Math.round((Date.now() - dataUpdatedAt) / 1000)}s ago`
    : 'Loading...';

  // Determine status colors for system metrics
  const getLatencyStatus = (ms: number) => {
    if (ms < 200) return 'ok';
    if (ms < 500) return 'warning';
    return 'error';
  };

  const getErrorStatus = (rate: number) => {
    if (rate < 1) return 'ok';
    if (rate < 5) return 'warning';
    return 'error';
  };

  const getCostStatus = (cost: number) => {
    if (cost < 20) return 'ok';
    if (cost < 50) return 'warning';
    return 'error';
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white">FYPGlow Dashboard</h1>
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <RefreshCw className="w-4 h-4 animate-spin" />
            <span>Updated: {lastUpdated}</span>
          </div>
        </div>

        {/* Block 1: Users Overview */}
        <div className="bg-slate-900/50 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center gap-2 mb-4">
            <Users className="w-5 h-5 text-teal-400" />
            <h2 className="text-lg font-semibold text-white">Users Today</h2>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <MetricCard label="DAU" value={overview?.dau ?? 0} loading={overviewLoading} />
            <MetricCard label="New" value={overview?.new_today ?? 0} loading={overviewLoading} />
            <MetricCard
              label="Total"
              value={overview?.total_users ?? 0}
              loading={overviewLoading}
              variant="highlight"
            />
          </div>
        </div>

        {/* Block 2: Challenge Funnel */}
        <div className="bg-slate-900/50 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Trophy className="w-5 h-5 text-amber-400" />
              <h2 className="text-lg font-semibold text-white">Challenge Funnel</h2>
            </div>
            <div className="text-sm text-slate-400">
              D7 Completion:{' '}
              <span className="text-amber-400 font-medium">
                {challenge?.d7_completion_rate ?? 0}%
              </span>
            </div>
          </div>
          <FunnelChart data={challenge?.funnel ?? []} loading={challengeLoading} />
        </div>

        {/* Block 3: Plan Performance */}
        <div className="bg-slate-900/50 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center gap-2 mb-4">
            <ClipboardList className="w-5 h-5 text-teal-400" />
            <h2 className="text-lg font-semibold text-white">Plan Performance</h2>
          </div>

          <div className="space-y-3 mb-6">
            <ProgressBar
              label="Clear"
              percent={plans?.step_completion?.clear ?? 0}
              loading={plansLoading}
              color="teal"
            />
            <ProgressBar
              label="Watch"
              percent={plans?.step_completion?.watch ?? 0}
              loading={plansLoading}
              color="teal"
            />
            <ProgressBar
              label="Reinforce"
              percent={plans?.step_completion?.reinforce ?? 0}
              loading={plansLoading}
              color="amber"
            />
          </div>

          <div className="pt-4 border-t border-slate-700">
            <p className="text-sm text-slate-400 mb-2">Average Signals per User</p>
            <div className="flex flex-wrap gap-4 text-sm">
              <span className="text-slate-300">
                Blocks: <span className="text-white font-medium">{plans?.signals?.blocks ?? 0}</span>
              </span>
              <span className="text-slate-300">
                Watches:{' '}
                <span className="text-white font-medium">{plans?.signals?.watches_full ?? 0}</span>
              </span>
              <span className="text-slate-300">
                Likes: <span className="text-white font-medium">{plans?.signals?.likes ?? 0}</span>
              </span>
              <span className="text-slate-300">
                Follows:{' '}
                <span className="text-white font-medium">{plans?.signals?.follows ?? 0}</span>
              </span>
              <span className="text-slate-300">
                Shares: <span className="text-white font-medium">{plans?.signals?.shares ?? 0}</span>
              </span>
            </div>
          </div>
        </div>

        {/* Block 4: System Health */}
        <div className="bg-slate-900/50 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center gap-2 mb-4">
            <Settings className="w-5 h-5 text-slate-400" />
            <h2 className="text-lg font-semibold text-white">System Health</h2>
          </div>
          <div className="flex flex-wrap gap-6">
            <StatusIndicator
              label="API p95"
              value={`${system?.api_latency_p95_ms ?? 0}ms`}
              status={getLatencyStatus(system?.api_latency_p95_ms ?? 0)}
              loading={systemLoading}
            />
            <StatusIndicator
              label="Errors"
              value={`${system?.error_rate_percent ?? 0}%`}
              status={getErrorStatus(system?.error_rate_percent ?? 0)}
              loading={systemLoading}
            />
            <StatusIndicator
              label="AI Cost"
              value={`$${(system?.ai_cost_today_usd ?? 0).toFixed(2)}`}
              status={getCostStatus(system?.ai_cost_today_usd ?? 0)}
              loading={systemLoading}
            />
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  system?.status === 'operational'
                    ? 'bg-green-500'
                    : system?.status === 'degraded'
                      ? 'bg-amber-500'
                      : 'bg-red-500'
                }`}
              />
              <span className="text-sm text-slate-400">Status:</span>
              <span className="text-sm font-medium text-white capitalize">
                {system?.status ?? 'unknown'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
