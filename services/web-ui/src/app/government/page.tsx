'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { GovernmentLevel, SystemStats } from '@/types/government';
import LoadingSpinner from '@/components/LoadingSpinner';
import { FederalIcon, ProvincialIcon, MunicipalIcon } from '@/components/Government/GovernmentIcons';

interface GovernmentPageData {
  levels: GovernmentLevel[];
  stats: SystemStats;
}

export default function GovernmentPage() {
  const [data, setData] = useState<GovernmentPageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [levelsResponse, statsResponse] = await Promise.all([
          fetch('/api/v1/multi-level-government/government-levels'),
          fetch('/api/v1/multi-level-government/stats/system')
        ]);

        if (!levelsResponse.ok || !statsResponse.ok) {
          throw new Error('Failed to fetch government data');
        }

        const [levelsData, statsData] = await Promise.all([
          levelsResponse.json(),
          statsResponse.json()
        ]);

        setData({
          levels: levelsData.items,
          stats: statsData
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load government data');
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
            <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Government Data</h2>
            <p className="text-red-600">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  const getGovernmentIcon = (levelName: string) => {
    switch (levelName.toLowerCase()) {
      case 'federal':
        return <FederalIcon className="w-16 h-16" />;
      case 'provincial':
        return <ProvincialIcon className="w-16 h-16" />;
      case 'municipal':
        return <MunicipalIcon className="w-16 h-16" />;
      default:
        return <div className="w-16 h-16 bg-gray-200 rounded-full" />;
    }
  };

  const getGovernmentDescription = (levelName: string) => {
    switch (levelName.toLowerCase()) {
      case 'federal':
        return 'Parliament of Canada, federal MPs, bills, and votes';
      case 'provincial':
        return 'Provincial and territorial legislatures across Canada';
      case 'municipal':
        return 'City councils, mayors, and municipal governments';
      default:
        return 'Government level information';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-op-blue to-blue-700 text-white">
        <div className="content-container py-16">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              Canadian Government Data
            </h1>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
              Explore comprehensive data from all levels of Canadian government - 
              federal, provincial, and municipal. Track representatives, bills, votes, and more.
            </p>
            
            {/* Quick Stats */}
            {data?.stats && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-100">{data.stats.total_representatives.toLocaleString()}</div>
                  <div className="text-blue-200">Representatives</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-100">{data.stats.total_bills.toLocaleString()}</div>
                  <div className="text-blue-200">Bills</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-100">{data.stats.total_jurisdictions.toLocaleString()}</div>
                  <div className="text-blue-200">Jurisdictions</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-100">{data.stats.total_votes.toLocaleString()}</div>
                  <div className="text-blue-200">Votes</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Government Levels Grid */}
      <div className="content-container py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Explore by Government Level
          </h2>
          <p className="text-lg text-gray-600">
            Navigate through Canada's apos;s three levels of government
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {data?.levels?.map((level) => (
            <Link
              key={level.id}
              href={`/government/${level.name.toLowerCase()}`}
              className="group bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-gray-200 hover:border-op-blue"
            >
              <div className="text-center">
                <div className="flex justify-center mb-6 text-op-blue group-hover:text-blue-600 transition-colors">
                  {getGovernmentIcon(level.name)}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-op-blue transition-colors">
                  {level.name}
                </h3>
                <p className="text-gray-600 mb-6">
                  {getGovernmentDescription(level.name)}
                </p>
                <div className="flex justify-center">
                  <span className="inline-flex items-center px-4 py-2 bg-op-blue text-white rounded-lg group-hover:bg-blue-600 transition-colors">
                    Explore {level.name}
                    <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Quick Access Section */}
      <div className="bg-white border-t border-gray-200">
        <div className="content-container py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Quick Access
            </h2>
            <p className="text-lg text-gray-600">
              Jump directly to specific data types across all government levels
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Link
              href="/government/representatives"
              className="group bg-gray-50 rounded-lg p-6 hover:bg-op-blue hover:text-white transition-all duration-300"
            >
              <div className="text-center">
                <svg className="w-12 h-12 mx-auto mb-4 text-op-blue group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <h3 className="font-semibold mb-2">All Representatives</h3>
                <p className="text-sm text-gray-600 group-hover:text-blue-100">MPs, MLAs, mayors, and councillors</p>
              </div>
            </Link>

            <Link
              href="/government/bills"
              className="group bg-gray-50 rounded-lg p-6 hover:bg-op-blue hover:text-white transition-all duration-300"
            >
              <div className="text-center">
                <svg className="w-12 h-12 mx-auto mb-4 text-op-blue group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="font-semibold mb-2">All Bills</h3>
                <p className="text-sm text-gray-600 group-hover:text-blue-100">Legislation across all levels</p>
              </div>
            </Link>

            <Link
              href="/government/votes"
              className="group bg-gray-50 rounded-lg p-6 hover:bg-op-blue hover:text-white transition-all duration-300"
            >
              <div className="text-center">
                <svg className="w-12 h-12 mx-auto mb-4 text-op-blue group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                <h3 className="font-semibold mb-2">All Votes</h3>
                <p className="text-sm text-gray-600 group-hover:text-blue-100">Voting records and patterns</p>
              </div>
            </Link>

            <Link
              href="/government/jurisdictions"
              className="group bg-gray-50 rounded-lg p-6 hover:bg-op-blue hover:text-white transition-all duration-300"
            >
              <div className="text-center">
                <svg className="w-12 h-12 mx-auto mb-4 text-op-blue group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <h3 className="font-semibold mb-2">All Jurisdictions</h3>
                <p className="text-sm text-gray-600 group-hover:text-blue-100">Federal, provincial, and municipal</p>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Data Sources Section */}
      <div className="bg-gray-50 border-t border-gray-200">
        <div className="content-container py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Data Sources & Transparency
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Our data comes from official government sources across Canada. 
              We track and maintain transparency about where every piece of information originates.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-op-blue rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Real-time Updates</h3>
              <p className="text-gray-600">
                Data is refreshed regularly from official government APIs and sources
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-op-blue rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Verified Sources</h3>
              <p className="text-gray-600">
                All data is sourced directly from official government websites and databases
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-op-blue rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Full Transparency</h3>
              <p className="text-gray-600">
                View detailed information about data sources, update schedules, and methodology
              </p>
            </div>
          </div>

          <div className="text-center mt-12">
            <Link
              href="/government/data-sources"
              className="inline-flex items-center px-6 py-3 bg-op-blue text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              View All Data Sources
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
