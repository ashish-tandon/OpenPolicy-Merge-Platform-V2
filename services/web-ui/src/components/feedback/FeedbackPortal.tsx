'use client';

import { useState, useEffect } from 'react';
import { 
  LightBulbIcon, 
  ChatBubbleLeftRightIcon, 
  HeartIcon, 
  ExclamationTriangleIcon,
  ArrowTopRightOnSquareIcon,
  CogIcon
} from '@heroicons/react/24/outline';

export default function FeedbackPortal() {
  const [fiderUrl, setFiderUrl] = useState('http://localhost:3000');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    // Check if Fider is accessible
    checkFiderStatus();
  }, []);

  const checkFiderStatus = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Try to fetch Fider status
      const response = await fetch(`${fiderUrl}/api/v1/health`, {
        method: 'GET',
        mode: 'no-cors', // Avoid CORS issues
      });
      
      setIsLoading(false);
    } catch (err) {
      setIsLoading(false);
      setError('Unable to connect to Fider service. Please check if the service is running.');
    }
  };

  const handleFiderUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFiderUrl(e.target.value);
  };

  const handleRefresh = () => {
    checkFiderStatus();
  };

  const openFiderInNewTab = () => {
    window.open(fiderUrl, '_blank');
  };

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center mb-4">
          <ExclamationTriangleIcon className="h-6 w-6 text-red-600 mr-2" />
          <h3 className="text-lg font-medium text-red-900">Connection Error</h3>
        </div>
        
        <p className="text-red-700 mb-4">{error}</p>
        
        <div className="space-y-4">
          <div>
            <label htmlFor="fider-url" className="block text-sm font-medium text-red-900 mb-2">
              Fider Service URL
            </label>
            <div className="flex space-x-2">
              <input
                type="url"
                id="fider-url"
                value={fiderUrl}
                onChange={handleFiderUrlChange}
                placeholder="http://localhost:3000"
                className="flex-1 px-3 py-2 border border-red-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
              />
              <button
                onClick={handleRefresh}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                Test Connection
              </button>
            </div>
          </div>
          
          <div className="text-sm text-red-600">
            <p className="font-medium">To resolve this issue:</p>
            <ol className="list-decimal list-inside mt-2 space-y-1">
              <li>Ensure Fider service is running on the specified URL</li>
              <li>Check if the port is accessible and not blocked by firewall</li>
              <li>Verify the Docker container is running: <code className="bg-red-100 px-1 rounded">docker-compose ps</code></li>
              <li>Check Fider logs: <code className="bg-red-100 px-1 rounded">docker-compose logs fider</code></li>
            </ol>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Feedback Portal Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <LightBulbIcon className="h-8 w-8 text-blue-600" />
            <h2 className="text-2xl font-bold text-gray-900">OpenPolicy Feedback Portal</h2>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-white rounded-md transition-colors"
              title="Settings"
            >
              <CogIcon className="h-5 w-5" />
            </button>
            
            <button
              onClick={openFiderInNewTab}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
            >
              <ArrowTopRightOnSquareIcon className="h-4 w-4 mr-2" />
              Open in New Tab
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <LightBulbIcon className="h-6 w-6 text-blue-600 mb-2" />
            <h3 className="font-medium text-gray-900 mb-1">Share Ideas</h3>
            <p className="text-sm text-gray-600">Submit feature requests and suggestions</p>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <HeartIcon className="h-6 w-6 text-blue-600 mb-2" />
            <h3 className="font-medium text-gray-900 mb-1">Vote & Support</h3>
            <p className="text-sm text-gray-600">Vote on existing ideas and show support</p>
          </div>
          
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <ChatBubbleLeftRightIcon className="h-6 w-6 text-blue-600 mb-2" />
            <h3 className="font-medium text-gray-900 mb-1">Track Progress</h3>
            <p className="text-sm text-gray-600">Monitor the status of your suggestions</p>
          </div>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Fider Service Configuration</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="fider-url-config" className="block text-sm font-medium text-gray-700 mb-2">
                Service URL
              </label>
              <input
                type="url"
                id="fider-url-config"
                value={fiderUrl}
                onChange={handleFiderUrlChange}
                placeholder="http://localhost:3000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
              />
            </div>
            
            <div className="flex items-end">
              <button
                onClick={handleRefresh}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                Test Connection
              </button>
            </div>
          </div>
          
          <div className="mt-3 text-sm text-gray-600">
            <p>Current Fider service URL: <code className="bg-gray-200 px-1 rounded">{fiderUrl}</code></p>
          </div>
        </div>
      )}

      {/* Fider Integration */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">Feedback Portal</h3>
            <div className="text-sm text-gray-500">
              Powered by <a href="https://getfider.com" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Fider</a>
            </div>
          </div>
        </div>
        
        {isLoading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Connecting to Fider service...</p>
          </div>
        ) : (
          <div className="h-[800px] w-full">
            <iframe
              src={fiderUrl}
              title="OpenPolicy Feedback Portal"
              width="100%"
              height="100%"
              frameBorder="0"
              allowFullScreen
              className="border-0"
              onLoad={() => setIsLoading(false)}
            />
          </div>
        )}
      </div>

      {/* Help Section */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="text-lg font-medium text-blue-900 mb-3">Need Help?</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <h4 className="font-medium mb-2">Getting Started</h4>
            <ul className="space-y-1">
              <li>• Browse existing suggestions and vote on them</li>
              <li>• Submit new feature requests or ideas</li>
              <li>• Comment on suggestions to provide context</li>
              <li>• Track the status of your submissions</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium mb-2">Service Information</h4>
            <ul className="space-y-1">
              <li>• Fider service runs on port 3000</li>
              <li>• Data is stored securely in Docker volumes</li>
              <li>• Email notifications for updates</li>
              <li>• Admin panel for moderators</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
