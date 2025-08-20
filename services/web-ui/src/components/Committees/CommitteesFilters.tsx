'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface CommitteesFiltersProps {
  currentFilters: {
    search?: string;
    type?: string;
    active?: string;
  };
}

export default function CommitteesFilters({ currentFilters }: CommitteesFiltersProps) {
  const router = useRouter();
  const [filters, setFilters] = useState(currentFilters);

  const committeeTypes = [
    { value: '', label: 'All Types' },
    { value: 'standing', label: 'Standing Committees' },
    { value: 'special', label: 'Special Committees' },
    { value: 'joint', label: 'Joint Committees' },
    { value: 'subcommittee', label: 'Subcommittees' },
  ];

  const applyFilters = () => {
    const params = new URLSearchParams();
    
    if (filters.search) params.set('search', filters.search);
    if (filters.type) params.set('type', filters.type);
    if (filters.active) params.set('active', filters.active);
    
    const queryString = params.toString();
    router.push(`/committees${queryString ? `?${queryString}` : ''}`);
  };

  const clearFilters = () => {
    setFilters({});
    router.push('/committees');
  };

  const hasActiveFilters = filters.search || filters.type || filters.active;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-bold mb-4">Filter Committees</h2>

      {/* Search */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Search committees
        </label>
        <input
          type="text"
          value={filters.search || ''}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          onKeyUp={(e) => e.key === 'Enter' && applyFilters()}
          placeholder="e.g., Finance, Health, Environment"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        />
      </div>

      {/* Committee Type */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Committee Type
        </label>
        <select
          value={filters.type || ''}
          onChange={(e) => setFilters({ ...filters, type: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          {committeeTypes.map(type => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>

      {/* Active Status */}
      <div className="mb-6">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={filters.active === 'true'}
            onChange={(e) => setFilters({ ...filters, active: e.target.checked ? 'true' : '' })}
            className="mr-2 rounded border-gray-300 text-op-blue focus:ring-op-blue"
          />
          <span className="text-sm text-gray-700">Show only active committees</span>
        </label>
      </div>

      {/* Apply/Clear Buttons */}
      <div className="space-y-2">
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

      {/* Committee Categories */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Popular Committees</h3>
        <div className="space-y-2">
          <button
            onClick={() => {
              setFilters({ search: 'Finance' });
              router.push('/committees?search=Finance');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Finance (FINA)
          </button>
          <button
            onClick={() => {
              setFilters({ search: 'Health' });
              router.push('/committees?search=Health');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Health (HESA)
          </button>
          <button
            onClick={() => {
              setFilters({ search: 'Environment' });
              router.push('/committees?search=Environment');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Environment and Sustainable Development
          </button>
          <button
            onClick={() => {
              setFilters({ search: 'Indigenous' });
              router.push('/committees?search=Indigenous');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Indigenous and Northern Affairs
          </button>
        </div>
      </div>

      {/* Committee Statistics */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Committee Stats</h3>
        <div className="space-y-2 text-sm text-gray-600">
          <div className="flex justify-between">
            <span>Standing:</span>
            <span className="font-medium">24</span>
          </div>
          <div className="flex justify-between">
            <span>Special:</span>
            <span className="font-medium">2</span>
          </div>
          <div className="flex justify-between">
            <span>Joint:</span>
            <span className="font-medium">2</span>
          </div>
          <div className="flex justify-between font-medium pt-2 border-t">
            <span>Total:</span>
            <span>28</span>
          </div>
        </div>
      </div>

      {/* Resources */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Resources</h3>
        <div className="space-y-2">
          <a
            href="https://www.ourcommons.ca/committees/en"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center text-sm text-op-blue hover:underline"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            Official Committee Portal
          </a>
          <a
            href="/api/v1/committees"
            className="flex items-center text-sm text-op-blue hover:underline"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            Committee API
          </a>
        </div>
      </div>
    </div>
  );
}
