import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import MPProfile from '@/components/MPs/MPProfile';
import MPVotes from '@/components/MPs/MPVotes';
import MPCommittees from '@/components/MPs/MPCommittees';
import MPActivity from '@/components/MPs/MPActivity';
import { Metadata } from 'next';

interface MPProfilePageProps {
  params: Promise<{
    id: string;
  }>;
}

export async function generateMetadata({ params }: MPProfilePageProps): Promise<Metadata> {
  const { id } = await params;
  try {
    const mp = await api.getMember(id);
    
    return {
      title: `${mp.full_name} | OpenPolicy`,
      description: `Profile and voting record for ${mp.full_name}, MP for ${mp.constituency || 'Canada'}`,
      openGraph: {
        title: mp.full_name,
        description: `Member of Parliament for ${mp.constituency || 'Canada'}`,
        type: 'website',
      },
    };
  } catch (_error) {
    return {
      title: 'MP Profile | OpenPolicy',
      description: 'View detailed information about Members of Parliament',
    };
  }
}

export default async function MPProfilePage({ params }: MPProfilePageProps) {
  const { id } = await params;
  try {
    // Fetch MP data
    const [mp, votes, committees, activity] = await Promise.all([
      api.getMember(id),
      api.getMemberVotes(id).catch(() => ({ results: [] })),
      api.getMemberCommittees(id).catch(() => ({ results: [] })),
      api.getMemberActivity(id).catch(() => ({ results: [] })),
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

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* MP Photo & Basic Info */}
            {mp.image && (
              <div className="bg-white rounded-lg shadow p-4">
                <img 
                  src={mp.image} 
                  alt={mp.full_name || mp.name}
                  className="w-full rounded-lg mb-2"
                />
                <p className="text-xs text-gray-500 text-center">House of Commons photo</p>
              </div>
            )}

            {/* Track this MP */}
            {mp.current_member && (
              <div className="bg-white rounded-lg shadow p-4">
                <h3 className="font-bold text-op-dark mb-3">Track {mp.name?.split(' ')[0]}</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <Link 
                      href={`/alerts/signup?politician=${mp.id}`}
                      className="text-op-blue hover:underline"
                    >
                      Get e-mail when {mp.pronoun_object || 'they'} speak{mp.pronoun_object === 'they' ? '' : 's'} in House debates
                    </Link>
                  </li>
                  <li>
                    Subscribe to feeds (<Link href="/about/rss" className="text-op-blue hover:underline">learn more</Link>) of{' '}
                    <Link href={`/rss/mp/${mp.id}/activity`} className="text-op-blue hover:underline">
                      recent activity
                    </Link>{' '}
                    or{' '}
                    <Link href={`/rss/mp/${mp.id}/statements`} className="text-op-blue hover:underline">
                      statements in the House
                    </Link>
                  </li>
                </ul>
              </div>
            )}

            {/* Contact */}
            {mp.current_member && mp.email && (
              <div className="bg-white rounded-lg shadow p-4">
                <h3 className="font-bold text-op-dark mb-3">Your Say</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <Link 
                      href={`/mps/${mp.slug}/contact`}
                      className="text-op-blue hover:underline"
                    >
                      Contact {mp.name?.split(' ')[0]}
                    </Link>
                  </li>
                </ul>
              </div>
            )}

            {/* In Parliament */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-bold text-op-dark mb-3">In Parliament</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link 
                    href={`/search?q=MP:"${mp.slug}" Type:"debate"&sort=date desc`}
                    className="text-op-blue hover:underline"
                  >
                    Speeches in House debates
                  </Link>
                </li>
              </ul>
            </div>

            {/* Elsewhere */}
            {mp.current_member && (mp.url || mp.twitter_username) && (
              <div className="bg-white rounded-lg shadow p-4">
                <h3 className="font-bold text-op-dark mb-3">Elsewhere</h3>
                <ul className="space-y-2 text-sm">
                  {mp.url && (
                    <li>
                      <a 
                        href={mp.url}
                        className="text-op-blue hover:underline"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {mp.pronoun_posessive || 'Their'} site
                      </a>
                    </li>
                  )}
                  {mp.twitter_username && (
                    <li>
                      <a 
                        href={`https://twitter.com/${mp.twitter_username}`}
                        className="text-op-blue hover:underline"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Twitter
                      </a>
                    </li>
                  )}
                </ul>
              </div>
            )}

            {/* Crucial Fact */}
            {mp.favourite_word && (
              <div className="bg-white rounded-lg shadow p-4">
                <h3 className="font-bold text-op-dark mb-3">Crucial Fact</h3>
                <p className="text-sm">
                  {mp.pronoun_posessive || 'Their'}{' '}
                  <span className="underline decoration-dotted" title="Most frequently spoken word in Parliament, compared to other MPs.">
                    favourite word
                  </span>{' '}
                  {mp.current_member ? 'is' : 'was'} <strong>{mp.favourite_word}</strong>.
                </p>
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-8">
            {/* Main MP Information */}
            <MPProfile mp={mp} />

            {/* Search Box */}
            <div className="bg-white rounded-lg shadow p-6">
              <form action="/search" method="GET" className="relative">
                <input type="hidden" name="prepend" value={`MP: "${mp.slug}"`} />
                <input
                  type="search"
                  name="q"
                  placeholder={`Search ${mp.name}'s speeches and votes`}
                  className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-transparent"
                />
                <button
                  type="submit"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 text-gray-500 hover:text-op-blue"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
              </form>
            </div>

            {/* Word Cloud */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-op-dark mb-4">Word Cloud</h2>
              <div className="h-64 bg-gray-50 rounded flex items-center justify-center">
                <p className="text-gray-500">Word cloud visualization coming soon</p>
              </div>
            </div>

            {/* Activity Timeline */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-op-dark mb-4">Recent Activity</h2>
              <MPActivity activity={activity.results} />
            </div>

            {/* MP Voting Record */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-op-dark mb-4">Voting Record</h2>
              <MPVotes votes={votes.results} mpId={id} />
            </div>

            {/* MP Committees */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-op-dark mb-4">Committee Work</h2>
              <MPCommittees committees={committees.results} />
            </div>
          </div>
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error loading MP profile:', error);
    notFound();
  }
}
