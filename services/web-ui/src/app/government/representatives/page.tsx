'use client';

import { useState, useEffect } from 'react';
import { PaginatedResponse, Representative, GovernmentLevel, RepresentativeFilters } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';
import { RepresentativeIcon } from '@/components/Government/GovernmentIcons';

export default function AllRepresentativesPage() {
  const [representatives, setRepresentatives] = useState<PaginatedResponse<Representative> | null>(null);
  const [governmentLevels, setGovernmentLevels] = useState<GovernmentLevel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<RepresentativeFilters>({
    page: 1,
    page_size: 20
  });

  const fetchRepresentatives = async (currentFilters: RepresentativeFilters) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      Object.entries(currentFilters).forEach(([key, value]) => {
        if (value !== undefined && value !== '') {
          params.append(key, value.toString());
        }
      });

      const response = await fetch(`/api/v1/multi-level-government/representatives?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch representatives');
      }

      const data = await response.json();
      setRepresentatives(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load representatives');
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
    fetchRepresentatives(filters);
  }, [filters]);

  const handleFilterChange = (key: keyof RepresentativeFilters, value: string | number | undefined) => {
    setFilters(prev => ({
      ...prev,
      [key]: value === '' ? undefined : value,
      page: key !== 'page' ? 1 : value // Reset to page 1 when changing other filters
    }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  const getPositionLabel = (position: string) => {
    const labels: Record<string, string> = {
      'mp': 'Member of Parliament',
      'mla': 'Member of Legislative Assembly',
      'mpp': 'Member of Provincial Parliament',
      'mayor': 'Mayor',
      'councillor': 'Councillor',
      'deputy_mayor': 'Deputy Mayor',
      'chair': 'Chair',
      'deputy_chair': 'Deputy Chair'
    };
    return labels[position] || position.toUpperCase();
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

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="content-container py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Representatives</h2>
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
            <RepresentativeIcon className="w-16 h-16 text-blue-100" />
            <div>
              <h1 className="text-4xl font-bold mb-2">All Representatives</h1>
              <p className="text-xl text-blue-100">
                Elected officials across all levels of Canadian government
              </p>
              {representatives && (
                <p className="text-blue-200 mt-2">
                  {representatives.pagination.total.toLocaleString()} total representatives
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="content-container py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filter Representatives</h2>
          <div className="grid md:grid-cols-4 gap-4">
            {/* Search */}
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                Search by name
              </label>
              <input
                type="text"
                id="search"
                value={filters.q || ''}
                onChange={(e) => handleFilterChange('q', e.target.value)}
                placeholder="Enter representative name..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              />
            </div>

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

            {/* Province */}
            <div>
              <label htmlFor="province" className="block text-sm font-medium text-gray-700 mb-1">
                Province/Territory
              </label>
              <input
                type="text"
                id="province"
                value={filters.province || ''}
                onChange={(e) => handleFilterChange('province', e.target.value)}
                placeholder="e.g., Ontario, Quebec"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              />
            </div>

            {/* Political Party */}
            <div>
              <label htmlFor="party" className="block text-sm font-medium text-gray-700 mb-1">
                Political Party
              </label>
              <input
                type="text"
                id="party"
                value={filters.party || ''}
                onChange={(e) => handleFilterChange('party', e.target.value)}
                placeholder="e.g., Liberal, Conservative"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              />
            </div>
          </div>

          {/* Clear Filters */}
          <div className="flex justify-end mt-4">
            <button
              onClick={() => setFilters({ page: 1, page_size: 20 })}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {/* Representatives List */}
        <div className="bg-white rounded-lg shadow-sm">
          {loading ? (
            <div className="p-12">
              <LoadingSpinner />
            </div>
          ) : representatives && representatives.items.length > 0 ? (
            <>
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Representatives ({representatives.pagination.total.toLocaleString()})
                  </h2>
                  <div className="text-sm text-gray-500">
                    Page {representatives.pagination.page} of {representatives.pagination.total_pages}
                  </div>
                </div>

                <div className="space-y-4">
                  {representatives.items.map((rep) => (
                    <div
                      key={rep.id}
                      className="border border-gray-200 rounded-lg p-4 hover:border-op-blue transition-colors"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-4">
                          <div className="w-12 h-12 bg-op-blue bg-opacity-10 rounded-full flex items-center justify-center">
                            <span className="text-op-blue font-medium">
                              {rep.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                            </span>
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <h3 className="font-semibold text-gray-900">{rep.name}</h3>
                              <span className={`px-2 py-1 rounded text-xs font-medium ${getGovernmentLevelColor(rep.jurisdiction.government_level.name)}`}>
                                {rep.jurisdiction.government_level.name}
                              </span>
                            </div>
                            <p className="text-gray-600 mb-1">
                              {getPositionLabel(rep.position)} • {rep.party || 'Independent'}
                            </p>
                            <p className="text-gray-500 text-sm mb-2">
                              {rep.riding && `${rep.riding} • `}
                              {rep.jurisdiction.name}
                              {rep.jurisdiction.province && ` • ${rep.jurisdiction.province}`}
                            </p>
                            <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                              {rep.email && (
                                <a
                                  href={`mailto:${rep.email}`}
                                  className="flex items-center space-x-1 hover:text-op-blue"
                                >
                                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                  </svg>
                                  <span>{rep.email}</span>
                                </a>
                              )}
                              {rep.phone && (
                                <a
                                  href={`tel:${rep.phone}`}
                                  className="flex items-center space-x-1 hover:text-op-blue"
                                >
                                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                  </svg>
                                  <span>{rep.phone}</span>
                                </a>
                              )}
                              {rep.website && (
                                <a
                                  href={rep.website}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="flex items-center space-x-1 hover:text-op-blue"
                                >
                                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                  </svg>
                                  <span>Website</span>
                                </a>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Pagination */}
              <div className="border-t border-gray-200 px-6 py-4">
                <Pagination
                  currentPage={representatives.pagination.page}
                  totalPages={representatives.pagination.total_pages}
                  onPageChange={handlePageChange}
                  showInfo={{
                    start: (representatives.pagination.page - 1) * representatives.pagination.page_size + 1,
                    end: Math.min(
                      representatives.pagination.page * representatives.pagination.page_size,
                      representatives.pagination.total
                    ),
                    total: representatives.pagination.total
                  }}
                />
              </div>
            </>
          ) : (
            <div className="p-12 text-center">
              <RepresentativeIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No representatives found</h3>
              <p className="text-gray-500">
                Try adjusting your filters to see more results.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
