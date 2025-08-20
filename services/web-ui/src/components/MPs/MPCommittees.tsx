'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface CommitteeMembership {
  id: number;
  committeeName: string;
  committeeSlug: string;
  role: 'Member' | 'Chair' | 'Vice-Chair';
  startDate: string;
  endDate?: string;
  current: boolean;
}

interface MPCommitteesProps {
  mpId: number;
}

export default function MPCommittees({ mpId }: MPCommitteesProps) {
  const [committees, setCommittees] = useState<CommitteeMembership[]>([
    {
      id: 1,
      committeeName: 'Standing Committee on Finance',
      committeeSlug: 'finance',
      role: 'Member',
      startDate: '2024-01-15',
      current: true,
    },
    {
      id: 2,
      committeeName: 'Standing Committee on Health',
      committeeSlug: 'health',
      role: 'Vice-Chair',
      startDate: '2024-02-01',
      current: true,
    },
    {
      id: 3,
      committeeName: 'Special Committee on COVID-19',
      committeeSlug: 'covid-19',
      role: 'Member',
      startDate: '2020-04-20',
      endDate: '2021-06-23',
      current: false,
    },
  ]);
  const [loading, setLoading] = useState(false);

  // In production, this would fetch real committee data
  useEffect(() => {
    // Placeholder for fetching committee memberships
  }, [mpId]);

  const currentCommittees = committees.filter(c => c.current);
  const pastCommittees = committees.filter(c => !c.current);

  const getRoleBadge = (role: string) => {
    switch (role) {
      case 'Chair':
        return 'bg-purple-100 text-purple-800';
      case 'Vice-Chair':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div>
      {loading ? (
        <div className="text-gray-500">Loading committee memberships...</div>
      ) : (
        <>
          {/* Current Committees */}
          {currentCommittees.length > 0 && (
            <div className="mb-8">
              <h3 className="text-lg font-bold text-gray-700 mb-4">Current Committee Memberships</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {currentCommittees.map((committee) => (
                  <div key={committee.id} className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <Link
                        href={`/committees/${committee.committeeSlug}`}
                        className="font-medium text-op-blue hover:underline"
                      >
                        {committee.committeeName}
                      </Link>
                      <span className={`text-xs px-2 py-1 rounded ${getRoleBadge(committee.role)}`}>
                        {committee.role}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Since {new Date(committee.startDate).toLocaleDateString('en-CA', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </p>
                    <div className="mt-3 flex items-center gap-3 text-sm">
                      <Link
                        href={`/committees/${committee.committeeSlug}/meetings`}
                        className="text-op-blue hover:underline"
                      >
                        View meetings
                      </Link>
                      <Link
                        href={`/committees/${committee.committeeSlug}/studies`}
                        className="text-op-blue hover:underline"
                      >
                        Current studies
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Past Committees */}
          {pastCommittees.length > 0 && (
            <div>
              <h3 className="text-lg font-bold text-gray-700 mb-4">Past Committee Memberships</h3>
              <div className="space-y-3">
                {pastCommittees.map((committee) => (
                  <div key={committee.id} className="border-b border-gray-200 pb-3">
                    <div className="flex items-center justify-between">
                      <div>
                        <Link
                          href={`/committees/${committee.committeeSlug}`}
                          className="font-medium text-op-blue hover:underline"
                        >
                          {committee.committeeName}
                        </Link>
                        <span className={`ml-2 text-xs px-2 py-0.5 rounded ${getRoleBadge(committee.role)}`}>
                          {committee.role}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">
                        {new Date(committee.startDate).toLocaleDateString('en-CA', {
                          year: 'numeric',
                          month: 'short',
                        })} - {committee.endDate ? new Date(committee.endDate).toLocaleDateString('en-CA', {
                          year: 'numeric',
                          month: 'short',
                        }) : 'Present'}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {committees.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No committee memberships found for this MP.
            </div>
          )}
        </>
      )}
    </div>
  );
}
