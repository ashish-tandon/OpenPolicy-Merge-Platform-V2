import { Metadata } from 'next';
import VotingRecordsList from '@/components/voting/VotingRecordsList';

export const metadata: Metadata = {
  title: 'Voting Records | OpenPolicy',
  description: 'Browse and analyze parliamentary voting records, bill outcomes, and MP voting patterns',
  openGraph: {
    title: 'Voting Records | OpenPolicy',
    description: 'Browse and analyze parliamentary voting records, bill outcomes, and MP voting patterns',
    type: 'website',
  },
};

export default function VotingRecordsPage() {
  return (
    <div className="content-container py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Voting Records</h1>
        <p className="text-lg text-gray-600">
          Explore parliamentary voting records to understand how bills are decided and how MPs vote on important issues. 
          Track voting patterns, party positions, and the democratic process in action.
        </p>
      </div>

      {/* Voting Records List */}
      <VotingRecordsList />
    </div>
  );
}
