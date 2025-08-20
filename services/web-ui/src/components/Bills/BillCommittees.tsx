'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface CommitteeReview {
  id: number;
  committeeName: string;
  committeeSlug: string;
  startDate: string;
  endDate?: string;
  status: 'ongoing' | 'completed';
  meetingsCount: number;
  witnessesCount: number;
  amendmentsProposed: number;
}

interface BillCommitteesProps {
  billId: number;
}

export default function BillCommittees({ billId }: BillCommitteesProps) {
  const [committees, setCommittees] = useState<CommitteeReview[]>([
    {
      id: 1,
      committeeName: 'Standing Committee on Justice and Human Rights',
      committeeSlug: 'justice',
      startDate: '2025-05-15',
      status: 'ongoing',
      meetingsCount: 5,
      witnessesCount: 23,
      amendmentsProposed: 7,
    },
    {
      id: 2,
      committeeName: 'Standing Committee on Public Safety',
      committeeSlug: 'public-safety',
      startDate: '2025-04-20',
      endDate: '2025-05-10',
      status: 'completed',
      meetingsCount: 3,
      witnessesCount: 15,
      amendmentsProposed: 3,
    },
  ]);
  const [loading, setLoading] = useState(false);

  // In production, this would fetch real committee data
  useEffect(() => {
    // Placeholder for fetching committee reviews
  }, [billId]);

  if (loading) {
    return <div className="text-gray-500">Loading committee information...</div>;
  }

  if (committees.length === 0) {
    return (
      <div className="text-gray-500">
        This bill has not been reviewed by any committees yet.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {committees.map((committee) => (
        <div key={committee.id} className="border border-gray-200 rounded-lg p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <Link
                href={`/committees/${committee.committeeSlug}`}
                className="text-lg font-medium text-op-blue hover:underline"
              >
                {committee.committeeName}
              </Link>
              <p className="text-sm text-gray-600 mt-1">
                {committee.startDate && new Date(committee.startDate).toLocaleDateString('en-CA', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
                {committee.endDate && ` - ${new Date(committee.endDate).toLocaleDateString('en-CA', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}`}
              </p>
            </div>
            <span className={`px-3 py-1 rounded text-sm font-medium ${
              committee.status === 'ongoing'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-800'
            }`}>
              {committee.status === 'ongoing' ? 'Ongoing Review' : 'Review Complete'}
            </span>
          </div>

          {/* Statistics */}
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-2xl font-bold text-gray-700">{committee.meetingsCount}</div>
              <div className="text-xs text-gray-600">Meetings</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-2xl font-bold text-gray-700">{committee.witnessesCount}</div>
              <div className="text-xs text-gray-600">Witnesses</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-2xl font-bold text-gray-700">{committee.amendmentsProposed}</div>
              <div className="text-xs text-gray-600">Amendments</div>
            </div>
          </div>

          {/* Key Activities */}
          <div className="space-y-2">
            <h4 className="font-medium text-gray-700">Recent Activities:</h4>
            <ul className="space-y-1 text-sm text-gray-600">
              <li className="flex items-start">
                <span className="text-gray-400 mr-2">•</span>
                Heard testimony from civil liberties organizations
              </li>
              <li className="flex items-start">
                <span className="text-gray-400 mr-2">•</span>
                Reviewed departmental impact assessments
              </li>
              <li className="flex items-start">
                <span className="text-gray-400 mr-2">•</span>
                Proposed amendments to sections 3 and 5
              </li>
            </ul>
          </div>

          {/* Actions */}
          <div className="mt-4 pt-4 border-t border-gray-200 flex items-center gap-4">
            <Link
              href={`/committees/${committee.committeeSlug}/meetings?bill=${billId}`}
              className="text-sm text-op-blue hover:underline"
            >
              View meeting transcripts
            </Link>
            <Link
              href={`/committees/${committee.committeeSlug}/reports?bill=${billId}`}
              className="text-sm text-op-blue hover:underline"
            >
              Committee reports
            </Link>
            <Link
              href={`/committees/${committee.committeeSlug}/witnesses?bill=${billId}`}
              className="text-sm text-op-blue hover:underline"
            >
              Witness list
            </Link>
          </div>
        </div>
      ))}

      {/* Related Information */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">Committee Stage Process</h4>
        <p className="text-sm text-blue-800">
          During committee review, members examine the bill clause-by-clause, hear from witnesses, 
          and may propose amendments. Committee reports are then presented back to the House for consideration.
        </p>
      </div>
    </div>
  );
}
