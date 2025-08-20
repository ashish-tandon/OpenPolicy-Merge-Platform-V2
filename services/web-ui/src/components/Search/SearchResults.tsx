'use client';

import Link from 'next/link';
import { SearchResult } from '@/lib/api';
import Pagination from '@/components/Pagination';

interface SearchResultsProps {
  results: SearchResult[];
  totalCount: number;
  currentPage: number;
  query: string;
  type: string;
}

// Based on legacy search/search_results.inc template
export default function SearchResults({ 
  results, 
  totalCount, 
  currentPage, 
  query, 
  type 
}: SearchResultsProps) {
  const pageSize = 20;
  const totalPages = Math.ceil(totalCount / pageSize);

  // Legacy code maps django_ct to result types
  const getResultTypeLabel = (index: string) => {
    const typeMap: Record<string, string> = {
      'core.politician': 'MP',
      'hansards.statement': 'Debate',
      'bills.bill': 'Bill',
      'committees.committee': 'Committee',
      'committees.meeting': 'Committee Meeting',
      'bills.votequestion': 'Vote',
      // New mappings for our API
      'politicians': 'MP',
      'bills': 'Bill',
      'debates': 'Debate',
      'committees': 'Committee',
      'votes': 'Vote'
    };
    return typeMap[index] || 'Result';
  };

  const getResultUrl = (result: SearchResult) => {
    const source = result._source as any;
    
    // Legacy URL patterns from search_results.inc
    if (result.django_ct) {
      switch (result.django_ct) {
        case 'core.politician':
          return source.url || `/politicians/${source.politician_id}/`;
        case 'hansards.statement':
          return `${source.url}#hl`;
        case 'bills.bill':
          return source.url || `/bills/${source.number}/`;
        default:
          return source.url || '#';
      }
    }
    
    // New API patterns
    switch (result._index) {
      case 'politicians':
        return `/mps/${source.slug || source.politician?.slug}`;
      case 'bills':
        return `/bills/${source.session}/${source.number}`;
      case 'debates':
        return `/debates/${source.date}/${source.number}`;
      case 'committees':
        return `/committees/${source.slug}`;
      case 'votes':
        return `/votes/${source.id}`;
      default:
        return '#';
    }
  };

  const getResultTitle = (result: SearchResult) => {
    const source = result._source as any;
    
    // Legacy patterns from search_results.inc
    if (result.django_ct) {
      switch (result.django_ct) {
        case 'core.politician':
          return source.politician || source.name || 'Unknown MP';
        case 'hansards.statement':
          return source.topic || (source.committee ? `${source.committee} committee` : 'House debate');
        case 'bills.bill':
          return `Bill ${source.number}`;
        default:
          return source.title || source.name || 'Unknown';
      }
    }
    
    // New API patterns
    switch (result._index) {
      case 'politicians':
        return source.name || source.politician?.name || 'Unknown MP';
      case 'bills':
        return `Bill ${source.number}: ${source.name}`;
      case 'debates':
        return source.h1_en || source.title || 'Debate';
      case 'committees':
        return source.name || 'Committee';
      case 'votes':
        return `Vote #${source.number} - ${source.description}`;
      default:
        return source.title || source.name || 'Unknown';
    }
  };

  const getResultDescription = (result: SearchResult) => {
    const source = result._source as any;
    
    // Legacy patterns from search_results.inc
    if (result.django_ct) {
      switch (result.django_ct) {
        case 'core.politician':
          return source.text || '';
        case 'hansards.statement':
          return source.text || '';
        case 'bills.bill':
          return source.text || source.title || '';
        default:
          return source.text || source.description || '';
      }
    }
    
    // New API patterns
    switch (result._index) {
      case 'politicians':
        return `${source.party?.name || ''} ${source.party ? '•' : ''} ${source.riding?.name || ''} ${source.riding?.province ? `(${source.riding.province})` : ''}`;
      case 'bills':
        return source.summary || source.description || 'No description available';
      case 'debates':
        return `${source.statements_count || 0} statements • Parliament ${source.parliament}, Session ${source.session}`;
      case 'committees':
        return source.description || 'Parliamentary committee';
      case 'votes':
        return `${source.result} • ${source.yea_total} yea, ${source.nay_total} nay`;
      default:
        return source.description || source.excerpt || '';
    }
  };

  const getResultMeta = (result: SearchResult) => {
    const source = result._source as any;
    
    // Legacy patterns include date and speaker info
    if (result.django_ct === 'hansards.statement' || result._index === 'debates') {
      return {
        date: source.date,
        speaker: source.politician,
        party: source.party,
        type: source.committee ? 'Committee meeting' : 'House debate'
      };
    }
    
    if (result.django_ct === 'bills.bill' || result._index === 'bills') {
      return {
        date: source.date || source.introduced,
        speaker: source.politician,
        party: source.party,
        type: 'Bill'
      };
    }
    
    return null;
  };

  // Legacy autohighlight function from solr.py
  const getHighlightedText = (result: SearchResult) => {
    if (result.highlight) {
      // Return first highlighted field found
      const fields = Object.keys(result.highlight);
      if (fields.length > 0) {
        return result.highlight[fields[0]][0];
      }
    }
    
    // Legacy uses "text" field for highlighted content
    const source = result._source as any;
    return source.text || null;
  };

  return (
    <div className="space-y-6">
      {/* Results Count - matches legacy template */}
      <div className="row search_header">
        <div className="columns small-12 medium-4 result_summary">
          {totalCount === 0 ? (
            <h2>No results found</h2>
          ) : totalCount === 1 ? (
            <span>1 result found</span>
          ) : (
            <span>
              Results <strong>{(currentPage - 1) * pageSize + 1}</strong>-
              <strong>{Math.min(currentPage * pageSize, totalCount)}</strong> of{' '}
              <strong>{totalCount}</strong>
            </span>
          )}
        </div>
      </div>

      {/* Results List - matches legacy template structure */}
      <div className="space-y-4">
        {results.map((result, index) => {
          const meta = getResultMeta(result);
          const highlightedText = getHighlightedText(result);
          
          return (
            <div key={`${result._index || result.django_ct}-${result._id}-${index}`} 
                 className="row result bg-white rounded-lg shadow-sm border border-gray-200 p-6"
                 data-url={getResultUrl(result)}>
              
              <div className="flex">
                {/* Main content column */}
                <div className="search-main-col flex-1">
                  <p>
                    <Link 
                      href={getResultUrl(result)}
                      className={`font-semibold text-blue-600 hover:text-blue-800 ${
                        result.django_ct === 'core.politician' || result._index === 'politicians' 
                          ? 'pol_name' 
                          : result.django_ct === 'hansards.statement' || result._index === 'debates'
                          ? 'statement_topic'
                          : ''
                      }`}
                    >
                      {getResultTitle(result)}
                    </Link>
                    {result.django_ct === 'bills.bill' && (
                      <span className="pol_affil ml-2 text-gray-600">
                        {(result._source as any).title}
                      </span>
                    )}
                  </p>
                  
                  {/* Highlighted text or description */}
                  {highlightedText && (
                    <p className="mt-2 text-gray-700" 
                       dangerouslySetInnerHTML={{ __html: highlightedText }} />
                  )}
                  {!highlightedText && (
                    <p className="mt-2 text-gray-700">{getResultDescription(result)}</p>
                  )}
                </div>

                {/* Context column - matches legacy template */}
                {meta && (
                  <div className="search-context-col ml-8 w-48 text-sm">
                    {meta.date && (
                      <p className="text-gray-600">
                        {new Date(meta.date).toLocaleDateString('en-US', { 
                          month: 'long', 
                          day: 'numeric', 
                          year: 'numeric' 
                        })}
                        <span className="br slash block sm:inline sm:ml-1">
                          {meta.type}
                        </span>
                      </p>
                    )}
                    {meta.speaker && (
                      <p className="mt-1">
                        <Link href={`/politicians/${(result._source as any).politician_id}/`} 
                              className="pol_name text-blue-600 hover:text-blue-800">
                          {meta.speaker}
                        </Link>
                        {meta.party && (
                          <span className="br space">
                            <span className={`tag partytag_${meta.party.toLowerCase().replace(/\s+/g, '-')} 
                                           ml-1 px-2 py-1 text-xs rounded bg-gray-100`}>
                              {meta.party}
                            </span>
                          </span>
                        )}
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* No Results */}
      {results.length === 0 && totalCount === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No results found for your search.</p>
          <p className="text-sm text-gray-400 mt-2">
            Try adjusting your search terms or filters.
          </p>
        </div>
      )}

      {/* Pagination - using foundation_paginator equivalent */}
      {totalPages > 1 && (
        <div className="mt-8">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            basePath={`/search?q=${encodeURIComponent(query)}&type=${type}`}
          />
        </div>
      )}
    </div>
  );
}
