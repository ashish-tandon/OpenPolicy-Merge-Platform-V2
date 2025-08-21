'use client';

import { useState } from 'react';
import { 
  UserIcon, 
  DocumentTextIcon, 
  FlagIcon, 
  ChatBubbleLeftRightIcon,
  BookmarkIcon,
  HeartIcon,
  ExclamationTriangleIcon,
  MapPinIcon,
  DevicePhoneMobileIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';
import { 
  MobileUser, 
  MobileBill, 
  MobileIssue, 
  MobileRepresentative,
  UserRegistrationData,
  UserLoginData,
  IssueCreationData,
  BillSupportData
} from '@/types/mobile-app';

export default function MobileAppDemo() {
  const [activeTab, setActiveTab] = useState<'overview' | 'user' | 'bills' | 'issues' | 'representatives' | 'chat'>('overview');
  const [demoData, setDemoData] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Demo user data
  const demoUser: UserRegistrationData = {
    name: "Demo User",
    email: "demo@example.com",
    password: "demo123",
    postal_code: "A1B2C3"
  };

  const demoBill: MobileBill = {
    id: 201,
    number: "B-234",
    title: "Education Reform Act",
    description: "Improves public education standards and funding.",
    status: "active",
    support_percentage: 65,
    oppose_percentage: 35,
    bookmarked: false,
    app_summary: "Reforms educational standards and funding."
  };

  const demoIssue: IssueCreationData = {
    bill_id: 201,
    title: "Funding clarification needed",
    description: "The bill description lacks details about funding allocation."
  };

  const handleApiCall = async (apiMethod: () => Promise<any>, description: string) => {
    setLoading(true);
    setMessage('');
    
    try {
      const result = await apiMethod();
      setDemoData(result);
      setMessage(`✅ ${description} successful!`);
    } catch (error) {
      console.error('API Error:', error);
      setMessage(`❌ ${description} failed: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const renderOverview = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <DevicePhoneMobileIcon className="h-6 w-6 text-blue-600 mr-2" />
          Mobile App Feature Parity
        </h3>
        <p className="text-gray-700 mb-4">
          The OpenPolicy web platform now provides 100% feature parity with the mobile app, 
          ensuring a seamless cross-platform experience for all users.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-gray-900 mb-2">✅ User Management</h4>
            <p className="text-sm text-gray-600">Registration, login, profile management, password changes</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-gray-900 mb-2">✅ Bill Management</h4>
            <p className="text-sm text-gray-600">Browse, search, support/oppose, bookmark bills</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-gray-900 mb-2">✅ Issue Reporting</h4>
            <p className="text-sm text-gray-600">Create, support, bookmark, and manage issues</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-gray-900 mb-2">✅ Representative Lookup</h4>
            <p className="text-sm text-gray-600">Find and contact your representatives</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-gray-900 mb-2">✅ AI Chat</h4>
            <p className="text-sm text-gray-600">Interactive AI-powered bill explanations</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-gray-900 mb-2">✅ Cross-Platform Sync</h4>
            <p className="text-sm text-gray-600">Unified data and preferences across devices</p>
          </div>
        </div>
      </div>

      <div className="bg-green-50 rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <GlobeAltIcon className="h-6 w-6 text-green-600 mr-2" />
          Web Platform Advantages
        </h3>
        <p className="text-gray-700 mb-4">
          While maintaining full mobile app compatibility, the web platform offers additional features:
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 border border-green-200">
            <h4 className="font-medium text-gray-900 mb-2">🖥️ Desktop Experience</h4>
            <p className="text-sm text-gray-600">Full-screen interface with advanced navigation</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-green-200">
            <h4 className="font-medium text-gray-900 mb-2">🔗 Deep Linking</h4>
            <p className="text-sm text-gray-600">Share specific bills and pages via URLs</p>
          </div>
          <div className="bg-white rounded-lg p-4 border border-green-200">
            <h4 className="font-medium text-gray-900 mb-2">📊 Advanced Analytics</h4>
            <p className="text-sm text-gray-600">Comprehensive voting and engagement data</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderUserManagement = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <UserIcon className="h-5 w-5 text-blue-600 mr-2" />
          User Registration & Authentication
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Registration</h4>
            <button
              onClick={() => handleApiCall(
                () => api.mobileAppRegister(demoUser),
                'User registration'
              )}
              disabled={loading}
              className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Registering...' : 'Register Demo User'}
            </button>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Login</h4>
            <button
              onClick={() => handleApiCall(
                () => api.mobileAppLogin({ email: demoUser.email, password: demoUser.password }),
                'User login'
              )}
              disabled={loading}
              className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Logging in...' : 'Login Demo User'}
            </button>
          </div>
        </div>
        
        <div className="mt-4">
          <h4 className="font-medium text-gray-900 mb-3">Profile Management</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <button
              onClick={() => handleApiCall(
                () => api.mobileAppGetProfile(),
                'Fetch profile'
              )}
              disabled={loading}
              className="bg-gray-600 text-white px-3 py-2 rounded-md hover:bg-gray-700 disabled:opacity-50 text-sm"
            >
              Get Profile
            </button>
            <button
              onClick={() => handleApiCall(
                () => api.mobileAppUpdateProfile({ name: "Updated Demo User" }),
                'Update profile'
              )}
              disabled={loading}
              className="bg-purple-600 text-white px-3 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 text-sm"
            >
              Update Profile
            </button>
            <button
              onClick={() => handleApiCall(
                () => api.mobileAppChangePassword({ old_password: "demo123", new_password: "newdemo123" }),
                'Change password'
              )}
              disabled={loading}
              className="bg-orange-600 text-white px-3 py-2 rounded-md hover:bg-orange-700 disabled:opacity-50 text-sm"
            >
              Change Password
            </button>
          </div>
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-md ${
          message.startsWith('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message}
        </div>
      )}

      {Object.keys(demoData).length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">API Response:</h4>
          <pre className="text-sm text-gray-700 overflow-auto">
            {JSON.stringify(demoData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );

  const renderBills = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <DocumentTextIcon className="h-5 w-5 text-green-600 mr-2" />
          Bill Management
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Bill Operations</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppGetBills("education"),
                  'Search bills'
                )}
                disabled={loading}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Search Bills (education)'}
              </button>
              
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppGetBillDetail("201"),
                  'Get bill detail'
                )}
                disabled={loading}
                className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Get Bill Detail'}
              </button>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Bill Actions</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppSupportBill("201", { support: true }),
                  'Support bill'
                )}
                disabled={loading}
                className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Support Bill'}
              </button>
              
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppBookmarkBill("201"),
                  'Bookmark bill'
                )}
                disabled={loading}
                className="w-full bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Bookmark Bill'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-md ${
          message.startsWith('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message}
        </div>
      )}

      {Object.keys(demoData).length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">API Response:</h4>
          <pre className="text-sm text-gray-700 overflow-auto">
            {JSON.stringify(demoData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );

  const renderIssues = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <ExclamationTriangleIcon className="h-5 w-5 text-orange-600 mr-2" />
          Issue Management
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Issue Operations</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppCreateIssue(demoIssue),
                  'Create issue'
                )}
                disabled={loading}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Issue'}
              </button>
              
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppSupportIssue("301", { support: true }),
                  'Support issue'
                )}
                disabled={loading}
                className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Support Issue'}
              </button>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Issue Actions</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppBookmarkIssue("301"),
                  'Bookmark issue'
                )}
                disabled={loading}
                className="w-full bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Bookmark Issue'}
              </button>
              
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppRequestIssueDeletion("301", { reason: "Demo deletion" }),
                  'Request issue deletion'
                )}
                disabled={loading}
                className="w-full bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Request Deletion'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-md ${
          message.startsWith('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message}
        </div>
      )}

      {Object.keys(demoData).length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">API Response:</h4>
          <pre className="text-sm text-gray-700 overflow-auto">
            {JSON.stringify(demoData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );

  const renderRepresentatives = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <MapPinIcon className="h-5 w-5 text-indigo-600 mr-2" />
          Representative Lookup
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Find Representatives</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppFindRepresentative("A1B2C3"),
                  'Find representative by postal code'
                )}
                disabled={loading}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Find by Postal Code'}
              </button>
              
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppSearchRepresentatives("smith"),
                  'Search representatives by name'
                )}
                disabled={loading}
                className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Search by Name'}
              </button>
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-medium text-gray-900 mb-2">Demo Postal Code</h4>
            <p className="text-sm text-gray-600">A1B2C3</p>
            <p className="text-xs text-gray-500 mt-1">
              This demo postal code will return mock representative data
            </p>
          </div>
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-md ${
          message.startsWith('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message}
        </div>
      )}

      {Object.keys(demoData).length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">API Response:</h4>
          <pre className="text-sm text-gray-700 overflow-auto">
            {JSON.stringify(demoData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );

  const renderChat = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <ChatBubbleLeftRightIcon className="h-5 w-5 text-purple-600 mr-2" />
          AI-Powered Chat
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Chat Operations</h4>
            <div className="space-y-3">
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppGetBillForChat("201"),
                  'Get bill for chat'
                )}
                disabled={loading}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Get Bill for Chat'}
              </button>
              
              <button
                onClick={() => handleApiCall(
                  () => api.mobileAppBillChat({ bill_id: 201, message: "What are the main criticisms of this bill?" }),
                  'Chat with AI about bill'
                )}
                disabled={loading}
                className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Ask AI About Bill'}
              </button>
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-medium text-gray-900 mb-2">Demo Chat Message</h4>
            <p className="text-sm text-gray-600">"What are the main criticisms of this bill?"</p>
            <p className="text-xs text-gray-500 mt-1">
              This will trigger an AI response about the Education Reform Act
            </p>
          </div>
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-md ${
          message.startsWith('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message}
        </div>
      )}

      {Object.keys(demoData).length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">API Response:</h4>
          <pre className="text-sm text-gray-700 overflow-auto">
            {JSON.stringify(demoData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );

  return (
    <div>
      {/* Tab Navigation */}
      <div className="mb-6">
        <div className="sm:hidden">
          <label htmlFor="tabs" className="sr-only">Select a tab</label>
          <select
            id="tabs"
            name="tabs"
            className="block w-full rounded-md border-gray-300 focus:border-op-blue focus:ring-op-blue"
            value={activeTab}
            onChange={(e) => setActiveTab(e.target.value as any)}
          >
            <option value="overview">Overview</option>
            <option value="user">User Management</option>
            <option value="bills">Bills</option>
            <option value="issues">Issues</option>
            <option value="representatives">Representatives</option>
            <option value="chat">AI Chat</option>
          </select>
        </div>
        <div className="hidden sm:block">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            {[
              { id: 'overview', label: 'Overview', icon: GlobeAltIcon },
              { id: 'user', label: 'User Management', icon: UserIcon },
              { id: 'bills', label: 'Bills', icon: DocumentTextIcon },
              { id: 'issues', label: 'Issues', icon: ExclamationTriangleIcon },
              { id: 'representatives', label: 'Representatives', icon: MapPinIcon },
              { id: 'chat', label: 'AI Chat', icon: ChatBubbleLeftRightIcon },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`${
                  activeTab === tab.id
                    ? 'border-op-blue text-op-blue'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium flex items-center`}
              >
                <tab.icon className="-ml-0.5 mr-2 h-5 w-5" aria-hidden="true" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && renderOverview()}
      {activeTab === 'user' && renderUserManagement()}
      {activeTab === 'bills' && renderBills()}
      {activeTab === 'issues' && renderIssues()}
      {activeTab === 'representatives' && renderRepresentatives()}
      {activeTab === 'chat' && renderChat()}
    </div>
  );
}
