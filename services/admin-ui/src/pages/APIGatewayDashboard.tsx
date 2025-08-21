import { useState, useEffect } from 'react';
import {
  ServerIcon,
  GlobeAltIcon,
  ChartBarIcon,
  ClockIcon,
  EyeIcon,
  CogIcon,
  BoltIcon
} from '@heroicons/react/24/outline';

interface APIEndpoint {
  path: string;
  method: string;
  status: 'active' | 'deprecated' | 'maintenance' | 'error';
  lastUsed: string;
  usageCount: number;
  avgResponseTime: number;
  errorRate: number;
  version: string;
  description: string;
  rateLimit: string;
  authentication: boolean;
  documentation: string;
}

interface APIService {
  name: string;
  port: number;
  status: 'running' | 'stopped' | 'error' | 'maintenance';
  uptime: string;
  version: string;
  lastRestart: string;
  memoryUsage: number;
  cpuUsage: number;
  activeConnections: number;
  maxConnections: number;
  health: 'healthy' | 'warning' | 'critical';
  endpoints: APIEndpoint[];
}

interface APIMetrics {
  totalEndpoints: number;
  activeEndpoints: number;
  totalRequests: number;
  avgResponseTime: number;
  errorRate: number;
  activeUsers: number;
  peakConcurrentUsers: number;
  totalDataTransferred: string;
  cacheHitRatio: number;
}

export default function APIGatewayDashboard() {
  const [services, setServices] = useState<APIService[]>([]);
  const [metrics, setMetrics] = useState<APIMetrics>({
    totalEndpoints: 0,
    activeEndpoints: 0,
    totalRequests: 0,
    avgResponseTime: 0,
    errorRate: 0,
    activeUsers: 0,
    peakConcurrentUsers: 0,
    totalDataTransferred: '0 MB',
    cacheHitRatio: 0
  });
  const [selectedEndpoint, setSelectedEndpoint] = useState<APIEndpoint | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'services' | 'endpoints' | 'performance'>('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAPIData();
    const interval = setInterval(fetchAPIData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchAPIData = async () => {
    try {
      // Mock data - replace with actual API calls
      const mockServices: APIService[] = [
        {
          name: 'API Gateway',
          port: 8080,
          status: 'running',
          uptime: '45 days, 12 hours',
          version: '1.2.0',
          lastRestart: new Date(Date.now() - 1000 * 60 * 60 * 24 * 45).toISOString(),
          memoryUsage: 45.2,
          cpuUsage: 23.8,
          activeConnections: 156,
          maxConnections: 1000,
          health: 'healthy',
          endpoints: [
            {
              path: '/api/v1/multi-level-government/government-levels',
              method: 'GET',
              status: 'active',
              lastUsed: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
              usageCount: 1247,
              avgResponseTime: 45,
              errorRate: 0.2,
              version: 'v1',
              description: 'Retrieve all government levels',
              rateLimit: '1000/hour',
              authentication: false,
              documentation: '/docs/api#get-government-levels'
            },
            {
              path: '/api/v1/multi-level-government/jurisdictions',
              method: 'GET',
              status: 'active',
              lastUsed: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
              usageCount: 892,
              avgResponseTime: 67,
              errorRate: 0.1,
              version: 'v1',
              description: 'Retrieve jurisdictions with pagination',
              rateLimit: '1000/hour',
              authentication: false,
              documentation: '/docs/api#get-jurisdictions'
            },
            {
              path: '/api/v1/multi-level-government/representatives',
              method: 'GET',
              status: 'active',
              lastUsed: new Date(Date.now() - 1000 * 60 * 1).toISOString(),
              usageCount: 2156,
              avgResponseTime: 89,
              errorRate: 0.3,
              version: 'v1',
              description: 'Retrieve representatives with filters',
              rateLimit: '1000/hour',
              authentication: false,
              documentation: '/docs/api#get-representatives'
            },
            {
              path: '/api/v1/multi-level-government/bills',
              method: 'GET',
              status: 'active',
              lastUsed: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
              usageCount: 1876,
              avgResponseTime: 123,
              errorRate: 0.5,
              version: 'v1',
              description: 'Retrieve bills with search and filters',
              rateLimit: '1000/hour',
              authentication: false,
              documentation: '/docs/api#get-bills'
            },
            {
              path: '/api/v1/multi-level-government/stats',
              method: 'GET',
              status: 'active',
              lastUsed: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
              usageCount: 445,
              avgResponseTime: 34,
              errorRate: 0.1,
              version: 'v1',
              description: 'Get system-wide statistics',
              rateLimit: '500/hour',
              authentication: false,
              documentation: '/docs/api#get-stats'
            }
          ]
        },
        {
          name: 'ETL Service',
          port: 8081,
          status: 'running',
          uptime: '12 days, 8 hours',
          version: '2.1.0',
          lastRestart: new Date(Date.now() - 1000 * 60 * 60 * 24 * 12).toISOString(),
          memoryUsage: 67.8,
          cpuUsage: 45.2,
          activeConnections: 23,
          maxConnections: 100,
          health: 'warning',
          endpoints: [
            {
              path: '/api/v1/etl/jobs',
              method: 'GET',
              status: 'active',
              lastUsed: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
              usageCount: 89,
              avgResponseTime: 156,
              errorRate: 2.1,
              version: 'v1',
              description: 'Get ETL job status',
              rateLimit: '100/hour',
              authentication: true,
              documentation: '/docs/etl#get-jobs'
            }
          ]
        },
        {
          name: 'Admin Service',
          port: 8082,
          status: 'running',
          uptime: '3 days, 15 hours',
          version: '1.0.0',
          lastRestart: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3).toISOString(),
          memoryUsage: 23.4,
          cpuUsage: 12.7,
          activeConnections: 8,
          maxConnections: 50,
          health: 'healthy',
          endpoints: [
            {
              path: '/api/v1/admin/activity',
              method: 'GET',
              status: 'active',
              lastUsed: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
              usageCount: 156,
              avgResponseTime: 78,
              errorRate: 0.0,
              version: 'v1',
              description: 'Get admin activity logs',
              rateLimit: '100/hour',
              authentication: true,
              documentation: '/docs/admin#get-activity'
            }
          ]
        }
      ];

      setServices(mockServices);
      setMetrics({
        totalEndpoints: mockServices.reduce((sum, service) => sum + service.endpoints.length, 0),
        activeEndpoints: mockServices.reduce((sum, service) => sum + service.endpoints.filter(e => e.status === 'active').length, 0),
        totalRequests: mockServices.reduce((sum, service) => sum + service.endpoints.reduce((eSum, endpoint) => eSum + endpoint.usageCount, 0), 0),
        avgResponseTime: Math.round(mockServices.reduce((sum, service) => sum + service.endpoints.reduce((eSum, endpoint) => eSum + endpoint.avgResponseTime, 0), 0) / mockServices.reduce((sum, service) => sum + service.endpoints.length, 0)),
        errorRate: Math.round((mockServices.reduce((sum, service) => sum + service.endpoints.reduce((eSum, endpoint) => eSum + (endpoint.usageCount * endpoint.errorRate / 100), 0), 0) / mockServices.reduce((sum, service) => sum + service.endpoints.reduce((eSum, endpoint) => eSum + endpoint.usageCount, 0), 0)) * 100 * 100) / 100,
        activeUsers: 89,
        peakConcurrentUsers: 156,
        totalDataTransferred: '2.4 GB',
        cacheHitRatio: 87.3
      });
    } catch (error) {
      console.error('Failed to fetch API data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-green-100 text-green-800';
      case 'stopped': return 'bg-red-100 text-red-800';
      case 'error': return 'bg-red-100 text-red-800';
      case 'maintenance': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'healthy': return 'bg-green-100 text-green-800';
      case 'warning': return 'bg-yellow-100 text-yellow-800';
      case 'critical': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getEndpointStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'deprecated': return 'bg-yellow-100 text-yellow-800';
      case 'maintenance': return 'bg-blue-100 text-blue-800';
      case 'error': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getMethodColor = (method: string) => {
    switch (method) {
      case 'GET': return 'bg-green-100 text-green-800';
      case 'POST': return 'bg-blue-100 text-blue-800';
      case 'PUT': return 'bg-yellow-100 text-yellow-800';
      case 'DELETE': return 'bg-red-100 text-red-800';
      case 'PATCH': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
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
          <h1 className="text-3xl font-bold text-gray-900">API Gateway Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Monitor API services, endpoints, performance, and usage across all OpenPolicy APIs
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: ChartBarIcon },
              { id: 'services', name: 'Services', icon: ServerIcon },
              { id: 'endpoints', name: 'Endpoints', icon: GlobeAltIcon },
              { id: 'performance', name: 'Performance', icon: BoltIcon }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-op-blue text-op-blue'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
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
            {/* API Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <GlobeAltIcon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Endpoints</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.totalEndpoints}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <BoltIcon className="h-6 w-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Requests</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.totalRequests.toLocaleString()}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <ClockIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Avg Response</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.avgResponseTime}ms</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <ChartBarIcon className="h-6 w-6 text-orange-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Error Rate</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.errorRate}%</p>
                  </div>
                </div>
          </div>
            </div>

            {/* Services Overview */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">API Services Status</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    {services.map((service) => (
                      <div key={service.name} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`w-3 h-3 rounded-full ${
                            service.health === 'healthy' ? 'bg-green-400' :
                            service.health === 'warning' ? 'bg-yellow-400' :
                            'bg-red-400'
                          }`} />
                          <div>
                            <div className="text-sm font-medium text-gray-900">{service.name}</div>
                            <div className="text-xs text-gray-500">Port {service.port}</div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                            {service.status}
                          </span>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getHealthColor(service.health)}`}>
                            {service.health}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">Performance Metrics</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Active Users</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.activeUsers}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Peak Concurrent</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.peakConcurrentUsers}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Data Transferred</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.totalDataTransferred}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Cache Hit Ratio</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.cacheHitRatio}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Services Tab */}
        {activeTab === 'services' && (
          <div className="space-y-6">
            {services.map((service) => (
              <div key={service.name} className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">{service.name}</h3>
                      <p className="text-sm text-gray-600">Port {service.port} • Version {service.version}</p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                        {service.status}
                      </span>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getHealthColor(service.health)}`}>
                        {service.health}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                    <div>
                      <p className="text-sm font-medium text-gray-500">Uptime</p>
                      <p className="text-sm text-gray-900">{service.uptime}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">Memory Usage</p>
                      <p className="text-sm text-gray-900">{service.memoryUsage}%</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">CPU Usage</p>
                      <p className="text-sm text-gray-900">{service.cpuUsage}%</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">Connections</p>
                      <p className="text-sm text-gray-900">{service.activeConnections}/{service.maxConnections}</p>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-3">Endpoints ({service.endpoints.length})</h4>
                    <div className="space-y-2">
                      {service.endpoints.map((endpoint) => (
                        <div key={endpoint.path} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                          <div className="flex items-center space-x-2">
                            <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${getMethodColor(endpoint.method)}`}>
                              {endpoint.method}
                            </span>
                            <span className="text-sm font-medium text-gray-900">{endpoint.path}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-xs text-gray-500">
                            <span>{endpoint.usageCount} requests</span>
                            <span>{endpoint.avgResponseTime}ms</span>
                            <span className={`${endpoint.errorRate > 1 ? 'text-red-600' : 'text-green-600'}`}>
                              {endpoint.errorRate}% error
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Endpoints Tab */}
        {activeTab === 'endpoints' && (
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">All API Endpoints</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Method
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Path
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Version
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Usage
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Response Time
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Error Rate
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Used
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {services.flatMap(service => 
                    service.endpoints.map(endpoint => (
                      <tr key={`${service.name}.${endpoint.path}`} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getMethodColor(endpoint.method)}`}>
                            {endpoint.method}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">{endpoint.path}</div>
                          <div className="text-xs text-gray-500">{endpoint.description}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getEndpointStatusColor(endpoint.status)}`}>
                            {endpoint.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {endpoint.version}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {endpoint.usageCount.toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {endpoint.avgResponseTime}ms
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          <span className={`${endpoint.errorRate > 1 ? 'text-red-600' : 'text-green-600'}`}>
                            {endpoint.errorRate}%
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {new Date(endpoint.lastUsed).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex space-x-2">
                            <button
                              onClick={() => setSelectedEndpoint(endpoint)}
                              className="text-op-blue hover:text-blue-700"
                              title="View Details"
                            >
                              <EyeIcon className="h-4 w-4" />
                            </button>
                            <button className="text-gray-400 hover:text-gray-600" title="Configure">
                              <CogIcon className="h-4 w-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Performance Tab */}
        {activeTab === 'performance' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">Response Time Trends</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    {services.flatMap(service => 
                      service.endpoints.map(endpoint => (
                        <div key={`${service.name}.${endpoint.path}`} className="border-b border-gray-100 pb-3 last:border-b-0">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-900">{endpoint.method} {endpoint.path}</span>
                            <span className="text-xs text-gray-500">{endpoint.avgResponseTime}ms</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                endpoint.avgResponseTime < 50 ? 'bg-green-600' :
                                endpoint.avgResponseTime < 100 ? 'bg-yellow-600' :
                                'bg-red-600'
                              }`}
                              style={{ width: `${Math.min((endpoint.avgResponseTime / 200) * 100, 100)}%` }}
                            ></div>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">Error Rate Analysis</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    {services.flatMap(service => 
                      service.endpoints.map(endpoint => (
                        <div key={`${service.name}.${endpoint.path}`} className="border-b border-gray-100 pb-3 last:border-b-0">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-900">{endpoint.method} {endpoint.path}</span>
                            <span className={`text-xs ${endpoint.errorRate > 1 ? 'text-red-600' : 'text-green-600'}`}>
                              {endpoint.errorRate}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                endpoint.errorRate < 0.5 ? 'bg-green-600' :
                                endpoint.errorRate < 2 ? 'bg-yellow-600' :
                                'bg-red-600'
                              }`}
                              style={{ width: `${Math.min(endpoint.errorRate * 10, 100)}%` }}
                            ></div>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Endpoint Detail Modal */}
        {selectedEndpoint && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Endpoint Details
                </h3>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Method</h4>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getMethodColor(selectedEndpoint.method)}`}>
                        {selectedEndpoint.method}
                      </span>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Status</h4>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getEndpointStatusColor(selectedEndpoint.status)}`}>
                        {selectedEndpoint.status}
                      </span>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Path</h4>
                    <p className="text-sm text-gray-900 font-mono">{selectedEndpoint.path}</p>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Description</h4>
                    <p className="text-sm text-gray-900">{selectedEndpoint.description}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Version</h4>
                      <p className="text-sm text-gray-900">{selectedEndpoint.version}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Rate Limit</h4>
                      <p className="text-sm text-gray-900">{selectedEndpoint.rateLimit}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Usage Count</h4>
                      <p className="text-sm text-gray-900">{selectedEndpoint.usageCount.toLocaleString()}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Last Used</h4>
                      <p className="text-sm text-gray-900">{new Date(selectedEndpoint.lastUsed).toLocaleString()}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Avg Response Time</h4>
                      <p className="text-sm text-gray-900">{selectedEndpoint.avgResponseTime}ms</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Error Rate</h4>
                      <p className="text-sm text-gray-900">{selectedEndpoint.errorRate}%</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Authentication</h4>
                      <p className="text-sm text-gray-900">{selectedEndpoint.authentication ? 'Required' : 'Not Required'}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Documentation</h4>
                      <a href={selectedEndpoint.documentation} className="text-sm text-op-blue hover:text-blue-700">
                        View Docs →
                      </a>
                    </div>
                  </div>
                </div>
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setSelectedEndpoint(null)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
