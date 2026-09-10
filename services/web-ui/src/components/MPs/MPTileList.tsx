'use client';

import Link from 'next/link';
import { Member } from '@/lib/api';
import Pagination from '@/components/Pagination';

interface MPTileListProps {
  members: Member[];
  pagination?: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
  filters: any;
}

export default function MPTileList({ members, pagination, filters }: MPTileListProps) {
  const provinceOrder = ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'NT', 'YT', 'NU'];
  const provinceNames: { [key: string]: string } = {
    'ON': 'Ontario',
    'QC': 'Quebec',
    'BC': 'British Columbia',
    'AB': 'Alberta',
    'MB': 'Manitoba',
    'SK': 'Saskatchewan',
    'NS': 'Nova Scotia',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'PE': 'Prince Edward Island',
    'NT': 'Northwest Territories',
    'YT': 'Yukon',
    'NU': 'Nunavut',
  };

  // Group MPs by province for the tile view
  const groupedMembers = members.reduce((acc, member) => {
    const province = member.riding?.province || 'Unknown';
    if (!acc[province]) acc[province] = [];
    acc[province].push(member);
    return acc;
  }, {} as { [key: string]: Member[] });

  // Sort members within each province alphabetically
  Object.keys(groupedMembers).forEach(province => {
    groupedMembers[province].sort((a, b) => a.name.localeCompare(b.name));
  });

  const getPartyColor = (partySlug?: string) => {
    switch (partySlug?.toLowerCase()) {
      case 'liberal': return 'text-red-600';
      case 'conservative': return 'text-blue-600';
      case 'ndp': return 'text-orange-600';
      case 'bloc': return 'text-cyan-600';
      case 'green': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-8">
      {provinceOrder.map(province => {
        if (!groupedMembers[province]) return null;
        
        return (
          <div key={province} className="bg-white rounded-lg shadow p-6">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Province Header */}
              <div className="lg:col-span-1">
                <h2 className="text-xl font-bold text-op-dark" id={province}>
                  {provinceNames[province]}
                </h2>
              </div>
              
              {/* MPs Grid */}
              <div className="lg:col-span-3">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                  {groupedMembers[province].map(member => (
                    <div key={member.id} className="text-sm">
                      <Link
                        href={`/mps/${member.slug}`}
                        className="hover:underline text-op-blue"
                        title={`${member.party?.short_name || 'Independent'} for ${member.riding?.name || 'Unknown riding'}`}
                      >
                        {member.name}
                      </Link>
                      {member.party && (
                        <span className={`ml-1 text-xs ${getPartyColor(member.party.slug)}`}>
                          ({member.party.short_name})
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );
      })}
      
      {/* Pagination if needed */}
      {pagination && pagination.totalPages > 1 && (
        <div className="mt-8">
          <Pagination
            currentPage={pagination.page}
            totalPages={pagination.totalPages}
            basePath="/mps"
          />
        </div>
      )}
    </div>
  );
}