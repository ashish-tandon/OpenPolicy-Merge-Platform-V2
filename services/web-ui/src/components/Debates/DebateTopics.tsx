'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Topic {
  id: number;
  name: string;
  category: string;
  mentions: number;
  speakers: number;
  sentiment: 'positive' | 'negative' | 'neutral' | 'mixed';
  relatedBills?: string[];
}

interface DebateTopicsProps {
  debateId: number;
}

export default function DebateTopics({ debateId }: DebateTopicsProps) {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedTopics, setExpandedTopics] = useState<Set<number>>(new Set());

  // In production, this would fetch extracted topics from the API
  useEffect(() => {
    setTimeout(() => {
      setTopics([
        {
          id: 1,
          name: 'Criminal Justice Reform',
          category: 'Justice',
          mentions: 47,
          speakers: 15,
          sentiment: 'mixed',
          relatedBills: ['C-5', 'C-3'],
        },
        {
          id: 2,
          name: 'Healthcare Funding',
          category: 'Health',
          mentions: 34,
          speakers: 12,
          sentiment: 'negative',
          relatedBills: [],
        },
        {
          id: 3,
          name: 'Climate Change Policy',
          category: 'Environment',
          mentions: 28,
          speakers: 10,
          sentiment: 'positive',
          relatedBills: ['C-12'],
        },
        {
          id: 4,
          name: 'Indigenous Affairs',
          category: 'Indigenous',
          mentions: 19,
          speakers: 7,
          sentiment: 'neutral',
          relatedBills: ['C-15'],
        },
        {
          id: 5,
          name: 'Economic Recovery',
          category: 'Economy',
          mentions: 15,
          speakers: 6,
          sentiment: 'mixed',
          relatedBills: [],
        },
      ]);
      setLoading(false);
    }, 800);
  }, [debateId]);

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      'Justice': 'bg-purple-100 text-purple-800',
      'Health': 'bg-red-100 text-red-800',
      'Environment': 'bg-green-100 text-green-800',
      'Indigenous': 'bg-orange-100 text-orange-800',
      'Economy': 'bg-blue-100 text-blue-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return <span className="text-green-600">↑</span>;
      case 'negative':
        return <span className="text-red-600">↓</span>;
      case 'mixed':
        return <span className="text-yellow-600">↕</span>;
      default:
        return <span className="text-gray-600">→</span>;
    }
  };

  const toggleExpanded = (topicId: number) => {
    const newExpanded = new Set(expandedTopics);
    if (newExpanded.has(topicId)) {
      newExpanded.delete(topicId);
    } else {
      newExpanded.add(topicId);
    }
    setExpandedTopics(newExpanded);
  };

  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map(i => (
          <div key={i} className="animate-pulse">
            <div className="h-16 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div>
      {/* Topics List */}
      <div className="space-y-3">
        {topics.map((topic) => (
          <div
            key={topic.id}
            className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
            onClick={() => toggleExpanded(topic.id)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h4 className="font-medium text-gray-900">{topic.name}</h4>
                  <span className={`text-xs px-2 py-0.5 rounded ${getCategoryColor(topic.category)}`}>
                    {topic.category}
                  </span>
                  <span className="text-lg">{getSentimentIcon(topic.sentiment)}</span>
                </div>
                
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span>{topic.mentions} mentions</span>
                  <span>•</span>
                  <span>{topic.speakers} speakers</span>
                  {topic.relatedBills && topic.relatedBills.length > 0 && (
                    <>
                      <span>•</span>
                      <span>Bills: {topic.relatedBills.join(', ')}</span>
                    </>
                  )}
                </div>

                {/* Expanded Content */}
                {expandedTopics.has(topic.id) && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-sm text-gray-700 mb-2">
                      This topic was discussed primarily during the {topic.category.toLowerCase()} portion 
                      of the debate, with contributions from members across party lines.
                    </p>
                    <div className="flex items-center gap-3 text-sm">
                      <Link
                        href={`/search?q=${encodeURIComponent(topic.name)}&type=debates`}
                        className="text-op-blue hover:underline"
                      >
                        Search related debates
                      </Link>
                      {topic.relatedBills?.map(bill => (
                        <Link
                          key={bill}
                          href={`/bills/45-1/${bill}`}
                          className="text-op-blue hover:underline"
                        >
                          View Bill {bill}
                        </Link>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              <svg
                className={`w-5 h-5 text-gray-400 transition-transform ${
                  expandedTopics.has(topic.id) ? 'rotate-90' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        ))}
      </div>

      {/* Topic Extraction Info */}
      <div className="mt-6 p-3 bg-gray-50 rounded text-xs text-gray-600">
        Topics are automatically extracted using natural language processing. 
        Sentiment analysis indicates the general tone of discussion for each topic.
      </div>
    </div>
  );
}
