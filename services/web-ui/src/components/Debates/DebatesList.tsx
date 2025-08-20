'use client';

import Link from 'next/link';
import { Debate } from '@/lib/api';
import Pagination from '@/components/Pagination';

interface DebatesListProps {
  debates: Debate[];
  totalCount: number;
  currentPage: number;
  filters: any;
}

export default function DebatesList({ debates, totalCount, currentPage, filters }: DebatesListProps) {
  const pageSize = 20;
  const totalPages = Math.ceil(totalCount / pageSize);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return {
      full: date.toLocaleDateString('en-CA', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      }),
      short: date.toLocaleDateString('en-CA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      }),
    };
  };

  const getDayOfWeek = (dateString: string) => {
    const date = new Date(dateString);
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[date.getDay()];
  };

  if (debates.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500">No debates found matching your criteria.</p>
        <Link href="/debates" className="mt-4 inline-block text-op-blue hover:underline">
          Clear filters
        </Link>
      </div>
    );
  }

  // Group debates by month for better organization
  const groupedDebates = debates.reduce((acc, debate) => {
    const monthYear = new Date(debate.date).toLocaleDateString('en-CA', {
      year: 'numeric',
      month: 'long',
    });
    if (!acc[monthYear]) acc[monthYear] = [];
    acc[monthYear].push(debate);
    return acc;
  }, {} as Record<string, Debate[]>);

  return (
    <div>
      {/* Results count */}
      <div className="mb-4 flex justify-between items-center">
        <span className="text-sm text-gray-600">
          Showing {((currentPage - 1) * pageSize) + 1} - {Math.min(currentPage * pageSize, totalCount)} of {totalCount} debates
        </span>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-500">
            Archive spans 30+ years (1994-present)
          </span>
        </div>
      </div>

      {/* Debates List */}
      <div className="space-y-8">
        {Object.entries(groupedDebates).map(([monthYear, monthDebates]) => (
          <div key={monthYear}>
            <h2 className="text-lg font-bold text-gray-700 mb-4 sticky top-16 bg-op-gray py-2">
              {monthYear}
            </h2>
            
            <div className="space-y-4">
              {monthDebates.map((debate) => {
                const dates = formatDate(debate.date);
                
                return (
                  <Link
                    key={debate.id}
                    href={`/debates/${debate.date}/${debate.number}`}
                    className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-medium text-op-blue hover:underline">
                            {dates.full}
                          </h3>
                          <span className="text-sm bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                            Hansard #{debate.number}
                          </span>
                        </div>

                        <div className="text-sm text-gray-600 mb-3">
                          Parliament {debate.parliament}, Session {debate.session}
                        </div>

                        {/* Debate Topics/Headlines */}
                        {(debate.h1_en || debate.h2_en) && (
                          <div className="space-y-1 mb-3">
                            {debate.h1_en && (
                              <h4 className="font-medium text-gray-800">{debate.h1_en}</h4>
                            )}
                            {debate.h2_en && (
                              <p className="text-gray-600">{debate.h2_en}</p>
                            )}
                          </div>
                        )}

                        {/* Statement Count and Metadata */}
                        <div className="flex items-center gap-4 text-sm">
                          <span className="flex items-center text-gray-500">
                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                            {debate.statements_count} statements
                          </span>
                          <span className="text-gray-500">
                            {getDayOfWeek(debate.date)} sitting
                          </span>
                        </div>
                      </div>

                      {/* AI Summary Badge */}
                      <div className="flex-shrink-0 ml-4">
                        <div className="bg-blue-50 text-blue-700 px-3 py-1 rounded text-sm">
                          AI Summary Available
                        </div>
                      </div>
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-8">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            baseUrl="/debates"
            queryParams={filters}
          />
        </div>
      )}

      {/* Archive Information */}
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-medium text-gray-700 mb-2">About the Hansard Archive</h3>
        <p className="text-sm text-gray-600">
          The House of Commons Hansard is the official report of debates. Our archive includes 
          over 30 years of transcripts, with advanced search capabilities, AI-generated summaries, 
          and topic extraction. Transcripts are usually available within 24 hours of the sitting day.
        </p>
        <div className="mt-3 flex items-center gap-4 text-sm">
          <a href="https://www.ourcommons.ca/documentviewer/en/house/hansard" className="text-op-blue hover:underline">
            Official Parliament source →
          </a>
          <Link href="/api/v1/debates" className="text-op-blue hover:underline">
            API access →
          </Link>
        </div>
      </div>
    </div>
  );
}
