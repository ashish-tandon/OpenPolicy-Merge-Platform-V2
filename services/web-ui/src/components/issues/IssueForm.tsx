'use client';

import { useState } from 'react';
import { 
  ExclamationTriangleIcon,
  DocumentTextIcon,
  TagIcon,
  FlagIcon,
  UserIcon,
  MapPinIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';

interface IssueFormProps {
  userId?: string;
  onIssueCreated?: (issue: any) => void;
  onCancel?: () => void;
}

interface IssueFormData {
  name: string;
  summary: string;
  description: string;
  category: string;
  priority: string;
  constituency?: string;
  postal_code?: string;
  contact_email?: string;
  tags: string[];
}

const CATEGORIES = [
  'environmental',
  'economic',
  'social',
  'infrastructure',
  'healthcare',
  'education',
  'security',
  'transportation',
  'housing',
  'other'
];

const PRIORITIES = [
  { value: 'low', label: 'Low', color: 'text-green-600' },
  { value: 'medium', label: 'Medium', color: 'text-yellow-600' },
  { value: 'high', label: 'High', color: 'text-red-600' }
];

const SUGGESTED_TAGS = [
  'community', 'policy', 'government', 'public', 'local', 'national',
  'environment', 'economy', 'health', 'education', 'safety', 'equity'
];

export default function IssueForm({ userId, onIssueCreated, onCancel }: IssueFormProps) {
  const [formData, setFormData] = useState<IssueFormData>({
    name: '',
    summary: '',
    description: '',
    category: 'general',
    priority: 'medium',
    constituency: '',
    postal_code: '',
    contact_email: '',
    tags: []
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showAdvanced, setShowAdvanced] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Issue name is required';
    } else if (formData.name.trim().length < 3) {
      newErrors.name = 'Issue name must be at least 3 characters';
    }

    if (!formData.summary.trim()) {
      newErrors.summary = 'Issue summary is required';
    } else if (formData.summary.trim().length < 10) {
      newErrors.summary = 'Issue summary must be at least 10 characters';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Issue description is required';
    } else if (formData.description.trim().length < 20) {
      newErrors.description = 'Issue description must be at least 20 characters';
    }

    if (formData.contact_email && !isValidEmail(formData.contact_email)) {
      newErrors.contact_email = 'Please enter a valid email address';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isValidEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const issueData = {
        ...formData,
        user_id: userId || 'demo-user',
        source: 'web',
        user_agent: navigator.userAgent,
        location: 'web'
      };

      const response = await api.createIssue(issueData);

      if (response.success) {
        // Reset form
        setFormData({
          name: '',
          summary: '',
          description: '',
          category: 'general',
          priority: 'medium',
          constituency: '',
          postal_code: '',
          contact_email: '',
          tags: []
        });
        setErrors({});
        setShowAdvanced(false);

        // Notify parent component
        if (onIssueCreated) {
          onIssueCreated(response.issue);
        }
      } else {
        throw new Error(response.message || 'Failed to create issue');
      }
    } catch (error) {
      console.error('Error creating issue:', error);
      setErrors({ submit: 'Failed to create issue. Please try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field: keyof IssueFormData, value: string | string[]) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const toggleTag = (tag: string) => {
    const newTags = formData.tags.includes(tag)
      ? formData.tags.filter(t => t !== tag)
      : [...formData.tags, tag];
    handleInputChange('tags', newTags);
  };

  const getPriorityColor = (priority: string) => {
    const priorityObj = PRIORITIES.find(p => p.value === priority);
    return priorityObj?.color || 'text-gray-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Report a Community Issue</h2>
        <p className="text-gray-600">
          Help improve your community by reporting issues that need government attention. 
          Your issue will be reviewed and may be shared with relevant authorities.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900 flex items-center">
            <DocumentTextIcon className="h-5 w-5 mr-2" />
            Basic Information
          </h3>

          {/* Issue Name */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Issue Name *
            </label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue ${
                errors.name ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="Brief, descriptive name for the issue"
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name}</p>
            )}
          </div>

          {/* Issue Summary */}
          <div>
            <label htmlFor="summary" className="block text-sm font-medium text-gray-700 mb-2">
              Issue Summary *
            </label>
            <textarea
              id="summary"
              value={formData.summary}
              onChange={(e) => handleInputChange('summary', e.target.value)}
              rows={3}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue ${
                errors.summary ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="Brief summary of the issue (at least 10 characters)"
            />
            {errors.summary && (
              <p className="mt-1 text-sm text-red-600">{errors.summary}</p>
            )}
          </div>

          {/* Issue Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Detailed Description *
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              rows={5}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue ${
                errors.description ? 'border-red-300' : 'border-gray-300'
              }`}
              placeholder="Provide detailed information about the issue, its impact, and any relevant context (at least 20 characters)"
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-600">{errors.description}</p>
            )}
          </div>

          {/* Category and Priority */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                Category
              </label>
              <select
                id="category"
                value={formData.category}
                onChange={(e) => handleInputChange('category', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
              >
                {CATEGORIES.map(category => (
                  <option key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                Priority
              </label>
              <select
                id="priority"
                value={formData.priority}
                onChange={(e) => handleInputChange('priority', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
              >
                {PRIORITIES.map(priority => (
                  <option key={priority.value} value={priority.value}>
                    {priority.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tags
            </label>
            <div className="flex flex-wrap gap-2">
              {SUGGESTED_TAGS.map(tag => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleTag(tag)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    formData.tags.includes(tag)
                      ? 'bg-op-blue text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <TagIcon className="h-3 w-3 inline mr-1" />
                  {tag}
                </button>
              ))}
            </div>
            {formData.tags.length > 0 && (
              <p className="mt-2 text-sm text-gray-500">
                Selected: {formData.tags.join(', ')}
              </p>
            )}
          </div>
        </div>

        {/* Advanced Options Toggle */}
        <div className="border-t border-gray-200 pt-4">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center text-sm text-op-blue hover:text-op-blue-700 transition-colors"
          >
            <FlagIcon className="h-4 w-4 mr-2" />
            {showAdvanced ? 'Hide' : 'Show'} Advanced Options
          </button>
        </div>

        {/* Advanced Options */}
        {showAdvanced && (
          <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
            <h4 className="text-md font-medium text-gray-900">Additional Information</h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Constituency */}
              <div>
                <label htmlFor="constituency" className="block text-sm font-medium text-gray-700 mb-2">
                  Constituency
                </label>
                <input
                  type="text"
                  id="constituency"
                  value={formData.constituency}
                  onChange={(e) => handleInputChange('constituency', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
                  placeholder="Your constituency (optional)"
                />
              </div>

              {/* Postal Code */}
              <div>
                <label htmlFor="postal_code" className="block text-sm font-medium text-gray-700 mb-2">
                  Postal Code
                </label>
                <input
                  type="text"
                  id="postal_code"
                  value={formData.postal_code}
                  onChange={(e) => handleInputChange('postal_code', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
                  placeholder="Your postal code (optional)"
                />
              </div>
            </div>

            {/* Contact Email */}
            <div>
              <label htmlFor="contact_email" className="block text-sm font-medium text-gray-700 mb-2">
                Contact Email
              </label>
              <input
                type="email"
                id="contact_email"
                value={formData.contact_email}
                onChange={(e) => handleInputChange('contact_email', e.target.value)}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue ${
                  errors.contact_email ? 'border-red-300' : 'border-gray-300'
                }`}
                placeholder="Your email for updates (optional)"
              />
              {errors.contact_email && (
                <p className="mt-1 text-sm text-red-600">{errors.contact_email}</p>
              )}
            </div>
          </div>
        )}

        {/* Submit Error */}
        {errors.submit && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-400 mr-2" />
              <p className="text-sm text-red-600">{errors.submit}</p>
            </div>
          </div>
        )}

        {/* Form Actions */}
        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Cancel
            </button>
          )}
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2 bg-op-blue text-white rounded-md hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isSubmitting ? 'Creating Issue...' : 'Submit Issue'}
          </button>
        </div>
      </form>

      {/* Information Note */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <div className="flex items-start">
          <UserIcon className="h-5 w-5 text-blue-600 mt-0.5 mr-2" />
          <div className="text-sm text-blue-800">
            <p className="font-medium">Your issue matters!</p>
            <p className="mt-1">
              Community issues help identify areas that need attention and can influence policy decisions. 
              All submissions are reviewed before being shared with the community.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
