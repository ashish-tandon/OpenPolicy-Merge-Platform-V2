'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ChevronRightIcon, ArrowPathIcon, ShareIcon } from '@heroicons/react/24/outline';

interface Haiku {
  lines: string[];
  source: {
    speaker: string;
    date: string;
    debate: string;
    originalText: string;
  };
  syllables: number[];
}

export default function ParliamentaryHaikuPage() {
  const [haikus, setHaikus] = useState<Haiku[]>([
    {
      lines: [
        "Climate change is real",
        "We must act now for our kids",
        "Time is running out"
      ],
      source: {
        speaker: "Hon. Elizabeth May",
        date: "2025-06-15",
        debate: "Debate on Bill C-12",
        originalText: "Mr. Speaker, climate change is real and we must act now for our kids. Time is running out for meaningful action."
      },
      syllables: [5, 7, 5]
    },
    {
      lines: [
        "Budget deficits",
        "Growing faster than maple",
        "Trees in the springtime"
      ],
      source: {
        speaker: "Pierre Poilievre",
        date: "2025-06-10",
        debate: "Budget Implementation Act",
        originalText: "The budget deficits are growing faster than maple trees in the springtime, and Canadians are paying the price."
      },
      syllables: [5, 7, 5]
    },
    {
      lines: [
        "Healthcare for all",
        "A promise we must fulfill",
        "Canadians wait"
      ],
      source: {
        speaker: "Jagmeet Singh",
        date: "2025-06-08",
        debate: "Question Period",
        originalText: "Healthcare for all is a promise we must fulfill, yet Canadians wait in emergency rooms."
      },
      syllables: [5, 7, 5]
    }
  ]);

  const [loading, setLoading] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState('all');
  const [selectedPeriod, setSelectedPeriod] = useState('week');

  const topics = [
    { value: 'all', label: 'All Topics' },
    { value: 'climate', label: 'Climate & Environment' },
    { value: 'economy', label: 'Economy & Finance' },
    { value: 'healthcare', label: 'Healthcare' },
    { value: 'indigenous', label: 'Indigenous Affairs' },
    { value: 'housing', label: 'Housing' },
  ];

  const periods = [
    { value: 'today', label: 'Today' },
    { value: 'week', label: 'This Week' },
    { value: 'month', label: 'This Month' },
    { value: 'year', label: 'This Year' },
  ];

  const generateNewHaikus = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      // In production, this would fetch new haikus from the API
      setHaikus([...haikus].sort(() => Math.random() - 0.5));
      setLoading(false);
    }, 1000);
  };

  const shareHaiku = (haiku: Haiku) => {
    const text = haiku.lines.join(' / ');
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text + ' - Parliamentary Haiku via @openparlca')}`;
    window.open(url, '_blank');
  };

  return (
    <div className="content-container py-8">
      {/* Breadcrumb */}
      <nav className="text-sm mb-6">
        <ol className="flex items-center space-x-2">
          <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li><Link href="/labs" className="text-gray-500 hover:text-op-blue">Labs</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li className="text-gray-700">Parliamentary Haiku</li>
        </ol>
      </nav>

      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-op-dark mb-4">
          🌸 Parliamentary Haiku
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover the poetry hidden in parliamentary debates. Our AI extracts haikus from the passionate speeches of Canadian MPs.
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-4 justify-center mb-8">
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-1">
            Topic
          </label>
          <select
            id="topic"
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-transparent"
          >
            {topics.map((topic) => (
              <option key={topic.value} value={topic.value}>
                {topic.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="period" className="block text-sm font-medium text-gray-700 mb-1">
            Time Period
          </label>
          <select
            id="period"
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-transparent"
          >
            {periods.map((period) => (
              <option key={period.value} value={period.value}>
                {period.label}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={generateNewHaikus}
          disabled={loading}
          className="px-4 py-2 bg-op-blue text-white rounded-md hover:bg-op-blue-dark disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <ArrowPathIcon className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          {loading ? 'Generating...' : 'Generate New'}
        </button>
      </div>

      {/* Haiku Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {haikus.map((haiku, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
            {/* Haiku Lines */}
            <div className="text-center mb-4">
              {haiku.lines.map((line, lineIndex) => (
                <p key={lineIndex} className="text-lg text-gray-800 mb-2 font-serif">
                  {line}
                </p>
              ))}
              <div className="text-xs text-gray-500 mt-2">
                {haiku.syllables.join(' • ')}
              </div>
            </div>

            {/* Source Information */}
            <div className="border-t border-gray-100 pt-4 mb-4">
              <div className="text-sm text-gray-600 space-y-1">
                <p><strong>Speaker:</strong> {haiku.source.speaker}</p>
                <p><strong>Date:</strong> {haiku.source.date}</p>
                <p><strong>Context:</strong> {haiku.source.debate}</p>
              </div>
            </div>

            {/* Original Text */}
            <details className="mb-4">
              <summary className="text-sm text-op-blue cursor-pointer hover:text-op-blue-dark">
                View original text
              </summary>
              <blockquote className="mt-2 text-sm text-gray-600 italic border-l-4 border-op-blue pl-3">
                "{haiku.source.originalText}"
              </blockquote>
            </details>

            {/* Actions */}
            <div className="flex justify-between items-center">
              <button
                onClick={() => shareHaiku(haiku)}
                className="text-sm text-op-blue hover:text-op-blue-dark flex items-center gap-1"
              >
                <ShareIcon className="w-4 h-4" />
                Share
              </button>
              <Link
                href={`/debates/${haiku.source.date}/1`}
                className="text-sm text-gray-500 hover:text-op-blue flex items-center gap-1"
              >
                View debate
                <ChevronRightIcon className="w-3 h-3" />
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Footer Info */}
      <div className="text-center mt-12 text-gray-500">
        <p className="text-sm">
          Haikus are automatically generated from parliamentary debates using AI analysis.
          <br />
          Each haiku maintains the traditional 5-7-5 syllable pattern.
        </p>
      </div>
    </div>
  );
}
