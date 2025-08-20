'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Debate {
  id: number;
  date: string;
  debateNumber: string;
  speakerName: string;
  speakerParty: string;
  excerpt: string;
  mentions: number;
}

interface RelatedDebatesProps {
  billNumber: string;
}

export default function RelatedDebates({ billNumber }: RelatedDebatesProps) {
  const [debates, setDebates] = useState<Debate[]>([
    {
      id: 1,
      date: '2025-06-20',
      debateNumber: '147',
      speakerName: 'Jane Smith',
      speakerParty: 'Liberal',
      excerpt: `Mr. Speaker, Bill ${billNumber} represents a critical step forward in addressing the challenges facing Canadians today. This legislation will provide much-needed support to families across the country...`,
      mentions: 5,
    },
    {
      id: 2,
      date: '2025-06-19',
      debateNumber: '146',
      speakerName: 'John Doe',
      speakerParty: 'Conservative',
      excerpt: `Mr. Speaker, while we support the intent behind Bill ${billNumber}, we have serious concerns about its implementation. The government has not adequately considered the fiscal impact...`,
      mentions: 3,
    },
    {
      id: 3,
      date: '2025-06-18',
      debateNumber: '145',
      speakerName: 'Sarah Johnson',
      speakerParty: 'NDP',
      excerpt: `Mr. Speaker, Bill ${billNumber} is a good start, but it doesn't go far enough. We need bolder action to address the root causes of this issue. Our amendments would strengthen...`,
      mentions: 2,
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [showAll, setShowAll] = useState(false);

  // In production, this would fetch real debate data mentioning the bill
  useEffect(() => {
    // Placeholder for fetching related debates
  }, [billNumber]);

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

  const displayedDebates = showAll ? debates : debates.slice(0, 3);

  if (loading) {
    return <div className=""ldquo;text-gray-500""ldquo;>Loading related debates...</div>;
  }

  if (debates.length === 0) {
    return (
      <div className=""ldquo;text-gray-500""ldquo;>
        No debates found mentioning this bill.
      </div>
    );
  }

  return (
    <div>
      <p className=""ldquo;text-sm text-gray-600 mb-4""ldquo;>
        Found {debates.length} debate{debates.length !== 1 ? 's' : ''} mentioning Bill {billNumber}
      </p>

      <div className=""ldquo;space-y-4""ldquo;>
        {displayedDebates.map((debate) => (
          <div key={debate.id} className=""ldquo;border-b border-gray-200 pb-4 last:border-0 last:pb-0""ldquo;>
            <div className=""ldquo;flex items-start justify-between mb-2""ldquo;>
              <div>
                <Link
                  href={`/debates/${debate.date}/${debate.debateNumber}`}
                  className=""ldquo;font-medium text-op-blue hover:underline""ldquo;
                >
                  {new Date(debate.date).toLocaleDateString('en-CA', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </Link>
                <div className=""ldquo;text-sm text-gray-600 mt-1""ldquo;>
                  <span className={`font-medium ${getPartyColor(debate.speakerParty)}`}>
                    {debate.speakerName}
                  </span>
                  <span className=""ldquo;text-gray-500""ldquo;> ({debate.speakerParty})</span>
                </div>
              </div>
              <span className=""ldquo;text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded""ldquo;>
                {debate.mentions} mention{debate.mentions !== 1 ? 's' : ''}
              </span>
            </div>

            <p className=""ldquo;text-gray-700 text-sm line-clamp-3""ldquo;>
              {debate.excerpt}
            </p>

            <Link
              href={`/debates/${debate.date}/${debate.debateNumber}#${billNumber}`}
              className=""ldquo;inline-flex items-center mt-2 text-sm text-op-blue hover:underline""ldquo;
            >
              Read full speech
              <svg className=""ldquo;w-4 h-4 ml-1""ldquo; fill=""ldquo;none""ldquo; stroke=""ldquo;currentColor""ldquo; viewBox=""ldquo;0 0 24 24""ldquo;>
                <path strokeLinecap=""ldquo;round""ldquo; strokeLinejoin=""ldquo;round""ldquo; strokeWidth={2} d=""ldquo;M9 5l7 7-7 7""ldquo; />
              </svg>
            </Link>
          </div>
        ))}
      </div>

      {debates.length > 3 && (
        <div className=""ldquo;mt-4 text-center""ldquo;>
          <button
            onClick={() => setShowAll(!showAll)}
            className=""ldquo;text-op-blue hover:underline text-sm""ldquo;
          >
            {showAll ? 'Show less' : `Show all ${debates.length} debates`}
          </button>
        </div>
      )}

      {/* Search for more */}
      <div className=""ldquo;mt-6 pt-6 border-t border-gray-200""ldquo;>
        <Link
          href={`/search?q=${encodeURIComponent(billNumber)}&type=debates`}
          className=""ldquo;inline-flex items-center text-sm text-op-blue hover:underline""ldquo;
        >
          <svg className=""ldquo;w-4 h-4 mr-1""ldquo; fill=""ldquo;none""ldquo; stroke=""ldquo;currentColor""ldquo; viewBox=""ldquo;0 0 24 24""ldquo;>
            <path strokeLinecap=""ldquo;round""ldquo; strokeLinejoin=""ldquo;round""ldquo; strokeWidth={2} d=""ldquo;M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z""ldquo; />
          </svg>
          Search all debates for ""ldquo;{billNumber}""ldquo;
        </Link>
      </div>
    </div>
  );
}
