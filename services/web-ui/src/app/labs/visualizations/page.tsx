'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function VisualizationsPage() {
  const [selectedVisualization, setSelectedVisualization] = useState('voting-patterns');
  
  const visualizations = [
    {
      id: 'voting-patterns',
      title: 'Party Voting Patterns',
      description: 'Visualize how parties vote together or diverge on key issues',
      type: 'heatmap',
    },
    {
      id: 'speech-frequency',
      title: 'MP Speech Frequency',
      description: 'Who speaks the most in Parliament? Interactive timeline',
      type: 'timeline',
    },
    {
      id: 'word-trends',
      title: 'Word Usage Trends',
      description: 'Track how political language evolves over time',
      type: 'line-chart',
    },
    {
      id: 'committee-network',
      title: 'Committee Networks',
      description: 'Explore connections between MPs through committee membership',
      type: 'network',
    },
    {
      id: 'bill-journey',
      title: 'Bill Journey Map',
      description: 'Follow the path of legislation through Parliament',
      type: 'sankey',
    },
  ];

  const currentViz = visualizations.find(v => v.id === selectedVisualization);

  return (
    <div className="content-container py-8">
      {/* Breadcrumb */}
      <nav className="text-sm mb-6">
        <ol className="flex items-center space-x-2">
          <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li><Link href="/labs" className="text-gray-500 hover:text-op-blue">Labs</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li className="text-gray-700">Data Visualizations</li>
        </ol>
      </nav>

      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-op-dark mb-4">
          📊 Parliamentary Data Visualizations
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Interactive visualizations that reveal patterns and insights in parliamentary data
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Visualization Menu */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="font-bold text-gray-700 mb-4">Choose Visualization</h2>
            <div className="space-y-2">
              {visualizations.map((viz) => (
                <button
                  key={viz.id}
                  onClick={() => setSelectedVisualization(viz.id)}
                  className={`w-full text-left px-4 py-3 rounded-md transition-colors ${
                    selectedVisualization === viz.id
                      ? 'bg-op-blue text-white'
                      : 'hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <div className="font-medium">{viz.title}</div>
                  <div className={`text-xs mt-1 ${
                    selectedVisualization === viz.id ? 'text-blue-100' : 'text-gray-500'
                  }`}>
                    {viz.type}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Visualization Display */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">{currentViz?.title}</h2>
              <p className="text-gray-600 mt-1">{currentViz?.description}</p>
            </div>
            
            <div className="p-8">
              {/* Placeholder for actual visualizations */}
              {selectedVisualization === 'voting-patterns' && (
                <div className="space-y-6">
                  <div className="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
                    <div className="text-center">
                      <div className="mb-4">
                        <svg className="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                      </div>
                      <p className="text-gray-500 mb-2">Party Voting Heatmap</p>
                      <p className="text-sm text-gray-400">
                        Shows correlation between party voting patterns
                      </p>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="bg-red-50 rounded p-3">
                      <div className="flex items-center justify-between">
                        <span className="text-red-700">Liberal-NDP</span>
                        <span className="font-bold text-red-800">78%</span>
                      </div>
                      <div className="text-xs text-red-600 mt-1">Vote together</div>
                    </div>
                    <div className="bg-blue-50 rounded p-3">
                      <div className="flex items-center justify-between">
                        <span className="text-blue-700">Conservative-Bloc</span>
                        <span className="font-bold text-blue-800">42%</span>
                      </div>
                      <div className="text-xs text-blue-600 mt-1">Vote together</div>
                    </div>
                    <div className="bg-green-50 rounded p-3">
                      <div className="flex items-center justify-between">
                        <span className="text-green-700">All Parties</span>
                        <span className="font-bold text-green-800">23%</span>
                      </div>
                      <div className="text-xs text-green-600 mt-1">Unanimous votes</div>
                    </div>
                  </div>
                </div>
              )}

              {selectedVisualization === 'speech-frequency' && (
                <div className="space-y-6">
                  <div className="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
                    <div className="text-center">
                      <p className="text-gray-500 mb-2">MP Speech Frequency Timeline</p>
                      <p className="text-sm text-gray-400">
                        Interactive timeline showing speaking patterns
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {selectedVisualization === 'word-trends' && (
                <div className="space-y-6">
                  <div className="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
                    <div className="text-center">
                      <p className="text-gray-500 mb-2">Word Usage Over Time</p>
                      <p className="text-sm text-gray-400">
                        Track how political vocabulary changes
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Controls */}
              <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-medium text-gray-700 mb-3">Visualization Controls</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">
                      Time Period
                    </label>
                    <select className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm">
                      <option>Last 30 days</option>
                      <option>Last 6 months</option>
                      <option>Last year</option>
                      <option>All time</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-600 mb-1">
                      Data Type
                    </label>
                    <select className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm">
                      <option>All votes</option>
                      <option>Government bills</option>
                      <option>Private bills</option>
                    </select>
                  </div>
                  <div className="flex items-end">
                    <button className="w-full px-4 py-2 bg-op-blue text-white rounded-md hover:bg-blue-700 text-sm">
                      Update
                    </button>
                  </div>
                </div>
              </div>

              {/* Export Options */}
              <div className="mt-6 flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  Data last updated: {new Date().toLocaleDateString('en-CA')}
                </div>
                <div className="flex items-center gap-3">
                  <button className="text-sm text-op-blue hover:underline">
                    Download PNG
                  </button>
                  <button className="text-sm text-op-blue hover:underline">
                    Export Data
                  </button>
                  <button className="text-sm text-op-blue hover:underline">
                    Embed
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Beta Notice */}
      <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-start">
          <svg className="w-5 h-5 text-yellow-600 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h3 className="font-medium text-yellow-900">Beta Feature</h3>
            <p className="text-sm text-yellow-800 mt-1">
              These visualizations are experimental and use sample data. Full interactive 
              versions with real-time data are coming soon.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
