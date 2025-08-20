import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import { AccessibilityProvider, SkipToContent } from '@/components/AccessibilityProvider'
import { ErrorBoundary } from '@/components/ErrorBoundary'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'OpenParliament.ca - Canadian Parliamentary Data',
  description: 'Track Canadian MPs, bills, debates, and committees. OpenParliament.ca is your window into the House of Commons.',
  icons: {
    icon: '/favicon.png',
  },
  // Accessibility metadata
  openGraph: {
    title: 'OpenParliament.ca',
    description: 'Track Canadian MPs, bills, debates, and committees',
    locale: 'en_CA',
    type: 'website',
  },
  // Improve SEO and accessibility
  alternates: {
    canonical: 'https://openparliament.ca',
    languages: {
      'en-CA': 'https://openparliament.ca',
      'fr-CA': 'https://openparliament.ca/fr',
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        {/* Preconnect to API for better performance */}
        <link rel="preconnect" href={process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'} />
        
        {/* Theme color for mobile browsers */}
        <meta name="theme-color" content="#183A54" />
        
        {/* Viewport for responsive design */}
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
      </head>
      <body className={`${inter.className} bg-op-gray antialiased`}>
        <ErrorBoundary>
          <AccessibilityProvider>
            {/* Skip to main content link for keyboard users */}
            <SkipToContent />
            
            {/* Main navigation */}
            <Navbar />
            
            {/* Main content with proper landmark */}
            <main id="main-content" className="min-h-screen focus:outline-none" tabIndex={-1}>
              {children}
            </main>
            
            {/* Footer with proper landmark */}
            <Footer />
          </AccessibilityProvider>
        </ErrorBoundary>
        
        {/* Add CSS for different font sizes */}
        <style jsx global>{`
          html[data-font-size="large"] {
            font-size: 18px;
          }
          
          html[data-font-size="extra-large"] {
            font-size: 20px;
          }
          
          /* Respect user's motion preferences */
          @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
              animation-duration: 0.01ms !important;
              animation-iteration-count: 1 !important;
              transition-duration: 0.01ms !important;
              scroll-behavior: auto !important;
            }
          }
          
          /* High contrast mode support */
          @media (prefers-contrast: high) {
            .bg-op-blue {
              background-color: #000080;
            }
            
            .text-op-blue {
              color: #0000FF;
            }
            
            .border-gray-200 {
              border-color: #000000;
            }
          }
          
          /* Focus visible for keyboard navigation */
          :focus-visible {
            outline: 2px solid #2563eb;
            outline-offset: 2px;
          }
          
          /* Print styles */
          @media print {
            nav,
            footer,
            .no-print {
              display: none !important;
            }
            
            main {
              width: 100% !important;
              margin: 0 !important;
              padding: 0 !important;
            }
          }
        `}</style>
      </body>
    </html>
<<<<<<< Current (Your changes)
  );
}
=======
  )
}
>>>>>>> Incoming (Background Agent changes)
