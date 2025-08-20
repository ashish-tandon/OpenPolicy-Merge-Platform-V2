import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white mt-12">
      <div className="content-container py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About Section */}
          <div>
            <h3 className="font-bold mb-4">About OpenParliament</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/about" className="text-gray-300 hover:text-white">About Us</Link></li>
              <li><Link href="/api" className="text-gray-300 hover:text-white">API Documentation</Link></li>
              <li><Link href="/downloads" className="text-gray-300 hover:text-white">Bulk Downloads</Link></li>
              <li><a href="https://github.com/openparlca" className="text-gray-300 hover:text-white">GitHub</a></li>
            </ul>
          </div>

          {/* Parliamentary Links */}
          <div>
            <h3 className="font-bold mb-4">Parliamentary Data</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/mps" className="text-gray-300 hover:text-white">Members of Parliament</Link></li>
              <li><Link href="/bills" className="text-gray-300 hover:text-white">Bills & Legislation</Link></li>
              <li><Link href="/debates" className="text-gray-300 hover:text-white">Debates & Hansard</Link></li>
              <li><Link href="/committees" className="text-gray-300 hover:text-white">Committees</Link></li>
            </ul>
          </div>

          {/* External Links */}
          <div>
            <h3 className="font-bold mb-4">External Resources</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="https://www.ourcommons.ca" className="text-gray-300 hover:text-white">House of Commons</a></li>
              <li><a href="https://www.parl.ca/legisinfo" className="text-gray-300 hover:text-white">LEGISinfo</a></li>
              <li><a href="https://www.elections.ca" className="text-gray-300 hover:text-white">Elections Canada</a></li>
              <li><a href="https://represent.opennorth.ca" className="text-gray-300 hover:text-white">Represent API</a></li>
            </ul>
          </div>

          {/* Contact & Social */}
          <div>
            <h3 className="font-bold mb-4">Stay Connected</h3>
            <ul className="space-y-2 text-sm">
              <li><Link href="/alerts" className="text-gray-300 hover:text-white">Email Alerts</Link></li>
              <li><Link href="/feeds/rss" className="text-gray-300 hover:text-white">RSS Feeds</Link></li>
              <li><a href="https://twitter.com/openparlca" className="text-gray-300 hover:text-white">Twitter</a></li>
              <li><Link href="/contact" className="text-gray-300 hover:text-white">Contact Us</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-700 text-center text-sm text-gray-400">
          <p>© 2025 OpenParliament.ca. An open-source project.</p>
          <p className="mt-2">
            Data from the <a href="https://www.ourcommons.ca" className="text-gray-300 hover:text-white">House of Commons</a> under the 
            <a href="https://www.ourcommons.ca/en/open-data" className="text-gray-300 hover:text-white"> Open Government Licence - Canada</a>.
          </p>
        </div>
      </div>
    </footer>
  );
}
