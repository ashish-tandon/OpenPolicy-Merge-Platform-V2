'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { Representative, Bill, Vote, Jurisdiction } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';
import { RepresentativeIcon } from '@/components/Government/GovernmentIcons';

interface RepresentativePageData {
  representative: Representative;
  sponsoredBills: PaginatedResponse<Bill>;
  votingRecord: PaginatedResponse<Vote>;
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

export default function RepresentativeDetailPage() {
  const params = useParams();
  const representativeId = params.id as string;
  
  const [data, setData] = useState<RepresentativePageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'bills' | 'votes' | 'contact'>('overview');

  useEffect(() => {
    const fetchRepresentativeData = async () => {
      try {
        setLoading(true);
        
        // Fetch representative details
        const representativeResponse = await fetch(`/api/v1/multi-level-government/representatives/${representativeId}`);
        if (!representativeResponse.ok) {
          throw new Error('Failed to fetch representative data');
        }
        const representativeData = await representativeResponse.json();

        // Fetch related data
        const [billsResponse, votesResponse] = await Promise.all([
          fetch(`/api/v1/multi-level-government/bills?sponsor_id=${representativeId}&page_size=10`),
          fetch(`/api/v1/multi-level-government/votes?representative_id=${representativeId}&page_size=20`)
        ]);

        const [billsData, votesData] = await Promise.all([
          billsResponse.json(),
          votesResponse.json()
        ]);

        setData({
          representative: representativeData,
          sponsoredBills: billsData,
          votingRecord: votesData,
          jurisdiction: representativeData.jurisdiction
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load representative data');
      } finally {
        setLoading(false);
      }
    };

    if (representativeId) {
      fetchRepresentativeData();
    }
  }, [representativeId]);

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
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Representative</h2>
            <p className="text-red-600">{error || 'Representative not found'}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Representative Header */}
      <div className="bg-gradient-to-br from-op-blue to-blue-700 text-white">
        <div className="content-container py-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <div className="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <RepresentativeIcon className="w-12 h-12 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold mb-2">{data.representative.name}</h1>
                <p className="text-xl text-blue-100">
                  {getPositionLabel(data.representative.position)}
                </p>
                <div className="flex items-center space-x-4 mt-2">
                  <span className={`px-3 py-1 rounded text-sm font-medium ${getGovernmentLevelColor(data.jurisdiction.government_level.name)}`}>
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
            <div className="text-right">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-2xl font-bold">{data.sponsoredBills.pagination.total.toLocaleString()}</div>
                  <div className="text-blue-200 text-sm">Bills Sponsored</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">{data.votingRecord.pagination.total.toLocaleString()}</div>
                  <div className="text-blue-200 text-sm">Votes Cast</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200 sticky top-16 z-40">
        <div className="content-container">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'bills', label: 'Bills Sponsored' },
              { id: 'votes', label: 'Voting Record' },
              { id: 'contact', label: 'Contact & Info' }
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
            {/* Representative Information */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Representative Information</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Basic Details</h3>
                  <div className="space-y-2 text-sm text-gray-600">
                    <p><span className="font-medium">Position:</span> {getPositionLabel(data.representative.position)}</p>
                    <p><span className="font-medium">Political Party:</span> {data.representative.party || 'Independent'}</p>
                    {data.representative.riding && (
                      <p><span className="font-medium">Electoral District:</span> {data.representative.riding}</p>
                    )}
                    <p><span className="font-medium">Jurisdiction:</span> {data.jurisdiction.name}</p>
                    <p><span className="font-medium">Government Level:</span> {data.jurisdiction.government_level.name}</p>
                    {data.jurisdiction.province && (
                      <p><span className="font-medium">Province/Territory:</span> {data.jurisdiction.province}</p>
                    )}
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Contact Information</h3>
                  <div className="space-y-3">
                    {data.representative.email && (
                      <a
                        href={`mailto:${data.representative.email}`}
                        className="flex items-center space-x-2 text-op-blue hover:text-blue-700"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                        <span>{data.representative.email}</span>
                      </a>
                    )}
                    {data.representative.phone && (
                      <a
                        href={`tel:${data.representative.phone}`}
                        className="flex items-center space-x-2 text-op-blue hover:text-blue-700"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                        </svg>
                        <span>{data.representative.phone}</span>
                      </a>
                    )}
                    {data.representative.website && (
                      <a
                        href={data.representative.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-2 text-op-blue hover:text-blue-700"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                        <span>Personal Website</span>
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Activity Summary */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Recent Bills */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Bills Sponsored</h3>
                  <Link href={`/government/representatives/${representativeId}?tab=bills`} className="text-op-blue hover:text-blue-700 text-sm">
                    View All →
                  </Link>
                </div>
                <div className="space-y-3">
                  {data.sponsoredBills.items.slice(0, 5).map((bill) => (
                    <div key={bill.id} className="border-l-4 border-op-blue pl-4">
                      <h4 className="font-medium text-gray-900 text-sm">{bill.bill_number}</h4>
                      <p className="text-gray-600 text-xs line-clamp-2">{bill.title}</p>
                      <p className="text-gray-500 text-xs mt-1">Status: {bill.status}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Votes */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Voting Activity</h3>
                  <Link href={`/government/representatives/${representativeId}?tab=votes`} className="text-op-blue hover:text-blue-700 text-sm">
                    View All →
                  </Link>
                </div>
                <div className="space-y-3">
                  {data.votingRecord.items.slice(0, 5).map((vote) => (
                    <div key={vote.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <p className="text-sm text-gray-900 line-clamp-1">
                          {vote.bill ? vote.bill.title : 'Bill information unavailable'}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(vote.vote_date).toLocaleDateString()}
                        </p>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getVotePositionColor(vote.vote_position)}`}>
                        {getVotePositionLabel(vote.vote_position)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'bills' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Bills Sponsored</h2>
            <div className="space-y-4">
              {data.sponsoredBills.items.map((bill) => (
                <div key={bill.id} className="border border-gray-200 rounded-lg p-4 hover:border-op-blue transition-colors">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="bg-op-blue text-white px-2 py-1 rounded text-sm font-medium">
                          {bill.bill_number}
                        </span>
                        <span className={`px-2 py-1 rounded text-sm ${
                          bill.status === 'enacted' ? 'bg-green-100 text-green-800' :
                          bill.status === 'introduced' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {bill.status}
                        </span>
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-2">{bill.title}</h3>
                      {bill.summary && (
                        <p className="text-gray-600 text-sm line-clamp-2">{bill.summary}</p>
                      )}
                      <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500">
                        {bill.introduced_date && (
                          <span>Introduced: {new Date(bill.introduced_date).toLocaleDateString()}</span>
                        )}
                        <span>Jurisdiction: {bill.jurisdiction.name}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {data.sponsoredBills.pagination.total_pages > 1 && (
              <div className="mt-6">
                <Pagination 
                  currentPage={data.sponsoredBills.pagination.page}
                  totalPages={data.sponsoredBills.pagination.total_pages}
                  baseUrl={`/government/representatives/${representativeId}`}
                  queryParams={{ tab: 'bills' }}
                />
              </div>
            )}
          </div>
        )}

        {activeTab === 'votes' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Voting Record</h2>
            <div className="space-y-4">
              {data.votingRecord.items.map((vote) => (
                <div key={vote.id} className="border border-gray-200 rounded-lg p-4 hover:border-op-blue transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <span className={`px-3 py-1 rounded text-sm font-medium ${getVotePositionColor(vote.vote_position)}`}>
                          {getVotePositionLabel(vote.vote_position)}
                        </span>
                        <span className="text-sm text-gray-500">
                          {new Date(vote.vote_date).toLocaleDateString()}
                        </span>
                      </div>
                      
                      {vote.bill ? (
                        <div>
                          <h3 className="font-semibold text-gray-900 mb-2">{vote.bill.title}</h3>
                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <span>Bill: {vote.bill.bill_number}</span>
                            <span>Status: {vote.bill.status}</span>
                            <span>Jurisdiction: {vote.bill.jurisdiction.name}</span>
                          </div>
                        </div>
                      ) : (
                        <p className="text-gray-500">Bill information unavailable</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {data.votingRecord.pagination.total_pages > 1 && (
              <div className="mt-6">
                <Pagination 
                  currentPage={data.votingRecord.pagination.page}
                  totalPages={data.votingRecord.pagination.total_pages}
                  baseUrl={`/government/representatives/${representativeId}`}
                  queryParams={{ tab: 'votes' }}
                />
              </div>
            )}
          </div>
        )}

        {activeTab === 'contact' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Contact & Additional Information</h2>
            
            {/* Contact Details */}
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
                <div className="space-y-4">
                  {data.representative.email && (
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Email</p>
                        <a href={`mailto:${data.representative.email}`} className="text-op-blue hover:text-blue-700">
                          {data.representative.email}
                        </a>
                      </div>
                    </div>
                  )}
                  
                  {data.representative.phone && (
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                        </svg>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Phone</p>
                        <a href={`tel:${data.representative.phone}`} className="text-op-blue hover:text-blue-700">
                          {data.representative.phone}
                        </a>
                      </div>
                    </div>
                  )}
                  
                  {data.representative.website && (
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                        <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Website</p>
                        <a 
                          href={data.representative.website} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-op-blue hover:text-blue-700"
                        >
                          Personal Website
                        </a>
                      </div>
                    </div>
                  )}
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Representative Details</h3>
                <div className="space-y-3 text-sm text-gray-600">
                  <p><span className="font-medium">Position:</span> {getPositionLabel(data.representative.position)}</p>
                  <p><span className="font-medium">Political Party:</span> {data.representative.party || 'Independent'}</p>
                  {data.representative.riding && (
                    <p><span className="font-medium">Electoral District:</span> {data.representative.riding}</p>
                  )}
                  <p><span className="font-medium">Jurisdiction:</span> {data.jurisdiction.name}</p>
                  <p><span className="font-medium">Government Level:</span> {data.jurisdiction.government_level.name}</p>
                  {data.jurisdiction.province && (
                    <p><span className="font-medium">Province/Territory:</span> {data.jurisdiction.province}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Additional Information */}
            {data.representative.extras && Object.keys(data.representative.extras).length > 0 && (
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Information</h3>
                <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded text-sm text-gray-600">
                  {JSON.stringify(data.representative.extras, null, 2)}
                </pre>
              </div>
            )}

            {/* Metadata */}
            {data.representative.metadata_json && Object.keys(data.representative.metadata_json).length > 0 && (
              <div className="border-t border-gray-200 pt-6 mt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Metadata</h3>
                <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded text-sm text-gray-600">
                  {JSON.stringify(data.representative.metadata_json, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
