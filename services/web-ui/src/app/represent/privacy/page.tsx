import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy - Represent | OpenParliament.ca',
  description: 'Privacy policy for the Represent electoral data platform, outlining how we collect, use, and protect your information.',
};

export default function RepresentPrivacyPage() {
  // Following FUNDAMENTAL RULE: Adapted from legacy/represent-canada/finder/templates/privacy.html
  return (
    <div className="content-container py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header - Adapted from legacy template */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-lg p-8 mb-12">
          <h1 className="text-4xl font-bold text-center">Privacy Policy</h1>
        </div>

        {/* Privacy Content - Adapted from legacy template */}
        <section className="bg-white border border-gray-200 rounded-lg p-8">
          <div className="prose max-w-none">
            <p className="text-gray-600 mb-6">May 12, 2012</p>

            <p className="text-lg mb-6">
              We care about your privacy. If you have any questions about this policy, feel free to{' '}
              <a 
                href="mailto:represent@opennorth.ca" 
                className="text-blue-600 hover:underline font-semibold"
              >
                contact us
              </a>.
            </p>

            <h2 className="text-2xl font-bold text-op-dark mb-4">Information we collect</h2>

            <ul className="space-y-4 mb-8">
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-600 rounded-full mt-3 mr-3 flex-shrink-0"></span>
                <div>
                  <strong>Log information</strong> - When you use this website, our servers automatically record information 
                  that your browser sends whenever you visit a website. These server logs may include information such as 
                  your web request, IP address, browser type, browser language, and the date and time of your request. 
                  We use server logs to track usage trends and to protect our services.
                </div>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-600 rounded-full mt-3 mr-3 flex-shrink-0"></span>
                <div>
                  <strong>User communications</strong> - When you send email or other communication to us, we may retain 
                  those communications in order to process your enquiries, respond to your requests, and improve our services.
                </div>
              </li>
            </ul>

            <h2 className="text-2xl font-bold text-op-dark mb-4">Information security</h2>

            <p className="text-lg mb-8">
              We do not share or sell any information that may potentially identify individuals, such as IP addresses.
            </p>

            <h2 className="text-2xl font-bold text-op-dark mb-4">Changes to this policy</h2>

            <p className="text-lg">
              Please note that this privacy policy may change from time to time. We will post any policy changes on this page.
            </p>
          </div>
        </section>

        {/* Contact Section */}
        <section className="mt-12 text-center">
          <div className="bg-gray-50 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-op-dark mb-4">
              Questions about Privacy?
            </h2>
            <p className="text-gray-600 mb-6">
              If you have concerns about how we handle your data or would like to know more about our privacy practices, 
              please don&apos;t hesitate to reach out.
            </p>
            <a 
              href="mailto:represent@opennorth.ca"
              className="inline-flex items-center px-6 py-3 bg-op-blue text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Contact Our Privacy Team
            </a>
          </div>
        </section>
      </div>
    </div>
  );
}
