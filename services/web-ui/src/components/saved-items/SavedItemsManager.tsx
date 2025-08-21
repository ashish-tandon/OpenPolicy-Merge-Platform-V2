'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  BookmarkIcon, 
  TrashIcon, 
  PencilIcon,
  TagIcon,
  AdjustmentsHorizontalIcon,
  MagnifyingGlassIcon,
  AdjustmentsVerticalIcon,
  EyeIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';
import { LoadingState, EmptyState } from '@/components/ui/EmptyState';

interface SavedItem {
  id: string;
  user_id: string;
  item_id: string;
  item_type: 'bill' | 'mp' | 'debate' | 'committee' | 'vote';
  item_title: string;
  item_url: string;
  saved_at: string;
  notes: string;
  tags: string[];
}

interface SavedItemsManagerProps {
  userId: string;
  className?: string;
}

export default function SavedItemsManager({ 
  userId, 
  className = "" 
}: SavedItemsManagerProps) {
  const [savedItems, setSavedItems] = useState<SavedItem[]>([]);
  const [filteredItems, setFilteredItems] = useState<SavedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filters and search
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<'saved_at' | 'item_title' | 'item_type'>('saved_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  
  // UI state
  const [showFilters, setShowFilters] = useState(false);
  const [editingItem, setEditingItem] = useState<string | null>(null);
  const [editNotes, setEditNotes] = useState('');
  const [editTags, setEditTags] = useState('');

  // Load saved items
  useEffect(() => {
    loadSavedItems();
  }, [userId]);

  // Apply filters and search
  useEffect(() => {
    applyFilters();
  }, [savedItems, searchQuery, selectedType, selectedTags, sortBy, sortOrder]);

  const loadSavedItems = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load all saved items for the user
      const allItems: SavedItem[] = [];
      const types: Array<'bill' | 'mp' | 'debate' | 'committee' | 'vote'> = ['bill', 'mp', 'debate', 'committee', 'vote'];
      
      for (const type of types) {
        try {
          const response = await api.getSavedItems(userId, type);
          allItems.push(...response.results);
        } catch (error) {
          console.error(`Error loading ${type} items:`, error);
        }
      }
      
      setSavedItems(allItems);
    } catch (error) {
      console.error('Error loading saved items:', error);
      setError('Failed to load saved items. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...savedItems];

    // Apply search query
    if (searchQuery) {
      filtered = filtered.filter(item =>
        item.item_title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.notes.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    // Apply type filter
    if (selectedType !== 'all') {
      filtered = filtered.filter(item => item.item_type === selectedType);
    }

    // Apply tag filter
    if (selectedTags.length > 0) {
      filtered = filtered.filter(item =>
        selectedTags.some(tag => item.tags.includes(tag))
      );
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: string | Date;
      let bValue: string | Date;

      switch (sortBy) {
        case 'saved_at':
          aValue = new Date(a.saved_at);
          bValue = new Date(b.saved_at);
          break;
        case 'item_title':
          aValue = a.item_title.toLowerCase();
          bValue = b.item_title.toLowerCase();
          break;
        case 'item_type':
          aValue = a.item_type;
          bValue = b.item_type;
          break;
        default:
          aValue = a.saved_at;
          bValue = b.saved_at;
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    setFilteredItems(filtered);
  };

  const handleRemoveItem = async (itemId: string, itemType: string) => {
    if (!confirm('Are you sure you want to remove this item from your saved list?')) {
      return;
    }

    try {
      await api.removeSavedItem(itemId, userId, itemType);
      setSavedItems(prev => prev.filter(item => !(item.id === itemId && item.item_type === itemType)));
    } catch (error) {
      console.error('Error removing saved item:', error);
      alert('Failed to remove item. Please try again.');
    }
  };

  const handleUpdateNotes = async (itemId: string, notes: string) => {
    try {
      await api.updateSavedItem(itemId, { notes });
      setSavedItems(prev => prev.map(item => 
        item.id === itemId ? { ...item, notes } : item
      ));
      setEditingItem(null);
      setEditNotes('');
    } catch (error) {
      console.error('Error updating notes:', error);
      alert('Failed to update notes. Please try again.');
    }
  };

  const handleUpdateTags = async (itemId: string, tagsString: string) => {
    const tags = tagsString.split(',').map(tag => tag.trim()).filter(tag => tag);
    
    try {
      await api.updateSavedItem(itemId, { tags });
      setSavedItems(prev => prev.map(item => 
        item.id === itemId ? { ...item, tags } : item
      ));
      setEditingItem(null);
      setEditTags('');
    } catch (error) {
      console.error('Error updating tags:', error);
      alert('Failed to update tags. Please try again.');
    }
  };

  const getItemTypeIcon = (type: string) => {
    switch (type) {
      case 'bill':
        return '📜';
      case 'mp':
        return '👤';
      case 'debate':
        return '💬';
      case 'committee':
        return '🏛️';
      case 'vote':
        return '✅';
      default:
        return '📄';
    }
  };

  const getItemTypeLabel = (type: string) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  const getItemUrl = (item: SavedItem) => {
    switch (item.item_type) {
      case 'bill':
        return `/bills/${item.item_id}`;
      case 'mp':
        return `/mps/${item.item_id}`;
      case 'debate':
        return `/debates/${item.item_id}`;
      case 'committee':
        return `/committees/${item.item_id}`;
      case 'vote':
        return `/voting-records/${item.item_id}`;
      default:
        return item.item_url;
    }
  };

  const getAllTags = () => {
    const tags = new Set<string>();
    savedItems.forEach(item => {
      item.tags.forEach(tag => tags.add(tag));
    });
    return Array.from(tags).sort();
  };

  if (loading) {
    return <LoadingState title="Loading saved items..." />;
  }

  if (error) {
    return (
      <ErrorState
        title="Error loading saved items"
        description={error}
        action={{
          label: 'Try Again',
          onClick: loadSavedItems
        }}
      />
    );
  }

  if (savedItems.length === 0) {
    return (
      <EmptyState
        type="generic"
        title="No saved items yet"
        description="Start saving bills, MPs, debates, and other parliamentary content to see them here."
        action={{
          label: 'Browse Content',
          onClick: () => window.location.href = '/',
          variant: 'primary'
        }}
      />
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Saved Items</h2>
          <p className="text-gray-600">
            {filteredItems.length} of {savedItems.length} items
          </p>
        </div>
        
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
        >
                          <AdjustmentsHorizontalIcon className="h-4 w-4 mr-2" />
          Filters
        </button>
      </div>

      {/* Filters and Search */}
      {showFilters && (
        <div className="bg-gray-50 rounded-lg p-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Search
              </label>
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search saved items..."
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
                />
              </div>
            </div>

            {/* Type Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
              >
                <option value="all">All Types</option>
                <option value="bill">Bills</option>
                <option value="mp">Members of Parliament</option>
                <option value="debate">Debates</option>
                <option value="committee">Committees</option>
                <option value="vote">Votes</option>
              </select>
            </div>

            {/* Sort By */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Sort By
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
              >
                <option value="saved_at">Date Saved</option>
                <option value="item_title">Title</option>
                <option value="item_type">Type</option>
              </select>
            </div>

            {/* Sort Order */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Order
              </label>
              <button
                onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue flex items-center justify-center"
              >
                <AdjustmentsVerticalIcon className={`h-4 w-4 mr-2 ${sortOrder === 'desc' ? 'rotate-180' : ''}`} />
                {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
              </button>
            </div>
          </div>

          {/* Tag Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filter by Tags
            </label>
            <div className="flex flex-wrap gap-2">
              {getAllTags().map(tag => (
                <button
                  key={tag}
                  onClick={() => setSelectedTags(prev => 
                    prev.includes(tag) 
                      ? prev.filter(t => t !== tag)
                      : [...prev, tag]
                  )}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    selectedTags.includes(tag)
                      ? 'bg-op-blue text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Saved Items List */}
      <div className="space-y-4">
        {filteredItems.map(item => (
          <div key={`${item.id}-${item.item_type}`} className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-lg">{getItemTypeIcon(item.item_type)}</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    {getItemTypeLabel(item.item_type)}
                  </span>
                  <span className="text-sm text-gray-500">
                    Saved {new Date(item.saved_at).toLocaleDateString()}
                  </span>
                </div>
                
                <Link 
                  href={getItemUrl(item)}
                  className="text-lg font-medium text-gray-900 hover:text-op-blue transition-colors block mb-2"
                >
                  {item.item_title}
                </Link>
                
                {/* Notes */}
                {editingItem === item.id ? (
                  <div className="mb-3">
                    <textarea
                      value={editNotes}
                      onChange={(e) => setEditNotes(e.target.value)}
                      placeholder="Add notes..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
                      rows={2}
                    />
                    <div className="flex space-x-2 mt-2">
                      <button
                        onClick={() => handleUpdateNotes(item.id, editNotes)}
                        className="px-2 py-1 text-xs bg-op-blue text-white rounded hover:bg-op-blue-700"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => {
                          setEditingItem(null);
                          setEditNotes('');
                        }}
                        className="px-2 py-1 text-xs bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="mb-3">
                    {item.notes ? (
                      <p className="text-gray-600 text-sm">{item.notes}</p>
                    ) : (
                      <button
                        onClick={() => {
                          setEditingItem(item.id);
                          setEditNotes('');
                        }}
                        className="text-sm text-gray-500 hover:text-gray-700"
                      >
                        Add notes...
                      </button>
                    )}
                  </div>
                )}
                
                {/* Tags */}
                {editingItem === item.id ? (
                  <div className="mb-3">
                    <input
                      type="text"
                      value={editTags}
                      onChange={(e) => setEditTags(e.target.value)}
                      placeholder="Enter tags separated by commas..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue text-sm"
                    />
                    <div className="flex space-x-2 mt-2">
                      <button
                        onClick={() => handleUpdateTags(item.id, editTags)}
                        className="px-2 py-1 text-xs bg-op-blue text-white rounded hover:bg-op-blue-700"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => {
                          setEditingItem(null);
                          setEditTags('');
                        }}
                        className="px-2 py-1 text-xs bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="mb-3">
                    {item.tags.length > 0 ? (
                      <div className="flex flex-wrap gap-1">
                        {item.tags.map(tag => (
                          <span
                            key={tag}
                            className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800"
                          >
                            <TagIcon className="h-3 w-3 mr-1" />
                            {tag}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <button
                        onClick={() => {
                          setEditingItem(item.id);
                          setEditTags('');
                        }}
                        className="text-sm text-gray-500 hover:text-gray-700"
                      >
                        Add tags...
                      </button>
                    )}
                  </div>
                )}
              </div>
              
              <div className="flex items-center space-x-2 ml-4">
                <Link
                  href={getItemUrl(item)}
                  className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                  title="View item"
                >
                  <EyeIcon className="h-4 w-4" />
                </Link>
                
                <button
                  onClick={() => {
                    setEditingItem(item.id);
                    setEditNotes(item.notes);
                    setEditTags(item.tags.join(', '));
                  }}
                  className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                  title="Edit notes and tags"
                >
                  <PencilIcon className="h-4 w-4" />
                </button>
                
                <button
                  onClick={() => handleRemoveItem(item.item_id, item.item_type)}
                  className="p-2 text-red-400 hover:text-red-600 transition-colors"
                  title="Remove from saved items"
                >
                  <TrashIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* No Results */}
      {filteredItems.length === 0 && savedItems.length > 0 && (
        <EmptyState
          type="search"
          title="No items match your filters"
          description="Try adjusting your search criteria or filters to see more results."
          action={{
            label: 'Clear Filters',
            onClick: () => {
              setSearchQuery('');
              setSelectedType('all');
              setSelectedTags([]);
            },
            variant: 'secondary'
          }}
        />
      )}
    </div>
  );
}
