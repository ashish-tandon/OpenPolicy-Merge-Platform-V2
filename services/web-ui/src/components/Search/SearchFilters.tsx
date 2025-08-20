'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

interface SearchFiltersProps {
  currentQuery: string;
  currentType: string;
}

export default function SearchFilters({ currentQuery, currentType }: SearchFiltersProps) {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState(currentQuery);
  const [selectedType, setSelectedType] = useState(currentType);

  useEffect(() => {
    setSearchQuery(currentQuery);
  }, [currentQuery]);

  const contentTypes = [
    { value: 'all', label: 'All Content', count: 133591 },
    { value: 'politicians', label: 'MPs', count: 1247 },
    { value: 'bills', label: 'Bills', count: 3456 },
    { value: 'debates', label: 'Debates', count: 98234 },
    { value: 'votes', label: 'Votes', count: 2341 },
    { value: 'committees', label: 'Committees', count: 567 },
    { value: 'speeches', label: 'Speeches', count: 27746 },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const params = new URLSearchParams();
      params.set('q', searchQuery);
      if (selectedType !== 'all') {
        params.set('type', selectedType);
      }
      router.push(`/search?${params.toString()}`);
    }
  };

  const handleTypeChange = (type: string) => {
    setSelectedType(type);
    if (currentQuery) {
      const params = new URLSearchParams();
      params.set('q', currentQuery);
      if (type !== 'all') {
        params.set('type', type);
      }
      router.push(`/search?${params.toString()}`);
    }
  };

  const isPostalCode = (input: string): boolean => {
    const postalCodeRegex = /^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$/;
    return postalCodeRegex.test(input.trim());
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-bold mb-4">Search & Filter</h2>

      {/* Search Box */}
      <form onSubmit={handleSearch} className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Search Query
        </label>
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search..."
            className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
          />
          <button
            type="submit"
            className="absolute right-2 top-2 text-gray-500 hover:text-op-blue"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
        {isPostalCode(searchQuery) && (
          <p className="mt-2 text-sm text-op-blue">
            <a href={`/search/postal/${searchQuery.replace(/\s/g, '')}`} className="hover:underline">
              → Find MP for postal code {searchQuery.toUpperCase()}
            </a>
          </p>
        )}
      </form>

      {/* Content Type Filter */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Filter by Type</h3>
        <div className="space-y-2">
          {contentTypes.map((type) => (
            <label
              key={type.value}
              className="flex items-center justify-between py-2 px-3 rounded hover:bg-gray-50 cursor-pointer"
            >
              <div className="flex items-center">
                <input
                  type="radio"
                  name="content-type"
                  value={type.value}
                  checked={selectedType === type.value}
                  onChange={() => handleTypeChange(type.value)}
                  className="mr-2 text-op-blue focus:ring-op-blue"
                />
                <span className="text-sm">{type.label}</span>
              </div>
              {currentQuery && (
                <span className="text-xs text-gray-500">
                  {type.count.toLocaleString()}
                </span>
              )}
            </label>
          ))}
        </div>
      </div>

      {/* Date Range Filter */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Date Range</h3>
        <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue text-sm">
          <option value="">Any time</option>
          <option value="day">Last 24 hours</option>
          <option value="week">Last week</option>
          <option value="month">Last month</option>
          <option value="year">Last year</option>
          <option value="custom">Custom range...</option>
        </select>
      </div>

      {/* Advanced Search Options */}
      <div className="pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Advanced Options</h3>
        <div className="space-y-3 text-sm">
          <label className="flex items-center">
            <input type="checkbox" className="mr-2 rounded text-op-blue focus:ring-op-blue" />
            <span>Search in titles only</span>
          </label>
          <label className="flex items-center">
            <input type="checkbox" className="mr-2 rounded text-op-blue focus:ring-op-blue" />
            <span>Exact phrase matching</span>
          </label>
          <label className="flex items-center">
            <input type="checkbox" className="mr-2 rounded text-op-blue focus:ring-op-blue" />
            <span>Include French results</span>
          </label>
        </div>
      </div>

      {/* Search History */}
      {currentQuery && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Recent Searches</h3>
          <div className="space-y-1">
            <button className="block w-full text-left text-sm text-op-blue hover:underline py-1">
              climate change
            </button>
            <button className="block w-full text-left text-sm text-op-blue hover:underline py-1">
              Bill C-5
            </button>
            <button className="block w-full text-left text-sm text-op-blue hover:underline py-1">
              healthcare funding
            </button>
          </div>
        </div>
      )}

      {/* Help Links */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Need Help?</h3>
        <ul className="space-y-2 text-sm">
          <li>
            <a href="/help/search" className="text-op-blue hover:underline">
              Search tips & tricks
            </a>
          </li>
          <li>
            <a href="/api" className="text-op-blue hover:underline">
              API for developers
            </a>
          </li>
          <li>
            <a href="/downloads" className="text-op-blue hover:underline">
              Bulk data downloads
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
}
