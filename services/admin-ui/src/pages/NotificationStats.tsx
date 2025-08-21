import { useState, useEffect } from 'react';
import { 
  ChartBarIcon, BellIcon, EnvelopeIcon, ChatBubbleLeftRightIcon, 
  DevicePhoneMobileIcon, CheckCircleIcon, XCircleIcon, ClockIcon,
  ArrowTrendingUpIcon, EyeIcon, CogIcon
} from '@heroicons/react/24/outline';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface NotificationStats {
  totalSent: number;
  totalDelivered: number;
  totalFailed: number;
  deliveryRate: number;
  averageResponseTime: number;
  activeServices: number;
  totalTemplates: number;
}

interface ChannelStats {
  channel: string;
  sent: number;
  delivered: number;
  failed: number;
  deliveryRate: number;
}

interface TimeSeriesData {
  date: string;
  sent: number;
  delivered: number;
  failed: number;
}

export default function NotificationStats() {
  const [activeTab, setActiveTab] = useState<'overview' | 'channels' | 'templates' | 'performance'>('overview');
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d' | '90d'>('7d');
  const [stats, setStats] = useState<NotificationStats | null>(null);
  const [channelStats, setChannelStats] = useState<ChannelStats[]>([]);
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData[]>([]);

  // Mock data for demonstration
  useEffect(() => {
    setStats({
      totalSent: 15420,
      totalDelivered: 14890,
      totalFailed: 530,
      deliveryRate: 96.6,
      averageResponseTime: 1.2,
      activeServices: 6,
      totalTemplates: 8
    });

    setChannelStats([
      { channel: 'Email', sent: 8230, delivered: 7980, failed: 250, deliveryRate: 97.0 },
      { channel: 'Slack', sent: 4560, delivered: 4450, failed: 110, deliveryRate: 97.6 },
      { channel: 'SMS', sent: 1890, delivered: 1820, failed: 70, deliveryRate: 96.3 },
      { channel: 'Discord', sent: 740, delivered: 640, failed: 100, deliveryRate: 86.5 }
    ]);

    // Generate time series data for the last 7 days
    const generateTimeSeriesData = () => {
      const data: TimeSeriesData[] = [];
      const today = new Date();
      
      for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        
        const sent = Math.floor(Math.random() * 500) + 200;
        const delivered = Math.floor(sent * 0.95 + Math.random() * 0.1);
        const failed = sent - delivered;
        
        data.push({
          date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          sent,
          delivered,
          failed
        });
      }
      
      return data;
    };

    setTimeSeriesData(generateTimeSeriesData());
  }, []);

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case 'email': return <EnvelopeIcon className="h-5 w-5 text-blue-500" />;
      case 'slack': return <ChatBubbleLeftRightIcon className="h-5 w-5 text-purple-500" />;
      case 'sms': return <DevicePhoneMobileIcon className="h-5 w-5 text-green-500" />;
      case 'discord': return <ChatBubbleLeftRightIcon className="h-5 w-5 text-indigo-500" />;
      case 'telegram': return <ChatBubbleLeftRightIcon className="h-5 w-5 text-blue-400" />;
      case 'whatsapp': return <DevicePhoneMobileIcon className="h-5 w-5 text-green-400" />;
      default: return <BellIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  // This function will be used in future iterations
  // const getStatusColor = (status: 'success' | 'warning' | 'error') => {
  //   switch (status) {
  //     case 'success': return 'text-green-600 bg-green-100';
  //     case 'warning': return 'text-yellow-600 bg-yellow-100';
  //     case 'error': return 'text-red-600 bg-red-100';
  //     default: return 'text-gray-600 bg-gray-100';
  //   }
  // };

  const getDeliveryRateColor = (rate: number) => {
    if (rate >= 95) return 'text-green-600';
    if (rate >= 85) return 'text-yellow-600';
    return 'text-red-600';
  };

  const lineChartData = {
    labels: timeSeriesData.map(d => d.date),
    datasets: [
      {
        label: 'Sent',
        data: timeSeriesData.map(d => d.sent),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
      {
        label: 'Delivered',
        data: timeSeriesData.map(d => d.delivered),
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4,
      },
      {
        label: 'Failed',
        data: timeSeriesData.map(d => d.failed),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const channelChartData = {
    labels: channelStats.map(c => c.channel),
    datasets: [
      {
        label: 'Delivery Rate (%)',
        data: channelStats.map(c => c.deliveryRate),
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(147, 51, 234, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(99, 102, 241, 0.8)',
        ],
        borderColor: [
          'rgb(59, 130, 246)',
          'rgb(147, 51, 234)',
          'rgb(34, 197, 94)',
          'rgb(99, 102, 241)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const doughnutData = {
    labels: ['Delivered', 'Failed'],
    datasets: [
      {
        data: [stats?.totalDelivered || 0, stats?.totalFailed || 0],
        backgroundColor: ['rgba(34, 197, 94, 0.8)', 'rgba(239, 68, 68, 0.8)'],
        borderColor: ['rgb(34, 197, 94)', 'rgb(239, 68, 68)'],
        borderWidth: 2,
      },
    ],
  };

  if (!stats) return <div>Loading...</div>;

  return (
    <div className="lg:pl-64">
      <div className="px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Notification Statistics</h1>
          <p className="mt-2 text-gray-600">
            Monitor and analyze notification performance across all channels
          </p>
        </div>

        {/* Time Range Selector */}
        <div className="mb-6">
          <div className="flex items-center space-x-4">
            <label className="text-sm font-medium text-gray-700">Time Range:</label>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value as any)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
            >
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: ChartBarIcon },
              { id: 'channels', name: 'Channels', icon: BellIcon },
              { id: 'templates', name: 'Templates', icon: CogIcon },
              { id: 'performance', name: 'Performance', icon: ArrowTrendingUpIcon }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === tab.id
                    ? 'text-op-blue bg-op-blue-50 border-b-2 border-op-blue'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <BellIcon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Sent</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.totalSent.toLocaleString()}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <CheckCircleIcon className="h-6 w-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Delivered</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.totalDelivered.toLocaleString()}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <XCircleIcon className="h-6 w-6 text-red-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Failed</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.totalFailed.toLocaleString()}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 rounded-lg">
                                          <ArrowTrendingUpIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Delivery Rate</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.deliveryRate}%</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Notification Trends</h3>
                <Line data={lineChartData} options={{
                  responsive: true,
                  plugins: {
                    legend: { position: 'top' },
                    title: { display: false }
                  },
                  scales: {
                    y: { beginAtZero: true }
                  }
                }} />
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Delivery Overview</h3>
                <Doughnut data={doughnutData} options={{
                  responsive: true,
                  plugins: {
                    legend: { position: 'bottom' },
                    title: { display: false }
                  }
                }} />
              </div>
            </div>

            {/* Additional Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Active Services</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.activeServices}</p>
                  </div>
                  <CogIcon className="h-8 w-8 text-gray-400" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Templates</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.totalTemplates}</p>
                  </div>
                  <CogIcon className="h-8 w-8 text-gray-400" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.averageResponseTime}s</p>
                  </div>
                  <ClockIcon className="h-8 w-8 text-gray-400" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Channels Tab */}
        {activeTab === 'channels' && (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900">Channel Performance</h2>
            
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Channel Statistics</h3>
              <Bar data={channelChartData} options={{
                responsive: true,
                plugins: {
                  legend: { display: false },
                  title: { display: false }
                },
                scales: {
                  y: { 
                    beginAtZero: true,
                    max: 100,
                    ticks: { callback: (value) => `${value}%` }
                  }
                }
              }} />
            </div>

            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Channel Details</h3>
              </div>
              <div className="divide-y divide-gray-200">
                {channelStats.map((channel) => (
                  <div key={channel.channel} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        {getChannelIcon(channel.channel)}
                        <div>
                          <h4 className="text-lg font-medium text-gray-900">{channel.channel}</h4>
                          <p className="text-sm text-gray-500">
                            {channel.sent.toLocaleString()} sent • {channel.delivered.toLocaleString()} delivered
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`text-lg font-semibold ${getDeliveryRateColor(channel.deliveryRate)}`}>
                          {channel.deliveryRate}%
                        </p>
                        <p className="text-sm text-gray-500">delivery rate</p>
                      </div>
                    </div>
                    
                    <div className="mt-4 grid grid-cols-3 gap-4">
                      <div className="text-center">
                        <p className="text-2xl font-semibold text-gray-900">{channel.sent.toLocaleString()}</p>
                        <p className="text-sm text-gray-500">Sent</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-semibold text-green-600">{channel.delivered.toLocaleString()}</p>
                        <p className="text-sm text-gray-500">Delivered</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-semibold text-red-600">{channel.failed.toLocaleString()}</p>
                        <p className="text-sm text-gray-500">Failed</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Templates Tab */}
        {activeTab === 'templates' && (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900">Template Performance</h2>
            
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Template Usage Statistics</h3>
              </div>
              <div className="divide-y divide-gray-200">
                {[
                  { name: 'OTP Verification', sent: 5230, success: 98.5, avgTime: 0.8 },
                  { name: 'Welcome Message', sent: 1890, success: 99.2, avgTime: 1.1 },
                  { name: 'Parliamentary Alert', sent: 4560, success: 96.8, avgTime: 1.5 },
                  { name: 'Bill Update', sent: 2340, success: 97.3, avgTime: 1.2 },
                  { name: 'Vote Reminder', sent: 1400, success: 95.7, avgTime: 1.8 }
                ].map((template) => (
                  <div key={template.name} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-lg font-medium text-gray-900">{template.name}</h4>
                        <p className="text-sm text-gray-500">
                          {template.sent.toLocaleString()} notifications sent
                        </p>
                      </div>
                      <div className="text-right">
                        <p className={`text-lg font-semibold ${getDeliveryRateColor(template.success)}`}>
                          {template.success}%
                        </p>
                        <p className="text-sm text-gray-500">success rate</p>
                      </div>
                    </div>
                    
                    <div className="mt-4 grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <p className="text-xl font-semibold text-gray-900">{template.sent.toLocaleString()}</p>
                        <p className="text-sm text-gray-500">Total Sent</p>
                      </div>
                      <div className="text-center">
                        <p className="text-xl font-semibold text-blue-600">{template.avgTime}s</p>
                        <p className="text-sm text-gray-500">Avg Response Time</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Performance Tab */}
        {activeTab === 'performance' && (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900">Performance Metrics</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Response Time Trends</h3>
                <Line data={{
                  labels: timeSeriesData.map(d => d.date),
                  datasets: [{
                    label: 'Average Response Time (s)',
                    data: timeSeriesData.map(() => Math.random() * 2 + 0.5),
                    borderColor: 'rgb(147, 51, 234)',
                    backgroundColor: 'rgba(147, 51, 234, 0.1)',
                    tension: 0.4,
                  }]
                }} options={{
                  responsive: true,
                  plugins: {
                    legend: { position: 'top' },
                    title: { display: false }
                  },
                  scales: {
                    y: { beginAtZero: true }
                  }
                }} />
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Error Rate Analysis</h3>
                <Bar data={{
                  labels: ['Email', 'Slack', 'SMS', 'Discord'],
                  datasets: [{
                    label: 'Error Rate (%)',
                    data: [3.0, 2.4, 3.7, 13.5],
                    backgroundColor: [
                      'rgba(59, 130, 246, 0.8)',
                      'rgba(147, 51, 234, 0.8)',
                      'rgba(34, 197, 94, 0.8)',
                      'rgba(99, 102, 241, 0.8)',
                    ],
                  }]
                }} options={{
                  responsive: true,
                  plugins: {
                    legend: { display: false },
                    title: { display: false }
                  },
                  scales: {
                    y: { 
                      beginAtZero: true,
                      max: 20,
                      ticks: { callback: (value) => `${value}%` }
                    }
                  }
                }} />
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Performance Insights</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <ArrowTrendingUpIcon className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <p className="text-sm font-medium text-green-800">Excellent Performance</p>
                  <p className="text-xs text-green-600">96.6% delivery rate</p>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <ClockIcon className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                  <p className="text-sm font-medium text-yellow-800">Fast Response</p>
                  <p className="text-xs text-yellow-600">1.2s average</p>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <EyeIcon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <p className="text-sm font-medium text-blue-800">High Volume</p>
                  <p className="text-xs text-blue-600">15K+ notifications</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
