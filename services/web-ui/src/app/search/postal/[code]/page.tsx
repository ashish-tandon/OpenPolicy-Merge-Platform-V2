'use client';

import { useEffect, useState } from 'react';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { PostalCodeService } from '@/services/postalCodeService';
import { PartyColorService } from '@/services/partyColorService';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { ErrorMessage } from '@/components/ErrorMessage';

interface PostalSearchPageProps {
  params: Promise<{
    code: string;
  }>;
}

interface MPResult {
  mp: {
    id: number;
    name: string;
    slug: string;
    party: { 
      name: string; 
      short_name: string; 
      slug: string;
    };
    riding: { 
      name: string; 
      province: string;
      slug: string;
    };
    email: string;
    phone?: string;
    image?: string;
    photo_url?: string;
  };
  confidence: number;
}

export default function PostalSearchPage({ params }: PostalSearchPageProps) {
  const [code, setCode] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<MPResult | null>(null);

  useEffect(() => {
    async function loadParams() {
      const resolvedParams = await params;
      setCode(resolvedParams.code);
    }
    loadParams();
  }, [params]);

  useEffect(() => {
    if (!code) return;

    async function fetchMP() {
      try {
        setLoading(true);
        setError(null);

        // Validate postal code format
        const normalizedCode = code.toUpperCase().replace(/\s/g, '');
        const postalCodeRegex = /^[A-Z]\d[A-Z]\d[A-Z]\d$/;
        
        if (!postalCodeRegex.test(normalizedCode)) {
          notFound();
        }

        // Call the new RESTful API endpoint
        const response = await PostalCodeService.findMPByPostalCode(normalizedCode);
        
        if (response && response.representatives.length > 0) {
          // Transform API response to component format
          const mp = response.representatives[0];
          setResult({
            mp: {
              id: Date.now(), // Temporary ID
              name: mp.name,
              slug: mp.name.toLowerCase().replace(/\s+/g, '-'),
              party: {
                name: mp.party,
                short_name: mp.party,
                slug: mp.party.toLowerCase().replace(/\s+/g, '-')
              },
              riding: {
                name: mp.riding,
                province: extractProvince(mp.riding),
                slug: mp.riding.toLowerCase().replace(/\s+/g, '-')
              },
              email: mp.email || `${mp.name.toLowerCase().replace(/\s+/g, '.')}@parl.gc.ca`,
              phone: mp.phone,
              photo_url: mp.photo_url,
              image: mp.photo_url
            },
            confidence: 100
          });
        } else {
          setResult(null);
        }
      } catch (err) {
        console.error('Error fetching MP:', err);
        setError('Failed to load MP information. Please try again later.');
      } finally {
        setLoading(false);
      }
    }

    fetchMP();
  }, [code]);

  // Format postal code for display
  const formattedCode = code.length === 6 
    ? `${code.slice(0, 3)} ${code.slice(3)}`
    : code;

  if (loading) {
    return (
      <div className="content-container py-8">
        <div className="max-w-4xl mx-auto">
          <LoadingSpinner message="Looking up your MP..." />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="content-container py-8">
        <div className="max-w-4xl mx-auto">
          <ErrorMessage message={error} />
        </div>
      </div>
    );
  }

  return (
    <div className="content-container py-8">
      {/* Breadcrumb */}
      <nav className="text-sm mb-6" aria-label="Breadcrumb">
        <ol className="flex items-center space-x-2">
          <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
          <li><span className="text-gray-400" aria-hidden="true">/</span></li>
          <li><Link href="/search" className="text-gray-500 hover:text-op-blue">Search</Link></li>
          <li><span className="text-gray-400" aria-hidden="true">/</span></li>
          <li className="text-gray-700" aria-current="page">Postal Code</li>
        </ol>
      </nav>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-op-dark mb-2">
          MP for Postal Code {formattedCode}
        </h1>

        {result ? (
          <MPCard result={result} />
        ) : (
          <NoResultsCard formattedCode={formattedCode} />
        )}

        {/* Postal Code Information */}
        <PostalCodeInfo />
      </div>
    </div>
  );
}

// Extracted components for better organization
function MPCard({ result }: { result: MPResult }) {
  const partyColor = PartyColorService.getPartyColor(result.mp.party.slug);

  return (
    <div className="bg-white rounded-lg shadow p-8 mt-6">
      <div className="flex flex-col md:flex-row gap-8">
        {/* MP Photo */}
        <div className="flex-shrink-0">
          {result.mp.image || result.mp.photo_url ? (
            <Image
              src={result.mp.image || result.mp.photo_url || '/mp-placeholder.jpg'}
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
              <span className={`w-4 h-4 rounded-full mr-2 ${partyColor}`}></span>
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

          <ContactInfo mp={result.mp} confidence={result.confidence} />

          <ActionButtons mp={result.mp} />
        </div>
      </div>

      <RidingInfo />
    </div>
  );
}

function ContactInfo({ mp, confidence }: { mp: MPResult['mp'], confidence: number }) {
  return (
    <div className="space-y-3 text-sm">
      <div>
        <span className="font-medium text-gray-600">Email:</span>
        <a href={`mailto:${mp.email}`} className="ml-2 text-op-blue hover:underline">
          {mp.email}
        </a>
      </div>
      {mp.phone && (
        <div>
          <span className="font-medium text-gray-600">Phone:</span>
          <a href={`tel:${mp.phone}`} className="ml-2 text-op-blue hover:underline">
            {mp.phone}
          </a>
        </div>
      )}
      <div>
        <span className="font-medium text-gray-600">Confidence:</span>
        <span className="ml-2">{confidence}% match</span>
      </div>
    </div>
  );
}

function ActionButtons({ mp }: { mp: MPResult['mp'] }) {
  return (
    <div className="flex flex-wrap gap-3 mt-6">
      <Link
        href={`/mps/${mp.slug}`}
        className="bg-op-blue text-white px-6 py-2 rounded hover:bg-blue-700 transition-colors"
      >
        View Full Profile
      </Link>
      <Link
        href={`/mps/${mp.slug}/votes`}
        className="border border-op-blue text-op-blue px-6 py-2 rounded hover:bg-blue-50 transition-colors"
      >
        Voting Record
      </Link>
      <a
        href={`mailto:${mp.email}`}
        className="border border-gray-300 text-gray-700 px-6 py-2 rounded hover:bg-gray-50 transition-colors"
      >
        Contact MP
      </a>
    </div>
  );
}

function RidingInfo() {
  return (
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
  );
}

function NoResultsCard({ formattedCode }: { formattedCode: string }) {
  return (
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
  );
}

function PostalCodeInfo() {
  return (
    <div className="mt-8 p-4 bg-blue-50 rounded-lg">
      <h3 className="font-medium text-blue-900 mb-2">About Postal Code Lookup</h3>
      <p className="text-sm text-blue-800">
        We use postal codes to determine your federal electoral district and identify your MP. 
        This service is powered by open data from Elections Canada and the Represent API. 
        Boundaries may change during electoral redistribution.
      </p>
    </div>
  );
}

// Utility function
function extractProvince(riding: string): string {
  // Simple extraction - in production this would be more sophisticated
  const provinces = ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'NT', 'YT', 'NU'];
  for (const prov of provinces) {
    if (riding.includes(prov)) return prov;
  }
  return 'Canada';
}
