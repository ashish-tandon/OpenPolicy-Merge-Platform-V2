import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'For Government - Data Contribution | OpenParliament.ca',
  description: 'Learn how to contribute your municipality\'s elected official data to Represent using our standardized CSV schema.',
};

export default function RepresentGovernmentPage() {
  // Following FUNDAMENTAL RULE: Adapted from legacy/represent-canada/finder/templates/government.html
  const municipalities = [
    { name: 'City of Ottawa', logo: 'ottawa.png', width: 119, height: 50 },
    { name: 'City of Vancouver', logo: 'vancouver.png', width: 129, height: 50 },
    { name: 'City of Guelph', logo: 'guelph.png', width: 168, height: 50 },
    { name: 'Town of Oakville', logo: 'oakville.png', width: 78, height: 50 },
    { name: 'City of Welland', logo: 'welland.png', width: 43, height: 50 },
    { name: 'City of London', logo: 'london.png', width: 41, height: 50 },
    { name: 'City of Langley', logo: 'langley.png', width: 123, height: 50 },
    { name: 'City of Surrey', logo: 'surrey.png', width: 137, height: 50 },
    { name: 'Strathcona County', logo: 'strathcona-county.png', width: 278, height: 50 },
    { name: 'City of Grande Prairie', logo: 'grande-prairie.png', width: 123, height: 50 },
    { name: 'City of Kelowna', logo: 'kelowna.png', width: 68, height: 50 },
    { name: 'City of Victoria', logo: 'victoria.png', width: 117, height: 50 },
    { name: 'City of Kitchener', logo: 'kitchener.png', width: 70, height: 50 },
    { name: 'City of Windsor', logo: 'windsor.png', width: 278, height: 50 },
    { name: 'Region of Peel', logo: 'peel.png', width: 171, height: 50 },
    { name: 'City of Burlington', logo: 'burlington.png', width: 196, height: 50 },
    { name: 'Niagara Region', logo: 'niagara.png', width: 290, height: 40 },
    { name: 'City of Brampton', logo: 'brampton.png', width: 151, height: 50 },
    { name: 'City of Waterloo', logo: 'waterloo.png', width: 138, height: 50 },
    { name: 'City of Toronto', logo: 'toronto.png', width: 159, height: 50 },
    { name: 'City of Greater Sudbury', logo: 'greater-sudbury.png', width: 192, height: 50 },
    { name: 'City of Kingston', logo: 'kingston.png', width: 52, height: 50 },
    { name: 'Region of Waterloo', logo: 'waterloo-region.png', width: 59, height: 50 },
    { name: 'Ville de Montréal', logo: 'montreal.png', width: 233, height: 50 },
    { name: 'Town of Grimsby', logo: 'grimsby.png', width: 32, height: 50 },
    { name: 'Town of Lincoln', logo: 'lincoln.png', width: 173, height: 50 },
    { name: 'Ville de Laval', logo: 'laval.png', width: 143, height: 50 },
    { name: 'City of St. Catharines', logo: 'st-catharines.png', width: 225, height: 50 },
    { name: 'Grande Prairie County No. 1', logo: 'grande-prairie-county-no-1.png', width: 60, height: 50 },
    { name: 'Town of Newmarket', logo: 'newmarket.png', width: 75, height: 50 },
    { name: 'City of Saint John', logo: 'saint-john.png', width: 59, height: 50 },
    { name: 'City of Cambridge', logo: 'cambridge.png', width: 166, height: 50 },
    { name: 'City of Moncton', logo: 'moncton.png', width: 95, height: 50 },
    { name: 'City of Saskatoon', logo: 'saskatoon.png', width: 222, height: 50 },
    { name: 'City of New Westminster', logo: 'new-westminster.png', width: 183, height: 50 },
  ];

  return (
    <div className="content-container py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header - Adapted from legacy template */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white rounded-lg p-8 mb-12">
          <h1 className="text-4xl font-bold text-center">
            Adding your elected officials to Represent is easy.
          </h1>
        </div>

        {/* Instructions - Adapted from legacy template */}
        <section className="mb-12">
          <div className="bg-white border border-gray-200 rounded-lg p-8">
            <ol className="space-y-6 text-lg">
              <li>
                <p className="mb-4">
                  Download our{' '}
                  <a 
                    href="/represent/template.csv" 
                    className="text-blue-600 hover:underline font-semibold"
                  >
                    spreadsheet template
                  </a>
                  , or create your own with the columns below. You may omit or leave columns blank. 
                  The most important are in <strong>bold</strong>.
                </p>
                
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold mb-4">Required Fields</h3>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <li><strong>District name</strong> (if your municipality is divided into wards, districts or divisions – <code>Ward 2</code> for example)</li>
                    <li><strong>District ID</strong> (if your wards have identifiers as well as names – <code>2</code> for example)</li>
                    <li><strong>Primary role</strong> (<code>Mayor</code> or <code>Councillor</code> for most municipalities)</li>
                    <li><strong>First name</strong></li>
                    <li><strong>Last name</strong></li>
                    <li><strong>Email</strong></li>
                    <li><strong>Photo URL</strong> (a link to a photo of the elected official)</li>
                  </ul>
                  
                  <h3 className="text-lg font-semibold mb-4 mt-6">Optional Fields</h3>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <li>Gender (<code>M</code> or <code>F</code> for example)</li>
                    <li>Party name</li>
                    <li>Source URL (a link to the elected official&apos;s profile on your municipal website)</li>
                    <li>Website (a link to the elected official&apos;s own website)</li>
                    <li>Address line 1</li>
                    <li>Address line 2</li>
                    <li>Locality</li>
                    <li>Province (<code>AB</code>, <code>BC</code>, <code>MB</code>, <code>NB</code>, <code>NL</code>, <code>NS</code>, <code>NT</code>, <code>NU</code>, <code>ON</code>, <code>PE</code>, <code>QC</code>, <code>SK</code> or <code>YT</code>)</li>
                    <li>Postal code (<code>A1A 1A1</code> for example)</li>
                    <li>Phone (<code>1 555 555-5555 Ext. 5555</code> for example)</li>
                    <li>Fax</li>
                    <li>Cell</li>
                                      <li>Facebook (a link to the elected official&apos;s Facebook page)</li>
                  <li>Twitter (a link to the elected official&apos;s Twitter page)</li>
                  </ul>
                </div>
              </li>
              
              <li>
                <p>
                  If you would like to specify multiple addresses or numbers, add a parenthesized label to the column header, 
                  e.g. <code>Phone (home)</code>.
                </p>
              </li>
              
              <li>
                <p>Save the spreadsheet in the CSV file format. Microsoft Excel and other programs can do this.</p>
              </li>
              
              <li>
                <p>Upload the CSV file to your municipal website. You may need to ask your webmaster.</p>
              </li>
              
              <li>
                <p>
                  <a 
                    href="mailto:represent@opennorth.ca" 
                    className="text-blue-600 hover:underline font-semibold"
                  >
                    Email us
                  </a>{' '}
                  the link to the spreadsheet, and we&apos;ll quickly add the information to Represent.
                </p>
              </li>
              
              <li>
                <p>
                  If you have an open data catalog, you may specify that &quot;This dataset conforms to the{' '}
                  <Link href="/represent/government" className="text-blue-600 hover:underline font-semibold">
                    Represent CSV Schema
                  </Link>{' '}
                  for elected officials&apos; contact information.&quot;
                </p>
              </li>
            </ol>
            
            <div className="mt-8 p-6 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-800">
                <strong>Now, all you have to do is update the spreadsheet when information changes. We&apos;ll automatically import those changes.</strong>
              </p>
              <p className="text-green-700 mt-2">
                If you have any questions, please do not hesitate to{' '}
                <a 
                  href="mailto:represent@opennorth.ca" 
                  className="text-green-600 hover:underline font-semibold"
                >
                  contact us
                </a>.
              </p>
            </div>
          </div>
        </section>

        {/* Municipal Adoption - Adapted from legacy template */}
        <section className="mb-12">
          <div className="bg-white border border-gray-200 rounded-lg p-8">
            <h2 className="text-3xl font-bold text-op-dark mb-6 text-center">
              Thanks to the following municipalities for providing information as CSV!
            </h2>
            
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
              {municipalities.map((municipality, index) => (
                <div key={index} className="text-center">
                  <div className="w-full h-16 bg-gray-100 rounded-lg flex items-center justify-center mb-2">
                    <div className="w-12 h-12 bg-gray-300 rounded mx-auto"></div>
                  </div>
                  <p className="text-sm text-gray-600">{municipality.name}</p>
                </div>
              ))}
            </div>
            
            <div className="mt-8 text-center">
              <p className="text-gray-600 mb-4">
                This project was supported by a grant from the Canadian Internet Registration Authority.
              </p>
              <Link 
                href="/represent"
                className="inline-flex items-center px-6 py-3 bg-op-blue text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Learn more about Represent
              </Link>
            </div>
          </div>
        </section>

        {/* CSV Template Download */}
        <section className="mb-12">
          <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-8 text-center">
            <h2 className="text-2xl font-bold text-op-dark mb-4">
              Get Started with Our CSV Template
            </h2>
            <p className="text-gray-600 mb-6">
              Download our standardized template to ensure your data meets our requirements.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <a 
                href="/represent/template.csv"
                download
                className="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
              >
                Download CSV Template
              </a>
              <Link 
                href="/represent/api"
                className="bg-op-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                View API Documentation
              </Link>
              <a 
                href="mailto:represent@opennorth.ca"
                className="border border-op-blue text-op-blue px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                Contact Support
              </a>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
