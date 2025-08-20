'use client';

import { useState } from 'react';
import Link from 'next/link';

interface RelatedDebate {
  id: string;
  date: string;
  debateNumber: number;
  speakerName: string;
  speakerParty: string;
  excerpt: string;
  mentions: number;
}

interface RelatedDebatesProps {
  billNumber: string;
  debates: RelatedDebate[];
  loading?: boolean;
}

export default function RelatedDebates({ billNumber, debates, loading = false }: RelatedDebatesProps) {
  const [showAll, setShowAll] = useState(false);

  const getPartyColor = (party: string): string => {
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
    return <div className="text-gray-500">Loading related debates...</div>;
  }

  if (debates.length === 0) {
    return (
      <div className="text-gray-500">
        No debates found mentioning this bill.
      </div>
    );
  }

  return (
    <div>
      <p className="text-sm text-gray-600 mb-4">
        Found {debates.length} debate{debates.length !== 1 ? 's' : ''} mentioning Bill {billNumber}
      </p>

      <div className="space-y-4">
        {displayedDebates.map((debate) => (
          <div key={debate.id} className="border-b border-gray-200 pb-4 last:border-0 last:pb-0">
            <div className="flex items-start justify-between mb-2">
              <div>
                <Link
                  href={`/debates/${debate.date}/${debate.debateNumber}`}
                  className="font-medium text-op-blue hover:underline"
                >
                  {new Date(debate.date).toLocaleDateString('en-CA', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </Link>
                <div className="text-sm text-gray-600 mt-1">
                  <span className={`font-medium ${getPartyColor(debate.speakerParty)}`}>
                    {debate.speakerName}
                  </span>
                  <span className="text-gray-500"> ({debate.speakerParty})</span>
                </div>
              </div>
              <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                {debate.mentions} mention{debate.mentions !== 1 ? 's' : ''}
              </span>
            </div>

            <p className="text-gray-700 text-sm line-clamp-3">
              {debate.excerpt}
            </p>

            <Link
              href={`/debates/${debate.date}/${debate.debateNumber}#${billNumber}`}
              className="inline-flex items-center mt-2 text-sm text-op-blue hover:underline"
            >
              Read full speech
              <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        ))}
      </div>

      {debates.length > 3 && (
        <div className="mt-4 text-center">
          <button
            onClick={() => setShowAll(!showAll)}
            className="text-op-blue hover:underline text-sm"
          >
            {showAll ? 'Show less' : `Show all ${debates.length} debates`}
          </button>
        </div>
      )}

      {/* Search for more */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <Link
          href={`/search?q=${encodeURIComponent(billNumber)}&type=debates`}
          className="inline-flex items-center text-sm text-op-blue hover:underline"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Search all debates for "{billNumber}"
        </Link>
      </div>
    </div>
  );
}
