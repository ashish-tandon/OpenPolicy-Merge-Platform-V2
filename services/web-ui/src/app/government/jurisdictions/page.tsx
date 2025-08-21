'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { PaginatedResponse, Jurisdiction, GovernmentLevel, JurisdictionFilters } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';
import { JurisdictionIcon, FederalIcon, ProvincialIcon, MunicipalIcon } from '@/components/Government/GovernmentIcons';

export default function AllJurisdictionsPage() {
  const [jurisdictions, setJurisdictions] = useState<PaginatedResponse<Jurisdiction> | null>(null);
  const [governmentLevels, setGovernmentLevels] = useState<GovernmentLevel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<JurisdictionFilters>({
    page: 1,
    page_size: 20
  });

  const fetchJurisdictions = async (currentFilters: JurisdictionFilters) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      Object.entries(currentFilters).forEach(([key, value]) => {
        if (value !== undefined && value !== '') {
          params.append(key, value.toString());
        }
      });

      const response = await fetch(`/api/v1/multi-level-government/jurisdictions?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch jurisdictions');
      }

      const data = await response.json();
      setJurisdictions(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load jurisdictions');
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
    fetchJurisdictions(filters);
  }, [filters]);

  const handleFilterChange = (key: keyof JurisdictionFilters, value: string | number | undefined) => {
    setFilters(prev => ({
      ...prev,
      [key]: value === '' ? undefined : value,
      page: key !== 'page' ? 1 : value
    }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  const getGovernmentIcon = (levelName: string) => {
    switch (levelName.toLowerCase()) {
      case 'federal':
        return <FederalIcon className="w-8 h-8" />;
      case 'provincial':
        return <ProvincialIcon className="w-8 h-8" />;
      case 'municipal':
        return <MunicipalIcon className="w-8 h-8" />;
      default:
        return <JurisdictionIcon className="w-8 h-8" />;
    }
  };

  const getGovernmentLevelColor = (levelName: string) => {
    switch (levelName.toLowerCase()) {
      case 'federal':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'provincial':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'municipal':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getJurisdictionTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'legislature': 'Legislature',
      'parliament': 'Parliament',
      'city_council': 'City Council',
      'town_council': 'Town Council',
      'regional_council': 'Regional Council',
      'first_nations': 'First Nations'
    };
    return labels[type] || type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ');
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="content-container py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Jurisdictions</h2>
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
            <JurisdictionIcon className="w-16 h-16 text-blue-100" />
            <div>
              <h1 className="text-4xl font-bold mb-2">All Jurisdictions</h1>
              <p className="text-xl text-blue-100">
                Federal, provincial, and municipal jurisdictions across Canada
              </p>
              {jurisdictions && (
                <p className="text-blue-200 mt-2">
                  {jurisdictions.pagination.total.toLocaleString()} total jurisdictions
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="content-container py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filter Jurisdictions</h2>
          <div className="grid md:grid-cols-4 gap-4">
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
              <select
                id="province"
                value={filters.province || ''}
                onChange={(e) => handleFilterChange('province', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              >
                <option value="">All provinces/territories</option>
                <option value="Alberta">Alberta</option>
                <option value="British Columbia">British Columbia</option>
                <option value="Manitoba">Manitoba</option>
                <option value="New Brunswick">New Brunswick</option>
                <option value="Newfoundland and Labrador">Newfoundland and Labrador</option>
                <option value="Northwest Territories">Northwest Territories</option>
                <option value="Nova Scotia">Nova Scotia</option>
                <option value="Nunavut">Nunavut</option>
                <option value="Ontario">Ontario</option>
                <option value="Prince Edward Island">Prince Edward Island</option>
                <option value="Quebec">Quebec</option>
                <option value="Saskatchewan">Saskatchewan</option>
                <option value="Yukon">Yukon</option>
              </select>
            </div>

            {/* Jurisdiction Type */}
            <div>
              <label htmlFor="jurisdiction_type" className="block text-sm font-medium text-gray-700 mb-1">
                Jurisdiction Type
              </label>
              <select
                id="jurisdiction_type"
                value={filters.jurisdiction_type || ''}
                onChange={(e) => handleFilterChange('jurisdiction_type', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              >
                <option value="">All types</option>
                <option value="parliament">Parliament</option>
                <option value="legislature">Legislature</option>
                <option value="city_council">City Council</option>
                <option value="town_council">Town Council</option>
                <option value="regional_council">Regional Council</option>
                <option value="first_nations">First Nations</option>
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

        {/* Jurisdictions List */}
        <div className="bg-white rounded-lg shadow-sm">
          {loading ? (
            <div className="p-12">
              <LoadingSpinner />
            </div>
          ) : jurisdictions && jurisdictions.items.length > 0 ? (
            <>
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Jurisdictions ({jurisdictions.pagination.total.toLocaleString()})
                  </h2>
                  <div className="text-sm text-gray-500">
                    Page {jurisdictions.pagination.page} of {jurisdictions.pagination.total_pages}
                  </div>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {jurisdictions.items.map((jurisdiction) => (
                    <Link
                      key={jurisdiction.id}
                      href={`/government/jurisdictions/${jurisdiction.id}`}
                      className={`group border-2 rounded-lg p-6 hover:shadow-lg transition-all duration-300 ${getGovernmentLevelColor(jurisdiction.government_level.name)}`}
                    >
                      <div className="flex items-start space-x-4">
                        <div className="text-gray-600 group-hover:text-gray-800 transition-colors">
                          {getGovernmentIcon(jurisdiction.government_level.name)}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <h3 className="font-semibold text-gray-900 group-hover:text-op-blue transition-colors">
                              {jurisdiction.name}
                            </h3>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">
                            {getJurisdictionTypeLabel(jurisdiction.jurisdiction_type)}
                          </p>
                          <div className="space-y-1 text-sm text-gray-500">
                            <p>Level: {jurisdiction.government_level.name}</p>
                            {jurisdiction.province && (
                              <p>Province: {jurisdiction.province}</p>
                            )}
                            <p>Code: {jurisdiction.code}</p>
                          </div>
                          {jurisdiction.website && (
                            <div className="mt-3">
                              <span className="inline-flex items-center text-xs text-op-blue group-hover:text-blue-700">
                                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                                Official Website
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Pagination */}
              <div className="border-t border-gray-200 px-6 py-4">
                <Pagination
                  currentPage={jurisdictions.pagination.page}
                  totalPages={jurisdictions.pagination.total_pages}
                  onPageChange={handlePageChange}
                  showInfo={{
                    start: (jurisdictions.pagination.page - 1) * jurisdictions.pagination.page_size + 1,
                    end: Math.min(
                      jurisdictions.pagination.page * jurisdictions.pagination.page_size,
                      jurisdictions.pagination.total
                    ),
                    total: jurisdictions.pagination.total
                  }}
                />
              </div>
            </>
          ) : (
            <div className="p-12 text-center">
              <JurisdictionIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No jurisdictions found</h3>
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
