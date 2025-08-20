import { Committee } from '@/lib/api';
import Link from 'next/link';

interface CommitteeHeaderProps {
  committee: Committee;
}

export default function CommitteeHeader({ committee }: CommitteeHeaderProps) {
  // Mock additional committee data
  const committeeData = {
    type: committee.name.includes('Special') ? 'Special' : 'Standing',
    established: '2021-12-16',
    mandate: 'To study matters related to ' + committee.name.toLowerCase().replace('standing committee on ', ''),
    memberCount: 12,
    chair: {
      name: 'Hon. John Smith',
      party: 'Liberal',
      mpSlug: 'john-smith',
    },
    viceChairs: [
      { name: 'Jane Doe', party: 'Conservative', mpSlug: 'jane-doe' },
      { name: 'Bob Wilson', party: 'NDP', mpSlug: 'bob-wilson' },
    ],
  };

  const getPartyColor = (party: string) => {
    switch (party.toLowerCase()) {
      case 'liberal': return 'text-red-600';
      case 'conservative': return 'text-blue-600';
      case 'ndp': return 'text-orange-600';
      case 'bloc': return 'text-cyan-600';
      case 'green': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-8">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold text-op-dark">
              {committee.name}
            </h1>
            <span className={`px-3 py-1 rounded text-sm font-medium ${
              committeeData.type === 'Special' 
                ? 'bg-purple-100 text-purple-800' 
                : 'bg-blue-100 text-blue-800'
            }`}>
              {committeeData.type}
            </span>
          </div>
          
          {committee.short_name && committee.short_name !== committee.name && (
            <p className="text-lg text-gray-600 mb-3">
              Commonly known as: <strong>{committee.short_name}</strong>
            </p>
          )}

          <p className="text-gray-700 mb-4">
            {committeeData.mandate}
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Established:</span>
              <span className="ml-2 font-medium">
                {new Date(committeeData.established).toLocaleDateString('en-CA', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </span>
            </div>
            <div>
              <span className="text-gray-500">Members:</span>
              <span className="ml-2 font-medium">{committeeData.memberCount}</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="flex flex-col gap-2 ml-6">
          <Link
            href={`/committees/${committee.slug}/meetings`}
            className="px-4 py-2 bg-op-blue text-white rounded hover:bg-blue-700 transition-colors text-center"
          >
            View Meetings
          </Link>
          <Link
            href={`/committees/${committee.slug}/studies`}
            className="px-4 py-2 border border-op-blue text-op-blue rounded hover:bg-blue-50 transition-colors text-center"
          >
            Current Studies
          </Link>
        </div>
      </div>

      {/* Leadership */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="font-medium text-gray-700 mb-3">Committee Leadership</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-sm text-gray-500 mb-1">Chair</p>
            <Link
              href={`/mps/${committeeData.chair.mpSlug}`}
              className={`font-medium hover:underline ${getPartyColor(committeeData.chair.party)}`}
            >
              {committeeData.chair.name}
            </Link>
            <span className="text-sm text-gray-600 ml-1">({committeeData.chair.party})</span>
          </div>
          {committeeData.viceChairs.map((viceChair, index) => (
            <div key={index}>
              <p className="text-sm text-gray-500 mb-1">Vice-Chair</p>
              <Link
                href={`/mps/${viceChair.mpSlug}`}
                className={`font-medium hover:underline ${getPartyColor(viceChair.party)}`}
              >
                {viceChair.name}
              </Link>
              <span className="text-sm text-gray-600 ml-1">({viceChair.party})</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
