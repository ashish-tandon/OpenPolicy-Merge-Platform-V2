import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Represent Demo - Interactive Electoral Lookup | OpenParliament.ca',
  description: 'Try our interactive demo to find elected officials and electoral districts across Canada.',
};

export default function RepresentDemoPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg p-8 mb-12">
          <h1 className="text-4xl font-bold mb-4">Represent Demo App</h1>
          <p className="text-xl">
            Interactive tools to explore electoral districts and find your representatives
          </p>
        </div>

        {/* Demo Tools */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-op-dark mb-6">Interactive Tools</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-3">Postal Code Lookup</h3>
              <p className="text-gray-600 mb-4">
                Enter your postal code to find your federal, provincial, and municipal representatives.
              </p>
              <div className="flex gap-2">
                <input 
                  type="text" 
                  placeholder="e.g., K1A 0A6" 
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button className="bg-op-blue text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                  Find
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Try: K1A 0A6 (Parliament Hill), M5V 3A8 (Toronto), V6B 1A1 (Vancouver)
              </p>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-3">Map Explorer</h3>
              <p className="text-gray-600 mb-4">
                Explore electoral districts on an interactive map. Click on districts to see details.
              </p>
              <div className="bg-gray-100 rounded-lg p-4 text-center">
                <svg className="w-16 h-16 mx-auto text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m-6 3l6-3" />
                </svg>
                <p className="text-sm text-gray-600">Interactive Map Coming Soon</p>
              </div>
            </div>
          </div>
        </section>

        {/* Sample Results */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-op-dark mb-6">Sample Results</h2>
          
          {/* Postal Code Result */}
          <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">Postal Code: K1A 0A6 (Parliament Hill)</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-3">Federal Representatives</h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                      <span className="text-red-600 text-sm font-bold">L</span>
                    </div>
                    <div>
                      <p className="font-medium">Hon. Chrystia Freeland</p>
                      <p className="text-sm text-gray-600">Liberal • University—Rosedale</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-700 mb-3">Electoral Districts</h4>
                <div className="space-y-2">
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="font-medium">University—Rosedale</p>
                    <p className="text-sm text-gray-600">Federal • Ontario</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="font-medium">University—Rosedale</p>
                    <p className="text-sm text-gray-600">Provincial • Ontario</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Representative Search Result */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Representative Search: "Trudeau"</h3>
            <div className="space-y-4">
              <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                  <span className="text-red-600 text-lg font-bold">L</span>
                </div>
                <div className="flex-1">
                  <h4 className="font-medium">Rt. Hon. Justin Trudeau</h4>
                  <p className="text-sm text-gray-600">Liberal • Papineau (Quebec)</p>
                  <p className="text-sm text-gray-600">Prime Minister of Canada</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500">MP since 2008</p>
                  <p className="text-sm text-gray-500">Email: justin.trudeau@parl.gc.ca</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                  <span className="text-red-600 text-lg font-bold">L</span>
                </div>
                <div className="flex-1">
                  <h4 className="font-medium">Hon. Sophie Grégoire Trudeau</h4>
                  <p className="text-sm text-gray-600">Spouse of Prime Minister</p>
                  <p className="text-sm text-gray-600">Mental Health Advocate</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500">Public Figure</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Interactive Features */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-op-dark mb-6">Interactive Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Advanced Search</h3>
              <p className="text-gray-600 text-sm">
                Search by name, party, district, or geographic coordinates
              </p>
            </div>
            
            <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m-6 3l6-3" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Interactive Maps</h3>
              <p className="text-gray-600 text-sm">
                Visualize electoral districts and boundaries on interactive maps
              </p>
            </div>
            
            <div className="bg-white border border-gray-200 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Contact Tools</h3>
              <p className="text-gray-600 text-sm">
                Get contact information and social media links for representatives
              </p>
            </div>
          </div>
        </section>

        {/* Use Cases */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-op-dark mb-6">How People Use This</h2>
          <div className="space-y-6">
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">Voter Outreach</h3>
                  <p className="text-gray-700 mb-3">
                    Nonprofits and advocacy groups use our tools to help supporters find and contact their representatives 
                    about important issues.
                  </p>
                  <p className="text-sm text-gray-600">
                    <strong>Example:</strong> Environmental organizations helping supporters write to MPs about climate change.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m-6 3l6-3" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">Election Coverage</h3>
                  <p className="text-gray-700 mb-3">
                    News organizations and journalists use our data to provide comprehensive election coverage 
                    and help voters understand their districts.
                  </p>
                  <p className="text-sm text-gray-600">
                    <strong>Example:</strong> The Tyee used our API for their BC Election Guide.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">Campaign Management</h3>
                  <p className="text-gray-700 mb-3">
                    Political campaigns use our data to map voters, organize canvassing efforts, 
                    and target outreach to specific electoral districts.
                  </p>
                  <p className="text-sm text-gray-600">
                    <strong>Example:</strong> Campaigns mapping donors and volunteers to electoral ridings.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Get Started */}
        <section className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-op-dark mb-4">Ready to Get Started?</h2>
          <p className="text-gray-600 mb-6">
            Explore our tools, integrate our API, or download data for your own applications.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link 
              href="/represent/api"
              className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              View API Documentation
            </Link>
            <Link 
              href="/represent/data"
              className="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
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
        </section>
      </div>
    </div>
  );
}
