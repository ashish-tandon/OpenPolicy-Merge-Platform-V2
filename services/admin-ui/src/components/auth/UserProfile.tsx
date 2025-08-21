import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import {
  UserCircleIcon,
  ChevronDownIcon,
  UserIcon,
  CogIcon,
  ArrowRightOnRectangleIcon,
  ShieldCheckIcon,
  BellIcon
} from '@heroicons/react/24/outline';

export default function UserProfile() {
  const { user, logout, hasRole } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  if (!user) return null;

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'admin': return 'bg-red-100 text-red-800';
      case 'moderator': return 'bg-yellow-100 text-yellow-800';
      case 'representative': return 'bg-purple-100 text-purple-800';
      case 'enterprise': return 'bg-green-100 text-green-800';
      case 'normal': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleLogout = () => {
    logout();
    setIsDropdownOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* User Profile Button */}
      <button
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
        className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 transition-colors"
      >
        {/* Avatar */}
        <div className="flex-shrink-0">
          {user.avatar ? (
            <img
              src={user.avatar}
              alt={`${user.firstName} ${user.lastName}`}
              className="h-8 w-8 rounded-full object-cover"
            />
          ) : (
            <UserCircleIcon className="h-8 w-8 text-gray-400" />
          )}
        </div>

        {/* User Info */}
        <div className="flex-1 min-w-0 text-left hidden sm:block">
          <p className="text-sm font-medium text-gray-900 truncate">
            {user.firstName} {user.lastName}
          </p>
          <p className="text-xs text-gray-500 truncate">
            {user.metadata.organization || user.email}
          </p>
        </div>

        {/* Dropdown Arrow */}
        <ChevronDownIcon 
          className={`h-4 w-4 text-gray-400 transition-transform ${
            isDropdownOpen ? 'transform rotate-180' : ''
          }`} 
        />
      </button>

      {/* Dropdown Menu */}
      {isDropdownOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          {/* User Header */}
          <div className="px-4 py-3 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                {user.avatar ? (
                  <img
                    src={user.avatar}
                    alt={`${user.firstName} ${user.lastName}`}
                    className="h-12 w-12 rounded-full object-cover"
                  />
                ) : (
                  <UserCircleIcon className="h-12 w-12 text-gray-400" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">
                  {user.firstName} {user.lastName}
                </p>
                <p className="text-xs text-gray-500">@{user.username}</p>
                <p className="text-xs text-gray-500">{user.email}</p>
                <div className="mt-1">
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getRoleBadgeColor(user.role)}`}>
                    {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* User Details */}
          <div className="px-4 py-3 border-b border-gray-200">
            <div className="space-y-2">
              {user.metadata.organization && (
                <div className="flex items-center text-xs text-gray-600">
                  <ShieldCheckIcon className="h-4 w-4 mr-2" />
                  {user.metadata.organization}
                  {user.metadata.department && ` - ${user.metadata.department}`}
                </div>
              )}
              <div className="flex items-center text-xs text-gray-600">
                <UserIcon className="h-4 w-4 mr-2" />
                Account Type: {user.accountType}
              </div>
              <div className="flex items-center text-xs text-gray-600">
                <ShieldCheckIcon className="h-4 w-4 mr-2" />
                Permissions: {user.permissions.includes('*') ? 'All Access' : `${user.permissions.length} granted`}
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-1">
            <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              <UserIcon className="h-4 w-4 mr-3 text-gray-400" />
              View Profile
            </button>
            <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              <CogIcon className="h-4 w-4 mr-3 text-gray-400" />
              Account Settings
            </button>
            <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
              <BellIcon className="h-4 w-4 mr-3 text-gray-400" />
              Notifications
            </button>
            
            {/* Admin-only items */}
            {hasRole(['admin', 'moderator']) && (
              <>
                <div className="border-t border-gray-200 my-1"></div>
                <button className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  <ShieldCheckIcon className="h-4 w-4 mr-3 text-gray-400" />
                  Admin Tools
                </button>
              </>
            )}
          </div>

          {/* Logout */}
          <div className="border-t border-gray-200">
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-4 py-2 text-sm text-red-700 hover:bg-red-50"
            >
              <ArrowRightOnRectangleIcon className="h-4 w-4 mr-3 text-red-400" />
              Sign Out
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
