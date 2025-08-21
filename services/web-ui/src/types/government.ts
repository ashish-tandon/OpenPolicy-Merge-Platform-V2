/**
 * Type definitions for Multi-Level Government API
 * Following FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL
 */

export interface GovernmentLevel {
  id: string;
  name: string;
  description: string;
  level_order: number;
  created_at: string;
  updated_at: string;
}

export interface Jurisdiction {
  id: string;
  name: string;
  code: string;
  government_level_id: string;
  province: string | null;
  jurisdiction_type: JurisdictionType;
  website: string | null;
  extras: Record<string, any>;
  government_level: GovernmentLevel;
  created_at: string;
  updated_at: string;
}

export interface Representative {
  id: string;
  name: string;
  jurisdiction_id: string;
  party: string | null;
  position: RepresentativePosition;
  riding: string | null;
  email: string | null;
  phone: string | null;
  website: string | null;
  extras: Record<string, any>;
  metadata_json: Record<string, any>;
  jurisdiction: Jurisdiction;
  created_at: string;
  updated_at: string;
}

export interface Office {
  id: string;
  name: string;
  jurisdiction_id: string;
  office_type: OfficeType;
  location: string | null;
  phone: string | null;
  email: string | null;
  extras: Record<string, any>;
  jurisdiction: Jurisdiction;
  created_at: string;
  updated_at: string;
}

export interface Bill {
  id: string;
  title: string;
  jurisdiction_id: string;
  bill_number: string;
  summary: string | null;
  status: BillStatus;
  introduced_date: string | null;
  sponsor_id: string | null;
  extras: Record<string, any>;
  jurisdiction: Jurisdiction;
  sponsor: Representative | null;
  created_at: string;
  updated_at: string;
}

export interface Vote {
  id: string;
  bill_id: string;
  representative_id: string;
  vote_position: VotePosition;
  vote_date: string;
  session: string | null;
  extras: Record<string, any>;
  bill: Bill;
  representative: Representative;
  created_at: string;
  updated_at: string;
}

export interface DataSource {
  id: string;
  name: string;
  jurisdiction_id: string;
  source_type: string;
  url: string | null;
  legacy_module: string | null;
  legacy_class: string | null;
  last_updated: string | null;
  extras: Record<string, any>;
  jurisdiction: Jurisdiction;
  created_at: string;
  updated_at: string;
}

export interface SystemStats {
  total_government_levels: number;
  total_jurisdictions: number;
  total_representatives: number;
  total_bills: number;
  total_votes: number;
  total_offices: number;
  total_data_sources: number;
  last_updated: string;
}

export interface GovernmentLevelStats {
  level_id: string;
  level_name: string;
  total_jurisdictions: number;
  total_representatives: number;
  total_bills: number;
  total_votes: number;
  total_offices: number;
  last_updated: string;
}

export interface JurisdictionStats {
  jurisdiction_id: string;
  jurisdiction_name: string;
  total_representatives: number;
  total_bills: number;
  total_votes: number;
  total_offices: number;
  last_updated: string;
}

export interface PaginationInfo {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: PaginationInfo;
}

// Enums
export type JurisdictionType = 
  | 'legislature'
  | 'parliament'
  | 'city_council'
  | 'town_council'
  | 'regional_council'
  | 'first_nations';

export type RepresentativePosition = 
  | 'mp'
  | 'mla'
  | 'mpp'
  | 'mayor'
  | 'councillor'
  | 'deputy_mayor'
  | 'chair'
  | 'deputy_chair';

export type OfficeType = 
  | 'constituency'
  | 'parliamentary'
  | 'city_hall'
  | 'town_hall'
  | 'regional_office'
  | 'legislative';

export type BillStatus = 
  | 'introduced'
  | 'first_reading'
  | 'second_reading'
  | 'third_reading'
  | 'committee'
  | 'royal_assent'
  | 'enacted'
  | 'defeated'
  | 'withdrawn';

export type VotePosition = 
  | 'yes'
  | 'no'
  | 'abstain'
  | 'absent'
  | 'paired';

export type GovernmentLevelName = 'federal' | 'provincial' | 'municipal';

// Search and filter types
export interface RepresentativeFilters {
  q?: string;
  jurisdiction_id?: string;
  government_level?: string;
  province?: string;
  party?: string;
  position?: RepresentativePosition;
  page?: number;
  page_size?: number;
}

export interface BillFilters {
  q?: string;
  jurisdiction_id?: string;
  government_level?: string;
  status?: BillStatus;
  sponsor_id?: string;
  introduced_after?: string;
  introduced_before?: string;
  page?: number;
  page_size?: number;
}

export interface VoteFilters {
  bill_id?: string;
  representative_id?: string;
  vote_position?: VotePosition;
  vote_after?: string;
  vote_before?: string;
  session?: string;
  page?: number;
  page_size?: number;
}

export interface JurisdictionFilters {
  government_level?: string;
  province?: string;
  jurisdiction_type?: JurisdictionType;
  page?: number;
  page_size?: number;
}

export interface OfficeFilters {
  jurisdiction_id?: string;
  government_level?: string;
  office_type?: OfficeType;
  province?: string;
  page?: number;
  page_size?: number;
}

export interface DataSourceFilters {
  jurisdiction_id?: string;
  government_level?: string;
  source_type?: string;
  page?: number;
  page_size?: number;
}
