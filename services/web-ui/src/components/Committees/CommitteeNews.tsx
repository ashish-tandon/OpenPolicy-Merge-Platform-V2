'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface NewsItem {
  id: number;
  date: string;
  type: 'meeting' | 'report' | 'study' | 'announcement';
  title: string;
  summary: string;
  link?: string;
}

interface CommitteeNewsProps {
  committeeId: number;
}

export default function CommitteeNews({ committeeId }: CommitteeNewsProps) {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);

  // In production, this would fetch actual news data from the API
  useEffect(() => {
    setTimeout(() => {
      setNews([
        {
          id: 1,
          date: '2025-06-20',
          type: 'meeting',
          title: 'Committee to Hold Emergency Meeting on Healthcare Crisis',
          summary: 'The committee has scheduled an emergency meeting for next Tuesday to discuss the ongoing healthcare funding crisis. Ministers and provincial representatives will testify.',
        },
        {
          id: 2,
          date: '2025-06-18',
          type: 'report',
          title: 'New Report Released on Climate Change Impacts',
          summary: 'The committee has released its comprehensive report on climate change impacts on northern communities, featuring 42 recommendations for government action.',
          link: '/committees/environment/reports/climate-impacts',
        },
        {
          id: 3,
          date: '2025-06-15',
          type: 'study',
          title: 'Committee Launches Study on Mental Health Framework',
          summary: 'A new study has been launched to examine mental health support systems across Canada. The committee is now accepting witness submissions.',
        },
        {
          id: 4,
          date: '2025-06-10',
          type: 'announcement',
          title: 'New Vice-Chair Elected',
          summary: 'MP Jane Doe has been elected as the new Vice-Chair of the committee, replacing MP John Smith who stepped down last month.',
        },
      ]);
      setLoading(false);
    }, 500);
  }, [committeeId]);

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'meeting':
        return (
          <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        );
      case 'report':
        return (
          <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
      case 'study':
        return (
          <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        );
      case 'announcement':
        return (
          <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
          </svg>
        );
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="animate-pulse">
            <div className="h-24 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div>
      {/* News Feed */}
      <div className="space-y-4">
        {news.map((item) => (
          <div key={item.id} className="border-b border-gray-200 pb-4 last:border-0 last:pb-0">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 mt-1">
                {getTypeIcon(item.type)}
              </div>
              
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-1">
                  <span className="text-sm text-gray-500">
                    {new Date(item.date).toLocaleDateString('en-CA', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </span>
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                    {item.type}
                  </span>
                </div>
                
                <h3 className="font-medium text-gray-900 mb-1">
                  {item.title}
                </h3>
                
                <p className="text-sm text-gray-700 mb-2">
                  {item.summary}
                </p>
                
                {item.link && (
                  <Link
                    href={item.link}
                    className="text-sm text-op-blue hover:underline"
                  >
                    Read more →
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Subscribe Options */}
      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-medium text-blue-900 mb-2">Stay Updated</h3>
        <p className="text-sm text-blue-800 mb-3">
          Get notified about committee activities, new reports, and upcoming meetings.
        </p>
        <div className="flex items-center gap-4">
          <button className="text-sm bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Set Email Alerts
          </button>
          <a
            href={`/api/v1/committees/${committeeId}/rss`}
            className="text-sm text-blue-700 hover:underline flex items-center"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z" />
            </svg>
            RSS Feed
          </a>
        </div>
      </div>
    </div>
  );
}
