'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Study {
  id: number;
  title: string;
  startDate: string;
  status: 'active' | 'completed' | 'suspended';
  meetingsHeld: number;
  witnessesHeard: number;
  reportDue?: string;
}

interface ActiveStudiesProps {
  committeeId: number;
}

export default function ActiveStudies({ committeeId }: ActiveStudiesProps) {
  const [studies, setStudies] = useState<Study[]>([]);
  const [loading, setLoading] = useState(true);

  // In production, this would fetch actual studies data from the API
  useEffect(() => {
    setTimeout(() => {
      setStudies([
        {
          id: 1,
          title: 'Climate Change Impacts on Northern Communities',
          startDate: '2025-05-15',
          status: 'active',
          meetingsHeld: 8,
          witnessesHeard: 24,
          reportDue: '2025-09-30',
        },
        {
          id: 2,
          title: 'Mental Health Support Framework',
          startDate: '2025-04-20',
          status: 'active',
          meetingsHeld: 12,
          witnessesHeard: 36,
          reportDue: '2025-08-15',
        },
        {
          id: 3,
          title: 'Economic Recovery Post-Pandemic',
          startDate: '2025-03-10',
          status: 'completed',
          meetingsHeld: 15,
          witnessesHeard: 45,
        },
      ]);
      setLoading(false);
    }, 500);
  }, [committeeId]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-gray-100 text-gray-800';
      case 'suspended': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2].map(i => (
          <div key={i} className="animate-pulse">
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  const activeStudies = studies.filter(s => s.status === 'active');

  if (activeStudies.length === 0) {
    return (
      <div className="text-gray-500 text-center py-4">
        No active studies at this time.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {activeStudies.map((study) => (
        <div key={study.id} className="border border-gray-200 rounded-lg p-4">
          <div className="flex items-start justify-between mb-2">
            <h4 className="font-medium text-gray-900 flex-1 pr-2">
              {study.title}
            </h4>
            <span className={`text-xs px-2 py-0.5 rounded ${getStatusColor(study.status)}`}>
              {study.status}
            </span>
          </div>
          
          <div className="grid grid-cols-2 gap-2 text-sm text-gray-600 mb-3">
            <div>
              <span className="font-medium">{study.meetingsHeld}</span> meetings
            </div>
            <div>
              <span className="font-medium">{study.witnessesHeard}</span> witnesses
            </div>
          </div>

          {study.reportDue && (
            <p className="text-xs text-gray-500 mb-2">
              Report due: {new Date(study.reportDue).toLocaleDateString('en-CA', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </p>
          )}

          <Link
            href={`/committees/${committeeId}/studies/${study.id}`}
            className="text-sm text-op-blue hover:underline"
          >
            View study details →
          </Link>
        </div>
      ))}

      <div className="text-center pt-2">
        <Link
          href={`/committees/${committeeId}/studies`}
          className="text-sm text-op-blue hover:underline"
        >
          View all studies ({studies.length})
        </Link>
      </div>
    </div>
  );
}
