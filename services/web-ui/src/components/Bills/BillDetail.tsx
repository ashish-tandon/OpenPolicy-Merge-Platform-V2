'use client';

import { useState } from 'react';
import { 
  CalendarIcon, 
  UserIcon, 
  DocumentTextIcon, 
  FlagIcon,
  BookmarkIcon,
  ShareIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { Bill } from '@/types/bills';
import BillVoteCasting from './BillVoteCasting';
import BillPublicVoting from './BillPublicVoting';
import BillChat from '../chat/BillChat';

interface BillDetailProps {
  bill: Bill;
}

export default function BillDetail({ bill }: BillDetailProps) {
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = () => {
    setIsSaved(!isSaved);
    // TODO: Implement save functionality with User Service
    console.log('Save bill:', bill.id);
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: bill.title,
        text: bill.description || `Check out this bill: ${bill.title}`,
        url: window.location.href,
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      // TODO: Add toast notification
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'passed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'in progress':
      case 'active':
        return 'bg-blue-100 text-blue-800';
      case 'withdrawn':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'passed':
        return '✅';
      case 'failed':
        return '❌';
      case 'in progress':
      case 'active':
        return '🔄';
      case 'withdrawn':
        return '⏸️';
      default:
        return '📋';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Bill Header */}
      <div className="bg-gradient-to-r from-op-blue to-op-blue-700 px-6 py-8 text-white">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            {/* Bill Number and Type */}
            <div className="flex items-center space-x-3 mb-4">
              <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">
                {bill.billNumber || 'Bill'}
              </span>
              <span className="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">
                {bill.type || 'Government Bill'}
              </span>
            </div>

            {/* Bill Title */}
            <h1 className="text-3xl font-bold mb-4 leading-tight">
              {bill.title}
            </h1>

            {/* Bill Description */}
            {bill.description && (
              <p className="text-lg text-white/90 leading-relaxed">
                {bill.description}
              </p>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col space-y-3 ml-6">
            <button
              onClick={handleSave}
              className={`p-3 rounded-full transition-colors ${
                isSaved 
                  ? 'bg-white text-op-blue' 
                  : 'bg-white/20 hover:bg-white/30 text-white'
              }`}
              title={isSaved ? 'Remove from saved' : 'Save bill'}
            >
              <BookmarkIcon className="h-5 w-5" />
            </button>
            
            <button
              onClick={handleShare}
              className="p-3 rounded-full bg-white/20 hover:bg-white/30 text-white transition-colors"
              title="Share bill"
            >
              <ShareIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Bill Content */}
      <div className="p-6">
        {/* Status and Key Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Status */}
          <div className="text-center">
            <div className="text-2xl mb-2">{getStatusIcon(bill.status)}</div>
            <div className="text-sm text-gray-600 mb-1">Status</div>
            <span className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(bill.status)}`}>
              {bill.status || 'Unknown'}
            </span>
          </div>

          {/* Introduced Date */}
          <div className="text-center">
            <CalendarIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <div className="text-sm text-gray-600 mb-1">Introduced</div>
            <div className="font-medium text-gray-900">
              {bill.introducedDate 
                ? format(new Date(bill.introducedDate), 'MMM dd, yyyy')
                : 'Not specified'
              }
            </div>
          </div>

          {/* Sponsor */}
          <div className="text-center">
            <UserIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <div className="text-sm text-gray-600 mb-1">Sponsor</div>
            <div className="font-medium text-gray-900">
              {bill.sponsor || 'Not specified'}
            </div>
          </div>

          {/* Bill Type */}
          <div className="text-center">
            <DocumentTextIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <div className="text-sm text-gray-600 mb-1">Type</div>
            <div className="font-medium text-gray-900">
              {bill.billType || 'Not specified'}
            </div>
          </div>
        </div>

        {/* Additional Details */}
        {(bill.summary || bill.keywords || bill.relatedBills) && (
          <div className="space-y-6">
            {/* Bill Summary */}
            {bill.summary && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Summary</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-700 leading-relaxed">{bill.summary}</p>
                </div>
              </div>
            )}

            {/* Keywords/Tags */}
            {bill.keywords && bill.keywords.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {bill.keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-op-blue/10 text-op-blue text-sm rounded-full border border-op-blue/20"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Related Bills */}
            {bill.relatedBills && bill.relatedBills.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Related Bills</h3>
                <div className="space-y-2">
                  {bill.relatedBills.map((relatedBill, index) => (
                    <div
                      key={index}
                      className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <DocumentTextIcon className="h-5 w-5 text-gray-400 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 truncate">
                          {relatedBill.title}
                        </div>
                        <div className="text-sm text-gray-500">
                          {relatedBill.billNumber} • {relatedBill.status}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Bill Vote Casting System */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Cast Your Vote</h3>
          <BillVoteCasting
            billId={bill.id}
            billTitle={bill.title}
            billNumber={bill.billNumber || 'Unknown'}
            userId="demo-user-123" // TODO: Replace with actual user ID from auth
            onVoteCast={(voteData) => {
              console.log('Vote cast:', voteData);
              // TODO: Refresh public voting data
            }}
          />
        </div>

        {/* Public Voting Results */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Public Opinion</h3>
          <BillPublicVoting
            billId={bill.id}
            billTitle={bill.title}
            billNumber={bill.billNumber || 'Unknown'}
          />
        </div>

        {/* AI Chat Assistant */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Chat Assistant</h3>
          <BillChat
            billNumber={bill.billNumber || 'Unknown'}
            billTitle={bill.title}
            billSummary={bill.description}
            userId="demo-user-123" // TODO: Replace with actual user ID from auth
          />
        </div>
      </div>
    </div>
  );
}
