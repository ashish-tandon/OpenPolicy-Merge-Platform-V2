import { notFound } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { api } from '@/lib/api';
import MPTabs from '@/components/MPs/MPTabs';
import MPContactInfo from '@/components/MPs/MPContactInfo';
import MPWordAnalysis from '@/components/MPs/MPWordAnalysis';

interface MPPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function MPPage({ params }: MPPageProps) {
  const { slug } = await params;
  try {
    const mp = await api.getMemberBySlug(slug);
    
    return (
      <div className="content-container py-8">
        {/* MP Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-6">
            {/* Photo */}
            <div className="flex-shrink-0">
              {mp.image ? (
                <Image
                  src={mp.image}
                  alt={mp.name}
                  width={200}
                  height={250}
                  className="rounded-lg object-cover"
                />
              ) : (
                <div className="w-[200px] h-[250px] bg-gray-200 rounded-lg flex items-center justify-center">
                  <svg className="w-20 h-20 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              )}
            </div>

            {/* Basic Info */}
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-op-dark mb-2">{mp.name}</h1>
              
              {mp.party && (
                <div className="flex items-center mb-3">
                  <span className={`w-4 h-4 rounded-full mr-2 ${getPartyColor(mp.party.slug)}`}></span>
                  <span className="text-lg">{mp.party.name}</span>
                </div>
              )}

              {mp.riding && (
                <div className="mb-4">
                  <h2 className="text-xl text-gray-700">
                    {mp.riding.name}
                    {mp.riding.province && ` (${mp.riding.province})`}
                  </h2>
                </div>
              )}

              {!mp.current_member && (
                <div className="mb-4">
                  <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded text-sm">
                    Former Member of Parliament
                  </span>
                </div>
              )}

              {/* Quick Actions */}
              <div className="flex flex-wrap gap-3 mt-6">
                <Link
                  href={`/mps/${params.slug}/votes`}
                  className="bg-op-blue text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
                >
                  View Voting Record
                </Link>
                <Link
                  href={`/mps/${params.slug}/speeches`}
                  className="border border-op-blue text-op-blue px-4 py-2 rounded hover:bg-blue-50 transition-colors"
                >
                  Read Speeches
                </Link>
                <button
                  className="border border-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-50 transition-colors"
                >
                  Set Email Alert
                </button>
              </div>
            </div>

            {/* Contact Info Sidebar */}
            <div className="flex-shrink-0 md:w-80">
              <MPContactInfo mp={mp} />
            </div>
          </div>
        </div>

        {/* Word Analysis Widget */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Favourite Words in Parliament</h2>
          <MPWordAnalysis mpId={mp.id} />
        </div>

        {/* Tabbed Content */}
        <div className="bg-white rounded-lg shadow">
          <MPTabs mp={mp} />
        </div>

        {/* RSS Feed Link */}
        <div className="mt-8 text-center">
          <a
            href={`/api/v1/mps/${params.slug}/rss`}
            className="inline-flex items-center text-op-blue hover:underline"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z" />
            </svg>
            Subscribe to RSS feed for {mp.name}
          </a>
        </div>
      </div>
    );
  } catch (_error) {
    notFound();
  }
}

function getPartyColor(slug: string) {
  switch (slug) {
    case 'liberal': return 'bg-red-600';
    case 'conservative': return 'bg-blue-600';
    case 'ndp': return 'bg-orange-600';
    case 'bloc': return 'bg-cyan-600';
    case 'green': return 'bg-green-600';
    default: return 'bg-gray-600';
  }
}
