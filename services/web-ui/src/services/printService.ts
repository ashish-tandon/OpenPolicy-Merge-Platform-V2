/**
 * Print Service
 * 
 * Centralized service for managing print functionality.
 * Provides consistent print styling and preview capabilities.
 */

interface PrintOptions {
  title?: string;
  hideElements?: string[]; // CSS selectors to hide
  showElements?: string[]; // CSS selectors to force show
  pageOrientation?: 'portrait' | 'landscape';
  pageMargins?: {
    top?: string;
    right?: string;
    bottom?: string;
    left?: string;
  };
  beforePrint?: () => void;
  afterPrint?: () => void;
}

export class PrintService {
  private static isPrinting = false;
  private static originalTitle: string = '';
  
  /**
   * Print the current page with optional configuration
   */
  static print(options: PrintOptions = {}): void {
    if (this.isPrinting) return;
    
    this.isPrinting = true;
    this.setupPrintStyles(options);
    
    // Store original title
    this.originalTitle = document.title;
    if (options.title) {
      document.title = options.title;
    }
    
    // Call before print callback
    options.beforePrint?.();
    
    // Add print event listeners
    window.addEventListener('beforeprint', this.handleBeforePrint);
    window.addEventListener('afterprint', () => this.handleAfterPrint(options));
    
    // Trigger print
    window.print();
  }
  
  /**
   * Open print preview in a new window
   */
  static printPreview(options: PrintOptions = {}): Window | null {
    const printWindow = window.open('', '_blank', 'width=800,height=600');
    if (!printWindow) return null;
    
    // Clone current document
    const content = document.documentElement.cloneNode(true) as HTMLElement;
    
    // Apply print styles to preview
    this.applyPrintStylesToElement(content, options);
    
    // Write to preview window
    printWindow.document.write('<!DOCTYPE html>');
    printWindow.document.write(content.outerHTML);
    printWindow.document.close();
    
    // Add print button to preview
    this.addPrintButton(printWindow);
    
    return printWindow;
  }
  
  /**
   * Print specific element
   */
  static printElement(selector: string, options: PrintOptions = {}): void {
    const element = document.querySelector(selector);
    if (!element) {
      console.error(`Element not found: ${selector}`);
      return;
    }
    
    // Create print container
    const printContainer = document.createElement('div');
    printContainer.id = 'print-container';
    printContainer.innerHTML = element.innerHTML;
    
    // Hide all other content
    document.body.style.display = 'none';
    document.body.appendChild(printContainer);
    
    // Print
    this.print({
      ...options,
      afterPrint: () => {
        // Restore original content
        document.body.removeChild(printContainer);
        document.body.style.display = '';
        options.afterPrint?.();
      }
    });
  }
  
  /**
   * Generate print-friendly version of bills
   */
  static printBill(billId: string): void {
    this.print({
      title: `Bill ${billId} - OpenPolicy`,
      hideElements: [
        '.header-nav',
        '.footer',
        '.sidebar',
        '.social-share',
        '.comments-section',
        '.vote-buttons',
        '.back-to-top'
      ],
      pageOrientation: 'portrait',
      beforePrint: () => {
        // Expand all collapsed sections
        document.querySelectorAll('.collapsible').forEach(el => {
          el.classList.add('expanded');
        });
      }
    });
  }
  
  /**
   * Generate print-friendly version of member profile
   */
  static printMemberProfile(memberId: string): void {
    this.print({
      title: `Member Profile - ${memberId}`,
      hideElements: [
        '.header-nav',
        '.footer',
        '.interactive-chart',
        '.social-links',
        '.edit-buttons'
      ],
      showElements: [
        '.member-photo',
        '.member-details',
        '.voting-record-summary'
      ],
      pageOrientation: 'portrait'
    });
  }
  
  /**
   * Generate print-friendly voting record
   */
  static printVotingRecord(memberId: string, options: { dateFrom?: string; dateTo?: string } = {}): void {
    this.print({
      title: `Voting Record - ${memberId}`,
      hideElements: [
        '.header-nav',
        '.footer',
        '.filters',
        '.pagination'
      ],
      pageOrientation: 'landscape',
      beforePrint: () => {
        // Add date range header if specified
        if (options.dateFrom || options.dateTo) {
          const header = document.createElement('div');
          header.className = 'print-date-range';
          header.textContent = `Date Range: ${options.dateFrom || 'Start'} to ${options.dateTo || 'Present'}`;
          document.querySelector('.voting-record')?.prepend(header);
        }
      }
    });
  }
  
  // Private methods
  
  private static setupPrintStyles(options: PrintOptions): void {
    let styleSheet = document.getElementById('print-styles') as HTMLStyleElement;
    
    if (!styleSheet) {
      styleSheet = document.createElement('style');
      styleSheet.id = 'print-styles';
      document.head.appendChild(styleSheet);
    }
    
    const styles = this.generatePrintStyles(options);
    styleSheet.textContent = styles;
  }
  
  private static generatePrintStyles(options: PrintOptions): string {
    const margins = options.pageMargins || {};
    const orientation = options.pageOrientation || 'portrait';
    
    let styles = `
      @media print {
        /* Page setup */
        @page {
          size: A4 ${orientation};
          margin: ${margins.top || '2cm'} ${margins.right || '2cm'} ${margins.bottom || '2cm'} ${margins.left || '2cm'};
        }
        
        /* Reset styles */
        * {
          -webkit-print-color-adjust: exact !important;
          print-color-adjust: exact !important;
        }
        
        /* Hide non-print elements */
        .no-print,
        .header-nav,
        .footer,
        .theme-toggle,
        .edit-button,
        .share-button {
          display: none !important;
        }
        
        /* Show print-only elements */
        .print-only {
          display: block !important;
        }
        
        /* Typography */
        body {
          font-size: 12pt !important;
          line-height: 1.5 !important;
          color: #000 !important;
          background: #fff !important;
        }
        
        h1 { font-size: 20pt !important; }
        h2 { font-size: 16pt !important; }
        h3 { font-size: 14pt !important; }
        
        /* Links */
        a {
          color: #000 !important;
          text-decoration: underline !important;
        }
        
        a[href^="http"]:after {
          content: " (" attr(href) ")";
          font-size: 0.8em;
          color: #666;
        }
        
        /* Images */
        img {
          max-width: 100% !important;
          page-break-inside: avoid;
        }
        
        /* Tables */
        table {
          border-collapse: collapse !important;
          width: 100% !important;
        }
        
        table, th, td {
          border: 1px solid #ccc !important;
          padding: 8px !important;
        }
        
        /* Page breaks */
        h1, h2, h3 {
          page-break-after: avoid;
        }
        
        p, blockquote, ul, ol {
          orphans: 3;
          widows: 3;
        }
        
        /* Bill-specific styles */
        .bill-section {
          page-break-inside: avoid;
          margin-bottom: 1em;
        }
        
        .bill-text {
          text-align: justify;
        }
        
        /* Member profile styles */
        .member-photo {
          max-width: 150px !important;
          float: left;
          margin-right: 1em;
        }
        
        .member-details {
          page-break-inside: avoid;
        }
        
        /* Voting record styles */
        .voting-table {
          font-size: 10pt !important;
        }
        
        .vote-yes { color: #047857 !important; }
        .vote-no { color: #B91C1C !important; }
        .vote-abstain { color: #6B7280 !important; }
    `;
    
    // Add custom hide elements
    if (options.hideElements) {
      styles += options.hideElements.map(selector => 
        `${selector} { display: none !important; }`
      ).join('\n');
    }
    
    // Add custom show elements
    if (options.showElements) {
      styles += options.showElements.map(selector => 
        `${selector} { display: block !important; }`
      ).join('\n');
    }
    
    styles += '\n}'; // Close @media print
    
    return styles;
  }
  
  private static applyPrintStylesToElement(element: HTMLElement, options: PrintOptions): void {
    const style = document.createElement('style');
    style.textContent = this.generatePrintStyles(options);
    element.querySelector('head')?.appendChild(style);
    
    // Apply inline styles for preview
    element.querySelectorAll('.no-print').forEach(el => {
      (el as HTMLElement).style.display = 'none';
    });
  }
  
  private static addPrintButton(printWindow: Window): void {
    const button = printWindow.document.createElement('button');
    button.textContent = 'Print This Page';
    button.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 10px 20px;
      background: #3B82F6;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      z-index: 9999;
      font-size: 16px;
    `;
    
    button.onclick = () => printWindow.print();
    printWindow.document.body.appendChild(button);
  }
  
  private static handleBeforePrint = (): void => {
    // Add print class to body
    document.body.classList.add('printing');
  };
  
  private static handleAfterPrint = (options: PrintOptions): void => {
    // Remove print class
    document.body.classList.remove('printing');
    
    // Restore original title
    if (this.originalTitle) {
      document.title = this.originalTitle;
    }
    
    // Call after print callback
    options.afterPrint?.();
    
    // Cleanup
    window.removeEventListener('beforeprint', this.handleBeforePrint);
    window.removeEventListener('afterprint', this.handleAfterPrint);
    
    this.isPrinting = false;
  };
}