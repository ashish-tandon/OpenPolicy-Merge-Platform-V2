import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import BillDetail from '@/components/Bills/BillDetail';
import BillVotes from '@/components/Bills/BillVotes';
import BillHistory from '@/components/Bills/BillHistory';
import { Metadata } from 'next';

interface BillDetailPageProps {
  params: Promise<{
    id: string;
  }>;
}

export async function generateMetadata({ params }: BillDetailPageProps): Promise<Metadata> {
  const { id } = await params;
  try {
    const bill = await api.getBill(id);
    
    return {
      title: `${bill.title} | OpenPolicy`,
      description: bill.summary || `Details about ${bill.title}`,
      openGraph: {
        title: bill.title,
        description: bill.summary || `Details about ${bill.title}`,
        type: 'website',
      },
    };
  } catch (_error) {
    return {
      title: 'Bill Details | OpenPolicy',
      description: 'View detailed information about parliamentary bills',
    };
  }
}

export default async function BillDetailPage({ params }: BillDetailPageProps) {
  const { id } = await params;
  try {
    // Fetch bill data
    const [bill, votes, history] = await Promise.all([
      api.getBill(id),
      api.getBillVotes(id).catch(() => ({ results: [] })),
      api.getBillHistory(id).catch(() => ({ results: [] })),
    ]);

    return (
      <div className="content-container py-8">
        {/* Breadcrumb Navigation */}
        <nav className="mb-6">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li>
              <Link href="/bills" className="hover:text-op-blue transition-colors">
                Bills
              </Link>
            </li>
            <li className="text-gray-400">/</li>
            <li className="text-gray-900 font-medium">{bill.title}</li>
          </ol>
        </nav>

        {/* Main Bill Information */}
        <BillDetail bill={bill} />

        {/* Bill Votes Section */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Voting Record</h2>
          <BillVotes votes={votes.results} billId={id} />
        </div>

        {/* Bill History Section */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Bill History</h2>
          <BillHistory history={history.results} />
        </div>
      </div>
    );
  } catch (_error) {
    console.error('Error loading bill details:', error);
    notFound();
  }
}
