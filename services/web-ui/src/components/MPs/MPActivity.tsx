'use client';
            
import { 
  ClockIcon, 
  DocumentTextIcon, 
  UserIcon, 
  FlagIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  CalendarIcon,
  MapPinIcon,
  TagIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { MPActivity } from '@/types/mps';
            
interface MPActivityProps {
  activity: MPActivity[];
}
            
export default function MPActivity({ activity }: MPActivityProps) {
  if (!activity || activity.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
        <ClockIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Activity Available</h3>
        <p className="text-gray-600">
          Activity timeline for this MP is not available yet.
        </p>
      </div>
    );
  }
            
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'speech':
        return <DocumentTextIcon className="h-5 w-5 text-blue-600" />;
      case 'question':
        return <UserIcon className="h-5 w-5 text-green-600" />;
      case 'motion':
        return <FlagIcon className="h-5 w-5 text-purple-600" />;
      case 'amendment':
        return <DocumentTextIcon className="h-5 w-5 text-orange-600" />;
      case 'committee_work':
        return <BuildingOfficeIcon className="h-5 w-5 text-indigo-600" />;
      case 'constituency_work':
        return <MapPinIcon className="h-5 w-5 text-red-600" />;
      case 'media_appearance':
        return <InformationCircleIcon className="h-5 w-5 text-yellow-600" />;
      case 'parliamentary_event':
        return <CheckCircleIcon className="h-5 w-5 text-teal-600" />;
      default:
        return <InformationCircleIcon className="h-5 w-5 text-gray-600" />;
    }
  };
            
  const getActivityColor = (type: string) => {
    switch (type) {
      case 'speech':
        return 'bg-blue-100 text-blue-800';
      case 'question':
        return 'bg-green-100 text-green-800';
      case 'motion':
        return 'bg-purple-100 text-purple-800';
      case 'amendment':
        return 'bg-orange-100 text-orange-800';
      case 'committee_work':
        return 'bg-indigo-100 text-indigo-800';
      case 'constituency_work':
        return 'bg-red-100 text-red-800';
      case 'media_appearance':
        return 'bg-yellow-100 text-yellow-800';
      case 'parliamentary_event':
        return 'bg-teal-100 text-teal-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
            
  const formatActivityType = (type: string) => {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };
            
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Activity Summary */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Activity Summary</h3>
        <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {activity.filter(a => a.type === 'speech').length}
            </div>
            <div className="text-sm text-gray-500">Speeches</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {activity.filter(a => a.type === 'question').length}
            </div>
            <div className="text-sm text-gray-500">Questions</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">
              {activity.filter(a => a.type === 'motion').length}
            </div>
            <div className="text-sm text-gray-500">Motions</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {activity.filter(a => a.type === 'amendment').length}
            </div>
            <div className="text-sm text-gray-500">Amendments</div>
          </div>
        </div>
      </div>
            
      {/* Activity Timeline */}
      <div className="px-6 py-4">
        <div className="flow-root">
          <ul className="-mb-8">
            {activity.map((item, index) => (
              <li key={item.id}>
                <div className="relative pb-8">
                  {index !== activity.length - 1 && (
                    <span
                      className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                      aria-hidden="true"
                    />
                  )}
                  <div className="relative flex space-x-3">
                    <div>
                      <span className="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white bg-white">
                        {getActivityIcon(item.type)}
                      </span>
                    </div>
                    <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                      <div>
                        <div className="flex items-center space-x-2">
                          <p className="text-sm font-medium text-gray-900">
                            {item.title}
                          </p>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getActivityColor(item.type)}`}>
                            {formatActivityType(item.type)}
                          </span>
                        </div>
                        
                        {item.description && (
                          <p className="text-sm text-gray-600 mt-1">{item.description}</p>
                        )}
                        
                        <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                          <div className="flex items-center space-x-1">
                            <CalendarIcon className="h-4 w-4" />
                            <span>{format(new Date(item.date), 'MMM dd, yyyy')}</span>
                          </div>
                          
                          {item.location && (
                            <div className="flex items-center space-x-1">
                              <MapPinIcon className="h-4 w-4" />
                              <span>{item.location}</span>
                            </div>
                          )}
                        </div>
                        
                        {/* Related Items */}
                        {(item.related_bill || item.related_committee || item.related_debate) && (
                          <div className="mt-2 flex flex-wrap gap-2">
                            {item.related_bill && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                Bill: {item.related_bill}
                              </span>
                            )}
                            {item.related_committee && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                Committee: {item.related_committee}
                              </span>
                            )}
                            {item.related_debate && (
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                                Debate: {item.related_debate}
                              </span>
                            )}
                          </div>
                        )}
                        
                        {/* Tags */}
                        {item.tags && item.tags.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-1">
                            {item.tags.map((tag, tagIndex) => (
                              <span
                                key={tagIndex}
                                className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                              >
                                <TagIcon className="h-3 w-3 mr-1" />
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
