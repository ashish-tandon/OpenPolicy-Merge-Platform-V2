'use client';

import { useState, useEffect } from 'react';

interface DebateSummaryProps {
  debateId: number;
}

export default function DebateSummary({ debateId }: DebateSummaryProps) {
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [accuracy, setAccuracy] = useState(85);

  // In production, this would fetch AI-generated summary from the API
  useEffect(() => {
    setTimeout(() => {
      setSummary(`
        Today's apos;s parliamentary session focused on three main areas: Bill C-5 amendments to the Criminal Code, 
        healthcare funding allocations, and climate change initiatives. 

        The debate on Bill C-5 dominated the morning session, with the government defending its approach to 
        criminal justice reform while opposition members raised concerns about public safety. Several amendments 
        were proposed, with particular focus on judicial discretion in sentencing.

        During Question Period, healthcare funding was a central topic, with opposition parties pressing the 
        government on wait times and provincial transfers. The Minister of Health announced new measures to 
        address surgical backlogs.

        The afternoon session saw extensive discussion on climate policy, including debate on carbon pricing 
        mechanisms and support for affected industries. Members from all parties contributed to discussions 
        on balancing environmental goals with economic concerns.
      `);
      setLoading(false);
    }, 1000);
  }, [debateId]);

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-4/6"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Accuracy Disclaimer */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div className="text-sm text-blue-800">
            <p className="font-medium mb-1">Computer-Generated Summary</p>
            <p>
              This summary is created using AI technology with approximately {accuracy}% accuracy. 
              While we strive for accuracy, some details may be incomplete or incorrect. 
              Always refer to the full transcript for authoritative records.
            </p>
          </div>
        </div>
      </div>

      {/* Summary Content */}
      <div className="prose max-w-none">
        {summary.split('\n\n').map((paragraph, index) => (
          <p key={index} className="mb-4 text-gray-700 leading-relaxed">
            {paragraph.trim()}
          </p>
        ))}
      </div>

      {/* Key Statistics */}
      <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-gray-700">3</div>
          <div className="text-xs text-gray-600">Main Topics</div>
        </div>
        <div className="bg-gray-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-gray-700">47</div>
          <div className="text-xs text-gray-600">Speakers</div>
        </div>
        <div className="bg-gray-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-gray-700">5.5</div>
          <div className="text-xs text-gray-600">Hours Duration</div>
        </div>
        <div className="bg-gray-50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-gray-700">12</div>
          <div className="text-xs text-gray-600">Bills Discussed</div>
        </div>
      </div>

      {/* Generation Info */}
      <div className="mt-6 text-xs text-gray-500">
        Summary generated on {new Date().toLocaleDateString('en-CA')} using natural language processing. 
        <button className="ml-2 text-op-blue hover:underline">Report an issue</button>
      </div>
    </div>
  );
}
