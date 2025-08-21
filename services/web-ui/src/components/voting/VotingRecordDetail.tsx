'use client';
            
import { useState } from 'react';
import Link from 'next/link';
import { 
  CalendarIcon, 
  DocumentTextIcon, 
  CheckCircleIcon, 
  XCircleIcon, 
  MinusIcon,
  UserGroupIcon,
  ChartBarIcon,
  FlagIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { VoteRecord } from '@/types/voting';
            
interface VotingRecordDetailProps {
  votingRecord: any; // Using any for now since the API response structure may vary
}
            
export default function VotingRecordDetail({ votingRecord }: VotingRecordDetailProps) {
  const [showDetailedBreakdown, setShowDetailedBreakdown] = useState(false);
            
  const getResultColor = (result: string) => {
    switch (result?.toLowerCase()) {
      case 'passed':
        return 'bg-green-100 text-green-800';
      case 'defeated':
        return 'bg-red-100 text-red-800';
      case 'tied':
        return 'bg-yellow-100 text-yellow-800';
      case 'withdrawn':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
            
  const getTypeColor = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'division':
        return 'bg-blue-100 text-blue-800';
      case 'voice':
        return 'bg-purple-100 text-purple-800';
      case 'unanimous':
        return 'bg-green-100 text-green-800';
      case 'recorded':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
            
  return (
    <div className="space-y-6">
      {/* Main Vote Information */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Vote on {votingRecord.bill_title || 'Parliamentary Bill'}
            </h1>
            
            {votingRecord.bill_number && (
              <p className="text-lg text-gray-600 mb-4">
                Bill {votingRecord.bill_number}
              </p>
            )}
            
            {votingRecord.description && (
              <p className="text-gray-700 mb-4">{votingRecord.description}</p>
            )}
          </div>
          
          <div className="ml-6 text-right space-y-2">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getResultColor(votingRecord.result)}`}>
              {votingRecord.result?.charAt(0).toUpperCase() + votingRecord.result?.slice(1) || 'Unknown'}
            </span>
            
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(votingRecord.type)}`}>
              {votingRecord.type?.charAt(0).toUpperCase() + votingRecord.type?.slice(1) || 'Division'}
            </span>
          </div>
        </div>
        
        {/* Vote Details Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="flex items-center space-x-3">
            <CalendarIcon className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-900">Vote Date</p>
              <p className="text-sm text-gray-600">
                {votingRecord.date ? format(new Date(votingRecord.date), 'MMM dd, yyyy') : 'Unknown'}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <UserGroupIcon className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-900">Total Votes</p>
              <p className="text-sm text-gray-600">{votingRecord.total_votes || 'Unknown'}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <ChartBarIcon className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-900">Turnout</p>
              <p className="text-sm text-gray-600">{votingRecord.turnout_percentage || 'Unknown'}%</p>
            </div>
          </div>
        </div>
        
        {/* Vote Breakdown */}
        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Vote Breakdown</h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {votingRecord.yes_votes || votingRecord.yea_total || 0}
              </div>
              <div className="text-sm text-gray-500">Yes</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {votingRecord.no_votes || votingRecord.nay_total || 0}
              </div>
              <div className="text-sm text-gray-500">No</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {votingRecord.abstentions || 0}
              </div>
              <div className="text-sm text-gray-500">Abstain</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-600">
                {votingRecord.absences || 0}
              </div>
              <div className="text-sm text-gray-500">Absent</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Bill Information */}
      {votingRecord.bill_id && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Related Bill</h3>
          
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-lg font-medium text-gray-900">
                {votingRecord.bill_title || 'Unknown Bill'}
              </h4>
              {votingRecord.bill_number && (
                <p className="text-gray-600">Bill {votingRecord.bill_number}</p>
              )}
            </div>
            
            <Link
              href={`/bills/${votingRecord.bill_id}`}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-op-blue hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue transition-colors"
            >
              View Bill
            </Link>
          </div>
        </div>
      )}
      
      {/* Vote Context */}
      {votingRecord.vote_context && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Vote Context</h3>
          <p className="text-gray-700">{votingRecord.vote_context}</p>
        </div>
      )}
      
      {/* Government and Opposition Positions */}
      {(votingRecord.government_position || votingRecord.opposition_position) && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Party Positions</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {votingRecord.government_position && (
              <div className="flex items-center space-x-3">
                <BuildingOfficeIcon className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Government Position</p>
                  <p className="text-sm text-gray-600 capitalize">
                    {votingRecord.government_position}
                  </p>
                </div>
              </div>
            )}
            
            {votingRecord.opposition_position && (
              <div className="flex items-center space-x-3">
                <FlagIcon className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Opposition Position</p>
                  <p className="text-sm text-gray-600 capitalize">
                    {votingRecord.opposition_position}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* Whip Status */}
      {votingRecord.whip_status && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Whip Status</h3>
          <p className="text-gray-700 capitalize">
            {votingRecord.whip_status === 'whipped' ? 'Party whip applied' : 
             votingRecord.whip_status === 'free' ? 'Free vote allowed' : 
             votingRecord.whip_status === 'rebel' ? 'Rebel vote detected' : 
             votingRecord.whip_status}
          </p>
        </div>
      )}
      
      {/* Additional Information */}
      {(votingRecord.related_amendment || votingRecord.committee_recommendation || votingRecord.constituency_impact) && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Additional Information</h3>
          
          <div className="space-y-3">
            {votingRecord.related_amendment && (
              <div>
                <p className="text-sm font-medium text-gray-900">Related Amendment</p>
                <p className="text-sm text-gray-600">{votingRecord.related_amendment}</p>
              </div>
            )}
            
            {votingRecord.committee_recommendation && (
              <div>
                <p className="text-sm font-medium text-gray-900">Committee Recommendation</p>
                <p className="text-sm text-gray-600">{votingRecord.committee_recommendation}</p>
              </div>
            )}
            
            {votingRecord.constituency_impact && (
              <div>
                <p className="text-sm font-medium text-gray-900">Constituency Impact</p>
                <p className="text-sm text-gray-600">{votingRecord.constituency_impact}</p>
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* Source Information */}
      {votingRecord.source && (
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">
            <span className="font-medium">Source:</span> {votingRecord.source}
          </p>
          {votingRecord.last_updated && (
            <p className="text-sm text-gray-600 mt-1">
              <span className="font-medium">Last Updated:</span> {votingRecord.last_updated}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
