import { notFound } from 'next/navigation';
import Link from 'next/link';
import DebateTranscript from '@/components/Debates/DebateTranscript';
import DebateSummary from '@/components/Debates/DebateSummary';
import DebateTopics from '@/components/Debates/DebateTopics';
import DebateWordCloud from '@/components/Debates/DebateWordCloud';
import { api } from '@/lib/api';

interface DebatePageProps {
  params: Promise<{
    date: string;
    number: string;
  }>;
}

export default async function DebatePage({ params }: DebatePageProps) {
  const { date, number } = await params;
  try {
    const debate = await api.getDebate(date, number);
    
    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleDateString('en-CA', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    };

    return (
      <div className="content-container py-8">
        {/* Breadcrumb */}
        <nav className="text-sm mb-6">
          <ol className="flex items-center space-x-2">
            <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li><Link href="/debates" className="text-gray-500 hover:text-op-blue">Debates</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li className="text-gray-700">{params.date}</li>
          </ol>
        </nav>

        {/* Debate Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-op-dark mb-2">
                {formatDate(debate.date)}
              </h1>
              <div className="flex items-center gap-4 text-gray-600">
                <span>Hansard #{debate.number}</span>
                <span>•</span>
                <span>Parliament {debate.parliament}, Session {debate.session}</span>
                <span>•</span>
                <span>{debate.statements_count} statements</span>
              </div>
              
              {/* Debate Headlines */}
              {(debate.h1_en || debate.h2_en) && (
                <div className="mt-4 space-y-1">
                  {debate.h1_en && (
                    <h2 className="text-xl font-medium text-gray-800">{debate.h1_en}</h2>
                  )}
                  {debate.h2_en && (
                    <h3 className="text-lg text-gray-600">{debate.h2_en}</h3>
                  )}
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="flex flex-col gap-2">
              <a
                href={`https://www.ourcommons.ca/documentviewer/en/${debate.parliament}-${debate.session}/house/sitting-${debate.number}/hansard`}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center px-4 py-2 bg-op-blue text-white rounded hover:bg-blue-700 transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                Official Source
              </a>
              <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors">
                Download PDF
              </button>
            </div>
          </div>
        </div>

        {/* AI-Generated Summary */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">AI-Generated Summary</h2>
          <DebateSummary debateId={debate.id} />
        </div>

        {/* Topics and Word Analysis Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Extracted Topics */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Key Topics Discussed</h2>
            <DebateTopics debateId={debate.id} />
          </div>

          {/* Word Cloud */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Word Frequency Analysis</h2>
            <DebateWordCloud debateId={debate.id} />
          </div>
        </div>

        {/* Full Transcript */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold">Full Transcript</h2>
            <p className="text-sm text-gray-600 mt-1">
              Complete record of parliamentary proceedings
            </p>
          </div>
          <DebateTranscript 
            debateId={debate.id} 
            date={debate.date}
            debateNumber={debate.number}
          />
        </div>

        {/* Navigation */}
        <div className="mt-8 flex justify-between">
          <Link
            href={`/debates/${getPreviousDate(debate.date)}`}
            className="flex items-center text-op-blue hover:underline"
          >
            <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Previous Day
          </Link>
          <Link
            href={`/debates/${getNextDate(debate.date)}`}
            className="flex items-center text-op-blue hover:underline"
          >
            Next Day
            <svg className="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      </div>
    );
  } catch (_error) {
    notFound();
  }
}

// Helper functions
function getPreviousDate(date: string): string {
  const d = new Date(date);
  d.setDate(d.getDate() - 1);
  return d.toISOString().split('T')[0];
}

function getNextDate(date: string): string {
  const d = new Date(date);
  d.setDate(d.getDate() + 1);
  return d.toISOString().split('T')[0];
}
