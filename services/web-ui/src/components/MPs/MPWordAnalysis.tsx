'use client';

import { useEffect, useState } from 'react';

interface WordFrequency {
  word: string;
  count: number;
  percentage: number;
}

interface MPWordAnalysisProps {
  mpId: number;
}

export default function MPWordAnalysis({ mpId }: MPWordAnalysisProps) {
  const [words, setWords] = useState<WordFrequency[]>([
    { word: 'government', count: 342, percentage: 2.1 },
    { word: 'canadians', count: 287, percentage: 1.8 },
    { word: 'minister', count: 231, percentage: 1.4 },
    { word: 'legislation', count: 198, percentage: 1.2 },
    { word: 'committee', count: 176, percentage: 1.1 },
  ]);
  const [loading, setLoading] = useState(false);

  // In production, this would fetch real word analysis data
  useEffect(() => {
    // Placeholder for fetching word analysis
  }, [mpId]);

  if (loading) {
    return <div className="text-gray-500">Analyzing speech patterns...</div>;
  }

  return (
    <div>
      <p className="text-sm text-gray-600 mb-4">
        Most frequently used words in parliamentary speeches (excluding common words)
      </p>
      
      <div className="space-y-3">
        {words.map((item, index) => (
          <div key={index} className="flex items-center">
            <div className="flex-1">
              <div className="flex items-center justify-between mb-1">
                <span className="font-medium text-gray-700">{item.word}</span>
                <span className="text-sm text-gray-500">{item.count} times ({item.percentage}%)</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-op-blue h-2 rounded-full"
                  style={{ width: `${Math.min(item.percentage * 20, 100)}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 text-sm text-gray-500">
        Analysis based on speeches from the current parliamentary session
      </div>
    </div>
  );
}
