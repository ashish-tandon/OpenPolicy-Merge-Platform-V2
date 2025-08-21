'use client';

import { useState } from 'react';
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  MinusIcon,
  CalendarIcon,
  UserGroupIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { BillVote } from '@/types/bills';

interface BillVotesProps {
  votes: BillVote[];
  billId: string;
}

export default function BillVotes({ votes, billId }: BillVotesProps) {
  const [selectedVote, setSelectedVote] = useState<BillVote | null>(null);

  if (!votes || votes.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
        <ChartBarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Voting Records</h3>
        <p className="text-gray-600">
          This bill hasn't been voted on yet, or voting records are not available.
        </p>
      </div>
    );
  }

  // Calculate vote statistics
  const totalVotes = votes.reduce((sum, vote) => sum + (vote.yes + vote.no + vote.abstain), 0);
  const totalYes = votes.reduce((sum, vote) => sum + vote.yes, 0);
  const totalNo = votes.reduce((sum, vote) => sum + vote.no, 0);
  const totalAbstain = votes.reduce((sum, vote) => sum + vote.abstain, 0);

  const getVoteResult = (vote: BillVote) => {
    if (vote.yes > vote.no) return 'passed';
    if (vote.no > vote.yes) return 'failed';
    return 'tied';
  };

  const getVoteResultColor = (result: string) => {
    switch (result) {
      case 'passed':
        return 'text-green-600 bg-green-100';
      case 'failed':
        return 'text-red-600 bg-red-100';
      case 'tied':
        return 'text-yellow-600 bg-yellow-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getVoteResultIcon = (result: string) => {
    switch (result) {
      case 'passed':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'failed':
        return <XCircleIcon className="h-5 w-5 text-red-600" />;
      case 'tied':
        return <MinusIcon className="h-5 w-5 text-yellow-600" />;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Vote Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-gray-900">{totalVotes}</div>
          <div className="text-sm text-gray-600">Total Votes</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-green-600">{totalYes}</div>
          <div className="text-sm text-gray-600">Yes</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-red-600">{totalNo}</div>
          <div className="text-sm text-gray-600">No</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-yellow-600">{totalAbstain}</div>
          <div className="text-sm text-gray-600">Abstain</div>
        </div>
      </div>

      {/* Individual Vote Records */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Voting Records</h3>
        </div>
        
        <div className="divide-y divide-gray-200">
          {votes.map((vote, index) => (
            <div
              key={index}
              className={`p-6 hover:bg-gray-50 transition-colors cursor-pointer ${
                selectedVote?.id === vote.id ? 'bg-blue-50' : ''
              }`}
              onClick={() => setSelectedVote(selectedVote?.id === vote.id ? null : vote)}
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  {/* Vote Date and Type */}
                  <div className="flex items-center space-x-4 mb-3">
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <CalendarIcon className="h-4 w-4" />
                      <span>
                        {vote.date ? format(new Date(vote.date), 'MMM dd, yyyy') : 'Date not specified'}
                      </span>
                    </div>
                    
                    {vote.voteType && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                        {vote.voteType}
                      </span>
                    )}
                  </div>

                  {/* Vote Description */}
                  {vote.description && (
                    <p className="text-gray-700 mb-3">{vote.description}</p>
                  )}

                  {/* Vote Breakdown */}
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-lg font-semibold text-green-600">{vote.yes}</div>
                      <div className="text-sm text-gray-600">Yes</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-semibold text-red-600">{vote.no}</div>
                      <div className="text-sm text-gray-600">No</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-semibold text-yellow-600">{vote.abstain}</div>
                      <div className="text-sm text-gray-600">Abstain</div>
                    </div>
                  </div>
                </div>

                {/* Vote Result */}
                <div className="ml-6 text-right">
                  <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getVoteResultColor(getVoteResult(vote))}`}>
                    {getVoteResultIcon(getVoteResult(vote))}
                    <span className="ml-1 capitalize">{getVoteResult(vote)}</span>
                  </div>
                </div>
              </div>

              {/* Expanded Vote Details */}
              {selectedVote?.id === vote.id && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Vote Details */}
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Vote Details</h4>
                      <div className="space-y-2 text-sm text-gray-600">
                        {vote.session && (
                          <div>Session: {vote.session}</div>
                        )}
                        {vote.division && (
                          <div>Division: {vote.division}</div>
                        )}
                        {vote.required && (
                          <div>Required Majority: {vote.required}</div>
                        )}
                      </div>
                    </div>

                    {/* Party Breakdown (if available) */}
                    {vote.partyBreakdown && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">Party Breakdown</h4>
                        <div className="space-y-2 text-sm">
                          {Object.entries(vote.partyBreakdown).map(([party, votes]) => (
                            <div key={party} className="flex justify-between">
                              <span className="text-gray-600">{party}</span>
                              <span className="font-medium">{votes}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Individual MP Votes (if available) */}
                  {vote.mpVotes && vote.mpVotes.length > 0 && (
                    <div className="mt-4">
                      <h4 className="font-medium text-gray-900 mb-2">Individual MP Votes</h4>
                      <div className="max-h-48 overflow-y-auto">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                          {vote.mpVotes.map((mpVote, mpIndex) => (
                            <div key={mpIndex} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                              <span className="text-gray-700">{mpVote.mpName}</span>
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                mpVote.vote === 'yes' ? 'bg-green-100 text-green-800' :
                                mpVote.vote === 'no' ? 'bg-red-100 text-red-800' :
                                'bg-yellow-100 text-yellow-800'
                              }`}>
                                {mpVote.vote}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
