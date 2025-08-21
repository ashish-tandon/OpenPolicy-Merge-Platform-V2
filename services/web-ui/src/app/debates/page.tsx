import { Suspense } from 'react';
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

  const debatesData = await api.getDebates({
    page: page.toString(),
    page_size: '20',
    date_gte: params.date_gte,
    date_lte: params.date_lte,
    q: params.search,
  });

  return (
    <div className="content-container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Debates & Hansard
        </h1>
        <p className="text-gray-600">
          Official transcripts of House proceedings dating back to 1994
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Filters Sidebar */}
        <div className="lg:col-span-1">
          <DebatesFilters currentFilters={searchParams} />
        </div>

        {/* Debates List */}
        <div className="lg:col-span-3">
          <Suspense fallback={<LoadingSpinner />}>
            <DebatesList
              debates={debatesData.debates || []}
              totalCount={debatesData.pagination?.total || 0}
              currentPage={page}
              filters={filters}
            />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
