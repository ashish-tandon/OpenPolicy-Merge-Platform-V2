import Link from 'next/link';
import { Bill } from '@/lib/api';

interface RecentBillsProps {
  bills: Bill[];
}

export default function RecentBills({ bills }: RecentBillsProps) {
  // Show up to 6 recent bills
  const recentBills = bills.slice(0, 6);

  if (recentBills.length === 0) {
    return <p className="text-gray-500 text-sm">No recent bills available</p>;
  }

  return (
    <ul className="space-y-3">
      {recentBills.map((bill) => (
        <li key={bill.id}>
          <Link 
            href={`/bills/${bill.session}/${bill.number}`}
            className="block hover:bg-gray-50 -mx-2 px-2 py-1 rounded"
          >
            <div className="flex items-center justify-between">
              <div>
                <span className="font-medium text-op-blue hover:underline">
                  {bill.number}
                </span>
                {bill.privatemember && (
                  <span className="ml-2 text-xs bg-purple-100 text-purple-800 px-2 py-0.5 rounded">
                    Private
                  </span>
                )}
              </div>
              {bill.law && (
                <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded">
                  Law
                </span>
              )}
            </div>
            <div className="text-sm text-gray-600 mt-1 line-clamp-2">
              {bill.name}
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}
