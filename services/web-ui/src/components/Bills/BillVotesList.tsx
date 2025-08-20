'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Vote {
  id: number;
  number: number;
  session: string;
  date: string;
  description: string;
  result: 'Passed' | 'Failed' | 'Tied';
  yea_total: number;
  nay_total: number;
  paired_total: number;
}

interface BillVotesListProps {
  billId: number;
}

export default function BillVotesList({ billId }: BillVotesListProps) {
  const [votes, setVotes] = useState<Vote[]>([
    {
      id: 1,
      number: 123,
      session: '45-1',
      date: '2025-06-20',
      description: 'Motion for second reading',
      result: 'Passed',
      yea_total: 178,
      nay_total: 145,
      paired_total: 5,
    },
    {
      id: 2,
      number: 115,
      session: '45-1',
      date: '2025-06-10',
      description: 'Amendment at committee stage',
      result: 'Failed',
      yea_total: 142,
      nay_total: 181,
      paired_total: 5,
    },
  ]);
  const [loading, setLoading] = useState(false);

  // In production, this would fetch real vote data for the bill
  useEffect(() => {
    // Placeholder for fetching votes
  }, [billId]);

  const getVoteMargin = (vote: Vote) => {
    const margin = Math.abs(vote.yea_total - vote.nay_total);
    return margin;
  };

  const getVotePercentage = (vote: Vote) => {
    const total = vote.yea_total + vote.nay_total;
    const yeaPercent = ((vote.yea_total / total) * 100).toFixed(1);
    const nayPercent = ((vote.nay_total / total) * 100).toFixed(1);
    return { yea: yeaPercent, nay: nayPercent };
  };

  if (loading) {
    return <div className="text-gray-500">Loading votes...</div>;
  }

  if (votes.length === 0) {
    return (
      <div className="text-gray-500">
        No votes have been held on this bill yet.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {votes.map((vote) => {
        const percentages = getVotePercentage(vote);
        const margin = getVoteMargin(vote);
        
        return (
          <div key={vote.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
            <div className="flex items-start justify-between mb-3">
              <div>
                <Link
                  href={`/votes/${vote.session}/${vote.number}`}
                  className="text-lg font-medium text-op-blue hover:underline"
                >
                  Vote #{vote.number}
                </Link>
                <p className="text-sm text-gray-600 mt-1">{vote.description}</p>
                <p className="text-sm text-gray-500">
                  {new Date(vote.date).toLocaleDateString('en-CA', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>
              <div className="text-right">
                <span className={`inline-block px-3 py-1 rounded text-sm font-medium ${
                  vote.result === 'Passed' 
                    ? 'bg-green-100 text-green-800' 
                    : vote.result === 'Failed'
                    ? 'bg-red-100 text-red-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {vote.result}
                </span>
                <p className="text-xs text-gray-500 mt-1">
                  Margin: {margin} votes
                </p>
              </div>
            </div>

            {/* Vote Breakdown */}
            <div className="grid grid-cols-3 gap-4 mb-3">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{vote.yea_total}</div>
                <div className="text-xs text-gray-600">Yea ({percentages.yea}%)</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">{vote.nay_total}</div>
                <div className="text-xs text-gray-600">Nay ({percentages.nay}%)</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{vote.paired_total}</div>
                <div className="text-xs text-gray-600">Paired</div>
              </div>
            </div>

            {/* Visual Vote Bar */}
            <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
              <div className="h-full flex">
                <div 
                  className="bg-green-500"
                  style={{ width: `${percentages.yea}%` }}
                />
                <div 
                  className="bg-red-500"
                  style={{ width: `${percentages.nay}%` }}
                />
              </div>
            </div>

            {/* Actions */}
            <div className="mt-3 flex items-center justify-between">
              <Link
                href={`/votes/${vote.session}/${vote.number}`}
                className="text-sm text-op-blue hover:underline"
              >
                View full vote details →
              </Link>
              <button className="text-sm text-gray-500 hover:text-gray-700">
                Party breakdown
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
