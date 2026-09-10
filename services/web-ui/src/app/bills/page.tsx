import { Suspense } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import BillsList from '@/components/Bills/BillsList';
import BillsFilters from '@/components/Bills/BillsFilters';
import LoadingSpinner from '@/components/LoadingSpinner';
import RecentVotes from '@/components/RecentVotes';
import RecentBills from '@/components/RecentBills';

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

  // Fetch bills, recent votes, and recently debated bills
  const [billsData, recentVotes, recentlyDebated] = await Promise.all([
    api.getBills({
      page: page.toString(),
      page_size: '20',
      q: filters.search,
      session: filters.session,
      privatemember: filters.privatemember ? 'true' : undefined,
    }),
    // Using bills as placeholder for votes (votes API needs to be enabled)
    api.getBills({ page: '1', page_size: '6' }).catch(() => ({ items: [] })),
    // Fetch recently debated bills
    api.getBills({ page: '1', page_size: '8' }).catch(() => ({ items: [] })),
  ]);

  return (
    <div className="content-container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Bills & Legislation
        </h1>
        <p className="text-gray-600">
          Track federal legislation through the parliamentary process
        </p>
        <Link 
          href="/rss/bills" 
          className="inline-flex items-center text-sm text-op-blue hover:underline mt-2"
        >
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path d="M5 3a1 1 0 000 2c5.523 0 10 4.477 10 10a1 1 0 102 0C17 8.373 11.627 3 5 3z"></path>
            <path d="M4 9a1 1 0 011-1 7 7 0 017 7 1 1 0 11-2 0 5 5 0 00-5-5 1 1 0 01-1-1zM3 15a2 2 0 114 0 2 2 0 01-4 0z"></path>
          </svg>
          RSS Feed
        </Link>
      </div>

      {/* Recent Votes Section */}
      {recentVotes.items && recentVotes.items.length > 0 && (
        <div className="mb-8 bg-white rounded-lg shadow p-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-1">
              <h2 className="text-xl font-bold text-op-dark">Recent votes</h2>
            </div>
            <div className="lg:col-span-3">
              <RecentVotes votes={recentVotes.items} />
              <Link href="/voting-records" className="text-sm text-op-blue hover:underline mt-4 inline-block">
                See all votes for this session →
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Recently Debated Bills Section */}
      {recentlyDebated.items && recentlyDebated.items.length > 0 && (
        <div className="mb-8 bg-white rounded-lg shadow p-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-1">
              <h2 className="text-xl font-bold text-op-dark">Recently debated bills</h2>
            </div>
            <div className="lg:col-span-3">
              <RecentBills bills={recentlyDebated.items} />
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Filters Sidebar */}
        <div className="lg:col-span-1">
          <BillsFilters currentFilters={params} />
        </div>

        {/* Bills List */}
        <div className="lg:col-span-3">
          <Suspense fallback={<LoadingSpinner />}>
            <BillsList 
              bills={billsData.items || []} 
              currentPage={page}
              totalPages={billsData.pagination?.total_pages || 1}
            />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
