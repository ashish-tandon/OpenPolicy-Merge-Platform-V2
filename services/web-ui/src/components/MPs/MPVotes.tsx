'use client';
            
import { useState } from 'react';
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  MinusIcon,
  CalendarIcon,
  DocumentTextIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { MPVote } from '@/types/mps';
            
interface MPVotesProps {
  votes: MPVote[];
  mpId: string;
}
            
export default function MPVotes({ votes, mpId }: MPVotesProps) {
  const [selectedVote, setSelectedVote] = useState<MPVote | null>(null);
            
  if (!votes || votes.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
        <ChartBarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Voting Records</h3>
        <p className="text-gray-600">
          This MP hasnn't apos;t participated in any votes yet, or voting records are not available.
        </p>
      </div>
    );
  }
            
  const getVoteIcon = (voteType: string) => {
    switch (voteType) {
      case 'yes':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'no':
        return <XCircleIcon className="h-5 w-5 text-red-600" />;
      case 'abstain':
        return <MinusIcon className="h-5 w-5 text-yellow-600" />;
      case 'absent':
        return <MinusIcon className="h-5 w-5 text-gray-400" />;
      default:
        return <MinusIcon className="h-5 w-5 text-gray-400" />;
    }
  };
            
  const getVoteColor = (voteType: string) => {
    switch (voteType) {
      case 'yes':
        return 'bg-green-100 text-green-800';
      case 'no':
        return 'bg-red-100 text-red-800';
      case 'abstain':
        return 'bg-yellow-100 text-yellow-800';
      case 'absent':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
            
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Voting Summary */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Voting Summary</h3>
        <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {votes.filter(v => v.vote_type === 'yes').length}
            </div>
            <div className="text-sm text-gray-500">Yes Votes</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">
              {votes.filter(v => v.vote_type === 'no').length}
            </div>
            <div className="text-sm text-gray-500">No Votes</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {votes.filter(v => v.vote_type === 'abstain').length}
            </div>
            <div className="text-sm text-gray-500">Abstentions</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-600">
              {votes.filter(v => v.vote_type === 'absent').length}
            </div>
            <div className="text-sm text-gray-500">Absences</div>
          </div>
        </div>
      </div>
            
      {/* Voting Records */}
      <div className="divide-y divide-gray-200">
        {votes.map((vote) => (
          <div key={vote.id} className="px-6 py-4 hover:bg-gray-50">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3">
                  {getVoteIcon(vote.vote_type)}
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-gray-900">
                      {vote.bill_title}
                    </h4>
                    {vote.bill_number && (
                      <p className="text-sm text-gray-500">Bill {vote.bill_number}</p>
                    )}
                  </div>
                </div>
                
                <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                  <div className="flex items-center space-x-1">
                    <CalendarIcon className="h-4 w-4" />
                    <span>{format(new Date(vote.vote_date), 'MMM dd, yyyy')}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <DocumentTextIcon className="h-4 w-4" />
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getVoteColor(vote.vote_type)}`}>
                      {vote.vote_type.charAt(0).toUpperCase() + vote.vote_type.slice(1)}
                    </span>
                  </div>
                  {vote.vote_result && (
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      vote.vote_result === 'passed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {vote.vote_result.charAt(0).toUpperCase() + vote.vote_result.slice(1)}
                    </span>
                  )}
                </div>
                
                {vote.vote_description && (
                  <p className="mt-2 text-sm text-gray-600">{vote.vote_description}</p>
                )}
                
                {/* Additional Vote Context */}
                {(vote.party_position || vote.constituency_impact || vote.whip_status) && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {vote.party_position && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        Party: {vote.party_position}
                      </span>
                    )}
                    {vote.whip_status && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                        {vote.whip_status.charAt(0).toUpperCase() + vote.whip_status.slice(1)}
                      </span>
                    )}
                    {vote.constituency_impact && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                        Constituency Impact
                      </span>
                    )}
                  </div>
                )}
              </div>
              
              {/* Vote Result */}
              <div className="ml-4 text-right">
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getVoteColor(vote.vote_type)}`}>
                  {vote.vote_type.charAt(0).toUpperCase() + vote.vote_type.slice(1)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
