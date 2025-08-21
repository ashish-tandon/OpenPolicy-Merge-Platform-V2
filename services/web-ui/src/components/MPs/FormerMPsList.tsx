'use client';
            
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  CalendarIcon,
  MapPinIcon,
  BuildingOfficeIcon,
  UserIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';
import { MP } from '@/types/mps';
            
export default function FormerMPsList() {
  const [formerMPs, setFormerMPs] = useState<MP[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedParty, setSelectedParty] = useState('');
  const [selectedProvince, setSelectedProvince] = useState('');
  const [selectedTerm, setSelectedTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
            
  // Mock data for demonstration - in production this would come from the API
  const mockFormerMPs: MP[] = [
    {
      id: '1',
      full_name: 'John Smith',
      constituency: 'Toronto Centre',
      party: 'Liberal Party',
      province: 'Ontario',
      first_elected: '2015-10-19',
      terms_served: 2,
      current_term_start: '2015-10-19',
      current_term_end: '2021-09-20',
      photo_url: undefined,
      bio: 'Former Liberal MP who served two terms representing Toronto Centre.',
      education: ['University of Toronto', 'Osgoode Hall Law School'],
      profession: 'Lawyer',
      committees: ['Standing Committee on Justice', 'Standing Committee on Finance'],
      voting_record: {
        total_votes: 156,
        yes_votes: 89,
        no_votes: 45,
        abstentions: 12,
        absences: 10,
        attendance_rate: 93.6,
        party_line_votes: 78,
        independent_votes: 78
      },
      attendance_rate: 93.6,
      last_activity: '2021-09-20',
      source: 'Parliament of Canada',
      last_updated: '2021-09-20'
    },
    {
      id: '2',
      full_name: 'Sarah Johnson',
      constituency: 'Vancouver South',
      party: 'Conservative Party',
      province: 'British Columbia',
      first_elected: '2011-05-02',
      terms_served: 3,
      current_term_start: '2011-05-02',
      current_term_end: '2019-10-21',
      photo_url: undefined,
      bio: 'Former Conservative MP who served three terms representing Vancouver South.',
      education: ['University of British Columbia', 'Simon Fraser University'],
      profession: 'Business Consultant',
      committees: ['Standing Committee on Industry', 'Standing Committee on Transport'],
      voting_record: {
        total_votes: 234,
        yes_votes: 67,
        no_votes: 145,
        abstentions: 15,
        absences: 7,
        attendance_rate: 97.0,
        party_line_votes: 89,
        independent_votes: 145
      },
      attendance_rate: 97.0,
      last_activity: '2019-10-21',
      source: 'Parliament of Canada',
      last_updated: '2019-10-21'
    },
    {
      id: '3',
      full_name: 'Michael Chen',
      constituency: 'Calgary Northeast',
      party: 'Conservative Party',
      province: 'Alberta',
      first_elected: '2008-10-14',
      terms_served: 4,
      current_term_start: '2008-10-14',
      current_term_end: '2021-09-20',
      photo_url: undefined,
      bio: 'Former Conservative MP who served four terms representing Calgary Northeast.',
      education: ['University of Calgary', 'University of Alberta'],
      profession: 'Engineer',
      committees: ['Standing Committee on Natural Resources', 'Standing Committee on Environment'],
      voting_record: {
        total_votes: 312,
        yes_votes: 89,
        no_votes: 198,
        abstentions: 18,
        absences: 7,
        attendance_rate: 97.8,
        party_line_votes: 156,
        independent_votes: 156
      },
      attendance_rate: 97.8,
      last_activity: '2021-09-20',
      source: 'Parliament of Canada',
      last_updated: '2021-09-20'
    }
  ];
            
  useEffect(() => {
    // Load former MPs from API
    const loadFormerMPs = async () => {
      setLoading(true);
      try {
        const response = await api.getFormerMembers(currentPage, 20, searchTerm, selectedParty, selectedProvince);
        setFormerMPs(response.results);
        setTotalPages(response.pagination.total_pages);
      } catch (error) {
        console.error('Error loading former MPs:', error);
        // Fallback to mock data if API fails
        setFormerMPs(mockFormerMPs);
        setTotalPages(1);
      } finally {
        setLoading(false);
      }
    };
            
    loadFormerMPs();
  }, [currentPage, searchTerm, selectedParty, selectedProvince]);
            
  const filteredMPs = formerMPs.filter(mp => {
    const matchesSearch = mp.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         mp.constituency.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesParty = !selectedParty || mp.party === selectedParty;
    const matchesProvince = !selectedProvince || mp.province === selectedProvince;
    const matchesTerm = !selectedTerm || mp.terms_served === parseInt(selectedTerm);
            
    return matchesSearch && matchesParty && matchesProvince && matchesTerm;
  });
            
  const parties = Array.from(new Set(formerMPs.map(mp => mp.party))).filter(Boolean);
  const provinces = Array.from(new Set(formerMPs.map(mp => mp.province))).filter(Boolean);
  const terms = Array.from(new Set(formerMPs.map(mp => mp.terms_served))).sort((a, b) => a - b);
            
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }
            
  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          {/* Search */}
          <div className="lg:col-span-2">
            <label htmlFor="search" className="sr-only">Search former MPs</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                id="search"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
                placeholder="Search by name or constituency..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
            
          {/* Party Filter */}
          <div>
            <label htmlFor="party" className="sr-only">Filter by party</label>
            <select
              id="party"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
              value={selectedParty}
              onChange={(e) => setSelectedParty(e.target.value)}
            >
              <option value="">All Parties</option>
              {parties.map(party => (
                <option key={party} value={party}>{party}</option>
              ))}
            </select>
          </div>
            
          {/* Province Filter */}
          <div>
            <label htmlFor="province" className="sr-only">Filter by province</label>
            <select
              id="province"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
              value={selectedProvince}
              onChange={(e) => setSelectedProvince(e.target.value)}
            >
              <option value="">All Provinces</option>
              {provinces.map(province => (
                <option key={province} value={province}>{province}</option>
              ))}
            </select>
          </div>
        </div>
            
        {/* Additional Filters */}
        <div className="mt-4 flex flex-wrap gap-4">
          <div className="flex items-center space-x-2">
            <FunnelIcon className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-500">Additional filters:</span>
          </div>
            
          {/* Terms Served Filter */}
          <div>
            <label htmlFor="terms" className="sr-only">Filter by terms served</label>
            <select
              id="terms"
              className="block px-3 py-1 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-op-blue focus:border-op-blue text-sm"
              value={selectedTerm}
              onChange={(e) => setSelectedTerm(e.target.value)}
            >
              <option value="">All Terms</option>
              {terms.map(term => (
                <option key={term} value={term}>{term} term{term > 1 ? 's' : ''}</option>
              ))}
            </select>
          </div>
        </div>
      </div>
            
      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-700">
          Showing {filteredMPs.length} former MP{filteredMPs.length !== 1 ? 's' : ''}
        </p>
      </div>
            
      {/* Former MPs Grid */}
      {filteredMPs.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredMPs.map((mp) => (
            <div key={mp.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
              <div className="p-6">
                {/* MP Photo and Basic Info */}
                <div className="flex items-start space-x-4 mb-4">
                  {mp.photo_url ? (
                    <img
                      src={mp.photo_url}
                      alt={mp.full_name}
                      className="h-16 w-16 rounded-full object-cover"
                    />
                  ) : (
                    <div className="h-16 w-16 rounded-full bg-gray-200 flex items-center justify-center">
                      <UserIcon className="h-8 w-8 text-gray-400" />
                    </div>
                  )}
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      <Link href={`/mps/${mp.id}`} className="hover:text-op-blue transition-colors">
                        {mp.full_name}
                      </Link>
                    </h3>
                    <p className="text-sm text-gray-600 truncate">{mp.constituency}</p>
                  </div>
                </div>
                
                {/* MP Details */}
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center space-x-2">
                    <BuildingOfficeIcon className="h-4 w-4 text-gray-400" />
                    <span>{mp.party}</span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <MapPinIcon className="h-4 w-4 text-gray-400" />
                    <span>{mp.province}</span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <CalendarIcon className="h-4 w-4 text-gray-400" />
                    <span>{mp.terms_served} term{mp.terms_served > 1 ? 's' : ''} ({mp.first_elected?.split('-')[0]} - {mp.current_term_end?.split('-')[0]})</span>
                  </div>
                </div>
                
                {/* Voting Record Summary */}
                {mp.voting_record && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Voting Record</h4>
                    <div className="grid grid-cols-3 gap-2 text-xs">
                      <div className="text-center">
                        <div className="font-medium text-green-600">{mp.voting_record.yes_votes}</div>
                        <div className="text-gray-500">Yes</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium text-red-600">{mp.voting_record.no_votes}</div>
                        <div className="text-gray-500">No</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium text-gray-600">{mp.attendance_rate}%</div>
                        <div className="text-gray-500">Attendance</div>
                      </div>
                    </div>
                  </div>
                )}
                
                {/* View Profile Button */}
                <div className="mt-4">
                  <Link
                    href={`/mps/${mp.id}`}
                    className="block w-full text-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-op-blue hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue transition-colors"
                  >
                    View Profile
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <UserIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Former MPs Found</h3>
          <p className="text-gray-600">
            No former Members of Parliament match your current search criteria. Try adjusting your filters.
          </p>
        </div>
      )}
    </div>
  );
}
