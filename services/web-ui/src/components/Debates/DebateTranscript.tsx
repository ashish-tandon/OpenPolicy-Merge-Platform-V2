'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Statement {
  id: number;
  time: string;
  speaker: {
    name: string;
    party: string;
    riding: string;
    mpSlug: string;
  };
  type: 'speech' | 'question' | 'answer' | 'point-of-order' | 'speaker-ruling';
  content: string;
  wordCount: number;
  language: 'en' | 'fr';
}

interface DebateTranscriptProps {
  debateId: number;
  date: string;
  debateNumber: string;
}

export default function DebateTranscript({ debateId, date, debateNumber }: DebateTranscriptProps) {
  const [statements, setStatements] = useState<Statement[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({
    speaker: '',
    type: 'all',
    search: '',
  });
  const [page, setPage] = useState(1);
  const statementsPerPage = 20;

  // In production, this would fetch actual transcript data from the API
  useEffect(() => {
    setTimeout(() => {
      setStatements([
        {
          id: 1,
          time: '10:00',
          speaker: {
            name: 'The Speaker',
            party: '',
            riding: '',
            mpSlug: 'speaker',
          },
          type: 'speaker-ruling',
          content: 'The House met at 10 a.m. Prayers.',
          wordCount: 8,
          language: 'en',
        },
        {
          id: 2,
          time: '10:02',
          speaker: {
            name: 'Justin Trudeau',
            party: 'Liberal',
            riding: 'Papineau',
            mpSlug: 'justin-trudeau',
          },
          type: 'speech',
          content: `Mr. Speaker, I rise today to address Bill C-5, which represents a critical step forward in modernizing our criminal justice system. This legislation will help ensure that our justice system treats all Canadians fairly while maintaining public safety as our top priority.

The bill proposes important reforms that have been carefully considered and developed in consultation with legal experts, community organizations, and Canadians across the country. We believe these changes will make our justice system more effective and more equitable.`,
          wordCount: 72,
          language: 'en',
        },
        {
          id: 3,
          time: '10:05',
          speaker: {
            name: 'Candice Bergen',
            party: 'Conservative',
            riding: 'Portage—Lisgar',
            mpSlug: 'candice-bergen',
          },
          type: 'question',
          content: 'Mr. Speaker, while the Prime Minister talks about fairness, Canadians are concerned about public safety. Can the Prime Minister explain how removing mandatory minimum penalties will keep our communities safe?',
          wordCount: 30,
          language: 'en',
        },
        {
          id: 4,
          time: '10:06',
          speaker: {
            name: 'Justin Trudeau',
            party: 'Liberal',
            riding: 'Papineau',
            mpSlug: 'justin-trudeau',
          },
          type: 'answer',
          content: 'Mr. Speaker, our government is committed to both public safety and justice. The evidence shows that mandatory minimums have not made our communities safer. Instead, they have led to overincarceration and prevented judges from considering individual circumstances. This bill will allow judges to impose appropriate sentences while maintaining serious consequences for serious crimes.',
          wordCount: 52,
          language: 'en',
        },
      ]);
      setLoading(false);
    }, 1000);
  }, [debateId]);

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

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'question':
        return <span className="text-blue-500">?</span>;
      case 'answer':
        return <span className="text-green-500">A</span>;
      case 'point-of-order':
        return <span className="text-yellow-500">!</span>;
      case 'speaker-ruling':
        return <span className="text-purple-500">§</span>;
      default:
        return null;
    }
  };

  const filteredStatements = statements.filter(statement => {
    if (filter.type !== 'all' && statement.type !== filter.type) return false;
    if (filter.speaker && !statement.speaker.name.toLowerCase().includes(filter.speaker.toLowerCase())) return false;
    if (filter.search && !statement.content.toLowerCase().includes(filter.search.toLowerCase())) return false;
    return true;
  });

  const paginatedStatements = filteredStatements.slice(
    (page - 1) * statementsPerPage,
    page * statementsPerPage
  );

  const totalPages = Math.ceil(filteredStatements.length / statementsPerPage);

  if (loading) {
    return (
      <div className="p-6">
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
              <div className="h-20 bg-gray-200 rounded"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Filters */}
      <div className="p-6 border-b border-gray-200 bg-gray-50">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search transcript
            </label>
            <input
              type="text"
              value={filter.search}
              onChange={(e) => setFilter({ ...filter, search: e.target.value })}
              placeholder="Search..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Filter by speaker
            </label>
            <input
              type="text"
              value={filter.speaker}
              onChange={(e) => setFilter({ ...filter, speaker: e.target.value })}
              placeholder="Speaker name..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Statement type
            </label>
            <select
              value={filter.type}
              onChange={(e) => setFilter({ ...filter, type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue text-sm"
            >
              <option value="all">All Types</option>
              <option value="speech">Speeches</option>
              <option value="question">Questions</option>
              <option value="answer">Answers</option>
              <option value="point-of-order">Points of Order</option>
              <option value="speaker-ruling">Speaker Rulings</option>
            </select>
          </div>
        </div>
      </div>

      {/* Transcript */}
      <div className="p-6">
        <div className="space-y-6">
          {paginatedStatements.map((statement) => (
            <div key={statement.id} id={`statement-${statement.id}`} className="scroll-mt-20">
              {/* Speaker Info */}
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-500">{statement.time}</span>
                  {statement.speaker.mpSlug !== 'speaker' ? (
                    <Link
                      href={`/mps/${statement.speaker.mpSlug}`}
                      className={`font-medium hover:underline ${getPartyColor(statement.speaker.party)}`}
                    >
                      {statement.speaker.name}
                    </Link>
                  ) : (
                    <span className="font-medium text-purple-600">{statement.speaker.name}</span>
                  )}
                  {statement.speaker.party && (
                    <>
                      <span className="text-gray-400">•</span>
                      <span className="text-sm text-gray-600">{statement.speaker.party}</span>
                    </>
                  )}
                  {statement.speaker.riding && (
                    <>
                      <span className="text-gray-400">•</span>
                      <span className="text-sm text-gray-600">{statement.speaker.riding}</span>
                    </>
                  )}
                  {getTypeIcon(statement.type) && (
                    <span className="text-lg">{getTypeIcon(statement.type)}</span>
                  )}
                </div>
                <div className="flex items-center gap-3 text-sm">
                  {statement.language === 'fr' && (
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">FR</span>
                  )}
                  <span className="text-gray-500">{statement.wordCount} words</span>
                  <button className="text-gray-400 hover:text-gray-600">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m9.032 4.026a9 9 0 10-15.432 0m15.432 0A9 9 0 015.284 16.974m15.432 0a9 9 0 01-7.716 4.026m-7.716-4.026A9 9 0 012.984 12" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Statement Content */}
              <div className="pl-16">
                <div className="prose max-w-none">
                  {statement.content.split('\n\n').map((paragraph, index) => (
                    <p key={index} className="mb-3 text-gray-700">
                      {paragraph}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="mt-8 flex items-center justify-center gap-2">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="text-sm text-gray-600">
              Page {page} of {totalPages}
            </span>
            <button
              onClick={() => setPage(Math.min(totalPages, page + 1))}
              disabled={page === totalPages}
              className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        )}
      </div>

      {/* Export Options */}
      <div className="p-6 border-t border-gray-200 bg-gray-50">
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-600">
            Showing {paginatedStatements.length} of {filteredStatements.length} statements
          </p>
          <div className="flex items-center gap-4">
            <button className="text-sm text-op-blue hover:underline">
              Download PDF
            </button>
            <button className="text-sm text-op-blue hover:underline">
              Export CSV
            </button>
            <a
              href={`https://www.ourcommons.ca/documentviewer/en/house/sitting-${debateNumber}/hansard`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-op-blue hover:underline"
            >
              View official source
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
