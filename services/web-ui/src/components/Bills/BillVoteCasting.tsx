'use client';

import { useState } from 'react';
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  MinusIcon,
  UserIcon,
  FlagIcon,
  ChartBarIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline';
import { api } from '@/lib/api';

interface BillVoteCastingProps {
  billId: string;
  billTitle: string;
  billNumber: string;
  userId: string;
  onVoteCast?: (voteData: any) => void;
}

export default function BillVoteCasting({ 
  billId, 
  billTitle, 
  billNumber, 
  userId, 
  onVoteCast 
}: BillVoteCastingProps) {
  const [voteChoice, setVoteChoice] = useState<'yes' | 'no' | 'abstain' | null>(null);
  const [reason, setReason] = useState('');
  const [confidenceLevel, setConfidenceLevel] = useState<'low' | 'medium' | 'high'>('medium');
  const [constituency, setConstituency] = useState('');
  const [partyPreference, setPartyPreference] = useState('');
  const [influenceFactors, setInfluenceFactors] = useState<string[]>([]);
  const [relatedIssues, setRelatedIssues] = useState<string[]>([]);
  const [publicVisibility, setPublicVisibility] = useState<'public' | 'private'>('public');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const predefinedInfluenceFactors = [
    'environmental_concerns',
    'economic_impact',
    'social_justice',
    'constituent_feedback',
    'party_alignment',
    'personal_values',
    'expert_opinion',
    'media_coverage'
  ];

  const predefinedIssues = [
    'climate_change',
    'healthcare',
    'economy',
    'education',
    'security',
    'immigration',
    'infrastructure',
    'taxation'
  ];

  const handleVoteCast = async () => {
    if (!voteChoice || !reason.trim()) {
      alert('Please select a vote choice and provide a reason.');
      return;
    }

    setIsSubmitting(true);

    try {
      const voteData = {
        user_id: userId,
        vote_choice: voteChoice,
        reason: reason.trim(),
        confidence_level: confidenceLevel,
        constituency: constituency || undefined,
        party_preference: partyPreference || undefined,
        influence_factors: influenceFactors,
        related_issues: relatedIssues,
        public_visibility: publicVisibility,
        vote_weight: 1.0,
        device: 'web',
        location: 'web',
        session_id: `session-${Date.now()}`
      };

      const response = await api.castBillVote(billId, voteData);

      if (response.success) {
        // Reset form
        setVoteChoice(null);
        setReason('');
        setConfidenceLevel('medium');
        setConstituency('');
        setPartyPreference('');
        setInfluenceFactors([]);
        setRelatedIssues([]);
        setPublicVisibility('public');
        setShowAdvanced(false);

        // Notify parent component
        if (onVoteCast) {
          onVoteCast(response.vote_record);
        }

        alert('Vote cast successfully!');
      } else {
        alert('Failed to cast vote. Please try again.');
      }
    } catch (_error) {
      console.error('Error casting vote:', error);
      alert('Error casting vote. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleInfluenceFactor = (factor: string) => {
    setInfluenceFactors(prev => 
      prev.includes(factor) 
        ? prev.filter(f => f !== factor)
        : [...prev, factor]
    );
  };

  const toggleRelatedIssue = (issue: string) => {
    setRelatedIssues(prev => 
      prev.includes(issue) 
        ? prev.filter(i => i !== issue)
        : [...prev, issue]
    );
  };

  const getVoteChoiceIcon = (choice: 'yes' | 'no' | 'abstain') => {
    switch (choice) {
      case 'yes':
        return <CheckCircleIcon className="h-6 w-6 text-green-600" />;
      case 'no':
        return <XCircleIcon className="h-6 w-6 text-red-600" />;
      case 'abstain':
        return <MinusIcon className="h-6 w-6 text-yellow-600" />;
      default:
        return null;
    }
  };

  const getVoteChoiceColor = (choice: 'yes' | 'no' | 'abstain') => {
    switch (choice) {
      case 'yes':
        return 'border-green-500 bg-green-50 text-green-700';
      case 'no':
        return 'border-red-500 bg-red-50 text-red-700';
      case 'abstain':
        return 'border-yellow-500 bg-yellow-50 text-yellow-700';
      default:
        return 'border-gray-300 bg-white text-gray-700';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Cast Your Vote</h3>
        <p className="text-sm text-gray-600">
          Vote on Bill {billNumber}: {billTitle}
        </p>
      </div>

      {/* Vote Choice Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          How do you vote on this bill? *
        </label>
        <div className="grid grid-cols-3 gap-3">
          {(['yes', 'no', 'abstain'] as const).map((choice) => (
            <button
              key={choice}
              onClick={() => setVoteChoice(choice)}
              className={`p-4 border-2 rounded-lg text-center transition-colors ${
                voteChoice === choice 
                  ? getVoteChoiceColor(choice)
                  : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
              }`}
            >
              <div className="flex flex-col items-center space-y-2">
                {getVoteChoiceIcon(choice)}
                <span className="font-medium capitalize">{choice}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Reason for Vote */}
      <div className="mb-6">
        <label htmlFor="reason" className="block text-sm font-medium text-gray-700 mb-2">
          Reason for your vote *
        </label>
        <textarea
          id="reason"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
          placeholder="Explain your reasoning for this vote..."
          required
        />
      </div>

      {/* Confidence Level */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          How confident are you in your decision?
        </label>
        <div className="flex space-x-4">
          {(['low', 'medium', 'high'] as const).map((level) => (
            <label key={level} className="flex items-center">
              <input
                type="radio"
                name="confidence"
                value={level}
                checked={confidenceLevel === level}
                onChange={(e) => setConfidenceLevel(e.target.value as 'low' | 'medium' | 'high')}
                className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300"
              />
              <span className="ml-2 text-sm text-gray-700 capitalize">{level}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Advanced Options Toggle */}
      <div className="mb-4">
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center text-sm text-op-blue hover:text-op-blue-700 transition-colors"
        >
          <LightBulbIcon className="h-4 w-4 mr-2" />
          {showAdvanced ? 'Hide' : 'Show'} Advanced Options
        </button>
      </div>

      {/* Advanced Options */}
      {showAdvanced && (
        <div className="space-y-6 p-4 bg-gray-50 rounded-lg">
          {/* Constituency and Party */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="constituency" className="block text-sm font-medium text-gray-700 mb-2">
                Constituency (Optional)
              </label>
              <input
                type="text"
                id="constituency"
                value={constituency}
                onChange={(e) => setConstituency(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
                placeholder="e.g., Toronto Centre"
              />
            </div>
            <div>
              <label htmlFor="party" className="block text-sm font-medium text-gray-700 mb-2">
                Party Preference (Optional)
              </label>
              <input
                type="text"
                id="party"
                value={partyPreference}
                onChange={(e) => setPartyPreference(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
                placeholder="e.g., Liberal, Conservative"
              />
            </div>
          </div>

          {/* Influence Factors */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What influenced your decision? (Optional)
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {predefinedInfluenceFactors.map((factor) => (
                <label key={factor} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={influenceFactors.includes(factor)}
                    onChange={() => toggleInfluenceFactor(factor)}
                    className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300 rounded"
                  />
                  <span className="ml-2 text-xs text-gray-700">
                    {factor.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Related Issues */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Related issues this bill addresses (Optional)
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {predefinedIssues.map((issue) => (
                <label key={issue} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={relatedIssues.includes(issue)}
                    onChange={() => toggleRelatedIssue(issue)}
                    className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300 rounded"
                  />
                  <span className="ml-2 text-xs text-gray-700">
                    {issue.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Public Visibility */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Vote Visibility
            </label>
            <div className="flex space-x-4">
              {(['public', 'private'] as const).map((visibility) => (
                <label key={visibility} className="flex items-center">
                  <input
                    type="radio"
                    name="visibility"
                    value={visibility}
                    checked={publicVisibility === visibility}
                    onChange={(e) => setPublicVisibility(e.target.value as 'public' | 'private')}
                    className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700 capitalize">{visibility}</span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Public votes are visible to others and contribute to public opinion analysis.
            </p>
          </div>
        </div>
      )}

      {/* Submit Button */}
      <div className="flex justify-end">
        <button
          onClick={handleVoteCast}
          disabled={!voteChoice || !reason.trim() || isSubmitting}
          className={`px-6 py-2 rounded-md font-medium transition-colors ${
            !voteChoice || !reason.trim() || isSubmitting
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-op-blue text-white hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue'
          }`}
        >
          {isSubmitting ? 'Casting Vote...' : 'Cast Vote'}
        </button>
      </div>

      {/* Information Note */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
        <div className="flex items-start">
          <UserIcon className="h-5 w-5 text-blue-600 mt-0.5 mr-2" />
          <div className="text-sm text-blue-800">
            <p className="font-medium">Your vote matters!</p>
            <p className="mt-1">
              Your vote contributes to public opinion analysis and helps inform democratic discourse. 
              All votes are anonymous and secure.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
