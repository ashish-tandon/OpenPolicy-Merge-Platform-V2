/**
 * Party Color Service
 * 
 * Centralized service for managing political party colors.
 * This consolidates party color logic to ensure consistency across the application.
 */

export class PartyColorService {
  // Define party colors as a static configuration
  private static readonly PARTY_COLORS: Record<string, string> = {
    // Federal parties
    'liberal': 'bg-red-600',
    'conservative': 'bg-blue-600',
    'ndp': 'bg-orange-600',
    'bloc': 'bg-cyan-600',
    'green': 'bg-green-600',
    'peoples-party': 'bg-purple-600',
    
    // Alternative names
    'liberal-party': 'bg-red-600',
    'conservative-party': 'bg-blue-600',
    'new-democratic-party': 'bg-orange-600',
    'bloc-quebecois': 'bg-cyan-600',
    'green-party': 'bg-green-600',
    
    // Default
    'independent': 'bg-gray-600',
    'default': 'bg-gray-600'
  };

  // Text colors for better contrast
  private static readonly PARTY_TEXT_COLORS: Record<string, string> = {
    'liberal': 'text-red-600',
    'conservative': 'text-blue-600',
    'ndp': 'text-orange-600',
    'bloc': 'text-cyan-600',
    'green': 'text-green-600',
    'peoples-party': 'text-purple-600',
    'independent': 'text-gray-600',
    'default': 'text-gray-600'
  };

  /**
   * Get the background color class for a party
   */
  static getPartyColor(partySlug: string): string {
    const normalized = partySlug.toLowerCase().trim();
    return this.PARTY_COLORS[normalized] || this.PARTY_COLORS['default'];
  }

  /**
   * Get the text color class for a party
   */
  static getPartyTextColor(partySlug: string): string {
    const normalized = partySlug.toLowerCase().trim();
    return this.PARTY_TEXT_COLORS[normalized] || this.PARTY_TEXT_COLORS['default'];
  }

  /**
   * Get the hex color value for a party (for charts, etc.)
   */
  static getPartyHexColor(partySlug: string): string {
    const hexColors: Record<string, string> = {
      'liberal': '#DC2626',      // red-600
      'conservative': '#2563EB',  // blue-600
      'ndp': '#EA580C',          // orange-600
      'bloc': '#0891B2',         // cyan-600
      'green': '#16A34A',        // green-600
      'peoples-party': '#9333EA', // purple-600
      'independent': '#4B5563',   // gray-600
      'default': '#4B5563'
    };

    const normalized = partySlug.toLowerCase().trim();
    return hexColors[normalized] || hexColors['default'];
  }

  /**
   * Get party display name from slug
   */
  static getPartyDisplayName(partySlug: string): string {
    const displayNames: Record<string, string> = {
      'liberal': 'Liberal Party',
      'conservative': 'Conservative Party',
      'ndp': 'New Democratic Party',
      'bloc': 'Bloc Québécois',
      'green': 'Green Party',
      'peoples-party': 'People\'s Party',
      'independent': 'Independent'
    };

    const normalized = partySlug.toLowerCase().trim();
    return displayNames[normalized] || partySlug;
  }

  /**
   * Check if a party slug is recognized
   */
  static isKnownParty(partySlug: string): boolean {
    const normalized = partySlug.toLowerCase().trim();
    return normalized in this.PARTY_COLORS && normalized !== 'default';
  }
}