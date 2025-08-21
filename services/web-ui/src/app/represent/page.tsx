import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Represent - Electoral Districts & Representatives | OpenParliament.ca',
  description: 'Find elected officials and electoral districts for any Canadian address or postal code, at all levels of government.',
};

export default function RepresentPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-6xl mx-auto">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-lg p-8 mb-12">
          <h1 className="text-4xl font-bold mb-4">
            Find Your Elected Representatives
          </h1>
          <p className="text-xl mb-6">
            Discover the elected officials and electoral districts for any Canadian address or postal code, 
            at all levels of government.
          </p>
                                <div className="flex flex-wrap gap-4">
                        <Link 
                          href="/represent/demo"
                          className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
                        >
                          Try the Demo App
                        </Link>
                        <Link 
                          href="/represent/api"
                          className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
                        >
                          Use the Free API
                        </Link>
                        <Link 
                          href="/represent/data"
                          className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
                        >
                          Download the Data
                        </Link>
                        <Link 
                          href="/represent/government"
                          className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
                        >
                          For Government
                        </Link>
                      </div>
        </div>

        {/* Benefits Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          <div>
            <h2 className="text-3xl font-bold text-op-dark mb-6">
              Connect your supporters with their political representatives
            </h2>
            <p className="text-lg text-gray-700 mb-6">
              Represent matches a supporter's apos;s postal code or geocoded address to the correct elected officials. 
              It makes it easy for you to build "email your representative" advocacy campaigns. During elections, 
              we can connect your activists to political candidates.
            </p>
            <div className="bg-gray-50 p-6 rounded-lg">
              <blockquote className="italic text-gray-700">
                "I used your municipal data as part of a successful letter writing campaign from constituents 
                to their elected municipal politicians, which resulted in the passage of the most definitive 
                resolution ever opposing oil tanker traffic expansion on B.C.'s apos;s coast."
                <cite className="block mt-2 font-semibold">– Karl Hardin, Dogwood Initiative</cite>
              </blockquote>
            </div>
          </div>
          
          <div className="bg-gray-100 rounded-lg p-8 flex items-center justify-center">
            <div className="text-center">
              <svg className="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <p className="text-gray-600">Interactive Map Interface</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          <div className="bg-gray-100 rounded-lg p-8 flex items-center justify-center order-2 lg:order-1">
            <div className="text-center">
              <svg className="w-24 h-24 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p className="text-gray-600">Electoral District Information</p>
            </div>
          </div>
          
          <div className="order-1 lg:order-2">
            <h2 className="text-3xl font-bold text-op-dark mb-6">
              Provide relevant information based on your user's apos;s electoral district
            </h2>
            <p className="text-lg text-gray-700 mb-6">
              Collect a user's apos;s postal code or address, and use Represent to match it to an electoral district. 
              By identifying their riding, you can invite supporters to take local actions or show readers 
              stories from their local election race.
            </p>
            <div className="bg-gray-50 p-6 rounded-lg">
              <blockquote className="italic text-gray-700">
                "For our BC Election Guide, we used a few endpoints of the Represent API: the representative 
                lookup by riding, the BC provincial riding boundaries and their simplified geometry, and the 
                riding lookup by latitude and longitude."
                <cite className="block mt-2 font-semibold">– Phillip Smith, The Tyee</cite>
              </blockquote>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          <div>
            <h2 className="text-3xl font-bold text-op-dark mb-6">
              Map your potential voters, donors and volunteers to electoral ridings
            </h2>
            <p className="text-lg text-gray-700 mb-6">
              If your people database contains postal codes or addresses, use Represent to match people to 
              their electoral districts. By mapping people geographically, you can better target canvassing, 
              mobilize volunteers, and organize donation drives.
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-100 rounded-lg p-6 text-center">
              <svg className="w-16 h-16 mx-auto text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <p className="text-gray-600">Toronto Districts</p>
            </div>
            <div className="bg-gray-100 rounded-lg p-6 text-center">
              <svg className="w-16 h-16 mx-auto text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <p className="text-gray-600">Montreal Districts</p>
            </div>
          </div>
        </div>

        {/* Users Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-op-dark mb-8 text-center">
            Used by nonprofits and unions across Canada
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
            {[
              'David Suzuki Foundation',
              'Sierra Club Canada',
              'Council of Canadians',
              'Tides Canada',
              'Greenpeace',
              'Leadnow',
              'Environmental Defence',
              'West Coast Environmental Law',
              'CUPE',
              'United Steelworkers',
              'NUPGE',
              'PSAC'
            ].map((org, index) => (
              <div key={index} className="bg-gray-100 rounded-lg p-4 text-center">
                <div className="w-12 h-12 bg-gray-300 rounded mx-auto mb-2"></div>
                <p className="text-sm text-gray-600">{org}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <h3 className="text-2xl font-bold text-op-dark mb-4">
            Ready to get started?
          </h3>
          <p className="text-gray-600 mb-6">
            Explore electoral districts, find representatives, or integrate our API into your application.
          </p>
                                <div className="flex flex-wrap justify-center gap-4">
                        <Link 
                          href="/represent/postal-code"
                          className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                          Lookup by Postal Code
                        </Link>
                        <Link 
                          href="/represent/boundaries"
                          className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                          Browse Electoral Districts
                        </Link>
                        <Link 
                          href="/represent/representatives"
                          className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                          Find Representatives
                        </Link>
                        <Link 
                          href="/represent/government"
                          className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                          For Government
                        </Link>
                      </div>
        </div>
      </div>
    </div>
  );
}
