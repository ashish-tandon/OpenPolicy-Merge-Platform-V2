'use client';

import { 
  ClockIcon, 
  DocumentTextIcon, 
  UserIcon, 
  FlagIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { BillHistoryItem } from '@/types/bills';

interface BillHistoryProps {
  history: BillHistoryItem[];
}

export default function BillHistory({ history }: BillHistoryProps) {
  if (!history || history.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
        <ClockIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No History Available</h3>
        <p className="text-gray-600">
          Legislative history for this bill is not available yet.
        </p>
      </div>
    );
  }

  const getStatusIcon = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'introduced':
        return <DocumentTextIcon className="h-5 w-5 text-blue-600" />;
      case 'first reading':
        return <DocumentTextIcon className="h-5 w-5 text-blue-600" />;
      case 'second reading':
        return <DocumentTextIcon className="h-5 w-5 text-blue-600" />;
      case 'third reading':
        return <DocumentTextIcon className="h-5 w-5 text-blue-600" />;
      case 'committee':
        return <UserIcon className="h-5 w-5 text-green-600" />;
      case 'amended':
        return <DocumentTextIcon className="h-5 w-5 text-yellow-600" />;
      case 'passed':
        return <CheckCircleIcon className="h-5 w-5 text-green-600" />;
      case 'failed':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-600" />;
      case 'withdrawn':
        return <FlagIcon className="h-5 w-5 text-gray-600" />;
      default:
        return <InformationCircleIcon className="h-5 w-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'introduced':
      case 'first reading':
      case 'second reading':
      case 'third reading':
        return 'bg-blue-100 text-blue-800';
      case 'committee':
        return 'bg-green-100 text-green-800';
      case 'amended':
        return 'bg-yellow-100 text-yellow-800';
      case 'passed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'withdrawn':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusDescription = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'introduced':
        return 'Bill introduced to Parliament';
      case 'first reading':
        return 'First reading in the House';
      case 'second reading':
        return 'Second reading and debate';
      case 'third reading':
        return 'Final reading and vote';
      case 'committee':
        return 'Under committee review';
      case 'amended':
        return 'Bill amended during process';
      case 'passed':
        return 'Bill passed by Parliament';
      case 'failed':
        return 'Bill failed to pass';
      case 'withdrawn':
        return 'Bill withdrawn by sponsor';
      default:
        return 'Legislative action taken';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Legislative History</h3>
        <p className="text-sm text-gray-600 mt-1">
          Timeline of key events in this bill's apos;s journey through Parliament
        </p>
      </div>

      <div className="p-6">
        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-200"></div>

          {/* Timeline Items */}
          <div className="space-y-6">
            {history.map((item, index) => (
              <div key={index} className="relative flex items-start space-x-4">
                {/* Timeline Dot */}
                <div className="relative z-10 flex-shrink-0">
                  <div className="h-12 w-12 rounded-full bg-white border-2 border-gray-200 flex items-center justify-center">
                    {getStatusIcon(item.status)}
                  </div>
                </div>

                {/* Timeline Content */}
                <div className="flex-1 min-w-0">
                  <div className="bg-gray-50 rounded-lg p-4">
                    {/* Status Header */}
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <span className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(item.status)}`}>
                          {item.status}
                        </span>
                        {item.chamber && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                            {item.chamber}
                          </span>
                        )}
                      </div>
                      
                      {item.date && (
                        <div className="text-sm text-gray-500">
                          {format(new Date(item.date), 'MMM dd, yyyy')}
                        </div>
                      )}
                    </div>

                    {/* Description */}
                    {item.description && (
                      <p className="text-gray-700 mb-3">{item.description}</p>
                    )}

                    {/* Additional Details */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      {/* Date Details */}
                      {item.date && (
                        <div>
                          <span className="font-medium text-gray-900">Date:</span>
                          <span className="ml-2 text-gray-600">
                            {format(new Date(item.date), 'EEEE, MMMM dd, yyyy')}
                          </span>
                        </div>
                      )}

                      {/* Session */}
                      {item.session && (
                        <div>
                          <span className="font-medium text-gray-900">Session:</span>
                          <span className="ml-2 text-gray-600">{item.session}</span>
                        </div>
                      )}

                      {/* Committee */}
                      {item.committee && (
                        <div>
                          <span className="font-medium text-gray-900">Committee:</span>
                          <span className="ml-2 text-gray-600">{item.committee}</span>
                        </div>
                      )}

                      {/* Vote Results */}
                      {item.voteResult && (
                        <div>
                          <span className="font-medium text-gray-900">Vote Result:</span>
                          <span className={`ml-2 px-2 py-1 rounded text-xs font-medium ${
                            item.voteResult === 'passed' ? 'bg-green-100 text-green-800' :
                            item.voteResult === 'failed' ? 'bg-red-100 text-red-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {item.voteResult}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Vote Breakdown */}
                    {item.voteBreakdown && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <h4 className="font-medium text-gray-900 mb-3">Vote Breakdown</h4>
                        <div className="grid grid-cols-3 gap-4 text-center">
                          <div>
                            <div className="text-lg font-semibold text-green-600">
                              {item.voteBreakdown.yes || 0}
                            </div>
                            <div className="text-sm text-gray-600">Yes</div>
                          </div>
                          <div>
                            <div className="text-lg font-semibold text-red-600">
                              {item.voteBreakdown.no || 0}
                            </div>
                            <div className="text-sm text-gray-600">No</div>
                          </div>
                          <div>
                            <div className="text-lg font-semibold text-yellow-600">
                              {item.voteBreakdown.abstain || 0}
                            </div>
                            <div className="text-sm text-gray-600">Abstain</div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Notes */}
                    {item.notes && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <h4 className="font-medium text-gray-900 mb-2">Notes</h4>
                        <p className="text-sm text-gray-600">{item.notes}</p>
                      </div>
                    )}

                    {/* Related Documents */}
                    {item.relatedDocuments && item.relatedDocuments.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <h4 className="font-medium text-gray-900 mb-2">Related Documents</h4>
                        <div className="space-y-2">
                          {item.relatedDocuments.map((doc, docIndex) => (
                            <div key={docIndex} className="flex items-center space-x-2 text-sm">
                              <DocumentTextIcon className="h-4 w-4 text-gray-400" />
                              <a
                                href={doc.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-op-blue hover:text-op-blue-700 hover:underline"
                              >
                                {doc.title}
                              </a>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
