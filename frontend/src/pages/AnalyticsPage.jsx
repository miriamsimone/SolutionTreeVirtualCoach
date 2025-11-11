import { BarChart3, Users, MessageSquare, TrendingUp, AlertCircle, RefreshCw } from 'lucide-react';
import { useAnalytics } from '../hooks/useAnalytics';

const AnalyticsPage = () => {
  const { analytics, loading, error, refetch } = useAnalytics();

  // Stats configuration
  const stats = [
    {
      label: 'Total Conversations',
      value: analytics?.total_conversations ?? '--',
      icon: MessageSquare,
      color: 'text-st-blue',
      bgColor: 'bg-st-blue-light/20'
    },
    {
      label: 'Active Users',
      value: analytics?.active_users ?? '--',
      icon: Users,
      color: 'text-st-green',
      bgColor: 'bg-st-green/20'
    },
    {
      label: 'Avg. Rating',
      value: analytics?.avg_rating ? analytics.avg_rating.toFixed(1) : '--',
      icon: TrendingUp,
      color: 'text-st-orange',
      bgColor: 'bg-st-orange/20'
    },
    {
      label: 'Sessions This Week',
      value: analytics?.sessions_this_week ?? '--',
      icon: BarChart3,
      color: 'text-st-blue-dark',
      bgColor: 'bg-st-blue-dark/20'
    }
  ];

  // Calculate agent usage percentages
  const agentUsage = analytics?.agent_usage ? [
    {
      name: 'Professional Learning Coach',
      percentage: analytics.agent_usage.professional_learning ?? 0,
      displayText: `${analytics.agent_usage.professional_learning ?? 0}%`,
      color: 'bg-st-blue'
    },
    {
      name: 'Classroom Curriculum Planning Coach',
      percentage: analytics.agent_usage.curriculum_planning ?? 0,
      displayText: `${analytics.agent_usage.curriculum_planning ?? 0}%`,
      color: 'bg-st-green'
    }
  ] : [
    { name: 'Professional Learning Coach', percentage: 0, displayText: '--', color: 'bg-st-blue' },
    { name: 'Classroom Curriculum Planning Coach', percentage: 0, displayText: '--', color: 'bg-st-green' }
  ];

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="mb-6 flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Analytics Dashboard</h1>
            <p className="text-gray-600">Monitor usage and engagement metrics</p>
          </div>
          <button
            onClick={refetch}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-red-800 mb-1">Error Loading Analytics</h3>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && !analytics && (
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <RefreshCw className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5 animate-spin" />
              <div>
                <h3 className="font-semibold text-blue-800 mb-1">Loading Analytics</h3>
                <p className="text-sm text-blue-700">Fetching usage and engagement data...</p>
              </div>
            </div>
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <div key={stat.label} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                    <Icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
                <p className="text-3xl font-bold text-gray-800 mb-1">{stat.value}</p>
                <p className="text-sm text-gray-600">{stat.label}</p>
              </div>
            );
          })}
        </div>

        {/* Agent Usage */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Agent Usage</h2>
          <div className="space-y-4">
            {agentUsage.map((agent) => (
              <div key={agent.name}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">{agent.name}</span>
                  <span className="text-sm text-gray-600">{agent.displayText}</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${agent.color} transition-all duration-500`}
                    style={{ width: `${agent.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h2>
          {analytics?.recent_activity && analytics.recent_activity.length > 0 ? (
            <div className="space-y-3">
              {analytics.recent_activity.map((activity, index) => (
                <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                  <span className="text-sm text-gray-600">
                    {new Date(activity.date).toLocaleDateString('en-US', {
                      weekday: 'short',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-st-blue transition-all duration-300"
                        style={{ width: `${Math.min(100, (activity.sessions / 20) * 100)}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium text-gray-700 w-12 text-right">
                      {activity.sessions}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <BarChart3 className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p>No recent activity data available</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;
