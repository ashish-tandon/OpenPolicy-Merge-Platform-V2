'use client';
            
import { useState } from 'react';
import { 
  CalendarIcon, 
  MapPinIcon, 
  BuildingOfficeIcon,
  UserIcon,
  AcademicCapIcon,
  BriefcaseIcon,
  GlobeAltIcon,
  BookmarkIcon,
  ShareIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { MP } from '@/types/mps';
            
interface MPProfileProps {
  mp: MP;
}
            
export default function MPProfile({ mp }: MPProfileProps) {
  const [isSaved, setIsSaved] = useState(false);
            
  const handleSave = () => {
    setIsSaved(!isSaved);
    // TODO: Implement save functionality with User Service
    console.log('Save MP:', mp.id);
  };
            
  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: `${mp.full_name} - MP Profile`,
        text: `View the profile of ${mp.full_name}, MP for ${mp.constituency || 'Canada'}`,
        url: window.location.href,
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      // TODO: Show toast notification
    }
  };
            
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* MP Photo */}
        <div className="flex-shrink-0">
          {mp.photo_url ? (
            <img
              src={mp.photo_url}
              alt={mp.full_name}
              className="h-24 w-24 rounded-full object-cover"
            />
          ) : (
            <div className="h-24 w-24 rounded-full bg-gray-200 flex items-center justify-center">
              <UserIcon className="h-12 w-12 text-gray-400" />
            </div>
          )}
        </div>
            
        {/* MP Information */}
        <div className="flex-1 space-y-4">
          {/* Name and Basic Info */}
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{mp.full_name}</h1>
            <p className="text-lg text-gray-600">
              Member of Parliament for {mp.constituency || 'Canada'}
            </p>
          </div>
            
          {/* Key Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mp.party && (
              <div className="flex items-center space-x-2">
                <BuildingOfficeIcon className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">{mp.party}</span>
              </div>
            )}
            
            {mp.province && (
              <div className="flex items-center space-x-2">
                <MapPinIcon className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">{mp.province}</span>
              </div>
            )}
            
            {mp.first_elected && (
              <div className="flex items-center space-x-2">
                <CalendarIcon className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">
                  First elected: {format(new Date(mp.first_elected), 'MMM yyyy')}
                </span>
              </div>
            )}
            
            {mp.terms_served && (
              <div className="flex items-center space-x-2">
                <UserIcon className="h-5 w-5 text-gray-400" />
                <span className="text-gray-700">
                  {mp.terms_served} term{mp.terms_served > 1 ? 's' : ''} served
                </span>
              </div>
            )}
          </div>
            
          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              onClick={handleSave}
              className={`inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md shadow-sm ${
                isSaved
                  ? 'border-green-300 text-green-700 bg-green-50 hover:bg-green-100'
                  : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
              }`}
            >
              <BookmarkIcon className={`-ml-1 mr-2 h-4 w-4 ${
                isSaved ? 'text-green-600' : 'text-gray-400'
              }`} />
              {isSaved ? 'Saved' : 'Save'}
            </button>
            
            <button
              onClick={handleShare}
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
            >
              <ShareIcon className="-ml-1 mr-2 h-4 w-4 text-gray-400" />
              Share
            </button>
          </div>
        </div>
      </div>
            
      {/* Additional Information */}
      {(mp.bio || mp.education || mp.profession || mp.committees) && (
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Bio */}
            {mp.bio && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Biography</h3>
                <p className="text-gray-600">{mp.bio}</p>
              </div>
            )}
            
            {/* Education */}
            {mp.education && mp.education.length > 0 && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Education</h3>
                <div className="space-y-1">
                  {mp.education.map((edu, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <AcademicCapIcon className="h-4 w-4 text-gray-400" />
                      <span className="text-gray-600">{edu}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Profession */}
            {mp.profession && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Profession</h3>
                <div className="flex items-center space-x-2">
                  <BriefcaseIcon className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600">{mp.profession}</span>
                </div>
              </div>
            )}
            
            {/* Committees */}
            {mp.committees && mp.committees.length > 0 && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Committee Memberships</h3>
                <div className="space-y-1">
                  {mp.committees.map((committee, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <BuildingOfficeIcon className="h-4 w-4 text-gray-400" />
                      <span className="text-gray-600">{committee}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
            
      {/* Social Media Links */}
      {(mp.website || mp.twitter || mp.facebook || mp.instagram || mp.linkedin) && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Connect</h3>
          <div className="flex space-x-4">
            {mp.website && (
              <a
                href={mp.website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-op-blue hover:text-op-blue-700 transition-colors"
              >
                <GlobeAltIcon className="h-6 w-6" />
                <span className="sr-only">Website</span>
              </a>
            )}
            {mp.twitter && (
              <a
                href={`https://twitter.com/${mp.twitter}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-600 transition-colors"
              >
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
                <span className="sr-only">Twitter</span>
              </a>
            )}
            {mp.facebook && (
              <a
                href={`https://facebook.com/${mp.facebook}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 transition-colors"
              >
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
                <span className="sr-only">Facebook</span>
              </a>
            )}
            {mp.instagram && (
              <a
                href={`https://instagram.com/${mp.instagram}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-pink-500 hover:text-pink-600 transition-colors"
              >
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987 6.62 0 11.987-5.367 11.987-11.987C24.014 5.367 18.637.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.49-3.323-1.297C4.198 14.895 3.708 13.744 3.708 12.447s.49-2.448 1.418-3.323c.875-.807 2.026-1.297 3.323-1.297s2.448.49 3.323 1.297c.928.875 1.418 2.026 1.418 3.323s-.49 2.448-1.418 3.323c-.875.807-2.026 1.297-3.323 1.297zm7.718-1.297c-.875.807-2.026 1.297-3.323 1.297s-2.448-.49-3.323-1.297c-.928-.875-1.418-2.026-1.418-3.323s.49-2.448 1.418-3.323c.875-.807 2.026-1.297 3.323-1.297s2.448.49 3.323 1.297c.928.875 1.418 2.026 1.418 3.323s-.49 2.448-1.418 3.323z"/>
                </svg>
                <span className="sr-only">Instagram</span>
              </a>
            )}
            {mp.linkedin && (
              <a
                href={`https://linkedin.com/in/${mp.linkedin}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-700 hover:text-blue-900 transition-colors"
              >
                <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
                <span className="sr-only">LinkedIn</span>
              </a>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
