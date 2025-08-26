import { Suspense } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import DebatesList from '@/components/Debates/DebatesList';
import DebatesFilters from '@/components/Debates/DebatesFilters';
import LoadingSpinner from '@/components/LoadingSpinner';

interface DebatesPageProps {
  searchParams: Promise<{
    page?: string;
    date_gte?: string;
    date_lte?: string;
    search?: string;
  }>;
}

export default async function DebatesPage({ searchParams }: DebatesPageProps) {
  const params = await searchParams;

  const page = parseInt(params.page || '1');
  const filters = {
    page,
    date_gte: params.date_gte,
    date_lte: params.date_lte,
  };

  // Check if we're filtering or just showing the default view
  const isFiltered = params.date_gte || params.date_lte || params.search || page > 1;

  // Fetch recent debates for the archive view
  const recentDebates = !isFiltered 
    ? await api.getDebates({ page: '1', page_size: '20' })
    : null;

  // Fetch debates with filters for the list view
  const debatesData = isFiltered 
    ? await api.getDebates({
        page: page.toString(),
        page_size: '20',
        date_gte: params.date_gte,
        date_lte: params.date_lte,
        q: params.search,
      })
    : null;

  // Generate list of years from current year back to 1994
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 1993 }, (_, i) => currentYear - i);

  return (
    <div className="content-container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Debates & Hansard
        </h1>
        <div className="bg-gray-50 rounded-lg p-4 mt-4">
          <p className="text-sm">
            When Parliament is in session, every word spoken by a member is faithfully transcribed, 
            and published in a document called a{' '}
            <a 
              href="https://en.wikipedia.org/wiki/Hansard" 
              className="text-op-blue hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Hansard
            </a>. We have the Hansards of the House of Commons dating back to 1994.
          </p>
        </div>
      </div>

      {!isFiltered ? (
        // Archive View - Show recent debates and year list
        <div className="space-y-8">
          {/* Recent Debates */}
          {recentDebates && recentDebates.debates && recentDebates.debates.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                <div className="lg:col-span-1">
                  <h2 className="text-xl font-bold text-op-dark">Recent</h2>
                </div>
                <div className="lg:col-span-3">
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                    {recentDebates.debates.map((debate: any) => (
                      <div key={debate.id} className="text-sm">
                        <Link 
                          href={`/debates/${debate.date}`}
                          className="text-op-blue hover:underline"
                        >
                          {new Date(debate.date).toLocaleDateString('en-CA', { 
                            month: 'long', 
                            day: 'numeric' 
                          })}
                        </Link>
                        {debate.most_frequent_word && (
                          <div className="mt-1">
                            <span 
                              className="text-xs text-gray-600 italic"
                              title="This is the word that came up the most, compared to other similar debates"
                            >
                              {debate.most_frequent_word}
                            </span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Past Years */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                <h2 className="text-xl font-bold text-op-dark">Past</h2>
              </div>
              <div className="lg:col-span-3">
                <div className="grid grid-cols-3 sm:grid-cols-5 md:grid-cols-6 gap-3">
                  {years.map(year => (
                    <div key={year} className="text-sm">
                      <Link 
                        href={`/debates/year/${year}`}
                        className="text-op-blue hover:underline"
                      >
                        {year}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Search Box */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-op-dark mb-4">Search Debates</h2>
            <form action="/debates" method="GET" className="relative">
              <input
                type="search"
                name="search"
                placeholder="Search debates by keyword, MP name, or topic"
                className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-transparent"
              />
              <button
                type="submit"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 text-gray-500 hover:text-op-blue"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      ) : (
        // Filtered View - Show debates list with sidebar filters
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <DebatesFilters currentFilters={params} />
          </div>

          {/* Debates List */}
          <div className="lg:col-span-3">
            <Suspense fallback={<LoadingSpinner />}>
              {debatesData && (
                <DebatesList
                  debates={debatesData.debates || []}
                  totalCount={debatesData.pagination?.total || 0}
                  currentPage={page}
                  filters={filters}
                />
              )}
            </Suspense>
          </div>
        </div>
      )}
    </div>
  );
}
