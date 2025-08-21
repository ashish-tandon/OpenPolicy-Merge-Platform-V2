import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import CommitteeTabs from '@/components/Committees/CommitteeTabs';
import CommitteeHeader from '@/components/Committees/CommitteeHeader';
import ActiveStudies from '@/components/Committees/ActiveStudies';
import RecentMeetings from '@/components/Committees/RecentMeetings';

interface CommitteePageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function CommitteePage({ params }: CommitteePageProps) {
  const { slug } = await params;
  try {
    const committee = await api.getCommitteeBySlug(slug);
    
    return (
      <div className="content-container py-8">
        {/* Breadcrumb */}
        <nav className="text-sm mb-6">
          <ol className="flex items-center space-x-2">
            <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li><Link href="/committees" className="text-gray-500 hover:text-op-blue">Committees</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li className="text-gray-700">{committee.short_name || committee.name}</li>
          </ol>
        </nav>

        {/* Committee Header */}
        <CommitteeHeader committee={committee} />

        {/* Quick Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {/* Active Studies */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Active Studies</h2>
            <ActiveStudies committeeId={parseInt(committee.id) || 0} />
          </div>

          {/* Recent Meetings */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Recent Meetings</h2>
            <RecentMeetings committeeId={parseInt(committee.id) || 0} />
          </div>
        </div>

        {/* Tabbed Content */}
        <div className="bg-white rounded-lg shadow">
          <CommitteeTabs committee={committee} />
        </div>

        {/* Committee Resources */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-medium text-gray-700 mb-2">Official Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a
                  href={`https://www.ourcommons.ca/committees/en/${committee.slug}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-op-blue hover:underline flex items-center"
                >
                  Committee website
                  <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </li>
              <li>
                <Link href={`/committees/${slug}/meetings`} className="text-op-blue hover:underline">
                  Meeting archives
                </Link>
              </li>
              <li>
                <Link href={`/committees/${slug}/reports`} className="text-op-blue hover:underline">
                  Published reports
                </Link>
              </li>
            </ul>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-medium text-gray-700 mb-2">Follow This Committee</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <button className="text-op-blue hover:underline">
                  Set email alerts
                </button>
              </li>
              <li>
                <a href={`/api/v1/committees/${slug}/rss`} className="text-op-blue hover:underline flex items-center">
                  RSS feed
                  <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z" />
                  </svg>
                </a>
              </li>
              <li>
                <a href={`/api/v1/committees/${slug}`} className="text-op-blue hover:underline">
                  API access
                </a>
              </li>
            </ul>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-medium text-gray-700 mb-2">Contact</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>
                <span className="font-medium">Clerk:</span><br />
                committees@parl.gc.ca
              </li>
              <li>
                <span className="font-medium">Phone:</span><br />
                613-992-3150
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  } catch (_error) {
    notFound();
  }
}
