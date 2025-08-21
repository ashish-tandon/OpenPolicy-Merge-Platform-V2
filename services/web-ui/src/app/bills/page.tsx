import { Suspense } from 'react';
import { api } from '@/lib/api';
import BillsList from '@/components/Bills/BillsList';
import BillsFilters from '@/components/Bills/BillsFilters';
import LoadingSpinner from '@/components/LoadingSpinner';

interface BillsPageProps {
  searchParams: Promise<{
    page?: string;
    search?: string;
    session?: string;
    type?: string;
    status?: string;
  }>;
}

export default async function BillsPage({ searchParams }: BillsPageProps) {
  const params = await searchParams;

  const page = parseInt(params.page || '1');
  const filters = {
    page,
    search: params.search,
    session: params.session,
    privatemember: params.type === 'private',
  };

  const billsData = await api.getBills({
    page: page.toString(),
    page_size: '20',
    q: filters.search,
    session: filters.session,
    privatemember: filters.privatemember ? 'true' : undefined,
  });

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
              bills={billsData.bills || []} 
              currentPage={page}
              totalPages={billsData.pagination?.pages || 1}
            />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
