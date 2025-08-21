'use client';

import { useState, useEffect } from 'react';
import { 
  BookmarkIcon as BookmarkOutline,
  BookmarkIcon as BookmarkSolid
} from '@heroicons/react/24/outline';
import { BookmarkIcon as BookmarkFilled } from '@heroicons/react/24/solid';
import { api } from '@/lib/api';

interface SaveButtonProps {
  itemId: string;
  itemType: 'bill' | 'mp' | 'debate' | 'committee' | 'vote';
  itemTitle: string;
  itemUrl: string;
  userId?: string;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
  onSaveChange?: (saved: boolean) => void;
}

export default function SaveButton({
  itemId,
  itemType,
  itemTitle,
  itemUrl,
  userId,
  className = "",
  size = 'md',
  showText = false,
  onSaveChange
}: SaveButtonProps) {
  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  // Check if item is already saved
  useEffect(() => {
    if (!userId) return;
    
    const checkSavedStatus = async () => {
      try {
        const response = await api.getSavedItems(userId, itemType);
        const saved = response.results.some((item: any) => item.item_id === itemId);
        setIsSaved(saved);
      } catch (error) {
        console.error('Error checking saved status:', error);
      }
    };

    checkSavedStatus();
  }, [itemId, itemType, userId]);

  const handleSaveToggle = async () => {
    if (!userId) {
      // Redirect to login or show login modal
      alert('Please log in to save items');
      return;
    }

    setIsLoading(true);
    try {
      if (isSaved) {
        // Remove from saved items
        await api.removeSavedItem(itemId, userId, itemType);
        setIsSaved(false);
        onSaveChange?.(false);
      } else {
        // Add to saved items
        const savedItemData = {
          user_id: userId,
          item_id: itemId,
          item_type: itemType,
          item_title: itemTitle,
          item_url: itemUrl,
          saved_at: new Date().toISOString(),
          notes: '',
          tags: []
        };
        
        await api.addSavedItem(savedItemData);
        setIsSaved(true);
        onSaveChange?.(true);
      }
    } catch (error) {
      console.error('Error toggling save status:', error);
      alert('Failed to update saved status. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return 'px-2 py-1 text-xs';
      case 'lg':
        return 'px-4 py-2 text-base';
      default:
        return 'px-3 py-1.5 text-sm';
    }
  };

  const getIconSize = () => {
    switch (size) {
      case 'sm':
        return 'h-4 w-4';
      case 'lg':
        return 'h-6 w-6';
      default:
        return 'h-5 w-5';
    }
  };

  const getButtonText = () => {
    if (isLoading) return 'Saving...';
    if (isSaved) return isHovered ? 'Remove' : 'Saved';
    return 'Save';
  };

  const getButtonClasses = () => {
    const baseClasses = `inline-flex items-center space-x-2 rounded-md font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 ${getSizeClasses()}`;
    
    if (isLoading) {
      return `${baseClasses} bg-gray-300 text-gray-500 cursor-not-allowed`;
    }
    
    if (isSaved) {
      return `${baseClasses} bg-op-blue-50 text-op-blue-700 border border-op-blue-200 hover:bg-op-blue-100 hover:border-op-blue-300 focus:ring-op-blue`;
    }
    
    return `${baseClasses} bg-op-blue text-white hover:bg-op-blue-700 focus:ring-op-blue`;
  };

  return (
    <button
      onClick={handleSaveToggle}
      disabled={isLoading}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`${getButtonClasses()} ${className}`}
      title={isSaved ? 'Remove from saved items' : 'Save to your list'}
    >
      {isLoading ? (
        <div className={`animate-spin rounded-full border-2 border-current border-t-transparent ${getIconSize()}`} />
      ) : isSaved ? (
        <BookmarkFilled className={getIconSize()} />
      ) : (
        <BookmarkOutline className={getIconSize()} />
      )}
      
      {showText && (
        <span>{getButtonText()}</span>
      )}
    </button>
  );
}

// Specialized save buttons for different item types
export function BillSaveButton(props: Omit<SaveButtonProps, 'itemType'>) {
  return <SaveButton {...props} itemType="bill" />;
}

export function MPSaveButton(props: Omit<SaveButtonProps, 'itemType'>) {
  return <SaveButton {...props} itemType="mp" />;
}

export function DebateSaveButton(props: Omit<SaveButtonProps, 'itemType'>) {
  return <SaveButton {...props} itemType="debate" />;
}

export function CommitteeSaveButton(props: Omit<SaveButtonProps, 'itemType'>) {
  return <SaveButton {...props} itemType="committee" />;
}

export function VoteSaveButton(props: Omit<SaveButtonProps, 'itemType'>) {
  return <SaveButton {...props} itemType="vote" />;
}
