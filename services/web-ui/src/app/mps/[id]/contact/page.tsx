import { notFound } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import { Metadata } from 'next';

interface ContactPageProps {
  params: Promise<{
    id: string;
  }>;
}

export async function generateMetadata({ params }: ContactPageProps): Promise<Metadata> {
  const { id } = await params;
  try {
    const mp = await api.getMember(id);
    
    return {
      title: `Contact ${mp.full_name} | OpenPolicy`,
      description: `Contact information and how to reach ${mp.full_name}, MP for ${mp.constituency || 'Canada'}`,
    };
  } catch (_error) {
    return {
      title: 'Contact MP | OpenPolicy',
      description: 'Contact your Member of Parliament',
    };
  }
}

export default async function ContactPage({ params }: ContactPageProps) {
  const { id } = await params;
  try {
    const mp = await api.getMember(id);

    return (
      <div className="content-container py-8">
        {/* Breadcrumb Navigation */}
        <nav className="mb-6">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li>
              <Link href="/mps" className="hover:text-op-blue transition-colors">
                MPs
              </Link>
            </li>
            <li className="text-gray-400">/</li>
            <li>
              <Link href={`/mps/${mp.slug}`} className="hover:text-op-blue transition-colors">
                {mp.full_name}
              </Link>
            </li>
            <li className="text-gray-400">/</li>
            <li className="text-gray-900 font-medium">Contact</li>
          </ol>
        </nav>

        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-op-dark mb-8">
            Contact {mp.full_name}
          </h1>

          {/* Contact Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Hill Office */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-op-dark mb-4">
                Hill Office
              </h2>
              <div className="space-y-3 text-sm">
                {mp.hill_phone && (
                  <div>
                    <strong className="text-gray-700">Phone:</strong>{' '}
                    <a href={`tel:${mp.hill_phone}`} className="text-op-blue hover:underline">
                      {mp.hill_phone}
                    </a>
                  </div>
                )}
                {mp.hill_fax && (
                  <div>
                    <strong className="text-gray-700">Fax:</strong>{' '}
                    <span>{mp.hill_fax}</span>
                  </div>
                )}
                {mp.email && (
                  <div>
                    <strong className="text-gray-700">Email:</strong>{' '}
                    <a href={`mailto:${mp.email}`} className="text-op-blue hover:underline">
                      {mp.email}
                    </a>
                  </div>
                )}
                {mp.hill_address && (
                  <div>
                    <strong className="text-gray-700">Address:</strong>
                    <address className="not-italic mt-1">
                      {mp.hill_address}
                    </address>
                  </div>
                )}
              </div>
            </div>

            {/* Constituency Office */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-op-dark mb-4">
                Constituency Office
              </h2>
              <div className="space-y-3 text-sm">
                {mp.constituency_phone && (
                  <div>
                    <strong className="text-gray-700">Phone:</strong>{' '}
                    <a href={`tel:${mp.constituency_phone}`} className="text-op-blue hover:underline">
                      {mp.constituency_phone}
                    </a>
                  </div>
                )}
                {mp.constituency_fax && (
                  <div>
                    <strong className="text-gray-700">Fax:</strong>{' '}
                    <span>{mp.constituency_fax}</span>
                  </div>
                )}
                {mp.constituency_address && (
                  <div>
                    <strong className="text-gray-700">Address:</strong>
                    <address className="not-italic mt-1">
                      {mp.constituency_address}
                    </address>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Tips for Contacting */}
          <div className="mt-8 bg-blue-50 rounded-lg p-6">
            <h2 className="text-xl font-bold text-op-dark mb-4">
              Tips for Contacting Your MP
            </h2>
            <ul className="space-y-2 text-sm">
              <li className="flex items-start">
                <span className="text-op-blue mr-2">•</span>
                <span>Be clear and concise in your message. State your main point at the beginning.</span>
              </li>
              <li className="flex items-start">
                <span className="text-op-blue mr-2">•</span>
                <span>Include your full name and address to show you're a constituent.</span>
              </li>
              <li className="flex items-start">
                <span className="text-op-blue mr-2">•</span>
                <span>Reference specific bills or issues you're concerned about.</span>
              </li>
              <li className="flex items-start">
                <span className="text-op-blue mr-2">•</span>
                <span>Be respectful and professional in your communication.</span>
              </li>
              <li className="flex items-start">
                <span className="text-op-blue mr-2">•</span>
                <span>Follow up if you don't receive a response within a few weeks.</span>
              </li>
            </ul>
          </div>

          {/* Social Media */}
          {(mp.twitter_username || mp.facebook_username) && (
            <div className="mt-8 bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-op-dark mb-4">
                Social Media
              </h2>
              <div className="flex space-x-4">
                {mp.twitter_username && (
                  <a
                    href={`https://twitter.com/${mp.twitter_username}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center text-op-blue hover:underline"
                  >
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                    </svg>
                    @{mp.twitter_username}
                  </a>
                )}
                {mp.facebook_username && (
                  <a
                    href={`https://facebook.com/${mp.facebook_username}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center text-op-blue hover:underline"
                  >
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                    </svg>
                    Facebook
                  </a>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  } catch (error) {
    console.error('Error loading MP contact info:', error);
    notFound();
  }
}