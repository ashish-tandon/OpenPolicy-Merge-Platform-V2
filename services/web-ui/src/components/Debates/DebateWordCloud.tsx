'use client';

import { useState, useEffect } from 'react';

interface Word {
  text: string;
  size: number;
  count: number;
}

interface DebateWordCloudProps {
  debateId: number;
}

export default function DebateWordCloud({ debateId }: DebateWordCloudProps) {
  const [words, setWords] = useState<Word[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('nouns');

  // In production, this would fetch word frequency data from the API
  useEffect(() => {
    setTimeout(() => {
      const wordData = filter === 'nouns' ? [
        { text: 'government', size: 40, count: 89 },
        { text: 'bill', size: 38, count: 76 },
        { text: 'canadians', size: 36, count: 65 },
        { text: 'minister', size: 32, count: 54 },
        { text: 'justice', size: 30, count: 48 },
        { text: 'committee', size: 28, count: 43 },
        { text: 'amendment', size: 26, count: 38 },
        { text: 'healthcare', size: 24, count: 32 },
        { text: 'climate', size: 22, count: 28 },
        { text: 'legislation', size: 20, count: 24 },
      ] : [
        { text: 'support', size: 36, count: 45 },
        { text: 'believe', size: 32, count: 38 },
        { text: 'ensure', size: 30, count: 34 },
        { text: 'protect', size: 28, count: 31 },
        { text: 'implement', size: 26, count: 27 },
        { text: 'consider', size: 24, count: 23 },
        { text: 'provide', size: 22, count: 20 },
        { text: 'address', size: 20, count: 18 },
      ];
      
      setWords(wordData);
      setLoading(false);
    }, 600);
  }, [debateId, filter]);

  const handleWordClick = (word: string) => {
    // Navigate to search with this word in the current debate
    window.location.href = `/search?q=${encodeURIComponent(word)}&type=debates`;
  };

  if (loading) {
    return (
      <div className="h-64 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-op-blue"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Filter Options */}
      <div className="mb-4 flex items-center gap-2">
        <span className="text-sm text-gray-600">Show:</span>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="text-sm px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          <option value="nouns">Nouns</option>
          <option value="verbs">Verbs</option>
          <option value="all">All Words</option>
        </select>
      </div>

      {/* Word Cloud */}
      <div className="relative h-64 bg-gray-50 rounded-lg p-4 overflow-hidden">
        <div className="flex flex-wrap gap-3 items-center justify-center h-full">
          {words.map((word, index) => (
            <button
              key={index}
              onClick={() => handleWordClick(word.text)}
              className="transition-all hover:scale-110 hover:text-op-blue cursor-pointer animate-fade-in"
              style={{ 
                fontSize: `${word.size}px`,
                animationDelay: `${index * 50}ms`
              }}
              title={`"${word.text}" mentioned ${word.count} times`}
            >
              {word.text}
            </button>
          ))}
        </div>
      </div>

      {/* Word List */}
      <div className="mt-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Top Words by Frequency</h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          {words.slice(0, 6).map((word, index) => (
            <div key={index} className="flex items-center justify-between py-1">
              <button
                onClick={() => handleWordClick(word.text)}
                className="text-gray-700 hover:text-op-blue hover:underline"
              >
                {word.text}
              </button>
              <span className="text-gray-500">{word.count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Analysis Info */}
      <div className="mt-4 text-xs text-gray-500">
        Word frequency calculated from {words.reduce((sum, w) => sum + w.count, 0).toLocaleString()} total words. 
        Common words (the, and, etc.) are excluded.
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: scale(0.8);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
}
