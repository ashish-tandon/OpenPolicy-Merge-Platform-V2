import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About - OpenParliament.ca',
  description: 'Learn about OpenParliament.ca, our mission, and how we make Canadian parliamentary data accessible.',
};

export default function AboutPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-op-dark mb-8">About OpenParliament.ca</h1>
        
        <div className="prose prose-lg max-w-none">
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Our Mission</h2>
            <p className="text-gray-700 mb-4">
              OpenParliament.ca is dedicated to making Canadian parliamentary democracy more accessible, 
              transparent, and engaging for all citizens. We believe that an informed citizenry is essential 
              to a healthy democracy.
            </p>
            <p className="text-gray-700">
              Our platform provides easy access to parliamentary proceedings, allowing Canadians to track 
              their representatives, understand legislation, and stay informed about the issues that matter most.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold text-op-dark mb-4">What We Do</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-xl font-semibold text-op-blue mb-3">Track MPs</h3>
                <p className="text-gray-600">
                  Follow your Member of Parliament&apos;s voting record, speeches, and committee work.
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-xl font-semibold text-op-blue mb-3">Monitor Legislation</h3>
                <p className="text-gray-600">
                  Stay updated on bills, their progress through Parliament, and voting results.
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-xl font-semibold text-op-blue mb-3">Follow Debates</h3>
                <p className="text-gray-600">
                  Read parliamentary debates and understand the issues being discussed.
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-xl font-semibold text-op-blue mb-3">Committee Insights</h3>
                <p className="text-gray-600">
                  Explore committee activities, reports, and recommendations.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Our Data</h2>
            <p className="text-gray-700 mb-4">
              We source our data from official parliamentary records, including:
            </p>
            <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
              <li>House of Commons Hansard (debate transcripts)</li>
              <li>Voting records and results</li>
              <li>Bill information and status</li>
              <li>Committee reports and activities</li>
              <li>MP profiles and contact information</li>
            </ul>
            <p className="text-gray-700">
              All data is publicly available under the Open Government Licence - Canada.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Technology</h2>
            <p className="text-gray-700 mb-4">
              OpenParliament.ca V2 is built with modern, open-source technologies:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded">
                <h4 className="font-semibold text-op-blue">Frontend</h4>
                <p className="text-sm text-gray-600">Next.js, React, TypeScript</p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <h4 className="font-semibold text-op-blue">Backend</h4>
                <p className="text-sm text-gray-600">FastAPI, Python, PostgreSQL</p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded">
                <h4 className="font-semibold text-op-blue">Infrastructure</h4>
                <p className="text-sm text-gray-600">Docker, Redis, Cloud Native</p>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Get Involved</h2>
            <p className="text-gray-700 mb-4">
              OpenParliament.ca is an open-source project. We welcome contributions from developers, 
              designers, researchers, and anyone interested in improving democratic transparency.
            </p>
            <div className="flex flex-wrap gap-4">
              <a 
                href="https://github.com/openparlca" 
                className="inline-flex items-center px-6 py-3 bg-op-blue text-white rounded-md hover:bg-op-blue-dark transition-colors"
              >
                View on GitHub
              </a>
              <a 
                href="/api" 
                className="inline-flex items-center px-6 py-3 border border-op-blue text-op-blue rounded-md hover:bg-op-blue hover:text-white transition-colors"
              >
                API Documentation
              </a>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold text-op-dark mb-4">Contact</h2>
            <p className="text-gray-700 mb-4">
              Have questions, suggestions, or want to get involved? We&apos;d love to hear from you.
            </p>
            <div className="bg-gray-50 p-6 rounded-lg">
              <p className="text-gray-700">
                <strong>Email:</strong> info@openparliament.ca<br/>
                <strong>Twitter:</strong> <a href="https://twitter.com/openparlca" className="text-op-blue hover:underline">@openparlca</a><br/>
                <strong>GitHub:</strong> <a href="https://github.com/openparlca" className="text-op-blue hover:underline">github.com/openparlca</a>
              </p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
