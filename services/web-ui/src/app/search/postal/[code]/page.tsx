import { notFound } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';

interface PostalSearchPageProps {
  params: {
    code: string;
  };
}

// Mock function - in production, this would call the Represent API or similar
async function findMPByPostalCode(postalCode: string) {
  // Normalize postal code
  const normalized = postalCode.toUpperCase().replace(/\s/g, '');
  
  // Mock data - in production, integrate with Represent API
  if (normalized.startsWith('M5')) {
    return {
      mp: {
        id: 1,
        name: 'Chrystia Freeland',
        slug: 'chrystia-freeland',
        party: { name: 'Liberal', short_name: 'Liberal', slug: 'liberal' },
        riding: { 
          name: 'University—Rosedale', 
          province: 'ON',
          slug: 'university-rosedale'
        },
        email: 'chrystia.freeland@parl.gc.ca',
        image: '/mp-placeholder.jpg',
      },
      confidence: 100,
    };
  }
  
  return null;
}

export default async function PostalSearchPage({ params }: PostalSearchPageProps) {
  const postalCode = params.code.toUpperCase();
  
  // Validate postal code format
  const postalCodeRegex = /^[A-Z]\d[A-Z]\d[A-Z]\d$/;
  if (!postalCodeRegex.test(postalCode.replace(/\s/g, ''))) {
    notFound();
  }

  const result = await findMPByPostalCode(postalCode);

  // Format postal code for display
  const formattedCode = postalCode.length === 6 
    ? `${postalCode.slice(0, 3)} ${postalCode.slice(3)}`
    : postalCode;

  return (
    <div className="content-container py-8">
      {/* Breadcrumb */}
      <nav className="text-sm mb-6">
        <ol className="flex items-center space-x-2">
          <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li><Link href="/search" className="text-gray-500 hover:text-op-blue">Search</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li className="text-gray-700">Postal Code</li>
        </ol>
      </nav>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          MP for Postal Code {formattedCode}
        </h1>

        {result ? (
          <div className="bg-white rounded-lg shadow p-8 mt-6">
            <div className="flex flex-col md:flex-row gap-8">
              {/* MP Photo */}
              <div className="flex-shrink-0">
                {result.mp.image ? (
                  <Image
                    src={result.mp.image}
                    alt={result.mp.name}
                    width={200}
                    height={250}
                    className="rounded-lg object-cover"
                  />
                ) : (
                  <div className="w-[200px] h-[250px] bg-gray-200 rounded-lg flex items-center justify-center">
                    <svg className="w-20 h-20 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                )}
              </div>

              {/* MP Info */}
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-op-dark mb-2">
                  {result.mp.name}
                </h2>
                
                {result.mp.party && (
                  <div className="flex items-center mb-3">
                    <span className={`w-4 h-4 rounded-full mr-2 ${getPartyColor(result.mp.party.slug)}`}></span>
                    <span className="text-lg">{result.mp.party.name}</span>
                  </div>
                )}

                <div className="mb-6">
                  <h3 className="text-xl text-gray-700">
                    {result.mp.riding.name}
                  </h3>
                  <p className="text-gray-600">
                    {result.mp.riding.province}
                  </p>
                </div>

                <div className="space-y-3 text-sm">
                  <div>
                    <span className="font-medium text-gray-600">Email:</span>
                    <a href={`mailto:${result.mp.email}`} className="ml-2 text-op-blue hover:underline">
                      {result.mp.email}
                    </a>
                  </div>
                  <div>
                    <span className="font-medium text-gray-600">Confidence:</span>
                    <span className="ml-2">{result.confidence}% match</span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-3 mt-6">
                  <Link
                    href={`/mps/${result.mp.slug}`}
                    className="bg-op-blue text-white px-6 py-2 rounded hover:bg-blue-700 transition-colors"
                  >
                    View Full Profile
                  </Link>
                  <Link
                    href={`/mps/${result.mp.slug}/votes`}
                    className="border border-op-blue text-op-blue px-6 py-2 rounded hover:bg-blue-50 transition-colors"
                  >
                    Voting Record
                  </Link>
                  <a
                    href={`mailto:${result.mp.email}`}
                    className="border border-gray-300 text-gray-700 px-6 py-2 rounded hover:bg-gray-50 transition-colors"
                  >
                    Contact MP
                  </a>
                </div>
              </div>
            </div>

            {/* Additional Information */}
            <div className="mt-8 pt-8 border-t border-gray-200">
              <h3 className="font-bold text-gray-700 mb-4">About Your Riding</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-600 mb-2">Quick Facts</h4>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• Population: ~110,000</li>
                    <li>• Major cities: Toronto (partial)</li>
                    <li>• Established: 2015 (redistribution)</li>
                    <li>• Previous MPs: 2</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-600 mb-2">Electoral History</h4>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• 2021: Liberal (re-elected)</li>
                    <li>• 2019: Liberal (elected)</li>
                    <li>• 2015: Liberal</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-8 mt-6">
            <div className="text-center">
              <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h2 className="text-xl font-medium text-gray-700 mb-2">
                No MP found for postal code {formattedCode}
              </h2>
              <p className="text-gray-500 mb-6">
                This postal code may not be valid or may not be in our database yet.
              </p>
              <div className="space-y-2">
                <p className="text-sm text-gray-600">You can try:</p>
                <Link href="/mps" className="block text-op-blue hover:underline">
                  Browse all MPs →
                </Link>
                <Link href="/search" className="block text-op-blue hover:underline">
                  Search by name or riding →
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Postal Code Information */}
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-medium text-blue-900 mb-2">About Postal Code Lookup</h3>
          <p className="text-sm text-blue-800">
            We use postal codes to determine your federal electoral district and identify your MP. 
            This service is powered by open data from Elections Canada and the Represent API. 
            Boundaries may change during electoral redistribution.
          </p>
        </div>
      </div>
    </div>
  );
}

function getPartyColor(slug: string) {
  switch (slug) {
    case 'liberal': return 'bg-red-600';
    case 'conservative': return 'bg-blue-600';
    case 'ndp': return 'bg-orange-600';
    case 'bloc': return 'bg-cyan-600';
    case 'green': return 'bg-green-600';
    default: return 'bg-gray-600';
  }
}
