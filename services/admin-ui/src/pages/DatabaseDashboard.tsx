import { useState, useEffect } from 'react';
import {
  ChartBarIcon,
  ServerIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  EyeIcon
} from '@heroicons/react/24/outline';

interface DatabaseSchema {
  name: string;
  description: string;
  tableCount: number;
  totalSize: string;
  lastUpdated: string;
  health: 'healthy' | 'warning' | 'critical';
  tables: DatabaseTable[];
}

interface DatabaseTable {
  name: string;
  schema: string;
  rowCount: number;
  size: string;
  lastModified: string;
  indexes: number;
  constraints: number;
  health: 'healthy' | 'warning' | 'critical';
  growthRate: number; // percentage
  lastVacuum: string;
  fragmentation: number; // percentage
}

interface DatabaseMetrics {
  totalSchemas: number;
  totalTables: number;
  totalRows: number;
  totalSize: string;
  activeConnections: number;
  maxConnections: number;
  cacheHitRatio: number;
  queryPerformance: number;
  uptime: string;
  version: string;
}

export default function DatabaseDashboard() {
  const [schemas, setSchemas] = useState<DatabaseSchema[]>([]);
  const [metrics, setMetrics] = useState<DatabaseMetrics>({
    totalSchemas: 0,
    totalTables: 0,
    totalRows: 0,
    totalSize: '0 MB',
    activeConnections: 0,
    maxConnections: 0,
    cacheHitRatio: 0,
    queryPerformance: 0,
    uptime: '0 days',
    version: 'Unknown'
  });
  const [selectedSchema, setSelectedSchema] = useState<DatabaseSchema | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'schemas' | 'tables' | 'performance'>('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDatabaseData();
    const interval = setInterval(fetchDatabaseData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  const fetchDatabaseData = async () => {
    try {
      // Mock data - replace with actual API calls
      const mockSchemas: DatabaseSchema[] = [
        {
          name: 'multi_level_government',
          description: 'Multi-level government data including federal, provincial, and municipal entities',
          tableCount: 8,
          totalSize: '2.4 GB',
          lastUpdated: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          health: 'healthy',
          tables: [
            {
              name: 'government_levels',
              schema: 'multi_level_government',
              rowCount: 3,
              size: '12 KB',
              lastModified: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
              indexes: 2,
              constraints: 3,
              health: 'healthy',
              growthRate: 0,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
              fragmentation: 2
            },
            {
              name: 'jurisdictions',
              schema: 'multi_level_government',
              rowCount: 156,
              size: '45 MB',
              lastModified: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
              indexes: 4,
              constraints: 5,
              health: 'healthy',
              growthRate: 5.2,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
              fragmentation: 8
            },
            {
              name: 'representatives',
              schema: 'multi_level_government',
              rowCount: 2847,
              size: '156 MB',
              lastModified: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
              indexes: 6,
              constraints: 8,
              health: 'healthy',
              growthRate: 12.8,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
              fragmentation: 15
            },
            {
              name: 'bills',
              schema: 'multi_level_government',
              rowCount: 12543,
              size: '890 MB',
              lastModified: new Date(Date.now() - 1000 * 60 * 20).toISOString(),
              indexes: 8,
              constraints: 12,
              health: 'warning',
              growthRate: 25.6,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
              fragmentation: 22
            },
            {
              name: 'votes',
              schema: 'multi_level_government',
              rowCount: 45678,
              size: '1.2 GB',
              lastModified: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
              indexes: 5,
              constraints: 7,
              health: 'healthy',
              growthRate: 18.4,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
              fragmentation: 12
            }
          ]
        },
        {
          name: 'openparliament',
          description: 'Open Parliament data including debates, sessions, and parliamentary activities',
          tableCount: 12,
          totalSize: '3.8 GB',
          lastUpdated: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
          health: 'healthy',
          tables: [
            {
              name: 'debates',
              schema: 'openparliament',
              rowCount: 23456,
              size: '1.5 GB',
              lastModified: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
              indexes: 7,
              constraints: 10,
              health: 'healthy',
              growthRate: 22.3,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(),
              fragmentation: 18
            },
            {
              name: 'sessions',
              schema: 'openparliament',
              rowCount: 1234,
              size: '45 MB',
              lastModified: new Date(Date.now() - 1000 * 60 * 40).toISOString(),
              indexes: 3,
              constraints: 4,
              health: 'healthy',
              growthRate: 3.1,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
              fragmentation: 5
            }
          ]
        },
        {
          name: 'represent_canada',
          description: 'Represent Canada data including electoral districts and candidate information',
          tableCount: 6,
          totalSize: '890 MB',
          lastUpdated: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
          health: 'warning',
          tables: [
            {
              name: 'electoral_districts',
              schema: 'represent_canada',
              rowCount: 338,
              size: '23 MB',
              lastModified: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
              indexes: 3,
              constraints: 4,
              health: 'warning',
              growthRate: 0.5,
              lastVacuum: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
              fragmentation: 28
            }
          ]
        }
      ];

      setSchemas(mockSchemas);
      setMetrics({
        totalSchemas: mockSchemas.length,
        totalTables: mockSchemas.reduce((sum, schema) => sum + schema.tableCount, 0),
        totalRows: mockSchemas.reduce((sum, schema) => sum + schema.tables.reduce((tSum, table) => tSum + table.rowCount, 0), 0),
        totalSize: '7.1 GB',
        activeConnections: 24,
        maxConnections: 100,
        cacheHitRatio: 94.2,
        queryPerformance: 87.6,
        uptime: '45 days',
        version: 'PostgreSQL 15.3'
      });
    } catch (error) {
      console.error('Failed to fetch database data:', error);
    } finally {
      setLoading(false);
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

  const getHealthIcon = (health: string) => {
    switch (health) {
      case 'healthy': return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'warning': return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
      case 'critical': return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      default: return <ExclamationTriangleIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const formatBytes = (bytes: string) => {
    return bytes; // Already formatted in mock data
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
          <h1 className="text-3xl font-bold text-gray-900">Database Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Monitor database health, performance, and schema statistics across all data sources
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: ChartBarIcon },
              { id: 'schemas', name: 'Schemas', icon: ServerIcon },
              { id: 'tables', name: 'Tables', icon: ChartBarIcon },
              { id: 'performance', name: 'Performance', icon: ServerIcon }
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
            {/* Database Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <ServerIcon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Schemas</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.totalSchemas}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <ChartBarIcon className="h-6 w-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Tables</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.totalTables}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <ChartBarIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Rows</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.totalRows.toLocaleString()}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <ServerIcon className="h-6 w-6 text-orange-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Size</p>
                    <p className="text-2xl font-semibold text-gray-900">{metrics.totalSize}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Database Health & Performance */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">Database Health</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Version</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.version}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Uptime</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.uptime}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Active Connections</span>
                      <span className="text-sm font-medium text-gray-900">
                        {metrics.activeConnections}/{metrics.maxConnections}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Cache Hit Ratio</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.cacheHitRatio}%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Query Performance</span>
                      <span className="text-sm font-medium text-gray-900">{metrics.queryPerformance}%</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">Schema Health Overview</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-3">
                    {schemas.map((schema) => (
                      <div key={schema.name} className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          {getHealthIcon(schema.health)}
                          <span className="text-sm font-medium text-gray-900">{schema.name}</span>
                        </div>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getHealthColor(schema.health)}`}>
                          {schema.health}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Schemas Tab */}
        {activeTab === 'schemas' && (
          <div className="space-y-6">
            {schemas.map((schema) => (
              <div key={schema.name} className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">{schema.name}</h3>
                      <p className="text-sm text-gray-600">{schema.description}</p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getHealthColor(schema.health)}`}>
                        {schema.health}
                      </span>
                      <button
                        onClick={() => setSelectedSchema(schema)}
                        className="text-op-blue hover:text-blue-700"
                      >
                        <EyeIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-sm font-medium text-gray-500">Tables</p>
                      <p className="text-lg font-semibold text-gray-900">{schema.tableCount}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">Total Size</p>
                      <p className="text-lg font-semibold text-gray-900">{schema.totalSize}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">Last Updated</p>
                      <p className="text-sm text-gray-900">{new Date(schema.lastUpdated).toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-500">Health</p>
                      <div className="flex items-center space-x-2">
                        {getHealthIcon(schema.health)}
                        <span className={`text-sm font-medium ${getHealthColor(schema.health).split(' ')[1]}`}>
                          {schema.health}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tables Tab */}
        {activeTab === 'tables' && (
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">All Database Tables</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Table Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Schema
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rows
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Size
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Growth Rate
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Health
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Modified
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {schemas.flatMap(schema => 
                    schema.tables.map(table => (
                      <tr key={`${schema.name}.${table.name}`} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">{table.name}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{schema.name}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {table.rowCount.toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{table.size}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          <div className="flex items-center">
                            {table.growthRate > 0 ? (
                              <ChartBarIcon className="h-4 w-4 text-green-500 mr-1" />
                            ) : (
                              <ServerIcon className="h-4 w-4 text-red-500 mr-1" />
                            )}
                            {Math.abs(table.growthRate)}%
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getHealthColor(table.health)}`}>
                            {table.health}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {new Date(table.lastModified).toLocaleString()}
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
                  <h3 className="text-lg font-medium text-gray-900">Table Performance Metrics</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    {schemas.flatMap(schema => 
                      schema.tables.map(table => (
                        <div key={`${schema.name}.${table.name}`} className="border-b border-gray-100 pb-3 last:border-b-0">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-900">{table.name}</span>
                            <span className="text-xs text-gray-500">{schema.name}</span>
                          </div>
                          <div className="grid grid-cols-3 gap-4 text-xs">
                            <div>
                              <span className="text-gray-500">Indexes:</span>
                              <span className="ml-1 font-medium">{table.indexes}</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Constraints:</span>
                              <span className="ml-1 font-medium">{table.constraints}</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Fragmentation:</span>
                              <span className="ml-1 font-medium">{table.fragmentation}%</span>
                            </div>
                          </div>
                          <div className="mt-2 text-xs text-gray-500">
                            Last vacuum: {new Date(table.lastVacuum).toLocaleDateString()}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">Database Performance</h3>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Cache Hit Ratio</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-600 h-2 rounded-full" 
                            style={{ width: `${metrics.cacheHitRatio}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-900">{metrics.cacheHitRatio}%</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Query Performance</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${metrics.queryPerformance}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-900">{metrics.queryPerformance}%</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Connection Usage</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-orange-600 h-2 rounded-full" 
                            style={{ width: `${(metrics.activeConnections / metrics.maxConnections) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-900">
                          {metrics.activeConnections}/{metrics.maxConnections}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Schema Detail Modal */}
        {selectedSchema && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Schema: {selectedSchema.name}
                </h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Description</h4>
                    <p className="text-sm text-gray-900">{selectedSchema.description}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Table Count</h4>
                      <p className="text-sm text-gray-900">{selectedSchema.tableCount}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Total Size</h4>
                      <p className="text-sm text-gray-900">{selectedSchema.totalSize}</p>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Tables</h4>
                    <div className="space-y-2">
                      {selectedSchema.tables.map((table) => (
                        <div key={table.name} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                          <span className="text-sm font-medium text-gray-900">{table.name}</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-xs text-gray-500">{table.rowCount.toLocaleString()} rows</span>
                            <span className="text-xs text-gray-500">{table.size}</span>
                            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getHealthColor(table.health)}`}>
                              {table.health}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setSelectedSchema(null)}
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
