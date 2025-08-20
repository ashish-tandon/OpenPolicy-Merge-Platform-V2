'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface BillsFiltersProps {
  currentFilters: {
    search?: string;
    session?: string;
    type?: string;
    status?: string;
  };
}

export default function BillsFilters({ currentFilters }: BillsFiltersProps) {
  const router = useRouter();
  const [filters, setFilters] = useState(currentFilters);

  const sessions = [
    { value: '', label: 'All Sessions' },
    { value: '45-1', label: '45th Parliament - 1st Session' },
    { value: '44-1', label: '44th Parliament - 1st Session' },
    { value: '43-2', label: '43rd Parliament - 2nd Session' },
    { value: '43-1', label: '43rd Parliament - 1st Session' },
    { value: '42-1', label: '42nd Parliament - 1st Session' },
  ];

  const billTypes = [
    { value: '', label: 'All Bill Types' },
    { value: 'government', label: 'Government Bills' },
    { value: 'private', label: 'Private Member Bills' },
  ];

  const billStatuses = [
    { value: '', label: 'All Statuses' },
    { value: 'law', label: 'Became Law' },
    { value: 'senate', label: 'In Senate' },
    { value: 'house', label: 'In House' },
    { value: 'committee', label: 'In Committee' },
    { value: 'first-reading', label: 'First Reading' },
    { value: 'second-reading', label: 'Second Reading' },
    { value: 'third-reading', label: 'Third Reading' },
    { value: 'defeated', label: 'Defeated' },
    { value: 'withdrawn', label: 'Withdrawn' },
  ];

  const applyFilters = () => {
    const params = new URLSearchParams();
    
    if (filters.search) params.set('search', filters.search);
    if (filters.session) params.set('session', filters.session);
    if (filters.type) params.set('type', filters.type);
    if (filters.status) params.set('status', filters.status);
    
    const queryString = params.toString();
    router.push(`/bills${queryString ? `?${queryString}` : ''}`);
  };

  const clearFilters = () => {
    setFilters({});
    router.push('/bills');
  };

  const hasActiveFilters = filters.search || filters.session || filters.type || filters.status;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-bold mb-4">Filter Bills</h2>

      {/* Search */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Search bills
        </label>
        <input
          type="text"
          value={filters.search || ''}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          onKeyUp={(e) => e.key === 'Enter' && applyFilters()}
          placeholder="e.g., C-5, climate, budget"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        />
      </div>

      {/* Session */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Parliamentary Session
        </label>
        <select
          value={filters.session || ''}
          onChange={(e) => setFilters({ ...filters, session: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          {sessions.map(session => (
            <option key={session.value} value={session.value}>
              {session.label}
            </option>
          ))}
        </select>
      </div>

      {/* Bill Type */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Bill Type
        </label>
        <select
          value={filters.type || ''}
          onChange={(e) => setFilters({ ...filters, type: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          {billTypes.map(type => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>
      </div>

      {/* Status */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Status
        </label>
        <select
          value={filters.status || ''}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          {billStatuses.map(status => (
            <option key={status.value} value={status.value}>
              {status.label}
            </option>
          ))}
        </select>
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

      {/* Quick Links */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Quick Filters</h3>
        <div className="space-y-2">
          <button
            onClick={() => {
              setFilters({ status: 'law' });
              router.push('/bills?status=law');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Bills that became law
          </button>
          <button
            onClick={() => {
              setFilters({ type: 'private' });
              router.push('/bills?type=private');
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Private member bills
          </button>
          <button
            onClick={() => {
              const currentSession = '45-1';
              setFilters({ session: currentSession });
              router.push(`/bills?session=${currentSession}`);
            }}
            className="w-full text-left text-sm text-op-blue hover:underline"
          >
            Current session only
          </button>
        </div>
      </div>

      {/* External Links */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-sm font-medium text-gray-700 mb-3">External Resources</h3>
        <div className="space-y-2">
          <a
            href="https://www.parl.ca/legisinfo"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center text-sm text-op-blue hover:underline"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            LEGISinfo
          </a>
        </div>
      </div>
    </div>
  );
}
