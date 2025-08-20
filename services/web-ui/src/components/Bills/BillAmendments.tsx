'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Amendment {
  id: number;
  number: string;
  clause: string;
  proposedBy: {
    name: string;
    party: string;
    mpSlug: string;
  };
  date: string;
  status: 'adopted' | 'rejected' | 'withdrawn' | 'pending';
  description: string;
  type: 'addition' | 'deletion' | 'modification';
}

interface BillAmendmentsProps {
  billId: number;
}

export default function BillAmendments({ billId }: BillAmendmentsProps) {
  const [amendments, setAmendments] = useState<Amendment[]>([
    {
      id: 1,
      number: 'NDP-1',
      clause: '3',
      proposedBy: {
        name: 'Sarah Johnson',
        party: 'NDP',
        mpSlug: 'sarah-johnson',
      },
      date: '2025-05-20',
      status: 'adopted',
      description: 'Add provision for judicial discretion in sentencing',
      type: 'addition',
    },
    {
      id: 2,
      number: 'CPC-3',
      clause: '5(2)',
      proposedBy: {
        name: 'John Doe',
        party: 'Conservative',
        mpSlug: 'john-doe',
      },
      date: '2025-05-22',
      status: 'rejected',
      description: 'Remove clause regarding mandatory review periods',
      type: 'deletion',
    },
    {
      id: 3,
      number: 'LPC-2',
      clause: '7',
      proposedBy: {
        name: 'Jane Smith',
        party: 'Liberal',
        mpSlug: 'jane-smith',
      },
      date: '2025-05-25',
      status: 'pending',
      description: 'Modify implementation timeline from 6 months to 12 months',
      type: 'modification',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');

  // In production, this would fetch real amendment data
  useEffect(() => {
    // Placeholder for fetching amendments
  }, [billId]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'adopted': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'withdrawn': return 'bg-gray-100 text-gray-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'addition':
        return <span className="text-green-600">+</span>;
      case 'deletion':
        return <span className="text-red-600">−</span>;
      case 'modification':
        return <span className="text-blue-600">≈</span>;
      default:
        return null;
    }
  };

  const getPartyColor = (party: string) => {
    switch (party.toLowerCase()) {
      case 'liberal': return 'text-red-600';
      case 'conservative': return 'text-blue-600';
      case 'ndp': return 'text-orange-600';
      case 'bloc': return 'text-cyan-600';
      case 'green': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  const filteredAmendments = filter === 'all' 
    ? amendments 
    : amendments.filter(a => a.status === filter);

  if (loading) {
    return <div className="text-gray-500">Loading amendments...</div>;
  }

  return (
    <div>
      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-gray-700">{amendments.length}</div>
          <div className="text-sm text-gray-600">Total Amendments</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">
            {amendments.filter(a => a.status === 'adopted').length}
          </div>
          <div className="text-sm text-gray-600">Adopted</div>
        </div>
        <div className="bg-red-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-red-600">
            {amendments.filter(a => a.status === 'rejected').length}
          </div>
          <div className="text-sm text-gray-600">Rejected</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-yellow-600">
            {amendments.filter(a => a.status === 'pending').length}
          </div>
          <div className="text-sm text-gray-600">Pending</div>
        </div>
      </div>

      {/* Filter */}
      <div className="mb-4">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          <option value="all">All Amendments</option>
          <option value="adopted">Adopted Only</option>
          <option value="rejected">Rejected Only</option>
          <option value="pending">Pending Only</option>
          <option value="withdrawn">Withdrawn Only</option>
        </select>
      </div>

      {/* Amendments List */}
      {filteredAmendments.length === 0 ? (
        <div className="text-gray-500">
          No amendments found matching your filter.
        </div>
      ) : (
        <div className="space-y-4">
          {filteredAmendments.map((amendment) => (
            <div key={amendment.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold">{getTypeIcon(amendment.type)}</span>
                  <div>
                    <h4 className="font-medium text-gray-900">
                      Amendment {amendment.number} - Clause {amendment.clause}
                    </h4>
                    <p className="text-sm text-gray-600">
                      Proposed by{' '}
                      <Link
                        href={`/mps/${amendment.proposedBy.mpSlug}`}
                        className={`font-medium hover:underline ${getPartyColor(amendment.proposedBy.party)}`}
                      >
                        {amendment.proposedBy.name}
                      </Link>
                      {' '}({amendment.proposedBy.party}) on {new Date(amendment.date).toLocaleDateString('en-CA')}
                    </p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded text-sm font-medium ${getStatusColor(amendment.status)}`}>
                  {amendment.status.charAt(0).toUpperCase() + amendment.status.slice(1)}
                </span>
              </div>

              <p className="text-gray-700 mb-3">{amendment.description}</p>

              {amendment.status === 'pending' && (
                <div className="bg-yellow-50 border border-yellow-200 rounded p-3 text-sm">
                  <p className="text-yellow-800">
                    This amendment is pending committee vote. Expected decision by next week.
                  </p>
                </div>
              )}

              <div className="mt-3 flex items-center gap-4 text-sm">
                <button className="text-op-blue hover:underline">
                  View full text
                </button>
                <button className="text-op-blue hover:underline">
                  See debate
                </button>
                {amendment.status !== 'pending' && (
                  <button className="text-op-blue hover:underline">
                    Vote details
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Information Box */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-700 mb-2">About Amendments</h4>
        <p className="text-sm text-gray-600">
          Amendments can be proposed during committee stage or report stage. They may add new provisions, 
          remove existing ones, or modify the text. All amendments must be voted on by the committee or 
          the House before being incorporated into the bill.
        </p>
      </div>
    </div>
  );
}
