'use client';

import { useState, useEffect } from 'react';
import { PaginatedResponse, Bill, GovernmentLevel, BillFilters } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';
import { BillIcon } from '@/components/Government/GovernmentIcons';

export default function AllBillsPage() {
  const [bills, setBills] = useState<PaginatedResponse<Bill> | null>(null);
  const [governmentLevels, setGovernmentLevels] = useState<GovernmentLevel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<BillFilters>({
    page: 1,
    page_size: 20
  });

  const fetchBills = async (currentFilters: BillFilters) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      Object.entries(currentFilters).forEach(([key, value]) => {
        if (value !== undefined && value !== '') {
          params.append(key, value.toString());
        }
      });

      const response = await fetch(`/api/v1/multi-level-government/bills?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch bills');
      }

      const data = await response.json();
      setBills(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load bills');
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
    fetchBills(filters);
  }, [filters]);

  const handleFilterChange = (key: keyof BillFilters, value: string | number | undefined) => {
    setFilters(prev => ({
      ...prev,
      [key]: value === '' ? undefined : value,
      page: key !== 'page' ? 1 : value // Reset to page 1 when changing other filters
    }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      'introduced': 'bg-blue-100 text-blue-800',
      'first_reading': 'bg-yellow-100 text-yellow-800',
      'second_reading': 'bg-orange-100 text-orange-800',
      'third_reading': 'bg-purple-100 text-purple-800',
      'committee': 'bg-indigo-100 text-indigo-800',
      'royal_assent': 'bg-green-100 text-green-800',
      'enacted': 'bg-green-200 text-green-900',
      'defeated': 'bg-red-100 text-red-800',
      'withdrawn': 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      'introduced': 'Introduced',
      'first_reading': 'First Reading',
      'second_reading': 'Second Reading',
      'third_reading': 'Third Reading',
      'committee': 'In Committee',
      'royal_assent': 'Royal Assent',
      'enacted': 'Enacted',
      'defeated': 'Defeated',
      'withdrawn': 'Withdrawn'
    };
    return labels[status] || status.charAt(0).toUpperCase() + status.slice(1);
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
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Bills</h2>
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
            <BillIcon className="w-16 h-16 text-blue-100" />
            <div>
              <h1 className="text-4xl font-bold mb-2">All Bills & Legislation</h1>
              <p className="text-xl text-blue-100">
                Legislation across all levels of Canadian government
              </p>
              {bills && (
                <p className="text-blue-200 mt-2">
                  {bills.pagination.total.toLocaleString()} total bills
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="content-container py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filter Bills</h2>
          <div className="grid md:grid-cols-4 gap-4">
            {/* Search */}
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                Search by title
              </label>
              <input
                type="text"
                id="search"
                value={filters.q || ''}
                onChange={(e) => handleFilterChange('q', e.target.value)}
                placeholder="Enter bill title or keywords..."
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

            {/* Status */}
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                Bill Status
              </label>
              <select
                id="status"
                value={filters.status || ''}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              >
                <option value="">All statuses</option>
                <option value="introduced">Introduced</option>
                <option value="first_reading">First Reading</option>
                <option value="second_reading">Second Reading</option>
                <option value="third_reading">Third Reading</option>
                <option value="committee">In Committee</option>
                <option value="royal_assent">Royal Assent</option>
                <option value="enacted">Enacted</option>
                <option value="defeated">Defeated</option>
                <option value="withdrawn">Withdrawn</option>
              </select>
            </div>

            {/* Date Range */}
            <div>
              <label htmlFor="introduced_after" className="block text-sm font-medium text-gray-700 mb-1">
                Introduced After
              </label>
              <input
                type="date"
                id="introduced_after"
                value={filters.introduced_after || ''}
                onChange={(e) => handleFilterChange('introduced_after', e.target.value)}
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

        {/* Bills List */}
        <div className="bg-white rounded-lg shadow-sm">
          {loading ? (
            <div className="p-12">
              <LoadingSpinner />
            </div>
          ) : bills && bills.items.length > 0 ? (
            <>
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Bills ({bills.pagination.total.toLocaleString()})
                  </h2>
                  <div className="text-sm text-gray-500">
                    Page {bills.pagination.page} of {bills.pagination.total_pages}
                  </div>
                </div>

                <div className="space-y-6">
                  {bills.items.map((bill) => (
                    <div
                      key={bill.id}
                      className="border border-gray-200 rounded-lg p-6 hover:border-op-blue transition-colors"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <span className="bg-op-blue text-white px-3 py-1 rounded text-sm font-medium">
                            {bill.bill_number}
                          </span>
                          <span className={`px-2 py-1 rounded text-sm font-medium ${getStatusColor(bill.status)}`}>
                            {getStatusLabel(bill.status)}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getGovernmentLevelColor(bill.jurisdiction.government_level.name)}`}>
                            {bill.jurisdiction.government_level.name}
                          </span>
                        </div>
                        {bill.introduced_date && (
                          <div className="text-sm text-gray-500">
                            Introduced: {new Date(bill.introduced_date).toLocaleDateString()}
                          </div>
                        )}
                      </div>

                      <h3 className="text-lg font-semibold text-gray-900 mb-3 line-clamp-2">
                        {bill.title}
                      </h3>

                      {bill.summary && (
                        <p className="text-gray-600 mb-4 line-clamp-3">
                          {bill.summary}
                        </p>
                      )}

                      <div className="flex items-center justify-between text-sm text-gray-500">
                        <div className="flex items-center space-x-4">
                          <span>
                            📍 {bill.jurisdiction.name}
                            {bill.jurisdiction.province && ` • ${bill.jurisdiction.province}`}
                          </span>
                          {bill.sponsor && (
                            <span>
                              👤 Sponsored by {bill.sponsor.name}
                            </span>
                          )}
                        </div>
                        <div className="flex space-x-2">
                          <button className="text-op-blue hover:text-blue-700 font-medium">
                            View Details
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Pagination */}
              <div className="border-t border-gray-200 px-6 py-4">
                <Pagination
                  currentPage={bills.pagination.page}
                  totalPages={bills.pagination.total_pages}
                  onPageChange={handlePageChange}
                  showInfo={{
                    start: (bills.pagination.page - 1) * bills.pagination.page_size + 1,
                    end: Math.min(
                      bills.pagination.page * bills.pagination.page_size,
                      bills.pagination.total
                    ),
                    total: bills.pagination.total
                  }}
                />
              </div>
            </>
          ) : (
            <div className="p-12 text-center">
              <BillIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No bills found</h3>
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
