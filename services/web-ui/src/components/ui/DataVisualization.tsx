'use client';

import { ReactNode, useState, useEffect, useRef } from 'react';
import { 
  ChartBarIcon,
  ChartPieIcon,
  ChartBarSquareIcon,
  PresentationChartLineIcon,
  TableCellsIcon,
  MapIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowDownTrayIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Chart Data Types
export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
  metadata?: Record<string, any>;
}

export interface ChartSeries {
  name: string;
  data: ChartDataPoint[];
  color?: string;
  type?: 'line' | 'bar' | 'area';
}

export interface ChartConfig {
  title?: string;
  subtitle?: string;
  type: 'bar' | 'line' | 'pie' | 'doughnut' | 'area' | 'scatter';
  height?: number;
  width?: number;
  showLegend?: boolean;
  showGrid?: boolean;
  showTooltip?: boolean;
  animate?: boolean;
  responsive?: boolean;
}

// Bar Chart Component
interface BarChartProps {
  data: ChartDataPoint[];
  config?: Partial<ChartConfig>;
  className?: string;
  onDataPointClick?: (point: ChartDataPoint) => void;
}

export function BarChart({
  data,
  config = {},
  className = "",
  onDataPointClick
}: BarChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const defaultConfig: ChartConfig = {
    type: 'bar',
    height: 300,
    showLegend: true,
    showGrid: true,
    showTooltip: true,
    animate: true,
    responsive: true,
    ...config
  };

  const maxValue = Math.max(...data.map(d => d.value));
  const minValue = Math.min(...data.map(d => d.value));

  useEffect(() => {
    if (defaultConfig.animate) {
      setIsAnimating(true);
      const timer = setTimeout(() => setIsAnimating(false), 1000);
      return () => clearTimeout(timer);
    }
  }, [data, defaultConfig.animate]);

  const getBarColor = (index: number, point: ChartDataPoint) => {
    if (hoveredIndex === index) {
      return point.color || '#3B82F6';
    }
    return point.color || '#E5E7EB';
  };

  const getBarHeight = (value: number) => {
    if (maxValue === minValue) return 50;
    return ((value - minValue) / (maxValue - minValue)) * 100;
  };

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      {/* Header */}
      {defaultConfig.title && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900">{defaultConfig.title}</h3>
          {defaultConfig.subtitle && (
            <p className="text-sm text-gray-500">{defaultConfig.subtitle}</p>
          )}
        </div>
      )}

      {/* Chart Container */}
      <div 
        className="relative"
        style={{ height: defaultConfig.height }}
      >
        {/* Grid Lines */}
        {defaultConfig.showGrid && (
          <div className="absolute inset-0 flex flex-col justify-between">
            {[0, 25, 50, 75, 100].map((percent) => (
              <div
                key={percent}
                className="border-t border-gray-200"
                style={{ top: `${percent}%` }}
              />
            ))}
          </div>
        )}

        {/* Bars */}
        <div className="relative h-full flex items-end justify-between space-x-2 px-4">
          {data.map((point, index) => (
            <div
              key={index}
              className="relative flex-1 flex flex-col items-center"
              onMouseEnter={() => setHoveredIndex(index)}
              onMouseLeave={() => setHoveredIndex(null)}
              onClick={() => onDataPointClick?.(point)}
            >
              {/* Bar */}
              <div
                className={cn(
                  "w-full rounded-t transition-all duration-500 cursor-pointer",
                  isAnimating && "animate-pulse"
                )}
                style={{
                  height: `${getBarHeight(point.value)}%`,
                  backgroundColor: getBarColor(index, point),
                  transform: isAnimating ? 'scaleY(0)' : 'scaleY(1)',
                  transformOrigin: 'bottom'
                }}
              />

              {/* Value Label */}
              <div className="absolute -top-8 left-1/2 transform -translate-x-1/2">
                <span className="text-xs font-medium text-gray-700 bg-white px-2 py-1 rounded shadow-sm">
                  {point.value}
                </span>
              </div>

              {/* X-Axis Label */}
              <div className="mt-2 text-xs text-gray-600 text-center">
                {point.label}
              </div>
            </div>
          ))}
        </div>

        {/* Y-Axis Labels */}
        <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-500">
          {[100, 75, 50, 25, 0].map((percent) => (
            <span key={percent}>
              {Math.round(minValue + (percent / 100) * (maxValue - minValue))}
            </span>
          ))}
        </div>
      </div>

      {/* Legend */}
      {defaultConfig.showLegend && data.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-4">
          {data.map((point, index) => (
            <div key={index} className="flex items-center space-x-2">
              <div
                className="w-3 h-3 rounded"
                style={{ backgroundColor: point.color || '#E5E7EB' }}
              />
              <span className="text-sm text-gray-600">{point.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Line Chart Component
interface LineChartProps {
  series: ChartSeries[];
  config?: Partial<ChartConfig>;
  className?: string;
  onDataPointClick?: (point: ChartDataPoint, seriesIndex: number) => void;
}

export function LineChart({
  series,
  config = {},
  className = "",
  onDataPointClick
}: LineChartProps) {
  const [hoveredPoint, setHoveredPoint] = useState<{ index: number; seriesIndex: number } | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const defaultConfig: ChartConfig = {
    type: 'line',
    height: 300,
    showLegend: true,
    showGrid: true,
    showTooltip: true,
    animate: true,
    responsive: true,
    ...config
  };

  const allDataPoints = series.flatMap(s => s.data);
  const maxValue = Math.max(...allDataPoints.map(d => d.value));
  const minValue = Math.min(...allDataPoints.map(d => d.value));

  useEffect(() => {
    if (defaultConfig.animate) {
      setIsAnimating(true);
      const timer = setTimeout(() => setIsAnimating(false), 1000);
      return () => clearTimeout(timer);
    }
  }, [series, defaultConfig.animate]);

  const getPointPosition = (value: number, index: number) => {
    const x = (index / (series[0]?.data.length - 1)) * 100;
    const y = 100 - ((value - minValue) / (maxValue - minValue)) * 100;
    return { x, y };
  };

  const generatePath = (data: ChartDataPoint[]) => {
    if (data.length < 2) return '';
    
    const points = data.map((point, index) => {
      const pos = getPointPosition(point.value, index);
      return `${pos.x}% ${pos.y}%`;
    });
    
    return `M ${points.join(' L ')}`;
  };

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      {/* Header */}
      {defaultConfig.title && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900">{defaultConfig.title}</h3>
          {defaultConfig.subtitle && (
            <p className="text-sm text-gray-500">{defaultConfig.subtitle}</p>
          )}
        </div>
      )}

      {/* Chart Container */}
      <div 
        className="relative"
        style={{ height: defaultConfig.height }}
      >
        {/* Grid Lines */}
        {defaultConfig.showGrid && (
          <div className="absolute inset-0 flex flex-col justify-between">
            {[0, 25, 50, 75, 100].map((percent) => (
              <div
                key={percent}
                className="border-t border-gray-200"
                style={{ top: `${percent}%` }}
              />
            ))}
          </div>
        )}

        {/* SVG Container */}
        <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          {/* Lines */}
          {series.map((s, seriesIndex) => (
            <g key={seriesIndex}>
              <path
                d={generatePath(s.data)}
                fill="none"
                stroke={s.color || '#3B82F6'}
                strokeWidth="2"
                className={cn(
                  "transition-all duration-500",
                  isAnimating && "stroke-dasharray-1000 stroke-dashoffset-1000"
                )}
                style={{
                  strokeDasharray: isAnimating ? 1000 : 0,
                  strokeDashoffset: isAnimating ? 1000 : 0
                }}
              />
              
              {/* Data Points */}
              {s.data.map((point, index) => {
                const pos = getPointPosition(point.value, index);
                const isHovered = hoveredPoint?.index === index && hoveredPoint?.seriesIndex === seriesIndex;
                
                return (
                  <circle
                    key={index}
                    cx={`${pos.x}%`}
                    cy={`${pos.y}%`}
                    r={isHovered ? 6 : 4}
                    fill={s.color || '#3B82F6'}
                    className="transition-all duration-200 cursor-pointer"
                    onMouseEnter={() => setHoveredPoint({ index, seriesIndex })}
                    onMouseLeave={() => setHoveredPoint(null)}
                    onClick={() => onDataPointClick?.(point, seriesIndex)}
                  />
                );
              })}
            </g>
          ))}
        </svg>

        {/* X-Axis Labels */}
        <div className="absolute bottom-0 left-0 right-0 flex justify-between px-4">
          {series[0]?.data.map((point, index) => (
            <span key={index} className="text-xs text-gray-600">
              {point.label}
            </span>
          ))}
        </div>

        {/* Y-Axis Labels */}
        <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-500">
          {[100, 75, 50, 25, 0].map((percent) => (
            <span key={percent}>
              {Math.round(minValue + (percent / 100) * (maxValue - minValue))}
            </span>
          ))}
        </div>
      </div>

      {/* Legend */}
      {defaultConfig.showLegend && series.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-4">
          {series.map((s, index) => (
            <div key={index} className="flex items-center space-x-2">
              <div
                className="w-3 h-3 rounded"
                style={{ backgroundColor: s.color || '#3B82F6' }}
              />
              <span className="text-sm text-gray-600">{s.name}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Pie Chart Component
interface PieChartProps {
  data: ChartDataPoint[];
  config?: Partial<ChartConfig>;
  className?: string;
  onSliceClick?: (point: ChartDataPoint) => void;
}

export function PieChart({
  data,
  config = {},
  className = "",
  onSliceClick
}: PieChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const defaultConfig: ChartConfig = {
    type: 'pie',
    height: 300,
    showLegend: true,
    animate: true,
    responsive: true,
    ...config
  };

  const total = data.reduce((sum, point) => sum + point.value, 0);

  useEffect(() => {
    if (defaultConfig.animate) {
      setIsAnimating(true);
      const timer = setTimeout(() => setIsAnimating(false), 1000);
      return () => clearTimeout(timer);
    }
  }, [data, defaultConfig.animate]);

  const generatePieSlice = (startAngle: number, endAngle: number, radius: number) => {
    const x1 = radius * Math.cos(startAngle);
    const y1 = radius * Math.sin(startAngle);
    const x2 = radius * Math.cos(endAngle);
    const y2 = radius * Math.sin(endAngle);
    
    const largeArcFlag = endAngle - startAngle > Math.PI ? 1 : 0;
    
    return [
      `M 0 0`,
      `L ${x1} ${y1}`,
      `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
      'Z'
    ].join(' ');
  };

  const radius = 80;
  let currentAngle = -Math.PI / 2; // Start from top

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      {/* Header */}
      {defaultConfig.title && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900">{defaultConfig.title}</h3>
          {defaultConfig.subtitle && (
            <p className="text-sm text-gray-500">{defaultConfig.subtitle}</p>
          )}
        </div>
      )}

      {/* Chart Container */}
      <div className="flex items-center justify-center">
        <div className="relative" style={{ height: defaultConfig.height }}>
          <svg
            width={defaultConfig.height}
            height={defaultConfig.height}
            viewBox="-100 -100 200 200"
            className={cn(
              "transition-all duration-500",
              isAnimating && "scale-0"
            )}
          >
            {data.map((point, index) => {
              const percentage = point.value / total;
              const sliceAngle = percentage * 2 * Math.PI;
              const endAngle = currentAngle + sliceAngle;
              
              const slice = generatePieSlice(currentAngle, endAngle, radius);
              const isHovered = hoveredIndex === index;
              
              const sliceElement = (
                <path
                  key={index}
                  d={slice}
                  fill={point.color || `hsl(${(index * 137.5) % 360}, 70%, 60%)`}
                  className={cn(
                    "transition-all duration-200 cursor-pointer",
                    isHovered && "opacity-80"
                  )}
                  onMouseEnter={() => setHoveredIndex(index)}
                  onMouseLeave={() => setHoveredIndex(null)}
                  onClick={() => onSliceClick?.(point)}
                  style={{
                    transform: isHovered ? 'scale(1.05)' : 'scale(1)',
                    transformOrigin: 'center'
                  }}
                />
              );
              
              currentAngle = endAngle;
              return sliceElement;
            })}
          </svg>

          {/* Center Label */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{total}</div>
              <div className="text-sm text-gray-500">Total</div>
            </div>
          </div>
        </div>
      </div>

      {/* Legend */}
      {defaultConfig.showLegend && data.length > 0 && (
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3">
          {data.map((point, index) => {
            const percentage = ((point.value / total) * 100).toFixed(1);
            const isHovered = hoveredIndex === index;
            
            return (
              <div
                key={index}
                className={cn(
                  "flex items-center space-x-3 p-2 rounded transition-all duration-200",
                  isHovered && "bg-gray-50"
                )}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                <div
                  className="w-4 h-4 rounded"
                  style={{ backgroundColor: point.color || `hsl(${(index * 137.5) % 360}, 70%, 60%)` }}
                />
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">{point.label}</div>
                  <div className="text-xs text-gray-500">{point.value} ({percentage}%)</div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// Data Table Component
interface DataTableProps {
  data: Record<string, any>[];
  columns: {
    key: string;
    label: string;
    render?: (value: any, row: Record<string, any>) => ReactNode;
    sortable?: boolean;
    width?: string;
  }[];
  config?: {
    title?: string;
    subtitle?: string;
    searchable?: boolean;
    sortable?: boolean;
    pagination?: boolean;
    pageSize?: number;
    exportable?: boolean;
  };
  className?: string;
  onRowClick?: (row: Record<string, any>) => void;
}

export function DataTable({
  data,
  columns,
  config = {},
  className = "",
  onRowClick
}: DataTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [currentPage, setCurrentPage] = useState(1);
  
  const defaultConfig = {
    searchable: true,
    sortable: true,
    pagination: true,
    pageSize: 10,
    exportable: true,
    ...config
  };

  // Filter data
  const filteredData = data.filter(row =>
    Object.values(row).some(value =>
      String(value).toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  // Sort data
  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortColumn) return 0;
    
    const aVal = a[sortColumn];
    const bVal = b[sortColumn];
    
    if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
    return 0;
  });

  // Paginate data
  const totalPages = Math.ceil(sortedData.length / defaultConfig.pageSize);
  const startIndex = (currentPage - 1) * defaultConfig.pageSize;
  const paginatedData = sortedData.slice(startIndex, startIndex + defaultConfig.pageSize);

  const handleSort = (columnKey: string) => {
    if (!defaultConfig.sortable) return;
    
    if (sortColumn === columnKey) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(columnKey);
      setSortDirection('asc');
    }
  };

  const exportData = () => {
    const csvContent = [
      columns.map(col => col.label).join(','),
      ...paginatedData.map(row => 
        columns.map(col => JSON.stringify(row[col.key])).join(',')
      )
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'data-export.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200", className)}>
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            {defaultConfig.title && (
              <h3 className="text-lg font-medium text-gray-900">{defaultConfig.title}</h3>
            )}
            {defaultConfig.subtitle && (
              <p className="text-sm text-gray-500">{defaultConfig.subtitle}</p>
            )}
          </div>
          
          <div className="flex items-center space-x-2">
            {defaultConfig.exportable && (
              <button
                onClick={exportData}
                className="flex items-center px-3 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
              >
                <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
                Export
              </button>
            )}
          </div>
        </div>

        {/* Search */}
        {defaultConfig.searchable && (
          <div className="mt-4">
            <div className="relative">
              <input
                type="text"
                placeholder="Search data..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <TableCellsIcon className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  scope="col"
                  className={cn(
                    "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    column.sortable && "cursor-pointer hover:bg-gray-100",
                    column.width
                  )}
                  onClick={() => column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center space-x-1">
                    <span>{column.label}</span>
                    {column.sortable && sortColumn === column.key && (
                      <span className="text-gray-400">
                        {sortDirection === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className={cn(
                  "hover:bg-gray-50 transition-colors",
                  onRowClick && "cursor-pointer"
                )}
                onClick={() => onRowClick?.(row)}
              >
                {columns.map((column) => (
                  <td key={column.key} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {column.render ? column.render(row[column.key], row) : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {defaultConfig.pagination && totalPages > 1 && (
        <div className="px-6 py-4 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-700">
              Showing {startIndex + 1} to {Math.min(startIndex + defaultConfig.pageSize, sortedData.length)} of {sortedData.length} results
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Previous
              </button>
              
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  className={cn(
                    "px-3 py-2 text-sm rounded transition-colors",
                    currentPage === page
                      ? "bg-op-blue text-white"
                      : "text-gray-600 hover:text-gray-800 hover:bg-gray-100"
                  )}
                >
                  {page}
                </button>
              ))}
              
              <button
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Stats Grid Component
interface StatsGridProps {
  stats: {
    title: string;
    value: string | number;
    change?: {
      value: number;
      type: 'increase' | 'decrease' | 'neutral';
    };
    icon?: ReactNode;
    color?: string;
  }[];
  config?: {
    title?: string;
    subtitle?: string;
    columns?: 2 | 3 | 4;
    showIcons?: boolean;
    animate?: boolean;
  };
  className?: string;
}

export function StatsGrid({
  stats,
  config = {},
  className = ""
}: StatsGridProps) {
  const [isVisible, setIsVisible] = useState(false);
  
  const defaultConfig = {
    columns: 4,
    showIcons: true,
    animate: true,
    ...config
  };

  useEffect(() => {
    if (defaultConfig.animate) {
      const timer = setTimeout(() => setIsVisible(true), 100);
      return () => clearTimeout(timer);
    } else {
      setIsVisible(true);
    }
  }, [defaultConfig.animate]);

  const gridCols = {
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
  };

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      {/* Header */}
      {defaultConfig.title && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900">{defaultConfig.title}</h3>
          {defaultConfig.subtitle && (
            <p className="text-sm text-gray-500">{defaultConfig.subtitle}</p>
          )}
        </div>
      )}

      {/* Stats Grid */}
      <div className={cn("grid gap-6", gridCols[defaultConfig.columns])}>
        {stats.map((stat, index) => (
          <div
            key={index}
            className={cn(
              "text-center transition-all duration-500",
              isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
            )}
            style={{
              transitionDelay: `${index * 100}ms`
            }}
          >
            {defaultConfig.showIcons && stat.icon && (
              <div className="mx-auto mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-gray-100">
                {stat.icon}
              </div>
            )}
            
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {stat.value}
            </div>
            
            <div className="text-sm text-gray-500 mb-2">
              {stat.title}
            </div>
            
            {stat.change && (
              <div className={cn(
                "text-xs font-medium",
                stat.change.type === 'increase' && "text-green-600",
                stat.change.type === 'decrease' && "text-red-600",
                stat.change.type === 'neutral' && "text-gray-600"
              )}>
                {stat.change.type === 'increase' && '+'}
                {stat.change.value}%
                {stat.change.type === 'increase' && ' ↑'}
                {stat.change.type === 'decrease' && ' ↓'}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
