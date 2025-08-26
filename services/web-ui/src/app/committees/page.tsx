import { Suspense } from 'react';
import { api } from '@/lib/api';
import CommitteesList from '@/components/Committees/CommitteesList';
import CommitteesFilters from '@/components/Committees/CommitteesFilters';
import LoadingSpinner from '@/components/LoadingSpinner';

interface CommitteesPageProps {
  searchParams: Promise<{
    page?: string;
    search?: string;
    type?: string;
    active?: string;
  }>;
}

export default async function CommitteesPage({ searchParams }: CommitteesPageProps) {
  const params = await searchParams;

  const page = parseInt(params.page || '1');
  const filters = {
    page,
    search: params.search,
    type: params.type,
    active: params.active,
  };

  // Check if we're filtering or showing the default view
  const isFiltered = params.search || params.type || params.active || page > 1;

  // Fetch committees data
  const committeesData = await api.getCommittees({
    page: page.toString(),
    page_size: isFiltered ? '20' : '100', // Get all for unfiltered view
    q: filters.search,
  });

  // Fetch recent studies for the main page
  const recentStudies = !isFiltered 
    ? await api.getCommitteeStudies({ page: '1', page_size: '12' }).catch(() => ({ items: [] }))
    : null;

  return (
    <div className="content-container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Parliamentary Committees
        </h1>
        <p className="text-gray-600">
          Standing, special, and joint committees conducting studies and reviewing legislation
        </p>
      </div>

      {!isFiltered ? (
        // Default view - Show current committees and recent studies
        <div className="space-y-8">
          {/* Current Committees */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                <h2 className="text-xl font-bold text-op-dark">Current committees</h2>
              </div>
              <div className="lg:col-span-3">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {(committeesData.items || []).map((committee: any) => (
                    <div key={committee.id}>
                      <a 
                        href={`/committees/${committee.slug || committee.id}`}
                        className="text-op-blue hover:underline"
                      >
                        {committee.name}
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Recent Studies */}
          {recentStudies && recentStudies.items && recentStudies.items.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                <div className="lg:col-span-1">
                  <h2 className="text-xl font-bold text-op-dark">Recent studies</h2>
                </div>
                <div className="lg:col-span-3">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {recentStudies.items.map((study: any) => (
                      <div key={study.id} className="text-sm line-clamp-2">
                        <a 
                          href={`/committees/${study.committee_slug}/studies/${study.id}`}
                          className="text-op-blue hover:underline"
                          title={study.name}
                        >
                          {study.name}
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        // Filtered view - Show list with sidebar
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <CommitteesFilters currentFilters={params} />
          </div>

          {/* Committees List */}
          <div className="lg:col-span-3">
            <Suspense fallback={<LoadingSpinner />}>
              <CommitteesList 
                committees={committeesData.items || []} 
                totalCount={committeesData.pagination?.total || 0}
                currentPage={page}
                filters={filters}
              />
            </Suspense>
          </div>
        </div>
      )}
    </div>
  );
}
