'use client';

import { useState, useEffect } from 'react';

interface BillTextProps {
  billId: number;
}

export default function BillText({ billId }: BillTextProps) {
  const [loading, setLoading] = useState(false);
  const [textAvailable, setTextAvailable] = useState(true);
  const [selectedVersion, setSelectedVersion] = useState('current');

  // In production, this would fetch the actual bill text
  useEffect(() => {
    // Placeholder for fetching bill text
  }, [billId]);

  if (loading) {
    return <div className="text-gray-500">Loading bill text...</div>;
  }

  if (!textAvailable) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500 mb-4">
          The full text of this bill is not available in our database.
        </p>
        <a
          href="https://www.parl.ca/legisinfo"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-op-blue hover:underline"
        >
          View on LEGISinfo
          <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      </div>
    );
  }

  return (
    <div>
      {/* Version Selector */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <label className="text-sm font-medium text-gray-700 mr-2">
            Version:
          </label>
          <select
            value={selectedVersion}
            onChange={(e) => setSelectedVersion(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue text-sm"
          >
            <option value="current">Current Version</option>
            <option value="first-reading">As First Read</option>
            <option value="second-reading">After Second Reading</option>
            <option value="committee">After Committee</option>
          </select>
        </div>
        <div className="flex items-center gap-4">
          <button className="text-sm text-op-blue hover:underline">
            Download PDF
          </button>
          <button className="text-sm text-op-blue hover:underline">
            Print
          </button>
        </div>
      </div>

      {/* Bill Text Display */}
      <div className="prose max-w-none">
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-bold mb-2">Summary</h3>
          <p className="text-gray-700">
            This enactment amends the Criminal Code to repeal certain mandatory minimum penalties, 
            to allow for judicial review of any prohibition order relating to the possession of 
            firearms and other regulated items, and to require that peace officers and other 
            authorized persons consider whether other measures would be adequate before laying 
            an information for certain administration of justice offences.
          </p>
        </div>

        <div className="space-y-6">
          <section>
            <h3 className="text-lg font-bold mb-3">Part I - Amendments to the Criminal Code</h3>
            
            <div className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Section 1</h4>
                <p className="text-gray-700">
                  1. Section 85 of the Criminal Code is amended by replacing subsection (3) with the following:
                </p>
                <blockquote className="border-l-4 border-gray-300 pl-4 ml-4 mt-2 text-gray-600">
                  (3) Every person who commits an offence under subsection (1) or (2) is guilty of an indictable 
                  offence and liable to imprisonment for a term not exceeding 14 years.
                </blockquote>
              </div>

              <div>
                <h4 className="font-medium mb-2">Section 2</h4>
                <p className="text-gray-700">
                  2. Subsection 95(2) of the Act is replaced by the following:
                </p>
                <blockquote className="border-l-4 border-gray-300 pl-4 ml-4 mt-2 text-gray-600">
                  (2) Every person who commits an offence under subsection (1) is guilty of an indictable offence 
                  and liable to imprisonment for a term not exceeding 10 years.
                </blockquote>
              </div>
            </div>
          </section>

          <section>
            <h3 className="text-lg font-bold mb-3">Part II - Coming into Force</h3>
            <p className="text-gray-700">
              This Act comes into force on a day to be fixed by order of the Governor in Council.
            </p>
          </section>
        </div>
      </div>

      {/* Navigation */}
      <div className="mt-8 pt-6 border-t border-gray-200 flex justify-between">
        <button className="text-op-blue hover:underline">
          ← Previous Section
        </button>
        <button className="text-op-blue hover:underline">
          Next Section →
        </button>
      </div>
    </div>
  );
}
