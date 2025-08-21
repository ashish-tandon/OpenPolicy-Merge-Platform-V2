import { Metadata } from 'next';
import FormerMPsList from '@/components/MPs/FormerMPsList';

export const metadata: Metadata = {
  title: 'Former Members of Parliament | OpenPolicy',
  description: 'Browse and search former Members of Parliament who have served in Canadian government',
  openGraph: {
    title: 'Former Members of Parliament | OpenPolicy',
    description: 'Browse and search former Members of Parliament who have served in Canadian government',
    type: 'website',
  },
};

export default function FormerMPsPage() {
  return (
    <div className="content-container py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Former Members of Parliament</h1>
        <p className="text-lg text-gray-600">
          Explore the history of Canadian democracy through the profiles of former Members of Parliament. 
          Discover their contributions, voting records, and impact on Canadian legislation.
        </p>
      </div>

      {/* Former MPs List */}
      <FormerMPsList />
    </div>
  );
}
