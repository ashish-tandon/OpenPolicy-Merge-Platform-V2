'use client';

import { useState } from 'react';
import Link from 'next/link';

interface Poem {
  id: number;
  title: string;
  lines: string[];
  source: {
    speaker: string;
    date: string;
    context: string;
  };
  style: 'free-verse' | 'found' | 'concrete' | 'erasure';
  themes: string[];
}

export default function PoetryPage() {
  const [poems, setPoems] = useState<Poem[]>([
    {
      id: 1,
      title: "The Weight of Waiting",
      lines: [
        "In emergency rooms across this nation,",
        "families sit in plastic chairs,",
        "counting hours like rosary beads,",
        "while the clock's apos;s hands mock their patience.",
        "",
        "We promised them care,",
        "we promised them healing,",
        "but promises donn't apos;t stop bleeding,",
        "and words cann't apos;t mend what's apos;s broken."
      ],
      source: {
        speaker: "Dr. Jane Smith, MP",
        date: "2025-06-18",
        context: "Debate on Healthcare Funding"
      },
      style: 'found',
      themes: ['healthcare', 'waiting', 'promises']
    },
    {
      id: 2,
      title: "Northern Lights, Southern Worries",
      lines: [
        "The ice",
        "    retreats",
        "        like memory",
        "            from an aging mind,",
        "",
        "leaving",
        "    bare earth",
        "        where white silence",
        "            once reigned."
      ],
      source: {
        speaker: "Hon. Michael Johnson",
        date: "2025-06-15",
        context: "Committee on Climate Change"
      },
      style: 'concrete',
      themes: ['climate', 'north', 'change']
    },
    {
      id: 3,
      title: "Budget Blues",
      lines: [
        "Numbers dance on spreadsheets—",
        "billions here, millions there,",
        "but behind each decimal point",
        "lives a family's apos;s prayer:",
        "",
        "for affordable rent,",
        "for a doctor who'll see them,",
        "for a job that pays enough",
        "to feed more than just dreams."
      ],
      source: {
        speaker: "Sarah Chen, MP",
        date: "2025-06-12",
        context: "Budget Debate"
      },
      style: 'free-verse',
      themes: ['economy', 'poverty', 'hope']
    }
  ]);

  const [selectedStyle, setSelectedStyle] = useState('all');
  const [selectedTheme, setSelectedTheme] = useState('all');
  const [loading, setLoading] = useState(false);

  const styles = [
    { value: 'all', label: 'All Styles' },
    { value: 'found', label: 'Found Poetry' },
    { value: 'free-verse', label: 'Free Verse' },
    { value: 'concrete', label: 'Concrete Poetry' },
    { value: 'erasure', label: 'Erasure Poetry' },
  ];

  const themes = [
    { value: 'all', label: 'All Themes' },
    { value: 'climate', label: 'Climate & Environment' },
    { value: 'healthcare', label: 'Healthcare' },
    { value: 'economy', label: 'Economy' },
    { value: 'justice', label: 'Justice' },
    { value: 'indigenous', label: 'Indigenous' },
  ];

  const filteredPoems = poems.filter(poem => {
    if (selectedStyle !== 'all' && poem.style !== selectedStyle) return false;
    if (selectedTheme !== 'all' && !poem.themes.includes(selectedTheme)) return false;
    return true;
  });

  const generateNewPoems = () => {
    setLoading(true);
    setTimeout(() => {
      // In production, this would fetch new poems from the API
      setPoems([...poems].sort(() => Math.random() - 0.5));
      setLoading(false);
    }, 1000);
  };

  const getStyleDescription = (style: string) => {
    switch (style) {
      case 'found':
        return 'Poetry discovered within natural speech patterns';
      case 'free-verse':
        return 'Restructured parliamentary words into poetic form';
      case 'concrete':
        return 'Visual poetry using spacing and arrangement';
      case 'erasure':
        return 'Poetry created by removing words from original text';
      default:
        return '';
    }
  };

  return (
    <div className="content-container py-8">
      {/* Breadcrumb */}
      <nav className="text-sm mb-6">
        <ol className="flex items-center space-x-2">
          <li><Link href="/" className="text-gray-500 hover:text-op-blue">Home</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li><Link href="/labs" className="text-gray-500 hover:text-op-blue">Labs</Link></li>
          <li><span className="text-gray-400">/</span></li>
          <li className="text-gray-700">Parliamentary Poetry</li>
        </ol>
      </nav>

      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-op-dark mb-4">
          📜 Parliamentary Poetry
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discovering the unexpected beauty in political discourse. 
          These poems are crafted from actual parliamentary speeches.
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Poetry Style
            </label>
            <select
              value={selectedStyle}
              onChange={(e) => setSelectedStyle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
            >
              {styles.map(style => (
                <option key={style.value} value={style.value}>
                  {style.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Theme
            </label>
            <select
              value={selectedTheme}
              onChange={(e) => setSelectedTheme(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
            >
              {themes.map(theme => (
                <option key={theme.value} value={theme.value}>
                  {theme.label}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={generateNewPoems}
              disabled={loading}
              className="w-full px-4 py-2 bg-op-blue text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Discovering...' : 'Discover New Poems'}
            </button>
          </div>
        </div>
      </div>

      {/* Poems Display */}
      <div className="space-y-8">
        {filteredPoems.map((poem) => (
          <div key={poem.id} className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                {poem.title}
              </h2>
              
              <div className={`
                ${poem.style === 'concrete' ? 'font-mono' : ''}
                ${poem.style === 'erasure' ? 'bg-black text-white p-4 rounded' : ''}
                whitespace-pre-line text-gray-700 leading-relaxed
              `}>
                {poem.lines.join('\n')}
              </div>
              
              <div className="mt-6 flex items-center gap-4">
                <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                  {poem.style}
                </span>
                {poem.themes.map(theme => (
                  <span key={theme} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                    #{theme}
                  </span>
                ))}
              </div>
            </div>
            
            <div className="p-6 bg-gray-50">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Source:</span> {poem.source.speaker}
                  </p>
                  <p className="text-sm text-gray-600">
                    {poem.source.date} • {poem.source.context}
                  </p>
                  <p className="text-xs text-gray-500 mt-2 italic">
                    {getStyleDescription(poem.style)}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <button className="text-sm text-op-blue hover:underline">
                    Share
                  </button>
                  <Link
                    href={`/debates/${poem.source.date}`}
                    className="text-sm text-op-blue hover:underline"
                  >
                    View source
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredPoems.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No poems found matching your filters. Try different options!
        </div>
      )}

      {/* About Section */}
      <div className="mt-12 bg-gray-50 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          The Art of Political Poetry
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="font-medium text-gray-700 mb-2">How We Find Poetry</h3>
            <p className="text-sm text-gray-600">
              Our algorithms analyze parliamentary transcripts for:
            </p>
            <ul className="mt-2 space-y-1 text-sm text-gray-600 list-disc list-inside">
              <li>Natural rhythm and cadence</li>
              <li>Emotional resonance</li>
              <li>Metaphorical language</li>
              <li>Repetition and patterns</li>
              <li>Unexpected juxtapositions</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium text-gray-700 mb-2">Poetry Styles Explained</h3>
            <dl className="space-y-2 text-sm">
              <div>
                <dt className="font-medium text-gray-600">Found Poetry:</dt>
                <dd className="text-gray-600">Existing text presented as poetry without changes</dd>
              </div>
              <div>
                <dt className="font-medium text-gray-600">Free Verse:</dt>
                <dd className="text-gray-600">Restructured text without formal rules</dd>
              </div>
              <div>
                <dt className="font-medium text-gray-600">Concrete Poetry:</dt>
                <dd className="text-gray-600">Visual arrangement creates meaning</dd>
              </div>
              <div>
                <dt className="font-medium text-gray-600">Erasure Poetry:</dt>
                <dd className="text-gray-600">New meaning by removing words</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      {/* Submit Your Own */}
      <div className="mt-8 text-center bg-purple-50 rounded-lg p-8">
        <h3 className="text-xl font-bold text-purple-900 mb-4">
          Create Your Own Parliamentary Poetry
        </h3>
        <p className="text-purple-800 mb-6">
          Use our tools to find poetry in any debate or speech
        </p>
        <Link
          href="/labs/poetry/create"
          className="inline-block bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700 transition-colors"
        >
          Poetry Workshop
        </Link>
      </div>
    </div>
  );
}
