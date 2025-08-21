'use client';

import { useState, useEffect } from 'react';
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  MinusIcon,
  ChartBarIcon,
  UserGroupIcon,
  MapPinIcon,
  FlagIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';

interface BillPublicVotingProps {
  billId: string;
  billTitle: string;
  billNumber: string;
}

export default function BillPublicVoting({ billId, billTitle, billNumber }: BillPublicVotingProps) {
  const [votingData, setVotingData] = useState<any>(null);
  const [userVotes, setUserVotes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showUserVotes, setShowUserVotes] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(10);

  useEffect(() => {
    loadVotingData();
  }, [billId]);

  const loadVotingData = async () => {
    try {
      setLoading(true);
      
      // Load voting summary
      const summaryResponse = await api.getBillVotingSummary(billId);
      
      // Load user votes
      const votesResponse = await api.getBillUserVotes(billId, currentPage, pageSize);
      
      setVotingData(summaryResponse.voting_summary);
      setUserVotes(votesResponse.results);
    } catch (error) {
      console.error('Error loading voting data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMoreUserVotes = async (page: number) => {
    try {
      const response = await api.getBillUserVotes(billId, page, pageSize);
      setUserVotes(response.results);
      setCurrentPage(page);
    } catch (error) {
      console.error('Error loading user votes:', error);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-6"></div>
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
          <div className="h-32 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!votingData) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <p className="text-gray-500 text-center">No voting data available for this bill.</p>
      </div>
    );
  }

  const { overall_statistics, constituency_breakdown, demographic_breakdown, voting_trends } = votingData;

  const getVoteIcon = (choice: string) => {
    switch (choice.toLowerCase()) {
      case 'yes':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'no':
        return <XCircleIcon className="h-5 w-5 text-red-600" />;
      case 'abstain':
        return <MinusIcon className="h-5 w-5 text-yellow-600" />;
      default:
        return null;
    }
  };

  const getVoteColor = (choice: string) => {
    switch (choice.toLowerCase()) {
      case 'yes':
        return 'bg-green-100 text-green-800';
      case 'no':
        return 'bg-red-100 text-red-800';
      case 'abstain':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Overall Voting Statistics */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Public Opinion on Bill {billNumber}</h3>
        
        {/* Vote Counts */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {overall_statistics.yes_votes}
            </div>
            <div className="text-sm text-gray-500">Yes Votes</div>
            <div className="text-xs text-gray-400">
              {overall_statistics.yes_percentage}%
            </div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-red-600">
              {overall_statistics.no_votes}
            </div>
            <div className="text-sm text-gray-500">No Votes</div>
            <div className="text-xs text-gray-400">
              {overall_statistics.no_percentage}%
            </div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-600">
              {overall_statistics.abstentions}
            </div>
            <div className="text-sm text-gray-500">Abstentions</div>
            <div className="text-xs text-gray-400">
              {overall_statistics.abstain_percentage}%
            </div>
          </div>
        </div>

        {/* Total Votes */}
        <div className="text-center p-4 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">
            {overall_statistics.total_votes_cast.toLocaleString()}
          </div>
          <div className="text-sm text-gray-600">Total Votes Cast</div>
        </div>
      </div>

      {/* Constituency Breakdown */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Constituency Breakdown</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Top Supporting Constituencies */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
              <CheckCircleIcon className="h-4 w-4 text-green-600 mr-2" />
              Top Supporting Constituencies
            </h4>
            <div className="space-y-2">
              {constituency_breakdown.top_supporting_constituencies.map((constituency: any, index: number) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <span className="text-gray-700">{constituency.name}</span>
                  <span className="text-green-600 font-medium">
                    {constituency.yes_percentage}% ({constituency.total_votes})
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Opposing Constituencies */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
              <XCircleIcon className="h-4 w-4 text-red-600 mr-2" />
              Top Opposing Constituencies
            </h4>
            <div className="space-y-2">
              {constituency_breakdown.top_opposing_constituencies.map((constituency: any, index: number) => (
                <div key={index} className="flex justify-between items-center text-sm">
                  <span className="text-gray-700">{constituency.name}</span>
                  <span className="text-red-600 font-medium">
                    {constituency.no_percentage}% ({constituency.total_votes})
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Coverage Stats */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-lg font-semibold text-gray-900">
                {constituency_breakdown.total_constituencies}
              </div>
              <div className="text-sm text-gray-600">Total Constituencies</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-gray-900">
                {constituency_breakdown.constituencies_with_votes}
              </div>
              <div className="text-sm text-gray-600">With Votes</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-gray-900">
                {constituency_breakdown.constituency_coverage}%
              </div>
              <div className="text-sm text-gray-600">Coverage</div>
            </div>
          </div>
        </div>
      </div>

      {/* Demographic Breakdown */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Demographic Breakdown</h3>
        
        {/* Age Groups */}
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Age Groups</h4>
          <div className="space-y-2">
            {Object.entries(demographic_breakdown.age_groups).map(([age, votes]: [string, any]) => (
              <div key={age} className="flex items-center justify-between">
                <span className="text-sm text-gray-600">{age}</span>
                <div className="flex space-x-4 text-sm">
                  <span className="text-green-600">{votes.yes} Yes</span>
                  <span className="text-red-600">{votes.no} No</span>
                  <span className="text-yellow-600">{votes.abstain} Abstain</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Party Preferences */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">Party Preferences</h4>
          <div className="space-y-2">
            {Object.entries(demographic_breakdown.party_preferences).map(([party, percentages]: [string, any]) => (
              <div key={party} className="flex items-center justify-between">
                <span className="text-sm text-gray-600">{party}</span>
                <div className="flex space-x-4 text-sm">
                  <span className="text-green-600">{percentages.yes}% Yes</span>
                  <span className="text-red-600">{percentages.no}% No</span>
                  <span className="text-yellow-600">{percentages.abstain}% Abstain</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Voting Trends */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Voting Trends</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-lg font-semibold text-blue-900">
              {voting_trends.peak_voting_time}
            </div>
            <div className="text-sm text-blue-700">Peak Voting Time</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-lg font-semibold text-green-900 capitalize">
              {voting_trends.voting_momentum}
            </div>
            <div className="text-sm text-green-700">Voting Momentum</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-lg font-semibold text-purple-900 capitalize">
              {voting_trends.constituency_spread}
            </div>
            <div className="text-sm text-purple-700">Constituency Spread</div>
          </div>
        </div>

        {/* Daily Voting Chart */}
        <div className="mt-6">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Daily Voting Activity</h4>
          <div className="grid grid-cols-6 gap-2">
            {Object.entries(voting_trends.daily_voting).map(([date, votes]: [string, any]) => (
              <div key={date} className="text-center">
                <div className="text-xs text-gray-500 mb-1">
                  {new Date(date).toLocaleDateString('en-CA', { month: 'short', day: 'numeric' })}
                </div>
                <div className="text-sm font-medium text-gray-900">{votes}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Individual User Votes */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">Recent User Votes</h3>
          <button
            onClick={() => setShowUserVotes(!showUserVotes)}
            className="flex items-center text-sm text-op-blue hover:text-op-blue-700 transition-colors"
          >
            {showUserVotes ? <EyeSlashIcon className="h-4 w-4 mr-2" /> : <EyeIcon className="h-4 w-4 mr-2" />}
            {showUserVotes ? 'Hide' : 'Show'} Individual Votes
          </button>
        </div>

        {showUserVotes && (
          <div className="space-y-4">
            {userVotes.map((vote) => (
              <div key={vote.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      {getVoteIcon(vote.vote_choice)}
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getVoteColor(vote.vote_choice)}`}>
                        {vote.vote_choice.charAt(0).toUpperCase() + vote.vote_choice.slice(1)}
                      </span>
                      <span className="text-sm text-gray-500">
                        {new Date(vote.vote_date).toLocaleDateString()}
                      </span>
                    </div>
                    
                    <p className="text-sm text-gray-700 mb-2">{vote.reason}</p>
                    
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      {vote.constituency && (
                        <div className="flex items-center">
                          <MapPinIcon className="h-3 w-3 mr-1" />
                          {vote.constituency}
                        </div>
                      )}
                      {vote.party_preference && (
                        <div className="flex items-center">
                          <FlagIcon className="h-3 w-3 mr-1" />
                          {vote.party_preference}
                        </div>
                      )}
                      <div className="flex items-center">
                        <ChartBarIcon className="h-3 w-3 mr-1" />
                        {vote.confidence_level} confidence
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Pagination */}
            <div className="flex justify-center space-x-2 mt-4">
              <button
                onClick={() => loadMoreUserVotes(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-3 py-1 text-sm border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Previous
              </button>
              <span className="px-3 py-1 text-sm text-gray-600">
                Page {currentPage}
              </span>
              <button
                onClick={() => loadMoreUserVotes(currentPage + 1)}
                disabled={userVotes.length < pageSize}
                className="px-3 py-1 text-sm border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
