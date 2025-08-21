import { Metadata } from 'next';
import MobileAppDemo from '@/components/mobile-app/MobileAppDemo';

export const metadata: Metadata = {
  title: 'Mobile App Features | OpenPolicy',
  description: 'Experience all OpenPolicy mobile app features on the web platform',
  openGraph: {
    title: 'Mobile App Features | OpenPolicy',
    description: 'Experience all OpenPolicy mobile app features on the web platform',
    type: 'website',
  },
};

export default function MobileAppPage() {
  return (
    <div className="content-container py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          Mobile App Features on Web
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Experience all the features from the OpenPolicy mobile app right here on the web. 
          This page demonstrates the complete cross-platform compatibility between mobile and web.
        </p>
        
        <MobileAppDemo />
      </div>
    </div>
  );
}
