'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { useTranslation } from '@/hooks/useTranslation';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function SearchBar() {
  const { t } = useTranslation();
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
    <div ref={searchRef} className="relative">
      <form onSubmit={handleSubmit}>
        <div className="relative group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t('common.search.placeholder')}
            className="w-full px-4 py-2 pr-10 text-sm bg-background border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent transition-all duration-200 placeholder:text-muted-foreground"
          />
          <button
            type="submit"
            className="absolute right-0 top-0 bottom-0 px-3 text-muted-foreground hover:text-foreground transition-colors"
            aria-label={t('common.search.submit')}
          >
            <MagnifyingGlassIcon className="w-5 h-5" />
          </button>
        </div>
      </form>

      {/* Autocomplete Suggestions */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-card border border-border rounded-lg shadow-lg z-50 animate-fade-in-down">
          {loading ? (
            <div className="px-4 py-2 text-sm text-muted-foreground">{t('common.search.searching')}</div>
          ) : (
            <>
              {isPostalCode(query) && (
                <button
                  onClick={() => {
                    setShowSuggestions(false);
                    router.push(`/search/postal/${encodeURIComponent(query.replace(/\s/g, ''))}`);
                  }}
                  className="w-full px-4 py-2 text-left text-sm hover:bg-accent transition-colors"
                >
                  <span className="font-medium">Find MP for postal code:</span> {query.toUpperCase()}
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
                  className="w-full px-4 py-2 text-left text-sm hover:bg-accent transition-colors border-t border-border first:border-t-0"
                >
                  <div className="font-medium text-foreground">{result._source.name || result._source.title}</div>
                  <div className="text-xs text-muted-foreground">
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
                className="w-full px-4 py-2 text-left text-sm hover:bg-accent transition-colors border-t border-border font-medium text-primary"
              >
                {t('common.actions.viewAll')} "{query}"
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
