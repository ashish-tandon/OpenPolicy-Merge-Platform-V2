'use client';

import Link from 'next/link';
import { Committee } from '@/lib/api';
import Pagination from '@/components/Pagination';

interface CommitteesListProps {
  committees: Committee[];
  totalCount: number;
  currentPage: number;
  filters: any;
}

export default function CommitteesList({ 
  committees, 
  totalCount, 
  currentPage, 
  filters 
}: CommitteesListProps) {
  const pageSize = 20;
  const totalPages = Math.ceil(totalCount / pageSize);

  // Mock additional data for committees
  const enrichedCommittees = committees.map(committee => ({
    ...committee,
    type: committee.name.includes('Special') ? 'special' : 'standing',
    activeStudies: Math.floor(Math.random() * 5) + 1,
    members: Math.floor(Math.random() * 6) + 10,
    lastMeeting: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
    chair: {
      name: 'John Doe',
      party: 'Liberal',
      mpSlug: 'john-doe',
    },
  }));

  const getCommitteeTypeColor = (type: string) => {
    switch (type) {
      case 'standing': return 'bg-blue-100 text-blue-800';
      case 'special': return 'bg-purple-100 text-purple-800';
      case 'joint': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (committees.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <p className="text-gray-500">No committees found matching your criteria.</p>
        <Link href="/committees" className="mt-4 inline-block text-op-blue hover:underline">
          Clear filters
        </Link>
      </div>
    );
  }

  return (
    <div>
      {/* Results count */}
      <div className="mb-4 flex justify-between items-center">
        <span className="text-sm text-gray-600">
          Showing {((currentPage - 1) * pageSize) + 1} - {Math.min(currentPage * pageSize, totalCount)} of {totalCount} committees
        </span>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">Sort by:</span>
          <select className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-op-blue">
            <option value="name">Name</option>
            <option value="activity">Most Active</option>
            <option value="recent">Recently Met</option>
          </select>
        </div>
      </div>

      {/* Committees Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {enrichedCommittees.map((committee) => (
          <Link
            key={committee.id}
            href={`/committees/${committee.slug}`}
            className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
          >
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-lg font-medium text-op-blue hover:underline flex-1 pr-2">
                {committee.name}
              </h3>
              <span className={`text-xs px-2 py-1 rounded flex-shrink-0 ${getCommitteeTypeColor(committee.type)}`}>
                {committee.type}
              </span>
            </div>

            {committee.short_name && committee.short_name !== committee.name && (
              <p className="text-sm text-gray-600 mb-3">({committee.short_name})</p>
            )}

            {/* Committee Stats */}
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <div className="text-xl font-bold text-gray-700">{committee.members}</div>
                <div className="text-xs text-gray-500">Members</div>
              </div>
              <div className="text-center">
                <div className="text-xl font-bold text-gray-700">{committee.activeStudies}</div>
                <div className="text-xs text-gray-500">Active Studies</div>
              </div>
              <div className="text-center">
                <div className="text-xl font-bold text-gray-700">
                  {new Date(committee.lastMeeting).toLocaleDateString('en-CA', { 
                    month: 'short', 
                    day: 'numeric' 
                  })}
                </div>
                <div className="text-xs text-gray-500">Last Met</div>
              </div>
            </div>

            {/* Current Chair */}
            {committee.chair && (
              <div className="pt-3 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  Chair: <span className="font-medium text-gray-700">{committee.chair.name}</span> ({committee.chair.party})
                </p>
              </div>
            )}

            {/* Active Studies Preview */}
            {committee.activeStudies > 0 && (
              <div className="mt-3 text-sm text-gray-600">
                <span className="font-medium">Current focus:</span> Climate policy, Healthcare funding
              </div>
            )}
          </Link>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-8">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            baseUrl="/committees"
            queryParams={filters}
          />
        </div>
      )}

      {/* Committee Information */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-blue-50 rounded-lg p-4">
          <h3 className="font-medium text-blue-900 mb-2">Standing Committees</h3>
          <p className="text-sm text-blue-800">
            Permanent committees established by Standing Orders with ongoing mandates in specific areas.
          </p>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <h3 className="font-medium text-purple-900 mb-2">Special Committees</h3>
          <p className="text-sm text-purple-800">
            Temporary committees created to study specific issues with defined timelines.
          </p>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <h3 className="font-medium text-green-900 mb-2">Joint Committees</h3>
          <p className="text-sm text-green-800">
            Committees with members from both the House of Commons and the Senate.
          </p>
        </div>
      </div>
    </div>
  );
}
