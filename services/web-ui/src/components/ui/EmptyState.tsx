import { 
  DocumentTextIcon, 
  UserGroupIcon, 
  ChatBubbleLeftRightIcon,
  BuildingOfficeIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  MagnifyingGlassIcon,
  NoSymbolIcon
} from '@heroicons/react/24/outline';

interface EmptyStateProps {
  type: 'bills' | 'mps' | 'debates' | 'committees' | 'votes' | 'search' | 'generic';
  title?: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
    variant?: 'primary' | 'secondary';
  };
  className?: string;
}

export default function EmptyState({ 
  type, 
  title, 
  description, 
  action,
  className = ""
}: EmptyStateProps) {
  const getIcon = () => {
    switch (type) {
      case 'bills':
        return <DocumentTextIcon className="h-12 w-12 text-gray-400" />;
      case 'mps':
        return <UserGroupIcon className="h-12 w-12 text-gray-400" />;
      case 'debates':
        return <ChatBubbleLeftRightIcon className="h-12 w-12 text-gray-400" />;
      case 'committees':
        return <BuildingOfficeIcon className="h-12 w-12 text-gray-400" />;
      case 'votes':
        return <CheckCircleIcon className="h-12 w-12 text-gray-400" />;
      case 'search':
        return <MagnifyingGlassIcon className="h-12 w-12 text-gray-400" />;
      case 'generic':
        return <InformationCircleIcon className="h-12 w-12 text-gray-400" />;
      default:
        return <NoSymbolIcon className="h-12 w-12 text-gray-400" />;
    }
  };

  const getDefaultTitle = () => {
    switch (type) {
      case 'bills':
        return 'No Bills Found';
      case 'mps':
        return 'No Members of Parliament Found';
      case 'debates':
        return 'No Debates Found';
      case 'committees':
        return 'No Committees Found';
      case 'votes':
        return 'No Voting Records Found';
      case 'search':
        return 'No Search Results';
      case 'generic':
        return 'No Data Available';
      default:
        return 'No Items Found';
    }
  };

  const getDefaultDescription = () => {
    switch (type) {
      case 'bills':
        return 'There are no bills matching your criteria. Try adjusting your filters or search terms.';
      case 'mps':
        return 'No Members of Parliament match your search criteria. Try different search terms or filters.';
      case 'debates':
        return 'No debate transcripts or summaries found. Check back later for new content.';
      case 'committees':
        return 'No committees found matching your criteria. Try adjusting your search or filters.';
      case 'votes':
        return 'No voting records found for the specified criteria. Try different search terms or date ranges.';
      case 'search':
        return 'No results found for your search. Try different keywords or check your spelling.';
      case 'generic':
        return 'No data is currently available. Please check back later or contact support if you need assistance.';
      default:
        return 'No items match your current criteria. Try adjusting your search or filters.';
    }
  };

  return (
    <div className={`text-center py-12 ${className}`}>
      <div className="flex justify-center mb-4">
        {getIcon()}
      </div>
      
      <h3 className="text-lg font-medium text-gray-900 mb-2">
        {title || getDefaultTitle()}
      </h3>
      
      <p className="text-gray-600 max-w-md mx-auto mb-6">
        {description || getDefaultDescription()}
      </p>
      
      {action && (
        <button
          onClick={action.onClick}
          className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md transition-colors ${
            action.variant === 'secondary'
              ? 'text-op-blue bg-op-blue-50 border-op-blue-200 hover:bg-op-blue-100'
              : 'text-white bg-op-blue hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue'
          }`}
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

// Specialized empty state components
export function BillsEmptyState({ 
  title, 
  description, 
  action,
  className 
}: Omit<EmptyStateProps, 'type'>) {
  return (
    <EmptyState
      type="bills"
      title={title}
      description={description}
      action={action}
      className={className}
    />
  );
}

export function MPsEmptyState({ 
  title, 
  description, 
  action,
  className 
}: Omit<EmptyStateProps, 'type'>) {
  return (
    <EmptyState
      type="mps"
      title={title}
      description={description}
      action={action}
      className={className}
    />
  );
}

export function DebatesEmptyState({ 
  title, 
  description, 
  action,
  className 
}: Omit<EmptyStateProps, 'type'>) {
  return (
    <EmptyState
      type="debates"
      title={title}
      description={description}
      action={action}
      className={className}
    />
  );
}

export function CommitteesEmptyState({ 
  title, 
  description, 
  action,
  className 
}: Omit<EmptyStateProps, 'type'>) {
  return (
    <EmptyState
      type="committees"
      title={title}
      description={description}
      action={action}
      className={className}
    />
  );
}

export function VotesEmptyState({ 
  title, 
  description, 
  action,
  className 
}: Omit<EmptyStateProps, 'type'>) {
  return (
    <EmptyState
      type="votes"
      title={title}
      description={description}
      action={action}
      className={className}
    />
  );
}

export function SearchEmptyState({ 
  title, 
  description, 
  action,
  className 
}: Omit<EmptyStateProps, 'type'>) {
  return (
    <EmptyState
      type="search"
      title={title}
      description={description}
      action={action}
      className={className}
    />
  );
}

// Error state component
export function ErrorState({ 
  title = 'Something went wrong',
  description = 'An error occurred while loading the data. Please try again.',
  action,
  className = ""
}: {
  title?: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}) {
  return (
    <div className={`text-center py-12 ${className}`}>
      <div className="flex justify-center mb-4">
        <ExclamationTriangleIcon className="h-12 w-12 text-red-400" />
      </div>
      
      <h3 className="text-lg font-medium text-gray-900 mb-2">
        {title}
      </h3>
      
      <p className="text-gray-600 max-w-md mx-auto mb-6">
        {description}
      </p>
      
      {action && (
        <button
          onClick={action.onClick}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

// Loading state component
export function LoadingState({ 
  title = 'Loading...',
  description = 'Please wait while we fetch the data.',
  className = ""
}: {
  title?: string;
  description?: string;
  className?: string;
}) {
  return (
    <div className={`text-center py-12 ${className}`}>
      <div className="flex justify-center mb-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-op-blue"></div>
      </div>
      
      <h3 className="text-lg font-medium text-gray-900 mb-2">
        {title}
      </h3>
      
      <p className="text-gray-600 max-w-md mx-auto">
        {description}
      </p>
    </div>
  );
}
