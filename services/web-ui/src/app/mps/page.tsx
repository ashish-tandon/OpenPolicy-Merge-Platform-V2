import { Suspense } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import MPList from '@/components/MPs/MPList';
import MPTileList from '@/components/MPs/MPTileList';
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
          {filters.current ? 'Current MPs' : 'Former MPs'}
        </h1>
        
        {/* Helpful text matching Django template */}
        <div className="bg-gray-50 rounded-lg p-4 mt-4">
          <p className="text-sm">
            <strong>Looking for your MP?</strong> Enter your postal code in the search field at the upper right of the page.{' '}
            <strong>Looking for an ex-Member?</strong> See our list of{' '}
            <Link href="/former-mps" className="text-op-blue hover:underline">
              former MPs
            </Link>{' '}
            (since 1994).
          </p>
        </div>
      </div>
      
      <div className="grid lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1">
          <MPFilters initialFilters={filters} />
        </div>
        
        <div className="lg:col-span-3">
          <Suspense fallback={<LoadingSpinner />}>
            {/* Use tile view for current MPs without filters */}
            {filters.current && !filters.search && !filters.party && !filters.province ? (
              <MPTileList 
                members={mpsData.results || []}
                pagination={{
                  page: mpsData.page || 1,
                  pageSize: mpsData.pageSize || 20,
                  total: mpsData.total || 0,
                  totalPages: mpsData.totalPages || 1,
                }}
                filters={filters}
              />
            ) : (
              <MPList 
                members={mpsData.results || []}
                totalCount={mpsData.total || 0}
                currentPage={page}
                filters={filters}
              />
            )}
          </Suspense>
        </div>
      </div>
    </div>
  );
}