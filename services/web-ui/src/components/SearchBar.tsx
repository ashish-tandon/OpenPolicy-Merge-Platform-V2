'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const searchRef = useRef<HTMLDivElement>(null);

  // Handle clicks outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Debounced search for autocomplete
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.length >= 2) {
        fetchSuggestions();
      } else {
        setSuggestions([]);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  const fetchSuggestions = async () => {
    setLoading(true);
    try {
      const response = await api.search(query, { page: 1 });
      if (response.results) {
        setSuggestions(response.results.slice(0, 5));
        setShowSuggestions(true);
      }
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setShowSuggestions(false);
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  const isPostalCode = (input: string): boolean => {
    const postalCodeRegex = /^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$/;
    return postalCodeRegex.test(input.trim());
  };

  return (
    <div ref={searchRef} className=""rdquo;""rdquo;ldquo;relative""rdquo;""rdquo;ldquo;>
      <form onSubmit={handleSubmit}>
        <div className=""rdquo;""rdquo;ldquo;relative""rdquo;""rdquo;ldquo;>
          <input
            type=""rdquo;""rdquo;ldquo;text""rdquo;""rdquo;ldquo;
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder=""rdquo;""rdquo;ldquo;Search MPs, bills, debates... or enter postal code""rdquo;""rdquo;ldquo;
            className=""rdquo;""rdquo;ldquo;w-full px-4 py-2 pr-10 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-transparent""rdquo;""rdquo;ldquo;
          />
          <button
            type=""rdquo;""rdquo;ldquo;submit""rdquo;""rdquo;ldquo;
            className=""rdquo;""rdquo;ldquo;absolute right-0 top-0 bottom-0 px-3 text-gray-500 hover:text-op-blue""rdquo;""rdquo;ldquo;
          >
            <svg className=""rdquo;""rdquo;ldquo;w-5 h-5""rdquo;""rdquo;ldquo; fill=""rdquo;""rdquo;ldquo;none""rdquo;""rdquo;ldquo; stroke=""rdquo;""rdquo;ldquo;currentColor""rdquo;""rdquo;ldquo; viewBox=""rdquo;""rdquo;ldquo;0 0 24 24""rdquo;""rdquo;ldquo;>
              <path strokeLinecap=""rdquo;""rdquo;ldquo;round""rdquo;""rdquo;ldquo; strokeLinejoin=""rdquo;""rdquo;ldquo;round""rdquo;""rdquo;ldquo; strokeWidth={2} d=""rdquo;""rdquo;ldquo;M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z""rdquo;""rdquo;ldquo; />
            </svg>
          </button>
        </div>
      </form>

      {/* Autocomplete Suggestions */}
      {showSuggestions && suggestions.length > 0 && (
        <div className=""rdquo;""rdquo;ldquo;absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-md shadow-lg z-50""rdquo;""rdquo;ldquo;>
          {loading ? (
            <div className=""rdquo;""rdquo;ldquo;px-4 py-2 text-sm text-gray-500""rdquo;""rdquo;ldquo;>Searching...</div>
          ) : (
            <>
              {isPostalCode(query) && (
                <button
                  onClick={() => {
                    setShowSuggestions(false);
                    router.push(`/search/postal/${encodeURIComponent(query.replace(/\s/g, ''))}`);
                  }}
                  className=""rdquo;""rdquo;ldquo;w-full px-4 py-2 text-left text-sm hover:bg-gray-100""rdquo;""rdquo;ldquo;
                >
                  <span className=""rdquo;""rdquo;ldquo;font-medium""rdquo;""rdquo;ldquo;>Find MP for postal code:</span> {query.toUpperCase()}
                </button>
              )}
              {suggestions.map((result, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setShowSuggestions(false);
                    // Navigate based on result type
                    if (result._index === 'politicians') {
                      router.push(`/mps/${result._source.slug}`);
                    } else if (result._index === 'bills') {
                      router.push(`/bills/${result._source.session}/${result._source.number}`);
                    } else {
                      router.push(`/search?q=${encodeURIComponent(query)}`);
                    }
                  }}
                  className=""rdquo;""rdquo;ldquo;w-full px-4 py-2 text-left text-sm hover:bg-gray-100 border-t border-gray-100 first:border-t-0""rdquo;""rdquo;ldquo;
                >
                  <div className=""rdquo;""rdquo;ldquo;font-medium""rdquo;""rdquo;ldquo;>{result._source.name || result._source.title}</div>
                  <div className=""rdquo;""rdquo;ldquo;text-xs text-gray-500""rdquo;""rdquo;ldquo;>
                    {result._index === 'politicians' ? 'MP' : 
                     result._index === 'bills' ? 'Bill' : 
                     result._index === 'debates' ? 'Debate' : 
                     result._index}
                  </div>
                </button>
              ))}
              <button
                onClick={() => {
                  setShowSuggestions(false);
                  router.push(`/search?q=${encodeURIComponent(query)}`);
                }}
                className=""rdquo;""rdquo;ldquo;w-full px-4 py-2 text-left text-sm hover:bg-gray-100 border-t border-gray-200""rdquo;""rdquo;ldquo;
              >
                View all results for ""rdquo;""rdquo;ldquo;{query}""rdquo;""rdquo;ldquo;
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
