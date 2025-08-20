import { Member } from '@/lib/api';

interface MPContactInfoProps {
  mp: Member;
}

export default function MPContactInfo({ mp }: MPContactInfoProps) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <h3 className="font-bold text-gray-700 mb-3">Contact Information</h3>
      
      <div className="space-y-3 text-sm">
        {/* Email */}
        {mp.email && (
          <div>
            <div className="font-medium text-gray-600">Email</div>
            <a href={`mailto:${mp.email}`} className="text-op-blue hover:underline break-all">
              {mp.email}
            </a>
          </div>
        )}

        {/* Parliament Office */}
        <div>
          <div className="font-medium text-gray-600">Parliament Office</div>
          <div className="text-gray-700">
            House of Commons<br />
            Ottawa, Ontario<br />
            K1A 0A6
          </div>
        </div>

        {/* Phone */}
        <div>
          <div className="font-medium text-gray-600">Phone</div>
          <a href="tel:+16139920000" className="text-op-blue hover:underline">
            (613) 992-0000
          </a>
        </div>

        {/* Website */}
        {mp.url && (
          <div>
            <div className="font-medium text-gray-600">Official Website</div>
            <a 
              href={mp.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-op-blue hover:underline break-all"
            >
              {mp.url}
            </a>
          </div>
        )}

        {/* Social Media */}
        <div>
          <div className="font-medium text-gray-600 mb-2">Social Media</div>
          <div className="flex gap-3">
            <a
              href={`https://twitter.com/search?q=${encodeURIComponent(mp.name)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-op-blue hover:text-blue-700"
              title="Search on Twitter"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </a>
          </div>
        </div>
      </div>

      {/* Contact MP Button */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <a
          href={`mailto:${mp.email}`}
          className="block w-full text-center bg-op-blue text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
        >
          Contact MP
        </a>
      </div>
    </div>
  );
}
