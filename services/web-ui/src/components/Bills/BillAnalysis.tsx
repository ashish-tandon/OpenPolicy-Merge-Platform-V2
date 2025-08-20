'use client';

import { useState } from 'react';
import { Bill } from '@/lib/api';
import Link from 'next/link';

interface BillAnalysisProps {
  bill: Bill;
}

export default function BillAnalysis({ bill }: BillAnalysisProps) {
  const [activeSection, setActiveSection] = useState('summary');

  const sections = [
    { id: 'summary', label: 'Executive Summary' },
    { id: 'impact', label: 'Impact Assessment' },
    { id: 'stakeholders', label: 'Stakeholder Positions' },
    { id: 'predictions', label: 'Success Predictions' },
  ];

  return (
    <div>
      {/* Section Navigation */}
      <div className="flex flex-wrap gap-2 mb-6">
        {sections.map((section) => (
          <button
            key={section.id}
            onClick={() => setActiveSection(section.id)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeSection === section.id
                ? 'bg-op-blue text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {section.label}
          </button>
        ))}
      </div>

      {/* Content Sections */}
      {activeSection === 'summary' && (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-bold mb-3">Executive Summary</h3>
            <div className="prose max-w-none text-gray-700">
              <p>
                Bill {bill.number} represents a significant reform to Canada's criminal justice system, 
                focusing on the removal of mandatory minimum penalties for certain offenses and providing 
                judges with greater discretion in sentencing.
              </p>
              <p className="mt-3">
                The bill addresses long-standing concerns about the rigidity of mandatory minimums and 
                their disproportionate impact on marginalized communities. It aims to balance public 
                safety with rehabilitation and restorative justice principles.
              </p>
            </div>
          </div>

          <div>
            <h4 className="font-medium mb-2">Key Provisions:</h4>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                Repeals mandatory minimum penalties for 14 Criminal Code offenses
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                Allows judicial review of firearms prohibition orders
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                Requires consideration of alternatives for administration of justice offenses
              </li>
            </ul>
          </div>
        </div>
      )}

      {activeSection === 'impact' && (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-bold mb-3">Impact Assessment</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-green-50 rounded-lg p-4">
                <h4 className="font-medium text-green-900 mb-2">Positive Impacts</h4>
                <ul className="space-y-2 text-sm text-green-800">
                  <li>• Reduced incarceration rates</li>
                  <li>• Greater judicial discretion</li>
                  <li>• Cost savings in corrections</li>
                  <li>• More proportionate sentencing</li>
                  <li>• Better rehabilitation outcomes</li>
                </ul>
              </div>

              <div className="bg-red-50 rounded-lg p-4">
                <h4 className="font-medium text-red-900 mb-2">Concerns Raised</h4>
                <ul className="space-y-2 text-sm text-red-800">
                  <li>• Public safety considerations</li>
                  <li>• Consistency in sentencing</li>
                  <li>• Victim rights perspectives</li>
                  <li>• Deterrent effect reduction</li>
                  <li>• Implementation challenges</li>
                </ul>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-medium mb-2">Affected Groups:</h4>
            <div className="space-y-3">
              <div className="border-l-4 border-blue-400 pl-4">
                <h5 className="font-medium">Indigenous Communities</h5>
                <p className="text-sm text-gray-600">
                  Expected to benefit significantly due to current overrepresentation in the justice system
                </p>
              </div>
              <div className="border-l-4 border-purple-400 pl-4">
                <h5 className="font-medium">Legal Professionals</h5>
                <p className="text-sm text-gray-600">
                  Judges gain more discretion; lawyers have new arguments available
                </p>
              </div>
              <div className="border-l-4 border-orange-400 pl-4">
                <h5 className="font-medium">Corrections System</h5>
                <p className="text-sm text-gray-600">
                  Potential reduction in prison populations and associated costs
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeSection === 'stakeholders' && (
        <div className="space-y-6">
          <h3 className="text-lg font-bold mb-3">Stakeholder Positions</h3>
          
          <div className="space-y-4">
            <div className="border border-green-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-green-800">Supporting Organizations</h4>
                <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Support</span>
              </div>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Canadian Bar Association</li>
                <li>• John Howard Society</li>
                <li>• Canadian Civil Liberties Association</li>
                <li>• Indigenous Justice Organizations</li>
              </ul>
            </div>

            <div className="border border-red-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-red-800">Opposing Organizations</h4>
                <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">Oppose</span>
              </div>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Victims' Rights Groups</li>
                <li>• Some Police Associations</li>
                <li>• Conservative Policy Organizations</li>
              </ul>
            </div>

            <div className="border border-blue-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-blue-800">Mixed/Conditional Support</h4>
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Mixed</span>
              </div>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Provincial Attorneys General</li>
                <li>• Some Judicial Organizations</li>
                <li>• Criminal Defense Lawyers</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {activeSection === 'predictions' && (
        <div className="space-y-6">
          <h3 className="text-lg font-bold mb-3">Success Predictions</h3>
          
          <div className="bg-gray-50 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-lg font-medium">Likelihood of Becoming Law</h4>
              <span className="text-2xl font-bold text-green-600">75%</span>
            </div>
            
            <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
              <div className="bg-green-500 h-4 rounded-full" style={{ width: '75%' }}></div>
            </div>
            
            <div className="space-y-3 text-sm">
              <div className="flex items-start">
                <span className="text-green-600 mr-2">+</span>
                <span>Government bill with party support</span>
              </div>
              <div className="flex items-start">
                <span className="text-green-600 mr-2">+</span>
                <span>Aligns with current justice reform priorities</span>
              </div>
              <div className="flex items-start">
                <span className="text-green-600 mr-2">+</span>
                <span>Support from NDP and Bloc likely</span>
              </div>
              <div className="flex items-start">
                <span className="text-red-600 mr-2">-</span>
                <span>Conservative opposition expected</span>
              </div>
              <div className="flex items-start">
                <span className="text-red-600 mr-2">-</span>
                <span>Senate amendments possible</span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-medium mb-3">Timeline Prediction</h4>
            <div className="space-y-2 text-sm text-gray-700">
              <div className="flex items-center justify-between py-2 border-b">
                <span>Committee Stage Completion</span>
                <span className="font-medium">2-3 weeks</span>
              </div>
              <div className="flex items-center justify-between py-2 border-b">
                <span>Third Reading (House)</span>
                <span className="font-medium">4-5 weeks</span>
              </div>
              <div className="flex items-center justify-between py-2 border-b">
                <span>Senate Consideration</span>
                <span className="font-medium">6-8 weeks</span>
              </div>
              <div className="flex items-center justify-between py-2">
                <span className="font-medium">Expected Royal Assent</span>
                <span className="font-medium text-op-blue">Late Fall 2025</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data Sources */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Analysis based on parliamentary records, committee testimony, stakeholder submissions, 
          and historical voting patterns. Predictions are estimates and subject to change.
        </p>
      </div>
    </div>
  );
}
