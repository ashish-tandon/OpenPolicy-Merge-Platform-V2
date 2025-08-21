/**
 * Government Level Icons
 * Custom SVG icons for different levels of government
 */

interface IconProps {
  className?: string;
}

export function FederalIcon({ className = "w-6 h-6" }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 100 100" fill="currentColor">
      {/* Parliament Building with Peace Tower */}
      <rect x="10" y="70" width="80" height="20" />
      <rect x="20" y="50" width="15" height="20" />
      <rect x="35" y="40" width="10" height="30" />
      <rect x="45" y="20" width="10" height="50" />
      <rect x="55" y="40" width="10" height="30" />
      <rect x="65" y="50" width="15" height="20" />
      
      {/* Peace Tower */}
      <rect x="47" y="10" width="6" height="10" />
      <polygon points="44,20 47,15 53,15 56,20" />
      
      {/* Flag */}
      <rect x="53" y="12" width="8" height="5" />
      <line x1="53" y1="12" x2="53" y2="20" stroke="currentColor" strokeWidth="1" />
    </svg>
  );
}

export function ProvincialIcon({ className = "w-6 h-6" }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 100 100" fill="currentColor">
      {/* Provincial Legislature Building */}
      <rect x="15" y="60" width="70" height="25" />
      <rect x="25" y="45" width="50" height="15" />
      <rect x="35" y="30" width="30" height="15" />
      
      {/* Dome */}
      <ellipse cx="50" cy="30" rx="20" ry="10" />
      <rect x="48" y="20" width="4" height="10" />
      
      {/* Columns */}
      <rect x="20" y="45" width="3" height="15" />
      <rect x="30" y="45" width="3" height="15" />
      <rect x="40" y="45" width="3" height="15" />
      <rect x="57" y="45" width="3" height="15" />
      <rect x="67" y="45" width="3" height="15" />
      <rect x="77" y="45" width="3" height="15" />
    </svg>
  );
}

export function MunicipalIcon({ className = "w-6 h-6" }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 100 100" fill="currentColor">
      {/* City Hall */}
      <rect x="20" y="70" width="60" height="20" />
      <rect x="30" y="50" width="40" height="20" />
      <rect x="40" y="35" width="20" height="15" />
      
      {/* Clock Tower */}
      <rect x="45" y="25" width="10" height="10" />
      <circle cx="50" cy="30" r="4" fill="none" stroke="currentColor" strokeWidth="1" />
      <line x1="50" y1="30" x2="50" y2="27" stroke="currentColor" strokeWidth="1" />
      <line x1="50" y1="30" x2="52" y2="30" stroke="currentColor" strokeWidth="1" />
      
      {/* Windows */}
      <rect x="35" y="55" width="4" height="6" fill="white" />
      <rect x="42" y="55" width="4" height="6" fill="white" />
      <rect x="54" y="55" width="4" height="6" fill="white" />
      <rect x="61" y="55" width="4" height="6" fill="white" />
      
      {/* Door */}
      <rect x="47" y="75" width="6" height="10" fill="white" />
    </svg>
  );
}

export function RepresentativeIcon({ className = "w-6 h-6" }: IconProps) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
    </svg>
  );
}

export function BillIcon({ className = "w-6 h-6" }: IconProps) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  );
}

export function VoteIcon({ className = "w-6 h-6" }: IconProps) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
        d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
    </svg>
  );
}

export function JurisdictionIcon({ className = "w-6 h-6" }: IconProps) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
    </svg>
  );
}
