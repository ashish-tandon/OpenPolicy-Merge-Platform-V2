'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface CommitteeMember {
  id: number;
  name: string;
  mpSlug: string;
  party: string;
  riding: string;
  role: 'Chair' | 'Vice-Chair' | 'Member';
  joinedDate: string;
  image?: string;
}

interface CommitteeMembersProps {
  committeeId: number;
}

export default function CommitteeMembers({ committeeId }: CommitteeMembersProps) {
  const [members, setMembers] = useState<CommitteeMember[]>([]);
  const [loading, setLoading] = useState(true);

  // In production, this would fetch actual member data from the API
  useEffect(() => {
    setTimeout(() => {
      setMembers([
        {
          id: 1,
          name: 'Hon. John Smith',
          mpSlug: 'john-smith',
          party: 'Liberal',
          riding: 'Toronto Centre',
          role: 'Chair',
          joinedDate: '2021-12-16',
        },
        {
          id: 2,
          name: 'Jane Doe',
          mpSlug: 'jane-doe',
          party: 'Conservative',
          riding: 'Calgary Centre',
          role: 'Vice-Chair',
          joinedDate: '2021-12-16',
        },
        {
          id: 3,
          name: 'Bob Wilson',
          mpSlug: 'bob-wilson',
          party: 'NDP',
          riding: 'Vancouver East',
          role: 'Vice-Chair',
          joinedDate: '2021-12-16',
        },
        {
          id: 4,
          name: 'Sarah Johnson',
          mpSlug: 'sarah-johnson',
          party: 'Liberal',
          riding: 'Ottawa Centre',
          role: 'Member',
          joinedDate: '2022-01-15',
        },
        {
          id: 5,
          name: 'Tom Brown',
          mpSlug: 'tom-brown',
          party: 'Conservative',
          riding: 'Edmonton Centre',
          role: 'Member',
          joinedDate: '2022-02-01',
        },
      ]);
      setLoading(false);
    }, 500);
  }, [committeeId]);

  const getPartyColor = (party: string) => {
    switch (party.toLowerCase()) {
      case 'liberal': return 'bg-red-600';
      case 'conservative': return 'bg-blue-600';
      case 'ndp': return 'bg-orange-600';
      case 'bloc': return 'bg-cyan-600';
      case 'green': return 'bg-green-600';
      default: return 'bg-gray-600';
    }
  };

  const getRoleBadge = (role: string) => {
    switch (role) {
      case 'Chair':
        return 'bg-purple-100 text-purple-800';
      case 'Vice-Chair':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="animate-pulse">
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  // Group members by party
  const membersByParty = members.reduce((acc, member) => {
    if (!acc[member.party]) acc[member.party] = [];
    acc[member.party].push(member);
    return acc;
  }, {} as Record<string, CommitteeMember[]>);

  return (
    <div>
      {/* Party Distribution */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-medium text-gray-700 mb-3">Party Representation</h3>
        <div className="flex items-center gap-4">
          {Object.entries(membersByParty).map(([party, partyMembers]) => (
            <div key={party} className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${getPartyColor(party)}`}></span>
              <span className="text-sm text-gray-600">
                {party}: {partyMembers.length}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Members List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {members.map((member) => (
          <div key={member.id} className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <Link
                  href={`/mps/${member.mpSlug}`}
                  className="font-medium text-op-blue hover:underline"
                >
                  {member.name}
                </Link>
                {member.role !== 'Member' && (
                  <span className={`ml-2 text-xs px-2 py-0.5 rounded ${getRoleBadge(member.role)}`}>
                    {member.role}
                  </span>
                )}
              </div>
              <span className={`w-3 h-3 rounded-full ${getPartyColor(member.party)}`}></span>
            </div>
            
            <p className="text-sm text-gray-600">
              {member.party} • {member.riding}
            </p>
            
            <p className="text-xs text-gray-500 mt-2">
              Member since {new Date(member.joinedDate).toLocaleDateString('en-CA', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </p>
          </div>
        ))}
      </div>

      {/* Membership Rules */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">Committee Membership</h4>
        <p className="text-sm text-blue-800">
          Committee members are appointed by their respective parties based on Standing Orders. 
          The committee typically consists of 12 members, with representation proportional to 
          party standings in the House.
        </p>
      </div>
    </div>
  );
}
