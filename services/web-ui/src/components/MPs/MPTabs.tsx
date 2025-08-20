'use client';

import { useState } from 'react';
import { Member } from '@/lib/api';
import MPVotingRecord from './MPVotingRecord';
import MPSpeeches from './MPSpeeches';
import MPCommittees from './MPCommittees';
import MPElectoralHistory from './MPElectoralHistory';

interface MPTabsProps {
  mp: Member;
}

export default function MPTabs({ mp }: MPTabsProps) {
  const [activeTab, setActiveTab] = useState('votes');

  const tabs = [
    { id: 'votes', label: 'Voting Record', component: <MPVotingRecord mpId={mp.id} /> },
    { id: 'speeches', label: 'Speeches', component: <MPSpeeches mpId={mp.id} /> },
    { id: 'committees', label: 'Committees', component: <MPCommittees mpId={mp.id} /> },
    { id: 'electoral', label: 'Electoral History', component: <MPElectoralHistory mpId={mp.id} /> },
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
