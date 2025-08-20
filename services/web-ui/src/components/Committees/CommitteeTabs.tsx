'use client';

import { useState } from 'react';
import { Committee } from '@/lib/api';
import CommitteeMembers from './CommitteeMembers';
import CommitteeReports from './CommitteeReports';
import CommitteeNews from './CommitteeNews';
import CommitteeHistory from './CommitteeHistory';

interface CommitteeTabsProps {
  committee: Committee;
}

export default function CommitteeTabs({ committee }: CommitteeTabsProps) {
  const [activeTab, setActiveTab] = useState('members');

  const tabs = [
    { id: 'members', label: 'Members', component: <CommitteeMembers committeeId={committee.id} /> },
    { id: 'reports', label: 'Reports', component: <CommitteeReports committeeId={committee.id} /> },
    { id: 'news', label: 'News & Updates', component: <CommitteeNews committeeId={committee.id} /> },
    { id: 'history', label: 'History', component: <CommitteeHistory committeeId={committee.id} /> },
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
