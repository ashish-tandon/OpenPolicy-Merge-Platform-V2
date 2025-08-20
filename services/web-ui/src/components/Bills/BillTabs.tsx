'use client';

import { useState } from 'react';
import { Bill } from '@/lib/api';
import BillText from './BillText';
import BillCommittees from './BillCommittees';
import BillAmendments from './BillAmendments';
import BillAnalysis from './BillAnalysis';

interface BillTabsProps {
  bill: Bill;
}

export default function BillTabs({ bill }: BillTabsProps) {
  const [activeTab, setActiveTab] = useState('text');

  const tabs = [
    { id: 'text', label: 'Bill Text', component: <BillText billId={bill.id} /> },
    { id: 'committees', label: 'Committee Review', component: <BillCommittees billId={bill.id} /> },
    { id: 'amendments', label: 'Amendments', component: <BillAmendments billId={bill.id} /> },
    { id: 'analysis', label: 'Analysis', component: <BillAnalysis bill={bill} /> },
  ];

  return (
    <div>
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="flex -mb-px">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                px-6 py-3 text-sm font-medium border-b-2 transition-colors
                ${activeTab === tab.id
                  ? 'border-op-blue text-op-blue'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {tabs.find(tab => tab.id === activeTab)?.component}
      </div>
    </div>
  );
}
