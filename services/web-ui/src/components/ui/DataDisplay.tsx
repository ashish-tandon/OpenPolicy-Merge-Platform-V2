'use client';

import { ReactNode, useState, useMemo } from 'react';
// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};
import { 
  ChevronUpIcon, 
  ChevronDownIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';

// Table Component
interface TableColumn<T> {
  key: string;
  header: string;
  render?: (value: any, item: T) => ReactNode;
  sortable?: boolean;
  width?: string;
  className?: string;
}

interface TableProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  sortable?: boolean;
  searchable?: boolean;
  filterable?: boolean;
  selectable?: boolean;
  onRowClick?: (item: T) => void;
  onSelectionChange?: (selectedItems: T[]) => void;
  className?: string;
  emptyMessage?: string;
  loading?: boolean;
}

export function Table<T extends { id?: string | number }>({
  data,
  columns,
  sortable = true,
  searchable = true,
  filterable = true,
  selectable = false,
  onRowClick,
  onSelectionChange,
  className = "",
  emptyMessage = "No data available",
  loading = false
}: TableProps<T>) {
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedItems, setSelectedItems] = useState<Set<string | number>>(new Set());
  const [filters, setFilters] = useState<Record<string, any>>({});

  const filteredAndSortedData = useMemo(() => {
    let result = [...data];

    // Apply search
    if (searchTerm) {
      result = result.filter(item =>
        columns.some(column => {
          const value = item[column.key as keyof T];
          return value && value.toString().toLowerCase().includes(searchTerm.toLowerCase());
        })
      );
    }

    // Apply filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        result = result.filter(item => {
          const itemValue = item[key as keyof T];
          if (Array.isArray(value)) {
            return value.includes(itemValue);
          }
          return itemValue === value;
        });
      }
    });

    // Apply sorting
    if (sortConfig) {
      result.sort((a, b) => {
        const aValue = a[sortConfig.key as keyof T];
        const bValue = b[sortConfig.key as keyof T];

        if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return result;
  }, [data, searchTerm, filters, sortConfig, columns]);

  const handleSort = (key: string) => {
    if (!sortable) return;

    setSortConfig(current => {
      if (current?.key === key) {
        return {
          key,
          direction: current.direction === 'asc' ? 'desc' : 'asc'
        };
      }
      return { key, direction: 'asc' };
    });
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      const allIds = filteredAndSortedData.map(item => item.id).filter((id): id is string | number => id !== undefined);
      setSelectedItems(new Set(allIds));
      onSelectionChange?.(filteredAndSortedData);
    } else {
      setSelectedItems(new Set());
      onSelectionChange?.([]);
    }
  };

  const handleSelectItem = (item: T, checked: boolean) => {
    if (!item.id) return;

    const newSelected = new Set(selectedItems);
    if (checked) {
      newSelected.add(item.id);
    } else {
      newSelected.delete(item.id);
    }
    setSelectedItems(newSelected);

    const selectedData = data.filter(item => item.id && newSelected.has(item.id));
    onSelectionChange?.(selectedData);
  };

  if (loading) {
    return (
      <div className={cn("animate-pulse", className)}>
        <div className="h-8 bg-gray-200 rounded mb-4"></div>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200", className)}>
      {/* Table Controls */}
      {(searchable || filterable) && (
        <div className="p-4 border-b border-gray-200">
          <div className="flex flex-col sm:flex-row gap-4">
            {searchable && (
              <div className="flex-1">
                <div className="relative">
                  <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
                  />
                </div>
              </div>
            )}
            
            {filterable && (
              <div className="flex gap-2">
                <button className="flex items-center px-3 py-2 text-sm text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
                  <FunnelIcon className="h-4 w-4 mr-2" />
                  Filters
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {selectable && (
                <th scope="col" className="px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    checked={selectedItems.size === filteredAndSortedData.length && filteredAndSortedData.length > 0}
                    onChange={(e) => handleSelectAll(e.target.checked)}
                    className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300 rounded"
                  />
                </th>
              )}
              
              {columns.map((column) => (
                <th
                  key={column.key}
                  scope="col"
                  className={cn(
                    "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    column.width && `w-${column.width}`,
                    column.className
                  )}
                >
                  <div className="flex items-center space-x-1">
                    <span>{column.header}</span>
                    {sortable && column.sortable !== false && (
                      <button
                        onClick={() => handleSort(column.key)}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                      >
                        {sortConfig?.key === column.key ? (
                          sortConfig.direction === 'asc' ? (
                            <ChevronUpIcon className="h-4 w-4" />
                          ) : (
                            <ChevronDownIcon className="h-4 w-4" />
                          )
                        ) : (
                          <div className="flex flex-col -space-y-1">
                            <ChevronUpIcon className="h-3 w-3" />
                            <ChevronDownIcon className="h-3 w-3" />
                          </div>
                        )}
                      </button>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredAndSortedData.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length + (selectable ? 1 : 0)}
                  className="px-6 py-12 text-center text-gray-500"
                >
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              filteredAndSortedData.map((item, index) => (
                <tr
                  key={item.id || index}
                  className={cn(
                    "hover:bg-gray-50 transition-colors",
                    onRowClick && "cursor-pointer"
                  )}
                  onClick={() => onRowClick?.(item)}
                >
                  {selectable && (
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="checkbox"
                        checked={item.id ? selectedItems.has(item.id) : false}
                        onChange={(e) => handleSelectItem(item, e.target.checked)}
                        onClick={(e) => e.stopPropagation()}
                        className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300 rounded"
                      />
                    </td>
                  )}
                  
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className={cn(
                        "px-6 py-4 whitespace-nowrap text-sm text-gray-900",
                        column.className
                      )}
                    >
                      {column.render
                        ? column.render(item[column.key as keyof T], item)
                        : String(item[column.key as keyof T] || '')
                      }
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Data Grid Component
interface DataGridProps<T> extends TableProps<T> {
  gridCols?: number;
  cardRenderer: (item: T) => ReactNode;
}

export function DataGrid<T extends { id?: string | number }>({
  data,
  columns,
  gridCols = 3,
  cardRenderer,
  searchable = true,
  filterable = true,
  selectable = false,
  onSelectionChange,
  className = "",
  emptyMessage = "No data available",
  loading = false
}: DataGridProps<T>) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedItems, setSelectedItems] = useState<Set<string | number>>(new Set());
  const [filters, setFilters] = useState<Record<string, any>>({});

  const filteredData = useMemo(() => {
    let result = [...data];

    if (searchTerm) {
      result = result.filter(item =>
        columns.some(column => {
          const value = item[column.key as keyof T];
          return value && value.toString().toLowerCase().includes(searchTerm.toLowerCase());
        })
      );
    }

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        result = result.filter(item => {
          const itemValue = item[key as keyof T];
          if (Array.isArray(value)) {
            return value.includes(itemValue);
          }
          return itemValue === value;
        });
      }
    });

    return result;
  }, [data, searchTerm, filters, columns]);

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      const allIds = filteredData.map(item => item.id).filter((id): id is string | number => id !== undefined);
      setSelectedItems(new Set(allIds));
      onSelectionChange?.(filteredData);
    } else {
      setSelectedItems(new Set());
      onSelectionChange?.([]);
    }
  };

  const handleSelectItem = (item: T, checked: boolean) => {
    if (!item.id) return;

    const newSelected = new Set(selectedItems);
    if (checked) {
      newSelected.add(item.id);
    } else {
      newSelected.delete(item.id);
    }
    setSelectedItems(newSelected);

    const selectedData = data.filter(item => item.id && newSelected.has(item.id));
    onSelectionChange?.(selectedData);
  };

  if (loading) {
    return (
      <div className={cn("animate-pulse", className)}>
        <div className="h-8 bg-gray-200 rounded mb-4"></div>
        <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-${gridCols} gap-6`}>
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-48 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={cn("space-y-6", className)}>
      {/* Controls */}
      {(searchable || filterable || selectable) && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            {searchable && (
              <div className="flex-1">
                <div className="relative">
                  <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
                  />
                </div>
              </div>
            )}
            
            {filterable && (
              <div className="flex gap-2">
                <button className="flex items-center px-3 py-2 text-sm text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
                  <FunnelIcon className="h-4 w-4 mr-2" />
                  Filters
                </button>
              </div>
            )}
            
            {selectable && (
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedItems.size === filteredData.length && filteredData.length > 0}
                  onChange={(e) => handleSelectAll(e.target.checked)}
                  className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300 rounded mr-2"
                />
                <span className="text-sm text-gray-600">Select All</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Grid */}
      {filteredData.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          {emptyMessage}
        </div>
      ) : (
        <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-${gridCols} gap-6`}>
          {filteredData.map((item, index) => (
            <div key={item.id || index} className="relative">
              {selectable && (
                <div className="absolute top-2 right-2 z-10">
                  <input
                    type="checkbox"
                    checked={item.id ? selectedItems.has(item.id) : false}
                    onChange={(e) => handleSelectItem(item, e.target.checked)}
                    className="h-4 w-4 text-op-blue focus:ring-op-blue border-gray-300 rounded"
                  />
                </div>
              )}
              {cardRenderer(item)}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// List Component
interface ListProps<T> {
  data: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor?: (item: T, index: number) => string | number;
  emptyMessage?: string;
  loading?: boolean;
  className?: string;
  itemClassName?: string;
}

export function List<T>({
  data,
  renderItem,
  keyExtractor = (_, index) => index,
  emptyMessage = "No items available",
  loading = false,
  className = "",
  itemClassName = ""
}: ListProps<T>) {
  if (loading) {
    return (
      <div className={cn("animate-pulse space-y-3", className)}>
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-200 rounded"></div>
        ))}
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className={cn("text-center py-12 text-gray-500", className)}>
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className={cn("space-y-3", className)}>
      {data.map((item, index) => (
        <div key={keyExtractor(item, index)} className={itemClassName}>
          {renderItem(item, index)}
        </div>
      ))}
    </div>
  );
}

// Stats Component
interface StatItem {
  label: string;
  value: string | number;
  change?: {
    value: number;
    type: 'increase' | 'decrease';
  };
  icon?: ReactNode;
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple' | 'gray';
}

interface StatsProps {
  items: StatItem[];
  columns?: number;
  className?: string;
}

export function Stats({ 
  items, 
  columns = 4, 
  className = "" 
}: StatsProps) {
  const getColorClasses = (color: StatItem['color'] = 'blue') => {
    const colors = {
      blue: 'bg-blue-50 text-blue-600',
      green: 'bg-green-50 text-green-600',
      red: 'bg-red-50 text-red-600',
      yellow: 'bg-yellow-50 text-yellow-600',
      purple: 'bg-purple-50 text-purple-600',
      gray: 'bg-gray-50 text-gray-600'
    };
    return colors[color];
  };

  const getChangeIcon = (type: 'increase' | 'decrease') => {
    return type === 'increase' ? (
      <ArrowUpIcon className="h-4 w-4 text-green-600" />
    ) : (
      <ArrowDownIcon className="h-4 w-4 text-red-600" />
    );
  };

  return (
    <div className={cn("grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6", className)}>
      {items.map((item, index) => (
        <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{item.label}</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{item.value}</p>
              
              {item.change && (
                <div className="flex items-center mt-2">
                  {getChangeIcon(item.change.type)}
                  <span className={cn(
                    "text-sm font-medium ml-1",
                    item.change.type === 'increase' ? 'text-green-600' : 'text-red-600'
                  )}>
                    {Math.abs(item.change.value)}%
                  </span>
                  <span className="text-sm text-gray-500 ml-1">from last month</span>
                </div>
              )}
            </div>
            
            {item.icon && (
              <div className={cn("p-3 rounded-full", getColorClasses(item.color))}>
                {item.icon}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

// Chart Component
interface ChartProps {
  title?: string;
  children: ReactNode;
  className?: string;
  loading?: boolean;
  error?: string;
}

export function Chart({ 
  title, 
  children, 
  className = "",
  loading = false,
  error
}: ChartProps) {
  if (loading) {
    return (
      <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
        <div className="animate-pulse">
          {title && <div className="h-6 bg-gray-200 rounded mb-4"></div>}
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
        <div className="text-center text-red-600">
          <p className="font-medium">Chart Error</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      {title && (
        <h3 className="text-lg font-medium text-gray-900 mb-4">{title}</h3>
      )}
      {children}
    </div>
  );
}

// Progress Component
interface ProgressProps {
  value: number;
  max?: number;
  label?: string;
  showValue?: boolean;
  size?: 'sm' | 'md' | 'lg';
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple';
  className?: string;
}

export function Progress({
  value,
  max = 100,
  label,
  showValue = true,
  size = 'md',
  color = 'blue',
  className = ""
}: ProgressProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  
  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  };
  
  const colorClasses = {
    blue: 'bg-op-blue',
    green: 'bg-green-500',
    red: 'bg-red-500',
    yellow: 'bg-yellow-500',
    purple: 'bg-purple-500'
  };

  return (
    <div className={cn("space-y-2", className)}>
      {(label || showValue) && (
        <div className="flex justify-between items-center">
          {label && <span className="text-sm font-medium text-gray-700">{label}</span>}
          {showValue && (
            <span className="text-sm text-gray-500">
              {value} / {max}
            </span>
          )}
        </div>
      )}
      
      <div className={cn("w-full bg-gray-200 rounded-full overflow-hidden", sizeClasses[size])}>
        <div
          className={cn("h-full rounded-full transition-all duration-300 ease-out", colorClasses[color])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

// Metric Component
interface MetricProps {
  label: string;
  value: string | number;
  description?: string;
  trend?: {
    value: number;
    type: 'increase' | 'decrease';
    period: string;
  };
  icon?: ReactNode;
  className?: string;
}

export function Metric({
  label,
  value,
  description,
  trend,
  icon,
  className = ""
}: MetricProps) {
  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          
          {description && (
            <p className="text-sm text-gray-500 mt-1">{description}</p>
          )}
          
          {trend && (
            <div className="flex items-center mt-2">
              {trend.type === 'increase' ? (
                <ArrowUpIcon className="h-4 w-4 text-green-600" />
              ) : (
                <ArrowDownIcon className="h-4 w-4 text-red-600" />
              )}
              <span className={cn(
                "text-sm font-medium ml-1",
                trend.type === 'increase' ? 'text-green-600' : 'text-red-600'
              )}>
                {Math.abs(trend.value)}%
              </span>
              <span className="text-sm text-gray-500 ml-1">vs {trend.period}</span>
            </div>
          )}
        </div>
        
        {icon && (
          <div className="p-3 bg-op-blue-50 text-op-blue rounded-full">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}
