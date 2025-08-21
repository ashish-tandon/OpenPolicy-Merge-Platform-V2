import { useState, useEffect } from 'react';
import { 
  ChartBarIcon, UsersIcon, GlobeAltIcon, DevicePhoneMobileIcon,
  ComputerDesktopIcon, ClockIcon, EyeIcon, CursorArrowRaysIcon,
  ArrowPathIcon, FunnelIcon, CalendarIcon, TrendingUpIcon
} from '@heroicons/react/24/outline';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement,
  BarElement, ArcElement, Title, Tooltip, Legend, TimeScale
} from 'chart.js';
import 'chartjs-adapter-date-fns';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement,
  Title, Tooltip, Legend, TimeScale
);

interface UmamiStats {
  pageviews: {
    total: number;
    change: number;
  };
  visitors: {
    total: number;
    unique: number;
    change: number;
  };
  bounceRate: number;
  avgSessionDuration: string;
  topPages: Array<{
    path: string;
    views: number;
    percentage: number;
  }>;
  topCountries: Array<{
    country: string;
    visitors: number;
    percentage: number;
  }>;
  devices: {
    desktop: number;
    mobile: number;
    tablet: number;
  };
  browsers: Array<{
    name: string;
    visitors: number;
    percentage: number;
  }>;
  realTimeUsers: number;
}

interface TimeSeriesData {
  date: string;
  pageviews: number;
  visitors: number;
}

export default function UmamiAnalytics() {
  const [activeTab, setActiveTab] = useState<'overview' | 'pages' | 'audience' | 'realtime'>('overview');
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d' | '90d'>('7d');
  const [stats, setStats] = useState<UmamiStats | null>(null);
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  // Mock data for demonstration - In production, this would fetch from Umami API
  useEffect(() => {
    const fetchAnalytics = async () => {
      setIsLoading(true);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock analytics data
      const mockStats: UmamiStats = {
        pageviews: {
          total: 45672,
          change: 12.5
        },
        visitors: {
          total: 18234,
          unique: 15678,
          change: 8.3
        },
        bounceRate: 32.4,
        avgSessionDuration: '4m 32s',
        topPages: [
          { path: '/', views: 12543, percentage: 27.5 },
          { path: '/mps', views: 8764, percentage: 19.2 },
          { path: '/bills', views: 6532, percentage: 14.3 },
          { path: '/debates', views: 4987, percentage: 10.9 },
          { path: '/government', views: 3876, percentage: 8.5 },
          { path: '/search', views: 2845, percentage: 6.2 }
        ],
        topCountries: [
          { country: 'Canada', visitors: 14587, percentage: 80.0 },
          { country: 'United States', visitors: 1823, percentage: 10.0 },
          { country: 'United Kingdom', visitors: 547, percentage: 3.0 },
          { country: 'Australia', visitors: 365, percentage: 2.0 },
          { country: 'France', visitors: 273, percentage: 1.5 },
          { country: 'Germany', visitors: 182, percentage: 1.0 }
        ],
        devices: {
          desktop: 65.2,
          mobile: 28.7,
          tablet: 6.1
        },
        browsers: [
          { name: 'Chrome', visitors: 10956, percentage: 60.1 },
          { name: 'Safari', visitors: 3647, percentage: 20.0 },
          { name: 'Firefox', visitors: 1823, percentage: 10.0 },
          { name: 'Edge', visitors: 1094, percentage: 6.0 },
          { name: 'Opera', visitors: 365, percentage: 2.0 },
          { name: 'Other', visitors: 349, percentage: 1.9 }
        ],
        realTimeUsers: 47
      };

      // Generate time series data
      const days = timeRange === '24h' ? 1 : timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90;
      const mockTimeSeries: TimeSeriesData[] = [];
      
      for (let i = days - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        mockTimeSeries.push({
          date: date.toISOString().split('T')[0],
          pageviews: Math.floor(Math.random() * 2000) + 1000,
          visitors: Math.floor(Math.random() * 800) + 400
        });
      }

      setStats(mockStats);
      setTimeSeriesData(mockTimeSeries);
      setLastUpdate(new Date());
      setIsLoading(false);
    };

    fetchAnalytics();
  }, [timeRange]);

  const getCountryFlag = (country: string) => {
    const flags: { [key: string]: string } = {
      'Canada': '🇨🇦',
      'United States': '🇺🇸',
      'United Kingdom': '🇬🇧',
      'Australia': '🇦🇺',
      'France': '🇫🇷',
      'Germany': '🇩🇪'
    };
    return flags[country] || '🌍';
  };

  const lineChartData = {
    labels: timeSeriesData.map(d => d.date),
    datasets: [
      {
        label: 'Page Views',
        data: timeSeriesData.map(d => d.pageviews),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'Visitors',
        data: timeSeriesData.map(d => d.visitors),
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  const deviceChartData = stats ? {
    labels: ['Desktop', 'Mobile', 'Tablet'],
    datasets: [{
      data: [stats.devices.desktop, stats.devices.mobile, stats.devices.tablet],
      backgroundColor: ['#3B82F6', '#10B981', '#F59E0B'],
      borderWidth: 0
    }]
  } : null;

  if (isLoading || !stats) {
    return (
      <div className="lg:pl-64">
        <div className="px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center min-h-96">
            <div className="text-center">
              <ArrowPathIcon className="h-12 w-12 text-blue-500 animate-spin mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Loading Analytics Data</h3>
              <p className="text-gray-500">Fetching latest Umami analytics...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="lg:pl-64">
      <div className="px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Website Analytics</h1>
              <p className="text-gray-600 mt-1">OpenParliament.ca & Admin Dashboard</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-gray-500">
                <ClockIcon className="h-4 w-4 mr-1" />
                Last updated: {lastUpdate.toLocaleTimeString()}
              </div>
              <div className="flex items-center bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                {stats.realTimeUsers} active users
              </div>
            </div>
          </div>
        </div>

        {/* Time Range Selector */}
        <div className="mb-6">
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <CalendarIcon className="h-5 w-5 text-gray-400 mr-2" />
              <span className="text-sm font-medium text-gray-700">Time Range:</span>
            </div>
            <div className="flex rounded-lg border border-gray-300 overflow-hidden">
              {[
                { key: '24h', label: '24 Hours' },
                { key: '7d', label: '7 Days' },
                { key: '30d', label: '30 Days' },
                { key: '90d', label: '90 Days' }
              ].map(({ key, label }) => (
                <button
                  key={key}
                  onClick={() => setTimeRange(key as any)}
                  className={`px-4 py-2 text-sm font-medium ${
                    timeRange === key
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  } transition-colors`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'overview', name: 'Overview', icon: ChartBarIcon },
                { id: 'pages', name: 'Pages', icon: GlobeAltIcon },
                { id: 'audience', name: 'Audience', icon: UsersIcon },
                { id: 'realtime', name: 'Real-time', icon: TrendingUpIcon }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="h-5 w-5 mr-2" />
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <EyeIcon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Page Views</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.pageviews.total.toLocaleString()}</p>
                    <p className="text-xs text-green-600">+{stats.pageviews.change}% from last period</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <UsersIcon className="h-6 w-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Visitors</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.visitors.total.toLocaleString()}</p>
                    <p className="text-xs text-green-600">+{stats.visitors.change}% from last period</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <CursorArrowRaysIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Bounce Rate</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.bounceRate}%</p>
                    <p className="text-xs text-gray-500">Lower is better</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <ClockIcon className="h-6 w-6 text-orange-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Avg. Session</p>
                    <p className="text-2xl font-semibold text-gray-900">{stats.avgSessionDuration}</p>
                    <p className="text-xs text-gray-500">Duration per visit</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Traffic Chart */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Traffic Overview</h3>
              <div className="h-80">
                <Line
                  data={lineChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'top' as const,
                      }
                    },
                    scales: {
                      y: {
                        beginAtZero: true
                      }
                    }
                  }}
                />
              </div>
            </div>

            {/* Device Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Device Types</h3>
                <div className="h-64">
                  {deviceChartData && (
                    <Doughnut
                      data={deviceChartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom' as const,
                          }
                        }
                      }}
                    />
                  )}
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Top Browsers</h3>
                <div className="space-y-3">
                  {stats.browsers.map((browser, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="w-3 h-3 rounded-full mr-3" style={{
                          backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#6B7280'][index]
                        }}></div>
                        <span className="text-sm font-medium text-gray-900">{browser.name}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-sm text-gray-600">{browser.visitors.toLocaleString()}</span>
                        <span className="text-xs text-gray-400 ml-2">({browser.percentage}%)</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Pages Tab */}
        {activeTab === 'pages' && (
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Top Pages</h3>
              <p className="text-sm text-gray-600">Most visited pages on your website</p>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Page</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Views</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">% of Total</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Visual</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {stats.topPages.map((page, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-blue-600 hover:text-blue-800">
                          {page.path === '/' ? 'Homepage' : page.path}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {page.views.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {page.percentage}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${page.percentage}%` }}
                          ></div>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Audience Tab */}
        {activeTab === 'audience' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Top Countries</h3>
                <p className="text-sm text-gray-600">Visitor distribution by country</p>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {stats.topCountries.map((country, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className="text-2xl mr-3">{getCountryFlag(country.country)}</span>
                        <span className="text-sm font-medium text-gray-900">{country.country}</span>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${country.percentage}%` }}
                          ></div>
                        </div>
                        <div className="text-right min-w-[100px]">
                          <span className="text-sm text-gray-600">{country.visitors.toLocaleString()}</span>
                          <span className="text-xs text-gray-400 ml-2">({country.percentage}%)</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Real-time Tab */}
        {activeTab === 'realtime' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-center">
                <div className="text-6xl font-bold text-blue-600 mb-2">{stats.realTimeUsers}</div>
                <p className="text-gray-600 mb-4">Active users right now</p>
                <div className="flex items-center justify-center text-sm text-gray-500">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                  Live data updates every 30 seconds
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Real-time Activity</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">Page views in last minute</span>
                  <span className="text-sm font-medium text-gray-900">34</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">New visitors</span>
                  <span className="text-sm font-medium text-gray-900">12</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">Returning visitors</span>
                  <span className="text-sm font-medium text-gray-900">35</span>
                </div>
                <div className="flex items-center justify-between py-2">
                  <span className="text-sm text-gray-600">Average session duration</span>
                  <span className="text-sm font-medium text-gray-900">3m 45s</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
