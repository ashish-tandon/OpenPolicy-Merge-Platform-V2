/**
 * TypeScript definitions for OpenPolicy Mobile App API
 * 
 * These types ensure compatibility between the mobile app and web platform
 * by defining the exact data structures expected by the mobile app.
 */

// ============================================================================
// 1. USER TYPES
// ============================================================================

export interface MobileUser {
  id: number;
  name: string;
  email: string;
  postal_code: string;
  avatar: string;
  role: number;
}

export interface UserRegistrationData {
  name: string;
  email: string;
  password: string;
  postal_code: string;
}

export interface UserLoginData {
  email: string;
  password: string;
}

export interface UserProfileUpdateData {
  name: string;
  avatar?: string;
  postal_code?: string;
}

export interface PasswordChangeData {
  old_password: string;
  new_password: string;
}

export interface AccountDeletionData {
  reason: string;
  email: string;
}

// ============================================================================
// 2. BILL TYPES
// ============================================================================

export interface MobileBill {
  id: number;
  number: string;
  title: string;
  description: string;
  status: string;
  support_percentage: number;
  oppose_percentage: number;
  bookmarked: boolean;
  app_summary: string;
}

export interface MobileBillDetail extends MobileBill {
  vote_cast: string;
  support_percentage: number;
  oppose_percentage: number;
  bookmark: boolean;
}

export interface BillSupportData {
  support: boolean;
}

// ============================================================================
// 3. ISSUE TYPES
// ============================================================================

export interface MobileIssue {
  id: number;
  title: string;
  description: string;
  status: string;
  related_bill: number;
  support_percentage?: number;
  bookmarked?: boolean;
}

export interface IssueCreationData {
  bill_id: number;
  title: string;
  description: string;
}

export interface IssueSupportData {
  support: boolean;
}

export interface IssueDeletionRequestData {
  reason: string;
}

// ============================================================================
// 4. REPRESENTATIVE TYPES
// ============================================================================

export interface MobileRepresentative {
  id: number;
  name: string;
  constituency: string;
  contact_info: {
    email: string;
    phone: string;
  };
}

// ============================================================================
// 5. CHAT TYPES
// ============================================================================

export interface BillChatData {
  bill_id: number;
  message: string;
}

// ============================================================================
// 6. API RESPONSE TYPES
// ============================================================================

export interface MobileApiResponse<T = any> {
  success: boolean;
  data?: T;
  user?: MobileUser;
  token?: string;
  message?: string;
  issue?: MobileIssue;
  representative?: MobileRepresentative;
  summary?: string;
  response?: string;
}

export interface MobileApiListResponse<T> extends MobileApiResponse<T[]> {
  data: T[];
}

// ============================================================================
// 7. ERROR TYPES
// ============================================================================

export interface MobileApiError {
  success: false;
  message: string;
}

// ============================================================================
// 8. MOBILE APP API ENDPOINTS
// ============================================================================

export const MOBILE_APP_ENDPOINTS = {
  // User APIs
  REGISTER: '/app-auth/register',
  LOGIN: '/app-auth/login',
  PROFILE: '/app/v1/profile',
  UPDATE_PROFILE: '/app/v1/profile',
  CHANGE_PASSWORD: '/app/v1/change-password',
  DELETE_ACCOUNT: '/app/v1/delete-account',
  
  // Bills APIs
  BILLS_LIST: '/app/v1/bills',
  BILL_DETAIL: '/app/v1/bills/{bill_id}',
  BILL_SUPPORT: '/app/v1/bills/{bill_id}/support',
  BILL_BOOKMARK: '/app/v1/bills/{bill_id}/bookmark',
  
  // Issues APIs
  ISSUE_CREATE: '/app/v1/issues/create',
  ISSUE_SUPPORT: '/app/v1/issues/{issue_id}/support',
  ISSUE_BOOKMARK: '/app/v1/issues/{issue_id}/bookmark',
  ISSUE_DELETION_REQUEST: '/app/v1/issues/{issue_id}/request-deletion',
  
  // Representative APIs
  FIND_REPRESENTATIVE: '/app/v1/representatives',
  SEARCH_REPRESENTATIVES: '/app/v1/representatives/all',
  
  // Chat APIs
  GET_BILL_FOR_CHAT: '/app/v1/chat/get-bill',
  BILL_CHAT: '/app/v1/chat/bill-chat',
} as const;

// ============================================================================
// 9. MOBILE APP CONSTANTS
// ============================================================================

export const MOBILE_APP_CONSTANTS = {
  // User roles
  USER_ROLE_CONSUMER: 0,
  USER_ROLE_ENTERPRISE: 1,
  USER_ROLE_TEST: 2,
  
  // Bill statuses
  BILL_STATUS_ACTIVE: 'active',
  BILL_STATUS_INACTIVE: 'inactive',
  BILL_STATUS_PENDING: 'pending',
  
  // Issue statuses
  ISSUE_STATUS_OPEN: 'open',
  ISSUE_STATUS_CLOSED: 'closed',
  ISSUE_STATUS_PENDING: 'pending',
  
  // Vote types
  VOTE_TYPE_SUPPORT: 'support',
  VOTE_TYPE_OPPOSE: 'oppose',
  VOTE_TYPE_ABSTAIN: 'abstain',
} as const;

// ============================================================================
// 10. UTILITY TYPES
// ============================================================================

export type MobileAppEndpoint = typeof MOBILE_APP_ENDPOINTS[keyof typeof MOBILE_APP_ENDPOINTS];
export type MobileUserRole = typeof MOBILE_APP_CONSTANTS[keyof typeof MOBILE_APP_CONSTANTS];
export type BillStatus = typeof MOBILE_APP_CONSTANTS[keyof typeof MOBILE_APP_CONSTANTS];
export type IssueStatus = typeof MOBILE_APP_CONSTANTS[keyof typeof MOBILE_APP_CONSTANTS];
export type VoteType = typeof MOBILE_APP_CONSTANTS[keyof typeof MOBILE_APP_CONSTANTS];
