import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';

interface DebatePageProps {
  params: Promise<{
    date: string;
    number: string;
  }>;
}

export default async function DebatePage({ params }: DebatePageProps) {
  const { date, number } = await params;
  try {
    const debate = await api.getDebate(date, number);
    
    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleDateString('en-CA', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    };

    return (
      <div className="content-container py-8">
        {/* Breadcrumb Navigation */}
        <nav className="mb-6">
          <ol className="flex items-center space-x-2 text-sm">
            <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li><Link href="/debates" className="text-gray-500 hover:text-op-blue">Debates</Link></li>
            <li><span className="text-gray-400">/</span></li>
            <li className="text-gray-700">{date}</li>
          </ol>
        </nav>

        {/* Debate Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          {debate ? (
            <div>
              <h1 className="text-3xl font-bold text-op-dark mb-2">
                {formatDate(debate.date)}
              </h1>
              <div className="flex items-center gap-4 text-gray-600">
                <span>Hansard #{debate.number}</span>
                <span>•</span>
                <span>{debate.statements_count} statements</span>
              </div>
            </div>
          ) : (
            <div>
              <h1 className="text-3xl font-bold text-op-dark mb-2">
                Debate Not Found
              </h1>
              <p className="text-gray-600">
                The requested debate for {formatDate(date)} could not be found. 
                The API method for fetching debate details has not been implemented yet.
              </p>
              <div className="mt-4">
                <Link 
                  href="/debates" 
                  className="text-op-blue hover:underline"
                >
                  ← Back to Debates
                </Link>
              </div>
            </div>
          )}
        </div>

        {/* Placeholder for future debate content */}
        {debate && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Debate Content</h2>
            <p className="text-gray-600">
              Full debate content will be displayed here once the API is implemented.
            </p>
          </div>
        )}
      </div>
    );
  } catch (_error) {
    notFound();
  }
}
