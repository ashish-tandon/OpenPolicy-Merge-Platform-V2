import { Suspense } from 'react';
import { api } from '@/lib/api';
import SearchResults from '@/components/Search/SearchResults';
import SearchFilters from '@/components/Search/SearchFilters';
import LoadingSpinner from '@/components/LoadingSpinner';

interface SearchPageProps {
  searchParams: {
    q?: string;
    type?: string;
    page?: string;
  };
}

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const query = searchParams.q || '';
  const type = searchParams.type || 'all';
  const page = parseInt(searchParams.page || '1');

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
    <div className=""rdquo;content-container py-8""rdquo;>
      <div className=""rdquo;mb-8""rdquo;>
        <h1 className=""rdquo;text-3xl font-bold text-op-dark mb-2""rdquo;>
          Search OpenParliament
        </h1>
        {query && (
          <p className=""rdquo;text-gray-600""rdquo;>
            {searchResults?.count || 0} results for ""rdquo;{query}""rdquo;
          </p>
        )}
      </div>

      <div className=""rdquo;grid grid-cols-1 lg:grid-cols-4 gap-8""rdquo;>
        {/* Filters Sidebar */}
        <div className=""rdquo;lg:col-span-1""rdquo;>
          <SearchFilters 
            currentQuery={query} 
            currentType={type} 
          />
        </div>

        {/* Search Results */}
        <div className=""rdquo;lg:col-span-3""rdquo;>
          {!query ? (
            <div className=""rdquo;bg-white rounded-lg shadow p-8 text-center""rdquo;>
              <svg className=""rdquo;w-16 h-16 mx-auto text-gray-400 mb-4""rdquo; fill=""rdquo;none""rdquo; stroke=""rdquo;currentColor""rdquo; viewBox=""rdquo;0 0 24 24""rdquo;>
                <path strokeLinecap=""rdquo;round""rdquo; strokeLinejoin=""rdquo;round""rdquo; strokeWidth={2} d=""rdquo;M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z""rdquo; />
              </svg>
              <h2 className=""rdquo;text-xl font-medium text-gray-700 mb-2""rdquo;>
                What are you looking for?
              </h2>
              <p className=""rdquo;text-gray-500 mb-6""rdquo;>
                Search for MPs, bills, debates, committees, or any topic across parliamentary records.
              </p>
              <div className=""rdquo;space-y-2 text-sm""rdquo;>
                <p className=""rdquo;text-gray-600""rdquo;>Try searching for:</p>
                <div className=""rdquo;flex flex-wrap justify-center gap-2""rdquo;>
                  <a href=""rdquo;/search?q=climate change""rdquo; className=""rdquo;px-3 py-1 bg-gray-100 rounded hover:bg-gray-200""rdquo;>
                    climate change
                  </a>
                  <a href=""rdquo;/search?q=Bill C-5""rdquo; className=""rdquo;px-3 py-1 bg-gray-100 rounded hover:bg-gray-200""rdquo;>
                    Bill C-5
                  </a>
                  <a href=""rdquo;/search?q=Justin Trudeau""rdquo; className=""rdquo;px-3 py-1 bg-gray-100 rounded hover:bg-gray-200""rdquo;>
                    Justin Trudeau
                  </a>
                  <a href=""rdquo;/search?q=healthcare""rdquo; className=""rdquo;px-3 py-1 bg-gray-100 rounded hover:bg-gray-200""rdquo;>
                    healthcare
                  </a>
                </div>
              </div>
            </div>
          ) : error ? (
            <div className=""rdquo;bg-red-50 border border-red-200 rounded-lg p-4""rdquo;>
              <p className=""rdquo;text-red-800""rdquo;>{error}</p>
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
