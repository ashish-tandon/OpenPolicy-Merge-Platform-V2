import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import MPProfile from '@/components/mps/MPProfile';
import MPVotes from '@/components/mps/MPVotes';
import MPCommittees from '@/components/mps/MPCommittees';
import MPActivity from '@/components/mps/MPActivity';
import { Metadata } from 'next';

interface MPProfilePageProps {
  params: {
    id: string;
  };
}

export async function generateMetadata({ params }: MPProfilePageProps): Promise<Metadata> {
  try {
    const mp = await api.getMember(params.id);
    
    return {
      title: `${mp.full_name} | OpenPolicy`,
      description: `Profile and voting record for ${mp.full_name}, MP for ${mp.constituency || 'Canada'}`,
      openGraph: {
        title: mp.full_name,
        description: `Member of Parliament for ${mp.constituency || 'Canada'}`,
        type: 'website',
      },
    };
  } catch (error) {
    return {
      title: 'MP Profile | OpenPolicy',
      description: 'View detailed information about Members of Parliament',
    };
  }
}

export default async function MPProfilePage({ params }: MPProfilePageProps) {
  try {
    // Fetch MP data
    const [mp, votes, committees, activity] = await Promise.all([
      api.getMember(params.id),
      api.getMemberVotes(params.id).catch(() => ({ results: [] })),
      api.getMemberCommittees(params.id).catch(() => ({ results: [] })),
      api.getMemberActivity(params.id).catch(() => ({ results: [] })),
    ]);

    return (
      <div className="content-container py-8">
        {/* Breadcrumb Navigation */}
        <nav className="mb-6">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li>
              <Link href="/mps" className="hover:text-op-blue transition-colors">
                MPs
              </Link>
            </li>
            <li className="text-gray-400">/</li>
            <li className="text-gray-900 font-medium">{mp.full_name}</li>
          </ol>
        </nav>

        {/* Main MP Information */}
        <MPProfile mp={mp} />

        {/* MP Voting Record */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Voting Record</h2>
          <MPVotes votes={votes.results} mpId={params.id} />
        </div>

        {/* MP Committees */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Committee Work</h2>
          <MPCommittees committees={committees.results} />
        </div>

        {/* MP Activity Timeline */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Activity Timeline</h2>
          <MPActivity activity={activity.results} />
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error loading MP profile:', error);
    notFound();
  }
}
