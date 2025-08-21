// Voting Types based on Legacy OpenPolicy Infrastructure and Current V2 System

export interface VoteRecord {
  id: string;
  bill_id: string;
  bill_title: string;
  bill_number?: string;
  vote_date: string;
  vote_type: 'division' | 'voice' | 'unanimous' | 'recorded';
  vote_result: 'passed' | 'defeated' | 'tied' | 'withdrawn';
  vote_description?: string;
  vote_context?: string;
  vote_summary?: string;
  total_votes: number;
  yes_votes: number;
  no_votes: number;
  abstentions: number;
  absences: number;
  turnout_percentage: number;
  government_position?: 'for' | 'against' | 'neutral' | 'free';
  opposition_position?: 'for' | 'against' | 'neutral' | 'free';
  whip_status?: 'whipped' | 'free' | 'rebel' | 'none';
  related_amendment?: string;
  committee_recommendation?: string;
  constituency_impact?: string;
  media_coverage?: string[];
  public_response?: string;
  source?: string;
  last_updated?: string;
}

export interface MPVoteDetail {
  id: string;
  mp_id: string;
  mp_name: string;
  mp_constituency: string;
  mp_party: string;
  mp_province: string;
  vote_cast: 'yes' | 'no' | 'abstain' | 'absent';
  vote_time?: string;
  vote_location?: string;
  party_position?: 'for' | 'against' | 'free';
  whip_status?: 'whipped' | 'free' | 'rebel';
  constituency_impact?: string;
  personal_statement?: string;
  media_comment?: string;
  follow_up_action?: string;
  source?: string;
}

export interface VoteBreakdown {
  total_mps: number;
  present_mps: number;
  absent_mps: number;
  yes_votes: number;
  no_votes: number;
  abstentions: number;
  turnout_percentage: number;
  party_breakdown: {
    [party: string]: {
      total: number;
      yes: number;
      no: number;
      abstain: number;
      absent: number;
      percentage_for: number;
      percentage_against: number;
    };
  };
  province_breakdown: {
    [province: string]: {
      total: number;
      yes: number;
      no: number;
      abstain: number;
      absent: number;
      percentage_for: number;
      percentage_against: number;
    };
  };
  gender_breakdown?: {
    male: {
      total: number;
      yes: number;
      no: number;
      abstain: number;
      absent: number;
    };
    female: {
      total: number;
      yes: number;
      no: number;
      abstain: number;
      absent: number;
    };
  };
  experience_breakdown?: {
    [termRange: string]: {
      total: number;
      yes: number;
      no: number;
      abstain: number;
      absent: number;
      percentage_for: number;
      percentage_against: number;
    };
  };
}

export interface VoteAnalysis {
  vote_id: string;
  bill_id: string;
  analysis_date: string;
  key_findings: string[];
  party_cohesion: {
    [party: string]: number; // Percentage of party members voting together
  };
  regional_patterns: {
    [region: string]: {
      dominant_vote: 'yes' | 'no' | 'mixed';
      percentage_for: number;
      percentage_against: number;
      key_factors: string[];
    };
  };
  swing_voters: {
    mp_id: string;
    mp_name: string;
    mp_party: string;
    usual_pattern: string;
    this_vote: string;
    potential_reasons: string[];
  }[];
  rebellion_analysis: {
    total_rebels: number;
    rebel_mps: {
      mp_id: string;
      mp_name: string;
      mp_party: string;
      rebel_type: 'minor' | 'major' | 'total';
      potential_consequences: string[];
    }[];
    party_impact: {
      [party: string]: 'low' | 'medium' | 'high';
    };
  };
  public_opinion_correlation?: {
    poll_results: {
      pollster: string;
      poll_date: string;
      support_percentage: number;
      oppose_percentage: number;
      undecided_percentage: number;
    }[];
    correlation_strength: 'strong' | 'moderate' | 'weak' | 'none';
    correlation_direction: 'positive' | 'negative' | 'mixed';
  };
  media_analysis: {
    coverage_tone: 'positive' | 'negative' | 'neutral' | 'mixed';
    key_headlines: string[];
    editorial_positions: {
      [outlet: string]: 'support' | 'oppose' | 'neutral';
    };
    social_media_sentiment: {
      platform: string;
      positive_percentage: number;
      negative_percentage: number;
      neutral_percentage: number;
      trending_hashtags: string[];
    };
  };
  historical_context: {
    similar_votes: {
      vote_id: string;
      bill_title: string;
      vote_date: string;
      result: string;
      similarity_score: number;
      key_differences: string[];
    }[];
    trend_analysis: string;
    pattern_recognition: string[];
  };
  impact_assessment: {
    immediate_effects: string[];
    long_term_implications: string[];
    stakeholder_impact: {
      [stakeholder: string]: 'positive' | 'negative' | 'neutral' | 'mixed';
    };
    economic_impact?: {
      short_term: string;
      long_term: string;
      affected_sectors: string[];
    };
    social_impact?: {
      affected_groups: string[];
      equity_considerations: string[];
      community_response: string;
    };
  };
}

export interface VoteSearchParams {
  bill_title?: string;
  bill_number?: string;
  vote_date_from?: string;
  vote_date_to?: string;
  vote_result?: 'passed' | 'defeated' | 'tied' | 'withdrawn';
  vote_type?: 'division' | 'voice' | 'unanimous' | 'recorded';
  party?: string;
  province?: string;
  mp_name?: string;
  government_position?: 'for' | 'against' | 'neutral' | 'free';
  whip_status?: 'whipped' | 'free' | 'rebel' | 'none';
  turnout_min?: number;
  turnout_max?: number;
  sort_by?: 'date' | 'bill_title' | 'turnout' | 'result' | 'total_votes';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

export interface VoteSearchResults {
  results: VoteRecord[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
  filters: VoteSearchParams;
  summary: {
    total_votes: number;
    passed_bills: number;
    defeated_bills: number;
    tied_bills: number;
    average_turnout: number;
    most_active_parties: { [party: string]: number };
    most_active_provinces: { [province: string]: number };
  };
}

export interface VoteComparison {
  vote1: VoteRecord;
  vote2: VoteRecord;
  comparison: {
    similarity_score: number;
    turnout_difference: number;
    result_difference: boolean;
    party_cohesion_changes: {
      [party: string]: {
        before: number;
        after: number;
        change: number;
      };
    };
    regional_pattern_changes: {
      [region: string]: {
        before: 'yes' | 'no' | 'mixed';
        after: 'yes' | 'no' | 'mixed';
        change_factor: string;
      };
    };
    key_differences: string[];
    potential_reasons: string[];
  };
}

export interface VoteTracker {
  id: string;
  user_id: string;
  vote_id: string;
  created_at: string;
  updated_at: string;
  notifications_enabled: boolean;
  notification_types: string[];
  last_activity_check: string;
  activity_summary: {
    total_activities: number;
    recent_updates: number;
    related_bills: number;
    related_committees: number;
  };
}

export interface VoteAnalytics {
  vote_id: string;
  period: 'day' | 'week' | 'month' | 'quarter' | 'year';
  start_date: string;
  end_date: string;
  metrics: {
    total_views: number;
    unique_visitors: number;
    page_views: number;
    time_on_page: number;
    bounce_rate: number;
    social_shares: number;
    media_coverage: number;
    public_engagement: number;
    academic_citations: number;
  };
  trends: {
    view_trend: 'increasing' | 'decreasing' | 'stable';
    engagement_trend: 'increasing' | 'decreasing' | 'stable';
    media_trend: 'increasing' | 'decreasing' | 'stable';
    academic_trend: 'increasing' | 'decreasing' | 'stable';
  };
  comparisons: {
    similar_votes_average: number;
    category_average: number;
    overall_average: number;
    ranking: number;
    percentile: number;
  };
}
