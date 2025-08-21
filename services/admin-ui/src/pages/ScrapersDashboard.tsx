import { useState, useEffect } from 'react';
import {
  PlayIcon,
  PauseIcon,
  ArrowPathIcon,
  ClockIcon,
  ChartBarIcon,
  EyeIcon,
  CogIcon
} from '@heroicons/react/24/outline';

interface Scraper {
  id: string;
  name: string;
  type: 'parliamentary' | 'municipal' | 'provincial' | 'federal' | 'custom';
  status: 'running' | 'idle' | 'error' | 'scheduled' | 'maintenance';
  lastRun: string;
  nextRun: string;
  schedule: string;
  dataPlan: DataPlan;
  ingestionStats: IngestionStats;
  health: 'healthy' | 'warning' | 'critical';
  lastError?: string;
  retryCount: number;
  maxRetries: number;
  priority: 'high' | 'medium' | 'low';
  dataSource: string;
  jurisdiction: string;
}

interface DataPlan {
  id: string;
  name: string;
  description: string;
  entities: string[];
  updateFrequency: string;
  dataRetention: string;
  qualityRules: string[];
  lastValidation: string;
  validationScore: number;
}

interface IngestionStats {
  totalRecords: number;
  newRecords: number;
  updatedRecords: number;
  failedRecords: number;
  lastIngestion: string;
  ingestionDuration: number;
  successRate: number;
}

interface ScraperSchedule {
  id: string;
  scraperId: string;
  cronExpression: string;
  timezone: string;
  isActive: boolean;
  lastTriggered: string;
  nextTrigger: string;
  description: string;
}

export default function ScrapersDashboard() {
  const [scrapers, setScrapers] = useState<Scraper[]>([]);
  const [schedules, setSchedules] = useState<ScraperSchedule[]>([]);
  const [selectedScraper, setSelectedScraper] = useState<Scraper | null>(null);
  const [showDataPlan, setShowDataPlan] = useState(false);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'schedules' | 'data-plans'>('overview');

  useEffect(() => {
    fetchScrapersData();
    const interval = setInterval(fetchScrapersData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchScrapersData = async () => {
    try {
      // Mock data - replace with actual API calls
      const mockScrapers: Scraper[] = [
        {
          id: '1',
          name: 'Federal Parliament Scraper',
          type: 'federal',
          status: 'running',
          lastRun: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 45).toISOString(),
          schedule: 'Every 2 hours',
          dataPlan: {
            id: 'dp1',
            name: 'Federal Parliamentary Data',
            description: 'Comprehensive data collection from House of Commons and Senate',
            entities: ['Bills', 'Debates', 'Votes', 'MPs', 'Committees'],
            updateFrequency: '2 hours',
            dataRetention: '10 years',
            qualityRules: ['Data validation', 'Duplicate detection', 'Source verification'],
            lastValidation: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
            validationScore: 98
          },
          ingestionStats: {
            totalRecords: 125000,
            newRecords: 45,
            updatedRecords: 23,
            failedRecords: 2,
            lastIngestion: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
            ingestionDuration: 1200,
            successRate: 99.8
          },
          health: 'healthy',
          retryCount: 0,
          maxRetries: 3,
          priority: 'high',
          dataSource: 'https://www.ourcommons.ca',
          jurisdiction: 'Federal'
        },
        {
          id: '2',
          name: 'Ontario Legislature Scraper',
          type: 'provincial',
          status: 'idle',
          lastRun: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 30).toISOString(),
          schedule: 'Every 4 hours',
          dataPlan: {
            id: 'dp2',
            name: 'Ontario Legislative Data',
            description: 'Provincial legislative data from Queen\'s Park',
            entities: ['Bills', 'Debates', 'Votes', 'MPPs', 'Committees'],
            updateFrequency: '4 hours',
            dataRetention: '8 years',
            qualityRules: ['Data validation', 'Source verification'],
            lastValidation: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
            validationScore: 95
          },
          ingestionStats: {
            totalRecords: 89000,
            newRecords: 12,
            updatedRecords: 8,
            failedRecords: 1,
            lastIngestion: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
            ingestionDuration: 900,
            successRate: 99.9
          },
          health: 'healthy',
          retryCount: 0,
          maxRetries: 3,
          priority: 'medium',
          dataSource: 'https://www.ola.org',
          jurisdiction: 'Ontario'
        },
        {
          id: '3',
          name: 'Toronto City Council Scraper',
          type: 'municipal',
          status: 'error',
          lastRun: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 15).toISOString(),
          schedule: 'Daily at 6 AM',
          dataPlan: {
            id: 'dp3',
            name: 'Toronto Municipal Data',
            description: 'City council meetings, bylaws, and municipal decisions',
            entities: ['Council Meetings', 'Bylaws', 'Decisions', 'Councillors'],
            updateFrequency: 'Daily',
            dataRetention: '5 years',
            qualityRules: ['Meeting validation', 'Document verification'],
            lastValidation: new Date(Date.now() - 1000 * 60 * 180).toISOString(),
            validationScore: 92
          },
          ingestionStats: {
            totalRecords: 45600,
            newRecords: 0,
            updatedRecords: 0,
            failedRecords: 15,
            lastIngestion: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
            ingestionDuration: 0,
            successRate: 0
          },
          health: 'critical',
          lastError: 'Authentication failed - API key expired',
          retryCount: 3,
          maxRetries: 3,
          priority: 'high',
          dataSource: 'https://www.toronto.ca/city-government',
          jurisdiction: 'Toronto'
        },
        {
          id: '4',
          name: 'Vancouver City Council Scraper',
          type: 'municipal',
          status: 'maintenance',
          lastRun: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          nextRun: new Date(Date.now() + 1000 * 60 * 60).toISOString(),
          schedule: 'Daily at 8 AM',
          dataPlan: {
            id: 'dp4',
            name: 'Vancouver Municipal Data',
            description: 'City council proceedings and municipal governance data',
            entities: ['Council Meetings', 'Bylaws', 'Decisions', 'Councillors'],
            updateFrequency: 'Daily',
            dataRetention: '5 years',
            qualityRules: ['Meeting validation', 'Document verification'],
            lastValidation: new Date(Date.now() - 1000 * 60 * 240).toISOString(),
            validationScore: 88
          },
          ingestionStats: {
            totalRecords: 23400,
            newRecords: 0,
            updatedRecords: 0,
            failedRecords: 0,
            lastIngestion: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
            ingestionDuration: 0,
            successRate: 0
          },
          health: 'warning',
          lastError: 'Service under maintenance',
          retryCount: 0,
          maxRetries: 3,
          priority: 'low',
          dataSource: 'https://vancouver.ca/your-government',
          jurisdiction: 'Vancouver'
        }
      ];

      const mockSchedules: ScraperSchedule[] = [
        {
          id: 's1',
          scraperId: '1',
          cronExpression: '0 */2 * * *',
          timezone: 'America/Toronto',
          isActive: true,
          lastTriggered: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          nextTrigger: new Date(Date.now() + 1000 * 60 * 45).toISOString(),
          description: 'Every 2 hours'
        },
        {
          id: 's2',
          scraperId: '2',
          cronExpression: '0 */4 * * *',
          timezone: 'America/Toronto',
          isActive: true,
          lastTriggered: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          nextTrigger: new Date(Date.now() + 1000 * 60 * 30).toISOString(),
          description: 'Every 4 hours'
        },
        {
          id: 's3',
          scraperId: '3',
          cronExpression: '0 6 * * *',
          timezone: 'America/Toronto',
          isActive: true,
          lastTriggered: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
          nextTrigger: new Date(Date.now() + 1000 * 60 * 15).toISOString(),
          description: 'Daily at 6 AM'
        },
        {
          id: 's4',
          scraperId: '4',
          cronExpression: '0 8 * * *',
          timezone: 'America/Vancouver',
          isActive: false,
          lastTriggered: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          nextTrigger: new Date(Date.now() + 1000 * 60 * 60).toISOString(),
          description: 'Daily at 8 AM (Paused)'
        }
      ];

      setScrapers(mockScrapers);
      setSchedules(mockSchedules);
    } catch (error) {
      console.error('Failed to fetch scrapers data:', error);
    } finally {
      setLoading(false);
    }
  };

  const startScraper = async (scraperId: string) => {
    try {
      console.log('Starting scraper:', scraperId);
      setScrapers(prev => prev.map(scraper => 
        scraper.id === scraperId ? { ...scraper, status: 'running' as const } : scraper
      ));
    } catch (error) {
      console.error('Failed to start scraper:', error);
    }
  };

  const stopScraper = async (scraperId: string) => {
    try {
      console.log('Stopping scraper:', scraperId);
      setScrapers(prev => prev.map(scraper => 
        scraper.id === scraperId ? { ...scraper, status: 'idle' as const } : scraper
      ));
    } catch (error) {
      console.error('Failed to stop scraper:', error);
    }
  };

  const retryScraper = async (scraperId: string) => {
    try {
      console.log('Retrying scraper:', scraperId);
      setScrapers(prev => prev.map(scraper => 
        scraper.id === scraperId ? { ...scraper, status: 'scheduled' as const, retryCount: 0 } : scraper
      ));
    } catch (error) {
      console.error('Failed to retry scraper:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-green-100 text-green-800';
      case 'idle': return 'bg-blue-100 text-blue-800';
      case 'error': return 'bg-red-100 text-red-800';
      case 'scheduled': return 'bg-yellow-100 text-yellow-800';
      case 'maintenance': return 'bg-gray-100 text-gray-800';
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

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'federal': return 'bg-red-100 text-red-800';
      case 'provincial': return 'bg-blue-100 text-blue-800';
      case 'municipal': return 'bg-green-100 text-green-800';
      case 'custom': return 'bg-purple-100 text-purple-800';
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
          <h1 className="text-3xl font-bold text-gray-900">Scrapers Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Monitor and control all data collection scrapers, schedules, and data plans
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: ChartBarIcon },
              { id: 'schedules', name: 'Schedules', icon: ClockIcon },
              { id: 'data-plans', name: 'Data Plans', icon: ChartBarIcon }
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
            {/* Scrapers Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {scrapers.map((scraper) => (
                <div key={scraper.id} className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">{scraper.name}</h3>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTypeColor(scraper.type)}`}>
                          {scraper.type}
                        </span>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(scraper.status)}`}>
                          {scraper.status}
                        </span>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getHealthColor(scraper.health)}`}>
                          {scraper.health}
                        </span>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setSelectedScraper(scraper)}
                        className="p-2 text-gray-400 hover:text-gray-600"
                        title="View Details"
                      >
                        <EyeIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => setShowDataPlan(true)}
                        className="p-2 text-gray-400 hover:text-gray-600"
                        title="View Data Plan"
                      >
                        <ChartBarIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-3 text-sm text-gray-600">
                    <div className="flex justify-between">
                      <span>Jurisdiction:</span>
                      <span className="font-medium">{scraper.jurisdiction}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Last Run:</span>
                      <span className="font-medium">{new Date(scraper.lastRun).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Next Run:</span>
                      <span className="font-medium">{new Date(scraper.nextRun).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Schedule:</span>
                      <span className="font-medium">{scraper.schedule}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Records:</span>
                      <span className="font-medium">{scraper.ingestionStats.totalRecords.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Success Rate:</span>
                      <span className="font-medium">{scraper.ingestionStats.successRate}%</span>
                    </div>
                  </div>

                  {scraper.lastError && (
                    <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
                      <strong>Last Error:</strong> {scraper.lastError}
                    </div>
                  )}

                  <div className="mt-4 flex space-x-2">
                    {scraper.status === 'running' ? (
                      <button
                        onClick={() => stopScraper(scraper.id)}
                        className="flex-1 inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-yellow-600 hover:bg-yellow-700"
                      >
                        <PauseIcon className="h-4 w-4 mr-2" />
                        Stop
                      </button>
                    ) : (
                      <button
                        onClick={() => startScraper(scraper.id)}
                        className="flex-1 inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                      >
                        <PlayIcon className="h-4 w-4 mr-2" />
                        Start
                      </button>
                    )}
                    {scraper.status === 'error' && (
                      <button
                        onClick={() => retryScraper(scraper.id)}
                        className="inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                      >
                        <ArrowPathIcon className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Schedules Tab */}
        {activeTab === 'schedules' && (
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Scraper Schedules</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Scraper
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Schedule
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Timezone
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Triggered
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Next Trigger
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {schedules.map((schedule) => {
                    const scraper = scrapers.find(s => s.id === schedule.scraperId);
                    return (
                      <tr key={schedule.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">
                            {scraper?.name || 'Unknown'}
                          </div>
                          <div className="text-sm text-gray-500">{scraper?.type}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {schedule.description}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {schedule.timezone}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            schedule.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                          }`}>
                            {schedule.isActive ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {new Date(schedule.lastTriggered).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {new Date(schedule.nextTrigger).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-op-blue hover:text-blue-700">
                            <CogIcon className="h-4 w-4" />
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Data Plans Tab */}
        {activeTab === 'data-plans' && (
          <div className="space-y-6">
            {scrapers.map((scraper) => (
              <div key={scraper.id} className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900">{scraper.name} - Data Plan</h3>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500 mb-2">Plan Details</h4>
                      <div className="space-y-2 text-sm">
                        <div><strong>Name:</strong> {scraper.dataPlan.name}</div>
                        <div><strong>Description:</strong> {scraper.dataPlan.description}</div>
                        <div><strong>Update Frequency:</strong> {scraper.dataPlan.updateFrequency}</div>
                        <div><strong>Data Retention:</strong> {scraper.dataPlan.dataRetention}</div>
                        <div><strong>Validation Score:</strong> {scraper.dataPlan.validationScore}%</div>
                      </div>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500 mb-2">Entities Collected</h4>
                      <div className="space-y-1">
                        {scraper.dataPlan.entities.map((entity, index) => (
                          <div key={index} className="inline-block bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded mr-2 mb-2">
                            {entity}
                          </div>
                        ))}
                      </div>
                      <h4 className="text-sm font-medium text-gray-500 mb-2 mt-4">Quality Rules</h4>
                      <div className="space-y-1">
                        {scraper.dataPlan.qualityRules.map((rule, index) => (
                          <div key={index} className="text-sm text-gray-600">• {rule}</div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Data Plan Modal */}
        {showDataPlan && selectedScraper && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Data Plan: {selectedScraper.dataPlan.name}
                </h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Description</h4>
                    <p className="text-sm text-gray-900">{selectedScraper.dataPlan.description}</p>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Entities</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedScraper.dataPlan.entities.map((entity, index) => (
                        <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                          {entity}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Update Frequency</h4>
                      <p className="text-sm text-gray-900">{selectedScraper.dataPlan.updateFrequency}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Data Retention</h4>
                      <p className="text-sm text-gray-900">{selectedScraper.dataPlan.dataRetention}</p>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Quality Rules</h4>
                    <ul className="text-sm text-gray-900 list-disc list-inside">
                      {selectedScraper.dataPlan.qualityRules.map((rule, index) => (
                        <li key={index}>{rule}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500">Validation</h4>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-900">Score: {selectedScraper.dataPlan.validationScore}%</span>
                      <span className="text-xs text-gray-500">
                        Last: {new Date(selectedScraper.dataPlan.lastValidation).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setShowDataPlan(false)}
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
