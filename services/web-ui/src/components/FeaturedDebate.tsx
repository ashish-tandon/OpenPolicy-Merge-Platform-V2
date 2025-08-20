import Link from 'next/link';
import { Debate } from '@/lib/api';

interface FeaturedDebateProps {
  debate?: Debate;
}

export default function FeaturedDebate({ debate }: FeaturedDebateProps) {
  if (!debate) {
    return (
      <div className="text-gray-500">
        <p>No recent debates available.</p>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-CA', { 
      weekday: 'long',
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  return (
    <div>
      <Link 
        href={`/debates/${debate.date}/${debate.number}`}
        className="block hover:bg-gray-50 -m-2 p-2 rounded"
      >
        <div className="flex items-start justify-between mb-2">
          <div>
            <h3 className="text-lg font-medium text-op-blue hover:underline">
              {formatDate(debate.date)}
            </h3>
            <p className="text-sm text-gray-600">
              Hansard #{debate.number} • Parliament {debate.parliament}, Session {debate.session}
            </p>
          </div>
          <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
            {debate.statements_count} statements
          </span>
        </div>
        
        {(debate.h1_en || debate.h2_en) && (
          <div className="mt-3 space-y-2">
            {debate.h1_en && (
              <p className="text-sm font-medium text-gray-700">
                {debate.h1_en}
              </p>
            )}
            {debate.h2_en && (
              <p className="text-sm text-gray-600">
                {debate.h2_en}
              </p>
            )}
          </div>
        )}

        <div className="mt-4 flex items-center text-sm text-gray-500">
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Full transcript available
        </div>
      </Link>

      {/* Computer-generated summary notice */}
      <div className="mt-4 p-3 bg-blue-50 rounded text-sm">
        <p className="text-blue-800">
          <strong>AI Summary:</strong> Computer-generated summaries for this debate will be available soon. 
          These summaries help identify key topics and speakers.
        </p>
      </div>
    </div>
  );
}
