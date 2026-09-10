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
    // Fetch committee data and related information
    const [committee, meetings, subcommittees, recentStudies] = await Promise.all([
      api.getCommitteeBySlug(slug),
      api.getCommitteeMeetings(slug, { page: '1', page_size: '10' }).catch(() => ({ items: [] })),
      api.getSubcommittees(slug).catch(() => ({ items: [] })),
      api.getCommitteeStudies({ committee: slug, page: '1', page_size: '6' }).catch(() => ({ items: [] }))
    ]);

    // Get archive years (current year back to 2000 or committee start)
    const currentYear = new Date().getFullYear();
    const archiveYears = Array.from({ length: currentYear - 1999 }, (_, i) => currentYear - i);
    
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

        {/* Search Box */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <form action="/search" method="GET" className="relative">
            <input type="hidden" name="prepend" value={`Committee: "${slug}"`} />
            <input
              type="search"
              name="q"
              placeholder={`Search ${committee.short_name || committee.name} meetings and evidence`}
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
          
          <div className="mt-4 space-y-2 text-sm text-gray-600">
            {committee.parent && (
              <p>
                This is a subcommittee of the{' '}
                <Link href={`/committees/${committee.parent.slug}`} className="text-op-blue hover:underline">
                  {committee.parent.name}
                </Link>{' '}
                committee.
              </p>
            )}
            <p>
              This committee's page on{' '}
              <a 
                href={committee.source_url || `https://www.parl.ca/committees/en/${slug}`}
                className="text-op-blue hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Parliament's site
              </a>{' '}
              is much more comprehensive than this page.
            </p>
          </div>
        </div>

        {/* Word Cloud */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="h-64 bg-gray-50 rounded flex items-center justify-center">
            <p className="text-gray-500">Committee word cloud visualization coming soon</p>
          </div>
        </div>

        {/* Meetings */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-1">
              <h2 className="text-xl font-bold text-op-dark">Meetings</h2>
            </div>
            <div className="lg:col-span-3">
              {meetings.items && meetings.items.length > 0 ? (
                <div className="space-y-2">
                  {meetings.items.map((meeting: any) => (
                    <div key={meeting.id} className="border-b border-gray-200 pb-2 last:border-0">
                      <Link 
                        href={`/committees/${slug}/meetings/${meeting.number}`}
                        className="text-op-blue hover:underline"
                      >
                        Meeting #{meeting.number}
                      </Link>
                      <span className="text-sm text-gray-600 ml-2">
                        {new Date(meeting.date).toLocaleDateString('en-CA', { 
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </span>
                      {meeting.description && (
                        <p className="text-sm text-gray-600 mt-1">{meeting.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No recent meetings found.</p>
              )}
            </div>
          </div>
        </div>

        {/* Subcommittees */}
        {subcommittees.items && subcommittees.items.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                <h2 className="text-xl font-bold text-op-dark">
                  Subcommittee{subcommittees.items.length > 1 ? 's' : ''}
                </h2>
              </div>
              <div className="lg:col-span-3">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {subcommittees.items.map((sub: any) => (
                    <div key={sub.id}>
                      <Link 
                        href={`/committees/${sub.slug}`}
                        className="text-op-blue hover:underline"
                      >
                        {sub.name}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Recent Studies */}
        {recentStudies.items && recentStudies.items.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                <h2 className="text-xl font-bold text-op-dark">Recent studies</h2>
              </div>
              <div className="lg:col-span-3">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {recentStudies.items.map((study: any) => (
                    <div key={study.id} className="text-sm line-clamp-2">
                      <Link 
                        href={`/committees/${slug}/studies/${study.id}`}
                        className="text-op-blue hover:underline"
                        title={study.name}
                      >
                        {study.name}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Archive */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-1">
              <h2 className="text-xl font-bold text-op-dark">Archive</h2>
            </div>
            <div className="lg:col-span-3">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {archiveYears.map(year => (
                  <div key={year} className="text-sm">
                    <Link 
                      href={`/committees/${slug}/archive/${year}`}
                      className="text-op-blue hover:underline"
                    >
                      {year}
                    </Link>
                  </div>
                ))}
              </div>
            </div>
          </div>
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
