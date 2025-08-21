import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import BillDetail from '@/components/bills/BillDetail';
import BillVotes from '@/components/bills/BillVotes';
import BillHistory from '@/components/bills/BillHistory';
import { Metadata } from 'next';

interface BillDetailPageProps {
  params: {
    id: string;
  };
}

export async function generateMetadata({ params }: BillDetailPageProps): Promise<Metadata> {
  try {
    const bill = await api.getBill(params.id);
    
    return {
      title: `${bill.title} | OpenPolicy`,
      description: bill.description || `Details about ${bill.title}`,
      openGraph: {
        title: bill.title,
        description: bill.description || `Details about ${bill.title}`,
        type: 'website',
      },
    };
  } catch (error) {
    return {
      title: 'Bill Details | OpenPolicy',
      description: 'View detailed information about parliamentary bills',
    };
  }
}

export default async function BillDetailPage({ params }: BillDetailPageProps) {
  try {
    // Fetch bill data
    const [bill, votes, history] = await Promise.all([
      api.getBill(params.id),
      api.getBillVotes(params.id).catch(() => ({ results: [] })),
      api.getBillHistory(params.id).catch(() => ({ results: [] })),
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
          <BillVotes votes={votes.results} billId={params.id} />
        </div>

        {/* Bill History Section */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Bill History</h2>
          <BillHistory history={history.results} />
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error loading bill details:', error);
    notFound();
  }
}
