'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { Bill, Vote, Representative, Jurisdiction } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';
import { BillIcon } from '@/components/Government/GovernmentIcons';

interface BillPageData {
  bill: Bill;
  votes: PaginatedResponse<Vote>;
  sponsor: Representative | null;
  jurisdiction: Jurisdiction;
}

interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  };
}

export default function BillDetailPage() {
  const params = useParams();
  const billId = params.id as string;
  
  const [data, setData] = useState<BillPageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'votes' | 'details' | 'history'>('overview');

  useEffect(() => {
    const fetchBillData = async () => {
      try {
        setLoading(true);
        
        // Fetch bill details
        const billResponse = await fetch(`/api/v1/multi-level-government/bills/${billId}`);
        if (!billResponse.ok) {
          throw new Error('Failed to fetch bill data');
        }
        const billData = await billResponse.json();

        // Fetch related data
        const votesResponse = await fetch(`/api/v1/multi-level-government/votes?bill_id=${billId}&page_size=50`);
        const votesData = await votesResponse.json();

        setData({
          bill: billData,
          votes: votesData,
          sponsor: billData.sponsor,
          jurisdiction: billData.jurisdiction
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load bill data');
      } finally {
        setLoading(false);
      }
    };

    if (billId) {
      fetchBillData();
    }
  }, [billId]);

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

  const calculateVoteStats = () => {
    if (!data?.votes.items.length) return null;
    
    const stats = {
      yes: 0,
      no: 0,
      abstain: 0,
      absent: 0,
      paired: 0,
      total: data.votes.items.length
    };

    data.votes.items.forEach(vote => {
      const position = vote.vote_position.toLowerCase();
      if (stats.hasOwnProperty(position)) {
        stats[position as keyof typeof stats]++;
      }
    });

    return stats;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="content-container py-12">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="content-container py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Bill</h2>
            <p className="text-red-600">{error || 'Bill not found'}</p>
          </div>
        </div>
      </div>
    );
  }

  const voteStats = calculateVoteStats();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Bill Header */}
      <div className="bg-gradient-to-br from-op-blue to-blue-700 text-white">
        <div className="content-container py-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <div className="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <BillIcon className="w-12 h-12 text-white" />
              </div>
              <div>
                <div className="flex items-center space-x-3 mb-2">
                  <h1 className="text-4xl font-bold">{data.bill.bill_number}</h1>
                  <span className={`px-3 py-1 rounded text-sm font-medium ${getStatusColor(data.bill.status)}`}>
                    {getStatusLabel(data.bill.status)}
                  </span>
                </div>
                <p className="text-xl text-blue-100 mb-2">{data.bill.title}</p>
                <div className="flex items-center space-x-4">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getGovernmentLevelColor(data.jurisdiction.government_level.name)}`}>
                    {data.jurisdiction.government_level.name}
                  </span>
                  <span className="text-blue-200">
                    {data.jurisdiction.name}
                    {data.jurisdiction.province && ` • ${data.jurisdiction.province}`}
                  </span>
                </div>
              </div>
            </div>
            
            {/* Quick Stats */}
            {voteStats && (
              <div className="text-right">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-2xl font-bold">{voteStats.total}</div>
                    <div className="text-blue-200 text-sm">Total Votes</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{voteStats.yes}</div>
                    <div className="text-blue-200 text-sm">Yes Votes</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200 sticky top-16 z-40">
        <div className="content-container">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'votes', label: 'Voting Record' },
              { id: 'details', label: 'Bill Details' },
              { id: 'history', label: 'Legislative History' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-2 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-op-blue text-op-blue'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="content-container py-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Bill Summary */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Bill Summary</h2>
              {data.bill.summary ? (
                <p className="text-gray-700 text-lg leading-relaxed">{data.bill.summary}</p>
              ) : (
                <p className="text-gray-500 italic">No summary available for this bill.</p>
              )}
            </div>

            {/* Bill Information */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Bill Information</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Basic Details</h3>
                  <div className="space-y-2 text-sm text-gray-600">
                    <p><span className="font-medium">Bill Number:</span> {data.bill.bill_number}</p>
                    <p><span className="font-medium">Status:</span> {getStatusLabel(data.bill.status)}</p>
                    <p><span className="font-medium">Jurisdiction:</span> {data.jurisdiction.name}</p>
                    <p><span className="font-medium">Government Level:</span> {data.jurisdiction.government_level.name}</p>
                    {data.jurisdiction.province && (
                      <p><span className="font-medium">Province/Territory:</span> {data.jurisdiction.province}</p>
                    )}
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Timeline</h3>
                  <div className="space-y-2 text-sm text-gray-600">
                    {data.bill.introduced_date && (
                      <p><span className="font-medium">Introduced:</span> {new Date(data.bill.introduced_date).toLocaleDateString()}</p>
                    )}
                    <p><span className="font-medium">Created:</span> {new Date(data.bill.created_at).toLocaleDateString()}</p>
                    <p><span className="font-medium">Last Updated:</span> {new Date(data.bill.updated_at).toLocaleDateString()}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Sponsor Information */}
            {data.sponsor && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Bill Sponsor</h2>
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-op-blue bg-opacity-10 rounded-full flex items-center justify-center">
                    <span className="text-op-blue font-medium text-lg">
                      {data.sponsor.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">{data.sponsor.name}</h3>
                    <p className="text-gray-600">{data.sponsor.position?.toUpperCase()} • {data.sponsor.party || 'Independent'}</p>
                    {data.sponsor.riding && (
                      <p className="text-gray-500 text-sm">{data.sponsor.riding}</p>
                    )}
                    <div className="flex space-x-3 mt-2">
                      {data.sponsor.email && (
                        <a
                          href={`mailto:${data.sponsor.email}`}
                          className="text-op-blue hover:text-blue-700 text-sm"
                        >
                          📧 Email Sponsor
                        </a>
                      )}
                      <Link
                        href={`/government/representatives/${data.sponsor.id}`}
                        className="text-op-blue hover:text-blue-700 text-sm"
                      >
                        👤 View Profile →
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Voting Summary */}
            {voteStats && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Voting Summary</h2>
                <div className="grid md:grid-cols-5 gap-4">
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{voteStats.yes}</div>
                    <div className="text-green-800 font-medium">Yes</div>
                    <div className="text-green-600 text-sm">
                      {Math.round((voteStats.yes / voteStats.total) * 100)}%
                    </div>
                  </div>
                  
                  <div className="text-center p-4 bg-red-50 rounded-lg">
                    <div className="text-2xl font-bold text-red-600">{voteStats.no}</div>
                    <div className="text-red-800 font-medium">No</div>
                    <div className="text-red-600 text-sm">
                      {Math.round((voteStats.no / voteStats.total) * 100)}%
                    </div>
                  </div>
                  
                  <div className="text-center p-4 bg-yellow-50 rounded-lg">
                    <div className="text-2xl font-bold text-yellow-600">{voteStats.abstain}</div>
                    <div className="text-yellow-800 font-medium">Abstain</div>
                    <div className="text-yellow-600 text-sm">
                      {Math.round((voteStats.abstain / voteStats.total) * 100)}%
                    </div>
                  </div>
                  
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-2xl font-bold text-gray-600">{voteStats.absent}</div>
                    <div className="text-gray-800 font-medium">Absent</div>
                    <div className="text-gray-600 text-sm">
                      {Math.round((voteStats.absent / voteStats.total) * 100)}%
                    </div>
                  </div>
                  
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{voteStats.total}</div>
                    <div className="text-blue-800 font-medium">Total</div>
                    <div className="text-blue-600 text-sm">100%</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'votes' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Voting Record</h2>
            {data.votes.items.length > 0 ? (
              <div className="space-y-4">
                {data.votes.items.map((vote) => (
                  <div key={vote.id} className="border border-gray-200 rounded-lg p-4 hover:border-op-blue transition-colors">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-op-blue bg-opacity-10 rounded-full flex items-center justify-center">
                          <span className="text-op-blue font-medium">
                            {vote.representative.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                          </span>
                        </div>
                        <div>
                          <h3 className="font-semibold text-gray-900">{vote.representative.name}</h3>
                          <p className="text-gray-600">{vote.representative.position?.toUpperCase()} • {vote.representative.party || 'Independent'}</p>
                          {vote.representative.riding && (
                            <p className="text-gray-500 text-sm">{vote.representative.riding}</p>
                          )}
                        </div>
                      </div>
                      <div className="text-right">
                        <span className={`px-3 py-1 rounded text-sm font-medium ${getVotePositionColor(vote.vote_position)}`}>
                          {getVotePositionLabel(vote.vote_position)}
                        </span>
                        <p className="text-sm text-gray-500 mt-1">
                          {new Date(vote.vote_date).toLocaleDateString()}
                        </p>
                        {vote.session && (
                          <p className="text-xs text-gray-400">{vote.session}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                <p className="text-gray-500">No voting records found for this bill</p>
                <p className="text-gray-400 text-sm mt-2">Voting data may not be available yet</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'details' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Bill Details</h2>
            
            {/* Additional Information */}
            {data.bill.extras && Object.keys(data.bill.extras).length > 0 && (
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Information</h3>
                <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded text-sm text-gray-600">
                  {JSON.stringify(data.bill.extras, null, 2)}
                </pre>
              </div>
            )}

            {/* Jurisdiction Details */}
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Jurisdiction Information</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Basic Details</h4>
                  <div className="space-y-2 text-sm text-gray-600">
                    <p><span className="font-medium">Name:</span> {data.jurisdiction.name}</p>
                    <p><span className="font-medium">Code:</span> {data.jurisdiction.code}</p>
                    <p><span className="font-medium">Type:</span> {data.jurisdiction.jurisdiction_type}</p>
                    <p><span className="font-medium">Government Level:</span> {data.jurisdiction.government_level.name}</p>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Contact & Resources</h4>
                  {data.jurisdiction.website ? (
                    <a
                      href={data.jurisdiction.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-2 text-op-blue hover:text-blue-700"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      <span>Official Website</span>
                    </a>
                  ) : (
                    <p className="text-gray-500 text-sm">No official website available</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Legislative History</h2>
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-gray-500">Legislative history tracking will be displayed here</p>
              <p className="text-gray-400 text-sm mt-2">Coming soon with detailed timeline and progress tracking</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
