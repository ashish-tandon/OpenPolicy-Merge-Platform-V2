'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Vote {
  id: number;
  number: number;
  session: string;
  date: string;
  description: string;
  result: 'Passed' | 'Failed';
  mpVote: 'Yea' | 'Nay' | 'Paired' | 'Absent';
  billNumber?: string;
}

interface MPVotingRecordProps {
  mpId: number;
}

export default function MPVotingRecord({ mpId }: MPVotingRecordProps) {
  const [votes, setVotes] = useState<Vote[]>([
    {
      id: 1,
      number: 123,
      session: '45-1',
      date: '2025-06-20',
      description: 'Motion for second reading of Bill C-5, An Act to amend the Criminal Code',
      result: 'Passed',
      mpVote: 'Yea',
      billNumber: 'C-5',
    },
    {
      id: 2,
      number: 122,
      session: '45-1',
      date: '2025-06-19',
      description: 'Amendment to Bill C-3 at report stage',
      result: 'Failed',
      mpVote: 'Nay',
      billNumber: 'C-3',
    },
    {
      id: 3,
      number: 121,
      session: '45-1',
      date: '2025-06-18',
      description: 'Motion for third reading of Bill C-2',
      result: 'Passed',
      mpVote: 'Yea',
      billNumber: 'C-2',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');

  // In production, this would fetch real voting data
  useEffect(() => {
    // Placeholder for fetching voting record
  }, [mpId]);

  const getVoteColor = (vote: string) => {
    switch (vote) {
      case 'Yea': return 'text-green-600';
      case 'Nay': return 'text-red-600';
      case 'Paired': return 'text-blue-600';
      case 'Absent': return 'text-gray-600';
      default: return 'text-gray-600';
    }
  };

  const filteredVotes = filter === 'all' 
    ? votes 
    : votes.filter(v => v.mpVote.toLowerCase() === filter);

  return (
    <div>
      {/* Voting Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">245</div>
          <div className="text-sm text-gray-600">Yea Votes</div>
        </div>
        <div className="bg-red-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-red-600">98</div>
          <div className="text-sm text-gray-600">Nay Votes</div>
        </div>
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-600">12</div>
          <div className="text-sm text-gray-600">Paired</div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-gray-600">5</div>
          <div className="text-sm text-gray-600">Absent</div>
        </div>
      </div>

      {/* Filter */}
      <div className="mb-4">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          <option value="all">All Votes</option>
          <option value="yea">Yea Votes Only</option>
          <option value="nay">Nay Votes Only</option>
          <option value="paired">Paired Votes</option>
          <option value="absent">Absent</option>
        </select>
      </div>

      {/* Voting List */}
      {loading ? (
        <div className="text-gray-500">Loading voting record...</div>
      ) : (
        <div className="space-y-4">
          {filteredVotes.map((vote) => (
            <div key={vote.id} className="border-b border-gray-200 pb-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <Link
                      href={`/votes/${vote.session}/${vote.number}`}
                      className="font-medium text-op-blue hover:underline"
                    >
                      Vote #{vote.number}
                    </Link>
                    <span className="text-sm text-gray-500">{vote.date}</span>
                    {vote.billNumber && (
                      <Link
                        href={`/bills/${vote.session}/${vote.billNumber}`}
                        className="text-sm bg-gray-100 px-2 py-0.5 rounded hover:bg-gray-200"
                      >
                        Bill {vote.billNumber}
                      </Link>
                    )}
                  </div>
                  <p className="text-gray-700">{vote.description}</p>
                </div>
                <div className="flex flex-col items-end ml-4">
                  <span className={`font-medium ${getVoteColor(vote.mpVote)}`}>
                    {vote.mpVote}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded mt-1 ${
                    vote.result === 'Passed' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {vote.result}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
