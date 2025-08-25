/**
 * Postal Code Service
 * 
 * Provides methods for interacting with the postal code API.
 * This service consolidates all postal code lookup functionality.
 */

interface PostalCodeResponse {
  postcode: string;
  representatives: Array<{
    name: string;
    party: string;
    riding: string;
    level: string;
    url: string;
    photo_url?: string;
    email?: string;
    phone?: string;
  }>;
  total_count: number;
  source: string;
  timestamp: string;
}

export class PostalCodeService {
  private static API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

  /**
   * Find MP by postal code using the RESTful API endpoint
   */
  static async findMPByPostalCode(postalCode: string): Promise<PostalCodeResponse | null> {
    try {
      const normalizedCode = postalCode.toUpperCase().replace(/\s/g, '');
      
      const response = await fetch(
        `${this.API_BASE_URL}/postal-codes/${normalizedCode}/members`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      return data as PostalCodeResponse;
    } catch (error) {
      console.error('Error fetching MP by postal code:', error);
      throw error;
    }
  }

  /**
   * Validate Canadian postal code format
   */
  static isValidPostalCode(postalCode: string): boolean {
    const normalized = postalCode.toUpperCase().replace(/\s/g, '');
    const regex = /^[A-Z]\d[A-Z]\d[A-Z]\d$/;
    return regex.test(normalized);
  }

  /**
   * Format postal code for display (add space in middle)
   */
  static formatPostalCode(postalCode: string): string {
    const normalized = postalCode.toUpperCase().replace(/\s/g, '');
    if (normalized.length === 6) {
      return `${normalized.slice(0, 3)} ${normalized.slice(3)}`;
    }
    return postalCode;
  }
}