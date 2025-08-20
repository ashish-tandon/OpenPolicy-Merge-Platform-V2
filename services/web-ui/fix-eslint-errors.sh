#!/bin/bash

# Fix unescaped entities in React components
sed -i "s/\"can't\"/\"can\&apos;t\"/g" src/app/labs/haiku/page.tsx
sed -i 's/"/"&ldquo;/g' src/app/labs/haiku/page.tsx | sed -i 's/"/"&rdquo;/g' src/app/labs/haiku/page.tsx
sed -i "s/There's/There\&apos;s/g" src/app/labs/page.tsx
sed -i "s/let's/let\&apos;s/g" src/app/labs/page.tsx
sed -i 's/"/"&ldquo;/g' src/app/search/page.tsx | sed -i 's/"/"&rdquo;/g' src/app/search/page.tsx
sed -i "s/'\([^']*\)'/\&lsquo;\1\&rsquo;/g" src/components/Bills/BillAnalysis.tsx
sed -i 's/"/"&ldquo;/g' src/components/Bills/RelatedDebates.tsx | sed -i 's/"/"&rdquo;/g' src/components/Bills/RelatedDebates.tsx
sed -i "s/committee's/committee\&apos;s/g" src/components/Committees/CommitteeHistory.tsx
sed -i "s/haven't/haven\&apos;t/g" src/components/Debates/DebatesFilters.tsx
sed -i 's/"/"&ldquo;/g' src/components/SearchBar.tsx | sed -i 's/"/"&rdquo;/g' src/components/SearchBar.tsx

# Fix unused variables - add underscore prefix
sed -i 's/} catch (error) {/} catch (_error) {/g' src/app/bills/\[session\]/\[number\]/page.tsx
sed -i 's/} catch (error) {/} catch (_error) {/g' src/app/committees/\[slug\]/page.tsx
sed -i 's/} catch (error) {/} catch (_error) {/g' src/app/debates/\[date\]/\[number\]/page.tsx
sed -i 's/} catch (error) {/} catch (_error) {/g' src/app/mps/\[slug\]/page.tsx
sed -i 's/} catch (e) {/} catch (_e) {/g' src/app/search/page.tsx

# Fix TypeScript any types by adding proper type annotations
echo "Fixing TypeScript any types..."

# Update BillsList.tsx
cat > src/components/Bills/BillsList.tsx << 'EOF'
'use client';

import Link from 'next/link';
import { Bill } from '@/lib/api';
import Pagination from '@/components/Pagination';

interface BillsListProps {
  bills: Bill[];
  currentPage: number;
  totalPages: number;
}

interface BillWithDetails extends Bill {
  latest_activity?: string;
  sponsor_name?: string;
}

export default function BillsList({ bills, currentPage, totalPages }: BillsListProps) {
  const getStatusBadgeClass = (status: string) => {
    switch (status.toLowerCase()) {
      case 'passed':
      case 'royal assent':
        return 'bg-green-100 text-green-800';
      case 'defeated':
        return 'bg-red-100 text-red-800';
      case 'active':
      case 'in committee':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      {bills.map((bill) => {
        const billDetails = bill as BillWithDetails;
        return (
          <div key={bill.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-sm font-medium text-gray-500">
                    Bill {bill.number}
                  </span>
                  <span className={`px-2 py-1 text-xs font-medium rounded ${getStatusBadgeClass(billDetails.latest_activity || 'Unknown')}`}>
                    {billDetails.latest_activity || 'Unknown Status'}
                  </span>
                  {bill.law && (
                    <span className="px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded">
                      Law
                    </span>
                  )}
                  {bill.privatemember && (
                    <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded">
                      Private Member
                    </span>
                  )}
                </div>
                
                <Link 
                  href={`/bills/${bill.session}/${bill.number}`}
                  className="text-lg font-semibold text-blue-600 hover:text-blue-800"
                >
                  {bill.name}
                </Link>
                
                <div className="mt-2 text-sm text-gray-600">
                  {billDetails.sponsor_name && (
                    <p>Sponsor: {billDetails.sponsor_name}</p>
                  )}
                  {bill.introduced && (
                    <p>Introduced: {new Date(bill.introduced).toLocaleDateString()}</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        );
      })}
      
      {bills.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500">No bills found matching your criteria.</p>
        </div>
      )}
      
      {totalPages > 1 && (
        <div className="mt-8">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            basePath="/bills"
          />
        </div>
      )}
    </div>
  );
}
EOF

echo "ESLint fixes applied!"
chmod +x fix-eslint-errors.sh
