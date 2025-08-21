import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import BillTabs from '@/components/Bills/BillTabs';
import BillStatusTracker from '@/components/Bills/BillStatusTracker';
import BillVotesList from '@/components/Bills/BillVotesList';
import RelatedDebates from '@/components/Bills/RelatedDebates';

interface BillPageProps {
  params: Promise<{
    session: string;
    number: string;
  }>;
}

export default async function BillPage({ params }: BillPageProps) {
  const { session, number } = await params;
  try {
    const bill = await api.getBillByNumber(session, number);
    
    return (
      <div className="content-container py-8">
        {/* Breadcrumb */}
        <nav className="text-sm mb-6">
          <ol className="flex items-center space-x-2">
            <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li><Link href="/bills" className="text-gray-500 hover:text-op-blue">Bills</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li className="text-gray-700">{bill.number}</li>
          </ol>
        </nav>

        {/* Bill Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-3xl font-bold text-op-dark">{bill.number}</h1>
                <span className={`px-3 py-1 rounded text-sm font-medium ${
                  bill.privatemember 
                    ? 'bg-purple-100 text-purple-800' 
                    : 'bg-blue-100 text-blue-800'
                }`}>
                  {bill.privatemember ? 'Private Member Bill' : 'Government Bill'}
                </span>
                {bill.law && (
                  <span className="px-3 py-1 rounded text-sm font-medium bg-green-100 text-green-800">
                    Law
                  </span>
                )}
              </div>
              <h2 className="text-xl text-gray-700 mb-4">{bill.name}</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Session:</span>
                  <span className="ml-2 font-medium">{bill.session}</span>
                </div>
                <div>
                  <span className="text-gray-500">Introduced:</span>
                  <span className="ml-2 font-medium">
                    {bill.introduced 
                      ? new Date(bill.introduced).toLocaleDateString('en-CA', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                        })
                      : 'Not available'
                    }
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Sponsor:</span>
                  <span className="ml-2 font-medium">
                    {bill.sponsor_politician_id ? (
                      <Link href={`/mps/${bill.sponsor_politician_id}`} className="text-op-blue hover:underline">
                        View Sponsor
                      </Link>
                    ) : (
                      'Not specified'
                    )}
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="flex flex-col gap-2 ml-6">
              <a
                href={`https://www.parl.ca/legisinfo/en/bill/${bill.session}/${bill.number}`}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center px-4 py-2 bg-op-blue text-white rounded hover:bg-blue-700 transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                LEGISinfo
              </a>
              <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors">
                Set Alert
              </button>
            </div>
          </div>
        </div>

        {/* Bill Status Tracker */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Legislative Progress</h2>
          <BillStatusTracker bill={bill} />
        </div>

        {/* Recent Votes */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Votes on this Bill</h2>
          <BillVotesList billId={bill.id} />
        </div>

        {/* Related Debates */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Related Debates</h2>
          <RelatedDebates billNumber={bill.number} />
        </div>

        {/* Tabbed Content */}
        <div className="bg-white rounded-lg shadow">
          <BillTabs bill={bill} />
        </div>
      </div>
    );
  } catch (_error) {
    notFound();
  }
}
