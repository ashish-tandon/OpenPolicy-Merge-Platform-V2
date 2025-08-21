'use client';
            
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  CalendarIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  XCircleIcon,
  MinusIcon,
  ChartBarIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';
import { VoteRecord } from '@/types/voting';
            
export default function VotingRecordsList() {
  const [votingRecords, setVotingRecords] = useState<VoteRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedResult, setSelectedResult] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [selectedDateFrom, setSelectedDateFrom] = useState('');
  const [selectedDateTo, setSelectedDateTo] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
            
  // Mock data for demonstration - in production this would come from the API
  const mockVotingRecords: VoteRecord[] = [
    {
      id: '1',
      bill_id: 'bill-001',
      bill_title: 'An Act to amend the Criminal Code (medical assistance in dying)',
      bill_number: 'C-7',
      vote_date: '2021-03-17',
      vote_type: 'division',
      vote_result: 'passed',
      vote_description: 'Third reading vote on medical assistance in dying legislation',
      vote_context: 'Controversial bill expanding access to medical assistance in dying',
      total_votes: 338,
      yes_votes: 180,
      no_votes: 149,
      abstentions: 9,
      absences: 0,
      turnout_percentage: 100,
      government_position: 'for',
      opposition_position: 'against',
      whip_status: 'whipped',
      source: 'Parliament of Canada',
      last_updated: '2021-03-17'
    },
    {
      id: '2',
      bill_id: 'bill-002',
      bill_title: 'An Act respecting a framework on payments to the families of missing and murdered Indigenous women and girls',
      bill_number: 'C-92',
      vote_date: '2019-06-21',
      vote_type: 'division',
      vote_result: 'passed',
      vote_description: 'Third reading vote on Indigenous child welfare legislation',
      vote_context: 'Bill establishing Indigenous jurisdiction over child and family services',
      total_votes: 338,
      yes_votes: 263,
      no_votes: 63,
      abstentions: 12,
      absences: 0,
      turnout_percentage: 100,
      government_position: 'for',
      opposition_position: 'mixed',
      whip_status: 'free',
      source: 'Parliament of Canada',
      last_updated: '2019-06-21'
    },
    {
      id: '3',
      bill_id: 'bill-003',
      bill_title: 'An Act to implement the Agreement between Canada, the United States of America and the United Mexican States',
      bill_number: 'C-100',
      vote_date: '2020-03-13',
      vote_type: 'division',
      vote_result: 'passed',
      vote_description: 'Third reading vote on USMCA trade agreement implementation',
      vote_context: 'Implementation of the new North American trade agreement',
      total_votes: 338,
      yes_votes: 275,
      no_votes: 56,
      abstentions: 7,
      absences: 0,
      turnout_percentage: 100,
      government_position: 'for',
      opposition_position: 'for',
      whip_status: 'whipped',
      source: 'Parliament of Canada',
      last_updated: '2020-03-13'
    },
    {
      id: '4',
      bill_id: 'bill-004',
      bill_title: 'An Act respecting the reduction of poverty',
      bill_number: 'C-97',
      vote_date: '2019-06-21',
      vote_type: 'division',
      vote_result: 'passed',
      vote_description: 'Third reading vote on poverty reduction strategy',
      vote_context: 'Bill establishing Canada\'s first poverty reduction strategy',
      total_votes: 338,
      yes_votes: 244,
      no_votes: 82,
      abstentions: 12,
      absences: 0,
      turnout_percentage: 100,
      government_position: 'for',
      opposition_position: 'mixed',
      whip_status: 'free',
      source: 'Parliament of Canada',
      last_updated: '2019-06-21'
    },
    {
      id: '5',
      bill_id: 'bill-005',
      bill_title: 'An Act to amend the Criminal Code and the Controlled Drugs and Substances Act',
      bill_number: 'C-45',
      vote_date: '2018-06-19',
      vote_type: 'division',
      vote_result: 'passed',
      vote_description: 'Third reading vote on cannabis legalization',
      vote_context: 'Historic bill legalizing recreational cannabis use in Canada',
      total_votes: 338,
      yes_votes: 205,
      no_votes: 82,
      abstentions: 51,
      absences: 0,
      turnout_percentage: 100,
      government_position: 'for',
      opposition_position: 'against',
      whip_status: 'whipped',
      source: 'Parliament of Canada',
      last_updated: '2018-06-19'
    }
  ];
            
  useEffect(() => {
    // Load voting records from API
    const loadVotingRecords = async () => {
      setLoading(true);
      try {
        const response = await api.getVotingRecords(currentPage, 20, searchTerm, selectedResult, selectedType);
        setVotingRecords(response.results);
        setTotalPages(response.pagination.total_pages);
      } catch (error) {
        console.error('Error loading voting records:', error);
        // Fallback to mock data if API fails
        setVotingRecords(mockVotingRecords);
        setTotalPages(1);
      } finally {
        setLoading(false);
      }
    };
            
    loadVotingRecords();
  }, [currentPage, searchTerm, selectedResult, selectedType]);
            
  const filteredRecords = votingRecords.filter(record => {
    const matchesSearch = record.bill_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (record.bill_number && record.bill_number.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesResult = !selectedResult || record.vote_result === selectedResult;
    const matchesType = !selectedType || record.vote_type === selectedType;
    const matchesDateFrom = !selectedDateFrom || record.vote_date >= selectedDateFrom;
    const matchesDateTo = !selectedDateTo || record.vote_date <= selectedDateTo;
            
    return matchesSearch && matchesResult && matchesType && matchesDateFrom && matchesDateTo;
  });
            
  const getResultColor = (result: string) => {
    switch (result) {
      case 'passed':
        return 'bg-green-100 text-green-800';
      case 'defeated':
        return 'bg-red-100 text-red-800';
      case 'tied':
        return 'bg-yellow-100 text-yellow-800';
      case 'withdrawn':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
            
  const getTypeColor = (type: string) => {
    switch (type) {
      case 'division':
        return 'bg-blue-100 text-blue-800';
      case 'voice':
        return 'bg-purple-100 text-purple-800';
      case 'unanimous':
        return 'bg-green-100 text-green-800';
      case 'recorded':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
            
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
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
          {/* Search */}
          <div className="lg:col-span-2">
            <label htmlFor="search" className="sr-only">Search voting records</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                id="search"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
                placeholder="Search by bill title or number..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
            
          {/* Result Filter */}
          <div>
            <label htmlFor="result" className="sr-only">Filter by result</label>
            <select
              id="result"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
              value={selectedResult}
              onChange={(e) => setSelectedResult(e.target.value)}
            >
              <option value="">All Results</option>
              <option value="passed">Passed</option>
              <option value="defeated">Defeated</option>
              <option value="tied">Tied</option>
              <option value="withdrawn">Withdrawn</option>
            </select>
          </div>
            
          {/* Type Filter */}
          <div>
            <label htmlFor="type" className="sr-only">Filter by vote type</label>
            <select
              id="type"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
            >
              <option value="">All Types</option>
              <option value="division">Division</option>
              <option value="voice">Voice</option>
              <option value="unanimous">Unanimous</option>
              <option value="recorded">Recorded</option>
            </select>
          </div>
        </div>
            
        {/* Date Range Filters */}
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="dateFrom" className="block text-sm font-medium text-gray-700 mb-1">
              Date From
            </label>
            <input
              type="date"
              id="dateFrom"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
              value={selectedDateFrom}
              onChange={(e) => setSelectedDateFrom(e.target.value)}
            />
          </div>
            
          <div>
            <label htmlFor="dateTo" className="block text-sm font-medium text-gray-700 mb-1">
              Date To
            </label>
            <input
              type="date"
              id="dateTo"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-op-blue focus:border-op-blue sm:text-sm"
              value={selectedDateTo}
              onChange={(e) => setSelectedDateTo(e.target.value)}
            />
          </div>
        </div>
      </div>
            
      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-700">
          Showing {filteredRecords.length} voting record{filteredRecords.length !== 1 ? 's' : ''}
        </p>
      </div>
            
      {/* Voting Records List */}
      {filteredRecords.length > 0 ? (
        <div className="space-y-4">
          {filteredRecords.map((record) => (
            <div key={record.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    {/* Bill Title and Number */}
                    <div className="flex items-center space-x-3 mb-2">
                      <DocumentTextIcon className="h-5 w-5 text-gray-400" />
                      <h3 className="text-lg font-medium text-gray-900">
                        <Link href={`/bills/${record.bill_id}`} className="hover:text-op-blue transition-colors">
                          {record.bill_title}
                        </Link>
                      </h3>
                    </div>
                    
                    {record.bill_number && (
                      <p className="text-sm text-gray-500 mb-3">Bill {record.bill_number}</p>
                    )}
                    
                    {/* Vote Details */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                      <div className="flex items-center space-x-2">
                        <CalendarIcon className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-600">
                          {format(new Date(record.vote_date), 'MMM dd, yyyy')}
                        </span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <ChartBarIcon className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-600">
                          {record.turnout_percentage}% turnout
                        </span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <UserGroupIcon className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-600">
                          {record.total_votes} MPs voted
                        </span>
                      </div>
                    </div>
                    
                    {/* Vote Description */}
                    {record.vote_description && (
                      <p className="text-sm text-gray-600 mb-4">{record.vote_description}</p>
                    )}
                    
                    {/* Vote Context */}
                    {record.vote_context && (
                      <p className="text-sm text-gray-500 mb-4 italic">{record.vote_context}</p>
                    )}
                    
                    {/* Vote Breakdown */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div className="text-center">
                        <div className="font-medium text-green-600">{record.yes_votes}</div>
                        <div className="text-gray-500">Yes</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium text-red-600">{record.no_votes}</div>
                        <div className="text-gray-500">No</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium text-yellow-600">{record.abstentions}</div>
                        <div className="text-gray-500">Abstain</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium text-gray-600">{record.absences}</div>
                        <div className="text-gray-500">Absent</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Vote Result and Type */}
                  <div className="ml-6 text-right space-y-2">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getResultColor(record.vote_result)}`}>
                      {record.vote_result.charAt(0).toUpperCase() + record.vote_result.slice(1)}
                    </span>
                    
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(record.vote_type)}`}>
                      {record.vote_type.charAt(0).toUpperCase() + record.vote_type.slice(1)}
                    </span>
                  </div>
                </div>
                
                {/* Action Buttons */}
                <div className="mt-6 flex space-x-3">
                  <Link
                    href={`/bills/${record.bill_id}`}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue transition-colors"
                  >
                    View Bill
                  </Link>
                  
                  <Link
                    href={`/voting-records/${record.id}`}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-op-blue hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue transition-colors"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <ChartBarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Voting Records Found</h3>
          <p className="text-gray-600">
            No voting records match your current search criteria. Try adjusting your filters.
          </p>
        </div>
      )}
    </div>
  );
}
