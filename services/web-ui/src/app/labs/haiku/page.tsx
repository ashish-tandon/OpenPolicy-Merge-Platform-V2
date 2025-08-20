'use client';

import { useState } from 'react';
import Link from 'next/link';

interface Haiku {
  lines: [string, string, string];
  source: {
    speaker: string;
    date: string;
    debate: string;
    originalText: string;
  };
  syllables: [number, number, number];
}

export default function HaikuPage() {
  const [haikus, setHaikus] = useState<Haiku[]>([
    {
      lines: [
        ""rdquo;Climate change is real""rdquo;,
        ""rdquo;We must act now for our kids""rdquo;,
        ""rdquo;Time is running out""rdquo;
      ],
      source: {
        speaker: ""rdquo;Hon. Elizabeth May""rdquo;,
        date: ""rdquo;2025-06-15""rdquo;,
        debate: ""rdquo;Debate on Bill C-12""rdquo;,
        originalText: ""rdquo;Mr. Speaker, climate change is real and we must act now for our kids. Time is running out for meaningful action.""rdquo;
      },
      syllables: [5, 7, 5]
    },
    {
      lines: [
        ""rdquo;Budget deficits""rdquo;,
        ""rdquo;Growing faster than maple""rdquo;,
        ""rdquo;Trees in the springtime""rdquo;
      ],
      source: {
        speaker: ""rdquo;Pierre Poilievre""rdquo;,
        date: ""rdquo;2025-06-10""rdquo;,
        debate: ""rdquo;Budget Implementation Act""rdquo;,
        originalText: ""rdquo;The budget deficits are growing faster than maple trees in the springtime, and Canadians are paying the price.""rdquo;
      },
      syllables: [5, 7, 5]
    },
    {
      lines: [
        ""rdquo;Healthcare for all""rdquo;,
        ""rdquo;A promise we must fulfill""rdquo;,
        ""rdquo;Canadians wait""rdquo;
      ],
      source: {
        speaker: ""rdquo;Jagmeet Singh""rdquo;,
        date: ""rdquo;2025-06-08""rdquo;,
        debate: ""rdquo;Question Period""rdquo;,
        originalText: ""rdquo;Healthcare for all is a promise we must fulfill, yet Canadians wait in emergency rooms.""rdquo;
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
    <div className=""rdquo;content-container py-8""rdquo;>
      {/* Breadcrumb */}
      <nav className=""rdquo;text-sm mb-6""rdquo;>
        <ol className=""rdquo;flex items-center space-x-2""rdquo;>
          <li><Link href=""rdquo;/""rdquo; className=""rdquo;text-gray-500 hover:text-op-blue""rdquo;>Home</Link></li>
          <li><span className=""rdquo;text-gray-400""rdquo;>/</span></li>
          <li><Link href=""rdquo;/labs""rdquo; className=""rdquo;text-gray-500 hover:text-op-blue""rdquo;>Labs</Link></li>
          <li><span className=""rdquo;text-gray-400""rdquo;>/</span></li>
          <li className=""rdquo;text-gray-700""rdquo;>Parliamentary Haiku</li>
        </ol>
      </nav>

      {/* Header */}
      <div className=""rdquo;text-center mb-8""rdquo;>
        <h1 className=""rdquo;text-4xl font-bold text-op-dark mb-4""rdquo;>
          🌸 Parliamentary Haiku
        </h1>
        <p className=""rdquo;text-xl text-gray-600 max-w-2xl mx-auto""rdquo;>
          Discover the poetry hidden in parliamentary discourse. 
          These haikus are extracted from actual speeches using natural language processing.
        </p>
      </div>

      {/* Filters */}
      <div className=""rdquo;bg-white rounded-lg shadow p-6 mb-8""rdquo;>
        <div className=""rdquo;grid grid-cols-1 md:grid-cols-3 gap-4""rdquo;>
          <div>
            <label className=""rdquo;block text-sm font-medium text-gray-700 mb-1""rdquo;>
              Topic
            </label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className=""rdquo;w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue""rdquo;
            >
              {topics.map(topic => (
                <option key={topic.value} value={topic.value}>
                  {topic.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className=""rdquo;block text-sm font-medium text-gray-700 mb-1""rdquo;>
              Time Period
            </label>
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className=""rdquo;w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue""rdquo;
            >
              {periods.map(period => (
                <option key={period.value} value={period.value}>
                  {period.label}
                </option>
              ))}
            </select>
          </div>
          <div className=""rdquo;flex items-end""rdquo;>
            <button
              onClick={generateNewHaikus}
              disabled={loading}
              className=""rdquo;w-full px-4 py-2 bg-op-blue text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50""rdquo;
            >
              {loading ? 'Generating...' : 'Generate New Haikus'}
            </button>
          </div>
        </div>
      </div>

      {/* Haiku Display */}
      <div className=""rdquo;grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6""rdquo;>
        {haikus.map((haiku, index) => (
          <div key={index} className=""rdquo;bg-white rounded-lg shadow-lg overflow-hidden""rdquo;>
            <div className=""rdquo;bg-gradient-to-br from-pink-100 to-purple-100 p-8 text-center""rdquo;>
              <div className=""rdquo;space-y-2""rdquo;>
                {haiku.lines.map((line, lineIndex) => (
                  <p key={lineIndex} className=""rdquo;text-lg font-medium text-gray-800""rdquo;>
                    {line}
                  </p>
                ))}
              </div>
              <div className=""rdquo;mt-4 text-xs text-gray-500""rdquo;>
                {haiku.syllables.join('-')}
              </div>
            </div>
            
            <div className=""rdquo;p-4 bg-gray-50""rdquo;>
              <div className=""rdquo;text-sm text-gray-600 mb-3""rdquo;>
                <p className=""rdquo;font-medium text-gray-700""rdquo;>{haiku.source.speaker}</p>
                <p>{haiku.source.date} • {haiku.source.debate}</p>
              </div>
              
              <details className=""rdquo;text-xs text-gray-500""rdquo;>
                <summary className=""rdquo;cursor-pointer hover:text-gray-700""rdquo;>
                  View original text
                </summary>
                <p className=""rdquo;mt-2 italic""rdquo;>""rdquo;{haiku.source.originalText}""rdquo;</p>
              </details>
              
              <div className=""rdquo;mt-3 flex items-center gap-2""rdquo;>
                <button
                  onClick={() => shareHaiku(haiku)}
                  className=""rdquo;text-sm text-op-blue hover:underline flex items-center""rdquo;
                >
                  <svg className=""rdquo;w-4 h-4 mr-1""rdquo; fill=""rdquo;currentColor""rdquo; viewBox=""rdquo;0 0 24 24""rdquo;>
                    <path d=""rdquo;M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84""rdquo; />
                  </svg>
                  Share
                </button>
                <Link
                  href={`/debates/${haiku.source.date}`}
                  className=""rdquo;text-sm text-op-blue hover:underline""rdquo;
                >
                  View debate →
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* About Section */}
      <div className=""rdquo;mt-12 bg-gray-50 rounded-lg p-8""rdquo;>
        <h2 className=""rdquo;text-2xl font-bold text-gray-900 mb-4""rdquo;>
          How It Works
        </h2>
        <div className=""rdquo;space-y-4 text-gray-700""rdquo;>
          <p>
            Our haiku generator uses natural language processing to identify potential 
            5-7-5 syllable patterns in parliamentary speeches. The algorithm:
          </p>
          <ol className=""rdquo;list-decimal list-inside space-y-2 ml-4""rdquo;>
            <li>Analyzes transcripts for syllable patterns</li>
            <li>Identifies complete thoughts that fit the haiku structure</li>
            <li>Preserves the original speaker's words without modification</li>
            <li>Selects the most poetic and meaningful combinations</li>
          </ol>
          <p>
            While not all results are perfect haikus in the traditional sense, 
            they offer a unique perspective on parliamentary discourse and occasionally 
            reveal surprising moments of accidental poetry.
          </p>
        </div>
      </div>

      {/* CTA */}
      <div className=""rdquo;mt-8 text-center""rdquo;>
        <p className=""rdquo;text-gray-600 mb-4""rdquo;>
          Want to see haikus from a specific debate or MP?
        </p>
        <Link
          href=""rdquo;/labs/haiku/search""rdquo;
          className=""rdquo;inline-block bg-op-blue text-white px-6 py-2 rounded hover:bg-blue-700 transition-colors""rdquo;
        >
          Advanced Haiku Search
        </Link>
      </div>
    </div>
  );
}
