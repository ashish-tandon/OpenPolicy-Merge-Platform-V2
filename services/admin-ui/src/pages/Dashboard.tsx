import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  UsersIcon,
  DocumentTextIcon,
  BuildingOfficeIcon,
  ServerIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

interface SystemStats {
  totalRepresentatives: number;
  totalBills: number;
  totalJurisdictions: number;
  totalVotes: number;
  activeScrapers: number;
  dataQualityScore: number;
  lastDataUpdate: string;
  systemHealth: 'healthy' | 'warning' | 'error';
}

interface RecentActivity {
  id: string;
  type: 'data_ingestion' | 'user_action' | 'system_event' | 'error';
  message: string;
  timestamp: string;
  severity: 'info' | 'warning' | 'error';
}

interface DataSourceStatus {
  name: string;
  status: 'active' | 'inactive' | 'error';
  lastUpdate: string;
  recordCount: number;
  health: 'good' | 'warning' | 'critical';
}

export default function Dashboard() {
  const [stats, setStats] = useState<SystemStats>({
    totalRepresentatives: 0,
    totalBills: 0,
    totalJurisdictions: 0,
    totalVotes: 0,
    activeScrapers: 0,
    dataQualityScore: 0,
    lastDataUpdate: '',
    systemHealth: 'healthy'
  });

  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [dataSources, setDataSources] = useState<DataSourceStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch system statistics
        const statsResponse = await fetch('/api/v1/multi-level-government/stats');

        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setStats({
            totalRepresentatives: statsData.total_representatives || 0,
            totalBills: statsData.total_bills || 0,
            totalJurisdictions: statsData.total_jurisdictions || 0,
            totalVotes: statsData.total_votes || 0,
            activeScrapers: 3, // Mock data for now
            dataQualityScore: 94, // Mock data for now
            lastDataUpdate: new Date().toISOString(),
            systemHealth: 'healthy'
          });
        }

        // Mock recent activity data
        setRecentActivity([
          {
            id: '1',
            type: 'data_ingestion',
            message: 'Successfully ingested data from Toronto City Council',
            timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
            severity: 'info'
          },
          {
            id: '2',
            type: 'user_action',
            message: 'Admin user updated representative profile for John Smith',
            timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
            severity: 'info'
          },
          {
            id: '3',
            type: 'system_event',
            message: 'Scheduled data quality check completed',
            timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
            severity: 'info'
          },
          {
            id: '4',
            type: 'error',
            message: 'Failed to connect to Vancouver data source',
            timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
            severity: 'warning'
          }
        ]);

        // Mock data source status
        setDataSources([
          {
            name: 'Federal Parliament',
            status: 'active',
            lastUpdate: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
            recordCount: 1250,
            health: 'good'
          },
          {
            name: 'Ontario Legislature',
            status: 'active',
            lastUpdate: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
            recordCount: 890,
            health: 'good'
          },
          {
            name: 'Toronto City Council',
            status: 'active',
            lastUpdate: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
            recordCount: 456,
            health: 'good'
          },
          {
            name: 'Vancouver City Council',
            status: 'error',
            lastUpdate: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
            recordCount: 234,
            health: 'critical'
          }
        ]);

      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'good': return 'text-green-600 bg-green-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'critical': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'error': return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      case 'warning': return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
      default: return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
    }
  };

  if (loading) {
    return (
      <div className="lg:pl-64">
        <div className="px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-op-blue"></div>
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
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Overview of the OpenPolicy platform and system health
          </p>
        </div>

        {/* System Health Status */}
        <div className="mb-8">
          <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
            stats.systemHealth === 'healthy' ? 'bg-green-100 text-green-800' :
            stats.systemHealth === 'warning' ? 'bg-yellow-100 text-yellow-800' :
            'bg-red-100 text-red-800'
          }`}>
            {stats.systemHealth === 'healthy' ? (
              <CheckCircleIcon className="h-4 w-4 mr-2" />
            ) : (
              <ExclamationTriangleIcon className="h-4 w-4 mr-2" />
            )}
            System Status: {stats.systemHealth.charAt(0).toUpperCase() + stats.systemHealth.slice(1)}
          </div>
        </div>

        {/* Key Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <UsersIcon className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Representatives</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.totalRepresentatives.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <DocumentTextIcon className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Bills</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.totalBills.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <BuildingOfficeIcon className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Jurisdictions</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.totalJurisdictions.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-orange-100 rounded-lg">
                <ChartBarIcon className="h-6 w-6 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Data Quality</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.dataQualityScore}%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Data Sources Status */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Data Sources Status</h3>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {dataSources.map((source) => (
                  <div key={source.name} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className={`w-3 h-3 rounded-full mr-3 ${
                        source.health === 'good' ? 'bg-green-400' :
                        source.health === 'warning' ? 'bg-yellow-400' :
                        'bg-red-400'
                      }`} />
                      <div>
                        <p className="text-sm font-medium text-gray-900">{source.name}</p>
                        <p className="text-xs text-gray-500">
                          {source.recordCount.toLocaleString()} records
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`text-xs px-2 py-1 rounded-full ${getHealthColor(source.health)}`}>
                        {source.health}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(source.lastUpdate).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4">
                <Link
                  to="/etl"
                  className="text-sm text-op-blue hover:text-blue-700 font-medium"
                >
                  View all data sources →
                </Link>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3">
                    {getSeverityIcon(activity.severity)}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900">{activity.message}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(activity.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4">
                <Link
                  to="/monitoring"
                  className="text-sm text-op-blue hover:text-blue-700 font-medium"
                >
                  View all activity →
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Link
                to="/data/quality"
                className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-op-blue hover:bg-blue-50 transition-colors"
              >
                <ServerIcon className="h-6 w-6 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Run Data Quality Check</p>
                  <p className="text-xs text-gray-500">Validate data integrity</p>
                </div>
              </Link>

              <Link
                to="/etl"
                className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-op-blue hover:bg-blue-50 transition-colors"
              >
                <ServerIcon className="h-6 w-6 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Manage ETL Jobs</p>
                  <p className="text-xs text-gray-500">Control data pipelines</p>
                </div>
              </Link>

              <Link
                to="/representatives"
                className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-op-blue hover:bg-blue-50 transition-colors"
              >
                <UsersIcon className="h-6 w-6 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Manage Representatives</p>
                  <p className="text-xs text-gray-500">Update profiles and data</p>
                </div>
              </Link>

              <Link
                to="/bills"
                className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-op-blue hover:bg-blue-50 transition-colors"
              >
                <DocumentTextIcon className="h-6 w-6 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Manage Bills</p>
                  <p className="text-xs text-gray-500">Update legislation data</p>
                </div>
              </Link>
            </div>
          </div>
        </div>

        {/* System Information */}
        <div className="mt-8 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">System Information</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h4 className="text-sm font-medium text-gray-500 mb-2">Last Data Update</h4>
                <p className="text-sm text-gray-900">
                  {new Date(stats.lastDataUpdate).toLocaleString()}
                </p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-500 mb-2">Active Scrapers</h4>
                <p className="text-sm text-gray-900">{stats.activeScrapers} running</p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-500 mb-2">Total Votes</h4>
                <p className="text-sm text-gray-900">{stats.totalVotes.toLocaleString()} recorded</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
