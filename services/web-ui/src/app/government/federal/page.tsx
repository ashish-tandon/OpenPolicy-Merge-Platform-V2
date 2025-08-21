'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { GovernmentLevelStats, PaginatedResponse, Representative, Bill, Jurisdiction } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import { FederalIcon } from '@/components/Government/GovernmentIcons';
import Pagination from '@/components/Pagination';

interface FederalPageData {
  stats: GovernmentLevelStats;
  jurisdictions: PaginatedResponse<Jurisdiction>;
  representatives: PaginatedResponse<Representative>;
  recentBills: PaginatedResponse<Bill>;
}

export default function FederalPage() {
  const [data, setData] = useState<FederalPageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'representatives' | 'bills' | 'votes'>('overview');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // First get the federal government level ID
        const levelsResponse = await fetch('/api/v1/multi-level-government/government-levels');
        const levelsData = await levelsResponse.json();
        const federalLevel = levelsData.items.find((level: any) => level.name.toLowerCase() === 'federal');
        
        if (!federalLevel) {
          throw new Error('Federal government level not found');
        }

        const [statsResponse, jurisdictionsResponse, representativesResponse, billsResponse] = await Promise.all([
          fetch(`/api/v1/multi-level-government/stats/government-levels/${federalLevel.id}`),
          fetch(`/api/v1/multi-level-government/jurisdictions?government_level=${federalLevel.id}&page_size=10`),
          fetch(`/api/v1/multi-level-government/representatives?government_level=${federalLevel.id}&page_size=10`),
          fetch(`/api/v1/multi-level-government/bills?government_level=${federalLevel.id}&page_size=10`)
        ]);

        if (!statsResponse.ok || !jurisdictionsResponse.ok || !representativesResponse.ok || !billsResponse.ok) {
          throw new Error('Failed to fetch federal data');
        }

        const [statsData, jurisdictionsData, representativesData, billsData] = await Promise.all([
          statsResponse.json(),
          jurisdictionsResponse.json(),
          representativesResponse.json(),
          billsResponse.json()
        ]);

        setData({
          stats: statsData,
          jurisdictions: jurisdictionsData,
          representatives: representativesData,
          recentBills: billsData
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load federal data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="content-container py-12">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="content-container py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Federal Data</h2>
            <p className="text-red-600">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Federal Header */}
      <div className="bg-gradient-to-br from-red-600 to-red-700 text-white">
        <div className="content-container py-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <FederalIcon className="w-20 h-20 text-red-100" />
              <div>
                <h1 className="text-4xl font-bold mb-2">Federal Government</h1>
                <p className="text-xl text-red-100">Parliament of Canada</p>
                <p className="text-red-200 mt-2">
                  House of Commons • Senate • Governor General
                </p>
              </div>
            </div>
            
            {/* Quick Stats */}
            {data?.stats && (
              <div className="text-right">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-2xl font-bold">{data.stats.total_representatives.toLocaleString()}</div>
                    <div className="text-red-200 text-sm">MPs & Senators</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{data.stats.total_bills.toLocaleString()}</div>
                    <div className="text-red-200 text-sm">Bills</div>
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
              { id: 'representatives', label: 'MPs & Senators' },
              { id: 'bills', label: 'Bills & Legislation' },
              { id: 'votes', label: 'Votes & Decisions' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-2 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-red-500 text-red-600'
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
            {/* Federal Institutions */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Federal Institutions</h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center p-6 bg-red-50 rounded-lg">
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">House of Commons</h3>
                  <p className="text-gray-600 text-sm">338 elected Members of Parliament</p>
                </div>

                <div className="text-center p-6 bg-red-50 rounded-lg">
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Senate</h3>
                  <p className="text-gray-600 text-sm">105 appointed Senators</p>
                </div>

                <div className="text-center p-6 bg-red-50 rounded-lg">
                  <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Governor General</h3>
                  <p className="text-gray-600 text-sm">Crown representative</p>
                </div>
              </div>
            </div>

            {/* Recent Federal Activity */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Recent Bills */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Bills</h3>
                  <Link href="/government/federal/bills" className="text-red-600 hover:text-red-700 text-sm">
                    View All →
                  </Link>
                </div>
                <div className="space-y-3">
                  {data?.recentBills.items.slice(0, 5).map((bill) => (
                    <div key={bill.id} className="border-l-4 border-red-200 pl-4">
                      <h4 className="font-medium text-gray-900 text-sm">{bill.bill_number}</h4>
                      <p className="text-gray-600 text-sm line-clamp-2">{bill.title}</p>
                      <p className="text-gray-500 text-xs mt-1">Status: {bill.status}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Key Federal MPs */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Key Federal Representatives</h3>
                  <Link href="/government/federal/representatives" className="text-red-600 hover:text-red-700 text-sm">
                    View All →
                  </Link>
                </div>
                <div className="space-y-3">
                  {data?.representatives.items.slice(0, 5).map((rep) => (
                    <div key={rep.id} className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                        <span className="text-red-600 font-medium text-sm">
                          {rep.name.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 text-sm">{rep.name}</h4>
                        <p className="text-gray-600 text-xs">{rep.position?.toUpperCase()} • {rep.party}</p>
                        <p className="text-gray-500 text-xs">{rep.riding}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'representatives' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Federal Representatives</h2>
            <div className="space-y-4">
              {data?.representatives.items.map((rep) => (
                <div key={rep.id} className="border border-gray-200 rounded-lg p-4 hover:border-red-300 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                        <span className="text-red-600 font-medium">
                          {rep.name.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{rep.name}</h3>
                        <p className="text-gray-600">{rep.position?.toUpperCase()} • {rep.party}</p>
                        <p className="text-gray-500 text-sm">{rep.riding}</p>
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
            
            {data?.representatives.pagination && (
              <div className="mt-6">
                <Pagination 
                  currentPage={data.representatives.pagination.page}
                  totalPages={data.representatives.pagination.total_pages}
                  baseUrl="/government/federal"
                  queryParams={{}}
                />
              </div>
            )}
          </div>
        )}

        {activeTab === 'bills' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Federal Bills & Legislation</h2>
            <div className="space-y-4">
              {data?.recentBills.items.map((bill) => (
                <div key={bill.id} className="border border-gray-200 rounded-lg p-4 hover:border-red-300 transition-colors">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm font-medium">
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
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Federal Votes & Decisions</h2>
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              <p className="text-gray-500">Federal voting data will be displayed here</p>
              <p className="text-gray-400 text-sm mt-2">Coming soon with full vote tracking</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
