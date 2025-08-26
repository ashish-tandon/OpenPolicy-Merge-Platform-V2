import { Suspense } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import DebatesList from '@/components/Debates/DebatesList';
import LoadingSpinner from '@/components/LoadingSpinner';

interface DebatesYearPageProps {
  params: Promise<{
    year: string;
  }>;
  searchParams: Promise<{
    page?: string;
  }>;
}

export default async function DebatesYearPage({ params, searchParams }: DebatesYearPageProps) {
  const { year } = await params;
  const { page = '1' } = await searchParams;

  const yearNum = parseInt(year);
  const currentPage = parseInt(page);

  // Validate year
  if (isNaN(yearNum) || yearNum < 1994 || yearNum > new Date().getFullYear()) {
    return (
      <div className="content-container py-8">
        <h1 className="text-3xl font-bold text-op-dark mb-4">Invalid Year</h1>
        <p className="text-gray-600">
          Please select a year between 1994 and {new Date().getFullYear()}.
        </p>
        <Link href="/debates" className="text-op-blue hover:underline">
          Back to debates
        </Link>
      </div>
    );
  }

  // Fetch debates for the specific year
  const debatesData = await api.getDebates({
    page: currentPage.toString(),
    page_size: '50', // Show more per page for year view
    date_gte: `${year}-01-01`,
    date_lte: `${year}-12-31`,
  });

  // Generate list of months with debates
  const monthsWithDebates = new Set<number>();
  if (debatesData.debates) {
    debatesData.debates.forEach((debate: any) => {
      const month = new Date(debate.date).getMonth();
      monthsWithDebates.add(month);
    });
  }

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  return (
    <div className="content-container py-8">
      {/* Breadcrumb Navigation */}
      <nav className="mb-6">
        <ol className="flex items-center space-x-2 text-sm text-gray-600">
          <li>
            <Link href="/debates" className="hover:text-op-blue transition-colors">
              Debates
            </Link>
          </li>
          <li className="text-gray-400">/</li>
          <li className="text-gray-900 font-medium">{year}</li>
        </ol>
      </nav>

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          Debates from {year}
        </h1>
        <p className="text-gray-600">
          Parliamentary debates and proceedings from {year}
        </p>
      </div>

      {/* Month Navigation */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-lg font-bold text-op-dark mb-4">Jump to Month</h2>
        <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
          {monthNames.map((month, index) => (
            <button
              key={month}
              onClick={() => {
                const element = document.getElementById(`month-${index}`);
                if (element) element.scrollIntoView({ behavior: 'smooth' });
              }}
              className={`text-sm py-2 px-3 rounded ${
                monthsWithDebates.has(index)
                  ? 'bg-op-blue text-white hover:bg-blue-700'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              }`}
              disabled={!monthsWithDebates.has(index)}
            >
              {month}
            </button>
          ))}
        </div>
      </div>

      {/* Debates List */}
      <Suspense fallback={<LoadingSpinner />}>
        {debatesData.debates && debatesData.debates.length > 0 ? (
          <div className="space-y-8">
            {/* Group debates by month */}
            {monthNames.map((month, monthIndex) => {
              const monthDebates = debatesData.debates.filter((debate: any) => 
                new Date(debate.date).getMonth() === monthIndex
              );

              if (monthDebates.length === 0) return null;

              return (
                <div key={month} id={`month-${monthIndex}`} className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-bold text-op-dark mb-4">{month}</h2>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                    {monthDebates.map((debate: any) => (
                      <div key={debate.id} className="text-sm">
                        <Link 
                          href={`/debates/${debate.date}`}
                          className="text-op-blue hover:underline"
                        >
                          {new Date(debate.date).toLocaleDateString('en-CA', { 
                            month: 'short', 
                            day: 'numeric' 
                          })}
                        </Link>
                        {debate.most_frequent_word && (
                          <div className="mt-1">
                            <span 
                              className="text-xs text-gray-600 italic"
                              title="This is the word that came up the most, compared to other similar debates"
                            >
                              {debate.most_frequent_word}
                            </span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-500">No debates found for {year}.</p>
            <Link href="/debates" className="mt-4 inline-block text-op-blue hover:underline">
              Back to all debates
            </Link>
          </div>
        )}
      </Suspense>

      {/* Year Navigation */}
      <div className="mt-8 flex justify-between items-center">
        {yearNum > 1994 && (
          <Link 
            href={`/debates/year/${yearNum - 1}`}
            className="text-op-blue hover:underline flex items-center"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            {yearNum - 1}
          </Link>
        )}
        {yearNum < new Date().getFullYear() && (
          <Link 
            href={`/debates/year/${yearNum + 1}`}
            className="text-op-blue hover:underline flex items-center ml-auto"
          >
            {yearNum + 1}
            <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        )}
      </div>
    </div>
  );
}