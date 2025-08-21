import { Metadata } from 'next';
import SavedItemsManager from '@/components/saved-items/SavedItemsManager';

export const metadata: Metadata = {
  title: 'Saved Items | OpenPolicy',
  description: 'View and manage your saved bills, MPs, debates, committees, and voting records',
  openGraph: {
    title: 'Saved Items | OpenPolicy',
    description: 'View and manage your saved parliamentary content',
    type: 'website',
  },
};

export default function SavedItemsPage() {
  // TODO: Replace with actual user ID from authentication
  const userId = "demo-user-123";

  return (
    <div className="content-container py-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Saved Items
          </h1>
          <p className="text-lg text-gray-600">
            Access your saved parliamentary content, including bills, MPs, debates, committees, and voting records.
          </p>
        </div>
        
        <SavedItemsManager userId={userId} />
      </div>
    </div>
  );
}
