// Bill Types based on Legacy OpenPolicy Infrastructure (Bill.php, BillVoteCast.php, etc.)

export interface Bill {
  id: string;
  title: string;
  description?: string;
  summary?: string;
  billNumber?: string;
  type?: string;
  billType?: string;
  status?: string;
  introducedDate?: string;
  sponsor?: string;
  keywords?: string[];
  relatedBills?: RelatedBill[];
  // Additional fields from legacy system
  session?: string;
  chamber?: string;
  committee?: string;
  lastModified?: string;
  source?: string;
}

export interface RelatedBill {
  id: string;
  title: string;
  billNumber: string;
  status: string;
}

export interface BillVote {
  id: string;
  billId: string;
  date?: string;
  voteType?: string;
  description?: string;
  yes: number;
  no: number;
  abstain: number;
  session?: string;
  division?: string;
  required?: string;
  partyBreakdown?: Record<string, number>;
  mpVotes?: MPVote[];
}

export interface MPVote {
  mpId: string;
  mpName: string;
  party: string;
  vote: 'yes' | 'no' | 'abstain';
  constituency?: string;
}

export interface BillHistoryItem {
  id: string;
  billId: string;
  status: string;
  date?: string;
  description?: string;
  session?: string;
  chamber?: string;
  committee?: string;
  voteResult?: 'passed' | 'failed' | 'tied';
  voteBreakdown?: {
    yes: number;
    no: number;
    abstain: number;
  };
  notes?: string;
  relatedDocuments?: RelatedDocument[];
}

export interface RelatedDocument {
  title: string;
  url: string;
  type?: string;
  date?: string;
}

// Extended Bill interface for detailed views
export interface BillDetail extends Bill {
  // Additional detailed fields
  fullText?: string;
  amendments?: BillAmendment[];
  debates?: BillDebate[];
  committees?: BillCommittee[];
  sponsors?: BillSponsor[];
  fiscalImpact?: FiscalImpact;
  publicOpinion?: PublicOpinion;
}

export interface BillAmendment {
  id: string;
  title: string;
  description: string;
  date: string;
  sponsor: string;
  status: 'proposed' | 'accepted' | 'rejected';
  text?: string;
}

export interface BillDebate {
  id: string;
  date: string;
  chamber: string;
  session: string;
  participants: DebateParticipant[];
  summary: string;
  transcript?: string;
}

export interface DebateParticipant {
  mpId: string;
  mpName: string;
  party: string;
  role: 'speaker' | 'respondent' | 'moderator';
  speakingTime?: number;
}

export interface BillCommittee {
  id: string;
  name: string;
  type: 'standing' | 'special' | 'joint';
  members: CommitteeMember[];
  reports?: CommitteeReport[];
}

export interface CommitteeMember {
  mpId: string;
  mpName: string;
  party: string;
  role: 'chair' | 'vice-chair' | 'member';
  constituency?: string;
}

export interface CommitteeReport {
  id: string;
  title: string;
  date: string;
  recommendations: string[];
  url?: string;
}

export interface BillSponsor {
  mpId: string;
  mpName: string;
  party: string;
  constituency: string;
  role: 'primary' | 'secondary' | 'co-sponsor';
}

export interface FiscalImpact {
  estimatedCost?: number;
  costDescription?: string;
  revenueImpact?: number;
  implementationCost?: number;
  annualCost?: number;
  costBreakdown?: Record<string, number>;
}

export interface PublicOpinion {
  supportPercentage?: number;
  oppositionPercentage?: number;
  undecidedPercentage?: number;
  pollDate?: string;
  pollSource?: string;
  keyIssues?: string[];
}

// Bill search and filtering types
export interface BillFilters {
  status?: string[];
  type?: string[];
  sponsor?: string[];
  dateRange?: {
    start: string;
    end: string;
  };
  keywords?: string[];
  chamber?: string[];
}

export interface BillSearchParams {
  query?: string;
  filters?: BillFilters;
  page?: number;
  limit?: number;
  sortBy?: 'date' | 'title' | 'status' | 'sponsor';
  sortOrder?: 'asc' | 'desc';
}

export interface BillSearchResults {
  bills: Bill[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Bill comparison types
export interface BillComparison {
  bill1: Bill;
  bill2: Bill;
  similarities: string[];
  differences: BillDifference[];
}

export interface BillDifference {
  field: string;
  bill1Value: any;
  bill2Value: any;
  significance: 'low' | 'medium' | 'high';
}

// Bill tracking types
export interface BillTracker {
  userId: string;
  billId: string;
  notifications: boolean;
  emailUpdates: boolean;
  pushUpdates: boolean;
  customAlerts?: string[];
  createdAt: string;
  updatedAt: string;
}

// Bill analytics types
export interface BillAnalytics {
  billId: string;
  views: number;
  saves: number;
  shares: number;
  comments: number;
  userEngagement: number;
  popularKeywords: string[];
  relatedSearches: string[];
  timeOnPage: number;
}

// Export all types
export type {
  Bill,
  BillDetail,
  BillVote,
  BillHistoryItem,
  RelatedBill,
  MPVote,
  RelatedDocument,
  BillAmendment,
  BillDebate,
  DebateParticipant,
  BillCommittee,
  CommitteeMember,
  CommitteeReport,
  BillSponsor,
  FiscalImpact,
  PublicOpinion,
  BillFilters,
  BillSearchParams,
  BillSearchResults,
  BillComparison,
  BillDifference,
  BillTracker,
  BillAnalytics,
};
