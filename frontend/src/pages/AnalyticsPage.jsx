import { BarChart3, Users, MessageSquare, TrendingUp, AlertCircle } from 'lucide-react';

const AnalyticsPage = () => {
  // Mocked data for display
  const mockStats = [
    {
      label: 'Total Conversations',
      value: '--',
      icon: MessageSquare,
      color: 'text-st-blue',
      bgColor: 'bg-st-blue-light/20'
    },
    {
      label: 'Active Users',
      value: '--',
      icon: Users,
      color: 'text-st-green',
      bgColor: 'bg-st-green/20'
    },
    {
      label: 'Avg. Rating',
      value: '--',
      icon: TrendingUp,
      color: 'text-st-orange',
      bgColor: 'bg-st-orange/20'
    },
    {
      label: 'Sessions This Week',
      value: '--',
      icon: BarChart3,
      color: 'text-st-blue-dark',
      bgColor: 'bg-st-blue-dark/20'
    }
  ];

  const mockAgentUsage = [
    { name: 'Professional Learning Coach', percentage: '--', color: 'bg-st-blue' },
    { name: 'Classroom Curriculum Planning Coach', percentage: '--', color: 'bg-st-green' }
  ];

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Analytics Dashboard</h1>
          <p className="text-gray-600">Monitor usage and engagement metrics</p>
        </div>

        {/* Notice Banner */}
        <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-800 mb-1">Analytics Coming Soon</h3>
              <p className="text-sm text-blue-700">
                This is a placeholder dashboard. Real analytics will be available once Firebase Analytics integration is complete.
              </p>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {mockStats.map((stat) => {
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
            {mockAgentUsage.map((agent) => (
              <div key={agent.name}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">{agent.name}</span>
                  <span className="text-sm text-gray-600">{agent.percentage}</span>
                </div>
                <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${agent.color} transition-all duration-300`}
                    style={{ width: '0%' }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h2>
          <div className="text-center py-8 text-gray-500">
            <BarChart3 className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>Activity data will appear here once analytics are enabled</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;
