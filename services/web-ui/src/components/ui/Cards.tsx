'use client';

import { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import Link from 'next/link';

// Base Card Component
interface BaseCardProps {
  children: ReactNode;
  className?: string;
  as?: 'div' | 'article' | 'section';
  onClick?: () => void;
  href?: string;
  target?: string;
  rel?: string;
}

export function BaseCard({
  children,
  className = "",
  as: Component = 'div',
  onClick,
  href,
  target,
  rel
}: BaseCardProps) {
  const baseClasses = "bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden transition-all duration-200";
  const interactiveClasses = onClick || href ? "hover:shadow-md hover:border-gray-300 cursor-pointer" : "";
  
  const cardClasses = cn(baseClasses, interactiveClasses, className);
  
  if (href) {
    return (
      <Link href={href} target={target} rel={rel} className={cardClasses}>
        {children}
      </Link>
    );
  }
  
  if (onClick) {
    return (
      <Component onClick={onClick} className={cardClasses}>
        {children}
      </Component>
    );
  }
  
  return (
    <Component className={cardClasses}>
      {children}
    </Component>
  );
}

// Bill Card Component
interface BillCardProps {
  bill: {
    id: string;
    title: string;
    billNumber?: string;
    description?: string;
    status?: string;
    introducedDate?: string;
    sponsor?: string;
    party?: string;
  };
  className?: string;
  showActions?: boolean;
  onSave?: () => void;
  onShare?: () => void;
  isSaved?: boolean;
}

export function BillCard({
  bill,
  className = "",
  showActions = true,
  onSave,
  onShare,
  isSaved = false
}: BillCardProps) {
  return (
    <BaseCard
      href={`/bills/${bill.id}`}
      className={cn("group", className)}
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2 mb-2">
              {bill.billNumber && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {bill.billNumber}
                </span>
              )}
              {bill.status && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  {bill.status}
                </span>
              )}
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-op-blue transition-colors line-clamp-2">
              {bill.title}
            </h3>
          </div>
        </div>
        
        {/* Description */}
        {bill.description && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {bill.description}
          </p>
        )}
        
        {/* Metadata */}
        <div className="space-y-2 text-sm text-gray-500">
          {bill.introducedDate && (
            <div className="flex items-center">
              <span className="font-medium">Introduced:</span>
              <span className="ml-2">{new Date(bill.introducedDate).toLocaleDateString()}</span>
            </div>
          )}
          
          {bill.sponsor && (
            <div className="flex items-center">
              <span className="font-medium">Sponsor:</span>
              <span className="ml-2">{bill.sponsor}</span>
              {bill.party && (
                <span className="ml-2 text-xs bg-gray-100 px-2 py-1 rounded">
                  {bill.party}
                </span>
              )}
            </div>
          )}
        </div>
        
        {/* Actions */}
        {showActions && (
          <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              {onSave && (
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    onSave();
                  }}
                  className={cn(
                    "inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md transition-colors",
                    isSaved
                      ? "bg-op-blue-50 text-op-blue-700 border border-op-blue-200"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  )}
                >
                  {isSaved ? 'Saved' : 'Save'}
                </button>
              )}
            </div>
            
            {onShare && (
              <button
                onClick={(e) => {
                  e.preventDefault();
                  onShare();
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                </svg>
              </button>
            )}
          </div>
        )}
      </div>
    </BaseCard>
  );
}

// MP Card Component
interface MPCardProps {
  mp: {
    id: string;
    name: string;
    constituency?: string;
    party?: string;
    province?: string;
    photoUrl?: string;
    role?: string;
    email?: string;
  };
  className?: string;
  showActions?: boolean;
  onSave?: () => void;
  onContact?: () => void;
  isSaved?: boolean;
}

export function MPCard({
  mp,
  className = "",
  showActions = true,
  onSave,
  onContact,
  isSaved = false
}: MPCardProps) {
  return (
    <BaseCard
      href={`/mps/${mp.id}`}
      className={cn("group", className)}
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start space-x-4 mb-4">
          {/* Photo */}
          <div className="flex-shrink-0">
            {mp.photoUrl ? (
              <img
                src={mp.photoUrl}
                alt={mp.name}
                className="h-16 w-16 rounded-full object-cover"
              />
            ) : (
              <div className="h-16 w-16 rounded-full bg-gray-200 flex items-center justify-center">
                <svg className="h-8 w-8 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8c0 2.208-1.79 4-3.998 4-2.208 0-3.998-1.792-3.998-4s1.79-4 3.998-4c2.208 0 3.998 1.792 3.998 4z" />
                </svg>
              </div>
            )}
          </div>
          
          {/* Info */}
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-op-blue transition-colors">
              {mp.name}
            </h3>
            
            <div className="mt-1 space-y-1">
              {mp.constituency && (
                <p className="text-sm text-gray-600">
                  {mp.constituency}
                </p>
              )}
              
              {mp.party && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {mp.party}
                </span>
              )}
              
              {mp.province && (
                <p className="text-sm text-gray-500">
                  {mp.province}
                </p>
              )}
            </div>
          </div>
        </div>
        
        {/* Role */}
        {mp.role && (
          <div className="mb-4">
            <p className="text-sm text-gray-600">
              <span className="font-medium">Role:</span> {mp.role}
            </p>
          </div>
        )}
        
        {/* Actions */}
        {showActions && (
          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              {onSave && (
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    onSave();
                  }}
                  className={cn(
                    "inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md transition-colors",
                    isSaved
                      ? "bg-op-blue-50 text-op-blue-700 border border-op-blue-200"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  )}
                >
                  {isSaved ? 'Saved' : 'Save'}
                </button>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              {onContact && (
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    onContact();
                  }}
                  className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md bg-op-blue text-white hover:bg-op-blue-700 transition-colors"
                >
                  Contact
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </BaseCard>
  );
}

// Debate Card Component
interface DebateCardProps {
  debate: {
    id: string;
    title: string;
    date?: string;
    participants?: string[];
    summary?: string;
    billNumber?: string;
    duration?: string;
  };
  className?: string;
  showActions?: boolean;
  onSave?: () => void;
  onView?: () => void;
  isSaved?: boolean;
}

export function DebateCard({
  debate,
  className = "",
  showActions = true,
  onSave,
  onView,
  isSaved = false
}: DebateCardProps) {
  return (
    <BaseCard
      href={`/debates/${debate.id}`}
      className={cn("group", className)}
    >
      <div className="p-6">
        {/* Header */}
        <div className="mb-4">
          <div className="flex items-center space-x-2 mb-2">
            {debate.billNumber && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                Bill {debate.billNumber}
              </span>
            )}
            {debate.duration && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                {debate.duration}
              </span>
            )}
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-op-blue transition-colors line-clamp-2">
            {debate.title}
          </h3>
        </div>
        
        {/* Summary */}
        {debate.summary && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {debate.summary}
          </p>
        )}
        
        {/* Metadata */}
        <div className="space-y-2 text-sm text-gray-500">
          {debate.date && (
            <div className="flex items-center">
              <span className="font-medium">Date:</span>
              <span className="ml-2">{new Date(debate.date).toLocaleDateString()}</span>
            </div>
          )}
          
          {debate.participants && debate.participants.length > 0 && (
            <div className="flex items-center">
              <span className="font-medium">Participants:</span>
              <span className="ml-2">{debate.participants.join(', ')}</span>
            </div>
          )}
        </div>
        
        {/* Actions */}
        {showActions && (
          <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              {onSave && (
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    onSave();
                  }}
                  className={cn(
                    "inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md transition-colors",
                    isSaved
                      ? "bg-op-blue-50 text-op-blue-700 border border-op-blue-200"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  )}
                >
                  {isSaved ? 'Saved' : 'Save'}
                </button>
              )}
            </div>
            
            {onView && (
              <button
                onClick={(e) => {
                  e.preventDefault();
                  onView();
                }}
                className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md bg-op-blue text-white hover:bg-op-blue-700 transition-colors"
              >
                View Debate
              </button>
            )}
          </div>
        )}
      </div>
    </BaseCard>
  );
}

// Committee Card Component
interface CommitteeCardProps {
  committee: {
    id: string;
    name: string;
    description?: string;
    chair?: string;
    members?: number;
    status?: string;
    type?: string;
  };
  className?: string;
  showActions?: boolean;
  onSave?: () => void;
  onView?: () => void;
  isSaved?: boolean;
}

export function CommitteeCard({
  committee,
  className = "",
  showActions = true,
  onSave,
  onView,
  isSaved = false
}: CommitteeCardProps) {
  return (
    <BaseCard
      href={`/committees/${committee.id}`}
      className={cn("group", className)}
    >
      <div className="p-6">
        {/* Header */}
        <div className="mb-4">
          <div className="flex items-center space-x-2 mb-2">
            {committee.type && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                {committee.type}
              </span>
            )}
            {committee.status && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                {committee.status}
              </span>
            )}
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-op-blue transition-colors line-clamp-2">
            {committee.name}
          </h3>
        </div>
        
        {/* Description */}
        {committee.description && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {committee.description}
          </p>
        )}
        
        {/* Metadata */}
        <div className="space-y-2 text-sm text-gray-500">
          {committee.chair && (
            <div className="flex items-center">
              <span className="font-medium">Chair:</span>
              <span className="ml-2">{committee.chair}</span>
            </div>
          )}
          
          {committee.members && (
            <div className="flex items-center">
              <span className="font-medium">Members:</span>
              <span className="ml-2">{committee.members}</span>
            </div>
          )}
        </div>
        
        {/* Actions */}
        {showActions && (
          <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              {onSave && (
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    onSave();
                  }}
                  className={cn(
                    "inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md transition-colors",
                    isSaved
                      ? "bg-op-blue-50 text-op-blue-700 border border-op-blue-200"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  )}
                >
                  {isSaved ? 'Saved' : 'Save'}
                </button>
              )}
            </div>
            
            {onView && (
              <button
                onClick={(e) => {
                  e.preventDefault();
                  onView();
                }}
                className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md bg-op-blue text-white hover:bg-op-blue-700 transition-colors"
              >
                View Committee
              </button>
            )}
          </div>
        )}
      </div>
    </BaseCard>
  );
}

// Vote Card Component
interface VoteCardProps {
  vote: {
    id: string;
    billTitle: string;
    billNumber?: string;
    date?: string;
    result?: string;
    yesVotes?: number;
    noVotes?: number;
    abstentions?: number;
    type?: string;
  };
  className?: string;
  showActions?: boolean;
  onSave?: () => void;
  onView?: () => void;
  isSaved?: boolean;
}

export function VoteCard({
  vote,
  className = "",
  showActions = true,
  onSave,
  onView,
  isSaved = false
}: VoteCardProps) {
  const getResultColor = (result?: string) => {
    if (!result) return 'bg-gray-100 text-gray-800';
    
    switch (result.toLowerCase()) {
      case 'passed':
        return 'bg-green-100 text-green-800';
      case 'defeated':
        return 'bg-red-100 text-red-800';
      case 'tied':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <BaseCard
      href={`/voting-records/${vote.id}`}
      className={cn("group", className)}
    >
      <div className="p-6">
        {/* Header */}
        <div className="mb-4">
          <div className="flex items-center space-x-2 mb-2">
            {vote.billNumber && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Bill {vote.billNumber}
              </span>
            )}
            {vote.type && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                {vote.type}
              </span>
            )}
            {vote.result && (
              <span className={cn(
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                getResultColor(vote.result)
              )}>
                {vote.result}
              </span>
            )}
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-op-blue transition-colors line-clamp-2">
            {vote.billTitle}
          </h3>
        </div>
        
        {/* Vote Breakdown */}
        {(vote.yesVotes !== undefined || vote.noVotes !== undefined || vote.abstentions !== undefined) && (
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {vote.yesVotes || 0}
              </div>
              <div className="text-xs text-gray-500">Yes</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {vote.noVotes || 0}
              </div>
              <div className="text-xs text-gray-500">No</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {vote.abstentions || 0}
              </div>
              <div className="text-xs text-gray-500">Abstain</div>
            </div>
          </div>
        )}
        
        {/* Metadata */}
        {vote.date && (
          <div className="text-sm text-gray-500 mb-4">
            <span className="font-medium">Vote Date:</span>
            <span className="ml-2">{new Date(vote.date).toLocaleDateString()}</span>
          </div>
        )}
        
        {/* Actions */}
        {showActions && (
          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              {onSave && (
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    onSave();
                  }}
                  className={cn(
                    "inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md transition-colors",
                    isSaved
                      ? "bg-op-blue-50 text-op-blue-700 border border-op-blue-200"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  )}
                >
                  {isSaved ? 'Saved' : 'Save'}
                </button>
              )}
            </div>
            
            {onView && (
              <button
                onClick={(e) => {
                  e.preventDefault();
                  onView();
                }}
                className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md bg-op-blue text-white hover:bg-op-blue-700 transition-colors"
              >
                View Details
              </button>
            )}
          </div>
        )}
      </div>
    </BaseCard>
  );
}
