import { useState, useEffect } from 'react';
import { 
  BellIcon, EnvelopeIcon, ChatBubbleLeftRightIcon, DevicePhoneMobileIcon,
  CogIcon, PlusIcon, PencilIcon, CheckIcon, XMarkIcon,
  PlayIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

interface NotificationService {
  id: string;
  name: string;
  type: 'email' | 'sms' | 'slack' | 'discord' | 'telegram' | 'whatsapp' | 'push' | 'custom';
  status: 'active' | 'inactive' | 'error';
  config: Record<string, any>;
  lastTest: string | null;
  testResult: boolean | null;
}

interface NotificationTemplate {
  id: string;
  name: string;
  type: 'otp' | 'welcome' | 'parliamentary_alert' | 'bill_update' | 'vote_reminder' | 'custom';
  subject: string;
  body: string;
  channels: string[];
  isActive: boolean;
}

export default function NotificationSetup() {
  const [activeTab, setActiveTab] = useState<'services' | 'templates' | 'settings' | 'testing'>('services');
  const [services, setServices] = useState<NotificationService[]>([]);
  const [templates, setTemplates] = useState<NotificationTemplate[]>([]);
  // These will be implemented in future iterations
  // const [showAddService, setShowAddService] = useState(false);
  // const [showAddTemplate, setShowAddTemplate] = useState(false);
  // const [editingService, setEditingService] = useState<NotificationService | null>(null);
  // const [editingTemplate, setEditingTemplate] = useState<NotificationTemplate | null>(null);

  // Mock data for demonstration
  useEffect(() => {
    setServices([
      {
        id: '1',
        name: 'Resend.com Email',
        type: 'email',
        status: 'active',
        config: { apiKey: 're_123...', fromEmail: 'noreply@openpolicy.me' },
        lastTest: '2024-01-15T10:30:00Z',
        testResult: true
      },
      {
        id: '2',
        name: 'Slack Team Alerts',
        type: 'slack',
        status: 'active',
        config: { webhookUrl: 'https://hooks.slack.com/...', channel: '#alerts' },
        lastTest: '2024-01-15T09:15:00Z',
        testResult: true
      },
      {
        id: '3',
        name: 'Twilio SMS',
        type: 'sms',
        status: 'inactive',
        config: { accountSid: 'AC123...', authToken: '***', fromNumber: '+1234567890' },
        lastTest: null,
        testResult: null
      },
      {
        id: '4',
        name: 'Discord Community',
        type: 'discord',
        status: 'active',
        config: { webhookUrl: 'https://discord.com/api/webhooks/...', username: 'OpenPolicy Bot' },
        lastTest: '2024-01-14T16:45:00Z',
        testResult: true
      }
    ]);

    setTemplates([
      {
        id: '1',
        name: 'OTP Verification',
        type: 'otp',
        subject: 'Your OpenPolicy Verification Code',
        body: 'Hello {{user_name}},\n\nYour verification code is: {{otp_code}}\n\nThis code will expire in 10 minutes.',
        channels: ['email', 'sms'],
        isActive: true
      },
      {
        id: '2',
        name: 'Welcome Message',
        type: 'welcome',
        subject: 'Welcome to OpenPolicy!',
        body: '🎉 Welcome to OpenPolicy, {{user_name}}!\n\nYour account has been created successfully.',
        channels: ['email', 'slack'],
        isActive: true
      },
      {
        id: '3',
        name: 'Parliamentary Alert',
        type: 'parliamentary_alert',
        subject: 'Parliamentary Alert: {{alert_type}}',
        body: '🏛️ New parliamentary activity:\n\n📋 {{description}}\n📜 Bill: {{bill_title}}\n👤 Politician: {{politician_name}}',
        channels: ['email', 'slack', 'discord'],
        isActive: true
      }
    ]);
  }, []);

  const handleTestService = async (serviceId: string) => {
    const service = services.find(s => s.id === serviceId);
    if (!service) return;

    toast.loading(`Testing ${service.name}...`);
    
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const success = Math.random() > 0.2; // 80% success rate for demo
      
      setServices(prev => prev.map(s => 
        s.id === serviceId 
          ? { ...s, lastTest: new Date().toISOString(), testResult: success }
          : s
      ));

      if (success) {
        toast.success(`${service.name} test successful!`);
      } else {
        toast.error(`${service.name} test failed!`);
      }
    } catch (error) {
      toast.error(`Test failed: ${error}`);
    }
  };

  const handleToggleService = (serviceId: string) => {
    setServices(prev => prev.map(s => 
      s.id === serviceId 
        ? { ...s, status: s.status === 'active' ? 'inactive' : 'active' }
        : s
    ));
    toast.success('Service status updated!');
  };

  const getServiceIcon = (type: string) => {
    switch (type) {
      case 'email': return <EnvelopeIcon className="h-6 w-6 text-blue-500" />;
      case 'sms': return <DevicePhoneMobileIcon className="h-6 w-6 text-green-500" />;
      case 'slack': return <ChatBubbleLeftRightIcon className="h-6 w-6 text-purple-500" />;
      case 'discord': return <ChatBubbleLeftRightIcon className="h-6 w-6 text-indigo-500" />;
      case 'telegram': return <ChatBubbleLeftRightIcon className="h-6 w-6 text-blue-400" />;
      case 'whatsapp': return <DevicePhoneMobileIcon className="h-6 w-6 text-green-400" />;
      case 'push': return <BellIcon className="h-6 w-6 text-orange-500" />;
      default: return <CogIcon className="h-6 w-6 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'inactive': return 'text-gray-600 bg-gray-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="lg:pl-64">
      <div className="px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Notification Setup</h1>
          <p className="mt-2 text-gray-600">
            Configure and manage all notification services for OpenPolicy
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'services', name: 'Services', icon: CogIcon },
              { id: 'templates', name: 'Templates', icon: BellIcon },
              { id: 'settings', name: 'Settings', icon: CogIcon },
              { id: 'testing', name: 'Testing', icon: PlayIcon }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === tab.id
                    ? 'text-op-blue bg-op-blue-50 border-b-2 border-op-blue'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Services Tab */}
        {activeTab === 'services' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-900">Notification Services</h2>
              <button
                onClick={() => alert('Add Service functionality coming soon!')}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-op-blue hover:bg-op-blue-700"
              >
                <PlusIcon className="h-4 w-4 mr-2" />
                Add Service
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services.map((service) => (
                <div key={service.id} className="bg-white rounded-lg shadow p-6 border border-gray-200">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      {getServiceIcon(service.type)}
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">{service.name}</h3>
                        <p className="text-sm text-gray-500 capitalize">{service.type}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                                              <button
                          onClick={() => alert('Edit Service functionality coming soon!')}
                          className="p-1 text-gray-400 hover:text-gray-600"
                          title="Edit"
                        >
                          <PencilIcon className="h-4 w-4" />
                        </button>
                      <button
                        onClick={() => handleToggleService(service.id)}
                        className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(service.status)}`}
                      >
                        {service.status}
                      </button>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="text-sm">
                      <span className="font-medium text-gray-700">Status:</span>
                      <span className={`ml-2 px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(service.status)}`}>
                        {service.status}
                      </span>
                    </div>

                    {service.lastTest && (
                      <div className="text-sm">
                        <span className="font-medium text-gray-700">Last Test:</span>
                        <span className="ml-2 text-gray-600">
                          {new Date(service.lastTest).toLocaleString()}
                        </span>
                      </div>
                    )}

                    {service.testResult !== null && (
                      <div className="text-sm">
                        <span className="font-medium text-gray-700">Test Result:</span>
                        <span className={`ml-2 ${service.testResult ? 'text-green-600' : 'text-red-600'}`}>
                          {service.testResult ? '✅ Success' : '❌ Failed'}
                        </span>
                      </div>
                    )}

                    <div className="flex space-x-2 pt-2">
                      <button
                        onClick={() => handleTestService(service.id)}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                      >
                        <PlayIcon className="h-4 w-4 mr-2" />
                        Test
                      </button>
                                              <button
                          onClick={() => alert('Edit Service functionality coming soon!')}
                          className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                        >
                          <PencilIcon className="h-4 w-4 mr-2" />
                          Edit
                        </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Templates Tab */}
        {activeTab === 'templates' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-900">Notification Templates</h2>
              <button
                onClick={() => alert('Add Template functionality coming soon!')}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-op-blue hover:bg-op-blue-700"
              >
                <PlusIcon className="h-4 w-4 mr-2" />
                Add Template
              </button>
            </div>

            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Available Templates</h3>
              </div>
              <div className="divide-y divide-gray-200">
                {templates.map((template) => (
                  <div key={template.id} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <h4 className="text-lg font-medium text-gray-900">{template.name}</h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                            template.isActive ? 'text-green-600 bg-green-100' : 'text-gray-600 bg-gray-100'
                          }`}>
                            {template.isActive ? 'Active' : 'Inactive'}
                          </span>
                        </div>
                        <p className="mt-1 text-sm text-gray-500">Type: {template.type.replace('_', ' ')}</p>
                        <p className="mt-2 text-sm text-gray-700">{template.subject}</p>
                        <div className="mt-2 flex flex-wrap gap-2">
                          {template.channels.map((channel) => (
                            <span key={channel} className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                              {channel}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => alert('Edit Template functionality coming soon!')}
                          className="p-2 text-gray-400 hover:text-gray-600"
                          title="Edit"
                        >
                          <PencilIcon className="h-5 w-5" />
                        </button>
                        <button
                          onClick={() => {
                            setTemplates(prev => prev.map(t => 
                              t.id === template.id ? { ...t, isActive: !t.isActive } : t
                            ));
                            toast.success(`Template ${template.isActive ? 'deactivated' : 'activated'}!`);
                          }}
                          className={`p-2 ${template.isActive ? 'text-green-600' : 'text-gray-400'} hover:text-green-700`}
                          title={template.isActive ? 'Deactivate' : 'Activate'}
                        >
                          {template.isActive ? <CheckIcon className="h-5 w-5" /> : <XMarkIcon className="h-5 w-5" />}
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900">Notification Settings</h2>
            
            <div className="bg-white shadow rounded-lg p-6">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Global Settings</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Default Notification Channels
                      </label>
                      <div className="space-y-2">
                        {['email', 'sms', 'slack', 'discord', 'telegram', 'push'].map((channel) => (
                          <label key={channel} className="flex items-center">
                            <input
                              type="checkbox"
                              defaultChecked={['email', 'slack'].includes(channel)}
                              className="rounded border-gray-300 text-op-blue focus:ring-op-blue"
                            />
                            <span className="ml-2 text-sm text-gray-700 capitalize">{channel}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Rate Limiting
                      </label>
                      <div className="space-y-3">
                        <div>
                          <label className="block text-xs text-gray-600 mb-1">Max notifications per minute</label>
                          <input
                            type="number"
                            defaultValue={100}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-600 mb-1">Max notifications per hour</label>
                          <input
                            type="number"
                            defaultValue={1000}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pt-6 border-t border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Security Settings</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          defaultChecked
                          className="rounded border-gray-300 text-op-blue focus:ring-op-blue"
                        />
                        <span className="ml-2 text-sm text-gray-700">Require authentication for API access</span>
                      </label>
                    </div>
                    <div>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          defaultChecked
                          className="rounded border-gray-300 text-op-blue focus:ring-op-blue"
                        />
                        <span className="ml-2 text-sm text-gray-700">Log all notification attempts</span>
                      </label>
                    </div>
                    <div>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          defaultChecked
                          className="rounded border-gray-300 text-op-blue focus:ring-op-blue"
                        />
                        <span className="ml-2 text-sm text-gray-700">Enable notification encryption</span>
                      </label>
                    </div>
                  </div>
                </div>

                <div className="pt-6 border-t border-gray-200">
                  <button className="w-full px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-op-blue hover:bg-op-blue-700">
                    Save Settings
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Testing Tab */}
        {activeTab === 'testing' && (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900">Notification Testing</h2>
            
            <div className="bg-white shadow rounded-lg p-6">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Test Notifications</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Test Type
                      </label>
                      <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue">
                        <option>OTP Verification</option>
                        <option>Welcome Message</option>
                        <option>Parliamentary Alert</option>
                        <option>Bill Update</option>
                        <option>Custom Message</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Target Channel
                      </label>
                      <select className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue">
                        <option>All Channels</option>
                        <option>Email Only</option>
                        <option>Slack Only</option>
                        <option>Discord Only</option>
                        <option>SMS Only</option>
                      </select>
                    </div>
                  </div>
                  
                  <div className="mt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Test Recipient
                    </label>
                    <input
                      type="text"
                      placeholder="email@example.com or phone number"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue"
                    />
                  </div>
                  
                  <div className="mt-6">
                    <button className="w-full px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700">
                      Send Test Notification
                    </button>
                  </div>
                </div>

                <div className="pt-6 border-t border-gray-200">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Test Results</h3>
                  <div className="space-y-3">
                    {services.filter(s => s.lastTest).map((service) => (
                      <div key={service.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          {getServiceIcon(service.type)}
                          <div>
                            <p className="text-sm font-medium text-gray-900">{service.name}</p>
                            <p className="text-xs text-gray-500">
                              {new Date(service.lastTest!).toLocaleString()}
                            </p>
                          </div>
                        </div>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          service.testResult ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'
                        }`}>
                          {service.testResult ? 'Success' : 'Failed'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
