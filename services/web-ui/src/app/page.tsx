import Link from 'next/link';
import { api } from '@/lib/api';
import HouseStatus from '@/components/HouseStatus';
import WordCloud from '@/components/WordCloud';
import RecentBills from '@/components/RecentBills';
import RecentVotes from '@/components/RecentVotes';
import FeaturedDebate from '@/components/FeaturedDebate';

export default async function HomePage() {
  // Fetch initial data for the homepage
  const [bills, votes, debates] = await Promise.all([
    api.getBills({ page: 1, privatemember: false }).catch(() => ({ results: [] })),
    api.getBills({ page: 1 }).catch(() => ({ results: [] })), // Using bills as placeholder for votes
    api.getDebates({ page: 1 }).catch(() => ({ results: [] })),
  ]);

  return (
    <div className="content-container py-8">
      {/* House Status Banner */}
      <HouseStatus />

      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold text-op-dark mb-4">
          Your window into the House of Commons
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Track Canadian MPs, bills, debates, and committees
        </p>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Featured Content */}
        <div className="lg:col-span-2 space-y-8">
          {/* Word Cloud */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 text-op-dark">
              What MPs are talking about
            </h2>
            <p className="text-sm text-gray-600 mb-4">
              Interactive word cloud from recent debates
            </p>
            <WordCloud />
          </div>

          {/* Featured Debate */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 text-op-dark">
              Latest House Transcript
            </h2>
            <FeaturedDebate debate={debates.results?.[0]} />
          </div>

          {/* Computer-Generated Summaries Notice */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-bold text-blue-900 mb-2">
              AI-Powered Debate Analysis
            </h3>
            <p className="text-sm text-blue-800">
              Our computer-generated summaries help you quickly understand parliamentary debates. 
              While we strive for accuracy, these summaries may occasionally contain errors. 
              Always refer to the official Hansard for authoritative records.
            </p>
          </div>
        </div>

        {/* Right Column - Recent Activity */}
        <div className="space-y-8">
          {/* Recent Bills */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4 text-op-dark">
              Recently Debated Bills
            </h2>
            <RecentBills bills={bills.results || []} />
            <Link href="/bills" className="block mt-4 text-sm text-op-blue hover:underline">
              View all bills →
            </Link>
          </div>

          {/* Recent Votes */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4 text-op-dark">
              Recent Votes
            </h2>
            <RecentVotes votes={votes.results || []} />
            <Link href="/votes" className="block mt-4 text-sm text-op-blue hover:underline">
              View all votes →
            </Link>
          </div>

          {/* Quick Links */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4 text-op-dark">
              Explore Parliament
            </h2>
            <ul className="space-y-3">
              <li>
                <Link href="/mps" className="flex items-center text-op-blue hover:underline">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  Find your MP
                </Link>
              </li>
              <li>
                <Link href="/committees" className="flex items-center text-op-blue hover:underline">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  Committee Activities
                </Link>
              </li>
              <li>
                <Link href="/labs" className="flex items-center text-op-blue hover:underline">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Labs & Experiments
                </Link>
              </li>
              <li>
                <Link href="/api" className="flex items-center text-op-blue hover:underline">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                  API Documentation
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Parliamentary Schedule */}
      <div className="mt-12 bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4 text-op-dark">
          Parliamentary Calendar
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-op-blue">15</div>
            <div className="text-sm text-gray-600">Days until House returns</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-op-blue">45-1</div>
            <div className="text-sm text-gray-600">Current Session</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-op-blue">87</div>
            <div className="text-sm text-gray-600">Sitting days this year</div>
          </div>
        </div>
      </div>
    </div>
  );
}
