import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Represent API Documentation - OpenParliament.ca',
  description: 'Comprehensive API documentation for finding elected officials and electoral districts across Canada.',
};

export default function RepresentAPIPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-lg p-8 mb-12">
          <h1 className="text-4xl font-bold mb-4">Represent API Reference</h1>
          <p className="text-xl">
            Free API for finding elected officials and electoral districts across Canada
          </p>
        </div>

        {/* Basics Section */}
        <section className="mb-12">
          <div className="bg-gray-50 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Basics</h2>
            
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold mb-2">Base URL</h3>
                <code className="bg-gray-200 px-3 py-1 rounded text-sm">
                  https://represent.opennorth.ca
                </code>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold mb-2">Output Format</h3>
                <p>All endpoints output JSON</p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold mb-2">Rate Limits</h3>
                <p>Free up to 60 requests per minute (86,400 queries/day)</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-3">Endpoints</h3>
              <ul className="space-y-2 text-gray-700">
                <li>• <a href="#postal-code" className="text-blue-600 hover:underline">Postal codes</a></li>
                <li>• <a href="#boundary-sets" className="text-blue-600 hover:underline">Boundary sets</a></li>
                <li>• <a href="#boundaries" className="text-blue-600 hover:underline">Boundaries</a></li>
                <li>• <a href="#representative-sets" className="text-blue-600 hover:underline">Representative sets</a></li>
                <li>• <a href="#representatives" className="text-blue-600 hover:underline">Representatives</a></li>
                <li>• <a href="#elections" className="text-blue-600 hover:underline">Elections</a></li>
                <li>• <a href="#candidates" className="text-blue-600 hover:underline">Candidates</a></li>
              </ul>
            </div>
            
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-3">Features</h3>
              <ul className="space-y-2 text-gray-700">
                <li>• Pagination (20 per page)</li>
                <li>• Advanced filtering</li>
                <li>• Bulk downloads</li>
                <li>• JSONP support</li>
                <li>• Debug formatting</li>
                <li>• Cross-domain requests</li>
              </ul>
            </div>
          </div>
        </section>

        {/* API Endpoints */}
        <section className="space-y-12">
          {/* Postal Code Endpoint */}
          <div id="postal-code" className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Postal Codes</h2>
            <p className="text-gray-700 mb-4">
              Find representatives and boundaries by postal code.
            </p>
            
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-700">
                    <strong>Note:</strong> Using postal codes can be error-prone. For 100% accuracy, 
                    geocode addresses and use latitude/longitude coordinates.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Request</h4>
              <code className="text-sm">
                GET /postcodes/{'{postal_code}'}/
              </code>
            </div>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Response Fields</h4>
              <ul className="text-sm space-y-1">
                <li><code>boundaries_centroid</code> - Boundaries containing the postal code center</li>
                <li><code>boundaries_concordance</code> - Boundaries linked by postal code</li>
                <li><code>representatives_centroid</code> - Representatives for centroid boundaries</li>
                <li><code>representatives_concordance</code> - Representatives for concordance boundaries</li>
              </ul>
            </div>
          </div>

          {/* Boundary Sets Endpoint */}
          <div id="boundary-sets" className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Boundary Sets</h2>
            <p className="text-gray-700 mb-4">
              Get available electoral boundary sets (federal, provincial, municipal).
            </p>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Request</h4>
              <code className="text-sm">
                GET /boundary-sets/
              </code>
            </div>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Response Fields</h4>
              <ul className="text-sm space-y-1">
                <li><code>name</code> - Name of the boundary set</li>
                <li><code>domain</code> - Domain (e.g., 'ca')</li>
                <li><code>authority</code> - Authority (e.g., 'Elections Canada')</li>
                <li><code>slug</code> - URL slug for the boundary set</li>
                <li><code>last_updated</code> - Last update timestamp</li>
              </ul>
            </div>
          </div>

          {/* Boundaries Endpoint */}
          <div id="boundaries" className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Boundaries</h2>
            <p className="text-gray-700 mb-4">
              Get boundaries for a specific boundary set.
            </p>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Request</h4>
              <code className="text-sm">
                GET /boundaries/{'{boundary_set_slug}'}/
              </code>
            </div>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Query Parameters</h4>
              <ul className="text-sm space-y-1">
                <li><code>limit</code> - Number of results per page (default: 20)</li>
                <li><code>offset</code> - Number of results to skip</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Response Fields</h4>
              <ul className="text-sm space-y-1">
                <li><code>name</code> - Name of the boundary</li>
                <li><code>boundary_set_name</code> - Name of the boundary set</li>
                <li><code>external_id</code> - External identifier</li>
                <li><code>centroid_lat</code> - Centroid latitude</li>
                <li><code>centroid_lon</code> - Centroid longitude</li>
                <li><code>area</code> - Area in square kilometers</li>
              </ul>
            </div>
          </div>

          {/* Representatives Endpoint */}
          <div id="representatives" className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Representatives</h2>
            <p className="text-gray-700 mb-4">
              Get representatives for a specific representative set.
            </p>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Request</h4>
              <code className="text-sm">
                GET /representatives/{'{representative_set_slug}'}/
              </code>
            </div>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Query Parameters</h4>
              <ul className="text-sm space-y-1">
                <li><code>limit</code> - Number of results per page (default: 20)</li>
                <li><code>offset</code> - Number of results to skip</li>
                <li><code>district_name</code> - Filter by district name</li>
                <li><code>party_name</code> - Filter by party name</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 p-4 rounded mb-4">
              <h4 className="font-semibold mb-2">Response Fields</h4>
              <ul className="text-sm space-y-1">
                <li><code>name</code> - Full name of the representative</li>
                <li><code>first_name</code> - First name</li>
                <li><code>last_name</code> - Last name</li>
                <li><code>party_name</code> - Political party name</li>
                <li><code>email</code> - Email address</li>
                <li><code>photo_url</code> - Photo URL</li>
                <li><code>elected_office</code> - Elected office (e.g., 'MP', 'MLA')</li>
                <li><code>district_name</code> - District/riding name</li>
                <li><code>url</code> - Personal website URL</li>
              </ul>
            </div>
          </div>

          {/* Geocoding Endpoint */}
          <div id="geocoding" className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Geocoding</h2>
            <p className="text-gray-700 mb-4">
              Look up electoral boundaries by geographic coordinates.
            </p>
            
                            <div className="bg-gray-50 p-4 rounded mb-4">
                  <h4 className="font-semibold mb-2">Request</h4>
                  <code className="text-sm">
                    GET /boundaries/?lat={'{latitude}'}&lon={'{longitude}'}
                  </code>
                </div>
                
                <div className="bg-gray-50 p-4 rounded mb-4">
                  <h4 className="font-semibold mb-2">Query Parameters</h4>
              <ul className="text-sm space-y-1">
                <li><code>lat</code> - Latitude (required)</li>
                <li><code>lon</code> - Longitude (required)</li>
                <li><code>sets</code> - Optional boundary set to limit search</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Libraries and Tools */}
        <section className="mt-16">
          <h2 className="text-2xl font-bold text-op-dark mb-6">Libraries and Tools</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { name: 'Drupal', url: 'https://drupal.org/project/represent' },
              { name: 'WordPress', url: 'https://wordpress.org/plugins/represent-api/' },
              { name: 'Ruby', url: 'https://github.com/opennorth/govkit-ca' },
              { name: 'Python', url: 'https://github.com/ncadou/pyrepresent' },
              { name: 'Node.js', url: 'https://github.com/sprice/represent' },
              { name: 'CiviCRM', url: 'https://drupal.org/project/civinorth' }
            ].map((lib, index) => (
              <a 
                key={index}
                href={lib.url}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-md transition-all"
              >
                <h3 className="font-semibold text-blue-600 mb-2">{lib.name}</h3>
                <p className="text-sm text-gray-600">Integration library</p>
              </a>
            ))}
          </div>
        </section>

        {/* Quick Start */}
        <section className="mt-16 bg-blue-50 rounded-lg p-8">
          <h2 className="text-2xl font-bold text-op-dark mb-4">Quick Start</h2>
          <div className="space-y-4">
            <div className="bg-white p-4 rounded border">
              <h3 className="font-semibold mb-2">1. Find your MP by postal code</h3>
              <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                GET https://represent.opennorth.ca/postcodes/K1A0A6/
              </code>
            </div>
            
            <div className="bg-white p-4 rounded border">
              <h3 className="font-semibold mb-2">2. Get all federal electoral districts</h3>
              <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                GET https://represent.opennorth.ca/boundaries/federal-electoral-districts/
              </code>
            </div>
            
            <div className="bg-white p-4 rounded border">
              <h3 className="font-semibold mb-2">3. Find representatives in a district</h3>
              <code className="text-sm bg-gray-100 px-2 py-1 rounded">
                GET https://represent.opennorth.ca/representatives/house-of-commons/?district_name=Ottawa
              </code>
            </div>
          </div>
        </section>

        {/* Footer Actions */}
        <div className="mt-16 text-center">
          <h3 className="text-xl font-bold text-op-dark mb-4">Ready to integrate?</h3>
          <div className="flex flex-wrap justify-center gap-4">
            <Link 
              href="/represent/demo"
              className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Try the Demo App
            </Link>
            <Link 
              href="/represent/data"
              className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Download Data
            </Link>
            <a 
              href="mailto:represent@opennorth.ca"
              className="border border-op-blue text-op-blue px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              Contact Support
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
