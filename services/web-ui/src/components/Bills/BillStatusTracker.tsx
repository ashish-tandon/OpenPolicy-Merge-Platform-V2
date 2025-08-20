'use client';

import { Bill } from '@/lib/api';

interface BillStatusTrackerProps {
  bill: Bill;
}

interface Stage {
  name: string;
  chamber: 'House' | 'Senate' | 'Royal';
  status: 'completed' | 'current' | 'upcoming';
  date?: string;
}

export default function BillStatusTracker({ bill }: BillStatusTrackerProps) {
  // This would be populated from real bill progress data
  const stages: Stage[] = [
    { name: 'First Reading', chamber: 'House', status: 'completed', date: bill.introduced || undefined },
    { name: 'Second Reading', chamber: 'House', status: 'completed' },
    { name: 'Committee Stage', chamber: 'House', status: 'current' },
    { name: 'Report Stage', chamber: 'House', status: 'upcoming' },
    { name: 'Third Reading', chamber: 'House', status: 'upcoming' },
    { name: 'First Reading', chamber: 'Senate', status: 'upcoming' },
    { name: 'Second Reading', chamber: 'Senate', status: 'upcoming' },
    { name: 'Committee Stage', chamber: 'Senate', status: 'upcoming' },
    { name: 'Third Reading', chamber: 'Senate', status: 'upcoming' },
    { name: 'Royal Assent', chamber: 'Royal', status: bill.law ? 'completed' : 'upcoming' },
  ];

  const getChamberColor = (chamber: string) => {
    switch (chamber) {
      case 'House': return 'bg-green-100 text-green-800 border-green-300';
      case 'Senate': return 'bg-red-100 text-red-800 border-red-300';
      case 'Royal': return 'bg-purple-100 text-purple-800 border-purple-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'current':
        return (
          <div className="w-5 h-5 rounded-full bg-op-blue animate-pulse" />
        );
      case 'upcoming':
        return (
          <div className="w-5 h-5 rounded-full bg-gray-300" />
        );
      default:
        return null;
    }
  };

  return (
    <div>
      {/* Timeline */}
      <div className="relative">
        {stages.map((stage, index) => (
          <div key={index} className="flex items-center mb-4 last:mb-0">
            {/* Icon */}
            <div className="flex-shrink-0 w-10 h-10 flex items-center justify-center">
              {getStatusIcon(stage.status)}
            </div>

            {/* Connecting Line */}
            {index < stages.length - 1 && (
              <div className="absolute left-5 top-10 w-0.5 h-full bg-gray-300" />
            )}

            {/* Stage Info */}
            <div className="ml-4 flex-1">
              <div className="flex items-center gap-3">
                <h3 className={`font-medium ${
                  stage.status === 'completed' ? 'text-gray-900' : 'text-gray-500'
                }`}>
                  {stage.name}
                </h3>
                <span className={`text-xs px-2 py-0.5 rounded border ${getChamberColor(stage.chamber)}`}>
                  {stage.chamber === 'Royal' ? 'Crown' : stage.chamber}
                </span>
              </div>
              {stage.date && (
                <p className="text-sm text-gray-500 mt-1">
                  {new Date(stage.date).toLocaleDateString('en-CA', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className="flex flex-wrap gap-6 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-green-600"></div>
            <span className="text-gray-600">Completed</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-op-blue animate-pulse"></div>
            <span className="text-gray-600">Current Stage</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-gray-300"></div>
            <span className="text-gray-600">Upcoming</span>
          </div>
        </div>
      </div>
    </div>
  );
}
