'use client';

import { useState, useEffect } from 'react';
import { PaginatedResponse, DataSource, GovernmentLevel, DataSourceFilters } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';

export default function DataSourcesPage() {
  const [dataSources, setDataSources] = useState<PaginatedResponse<DataSource> | null>(null);
  const [governmentLevels, setGovernmentLevels] = useState<GovernmentLevel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<DataSourceFilters>({
    page: 1,
    page_size: 20
  });

  const fetchDataSources = async (currentFilters: DataSourceFilters) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      Object.entries(currentFilters).forEach(([key, value]) => {
        if (value !== undefined && value !== '') {
          params.append(key, value.toString());
        }
      });

      const response = await fetch(`/api/v1/multi-level-government/data-sources?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch data sources');
      }

      const data = await response.json();
      setDataSources(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data sources');
    } finally {
      setLoading(false);
    }
  };

  const fetchGovernmentLevels = async () => {
    try {
      const response = await fetch('/api/v1/multi-level-government/government-levels');
      if (!response.ok) {
        throw new Error('Failed to fetch government levels');
      }
      const data = await response.json();
      setGovernmentLevels(data.items);
    } catch (err) {
      console.error('Failed to fetch government levels:', err);
    }
  };

  useEffect(() => {
    fetchGovernmentLevels();
  }, []);

  useEffect(() => {
    fetchDataSources(filters);
  }, [filters]);

  const handleFilterChange = (key: keyof DataSourceFilters, value: string | number | undefined) => {
    setFilters(prev => ({
      ...prev,
      [key]: key === 'page' ? (typeof value === 'string' ? parseInt(value) : value) : (value === '' ? undefined : value),
      page: key !== 'page' ? 1 : (typeof value === 'string' ? parseInt(value) : value)
    }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  const getSourceTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      'api': 'bg-blue-100 text-blue-800',
      'scraper': 'bg-green-100 text-green-800',
      'csv': 'bg-yellow-100 text-yellow-800',
      'xml': 'bg-purple-100 text-purple-800',
      'json': 'bg-indigo-100 text-indigo-800',
      'legacy': 'bg-gray-100 text-gray-800'
    };
    return colors[type.toLowerCase()] || 'bg-gray-100 text-gray-800';
  };

  const getGovernmentLevelColor = (levelName: string) => {
    switch (levelName.toLowerCase()) {
      case 'federal':
        return 'bg-red-100 text-red-800';
      case 'provincial':
        return 'bg-blue-100 text-blue-800';
      case 'municipal':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatLastUpdated = (dateString: string | null) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Less than 1 hour ago';
    if (diffInHours < 24) return `${diffInHours} hours ago`;
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) return `${diffInDays} days ago`;
    return date.toLocaleDateString();
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="content-container py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Data Sources</h2>
            <p className="text-red-600">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-op-blue to-blue-700 text-white">
        <div className="content-container py-12">
          <div className="flex items-center space-x-6">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-op-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
              </svg>
            </div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Data Sources & Transparency</h1>
              <p className="text-xl text-blue-100">
                Complete transparency on where our government data comes from
              </p>
              {dataSources && (
                <p className="text-blue-200 mt-2">
                  {dataSources.pagination.total.toLocaleString()} data sources tracked
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="content-container py-8">
        {/* Overview Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6 text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Real-time APIs</h3>
            <p className="text-sm text-gray-600">Direct government feeds</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Verified Sources</h3>
            <p className="text-sm text-gray-600">Official government sites</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 text-center">
            <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Regular Updates</h3>
            <p className="text-sm text-gray-600">Scheduled data refresh</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">Data Quality</h3>
            <p className="text-sm text-gray-600">Validation & monitoring</p>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filter Data Sources</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {/* Government Level */}
            <div>
              <label htmlFor="government_level" className="block text-sm font-medium text-gray-700 mb-1">
                Government Level
              </label>
              <select
                id="government_level"
                value={filters.government_level || ''}
                onChange={(e) => handleFilterChange('government_level', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              >
                <option value="">All levels</option>
                {governmentLevels.map((level) => (
                  <option key={level.id} value={level.id}>
                    {level.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Source Type */}
            <div>
              <label htmlFor="source_type" className="block text-sm font-medium text-gray-700 mb-1">
                Source Type
              </label>
              <select
                id="source_type"
                value={filters.source_type || ''}
                onChange={(e) => handleFilterChange('source_type', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              >
                <option value="">All types</option>
                <option value="api">API</option>
                <option value="scraper">Web Scraper</option>
                <option value="csv">CSV Feed</option>
                <option value="xml">XML Feed</option>
                <option value="json">JSON Feed</option>
                <option value="legacy">Legacy System</option>
              </select>
            </div>

            {/* Clear Filters */}
            <div className="flex items-end">
              <button
                onClick={() => setFilters({ page: 1, page_size: 20 })}
                className="w-full px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>

        {/* Data Sources List */}
        <div className="bg-white rounded-lg shadow-sm">
          {loading ? (
            <div className="p-12">
              <LoadingSpinner />
            </div>
          ) : dataSources && dataSources.items.length > 0 ? (
            <>
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Data Sources ({dataSources.pagination.total.toLocaleString()})
                  </h2>
                  <div className="text-sm text-gray-500">
                    Page {dataSources.pagination.page} of {dataSources.pagination.total_pages}
                  </div>
                </div>

                <div className="space-y-4">
                  {dataSources.items.map((source) => (
                    <div
                      key={source.id}
                      className="border border-gray-200 rounded-lg p-6 hover:border-op-blue transition-colors"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <h3 className="font-semibold text-gray-900">{source.name}</h3>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getSourceTypeColor(source.source_type)}`}>
                            {source.source_type.toUpperCase()}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getGovernmentLevelColor(source.jurisdiction.government_level.name)}`}>
                            {source.jurisdiction.government_level.name}
                          </span>
                        </div>
                        <div className="text-sm text-gray-500">
                          Last updated: {formatLastUpdated(source.last_updated)}
                        </div>
                      </div>

                      <div className="grid md:grid-cols-2 gap-6">
                        <div>
                          <h4 className="font-medium text-gray-700 mb-2">Jurisdiction Details</h4>
                          <div className="space-y-1 text-sm text-gray-600">
                            <p><span className="font-medium">Name:</span> {source.jurisdiction.name}</p>
                            <p><span className="font-medium">Code:</span> {source.jurisdiction.code}</p>
                            {source.jurisdiction.province && (
                              <p><span className="font-medium">Province:</span> {source.jurisdiction.province}</p>
                            )}
                            <p><span className="font-medium">Type:</span> {source.jurisdiction.jurisdiction_type}</p>
                          </div>
                        </div>

                        <div>
                          <h4 className="font-medium text-gray-700 mb-2">Technical Details</h4>
                          <div className="space-y-1 text-sm text-gray-600">
                            {source.url && (
                              <p>
                                <span className="font-medium">URL:</span>{' '}
                                <a 
                                  href={source.url} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="text-op-blue hover:text-blue-700 underline"
                                >
                                  {source.url}
                                </a>
                              </p>
                            )}
                            {source.legacy_module && (
                              <p><span className="font-medium">Legacy Module:</span> {source.legacy_module}</p>
                            )}
                            {source.legacy_class && (
                              <p><span className="font-medium">Legacy Class:</span> {source.legacy_class}</p>
                            )}
                          </div>
                        </div>
                      </div>

                      {source.extras && Object.keys(source.extras).length > 0 && (
                        <div className="mt-4 pt-4 border-t border-gray-100">
                          <h4 className="font-medium text-gray-700 mb-2">Additional Information</h4>
                          <div className="text-sm text-gray-600">
                            <pre className="whitespace-pre-wrap bg-gray-50 p-2 rounded text-xs">
                              {JSON.stringify(source.extras, null, 2)}
                            </pre>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Pagination */}
              <div className="border-t border-gray-200 px-6 py-4">
                <Pagination
                  currentPage={dataSources.pagination.page}
                  totalPages={dataSources.pagination.total_pages}
                  baseUrl="/government/data-sources"
                  queryParams={filters}
                />
              </div>
            </>
          ) : (
            <div className="p-12 text-center">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No data sources found</h3>
              <p className="text-gray-500">
                Try adjusting your filters to see more results.
              </p>
            </div>
          )}
        </div>

        {/* Methodology Section */}
        <div className="mt-12 bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Data Collection Methodology</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Data Sources Priority</h3>
              <ol className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start space-x-2">
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-medium">1</span>
                  <span>Official government APIs and data feeds</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">2</span>
                  <span>Structured data from official websites</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs font-medium">3</span>
                  <span>Web scraping of public government pages</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs font-medium">4</span>
                  <span>Legacy data integration and migration</span>
                </li>
              </ol>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Quality Assurance</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center space-x-2">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Automated data validation and integrity checks</span>
                </li>
                <li className="flex items-center space-x-2">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Regular monitoring of source availability</span>
                </li>
                <li className="flex items-center space-x-2">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Cross-referencing with multiple sources when possible</span>
                </li>
                <li className="flex items-center space-x-2">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Full audit trail and data provenance tracking</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
