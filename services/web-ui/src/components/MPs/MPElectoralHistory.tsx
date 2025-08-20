'use client';

import { useState, useEffect } from 'react';

interface ElectionResult {
  id: number;
  electionDate: string;
  electionType: 'General' | 'By-election';
  riding: string;
  result: 'Elected' | 'Defeated' | 'Did not run';
  votesReceived: number;
  votePercentage: number;
  margin?: number;
  opponents: {
    name: string;
    party: string;
    votes: number;
    percentage: number;
  }[];
}

interface MPElectoralHistoryProps {
  mpId: number;
}

export default function MPElectoralHistory({ mpId }: MPElectoralHistoryProps) {
  const [elections, setElections] = useState<ElectionResult[]>([
    {
      id: 1,
      electionDate: '2021-09-20',
      electionType: 'General',
      riding: 'Toronto Centre',
      result: 'Elected',
      votesReceived: 18456,
      votePercentage: 42.3,
      margin: 8.7,
      opponents: [
        { name: 'John Smith', party: 'Conservative', votes: 14234, percentage: 33.6 },
        { name: 'Jane Doe', party: 'NDP', votes: 8123, percentage: 19.2 },
        { name: 'Bob Wilson', party: 'Green', votes: 2089, percentage: 4.9 },
      ],
    },
    {
      id: 2,
      electionDate: '2019-10-21',
      electionType: 'General',
      riding: 'Toronto Centre',
      result: 'Elected',
      votesReceived: 17234,
      votePercentage: 39.8,
      margin: 5.2,
      opponents: [
        { name: 'Mary Johnson', party: 'Conservative', votes: 15123, percentage: 34.6 },
        { name: 'Tom Brown', party: 'NDP', votes: 9876, percentage: 22.6 },
        { name: 'Sarah Green', party: 'Green', votes: 1345, percentage: 3.0 },
      ],
    },
  ]);
  const [loading, setLoading] = useState(false);

  // In production, this would fetch real electoral data
  useEffect(() => {
    // Placeholder for fetching electoral history
  }, [mpId]);

  const getResultColor = (result: string) => {
    switch (result) {
      case 'Elected': return 'bg-green-100 text-green-800';
      case 'Defeated': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPartyColor = (party: string) => {
    switch (party.toLowerCase()) {
      case 'liberal': return 'bg-red-600';
      case 'conservative': return 'bg-blue-600';
      case 'ndp': return 'bg-orange-600';
      case 'bloc': return 'bg-cyan-600';
      case 'green': return 'bg-green-600';
      default: return 'bg-gray-600';
    }
  };

  return (
    <div>
      {loading ? (
        <div className="text-gray-500">Loading electoral history...</div>
      ) : (
        <div className="space-y-8">
          {elections.map((election) => (
            <div key={election.id} className="bg-gray-50 rounded-lg p-6">
              {/* Election Header */}
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-700">
                    {election.electionType} Election - {new Date(election.electionDate).toLocaleDateString('en-CA', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </h3>
                  <p className="text-gray-600">{election.riding}</p>
                </div>
                <span className={`px-3 py-1 rounded text-sm font-medium ${getResultColor(election.result)}`}>
                  {election.result}
                </span>
              </div>

              {/* Results */}
              {election.result !== 'Did not run' && (
                <>
                  {/* Winner Stats */}
                  <div className="mb-4 p-4 bg-white rounded-lg border border-gray-200">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-gray-700">MP Result</span>
                      <span className="text-sm text-gray-500">
                        {election.margin && `Won by ${election.margin}%`}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-bold text-op-blue">
                        {election.votesReceived.toLocaleString()} votes
                      </span>
                      <span className="text-lg font-medium text-gray-600">
                        {election.votePercentage}%
                      </span>
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-op-blue h-2 rounded-full"
                          style={{ width: `${election.votePercentage}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Opponents */}
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-700 mb-2">Other Candidates</h4>
                    {election.opponents.map((opponent, index) => (
                      <div key={index} className="flex items-center justify-between py-2 border-b border-gray-200 last:border-0">
                        <div className="flex items-center">
                          <span className={`w-3 h-3 rounded-full mr-2 ${getPartyColor(opponent.party)}`}></span>
                          <span className="text-sm">{opponent.name} ({opponent.party})</span>
                        </div>
                        <div className="text-sm text-gray-600">
                          {opponent.votes.toLocaleString()} ({opponent.percentage}%)
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      )}

      {elections.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No electoral history found for this MP.
        </div>
      )}
    </div>
  );
}
