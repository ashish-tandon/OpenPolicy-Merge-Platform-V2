'use client';

import { useState, useEffect } from 'react';
import { PaginatedResponse, Vote, GovernmentLevel, VoteFilters } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';
import { VoteIcon } from '@/components/Government/GovernmentIcons';

export default function AllVotesPage() {
  const [votes, setVotes] = useState<PaginatedResponse<Vote> | null>(null);
  const [governmentLevels, setGovernmentLevels] = useState<GovernmentLevel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<VoteFilters>({
    page: 1,
    page_size: 20
  });

  const fetchVotes = async (currentFilters: VoteFilters) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      Object.entries(currentFilters).forEach(([key, value]) => {
        if (value !== undefined && value !== '') {
          params.append(key, value.toString());
        }
      });

      const response = await fetch(`/api/v1/multi-level-government/votes?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch votes');
      }

      const data = await response.json();
      setVotes(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load votes');
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
    fetchVotes(filters);
  }, [filters]);

  const handleFilterChange = (key: keyof VoteFilters, value: string | number | undefined) => {
    setFilters(prev => ({
      ...prev,
      [key]: value === '' ? undefined : value,
      page: key !== 'page' ? 1 : value
    }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  const getVotePositionColor = (position: string) => {
    const colors: Record<string, string> = {
      'yes': 'bg-green-100 text-green-800',
      'no': 'bg-red-100 text-red-800',
      'abstain': 'bg-yellow-100 text-yellow-800',
      'absent': 'bg-gray-100 text-gray-800',
      'paired': 'bg-blue-100 text-blue-800'
    };
    return colors[position.toLowerCase()] || 'bg-gray-100 text-gray-800';
  };

  const getVotePositionLabel = (position: string) => {
    const labels: Record<string, string> = {
      'yes': 'Yes',
      'no': 'No',
      'abstain': 'Abstain',
      'absent': 'Absent',
      'paired': 'Paired'
    };
    return labels[position.toLowerCase()] || position.charAt(0).toUpperCase() + position.slice(1);
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
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Votes</h2>
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
            <VoteIcon className="w-16 h-16 text-blue-100" />
            <div>
              <h1 className="text-4xl font-bold mb-2">All Votes & Decisions</h1>
              <p className="text-xl text-blue-100">
                Voting records across all levels of Canadian government
              </p>
              {votes && (
                <p className="text-blue-200 mt-2">
                  {votes.pagination.total.toLocaleString()} total votes tracked
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="content-container py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filter Votes</h2>
          <div className="grid md:grid-cols-4 gap-4">
            {/* Vote Position */}
            <div>
              <label htmlFor="vote_position" className="block text-sm font-medium text-gray-700 mb-1">
                Vote Position
              </label>
              <select
                id="vote_position"
                value={filters.vote_position || ''}
                onChange={(e) => handleFilterChange('vote_position', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              >
                <option value="">All positions</option>
                <option value="yes">Yes</option>
                <option value="no">No</option>
                <option value="abstain">Abstain</option>
                <option value="absent">Absent</option>
                <option value="paired">Paired</option>
              </select>
            </div>

            {/* Session */}
            <div>
              <label htmlFor="session" className="block text-sm font-medium text-gray-700 mb-1">
                Session
              </label>
              <input
                type="text"
                id="session"
                value={filters.session || ''}
                onChange={(e) => handleFilterChange('session', e.target.value)}
                placeholder="e.g., 44th Parliament"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              />
            </div>

            {/* Vote Date After */}
            <div>
              <label htmlFor="vote_after" className="block text-sm font-medium text-gray-700 mb-1">
                Vote Date After
              </label>
              <input
                type="date"
                id="vote_after"
                value={filters.vote_after || ''}
                onChange={(e) => handleFilterChange('vote_after', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-op-blue focus:border-op-blue"
              />
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

        {/* Votes List */}
        <div className="bg-white rounded-lg shadow-sm">
          {loading ? (
            <div className="p-12">
              <LoadingSpinner />
            </div>
          ) : votes && votes.items.length > 0 ? (
            <>
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Votes ({votes.pagination.total.toLocaleString()})
                  </h2>
                  <div className="text-sm text-gray-500">
                    Page {votes.pagination.page} of {votes.pagination.total_pages}
                  </div>
                </div>

                <div className="space-y-4">
                  {votes.items.map((vote) => (
                    <div
                      key={vote.id}
                      className="border border-gray-200 rounded-lg p-6 hover:border-op-blue transition-colors"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <span className={`px-3 py-1 rounded text-sm font-medium ${getVotePositionColor(vote.vote_position)}`}>
                            {getVotePositionLabel(vote.vote_position)}
                          </span>
                          {vote.bill && vote.bill.jurisdiction && (
                            <span className={`px-2 py-1 rounded text-xs font-medium ${getGovernmentLevelColor(vote.bill.jurisdiction.government_level.name)}`}>
                              {vote.bill.jurisdiction.government_level.name}
                            </span>
                          )}
                        </div>
                        <div className="text-sm text-gray-500">
                          {new Date(vote.vote_date).toLocaleDateString()}
                        </div>
                      </div>

                      <div className="grid md:grid-cols-2 gap-6">
                        <div>
                          <h3 className="font-semibold text-gray-900 mb-2">Representative</h3>
                          <div className="space-y-1 text-sm text-gray-600">
                            <p><span className="font-medium">Name:</span> {vote.representative.name}</p>
                            <p><span className="font-medium">Position:</span> {vote.representative.position?.toUpperCase()}</p>
                            {vote.representative.party && (
                              <p><span className="font-medium">Party:</span> {vote.representative.party}</p>
                            )}
                            {vote.representative.riding && (
                              <p><span className="font-medium">Riding:</span> {vote.representative.riding}</p>
                            )}
                          </div>
                        </div>

                        <div>
                          <h3 className="font-semibold text-gray-900 mb-2">Bill Information</h3>
                          {vote.bill ? (
                            <div className="space-y-1 text-sm text-gray-600">
                              <p><span className="font-medium">Bill:</span> {vote.bill.bill_number}</p>
                              <p><span className="font-medium">Title:</span> {vote.bill.title}</p>
                              <p><span className="font-medium">Status:</span> {vote.bill.status}</p>
                              {vote.bill.jurisdiction && (
                                <p><span className="font-medium">Jurisdiction:</span> {vote.bill.jurisdiction.name}</p>
                              )}
                            </div>
                          ) : (
                            <p className="text-sm text-gray-500">Bill information not available</p>
                          )}
                        </div>
                      </div>

                      {vote.session && (
                        <div className="mt-4 pt-4 border-t border-gray-100">
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Session:</span> {vote.session}
                          </p>
                        </div>
                      )}

                      {vote.extras && Object.keys(vote.extras).length > 0 && (
                        <div className="mt-4 pt-4 border-t border-gray-100">
                          <details className="text-sm">
                            <summary className="font-medium text-gray-700 cursor-pointer">Additional Details</summary>
                            <pre className="mt-2 whitespace-pre-wrap bg-gray-50 p-2 rounded text-xs text-gray-600">
                              {JSON.stringify(vote.extras, null, 2)}
                            </pre>
                          </details>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Pagination */}
              <div className="border-t border-gray-200 px-6 py-4">
                <Pagination
                  currentPage={votes.pagination.page}
                  totalPages={votes.pagination.total_pages}
                  baseUrl="/government/votes"
                  queryParams={filters}
                />
              </div>
            </>
          ) : (
            <div className="p-12 text-center">
              <VoteIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No votes found</h3>
              <p className="text-gray-500">
                Try adjusting your filters to see more results, or check back later as more voting data becomes available.
              </p>
            </div>
          )}
        </div>

        {/* Voting Pattern Analytics */}
        <div className="mt-12 bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Understanding Voting Patterns</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Vote Types</h3>
              <div className="space-y-2 text-sm">
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                  <span><strong>Yes:</strong> Vote in favor of the motion or bill</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-red-500 rounded-full"></span>
                  <span><strong>No:</strong> Vote against the motion or bill</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
                  <span><strong>Abstain:</strong> Deliberately not voting</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-gray-500 rounded-full"></span>
                  <span><strong>Absent:</strong> Not present for the vote</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
                  <span><strong>Paired:</strong> Paired with opposing member</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Data Sources</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Official legislative voting records</li>
                <li>• Parliamentary transcripts and minutes</li>
                <li>• Municipal council meeting records</li>
                <li>• Provincial legislature databases</li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Analysis Features</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Party voting cohesion analysis</li>
                <li>• Representative voting patterns</li>
                <li>• Bill passage success rates</li>
                <li>• Cross-party collaboration tracking</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
