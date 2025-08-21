import { Suspense } from 'react';
import { api } from '@/lib/api';
import MPList from '@/components/MPs/MPList';
import MPFilters from '@/components/MPs/MPFilters';
import LoadingSpinner from '@/components/LoadingSpinner';

interface MPsPageProps {
  searchParams: Promise<{
    page?: string;
    search?: string;
    province?: string;
    party?: string;
    current?: string;
  }>;
}

export default async function MPsPage({ searchParams }: MPsPageProps) {
  const params = await searchParams;

  const page = parseInt(params.page || '1');
  const filters = {
    page,
    search: params.search,
    province: params.province,
    party: params.party,
    current: params.current === 'false' ? false : true,
  };

  const mpsData = await api.getMembers({
    page: page.toString(),
    page_size: '20',
    q: filters.search,
    province: filters.province,
    party: filters.party,
    current: filters.current ? 'true' : 'false',
  });

  return (
    <div className="content-container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Members of Parliament
        </h1>
        <p className="text-gray-600">
          Browse and search through {filters.current ? 'current' : 'former'} MPs
        </p>
      </div>
      
      <div className="grid lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1">
          <MPFilters initialFilters={filters} />
        </div>
        
        <div className="lg:col-span-3">
          <Suspense fallback={<LoadingSpinner />}>
            <MPList 
              members={mpsData.results}
              pagination={{
                page: mpsData.page,
                pageSize: mpsData.pageSize,
                total: mpsData.total,
                totalPages: mpsData.totalPages,
              }}
              filters={filters}
            />
          </Suspense>
        </div>
      </div>
    </div>
  );
}