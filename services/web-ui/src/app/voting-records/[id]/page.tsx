import { notFound } from 'next/navigation';
import Link from 'next/link';
import { Metadata } from 'next';
import { api } from '@/lib/api';
import VotingRecordDetail from '@/components/voting/VotingRecordDetail';

interface VotingRecordPageProps {
  params: Promise<{
    id: string;
  }>;
}

export async function generateMetadata({ params }: VotingRecordPageProps): Promise<Metadata> {
  const { id } = await params;
  try {
    const votingRecord = await api.getVotingRecord(id);
    
    return {
      title: `Vote on ${votingRecord.bill_title || 'Bill'} | OpenPolicy`,
      description: `Voting record for ${votingRecord.bill_title || 'parliamentary bill'} on ${votingRecord.date}`,
      openGraph: {
        title: `Vote on ${votingRecord.bill_title || 'Bill'}`,
        description: `Voting record for ${votingRecord.bill_title || 'parliamentary bill'}`,
        type: 'website',
      },
    };
  } catch (_error) {
    return {
      title: 'Voting Record | OpenPolicy',
      description: 'View detailed voting record for parliamentary bills',
    };
  }
}

export default async function VotingRecordPage({ params }: VotingRecordPageProps) {
  const { id } = await params;
  try {
    // Fetch voting record data
    const votingRecord = await api.getVotingRecord(id);

    return (
      <div className="content-container py-8">
        {/* Breadcrumb Navigation */}
        <nav className="mb-6">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li>
              <Link href="/voting-records" className="hover:text-op-blue transition-colors">
                Voting Records
              </Link>
            </li>
            <li className="text-gray-400">/</li>
            <li className="text-gray-900 font-medium">
              Vote on {votingRecord.bill_title || 'Bill'}
            </li>
          </ol>
        </nav>

        {/* Main Voting Record Information */}
        <VotingRecordDetail votingRecord={votingRecord} />
      </div>
    );
  } catch (_error) {
    console.error('Error loading voting record:', error);
    notFound();
  }
}
