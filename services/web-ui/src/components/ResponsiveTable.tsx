/**
 * Responsive table component that adapts to mobile screens
 * Based on legacy responsive patterns from foundation
 */

interface Column {
  key: string;
  label: string;
  sortable?: boolean;
  className?: string;
}

interface ResponsiveTableProps {
  columns: Column[];
  data: any[];
  onSort?: (column: string) => void;
  sortColumn?: string;
  sortDirection?: 'asc' | 'desc';
  loading?: boolean;
  emptyMessage?: string;
}

import SkeletonLoader from './SkeletonLoader';

export default function ResponsiveTable({
  columns,
  data,
  onSort,
  sortColumn,
  sortDirection,
  loading = false,
  emptyMessage = 'No data available'
}: ResponsiveTableProps) {
  // Based on legacy responsive patterns
  const handleSort = (column: string) => {
    if (onSort) {
      onSort(column);
    }
  };
  
  if (loading) {
    return <SkeletonLoader type="table" />;
  }
  
  return (
    <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
      {/* Desktop table */}
      <table className="min-w-full divide-y divide-gray-300 hidden md:table">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                scope="col"
                className={`px-6 py-3 text-left text-xs font-medium text-gray-900 uppercase tracking-wider ${
                  column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                } ${column.className || ''}`}
                onClick={() => column.sortable && handleSort(column.key)}
                role={column.sortable ? 'button' : undefined}
                aria-sort={
                  sortColumn === column.key
                    ? sortDirection === 'asc'
                      ? 'ascending'
                      : 'descending'
                    : 'none'
                }
              >
                <div className="flex items-center space-x-1">
                  <span>{column.label}</span>
                  {column.sortable && (
                    <svg
                      className={`h-4 w-4 ${
                        sortColumn === column.key
                          ? 'text-gray-900'
                          : 'text-gray-400'
                      }`}
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                      aria-hidden="true"
                    >
                      <path
                        fillRule="evenodd"
                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length}
                className="px-6 py-12 text-center text-gray-500"
              >
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-gray-50">
                {columns.map((column) => (
                  <td
                    key={column.key}
                    className={`px-6 py-4 whitespace-nowrap text-sm text-gray-900 ${
                      column.className || ''
                    }`}
                  >
                    {row[column.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
      
      {/* Mobile cards */}
      <div className="md:hidden">
        {data.length === 0 ? (
          <div className="px-6 py-12 text-center text-gray-500">
            {emptyMessage}
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {data.map((row, rowIndex) => (
              <li key={rowIndex} className="px-4 py-4">
                <div className="space-y-2">
                  {columns.map((column) => (
                    <div key={column.key} className="flex justify-between">
                      <span className="text-sm font-medium text-gray-500">
                        {column.label}:
                      </span>
                      <span className="text-sm text-gray-900">
                        {row[column.key]}
                      </span>
                    </div>
                  ))}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
