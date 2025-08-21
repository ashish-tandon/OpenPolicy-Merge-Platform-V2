'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { Jurisdiction, Representative, Bill, Vote, GovernmentLevel } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import Pagination from '@/components/Pagination';
import { JurisdictionIcon, FederalIcon, ProvincialIcon, MunicipalIcon } from '@/components/Government/GovernmentIcons';

interface JurisdictionPageData {
  jurisdiction: Jurisdiction;
  stats: {
    total_representatives: number;
    total_bills: number;
    total_votes: number;
    total_offices: number;
  };
  representatives: PaginatedResponse<Representative>;
  recentBills: PaginatedResponse<Bill>;
  recentVotes: PaginatedResponse<Vote>;
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

export default function JurisdictionDetailPage() {
  const params = useParams();
  const jurisdictionId = params.id as string;
  
  const [data, setData] = useState<JurisdictionPageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'representatives' | 'bills' | 'votes' | 'offices'>('overview');

  useEffect(() => {
    const fetchJurisdictionData = async () => {
      try {
        setLoading(true);
        
        // Fetch jurisdiction details and stats
        const [jurisdictionResponse, statsResponse] = await Promise.all([
          fetch(`/api/v1/multi-level-government/jurisdictions/${jurisdictionId}`),
          fetch(`/api/v1/multi-level-government/stats/jurisdictions/${jurisdictionId}`)
        ]);

        if (!jurisdictionResponse.ok || !statsResponse.ok) {
          throw new Error('Failed to fetch jurisdiction data');
        }

        const [jurisdictionData, statsData] = await Promise.all([
          jurisdictionResponse.json(),
          statsResponse.json()
        ]);

        // Fetch related data
        const [representativesResponse, billsResponse, votesResponse] = await Promise.all([
          fetch(`/api/v1/multi-level-government/representatives?jurisdiction_id=${jurisdictionId}&page_size=10`),
          fetch(`/api/v1/multi-level-government/bills?jurisdiction_id=${jurisdictionId}&page_size=10`),
          fetch(`/api/v1/multi-level-government/votes?page_size=10`)
        ]);

        const [representativesData, billsData, votesData] = await Promise.all([
          representativesResponse.json(),
          billsResponse.json(),
          votesResponse.json()
        ]);

        setData({
          jurisdiction: jurisdictionData,
          stats: statsData,
          representatives: representativesData,
          recentBills: billsData,
          recentVotes: votesData
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load jurisdiction data');
      } finally {
        setLoading(false);
      }
    };

    if (jurisdictionId) {
      fetchJurisdictionData();
    }
  }, [jurisdictionId]);

  const getGovernmentIcon = (levelName: string) => {
    switch (levelName.toLowerCase()) {
      case 'federal':
        return <FederalIcon className="w-16 h-16" />;
      case 'provincial':
        return <ProvincialIcon className="w-16 h-16" />;
      case 'municipal':
        return <MunicipalIcon className="w-16 h-16" />;
      default:
        return <JurisdictionIcon className="w-16 h-16" />;
    }
  };

  const getGovernmentLevelColor = (levelName: string) => {
    switch (levelName.toLowerCase()) {
      case 'federal':
        return 'from-red-600 to-red-700';
      case 'provincial':
        return 'from-blue-600 to-blue-700';
      case 'municipal':
        return 'from-green-600 to-green-700';
      default:
        return 'from-gray-600 to-gray-700';
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
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Jurisdiction</h2>
            <p className="text-red-600">{error || 'Jurisdiction not found'}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Jurisdiction Header */}
      <div className={`bg-gradient-to-br ${getGovernmentLevelColor(data.jurisdiction.government_level.name)} text-white`}>
        <div className="content-container py-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <div className="text-white">
                {getGovernmentIcon(data.jurisdiction.government_level.name)}
              </div>
              <div>
                <h1 className="text-4xl font-bold mb-2">{data.jurisdiction.name}</h1>
                <p className="text-xl text-gray-100">
                  {getJurisdictionTypeLabel(data.jurisdiction.jurisdiction_type)}
                </p>
                <p className="text-gray-200 mt-2">
                  {data.jurisdiction.government_level.name} Government
                  {data.jurisdiction.province && ` • ${data.jurisdiction.province}`}
                </p>
              </div>
            </div>
            
            {/* Quick Stats */}
            <div className="text-right">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-2xl font-bold">{data.stats.total_representatives.toLocaleString()}</div>
                  <div className="text-gray-200 text-sm">Representatives</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">{data.stats.total_bills.toLocaleString()}</div>
                  <div className="text-gray-200 text-sm">Bills</div>
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
              { id: 'representatives', label: 'Representatives' },
              { id: 'bills', label: 'Bills & Legislation' },
              { id: 'votes', label: 'Votes & Decisions' },
              { id: 'offices', label: 'Offices & Contact' }
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
            {/* Jurisdiction Information */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Jurisdiction Information</h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Basic Details</h3>
                  <div className="space-y-2 text-sm text-gray-600">
                    <p><span className="font-medium">Code:</span> {data.jurisdiction.code}</p>
                    <p><span className="font-medium">Type:</span> {getJurisdictionTypeLabel(data.jurisdiction.jurisdiction_type)}</p>
                    <p><span className="font-medium">Government Level:</span> {data.jurisdiction.government_level.name}</p>
                    {data.jurisdiction.province && (
                      <p><span className="font-medium">Province/Territory:</span> {data.jurisdiction.province}</p>
                    )}
                    <p><span className="font-medium">Created:</span> {new Date(data.jurisdiction.created_at).toLocaleDateString()}</p>
                    <p><span className="font-medium">Last Updated:</span> {new Date(data.jurisdiction.updated_at).toLocaleDateString()}</p>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Contact & Resources</h3>
                  {data.jurisdiction.website ? (
                    <a
                      href={data.jurisdiction.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-2 text-op-blue hover:text-blue-700 mb-3"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      <span>Official Website</span>
                    </a>
                  ) : (
                    <p className="text-gray-500 text-sm">No official website available</p>
                  )}
                  
                  {data.jurisdiction.extras && Object.keys(data.jurisdiction.extras).length > 0 && (
                    <div className="mt-4">
                      <h4 className="font-medium text-gray-700 mb-2">Additional Information</h4>
                      <pre className="whitespace-pre-wrap bg-gray-50 p-3 rounded text-xs text-gray-600">
                        {JSON.stringify(data.jurisdiction.extras, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Statistics Overview */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Statistics Overview</h2>
              <div className="grid md:grid-cols-4 gap-6">
                <div className="text-center p-6 bg-blue-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600 mb-2">{data.stats.total_representatives.toLocaleString()}</div>
                  <div className="text-blue-800 font-medium">Representatives</div>
                  <p className="text-blue-600 text-sm mt-1">Elected officials</p>
                </div>
                
                <div className="text-center p-6 bg-green-50 rounded-lg">
                  <div className="text-3xl font-bold text-green-600 mb-2">{data.stats.total_bills.toLocaleString()}</div>
                  <div className="text-green-800 font-medium">Bills</div>
                  <p className="text-blue-600 text-sm mt-1">Legislation</p>
                </div>
                
                <div className="text-center p-6 bg-purple-50 rounded-lg">
                  <div className="text-3xl font-bold text-purple-600 mb-2">{data.stats.total_votes.toLocaleString()}</div>
                  <div className="text-purple-800 font-medium">Votes</div>
                  <p className="text-purple-600 text-sm mt-1">Decisions recorded</p>
                </div>
                
                <div className="text-center p-6 bg-orange-50 rounded-lg">
                  <div className="text-3xl font-bold text-orange-600 mb-2">{data.stats.total_offices.toLocaleString()}</div>
                  <div className="text-orange-800 font-medium">Offices</div>
                  <p className="text-orange-600 text-sm mt-1">Contact locations</p>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Recent Representatives */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Representatives</h3>
                  <Link href={`/government/jurisdictions/${jurisdictionId}?tab=representatives`} className="text-op-blue hover:text-blue-700 text-sm">
                    View All →
                  </Link>
                </div>
                <div className="space-y-3">
                  {data.representatives.items.slice(0, 5).map((rep) => (
                    <div key={rep.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                      <div className="w-10 h-10 bg-op-blue bg-opacity-10 rounded-full flex items-center justify-center">
                        <span className="text-op-blue font-medium text-sm">
                          {rep.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                        </span>
                      </div>
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 text-sm">{rep.name}</h4>
                        <p className="text-gray-600 text-xs">{rep.position?.toUpperCase()} • {rep.party || 'Independent'}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Bills */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Bills</h3>
                  <Link href={`/government/jurisdictions/${jurisdictionId}?tab=bills`} className="text-op-blue hover:text-blue-700 text-sm">
                    View All →
                  </Link>
                </div>
                <div className="space-y-3">
                  {data.recentBills.items.slice(0, 5).map((bill) => (
                    <div key={bill.id} className="border-l-4 border-op-blue pl-4">
                      <h4 className="font-medium text-gray-900 text-sm">{bill.bill_number}</h4>
                      <p className="text-gray-600 text-xs line-clamp-2">{bill.title}</p>
                      <p className="text-gray-500 text-xs mt-1">Status: {bill.status}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'representatives' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Representatives</h2>
            <div className="space-y-4">
              {data.representatives.items.map((rep) => (
                <div key={rep.id} className="border border-gray-200 rounded-lg p-4 hover:border-op-blue transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-op-blue bg-opacity-10 rounded-full flex items-center justify-center">
                        <span className="text-op-blue font-medium">
                          {rep.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                        </span>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{rep.name}</h3>
                        <p className="text-gray-600">{rep.position?.toUpperCase()} • {rep.party || 'Independent'}</p>
                        {rep.riding && <p className="text-gray-500 text-sm">{rep.riding}</p>}
                      </div>
                    </div>
                    <div className="text-right text-sm text-gray-500">
                      {rep.email && <p>📧 {rep.email}</p>}
                      {rep.phone && <p>📞 {rep.phone}</p>}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {data.representatives.pagination.total_pages > 1 && (
              <div className="mt-6">
                <Pagination 
                  currentPage={data.representatives.pagination.page}
                  totalPages={data.representatives.pagination.total_pages}
                  baseUrl={`/government/jurisdictions/${id}`}
                  queryParams={{}}
                />
              </div>
            )}
          </div>
        )}

        {activeTab === 'bills' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Bills & Legislation</h2>
            <div className="space-y-4">
              {data.recentBills.items.map((bill) => (
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
                        {bill.sponsor && (
                          <span>Sponsor: {bill.sponsor.name}</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'votes' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Votes & Decisions</h2>
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              <p className="text-gray-500">Voting data for this jurisdiction will be displayed here</p>
              <p className="text-gray-400 text-sm mt-2">Coming soon with comprehensive vote tracking</p>
            </div>
          </div>
        )}

        {activeTab === 'offices' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Offices & Contact Information</h2>
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <p className="text-gray-500">Office and contact information will be displayed here</p>
              <p className="text-gray-400 text-sm mt-2">Coming soon with location and contact details</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
