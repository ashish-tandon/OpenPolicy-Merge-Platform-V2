import { Suspense } from 'react';
import { api } from '@/lib/api';
import SearchFilters from '@/components/Search/SearchFilters';
import SearchResults from '@/components/Search/SearchResults';
import LoadingSpinner from '@/components/LoadingSpinner';

interface SearchPageProps {
  searchParams: {
    q?: string;
    type?: string;
    page?: string;
  };
}

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const params = await searchParams;

  const query = params.q || '';
  const type = params.type || 'all';
  const page = parseInt(params.page || '1');

  let searchResults = null;
  let error = null;

  if (query) {
    try {
      searchResults = await api.search(query, { page, type: type !== 'all' ? type : undefined });
    } catch (_e) {
      error = 'Failed to perform search. Please try again.';
    }
  }

  return (
    <div className="content-container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Search OpenParliament
        </h1>
        {query && (
          <p className="text-gray-600">
            {searchResults?.count || 0} results for "{query}"
          </p>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Filters Sidebar */}
        <div className="lg:col-span-1">
          <SearchFilters 
            currentQuery={query} 
            currentType={type} 
          />
        </div>

        {/* Search Results */}
        <div className="lg:col-span-3">
          {!query ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <h2 className="text-xl font-medium text-gray-700 mb-2">
                What are you looking for?
              </h2>
              <p className="text-gray-500 mb-6">
                Search for MPs, bills, debates, committees, or any topic across parliamentary records.
              </p>
              <div className="space-y-2 text-sm">
                <p className="text-gray-600">Try searching for:</p>
                <div className="flex flex-wrap justify-center gap-2">
                  <a href="/search?q=climate change" className="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200">
                    climate change
                  </a>
                  <a href="/search?q=Bill C-5" className="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200">
                    Bill C-5
                  </a>
                  <a href="/search?q=Justin Trudeau" className="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200">
                    Justin Trudeau
                  </a>
                  <a href="/search?q=healthcare" className="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200">
                    healthcare
                  </a>
                </div>
              </div>
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800">{error}</p>
            </div>
          ) : (
            <Suspense fallback={<LoadingSpinner />}>
              <SearchResults 
                results={searchResults?.results || []} 
                totalCount={searchResults?.count || 0}
                currentPage={page}
                query={query}
                type={type}
              />
            </Suspense>
          )}
        </div>
      </div>
    </div>
  );
}
