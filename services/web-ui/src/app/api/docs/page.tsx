import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'FastAPI Documentation - OpenParliament.ca',
  description: 'Interactive API documentation powered by FastAPI and Swagger UI.',
};

export default function FastAPIDocsPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-op-dark mb-4">FastAPI Interactive Documentation</h1>
          <p className="text-xl text-gray-600">
            Explore our API endpoints with interactive documentation powered by FastAPI and Swagger UI.
          </p>
          <div className="mt-4 flex flex-wrap gap-4">
            <a 
              href="/api" 
              className="inline-flex items-center px-4 py-2 border border-op-blue text-op-blue rounded-md hover:bg-op-blue hover:text-white transition-colors"
            >
              ← Back to Traditional API Docs
            </a>
            <a 
              href="http://localhost:8080/docs" 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center px-4 py-2 bg-op-blue text-white rounded-md hover:bg-op-blue-dark transition-colors"
            >
              Open in New Tab
            </a>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-gray-50 px-6 py-4 border-b">
            <h2 className="text-lg font-semibold text-gray-800">Interactive API Explorer</h2>
            <p className="text-sm text-gray-600">
              Test API endpoints directly from this interface. Click on any endpoint to expand and try it out.
            </p>
          </div>
          
          <div className="h-[800px] w-full">
            <iframe
              src="http://localhost:8080/docs"
              className="w-full h-full border-0"
              title="FastAPI Documentation"
              sandbox="allow-scripts allow-same-origin allow-forms"
            />
          </div>
        </div>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold text-op-dark mb-3">FastAPI Features</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• Automatic API documentation</li>
              <li>• Interactive request/response testing</li>
              <li>• OpenAPI 3.0 specification</li>
              <li>• Built-in validation and serialization</li>
              <li>• Real-time API testing</li>
            </ul>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold text-op-dark mb-3">API Endpoints</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• <code className="bg-gray-100 px-2 py-1 rounded">/api/v1/mps</code> - Members of Parliament</li>
              <li>• <code className="bg-gray-100 px-2 py-1 rounded">/api/v1/bills</code> - Legislation</li>
              <li>• <code className="bg-gray-100 px-2 py-1 rounded">/api/v1/debates</code> - Parliamentary debates</li>
              <li>• <code className="bg-gray-100 px-2 py-1 rounded">/api/v1/committees</code> - Committee data</li>
              <li>• <code className="bg-gray-100 px-2 py-1 rounded">/api/v1/search</code> - Full-text search</li>
            </ul>
          </div>
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Getting Started</h3>
          <p className="text-blue-800 mb-4">
            Use the interactive documentation above to explore our API endpoints. You can:
          </p>
          <ul className="text-blue-800 space-y-1 text-sm">
            <li>• Click on any endpoint to expand and see details</li>
            <li>• Try out requests with different parameters</li>
            <li>• View response schemas and examples</li>
            <li>• Copy generated code snippets</li>
            <li>• Download the OpenAPI specification</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
