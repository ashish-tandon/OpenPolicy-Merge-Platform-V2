'use client';

import { useState, useEffect, useRef } from 'react';
import { 
  MagnifyingGlassIcon, 
  FunnelIcon, 
  ClockIcon,
  XMarkIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';

interface SearchFilters {
  jurisdiction: string;
  category: string;
  dateRange: string;
  status: string;
  party: string;
}

interface SearchHistory {
  id: string;
  query: string;
  timestamp: Date;
  resultCount: number;
}

interface AdvancedSearchProps {
  onSearch: (query: string, filters: SearchFilters) => void;
  placeholder?: string;
  className?: string;
}

export default function AdvancedSearch({ 
  onSearch, 
  placeholder = "Search bills, MPs, debates, committees...",
  className = ""
}: AdvancedSearchProps) {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<SearchFilters>({
    jurisdiction: '',
    category: '',
    dateRange: '',
    status: '',
    party: ''
  });
  const [showFilters, setShowFilters] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [searchHistory, setSearchHistory] = useState<SearchHistory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  // Load search history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('openpolicy_search_history');
    if (savedHistory) {
      try {
        setSearchHistory(JSON.parse(savedHistory).map((item: any) => ({
          ...item,
          timestamp: new Date(item.timestamp)
        })));
      } catch (_error) {
        console.error('Error loading search history:', error);
      }
    }
  }, []);

  // Save search history to localStorage
  const saveSearchHistory = (query: string, resultCount: number) => {
    const newHistory: SearchHistory = {
      id: Date.now().toString(),
      query,
      timestamp: new Date(),
      resultCount
    };

    const updatedHistory = [newHistory, ...searchHistory.filter(h => h.query !== query)].slice(0, 10);
    setSearchHistory(updatedHistory);
    localStorage.setItem('openpolicy_search_history', JSON.stringify(updatedHistory));
  };

  // Generate search suggestions based on query
  useEffect(() => {
    if (query.length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    const generateSuggestions = async () => {
      try {
        // Get suggestions from API or generate based on common terms
        const commonTerms = [
          'climate change', 'healthcare', 'economy', 'education', 'security',
          'immigration', 'infrastructure', 'taxation', 'environment', 'justice'
        ];

        const filteredSuggestions = commonTerms
          .filter(term => term.toLowerCase().includes(query.toLowerCase()))
          .slice(0, 5);

        setSuggestions(filteredSuggestions);
        setShowSuggestions(filteredSuggestions.length > 0);
      } catch (_error) {
        console.error('Error generating suggestions:', error);
      }
    };

    const debounceTimer = setTimeout(generateSuggestions, 300);
    return () => clearTimeout(debounceTimer);
  }, [query]);

  // Handle search submission
  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      // Perform search (this will be handled by parent component)
      onSearch(query.trim(), filters);
      
      // Save to search history
      saveSearchHistory(query.trim(), 0); // Result count will be updated after search
      
      // Hide suggestions
      setShowSuggestions(false);
    } catch (_error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle suggestion selection
  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    setShowSuggestions(false);
    handleSearch();
  };

  // Handle history item click
  const handleHistoryClick = (historyItem: SearchHistory) => {
    setQuery(historyItem.query);
    handleSearch();
  };

  // Clear search
  const clearSearch = () => {
    setQuery('');
    setFilters({
      jurisdiction: '',
      category: '',
      dateRange: '',
      status: '',
      party: ''
    });
    setShowSuggestions(false);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSearch();
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`relative ${className}`} ref={searchRef}>
      {/* Search Input */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
        </div>
        
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="block w-full pl-10 pr-20 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-op-blue focus:border-op-blue sm:text-sm"
        />
        
        <div className="absolute inset-y-0 right-0 flex items-center pr-2 space-x-1">
          {query && (
            <button
              onClick={clearSearch}
              className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
              title="Clear search"
            >
              <XMarkIcon className="h-4 w-4" />
            </button>
          )}
          
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`p-1 rounded transition-colors ${
              showFilters 
                ? 'text-op-blue bg-op-blue-50' 
                : 'text-gray-400 hover:text-gray-600'
            }`}
            title="Toggle filters"
          >
            <FunnelIcon className="h-4 w-4" />
          </button>
          
          <button
            onClick={handleSearch}
            disabled={!query.trim() || isLoading}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              !query.trim() || isLoading
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-op-blue text-white hover:bg-op-blue-700'
            }`}
          >
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {/* Advanced Filters */}
      {showFilters && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Jurisdiction Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Jurisdiction
              </label>
              <select
                value={filters.jurisdiction}
                onChange={(e) => setFilters({ ...filters, jurisdiction: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
              >
                <option value="">All Jurisdictions</option>
                <option value="federal">Federal</option>
                <option value="provincial">Provincial</option>
                <option value="municipal">Municipal</option>
              </select>
            </div>

            {/* Category Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <select
                value={filters.category}
                onChange={(e) => setFilters({ ...filters, category: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
              >
                <option value="">All Categories</option>
                <option value="bills">Bills</option>
                <option value="mps">Members of Parliament</option>
                <option value="debates">Debates</option>
                <option value="committees">Committees</option>
                <option value="votes">Votes</option>
              </select>
            </div>

            {/* Date Range Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date Range
              </label>
              <select
                value={filters.dateRange}
                onChange={(e) => setFilters({ ...filters, dateRange: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
              >
                <option value="">All Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="year">This Year</option>
                <option value="custom">Custom Range</option>
              </select>
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
              >
                <option value="">All Statuses</option>
                <option value="active">Active</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            {/* Party Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Party
              </label>
              <select
                value={filters.party}
                onChange={(e) => setFilters({ ...filters, party: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
              >
                <option value="">All Parties</option>
                <option value="liberal">Liberal</option>
                <option value="conservative">Conservative</option>
                <option value="ndp">NDP</option>
                <option value="bloc">Bloc Québécois</option>
                <option value="green">Green Party</option>
                <option value="independent">Independent</option>
              </select>
            </div>
          </div>

          {/* Filter Actions */}
          <div className="mt-4 flex justify-between items-center">
            <button
              onClick={() => setFilters({
                jurisdiction: '',
                category: '',
                dateRange: '',
                status: '',
                party: ''
              })}
              className="text-sm text-gray-600 hover:text-gray-800 transition-colors"
            >
              Clear All Filters
            </button>
            
            <div className="text-sm text-gray-500">
              {Object.values(filters).filter(f => f).length} filters active
            </div>
          </div>
        </div>
      )}

      {/* Search Suggestions */}
      {showSuggestions && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg">
          <div className="py-2">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 focus:bg-gray-50 focus:outline-none"
              >
                <MagnifyingGlassIcon className="h-4 w-4 inline mr-2 text-gray-400" />
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Search History */}
      {searchHistory.length > 0 && !showSuggestions && !query && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg">
          <div className="px-4 py-2 border-b border-gray-200">
            <div className="flex items-center text-sm text-gray-600">
              <ClockIcon className="h-4 w-4 mr-2" />
              Recent Searches
            </div>
          </div>
          
          <div className="py-2 max-h-60 overflow-y-auto">
            {searchHistory.map((historyItem) => (
              <button
                key={historyItem.id}
                onClick={() => handleHistoryClick(historyItem)}
                className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 focus:bg-gray-50 focus:outline-none"
              >
                <div className="flex items-center justify-between">
                  <span className="truncate">{historyItem.query}</span>
                  <span className="text-xs text-gray-400 ml-2">
                    {historyItem.timestamp.toLocaleDateString()}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
