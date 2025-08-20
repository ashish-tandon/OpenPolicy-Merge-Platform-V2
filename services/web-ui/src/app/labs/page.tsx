import Link from 'next/link';

export default function LabsPage() {
  const experiments = [
    {
      id: 'haiku',
      title: 'Parliamentary Haiku',
      description: 'Transform parliamentary speeches into beautiful 5-7-5 haiku poetry',
      icon: '🌸',
      status: 'live',
      link: '/labs/haiku',
    },
    {
      id: 'poetry',
      title: 'Found Poetry',
      description: 'Discover accidental poetry hidden in political discourse',
      icon: '📜',
      status: 'live',
      link: '/labs/poetry',
    },
    {
      id: 'wordplay',
      title: 'Word Analysis Playground',
      description: 'Explore linguistic patterns and word frequencies across debates',
      icon: '🔤',
      status: 'beta',
      link: '/labs/wordplay',
    },
    {
      id: 'visualizations',
      title: 'Data Visualizations',
      description: 'Interactive charts and graphs of parliamentary data',
      icon: '📊',
      status: 'beta',
      link: '/labs/visualizations',
    },
    {
      id: 'sentiment',
      title: 'Sentiment Analysis',
      description: 'Analyze the emotional tone of parliamentary debates',
      icon: '😊',
      status: 'experimental',
      link: '/labs/sentiment',
    },
    {
      id: 'predictions',
      title: 'Vote Predictions',
      description: 'Machine learning predictions for upcoming votes',
      icon: '🔮',
      status: 'experimental',
      link: '/labs/predictions',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'live': return 'bg-green-100 text-green-800';
      case 'beta': return 'bg-yellow-100 text-yellow-800';
      case 'experimental': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="content-container py-8">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-op-dark mb-4">
          OpenParliament Labs
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Experimental features and creative explorations of parliamentary data. 
          These projects showcase innovative ways to engage with democracy.
        </p>
      </div>

      {/* Warning Banner */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
        <div className="flex items-start">
          <svg className="w-5 h-5 text-yellow-600 mr-2 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h3 className="font-medium text-yellow-900">Experimental Features</h3>
            <p className="text-sm text-yellow-800 mt-1">
              These features are experimental and may contain errors, produce unexpected results, 
              or change without notice. They're meant for exploration and entertainment.
            </p>
          </div>
        </div>
      </div>

      {/* Experiments Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {experiments.map((experiment) => (
          <Link
            key={experiment.id}
            href={experiment.link}
            className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 block"
          >
            <div className="flex items-start justify-between mb-4">
              <span className="text-4xl">{experiment.icon}</span>
              <span className={`text-xs px-2 py-1 rounded ${getStatusColor(experiment.status)}`}>
                {experiment.status}
              </span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {experiment.title}
            </h3>
            <p className="text-sm text-gray-600">
              {experiment.description}
            </p>
            <div className="mt-4 text-sm text-op-blue hover:underline">
              Try it out →
            </div>
          </Link>
        ))}
      </div>

      {/* Beta Features Section */}
      <div className="bg-gray-50 rounded-lg p-8 mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Coming Soon
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-medium text-gray-700 mb-2">🎮 Parliamentary Games</h3>
            <p className="text-sm text-gray-600">
              Test your knowledge of Canadian politics with interactive quizzes and games.
            </p>
          </div>
          <div>
            <h3 className="font-medium text-gray-700 mb-2">🤖 Debate Bot</h3>
            <p className="text-sm text-gray-600">
              An AI that can debate any topic using actual parliamentary speech patterns.
            </p>
          </div>
          <div>
            <h3 className="font-medium text-gray-700 mb-2">📱 Mobile App</h3>
            <p className="text-sm text-gray-600">
              Take OpenParliament with you - native iOS and Android apps in development.
            </p>
          </div>
          <div>
            <h3 className="font-medium text-gray-700 mb-2">🎯 Issue Tracker</h3>
            <p className="text-sm text-gray-600">
              Track how specific issues evolve through the parliamentary process.
            </p>
          </div>
        </div>
      </div>

      {/* Developer Section */}
      <div className="bg-blue-50 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-blue-900 mb-4">
          For Developers
        </h2>
        <p className="text-blue-800 mb-6">
          Want to build your own experiments? Our API provides full access to parliamentary data.
        </p>
        <div className="flex flex-wrap gap-4">
          <Link
            href="/api"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition-colors"
          >
            API Documentation
          </Link>
          <a
            href="https://github.com/openparlca"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-800 text-white px-6 py-2 rounded hover:bg-gray-900 transition-colors"
          >
            View on GitHub
          </a>
          <Link
            href="/labs/contribute"
            className="border border-blue-600 text-blue-600 px-6 py-2 rounded hover:bg-blue-50 transition-colors"
          >
            Submit Your Experiment
          </Link>
        </div>
      </div>

      {/* Feedback Section */}
      <div className="mt-12 text-center">
        <p className="text-gray-600 mb-4">
          Have ideas for new experiments? Found a bug? We'd love to hear from you!
        </p>
        <Link
          href="/contact"
          className="text-op-blue hover:underline"
        >
          Send us feedback →
        </Link>
      </div>
    </div>
  );
}
