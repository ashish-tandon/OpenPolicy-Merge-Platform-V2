'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Speech {
  id: number;
  date: string;
  debateNumber: string;
  topic: string;
  excerpt: string;
  wordCount: number;
}

interface MPSpeechesProps {
  mpId: number;
}

export default function MPSpeeches({ mpId }: MPSpeechesProps) {
  const [speeches, setSpeeches] = useState<Speech[]>([
    {
      id: 1,
      date: '2025-06-20',
      debateNumber: '147',
      topic: 'Bill C-5 - Criminal Code Amendment',
      excerpt: 'Mr. Speaker, I rise today to speak in support of Bill C-5. This legislation represents an important step forward in modernizing our criminal justice system...',
      wordCount: 1243,
    },
    {
      id: 2,
      date: '2025-06-19',
      debateNumber: '146',
      topic: 'Question Period',
      excerpt: 'Mr. Speaker, my question is for the Minister of Finance. Canadian families are struggling with the rising cost of living. What specific measures is the government taking...',
      wordCount: 156,
    },
    {
      id: 3,
      date: '2025-06-18',
      debateNumber: '145',
      topic: 'Private Members Business - M-42',
      excerpt: 'Mr. Speaker, I am pleased to rise today to speak to Motion M-42, which calls for the establishment of a national framework for mental health support...',
      wordCount: 2341,
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // In production, this would fetch real speech data
  useEffect(() => {
    // Placeholder for fetching speeches
  }, [mpId]);

  const filteredSpeeches = speeches.filter(speech =>
    speech.topic.toLowerCase().includes(searchTerm.toLowerCase()) ||
    speech.excerpt.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      {/* Search */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Search speeches..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        />
      </div>

      {/* Speech Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-op-blue">142</div>
          <div className="text-sm text-gray-600">Total Speeches</div>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-purple-600">23,456</div>
          <div className="text-sm text-gray-600">Total Words Spoken</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-green-600">165</div>
          <div className="text-sm text-gray-600">Average Words per Speech</div>
        </div>
      </div>

      {/* Speeches List */}
      {loading ? (
        <div className="text-gray-500">Loading speeches...</div>
      ) : (
        <div className="space-y-6">
          {filteredSpeeches.map((speech) => (
            <div key={speech.id} className="border-b border-gray-200 pb-6">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <Link
                    href={`/debates/${speech.date}/${speech.debateNumber}`}
                    className="text-lg font-medium text-op-blue hover:underline"
                  >
                    {speech.topic}
                  </Link>
                  <div className="text-sm text-gray-500 mt-1">
                    {new Date(speech.date).toLocaleDateString('en-CA', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })} • Debate #{speech.debateNumber}
                  </div>
                </div>
                <span className="text-sm text-gray-500">{speech.wordCount} words</span>
              </div>
              
              <p className="text-gray-700 line-clamp-3">{speech.excerpt}</p>
              
              <Link
                href={`/debates/${speech.date}/${speech.debateNumber}#speech-${speech.id}`}
                className="inline-flex items-center mt-2 text-sm text-op-blue hover:underline"
              >
                Read full speech
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          ))}
        </div>
      )}

      {filteredSpeeches.length === 0 && !loading && (
        <div className="text-center py-8 text-gray-500">
          No speeches found matching your search.
        </div>
      )}
    </div>
  );
}
