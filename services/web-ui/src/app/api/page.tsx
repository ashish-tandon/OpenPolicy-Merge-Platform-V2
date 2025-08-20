import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'API Documentation - OpenParliament.ca',
  description: 'Access parliamentary data through our REST API. Comprehensive documentation and examples.',
};

export default function APIPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-op-dark mb-8">API Documentation</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-op-dark">Traditional Documentation</h2>
                <p className="text-gray-600">Comprehensive API reference and examples</p>
              </div>
            </div>
            <p className="text-gray-700 mb-6">
              Detailed documentation with code examples, response schemas, and integration guides 
              for developers building applications with parliamentary data.
            </p>
            <a 
              href="/api/docs" 
              className="inline-flex items-center px-6 py-3 bg-op-blue text-white rounded-md hover:bg-op-blue-dark transition-colors"
            >
              View Documentation
            </a>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-op-dark">Interactive FastAPI Docs</h2>
                <p className="text-gray-600">Test endpoints directly in your browser</p>
              </div>
            </div>
            <p className="text-gray-700 mb-6">
              Interactive API documentation powered by FastAPI and Swagger UI. Test endpoints, 
              view schemas, and try requests with real-time validation.
            </p>
            <a 
              href="/api/docs" 
              className="inline-flex items-center px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
            >
              Try Interactive Docs
            </a>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-op-dark mb-6">API Overview</h2>
          <p className="text-gray-700 mb-6">
            The OpenParliament.ca API provides programmatic access to Canadian parliamentary data, 
            including Members of Parliament, bills, debates, committees, and voting records.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="text-lg font-semibold text-op-dark mb-3">Base URL</h3>
              <code className="bg-gray-100 px-3 py-2 rounded text-sm font-mono">
                http://localhost:8080/api/v1
              </code>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-op-dark mb-3">Authentication</h3>
              <p className="text-gray-600">Currently no authentication required for public endpoints</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full border border-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 border-b">Endpoint</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 border-b">Description</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 border-b">Method</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="px-4 py-3 text-sm font-mono text-blue-600">/mps</td>
                  <td className="px-4 py-3 text-sm text-gray-700">Members of Parliament</td>
                  <td className="px-4 py-3 text-sm text-gray-700">GET</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm font-mono text-blue-600">/bills</td>
                  <td className="px-4 py-3 text-sm text-gray-700">Legislation and bills</td>
                  <td className="px-4 py-3 text-sm text-gray-700">GET</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm font-mono text-blue-600">/debates</td>
                  <td className="px-4 py-3 text-sm text-gray-700">Parliamentary debates</td>
                  <td className="px-4 py-3 text-sm text-gray-700">GET</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm font-mono text-blue-600">/committees</td>
                  <td className="px-4 py-3 text-sm text-gray-700">Committee information</td>
                  <td className="px-4 py-3 text-sm text-gray-700">GET</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm font-mono text-blue-600">/search</td>
                  <td className="px-4 py-3 text-sm text-gray-700">Full-text search</td>
                  <td className="px-4 py-3 text-sm text-gray-700">GET</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-op-dark mb-6">Quick Start</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-op-dark mb-2">1. Get All MPs</h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto">
                <pre className="text-sm">
{`curl "http://localhost:8080/api/v1/mps/" \\
  -H "Accept: application/json"`}
                </pre>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-op-dark mb-2">2. Search for Bills</h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto">
                <pre className="text-sm">
{`curl "http://localhost:8080/api/v1/bills/?q=climate" \\
  -H "Accept: application/json"`}
                </pre>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-op-dark mb-2">3. Get Recent Debates</h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto">
                <pre className="text-sm">
{`curl "http://localhost:8080/api/v1/debates/?page=1&page_size=10" \\
  -H "Accept: application/json"`}
                </pre>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Need Help?</h3>
          <p className="text-blue-800 mb-4">
            For questions about the API, examples, or integration help:
          </p>
          <ul className="text-blue-800 space-y-1 text-sm">
            <li>• Check our <a href="/api/docs" className="underline font-medium">interactive documentation</a></li>
            <li>• Review the <a href="https://github.com/openparlca" className="underline font-medium">GitHub repository</a></li>
            <li>• Contact us at <a href="mailto:info@openparliament.ca" className="underline font-medium">info@openparliament.ca</a></li>
          </ul>
        </div>
      </div>
    </div>
  );
}
