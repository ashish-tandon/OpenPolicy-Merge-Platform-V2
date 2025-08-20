'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Report {
  id: number;
  title: string;
  type: 'study' | 'government-response' | 'budget' | 'annual';
  publishedDate: string;
  parliamentSession: string;
  pageCount: number;
  hasGovernmentResponse: boolean;
  responseDate?: string;
}

interface CommitteeReportsProps {
  committeeId: number;
}

export default function CommitteeReports({ committeeId }: CommitteeReportsProps) {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  // In production, this would fetch actual report data from the API
  useEffect(() => {
    setTimeout(() => {
      setReports([
        {
          id: 1,
          title: 'Report on Climate Change Impacts on Northern Communities',
          type: 'study',
          publishedDate: '2025-06-01',
          parliamentSession: '45-1',
          pageCount: 125,
          hasGovernmentResponse: true,
          responseDate: '2025-07-15',
        },
        {
          id: 2,
          title: 'Mental Health Support Framework: Recommendations for Action',
          type: 'study',
          publishedDate: '2025-05-15',
          parliamentSession: '45-1',
          pageCount: 87,
          hasGovernmentResponse: false,
        },
        {
          id: 3,
          title: 'Committee Activities and Expenditures 2024-2025',
          type: 'annual',
          publishedDate: '2025-04-01',
          parliamentSession: '45-1',
          pageCount: 42,
          hasGovernmentResponse: false,
        },
        {
          id: 4,
          title: 'Government Response to Report on Economic Recovery',
          type: 'government-response',
          publishedDate: '2025-03-20',
          parliamentSession: '45-1',
          pageCount: 28,
          hasGovernmentResponse: false,
        },
      ]);
      setLoading(false);
    }, 500);
  }, [committeeId]);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'study': return 'bg-blue-100 text-blue-800';
      case 'government-response': return 'bg-green-100 text-green-800';
      case 'budget': return 'bg-yellow-100 text-yellow-800';
      case 'annual': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredReports = filter === 'all' 
    ? reports 
    : reports.filter(r => r.type === filter);

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
      {/* Filter */}
      <div className="mb-6">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
        >
          <option value="all">All Report Types</option>
          <option value="study">Study Reports</option>
          <option value="government-response">Government Responses</option>
          <option value="annual">Annual Reports</option>
          <option value="budget">Budget Reports</option>
        </select>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        {filteredReports.map((report) => (
          <div key={report.id} className="border border-gray-200 rounded-lg p-6">
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h3 className="text-lg font-medium text-gray-900 mb-1">
                  {report.title}
                </h3>
                <div className="flex items-center gap-3 text-sm text-gray-600">
                  <span className={`px-2 py-0.5 rounded text-xs ${getTypeColor(report.type)}`}>
                    {report.type.replace('-', ' ')}
                  </span>
                  <span>
                    {new Date(report.publishedDate).toLocaleDateString('en-CA', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </span>
                  <span>{report.pageCount} pages</span>
                  <span>Session {report.parliamentSession}</span>
                </div>
              </div>
            </div>

            {/* Government Response Status */}
            {report.type === 'study' && (
              <div className="mb-3">
                {report.hasGovernmentResponse ? (
                  <div className="flex items-center text-sm text-green-700">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    Government response received on {report.responseDate && new Date(report.responseDate).toLocaleDateString('en-CA')}
                  </div>
                ) : (
                  <div className="flex items-center text-sm text-yellow-700">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Awaiting government response
                  </div>
                )}
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center gap-4">
              <a
                href={`/committees/${committeeId}/reports/${report.id}/pdf`}
                className="text-sm text-op-blue hover:underline flex items-center"
              >
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download PDF
              </a>
              <Link
                href={`/committees/${committeeId}/reports/${report.id}`}
                className="text-sm text-op-blue hover:underline"
              >
                View full report →
              </Link>
              {report.hasGovernmentResponse && (
                <Link
                  href={`/committees/${committeeId}/reports/${report.id}/response`}
                  className="text-sm text-op-blue hover:underline"
                >
                  Read government response →
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>

      {filteredReports.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No reports found matching your filter.
        </div>
      )}
    </div>
  );
}
