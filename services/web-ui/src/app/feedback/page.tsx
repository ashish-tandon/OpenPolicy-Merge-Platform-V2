import { Metadata } from 'next';
import FeedbackPortal from '@/components/feedback/FeedbackPortal';

export const metadata: Metadata = {
  title: 'Feedback & Suggestions | OpenPolicy',
  description: 'Share your feedback, suggest new features, and vote on ideas for OpenPolicy V2',
  openGraph: {
    title: 'Feedback & Suggestions | OpenPolicy',
    description: 'Share your feedback, suggest new features, and vote on ideas for OpenPolicy V2',
    type: 'website',
  },
};

export default function FeedbackPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Feedback & Suggestions
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Help us improve OpenPolicy V2! Share your ideas, vote on existing suggestions, 
            and help us prioritize the features that matter most to you.
          </p>
        </div>
        
        <FeedbackPortal />
      </div>
    </div>
  );
}
