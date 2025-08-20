'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

interface MPFiltersProps {
  currentFilters: {
    search?: string;
    province?: string;
    party?: string;
    current?: boolean;
  };
}

export default function MPFilters({ currentFilters }: MPFiltersProps) {
  const router = useRouter();
  const [filters, setFilters] = useState(currentFilters);

  const provinces = [
    { code: '', name: 'All Provinces' },
    { code: 'ON', name: 'Ontario' },
    { code: 'QC', name: 'Quebec' },
    { code: 'BC', name: 'British Columbia' },
    { code: 'AB', name: 'Alberta' },
    { code: 'MB', name: 'Manitoba' },
    { code: 'SK', name: 'Saskatchewan' },
    { code: 'NS', name: 'Nova Scotia' },
    { code: 'NB', name: 'New Brunswick' },
    { code: 'NL', name: 'Newfoundland and Labrador' },
    { code: 'PE', name: 'Prince Edward Island' },
    { code: 'NT', name: 'Northwest Territories' },
    { code: 'YT', name: 'Yukon' },
    { code: 'NU', name: 'Nunavut' },
  ];

  const parties = [
    { slug: '', name: 'All Parties' },
    { slug: 'liberal', name: 'Liberal' },
    { slug: 'conservative', name: 'Conservative' },
    { slug: 'ndp', name: 'NDP' },
    { slug: 'bloc', name: 'Bloc Québécois' },
    { slug: 'green', name: 'Green' },
  ];

  const applyFilters = () => {
    const params = new URLSearchParams();
    
    if (filters.search) params.set('search', filters.search);
    if (filters.province) params.set('province', filters.province);
    if (filters.party) params.set('party', filters.party);
    if (filters.current === false) params.set('current', 'false');
    
    const queryString = params.toString();
    router.push(`/mps${queryString ? `?${queryString}` : ''}`);
  };

  const clearFilters = () => {
    setFilters({ current: true });
    router.push('/mps');
  };

  const hasActiveFilters = filters.search || filters.province || filters.party || filters.current === false;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-bold mb-4">Filter MPs</h2>

      {/* Search */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Search by name or riding
        </label>
        <input
          type="text"
          value={filters.search || ''}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          onKeyUp={(e) => e.key === 'Enter' && applyFilters()}
          placeholder="e.g., Trudeau or Ottawa"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        />
      </div>

      {/* Province */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Province/Territory
        </label>
        <select
          value={filters.province || ''}
          onChange={(e) => setFilters({ ...filters, province: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          {provinces.map(province => (
            <option key={province.code} value={province.code}>
              {province.name}
            </option>
          ))}
        </select>
      </div>

      {/* Party */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Political Party
        </label>
        <select
          value={filters.party || ''}
          onChange={(e) => setFilters({ ...filters, party: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          {parties.map(party => (
            <option key={party.slug} value={party.slug}>
              {party.name}
            </option>
          ))}
        </select>
      </div>

      {/* Current/Former */}
      <div className="mb-6">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={filters.current !== false}
            onChange={(e) => setFilters({ ...filters, current: e.target.checked })}
            className="mr-2 rounded border-gray-300 text-op-blue focus:ring-op-blue"
          />
          <span className="text-sm text-gray-700">Current MPs only</span>
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

      {/* RSS Feed Link */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <a
          href="/api/v1/mps/rss"
          className="flex items-center text-sm text-op-blue hover:underline"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z" />
          </svg>
          RSS Feed
        </a>
      </div>
    </div>
  );
}
