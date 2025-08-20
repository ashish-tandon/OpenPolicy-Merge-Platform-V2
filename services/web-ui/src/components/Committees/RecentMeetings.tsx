'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Meeting {
  id: number;
  number: number;
  date: string;
  time: string;
  type: 'regular' | 'special' | 'subcommittee';
  subject: string;
  hasEvidence: boolean;
  hasMinutes: boolean;
  witnessCount: number;
}

interface RecentMeetingsProps {
  committeeId: number;
}

export default function RecentMeetings({ committeeId }: RecentMeetingsProps) {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);

  // In production, this would fetch actual meeting data from the API
  useEffect(() => {
    setTimeout(() => {
      setMeetings([
        {
          id: 1,
          number: 47,
          date: '2025-06-18',
          time: '11:00 AM',
          type: 'regular',
          subject: 'Study on Climate Change Impacts - Witness Testimony',
          hasEvidence: true,
          hasMinutes: true,
          witnessCount: 4,
        },
        {
          id: 2,
          number: 46,
          date: '2025-06-15',
          time: '3:30 PM',
          type: 'regular',
          subject: 'Committee Business - Report Consideration',
          hasEvidence: true,
          hasMinutes: false,
          witnessCount: 0,
        },
        {
          id: 3,
          number: 45,
          date: '2025-06-12',
          time: '11:00 AM',
          type: 'special',
          subject: 'Emergency Meeting - Healthcare Funding Crisis',
          hasEvidence: true,
          hasMinutes: true,
          witnessCount: 6,
        },
      ]);
      setLoading(false);
    }, 500);
  }, [committeeId]);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'special': return 'text-red-600';
      case 'subcommittee': return 'text-purple-600';
      default: return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map(i => (
          <div key={i} className="animate-pulse">
            <div className="h-16 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {meetings.map((meeting) => (
        <div key={meeting.id} className="border-b border-gray-200 pb-3 last:border-0 last:pb-0">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <Link
                  href={`/committees/${committeeId}/meetings/${meeting.number}`}
                  className="font-medium text-op-blue hover:underline"
                >
                  Meeting #{meeting.number}
                </Link>
                {meeting.type !== 'regular' && (
                  <span className={`text-xs font-medium ${getTypeColor(meeting.type)}`}>
                    {meeting.type}
                  </span>
                )}
              </div>
              
              <p className="text-sm text-gray-700 mb-1">
                {meeting.subject}
              </p>
              
              <div className="flex items-center gap-3 text-xs text-gray-500">
                <span>
                  {new Date(meeting.date).toLocaleDateString('en-CA', {
                    weekday: 'short',
                    month: 'short',
                    day: 'numeric',
                  })} at {meeting.time}
                </span>
                {meeting.witnessCount > 0 && (
                  <span>{meeting.witnessCount} witnesses</span>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2 ml-4">
              {meeting.hasEvidence && (
                <Link
                  href={`/committees/${committeeId}/meetings/${meeting.number}/evidence`}
                  className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200"
                  title="Evidence available"
                >
                  Evidence
                </Link>
              )}
              {meeting.hasMinutes && (
                <Link
                  href={`/committees/${committeeId}/meetings/${meeting.number}/minutes`}
                  className="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded hover:bg-gray-200"
                  title="Minutes available"
                >
                  Minutes
                </Link>
              )}
            </div>
          </div>
        </div>
      ))}

      <div className="text-center pt-2">
        <Link
          href={`/committees/${committeeId}/meetings`}
          className="text-sm text-op-blue hover:underline"
        >
          View all meetings
        </Link>
      </div>
    </div>
  );
}
