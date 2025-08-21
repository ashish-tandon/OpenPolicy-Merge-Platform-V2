import { useState, useEffect } from 'react';
import {
  PlayIcon,
  PauseIcon,
  ArrowPathIcon,
  ExclamationTriangleIcon,
  ServerIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

interface ETLJob {
  id: string;
  name: string;
  status: 'running' | 'completed' | 'failed' | 'scheduled' | 'paused';
  lastRun: string;
  nextRun: string;
  duration: number;
  recordsProcessed: number;
  errors: number;
  dataSource: string;
  priority: 'high' | 'medium' | 'low';
}

interface DataSource {
  name: string;
  status: 'active' | 'inactive' | 'error';
  lastUpdate: string;
  recordCount: number;
  health: 'good' | 'warning' | 'critical';
  lastError?: string;
  retryCount: number;
  maxRetries: number;
}

interface PipelineMetrics {
  totalJobs: number;
  runningJobs: number;
  completedJobs: number;
  failedJobs: number;
  totalRecordsProcessed: number;
  averageProcessingTime: number;
  dataQualityScore: number;
}

export default function ETLManagement() {
  const [jobs, setJobs] = useState<ETLJob[]>([]);
  const [dataSources, setDataSources] = useState<DataSource[]>([]);
  const [metrics, setMetrics] = useState<PipelineMetrics>({
    totalJobs: 0,
    runningJobs: 0,
    completedJobs: 0,
    failedJobs: 0,
    totalRecordsProcessed: 0,
    averageProcessingTime: 0,
    dataQualityScore: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchETLData();
    // Set up polling for real-time updates
    const interval = setInterval(fetchETLData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchETLData = async () => {
    try {
      // Mock data for now - replace with actual API calls
      const mockJobs: ETLJob[] = [
        {
          id: '1',
          name: 'Federal Parliament Scraper',
          status: 'running',
          lastRun: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 45).toISOString(),
          duration: 1200,
          recordsProcessed: 1250,
          errors: 0,
          dataSource: 'Federal Parliament',
          priority: 'high'
        },
        {
          id: '2',
          name: 'Ontario Legislature Scraper',
          status: 'completed',
          lastRun: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 30).toISOString(),
          duration: 900,
          recordsProcessed: 890,
          errors: 2,
          dataSource: 'Ontario Legislature',
          priority: 'medium'
        },
        {
          id: '3',
          name: 'Toronto City Council Scraper',
          status: 'failed',
          lastRun: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 15).toISOString(),
          duration: 0,
          recordsProcessed: 0,
          errors: 15,
          dataSource: 'Toronto City Council',
          priority: 'high'
        },
        {
          id: '4',
          name: 'Vancouver City Council Scraper',
          status: 'paused',
          lastRun: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 60).toISOString(),
          duration: 0,
          recordsProcessed: 0,
          errors: 0,
          dataSource: 'Vancouver City Council',
          priority: 'low'
        }
      ];

      const mockDataSources: DataSource[] = [
        {
          name: 'Federal Parliament',
          status: 'active',
          lastUpdate: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          recordCount: 1250,
          health: 'good',
          retryCount: 0,
          maxRetries: 3
        },
        {
          name: 'Ontario Legislature',
          status: 'active',
          lastUpdate: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          recordCount: 890,
          health: 'warning',
          lastError: 'Connection timeout',
          retryCount: 1,
          maxRetries: 3
        },
        {
          name: 'Toronto City Council',
          status: 'error',
          lastUpdate: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
          recordCount: 456,
          health: 'critical',
          lastError: 'Authentication failed',
          retryCount: 3,
          maxRetries: 3
        },
        {
          name: 'Vancouver City Council',
          status: 'inactive',
          lastUpdate: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          recordCount: 234,
          health: 'critical',
          lastError: 'Service unavailable',
          retryCount: 5,
          maxRetries: 3
        }
      ];

      setJobs(mockJobs);
      setDataSources(mockDataSources);
      setMetrics({
        totalJobs: mockJobs.length,
        runningJobs: mockJobs.filter(j => j.status === 'running').length,
        completedJobs: mockJobs.filter(j => j.status === 'completed').length,
        failedJobs: mockJobs.filter(j => j.status === 'failed').length,
        totalRecordsProcessed: mockJobs.reduce((sum, j) => sum + j.recordsProcessed, 0),
        averageProcessingTime: mockJobs.reduce((sum, j) => sum + j.duration, 0) / mockJobs.length,
        dataQualityScore: 94
      });

    } catch (error) {
      console.error('Failed to fetch ETL data:', error);
    } finally {
      setLoading(false);
    }
  };

  const startJob = async (jobId: string) => {
    try {
      // Mock API call
      console.log('Starting job:', jobId);
      // Update local state
      setJobs(prev => prev.map(job => 
        job.id === jobId ? { ...job, status: 'running' as const } : job
      ));
    } catch (error) {
      console.error('Failed to start job:', error);
    }
  };

  const pauseJob = async (jobId: string) => {
    try {
      // Mock API call
      console.log('Pausing job:', jobId);
      // Update local state
      setJobs(prev => prev.map(job => 
        job.id === jobId ? { ...job, status: 'paused' as const } : job
      ));
    } catch (error) {
      console.error('Failed to pause job:', error);
    }
  };

  const retryJob = async (jobId: string) => {
    try {
      // Mock API call
      console.log('Retrying job:', jobId);
      // Update local state
      setJobs(prev => prev.map(job => 
        job.id === jobId ? { ...job, status: 'scheduled' as const, errors: 0 } : job
      ));
    } catch (error) {
      console.error('Failed to retry job:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'scheduled': return 'bg-yellow-100 text-yellow-800';
      case 'paused': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'good': return 'text-green-600 bg-green-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'critical': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
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
          <h1 className="text-3xl font-bold text-gray-900">ETL & Data Pipeline Management</h1>
          <p className="mt-2 text-gray-600">
            Monitor and control data extraction, transformation, and loading processes
          </p>
        </div>

        {/* Pipeline Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <ServerIcon className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Jobs</p>
                <p className="text-2xl font-semibold text-gray-900">{metrics.totalJobs}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <PlayIcon className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Running</p>
                <p className="text-2xl font-semibold text-gray-900">{metrics.runningJobs}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Failed</p>
                <p className="text-2xl font-semibold text-gray-900">{metrics.failedJobs}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <ChartBarIcon className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Data Quality</p>
                <p className="text-2xl font-semibold text-gray-900">{metrics.dataQualityScore}%</p>
              </div>
            </div>
          </div>
        </div>

        {/* ETL Jobs */}
        <div className="bg-white shadow rounded-lg mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">ETL Jobs</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Job Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Data Source
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Priority
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Run
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Records
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {jobs.map((job) => (
                  <tr key={job.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{job.name}</div>
                        <div className="text-sm text-gray-500">ID: {job.id}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(job.status)}`}>
                        {job.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {job.dataSource}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(job.priority)}`}>
                        {job.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(job.lastRun).toLocaleTimeString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {job.recordsProcessed.toLocaleString()}
                      {job.errors > 0 && (
                        <span className="ml-2 text-red-600">({job.errors} errors)</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        {job.status === 'running' ? (
                          <button
                            onClick={() => pauseJob(job.id)}
                            className="text-yellow-600 hover:text-yellow-900"
                            title="Pause Job"
                          >
                            <PauseIcon className="h-4 w-4" />
                          </button>
                        ) : (
                          <button
                            onClick={() => startJob(job.id)}
                            className="text-green-600 hover:text-green-900"
                            title="Start Job"
                          >
                            <PlayIcon className="h-4 w-4" />
                          </button>
                        )}
                        {job.status === 'failed' && (
                          <button
                            onClick={() => retryJob(job.id)}
                            className="text-blue-600 hover:text-blue-900"
                            title="Retry Job"
                          >
                            <ArrowPathIcon className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Data Sources Status */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Data Sources Status</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {dataSources.map((source) => (
                <div key={source.name} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="text-lg font-medium text-gray-900">{source.name}</h4>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getHealthColor(source.health)}`}>
                      {source.health}
                    </span>
                  </div>
                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex justify-between">
                      <span>Status:</span>
                      <span className={`font-medium ${
                        source.status === 'active' ? 'text-green-600' :
                        source.status === 'inactive' ? 'text-gray-600' :
                        'text-red-600'
                      }`}>
                        {source.status}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Records:</span>
                      <span className="font-medium">{source.recordCount.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Last Update:</span>
                      <span className="font-medium">{new Date(source.lastUpdate).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Retry Count:</span>
                      <span className={`font-medium ${
                        source.retryCount >= source.maxRetries ? 'text-red-600' :
                        source.retryCount > 0 ? 'text-yellow-600' :
                        'text-green-600'
                      }`}>
                        {source.retryCount}/{source.maxRetries}
                      </span>
                    </div>
                    {source.lastError && (
                      <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
                        <strong>Last Error:</strong> {source.lastError}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
