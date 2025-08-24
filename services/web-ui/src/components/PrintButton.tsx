/**
 * Print Button Component
 * 
 * Reusable print button that integrates with PrintService.
 */

import { PrinterIcon } from '@heroicons/react/24/outline';
import { PrintService } from '@/services/printService';

interface PrintButtonProps {
  // What to print
  mode?: 'page' | 'element' | 'bill' | 'member' | 'voting-record';
  
  // For element mode
  elementSelector?: string;
  
  // For specific content types
  billId?: string;
  memberId?: string;
  
  // UI options
  showLabel?: boolean;
  showPreview?: boolean;
  className?: string;
  size?: 'small' | 'medium' | 'large';
  variant?: 'primary' | 'secondary' | 'ghost';
  
  // Custom options
  title?: string;
  orientation?: 'portrait' | 'landscape';
  hideElements?: string[];
  beforePrint?: () => void;
  afterPrint?: () => void;
}

export function PrintButton({
  mode = 'page',
  elementSelector,
  billId,
  memberId,
  showLabel = true,
  showPreview = false,
  className = '',
  size = 'medium',
  variant = 'secondary',
  title,
  orientation,
  hideElements,
  beforePrint,
  afterPrint
}: PrintButtonProps) {
  
  const handlePrint = () => {
    const options = {
      title,
      pageOrientation: orientation,
      hideElements,
      beforePrint,
      afterPrint
    };
    
    switch (mode) {
      case 'bill':
        if (billId) {
          PrintService.printBill(billId);
        }
        break;
        
      case 'member':
        if (memberId) {
          PrintService.printMemberProfile(memberId);
        }
        break;
        
      case 'voting-record':
        if (memberId) {
          PrintService.printVotingRecord(memberId);
        }
        break;
        
      case 'element':
        if (elementSelector) {
          PrintService.printElement(elementSelector, options);
        }
        break;
        
      case 'page':
      default:
        if (showPreview) {
          PrintService.printPreview(options);
        } else {
          PrintService.print(options);
        }
        break;
    }
  };
  
  const sizeClasses = {
    small: 'px-2 py-1 text-xs',
    medium: 'px-3 py-2 text-sm',
    large: 'px-4 py-3 text-base'
  };
  
  const variantClasses = {
    primary: 'bg-op-blue text-white hover:bg-blue-700 focus:ring-op-blue',
    secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700',
    ghost: 'text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-100 dark:hover:bg-gray-800'
  };
  
  const iconSize = {
    small: 'h-3 w-3',
    medium: 'h-4 w-4',
    large: 'h-5 w-5'
  };
  
  return (
    <button
      onClick={handlePrint}
      className={`
        inline-flex items-center gap-2 font-medium rounded-md
        transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        ${className}
      `}
      aria-label={showLabel ? undefined : 'Print'}
    >
      <PrinterIcon className={iconSize[size]} />
      {showLabel && <span>Print</span>}
    </button>
  );
}

// Specialized print buttons

export function BillPrintButton({ billId, ...props }: Omit<PrintButtonProps, 'mode' | 'billId'> & { billId: string }) {
  return <PrintButton mode="bill" billId={billId} {...props} />;
}

export function MemberPrintButton({ memberId, ...props }: Omit<PrintButtonProps, 'mode' | 'memberId'> & { memberId: string }) {
  return <PrintButton mode="member" memberId={memberId} {...props} />;
}

export function VotingRecordPrintButton({ memberId, ...props }: Omit<PrintButtonProps, 'mode' | 'memberId'> & { memberId: string }) {
  return <PrintButton mode="voting-record" memberId={memberId} showLabel={true} {...props} />;
}