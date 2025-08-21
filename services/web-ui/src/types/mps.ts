// MP Types based on Legacy OpenPolicy Infrastructure and Current V2 System

export interface MP {
  id: string;
  full_name: string;
  first_name?: string;
  last_name?: string;
  constituency?: string;
  party?: string;
  province?: string;
  email?: string;
  phone?: string;
  website?: string;
  twitter?: string;
  facebook?: string;
  instagram?: string;
  linkedin?: string;
  photo_url?: string;
  bio?: string;
  education?: string[];
  profession?: string;
  date_of_birth?: string;
  place_of_birth?: string;
  languages?: string[];
  committees?: string[];
  cabinet_position?: string;
  opposition_critic?: string;
  parliamentary_secretary?: string;
  first_elected?: string;
  terms_served?: number;
  current_term_start?: string;
  current_term_end?: string;
  previous_constituencies?: string[];
  previous_parties?: string[];
  awards?: string[];
  publications?: string[];
  interests?: string[];
  voting_record?: VotingStats;
  attendance_rate?: number;
  last_activity?: string;
  source?: string;
  last_updated?: string;
}

export interface VotingStats {
  total_votes: number;
  yes_votes: number;
  no_votes: number;
  abstentions: number;
  absences: number;
  attendance_rate: number;
  party_line_votes: number;
  independent_votes: number;
}

export interface MPVote {
  id: string;
  bill_id: string;
  bill_title: string;
  bill_number?: string;
  vote_date: string;
  vote_type: 'yes' | 'no' | 'abstain' | 'absent';
  vote_result: 'passed' | 'defeated' | 'tied';
  vote_description?: string;
  vote_context?: string;
  party_position?: 'for' | 'against' | 'free';
  constituency_impact?: string;
  related_amendment?: string;
  committee_recommendation?: string;
  government_position?: 'for' | 'against' | 'neutral';
  opposition_position?: 'for' | 'against' | 'neutral';
  whip_status?: 'whipped' | 'free' | 'rebel';
  vote_confidence?: 'high' | 'medium' | 'low';
  source?: string;
}

export interface MPCommittee {
  id: string;
  name: string;
  role: 'member' | 'chair' | 'vice_chair' | 'ex_officio';
  start_date: string;
  end_date?: string;
  committee_type: 'standing' | 'special' | 'joint' | 'subcommittee';
  jurisdiction: string;
  description?: string;
  meeting_attendance?: number;
  total_meetings?: number;
  reports_contributed?: number;
  amendments_proposed?: number;
  amendments_passed?: number;
  source?: string;
}

export interface MPActivity {
  id: string;
  type: 'speech' | 'question' | 'motion' | 'amendment' | 'committee_work' | 'constituency_work' | 'media_appearance' | 'parliamentary_event';
  title: string;
  description?: string;
  date: string;
  location?: string;
  related_bill?: string;
  related_committee?: string;
  related_debate?: string;
  media_coverage?: string[];
  public_response?: string;
  impact_assessment?: string;
  tags?: string[];
  source?: string;
}

export interface MPSpeech {
  id: string;
  date: string;
  topic: string;
  content: string;
  duration: number;
  word_count: number;
  audience: string;
  context: string;
  related_bill?: string;
  related_debate?: string;
  media_coverage?: string[];
  public_response?: string;
  source?: string;
}

export interface MPQuestion {
  id: string;
  date: string;
  question_number: string;
  question_type: 'oral' | 'written' | 'emergency' | 'order_paper';
  topic: string;
  content: string;
  minister: string;
  department: string;
  answer?: string;
  answer_date?: string;
  follow_up?: string;
  status: 'asked' | 'answered' | 'pending' | 'withdrawn';
  source?: string;
}

export interface MPMotion {
  id: string;
  date: string;
  motion_number: string;
  title: string;
  content: string;
  motion_type: 'government' | 'opposition' | 'private_member' | 'committee';
  status: 'introduced' | 'debated' | 'amended' | 'passed' | 'defeated' | 'withdrawn';
  vote_result?: 'passed' | 'defeated' | 'tied';
  vote_breakdown?: {
    yes: number;
    no: number;
    abstain: number;
    absent: number;
  };
  related_bill?: string;
  related_committee?: string;
  source?: string;
}

export interface MPAmendment {
  id: string;
  date: string;
  amendment_number: string;
  bill_id: string;
  bill_title: string;
  title: string;
  content: string;
  amendment_type: 'text' | 'clause' | 'schedule' | 'title' | 'preamble';
  status: 'introduced' | 'debated' | 'passed' | 'defeated' | 'withdrawn';
  vote_result?: 'passed' | 'defeated' | 'tied';
  vote_breakdown?: {
    yes: number;
    no: number;
    abstain: number;
    absent: number;
  };
  committee_recommendation?: string;
  government_position?: 'for' | 'against' | 'neutral';
  opposition_position?: 'for' | 'against' | 'neutral';
  source?: string;
}

export interface MPConstituencyWork {
  id: string;
  date: string;
  type: 'constituency_office' | 'community_event' | 'public_meeting' | 'casework' | 'media_interview' | 'social_media';
  title: string;
  description?: string;
  location: string;
  attendees?: number;
  media_coverage?: string[];
  public_response?: string;
  impact_assessment?: string;
  follow_up_required?: boolean;
  source?: string;
}

export interface MPMediaAppearance {
  id: string;
  date: string;
  type: 'interview' | 'article' | 'op_ed' | 'press_release' | 'social_media' | 'podcast' | 'television' | 'radio';
  title: string;
  outlet: string;
  content?: string;
  url?: string;
  audience?: string;
  key_messages?: string[];
  public_response?: string;
  impact_assessment?: string;
  related_topics?: string[];
  source?: string;
}

export interface MPParliamentaryEvent {
  id: string;
  date: string;
  type: 'swearing_in' | 'resignation' | 'election' | 'party_change' | 'cabinet_appointment' | 'opposition_critic_appointment' | 'parliamentary_secretary_appointment' | 'committee_appointment' | 'award' | 'recognition';
  title: string;
  description?: string;
  location?: string;
  attendees?: string[];
  media_coverage?: string[];
  public_response?: string;
  impact_assessment?: string;
  related_mp?: string;
  source?: string;
}

export interface MPSearchParams {
  name?: string;
  party?: string;
  province?: string;
  constituency?: string;
  committee?: string;
  cabinet_position?: string;
  opposition_critic?: string;
  parliamentary_secretary?: string;
  first_elected_after?: string;
  first_elected_before?: string;
  terms_served_min?: number;
  terms_served_max?: number;
  attendance_rate_min?: number;
  attendance_rate_max?: number;
  voting_record?: {
    yes_votes_min?: number;
    no_votes_min?: number;
    independent_votes_min?: number;
  };
  sort_by?: 'name' | 'constituency' | 'party' | 'first_elected' | 'terms_served' | 'attendance_rate' | 'total_votes';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

export interface MPSearchResults {
  results: MP[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
  filters: MPSearchParams;
  summary: {
    total_mps: number;
    parties: { [key: string]: number };
    provinces: { [key: string]: number };
    average_attendance: number;
    average_terms: number;
  };
}

export interface MPComparison {
  mp1: MP;
  mp2: MP;
  comparison: {
    voting_similarity: number;
    attendance_comparison: number;
    committee_overlap: string[];
    party_differences: string[];
    term_comparison: number;
    constituency_demographics?: {
      population: number;
      median_income: number;
      education_level: number;
      urban_rural: string;
    };
  };
}

export interface MPTracker {
  id: string;
  mp_id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  notifications_enabled: boolean;
  notification_types: string[];
  last_activity_check: string;
  activity_summary: {
    total_activities: number;
    recent_speeches: number;
    recent_votes: number;
    recent_questions: number;
    recent_motions: number;
    recent_amendments: number;
    recent_constituency_work: number;
    recent_media_appearances: number;
    recent_parliamentary_events: number;
  };
}

export interface MPAnalytics {
  mp_id: string;
  period: 'week' | 'month' | 'quarter' | 'year' | 'term';
  start_date: string;
  end_date: string;
  metrics: {
    total_activities: number;
    speeches: number;
    questions: number;
    motions: number;
    amendments: number;
    constituency_work: number;
    media_appearances: number;
    parliamentary_events: number;
    voting_attendance: number;
    party_line_votes: number;
    independent_votes: number;
    committee_meetings: number;
    public_engagement: number;
    media_coverage: number;
  };
  trends: {
    activity_trend: 'increasing' | 'decreasing' | 'stable';
    engagement_trend: 'increasing' | 'decreasing' | 'stable';
    media_trend: 'increasing' | 'decreasing' | 'stable';
    voting_trend: 'increasing' | 'decreasing' | 'stable';
  };
  comparisons: {
    party_average: number;
    province_average: number;
    national_average: number;
    ranking: number;
    percentile: number;
  };
}
