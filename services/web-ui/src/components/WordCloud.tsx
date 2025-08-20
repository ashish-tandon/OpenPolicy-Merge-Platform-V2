'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

interface Word {
  text: string;
  size: number;
  count: number;
}

export default function WordCloud() {
  const [words, setWords] = useState<Word[]>([
    { text: 'c-5', size: 48, count: 127 },
    { text: 'bill', size: 40, count: 89 },
    { text: 'government', size: 36, count: 76 },
    { text: 'canadians', size: 32, count: 65 },
    { text: 'committee', size: 28, count: 54 },
    { text: 'minister', size: 26, count: 48 },
    { text: 'legislation', size: 24, count: 43 },
    { text: 'support', size: 22, count: 38 },
    { text: 'amendments', size: 20, count: 32 },
    { text: 'debate', size: 18, count: 28 },
  ]);

  // In production, this would fetch real data from the API
  useEffect(() => {
    // Placeholder for fetching word cloud data
  }, []);

  const handleWordClick = (word: string) => {
    window.location.href = `/search?q=${encodeURIComponent(word)}`;
  };

  return (
    <div className="relative h-64 flex items-center justify-center">
      <div className="flex flex-wrap gap-4 items-center justify-center p-4">
        {words.map((word, index) => (
          <button
            key={index}
            onClick={() => handleWordClick(word.text)}
            className="transition-all hover:scale-110 hover:text-op-blue cursor-pointer"
            style={{ fontSize: `${word.size}px` }}
            title={`"${word.text}" mentioned ${word.count} times`}
          >
            {word.text}
          </button>
        ))}
      </div>
      <div className="absolute bottom-0 left-0 text-xs text-gray-500">
        Word size indicates frequency in recent debates
      </div>
    </div>
  );
}
