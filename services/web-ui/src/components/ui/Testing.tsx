'use client';

import { ReactNode, useState, useEffect, useRef } from 'react';
import { 
  PlayIcon, 
  PauseIcon, 
  StopIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  ClockIcon,
  ChartBarIcon,
  BugIcon,
  CogIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Test Result Types
export interface TestResult {
  id: string;
  name: string;
  status: 'passed' | 'failed' | 'skipped' | 'running';
  duration?: number;
  error?: string;
  stackTrace?: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface TestSuite {
  id: string;
  name: string;
  tests: TestResult[];
  status: 'passed' | 'failed' | 'skipped' | 'running';
  duration?: number;
  timestamp: Date;
}

export interface TestRun {
  id: string;
  name: string;
  suites: TestSuite[];
  status: 'running' | 'completed' | 'failed';
  startTime: Date;
  endTime?: Date;
  totalTests: number;
  passedTests: number;
  failedTests: number;
  skippedTests: number;
}

// Test Runner Component
interface TestRunnerProps {
  tests: TestResult[];
  onRun?: (tests: TestResult[]) => void;
  onStop?: () => void;
  onReset?: () => void;
  className?: string;
  autoRun?: boolean;
  showProgress?: boolean;
}

export function TestRunner({
  tests,
  onRun,
  onStop,
  onReset,
  className = "",
  autoRun = false,
  showProgress = true
}: TestRunnerProps) {
  const [isRunning, setIsRunning] = useState(false);
  const [currentTestIndex, setCurrentTestIndex] = useState(0);
  const [results, setResults] = useState<TestResult[]>(tests);
  const [progress, setProgress] = useState(0);

  const runTests = async () => {
    setIsRunning(true);
    setCurrentTestIndex(0);
    setProgress(0);

    for (let i = 0; i < tests.length; i++) {
      if (!isRunning) break;

      setCurrentTestIndex(i);
      setProgress((i / tests.length) * 100);

      // Simulate test execution
      const test = tests[i];
      const startTime = Date.now();
      
      try {
        await new Promise(resolve => setTimeout(resolve, Math.random() * 1000 + 500));
        
        const duration = Date.now() - startTime;
        const status = Math.random() > 0.2 ? 'passed' : 'failed';
        const error = status === 'failed' ? 'Test assertion failed' : undefined;
        
        const updatedTest: TestResult = {
          ...test,
          status,
          duration,
          error,
          timestamp: new Date()
        };

        setResults(prev => prev.map(t => t.id === test.id ? updatedTest : t));
      } catch (error) {
        const duration = Date.now() - startTime;
        const updatedTest: TestResult = {
          ...test,
          status: 'failed',
          duration,
          error: error instanceof Error ? error.message : 'Unknown error',
          timestamp: new Date()
        };

        setResults(prev => prev.map(t => t.id === test.id ? updatedTest : t));
      }
    }

    setIsRunning(false);
    setProgress(100);
    onRun?.(results);
  };

  const stopTests = () => {
    setIsRunning(false);
    onStop?.();
  };

  const resetTests = () => {
    setResults(tests);
    setCurrentTestIndex(0);
    setProgress(0);
    onReset?.();
  };

  useEffect(() => {
    if (autoRun && !isRunning) {
      runTests();
    }
  }, [autoRun]);

  const passedCount = results.filter(t => t.status === 'passed').length;
  const failedCount = results.filter(t => t.status === 'failed').length;
  const skippedCount = results.filter(t => t.status === 'skipped').length;

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Test Runner</h3>
          <p className="text-sm text-gray-500">
            {results.length} tests • {passedCount} passed • {failedCount} failed • {skippedCount} skipped
          </p>
        </div>
        
        <div className="flex space-x-2">
          {!isRunning ? (
            <button
              onClick={runTests}
              className="flex items-center px-4 py-2 bg-op-blue text-white rounded-md hover:bg-op-blue-700 transition-colors"
            >
              <PlayIcon className="h-4 w-4 mr-2" />
              Run Tests
            </button>
          ) : (
            <button
              onClick={stopTests}
              className="flex items-center px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              <StopIcon className="h-4 w-4 mr-2" />
              Stop
            </button>
          )}
          
          <button
            onClick={resetTests}
            className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
          >
            <CogIcon className="h-4 w-4 mr-2" />
            Reset
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      {showProgress && (
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Progress</span>
            <span className="text-sm text-gray-500">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-op-blue h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Test Results */}
      <div className="space-y-3">
        {results.map((test, index) => (
          <TestResultItem
            key={test.id}
            test={test}
            isRunning={isRunning && index === currentTestIndex}
            isCurrent={index === currentTestIndex}
          />
        ))}
      </div>
    </div>
  );
}

// Test Result Item Component
interface TestResultItemProps {
  test: TestResult;
  isRunning?: boolean;
  isCurrent?: boolean;
  className?: string;
}

export function TestResultItem({
  test,
  isRunning = false,
  isCurrent = false,
  className = ""
}: TestResultItemProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getStatusIcon = () => {
    switch (test.status) {
      case 'passed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'failed':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      case 'skipped':
        return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
      case 'running':
        return <ClockIcon className="h-5 w-5 text-blue-500 animate-spin" />;
      default:
        return <InformationCircleIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = () => {
    switch (test.status) {
      case 'passed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'skipped':
        return 'bg-yellow-100 text-yellow-800';
      case 'running':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className={cn(
      "border border-gray-200 rounded-lg p-4 transition-all",
      isCurrent && "ring-2 ring-op-blue ring-opacity-50",
      className
    )}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <h4 className="text-sm font-medium text-gray-900">{test.name}</h4>
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <span className={cn("px-2 py-1 rounded-full", getStatusColor())}>
                {test.status}
              </span>
              {test.duration && (
                <span>{test.duration}ms</span>
              )}
              <span>{test.timestamp.toLocaleTimeString()}</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {test.error && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-xs text-red-600 hover:text-red-800 transition-colors"
            >
              {isExpanded ? 'Hide' : 'Show'} Error
            </button>
          )}
        </div>
      </div>

      {/* Error Details */}
      {isExpanded && test.error && (
        <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-md">
          <h5 className="text-sm font-medium text-red-800 mb-2">Error Details</h5>
          <p className="text-sm text-red-700 mb-2">{test.error}</p>
          {test.stackTrace && (
            <details className="text-xs text-red-600">
              <summary className="cursor-pointer hover:text-red-800">Stack Trace</summary>
              <pre className="mt-2 p-2 bg-red-100 rounded overflow-x-auto">
                {test.stackTrace}
              </pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
}

// Test Suite Component
interface TestSuiteProps {
  suite: TestSuite;
  onRunSuite?: (suite: TestSuite) => void;
  className?: string;
}

export function TestSuite({
  suite,
  onRunSuite,
  className = ""
}: TestSuiteProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getStatusIcon = () => {
    switch (suite.status) {
      case 'passed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'failed':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      case 'skipped':
        return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
      case 'running':
        return <ClockIcon className="h-5 w-5 text-blue-500 animate-spin" />;
      default:
        return <InformationCircleIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = () => {
    switch (suite.status) {
      case 'passed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'skipped':
        return 'bg-yellow-100 text-yellow-800';
      case 'running':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const passedCount = suite.tests.filter(t => t.status === 'passed').length;
  const failedCount = suite.tests.filter(t => t.status === 'failed').length;
  const skippedCount = suite.tests.filter(t => t.status === 'skipped').length;

  return (
    <div className={cn("border border-gray-200 rounded-lg", className)}>
      <div className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {getStatusIcon()}
            <div>
              <h4 className="text-sm font-medium text-gray-900">{suite.name}</h4>
              <div className="flex items-center space-x-2 text-xs text-gray-500">
                <span className={cn("px-2 py-1 rounded-full", getStatusColor())}>
                  {suite.status}
                </span>
                <span>{suite.tests.length} tests</span>
                <span>• {passedCount} passed</span>
                <span>• {failedCount} failed</span>
                <span>• {skippedCount} skipped</span>
                {suite.duration && <span>• {suite.duration}ms</span>}
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-xs text-gray-600 hover:text-gray-800 transition-colors"
            >
              {isExpanded ? 'Hide' : 'Show'} Tests
            </button>
            
            {onRunSuite && (
              <button
                onClick={() => onRunSuite(suite)}
                className="text-xs text-op-blue hover:text-op-blue-800 transition-colors"
              >
                Run Suite
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Test Results */}
      {isExpanded && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          <div className="space-y-2">
            {suite.tests.map((test) => (
              <TestResultItem
                key={test.id}
                test={test}
                className="bg-white"
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Test Dashboard Component
interface TestDashboardProps {
  testRun: TestRun;
  className?: string;
}

export function TestDashboard({
  testRun,
  className = ""
}: TestDashboardProps) {
  const getStatusIcon = () => {
    switch (testRun.status) {
      case 'running':
        return <ClockIcon className="h-8 w-8 text-blue-500 animate-spin" />;
      case 'completed':
        return <CheckCircleIcon className="h-8 w-8 text-green-500" />;
      case 'failed':
        return <XCircleIcon className="h-8 w-8 text-red-500" />;
      default:
        return <InformationCircleIcon className="h-8 w-8 text-gray-500" />;
    }
  };

  const getStatusColor = () => {
    switch (testRun.status) {
      case 'running':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const totalDuration = testRun.endTime && testRun.startTime 
    ? testRun.endTime.getTime() - testRun.startTime.getTime()
    : undefined;

  const successRate = testRun.totalTests > 0 
    ? (testRun.passedTests / testRun.totalTests) * 100
    : 0;

  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200 p-6", className)}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <h3 className="text-lg font-medium text-gray-900">{testRun.name}</h3>
            <p className="text-sm text-gray-500">
              Started at {testRun.startTime.toLocaleString()}
            </p>
          </div>
        </div>
        
        <span className={cn("px-3 py-1 rounded-full text-sm font-medium", getStatusColor())}>
          {testRun.status}
        </span>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-gray-900">{testRun.totalTests}</div>
          <div className="text-sm text-gray-500">Total Tests</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{testRun.passedTests}</div>
          <div className="text-sm text-gray-500">Passed</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-red-600">{testRun.failedTests}</div>
          <div className="text-sm text-gray-500">Failed</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-600">{testRun.skippedTests}</div>
          <div className="text-sm text-gray-500">Skipped</div>
        </div>
      </div>

      {/* Progress and Duration */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Success Rate</span>
            <span className="text-sm text-gray-500">{successRate.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-green-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${successRate}%` }}
            />
          </div>
        </div>
        
        {totalDuration && (
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">
              {Math.round(totalDuration / 1000)}s
            </div>
            <div className="text-sm text-gray-500">Total Duration</div>
          </div>
        )}
      </div>

      {/* Test Suites */}
      <div className="space-y-4">
        <h4 className="text-sm font-medium text-gray-900">Test Suites</h4>
        {testRun.suites.map((suite) => (
          <TestSuite key={suite.id} suite={suite} />
        ))}
      </div>
    </div>
  );
}

// Test Debugger Component
interface TestDebuggerProps {
  test: TestResult;
  onDebug?: (test: TestResult) => void;
  className?: string;
}

export function TestDebugger({
  test,
  onDebug,
  className = ""
}: TestDebuggerProps) {
  const [isDebugging, setIsDebugging] = useState(false);
  const [debugInfo, setDebugInfo] = useState<any>(null);

  const startDebugging = async () => {
    setIsDebugging(true);
    
    // Simulate debugging process
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setDebugInfo({
      variables: {
        input: 'test input',
        expected: 'expected output',
        actual: 'actual output'
      },
      callStack: [
        'testFunction() at test.js:15',
        'runTest() at test.js:25',
        'executeSuite() at test.js:35'
      ],
      environment: {
        nodeVersion: '18.0.0',
        platform: 'darwin',
        memory: '512MB'
      }
    });
    
    setIsDebugging(false);
  };

  if (test.status !== 'failed') {
    return null;
  }

  return (
    <div className={cn("border border-red-200 rounded-lg p-4 bg-red-50", className)}>
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-sm font-medium text-red-800">Debug Information</h4>
        <button
          onClick={startDebugging}
          disabled={isDebugging}
          className="flex items-center px-3 py-1 bg-red-600 text-white text-xs rounded hover:bg-red-700 disabled:opacity-50 transition-colors"
        >
          <BugIcon className="h-3 w-3 mr-1" />
          {isDebugging ? 'Debugging...' : 'Debug'}
        </button>
      </div>

      {isDebugging && (
        <div className="text-center py-4">
          <div className="animate-spin h-6 w-6 border-2 border-red-600 border-t-transparent rounded-full mx-auto mb-2"></div>
          <p className="text-sm text-red-600">Analyzing test failure...</p>
        </div>
      )}

      {debugInfo && (
        <div className="space-y-4">
          <div>
            <h5 className="text-xs font-medium text-red-700 mb-2">Variables</h5>
            <div className="bg-white p-3 rounded border border-red-200">
              <pre className="text-xs text-red-800 overflow-x-auto">
                {JSON.stringify(debugInfo.variables, null, 2)}
              </pre>
            </div>
          </div>

          <div>
            <h5 className="text-xs font-medium text-red-700 mb-2">Call Stack</h5>
            <div className="bg-white p-3 rounded border border-red-200">
              <div className="space-y-1">
                {debugInfo.callStack.map((call, index) => (
                  <div key={index} className="text-xs text-red-800 font-mono">
                    {call}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div>
            <h5 className="text-xs font-medium text-red-700 mb-2">Environment</h5>
            <div className="bg-white p-3 rounded border border-red-200">
              <pre className="text-xs text-red-800 overflow-x-auto">
                {JSON.stringify(debugInfo.environment, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
