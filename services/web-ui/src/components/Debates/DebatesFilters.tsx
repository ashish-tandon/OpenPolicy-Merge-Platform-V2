'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface DebatesFiltersProps {
  currentFilters: {
    date_gte?: string;
    date_lte?: string;
    search?: string;
  };
}

export default function DebatesFilters({ currentFilters }: DebatesFiltersProps) {
  const router = useRouter();
  const [filters, setFilters] = useState({
    dateRange: 'all',
    customStartDate: currentFilters.date_gte || '',
    customEndDate: currentFilters.date_lte || '',
    search: currentFilters.search || '',
  });

  const dateRanges = [
    { value: 'all', label: 'All Time' },
    { value: 'week', label: 'Past Week' },
    { value: 'month', label: 'Past Month' },
    { value: 'year', label: 'Past Year' },
    { value: 'session', label: 'Current Session' },
    { value: 'custom', label: 'Custom Range' },
  ];

  const parliamentarySessions = [
    { value: '45-1', label: '45th Parliament - 1st Session' },
    { value: '44-1', label: '44th Parliament - 1st Session' },
    { value: '43-2', label: '43rd Parliament - 2nd Session' },
    { value: '43-1', label: '43rd Parliament - 1st Session' },
    { value: '42-1', label: '42nd Parliament - 1st Session' },
  ];

  const applyFilters = () => {
    const params = new URLSearchParams();
    
    if (filters.search) params.set('search', filters.search);
    
    // Handle date range
    if (filters.dateRange === 'week') {
      const date = new Date();
      date.setDate(date.getDate() - 7);
      params.set('date_gte', date.toISOString().split('T')[0]);
    } else if (filters.dateRange === 'month') {
      const date = new Date();
      date.setMonth(date.getMonth() - 1);
      params.set('date_gte', date.toISOString().split('T')[0]);
    } else if (filters.dateRange === 'year') {
      const date = new Date();
      date.setFullYear(date.getFullYear() - 1);
      params.set('date_gte', date.toISOString().split('T')[0]);
    } else if (filters.dateRange === 'custom') {
      if (filters.customStartDate) params.set('date_gte', filters.customStartDate);
      if (filters.customEndDate) params.set('date_lte', filters.customEndDate);
    }
    
    const queryString = params.toString();
    router.push(`/debates${queryString ? `?${queryString}` : ''}`);
  };

  const clearFilters = () => {
    setFilters({
      dateRange: 'all',
      customStartDate: '',
      customEndDate: '',
      search: '',
    });
    router.push('/debates');
  };

  const hasActiveFilters = filters.search || filters.dateRange !== 'all';

  // Calculate stats
  const currentYear = new Date().getFullYear();
  const totalYears = currentYear - 1994 + 1;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-bold mb-4">Filter Debates</h2>

      {/* Search */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Search debates
        </label>
        <input
          type="text"
          value={filters.search || ''}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          onKeyUp={(e) => e.key === 'Enter' && applyFilters()}
          placeholder="e.g., climate, healthcare, budget"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        />
      </div>

      {/* Date Range */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Date Range
        </label>
        <select
          value={filters.dateRange}
          onChange={(e) => setFilters({ ...filters, dateRange: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          {dateRanges.map(range => (
            <option key={range.value} value={range.value}>
              {range.label}
            </option>
          ))}
        </select>
      </div>

      {/* Custom Date Range */}
      {filters.dateRange === 'custom' && (
        <div className="mb-4 space-y-2">
          <div>
            <label className="block text-xs text-gray-600">Start Date</label>
            <input
              type="date"
              value={filters.customStartDate}
              onChange={(e) => setFilters({ ...filters, customStartDate: e.target.value })}
              min="1994-01-17"
              max={new Date().toISOString().split('T')[0]}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
            />
          </div>
          <div>
            <label className="block text-xs text-gray-600">End Date</label>
            <input
              type="date"
              value={filters.customEndDate}
              onChange={(e) => setFilters({ ...filters, customEndDate: e.target.value })}
              min="1994-01-17"
              max={new Date().toISOString().split('T')[0]}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
            />
          </div>
        </div>
      )}

      {/* Apply/Clear Buttons */}
      <div className="space-y-2 mb-6">
        <button
          onClick={applyFilters}
          className="w-full px-4 py-2 bg-op-blue text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Apply Filters
        </button>
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="w-full px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
          >
            Clear All
          </button>
        )}
      </div>

      {/* Archive Statistics */}
      <div className="pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Archive Statistics</h3>
        <div className="space-y-2 text-sm text-gray-600">
          <div className="flex justify-between">
            <span>Years covered:</span>
            <span className="font-medium">{totalYears}</span>
          </div>
          <div className="flex justify-between">
            <span>First debate:</span>
            <span className="font-medium">Jan 17, 1994</span>
          </div>
          <div className="flex justify-between">
            <span>Total debates:</span>
            <span className="font-medium">~5,000+</span>
          </div>
          <div className="flex justify-between">
            <span>Total statements:</span>
            <span className="font-medium">~500,000+</span>
          </div>
        </div>
      </div>

      {/* Quick Links */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Quick Access</h3>
        <div className="space-y-2">
          <button
            onClick={() => {
              const today = new Date().toISOString().split('T')[0];
              router.push(`/debates?date_gte=${today}`);
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Today's apos;s debates
          </button>
          <button
            onClick={() => {
              setFilters({ ...filters, search: 'question period' });
              router.push('/debates?search=question%20period');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Question Period transcripts
          </button>
          <button
            onClick={() => {
              setFilters({ ...filters, search: 'throne speech' });
              router.push('/debates?search=throne%20speech');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Throne speeches
          </button>
        </div>
      </div>

      {/* RSS Feed */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <a
          href="/api/v1/debates/rss"
          className="flex items-center text-sm text-op-blue hover:underline"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z" />
          </svg>
          RSS Feed for Debates
        </a>
      </div>
    </div>
  );
}
