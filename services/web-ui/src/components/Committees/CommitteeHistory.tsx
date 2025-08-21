'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface HistoricalEvent {
  id: number;
  date: string;
  parliament: string;
  type: 'established' | 'renamed' | 'mandate-change' | 'chair-election' | 'major-study';
  title: string;
  description: string;
  relatedPeople?: { name: string; role: string; mpSlug?: string }[];
}

interface CommitteeHistoryProps {
  committeeId: number;
}

export default function CommitteeHistory({ committeeId }: CommitteeHistoryProps) {
  const [events, setEvents] = useState<HistoricalEvent[]>([]);
  const [loading, setLoading] = useState(true);

  // In production, this would fetch actual historical data from the API
  useEffect(() => {
    setTimeout(() => {
      setEvents([
        {
          id: 1,
          date: '2021-12-16',
          parliament: '44-1',
          type: 'established',
          title: 'Committee Re-established',
          description: 'The Standing Committee was re-established following the 44th general election with a mandate to study matters related to the environment and sustainable development.',
        },
        {
          id: 2,
          date: '2022-02-15',
          parliament: '44-1',
          type: 'chair-election',
          title: 'New Chair Elected',
          description: 'Hon. John Smith was elected as Committee Chair, bringing extensive experience in environmental policy.',
          relatedPeople: [
            { name: 'Hon. John Smith', role: 'Chair', mpSlug: 'john-smith' },
          ],
        },
        {
          id: 3,
          date: '2023-03-20',
          parliament: '44-1',
          type: 'major-study',
          title: 'Landmark Climate Study Completed',
          description: 'The committee completed its comprehensive study on climate adaptation strategies, resulting in 58 recommendations that were largely adopted by the government.',
        },
        {
          id: 4,
          date: '2019-12-13',
          parliament: '43-1',
          type: 'established',
          title: 'Committee Established in 43rd Parliament',
          description: 'Following the 2019 election, the committee was established with 12 members representing all recognized parties.',
        },
        {
          id: 5,
          date: '2020-08-18',
          parliament: '43-1',
          type: 'mandate-change',
          title: 'Mandate Expanded',
          description: 'The committee\'s apos;s mandate was expanded to include oversight of pandemic recovery efforts related to environmental sustainability.',
        },
      ]);
      setLoading(false);
    }, 500);
  }, [committeeId]);

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'established':
        return '🏛️';
      case 'renamed':
        return '📝';
      case 'mandate-change':
        return '📋';
      case 'chair-election':
        return '🗳️';
      case 'major-study':
        return '📚';
      default:
        return '📌';
    }
  };

  const getEventColor = (type: string) => {
    switch (type) {
      case 'established': return 'border-green-400';
      case 'renamed': return 'border-blue-400';
      case 'mandate-change': return 'border-purple-400';
      case 'chair-election': return 'border-yellow-400';
      case 'major-study': return 'border-red-400';
      default: return 'border-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="animate-pulse">
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  // Group events by parliament
  const eventsByParliament = events.reduce((acc, event) => {
    if (!acc[event.parliament]) acc[event.parliament] = [];
    acc[event.parliament].push(event);
    return acc;
  }, {} as Record<string, HistoricalEvent[]>);

  return (
    <div>
      {/* Timeline */}
      <div className="space-y-8">
        {Object.entries(eventsByParliament)
          .sort(([a], [b]) => b.localeCompare(a))
          .map(([parliament, parliamentEvents]) => (
            <div key={parliament}>
              <h3 className="text-lg font-bold text-gray-700 mb-4">
                {parliament.replace('-', 'th Parliament - ')} Session
              </h3>
              
              <div className="space-y-4 ml-8 relative">
                {/* Vertical line */}
                <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-gray-300"></div>
                
                {parliamentEvents
                  .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                  .map((event) => (
                    <div key={event.id} className="relative">
                      {/* Timeline dot */}
                      <div className={`absolute -left-[13px] top-3 w-6 h-6 bg-white border-4 ${getEventColor(event.type)} rounded-full flex items-center justify-center text-xs`}>
                        {getEventIcon(event.type)}
                      </div>
                      
                      {/* Event content */}
                      <div className="ml-8 bg-white border border-gray-200 rounded-lg p-4">
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h4 className="font-medium text-gray-900">
                              {event.title}
                            </h4>
                            <p className="text-sm text-gray-500">
                              {new Date(event.date).toLocaleDateString('en-CA', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                              })}
                            </p>
                          </div>
                          <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                            {event.type.replace('-', ' ')}
                          </span>
                        </div>
                        
                        <p className="text-sm text-gray-700">
                          {event.description}
                        </p>
                        
                        {event.relatedPeople && event.relatedPeople.length > 0 && (
                          <div className="mt-2 text-sm">
                            <span className="text-gray-500">Related: </span>
                            {event.relatedPeople.map((person, index) => (
                              <span key={index}>
                                {person.mpSlug ? (
                                  <Link
                                    href={`/mps/${person.mpSlug}`}
                                    className="text-op-blue hover:underline"
                                  >
                                    {person.name}
                                  </Link>
                                ) : (
                                  <span className="text-gray-700">{person.name}</span>
                                )}
                                <span className="text-gray-500"> ({person.role})</span>
                                {index < event.relatedPeople!.length - 1 && ', '}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          ))}
      </div>

      {/* Historical Note */}
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-700 mb-2">About Committee History</h4>
        <p className="text-sm text-gray-600">
          This timeline shows major events in the committee&apos;s history. Standing committees are 
          typically re-established at the beginning of each Parliament, while their membership 
          and leadership may change throughout the session.
        </p>
      </div>
    </div>
  );
}
