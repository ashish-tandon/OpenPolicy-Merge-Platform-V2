import { Suspense } from 'react';
import { api } from '@/lib/api';
import BillsList from '@/components/Bills/BillsList';
import BillsFilters from '@/components/Bills/BillsFilters';
import LoadingSpinner from '@/components/LoadingSpinner';

interface BillsPageProps {
  searchParams: {
    page?: string;
    search?: string;
    session?: string;
    type?: string;
    status?: string;
  };
}

export default async function BillsPage({ searchParams }: BillsPageProps) {
  const page = parseInt(searchParams.page || '1');
  const filters = {
    page,
    search: searchParams.search,
    session: searchParams.session,
    privatemember: searchParams.type === 'private',
  };

  const billsData = await api.getBills(filters);

  return (
    <div className="content-container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Bills & Legislation
        </h1>
        <p className="text-gray-600">
          Track federal legislation through the parliamentary process
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Filters Sidebar */}
        <div className="lg:col-span-1">
          <BillsFilters currentFilters={searchParams} />
        </div>

        {/* Bills List */}
        <div className="lg:col-span-3">
          <Suspense fallback={<LoadingSpinner />}>
            <BillsList 
              bills={billsData.results || []} 
              totalCount={billsData.count || 0}
              currentPage={page}
              filters={filters}
            />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
