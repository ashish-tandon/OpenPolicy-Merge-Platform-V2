import { useState, useEffect } from 'react';
import {
  UserIcon,
  UserGroupIcon,
  ShieldCheckIcon,
  CogIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  LockClosedIcon,
  LockOpenIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ChartBarIcon,
  BuildingOfficeIcon,
  ChatBubbleLeftRightIcon,
  HeartIcon,
  ClockIcon,
  CreditCardIcon,
  BuildingLibraryIcon,
  BeakerIcon,
} from '@heroicons/react/24/outline';
import UserActivity from '../components/users/UserActivity';

interface User {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'normal' | 'enterprise' | 'representative' | 'moderator' | 'admin';
  accountType: 'consumer' | 'internal' | 'test';
  status: 'active' | 'suspended' | 'pending' | 'deactivated';
  createdAt: string;
  lastLogin: string;
  emailVerified: boolean;
  twoFactorEnabled: boolean;
  permissions: string[];
  metadata: {
    organization?: string;
    department?: string;
    phone?: string;
    location?: string;
    preferences?: Record<string, any>;
  };
  activity: {
    totalVotes: number;
    totalComments: number;
    totalLikes: number;
    totalReports: number;
    lastActivity: string;
  };
}

interface UserRole {
  id: string;
  name: string;
  description: string;
  permissions: string[];
  color: string;
  icon: any;
  userCount: number;
}

export default function UserManagement() {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showAccountTypeModal, setShowAccountTypeModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [accountTypeFilter, setAccountTypeFilter] = useState<string>('all');
  const [activeTab, setActiveTab] = useState<'users' | 'roles' | 'activity'>('users');
  const [loading, setLoading] = useState(true);

  const userRoles: UserRole[] = [
    {
      id: 'normal',
      name: 'Normal Consumer Users',
      description: 'Basic users with voting, tracking, and community features',
      permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills'],
      color: 'bg-blue-100 text-blue-800',
      icon: UserIcon,
      userCount: 0
    },
    {
      id: 'enterprise',
      name: 'Enterprise Users',
      description: 'Advanced users with reporting and analytics capabilities',
      permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills', 'build_reports'],
      color: 'bg-green-100 text-green-800',
      icon: BuildingOfficeIcon,
      userCount: 0
    },
    {
      id: 'representative',
      name: 'Representative & Office Users',
      description: 'Government representatives with polling and question capabilities',
      permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills', 'build_polls', 'ask_questions'],
      color: 'bg-purple-100 text-purple-800',
      icon: UserGroupIcon,
      userCount: 0
    },
    {
      id: 'moderator',
      name: 'Moderator Users',
      description: 'Content moderators with deletion and management capabilities',
      permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills', 'delete_accounts', 'delete_comments', 'moderate_content'],
      color: 'bg-yellow-100 text-yellow-800',
      icon: ShieldCheckIcon,
      userCount: 0
    },
    {
      id: 'admin',
      name: 'Admin Users',
      description: 'Backend engineers with full system access',
      permissions: ['*'],
      color: 'bg-red-100 text-red-800',
      icon: CogIcon,
      userCount: 0
    }
  ];

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      // Mock data - replace with actual API calls
      const mockUsers: User[] = [
        {
          id: '1',
          username: 'john_doe',
          email: 'john.doe@example.com',
          firstName: 'John',
          lastName: 'Doe',
          role: 'normal',
          accountType: 'consumer',
          status: 'active',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30).toISOString(),
          lastLogin: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
          emailVerified: true,
          twoFactorEnabled: false,
          permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills'],
          metadata: {
            location: 'Toronto, ON',
            preferences: { theme: 'light', notifications: true }
          },
          activity: {
            totalVotes: 45,
            totalComments: 12,
            totalLikes: 23,
            totalReports: 0,
            lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 1).toISOString()
          }
        },
        {
          id: '2',
          username: 'enterprise_user',
          email: 'admin@enterprise.com',
          firstName: 'Enterprise',
          lastName: 'User',
          role: 'enterprise',
          accountType: 'consumer',
          status: 'active',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 15).toISOString(),
          lastLogin: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
          emailVerified: true,
          twoFactorEnabled: true,
          permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills', 'build_reports'],
          metadata: {
            organization: 'Enterprise Corp',
            department: 'Analytics',
            preferences: { theme: 'dark', notifications: true }
          },
          activity: {
            totalVotes: 156,
            totalComments: 45,
            totalLikes: 89,
            totalReports: 12,
            lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString()
          }
        },
        {
          id: '3',
          username: 'rep_smith',
          email: 'smith@parliament.ca',
          firstName: 'Sarah',
          lastName: 'Smith',
          role: 'representative',
          accountType: 'internal',
          status: 'active',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 90).toISOString(),
          lastLogin: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
          emailVerified: true,
          twoFactorEnabled: true,
          permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills', 'build_polls', 'ask_questions'],
          metadata: {
            organization: 'Parliament of Canada',
            department: 'House of Commons',
            phone: '+1-613-123-4567',
            preferences: { theme: 'light', notifications: true }
          },
          activity: {
            totalVotes: 89,
            totalComments: 67,
            totalLikes: 34,
            totalReports: 5,
            lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString()
          }
        },
        {
          id: '4',
          username: 'moderator_jane',
          email: 'jane@openpolicy.org',
          firstName: 'Jane',
          lastName: 'Wilson',
          role: 'moderator',
          accountType: 'internal',
          status: 'active',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 180).toISOString(),
          lastLogin: new Date(Date.now() - 1000 * 60 * 60 * 1).toISOString(),
          emailVerified: true,
          twoFactorEnabled: true,
          permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills', 'delete_accounts', 'delete_comments', 'moderate_content'],
          metadata: {
            organization: 'OpenPolicy',
            department: 'Content Moderation',
            preferences: { theme: 'dark', notifications: true }
          },
          activity: {
            totalVotes: 234,
            totalComments: 156,
            totalLikes: 89,
            totalReports: 45,
            lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 1).toISOString()
          }
        },
        {
          id: '5',
          username: 'admin_backend',
          email: 'backend@openpolicy.org',
          firstName: 'Admin',
          lastName: 'User',
          role: 'admin',
          accountType: 'internal',
          status: 'active',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 365).toISOString(),
          lastLogin: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString(),
          emailVerified: true,
          twoFactorEnabled: true,
          permissions: ['*'],
          metadata: {
            organization: 'OpenPolicy',
            department: 'Engineering',
            preferences: { theme: 'dark', notifications: true }
          },
          activity: {
            totalVotes: 0,
            totalComments: 0,
            totalLikes: 0,
            totalReports: 0,
            lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString()
          }
        },
        {
          id: '6',
          username: 'test_user',
          email: 'test@openpolicy.org',
          firstName: 'Test',
          lastName: 'User',
          role: 'normal',
          accountType: 'test',
          status: 'active',
          createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5).toISOString(),
          lastLogin: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
          emailVerified: false,
          twoFactorEnabled: false,
          permissions: ['vote', 'track_votes', 'authenticate', 'verify', 'chat', 'comment', 'like_bills'],
          metadata: {
            preferences: { theme: 'light', notifications: false }
          },
          activity: {
            totalVotes: 5,
            totalComments: 2,
            totalLikes: 1,
            totalReports: 0,
            lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString()
          }
        }
      ];

      setUsers(mockUsers);
      
      // Update user counts for each role
      userRoles.forEach(role => {
        role.userCount = mockUsers.filter(user => user.role === role.id).length;
      });
    } catch (error) {
      console.error('Failed to fetch users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChangeAccountType = (userId: string, newAccountType: string) => {
    setUsers(prev => prev.map(user => 
      user.id === userId 
        ? { ...user, accountType: newAccountType as any }
        : user
    ));
    setShowAccountTypeModal(false);
    setSelectedUser(null);
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         `${user.firstName} ${user.lastName}`.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter;
    const matchesAccountType = accountTypeFilter === 'all' || user.accountType === accountTypeFilter;
    
    return matchesSearch && matchesRole && matchesStatus && matchesAccountType;
  });

  const getRoleInfo = (roleId: string) => {
    return userRoles.find(role => role.id === roleId) || userRoles[0];
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'suspended': return 'bg-red-100 text-red-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'deactivated': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getAccountTypeColor = (type: string) => {
    switch (type) {
      case 'consumer': return 'bg-blue-100 text-blue-800';
      case 'internal': return 'bg-purple-100 text-purple-800';
      case 'test': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="lg:pl-64">
        <div className="px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-op-blue"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="lg:pl-64">
      <div className="px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="mt-2 text-gray-600">
            Manage user accounts, roles, permissions, and access across all OpenPolicy platforms
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'users', name: 'Users', icon: UserIcon },
              { id: 'roles', name: 'Roles & Permissions', icon: ShieldCheckIcon },
              { id: 'activity', name: 'Activity Logs', icon: ClockIcon }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-op-blue text-op-blue'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* User Role Overview */}
        {activeTab === 'roles' && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">User Roles & Permissions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {userRoles.map((role) => {
              const IconComponent = role.icon;
              return (
                <div key={role.id} className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center mb-4">
                    <div className={`p-3 rounded-lg ${role.color.split(' ')[0]} ${role.color.split(' ')[1]}`}>
                      <IconComponent className="h-6 w-6" />
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-medium text-gray-900">{role.name}</h3>
                      <p className="text-sm text-gray-500">{role.userCount} users</p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mb-4">{role.description}</p>
                  <div className="space-y-2">
                    <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wide">Key Permissions</h4>
                    <div className="flex flex-wrap gap-1">
                      {role.permissions.slice(0, 3).map((permission) => (
                        <span key={permission} className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700">
                          {permission.replace('_', ' ')}
                        </span>
                      ))}
                      {role.permissions.length > 3 && (
                        <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700">
                          +{role.permissions.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          </div>
        )}

        {/* Activity Logs Tab */}
        {activeTab === 'activity' && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">User Activity Logs</h2>
            <UserActivity showFilters={true} limit={100} />
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div>
            {/* Controls */}
            <div className="mb-6 flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
          <div className="flex flex-col sm:flex-row gap-4">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                Search Users
              </label>
              <input
                type="text"
                id="search"
                placeholder="Search by username, email, or name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="block w-full sm:w-64 rounded-md border-gray-300 shadow-sm focus:border-op-blue focus:ring-op-blue sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="role-filter" className="block text-sm font-medium text-gray-700 mb-1">
                Filter by Role
              </label>
              <select
                id="role-filter"
                value={roleFilter}
                onChange={(e) => setRoleFilter(e.target.value)}
                className="block w-full sm:w-40 rounded-md border-gray-300 shadow-sm focus:border-op-blue focus:ring-op-blue sm:text-sm"
              >
                <option value="all">All Roles</option>
                {userRoles.map((role) => (
                  <option key={role.id} value={role.id}>{role.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="status-filter" className="block text-sm font-medium text-gray-700 mb-1">
                Filter by Status
              </label>
              <select
                id="status-filter"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="block w-full sm:w-40 rounded-md border-gray-300 shadow-sm focus:border-op-blue focus:ring-op-blue sm:text-sm"
              >
                <option value="all">All Statuses</option>
                <option value="active">Active</option>
                <option value="suspended">Suspended</option>
                <option value="pending">Pending</option>
                <option value="deactivated">Deactivated</option>
              </select>
            </div>
            <div>
              <label htmlFor="account-type-filter" className="block text-sm font-medium text-gray-700 mb-1">
                Filter by Account Type
              </label>
              <select
                id="account-type-filter"
                value={accountTypeFilter}
                onChange={(e) => setAccountTypeFilter(e.target.value)}
                className="block w-full sm:w-40 rounded-md border-gray-300 shadow-sm focus:border-op-blue focus:ring-op-blue sm:text-sm"
              >
                <option value="all">All Account Types</option>
                <option value="consumer">Consumer</option>
                <option value="internal">Internal</option>
                <option value="test">Test</option>
              </select>
            </div>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-op-blue hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Add User
          </button>
        </div>

        {/* Users Table */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              Users ({filteredUsers.length})
            </h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Role
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Account Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Activity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Security
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Login
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredUsers.map((user) => {
                  const roleInfo = getRoleInfo(user.role);
                  return (
                    <tr key={user.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-10 w-10">
                            <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                              <UserIcon className="h-6 w-6 text-gray-600" />
                            </div>
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-medium text-gray-900">
                              {user.firstName} {user.lastName}
                            </div>
                            <div className="text-sm text-gray-500">{user.username}</div>
                            <div className="text-sm text-gray-500">{user.email}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${roleInfo.color}`}>
                          {roleInfo.name.split(' ')[0]}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAccountTypeColor(user.accountType)}`}>
                          {user.accountType}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(user.status)}`}>
                          {user.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          <div className="flex items-center space-x-4 text-xs">
                            <span title="Votes">
                              <ChartBarIcon className="h-4 w-4 inline mr-1" />
                              {user.activity.totalVotes}
                            </span>
                            <span title="Comments">
                              <ChatBubbleLeftRightIcon className="h-4 w-4 inline mr-1" />
                              {user.activity.totalComments}
                            </span>
                            <span title="Likes">
                              <HeartIcon className="h-4 w-4 inline mr-1" />
                              {user.activity.totalLikes}
                            </span>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          {user.emailVerified ? (
                            <CheckCircleIcon className="h-4 w-4 text-green-600" title="Email Verified" />
                          ) : (
                            <ExclamationTriangleIcon className="h-4 w-4 text-yellow-600" title="Email Not Verified" />
                          )}
                          {user.twoFactorEnabled ? (
                            <LockClosedIcon className="h-4 w-4 text-blue-600" title="2FA Enabled" />
                          ) : (
                            <LockOpenIcon className="h-4 w-4 text-gray-400" title="2FA Disabled" />
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(user.lastLogin).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => setSelectedUser(user)}
                            className="text-op-blue hover:text-blue-700"
                            title="View Details"
                          >
                            <EyeIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => {
                              setSelectedUser(user);
                              setShowEditModal(true);
                            }}
                            className="text-gray-400 hover:text-gray-600"
                            title="Edit User"
                          >
                            <PencilIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => {
                              setSelectedUser(user);
                              setShowDeleteModal(true);
                            }}
                            className="text-red-400 hover:text-red-600"
                            title="Delete User"
                          >
                            <TrashIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => {
                              setSelectedUser(user);
                              setShowAccountTypeModal(true);
                            }}
                            className="text-purple-400 hover:text-purple-600"
                            title="Change Account Type"
                          >
                            <CreditCardIcon className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* User Detail Modal */}
        {selectedUser && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  User Details: {selectedUser.firstName} {selectedUser.lastName}
                </h3>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Username</h4>
                      <p className="text-sm text-gray-900">{selectedUser.username}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Email</h4>
                      <p className="text-sm text-gray-900">{selectedUser.email}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Role</h4>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleInfo(selectedUser.role).color}`}>
                        {getRoleInfo(selectedUser.role).name}
                      </span>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Account Type</h4>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAccountTypeColor(selectedUser.accountType)}`}>
                        {selectedUser.accountType}
                      </span>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Status</h4>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(selectedUser.status)}`}>
                        {selectedUser.status}
                      </span>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Created</h4>
                      <p className="text-sm text-gray-900">{new Date(selectedUser.createdAt).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-2">Permissions</h4>
                    <div className="flex flex-wrap gap-1">
                      {selectedUser.permissions.map((permission) => (
                        <span key={permission} className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700">
                          {permission.replace('_', ' ')}
                        </span>
                      ))}
                    </div>
                  </div>
                  {selectedUser.metadata.organization && (
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <h4 className="text-sm font-medium text-gray-500">Organization</h4>
                        <p className="text-sm text-gray-900">{selectedUser.metadata.organization}</p>
                      </div>
                      {selectedUser.metadata.department && (
                        <div>
                          <h4 className="text-sm font-medium text-gray-500">Department</h4>
                          <p className="text-sm text-gray-900">{selectedUser.metadata.department}</p>
                        </div>
                      )}
                    </div>
                  )}
                  <div>
                    <h4 className="text-sm font-medium text-gray-500 mb-2">Activity Summary</h4>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>Total Votes: {selectedUser.activity.totalVotes}</div>
                      <div>Total Comments: {selectedUser.activity.totalComments}</div>
                      <div>Total Likes: {selectedUser.activity.totalLikes}</div>
                      <div>Total Reports: {selectedUser.activity.totalReports}</div>
                    </div>
                  </div>
                </div>
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setSelectedUser(null)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Create/Edit User Modal Placeholder */}
        {(showCreateModal || showEditModal) && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  {showCreateModal ? 'Create New User' : 'Edit User'}
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  User creation and editing functionality will be implemented here.
                </p>
                <div className="mt-6 flex justify-end space-x-3">
                  <button
                    onClick={() => {
                      setShowCreateModal(false);
                      setShowEditModal(false);
                    }}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                  <button className="px-4 py-2 bg-op-blue text-white rounded-md hover:bg-blue-700">
                    {showCreateModal ? 'Create User' : 'Save Changes'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Delete User Modal Placeholder */}
        {showDeleteModal && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Delete User
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Are you sure you want to delete {selectedUser?.firstName} {selectedUser?.lastName}? This action cannot be undone.
                </p>
                <div className="mt-6 flex justify-end space-x-3">
                  <button
                    onClick={() => setShowDeleteModal(false)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                  <button className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
                    Delete User
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Change Account Type Modal */}
        {showAccountTypeModal && selectedUser && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Change Account Type
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Change account type for {selectedUser.firstName} {selectedUser.lastName}
                </p>
                
                <div className="space-y-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Current Account Type
                    </label>
                    <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-md">
                      {selectedUser.accountType === 'consumer' && <CreditCardIcon className="h-5 w-5 text-blue-500" />}
                      {selectedUser.accountType === 'internal' && <BuildingLibraryIcon className="h-5 w-5 text-green-500" />}
                      {selectedUser.accountType === 'test' && <BeakerIcon className="h-5 w-5 text-purple-500" />}
                      <span className="text-sm font-medium text-gray-900 capitalize">
                        {selectedUser.accountType}
                      </span>
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      New Account Type
                    </label>
                    <select 
                      id="newAccountType"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
                    >
                      <option value="consumer">Consumer - Basic user with voting and tracking</option>
                      <option value="internal">Internal - Advanced user with reporting</option>
                      <option value="test">Test - Limited access for testing</option>
                    </select>
                  </div>
                </div>
                
                <div className="mt-6 flex justify-end space-x-3">
                  <button
                    onClick={() => setShowAccountTypeModal(false)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                  <button 
                    onClick={() => {
                      const newType = (document.getElementById('newAccountType') as HTMLSelectElement).value;
                      handleChangeAccountType(selectedUser.id, newType);
                    }}
                    className="px-4 py-2 bg-op-blue text-white rounded-md hover:bg-blue-700"
                  >
                    Change Account Type
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
          </div>
        )}
      </div>
    </div>
  );
}
