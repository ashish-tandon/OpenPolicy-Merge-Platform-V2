'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Member } from '@/lib/api';
import Pagination from '@/components/Pagination';

interface MPListProps {
  members: Member[];
  totalCount: number;
  currentPage: number;
  filters: any;
}

export default function MPList({ members, totalCount, currentPage, filters }: MPListProps) {
  const pageSize = 20;
  const totalPages = Math.ceil(totalCount / pageSize);

  // Group MPs by province if no specific filters
  const groupByProvince = !filters.search && !filters.party && filters.current;

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

  const groupedMembers = groupByProvince
    ? members.reduce((acc, member) => {
        const province = member.riding?.province || 'Unknown';
        if (!acc[province]) acc[province] = [];
        acc[province].push(member);
        return acc;
      }, {} as { [key: string]: Member[] })
    : null;

  const getPartyColor = (partySlug?: string) => {
    switch (partySlug) {
      case 'liberal': return 'bg-red-600';
      case 'conservative': return 'bg-blue-600';
      case 'ndp': return 'bg-orange-600';
      case 'bloc': return 'bg-cyan-600';
      case 'green': return 'bg-green-600';
      default: return 'bg-gray-600';
    }
  };

  const MPCard = ({ member }: { member: Member }) => (
    <Link
      href={`/mps/${member.slug}`}
      className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-4"
    >
      <div className="flex items-start space-x-4">
        {/* MP Photo */}
        <div className="flex-shrink-0">
          {member.image ? (
            <Image
              src={member.image}
              alt={member.name}
              width={64}
              height={80}
              className="rounded-md object-cover"
            />
          ) : (
            <div className="w-16 h-20 bg-gray-200 rounded-md flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          )}
        </div>

        {/* MP Info */}
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-medium text-op-blue hover:underline truncate">
            {member.name}
          </h3>
          
          {member.party && (
            <div className="flex items-center mt-1">
              <span className={`w-3 h-3 rounded-full mr-2 ${getPartyColor(member.party.slug)}`}></span>
              <span className="text-sm text-gray-600">{member.party.short_name}</span>
            </div>
          )}
          
          {member.riding && (
            <p className="text-sm text-gray-600 mt-1">
              {member.riding.name}
              {member.riding.province && ` (${member.riding.province})`}
            </p>
          )}

          {!member.current_member && (
            <span className="inline-block mt-2 text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
              Former MP
            </span>
          )}
        </div>
      </div>
    </Link>
  );

  if (members.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500">No MPs found matching your criteria.</p>
        <Link href="/mps" className="mt-4 inline-block text-op-blue hover:underline">
          Clear filters
        </Link>
      </div>
    );
  }

  return (
    <div>
      {/* Results count */}
      <div className="mb-4 text-sm text-gray-600">
        Showing {((currentPage - 1) * pageSize) + 1} - {Math.min(currentPage * pageSize, totalCount)} of {totalCount} MPs
      </div>

      {/* MPs Grid or Grouped List */}
      {groupedMembers ? (
        <div className="space-y-8">
          {provinceOrder.map(province => {
            if (!groupedMembers[province]) return null;
            return (
              <div key={province}>
                <h2 className="text-xl font-bold text-op-dark mb-4">
                  {provinceNames[province]} ({groupedMembers[province].length})
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {groupedMembers[province].map(member => (
                    <MPCard key={member.id} member={member} />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {members.map(member => (
            <MPCard key={member.id} member={member} />
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-8">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            baseUrl="/mps"
            queryParams={filters}
          />
        </div>
      )}
    </div>
  );
}
