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
  };

  const committeesData = await api.getCommittees({
    page: page.toString(),
    page_size: '20',
    q: filters.search,
  });

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
    </div>
  );
}
