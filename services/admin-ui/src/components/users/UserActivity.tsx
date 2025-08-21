import { useState, useEffect } from 'react';
import {
  ClockIcon,
  UserIcon,
  DocumentTextIcon,
  ChatBubbleLeftRightIcon,
  HeartIcon,
  ShieldCheckIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  EyeIcon,
  TrashIcon
} from '@heroicons/react/24/outline';

interface ActivityLog {
  id: string;
  userId: string;
  action: string;
  actionType: 'login' | 'logout' | 'vote' | 'comment' | 'like' | 'report' | 'moderate' | 'admin' | 'create' | 'update' | 'delete';
  target?: string;
  targetType?: 'bill' | 'comment' | 'user' | 'system';
  timestamp: string;
  ipAddress: string;
  userAgent: string;
  metadata?: Record<string, any>;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

interface UserActivityProps {
  userId?: string;
  limit?: number;
  showFilters?: boolean;
}

export default function UserActivity({ userId, limit = 50, showFilters = true }: UserActivityProps) {
  const [activities, setActivities] = useState<ActivityLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');
  const [timeRange, setTimeRange] = useState<string>('24h');

  useEffect(() => {
    fetchActivities();
  }, [userId, filter, timeRange]);

  const fetchActivities = async () => {
    try {
      // Mock data - replace with actual API calls
      const mockActivities: ActivityLog[] = [
        {
          id: '1',
          userId: '1',
          action: 'Logged into admin dashboard',
          actionType: 'login',
          timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          ipAddress: '192.168.1.100',
          userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
          severity: 'low'
        },
        {
          id: '2',
          userId: '1',
          action: 'Viewed user management page',
          actionType: 'admin',
          target: 'User Management',
          targetType: 'system',
          timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          ipAddress: '192.168.1.100',
          userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
          severity: 'low'
        },
        {
          id: '3',
          userId: '2',
          action: 'Created new user account',
          actionType: 'create',
          target: 'John Doe',
          targetType: 'user',
          timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
          ipAddress: '192.168.1.101',
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
          severity: 'medium',
          metadata: { role: 'normal', accountType: 'consumer' }
        },
        {
          id: '4',
          userId: '3',
          action: 'Voted on Bill C-123',
          actionType: 'vote',
          target: 'Bill C-123',
          targetType: 'bill',
          timestamp: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
          ipAddress: '203.0.113.42',
          userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
          severity: 'low',
          metadata: { vote: 'yes', billTitle: 'Environmental Protection Act' }
        },
        {
          id: '5',
          userId: '4',
          action: 'Deleted inappropriate comment',
          actionType: 'moderate',
          target: 'Comment #456',
          targetType: 'comment',
          timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
          ipAddress: '192.168.1.102',
          userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
          severity: 'high',
          metadata: { reason: 'spam', originalCommentId: '456' }
        },
        {
          id: '6',
          userId: '1',
          action: 'Updated system settings',
          actionType: 'admin',
          target: 'API Rate Limits',
          targetType: 'system',
          timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          ipAddress: '192.168.1.100',
          userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
          severity: 'critical',
          metadata: { oldValue: '1000/hour', newValue: '2000/hour' }
        }
      ];

      // Filter by userId if provided
      const filteredActivities = userId 
        ? mockActivities.filter(activity => activity.userId === userId)
        : mockActivities;

      setActivities(filteredActivities.slice(0, limit));
    } catch (error) {
      console.error('Failed to fetch user activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActionIcon = (actionType: string) => {
    switch (actionType) {
      case 'login':
      case 'logout':
        return UserIcon;
      case 'vote':
        return CheckCircleIcon;
      case 'comment':
        return ChatBubbleLeftRightIcon;
      case 'like':
        return HeartIcon;
      case 'report':
        return ExclamationTriangleIcon;
      case 'moderate':
        return ShieldCheckIcon;
      case 'admin':
        return ShieldCheckIcon;
      case 'create':
        return DocumentTextIcon;
      case 'update':
        return EyeIcon;
      case 'delete':
        return TrashIcon;
      default:
        return ClockIcon;
    }
  };

  const getActionColor = (actionType: string, severity: string) => {
    if (severity === 'critical') return 'text-red-600 bg-red-100';
    if (severity === 'high') return 'text-orange-600 bg-orange-100';
    if (severity === 'medium') return 'text-yellow-600 bg-yellow-100';
    
    switch (actionType) {
      case 'login':
        return 'text-green-600 bg-green-100';
      case 'logout':
        return 'text-gray-600 bg-gray-100';
      case 'vote':
        return 'text-blue-600 bg-blue-100';
      case 'comment':
        return 'text-purple-600 bg-purple-100';
      case 'like':
        return 'text-pink-600 bg-pink-100';
      case 'report':
        return 'text-red-600 bg-red-100';
      case 'moderate':
        return 'text-orange-600 bg-orange-100';
      case 'admin':
        return 'text-indigo-600 bg-indigo-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getSeverityBadge = (severity: string) => {
    const colors = {
      low: 'bg-green-100 text-green-800',
      medium: 'bg-yellow-100 text-yellow-800',
      high: 'bg-orange-100 text-orange-800',
      critical: 'bg-red-100 text-red-800'
    };
    
    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${colors[severity as keyof typeof colors]}`}>
        {severity}
      </span>
    );
  };

  const formatTimeAgo = (timestamp: string) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInSeconds = Math.floor((now.getTime() - time.getTime()) / 1000);
    
    if (diffInSeconds < 60) return `${diffInSeconds}s ago`;
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    return `${Math.floor(diffInSeconds / 86400)}d ago`;
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="animate-pulse flex space-x-4 p-4 bg-gray-50 rounded-lg">
            <div className="rounded-full bg-gray-300 h-10 w-10"></div>
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-300 rounded w-3/4"></div>
              <div className="h-3 bg-gray-300 rounded w-1/2"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      {showFilters && (
        <div className="flex flex-wrap gap-4 p-4 bg-gray-50 rounded-lg">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Action Type
            </label>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="block w-32 rounded-md border-gray-300 shadow-sm focus:border-op-blue focus:ring-op-blue sm:text-sm"
            >
              <option value="all">All Actions</option>
              <option value="login">Login/Logout</option>
              <option value="vote">Voting</option>
              <option value="comment">Comments</option>
              <option value="moderate">Moderation</option>
              <option value="admin">Admin Actions</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Time Range
            </label>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="block w-32 rounded-md border-gray-300 shadow-sm focus:border-op-blue focus:ring-op-blue sm:text-sm"
            >
              <option value="1h">Last Hour</option>
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
            </select>
          </div>
        </div>
      )}

      {/* Activity Feed */}
      <div className="space-y-3">
        {activities.map((activity) => {
          const IconComponent = getActionIcon(activity.actionType);
          const colorClass = getActionColor(activity.actionType, activity.severity);
          
          return (
            <div key={activity.id} className="flex items-start space-x-3 p-4 bg-white border border-gray-200 rounded-lg hover:shadow-sm transition-shadow">
              <div className={`flex-shrink-0 p-2 rounded-full ${colorClass}`}>
                <IconComponent className="h-5 w-5" />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {activity.action}
                    </p>
                    {activity.target && (
                      <p className="text-xs text-gray-500">
                        Target: {activity.target}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center space-x-2">
                    {getSeverityBadge(activity.severity)}
                    <span className="text-xs text-gray-500">
                      {formatTimeAgo(activity.timestamp)}
                    </span>
                  </div>
                </div>
                
                <div className="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                  <span>IP: {activity.ipAddress}</span>
                  <span>User ID: {activity.userId}</span>
                  {activity.metadata && Object.keys(activity.metadata).length > 0 && (
                    <span>
                      Additional data: {Object.keys(activity.metadata).join(', ')}
                    </span>
                  )}
                </div>
                
                <div className="mt-1 text-xs text-gray-400 truncate">
                  {activity.userAgent}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {activities.length === 0 && (
        <div className="text-center py-8">
          <ClockIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No activity found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {userId ? 'This user has no recorded activity.' : 'No activities match the current filters.'}
          </p>
        </div>
      )}
    </div>
  );
}
