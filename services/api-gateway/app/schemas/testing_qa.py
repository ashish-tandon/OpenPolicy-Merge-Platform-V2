"""
Testing and Quality Assurance Schemas for OpenPolicy V2

Comprehensive Pydantic schemas for testing and quality assurance system.
Implements P2 priority feature for enhanced system quality and reliability.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class SuiteCategoryEnum(str, Enum):
    """Test suite category enumeration."""
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ACCESSIBILITY = "accessibility"
    API = "api"
    UI = "ui"


class TestFrameworkEnum(str, Enum):
    """Test framework enumeration."""
    PYTEST = "pytest"
    JEST = "jest"
    CYPRESS = "cypress"
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"
    JUNIT = "junit"
    NUNIT = "nunit"
    MSTEST = "mstest"
    CUSTOM = "custom"


class ExecutionFrequencyEnum(str, Enum):
    """Execution frequency enumeration."""
    ON_COMMIT = "on_commit"
    DAILY = "daily"
    WEEKLY = "weekly"
    MANUAL = "manual"
    CONTINUOUS = "continuous"
    ON_DEMAND = "on_demand"


class TestTypeEnum(str, Enum):
    """Test type enumeration."""
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ACCESSIBILITY = "accessibility"
    USABILITY = "usability"
    COMPATIBILITY = "compatibility"
    LOCALIZATION = "localization"
    EXPLORATORY = "exploratory"


class PriorityEnum(str, Enum):
    """Priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplexityEnum(str, Enum):
    """Complexity enumeration."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class RunTypeEnum(str, Enum):
    """Test run type enumeration."""
    SCHEDULED = "scheduled"
    MANUAL = "manual"
    TRIGGERED = "triggered"
    CI_CD = "ci_cd"
    WEBHOOK = "webhook"
    API = "api"


class TestStatusEnum(str, Enum):
    """Test status enumeration."""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    ERROR = "error"


class TestResultStatusEnum(str, Enum):
    """Test result status enumeration."""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"
    BLOCKED = "blocked"


class EnvironmentTypeEnum(str, Enum):
    """Environment type enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    CI = "ci"
    TESTING = "testing"
    DEMO = "demo"


class ReportTypeEnum(str, Enum):
    """Report type enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"
    REAL_TIME = "real_time"
    ON_DEMAND = "on_demand"


class CoverageTypeEnum(str, Enum):
    """Coverage type enumeration."""
    LINE = "line"
    BRANCH = "branch"
    FUNCTION = "function"
    STATEMENT = "statement"
    PATH = "path"
    CONDITION = "condition"


class MetricTypeEnum(str, Enum):
    """Metric type enumeration."""
    COVERAGE = "coverage"
    RELIABILITY = "reliability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    TESTABILITY = "testability"


class MetricCategoryEnum(str, Enum):
    """Metric category enumeration."""
    TEST = "test"
    CODE = "code"
    DEPLOYMENT = "deployment"
    USER = "user"
    BUSINESS = "business"
    TECHNICAL = "technical"


# ============================================================================
# BASE MODELS
# ============================================================================

class TestSuiteBase(BaseModel):
    """Base model for test suites."""
    model_config = ConfigDict(from_attributes=True)
    
    suite_name: str = Field(..., min_length=1, max_length=200, description="Test suite identifier")
    suite_description: Optional[str] = Field(None, description="Test suite description")
    suite_category: SuiteCategoryEnum = Field(..., description="Test suite category")
    test_framework: TestFrameworkEnum = Field(..., description="Test framework")
    is_active: bool = Field(True, description="Whether suite is active")
    is_automated: bool = Field(True, description="Whether suite is automated")
    execution_frequency: ExecutionFrequencyEnum = Field(..., description="Execution frequency")
    timeout_seconds: int = Field(300, ge=1, description="Test suite timeout")
    parallel_execution: bool = Field(False, description="Whether tests run in parallel")
    retry_count: int = Field(0, ge=0, description="Number of retries on failure")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the test suite")


class TestCaseBase(BaseModel):
    """Base model for test cases."""
    model_config = ConfigDict(from_attributes=True)
    
    test_suite_id: str = Field(..., description="Test suite ID")
    test_name: str = Field(..., min_length=1, max_length=200, description="Test case name")
    test_description: Optional[str] = Field(None, description="Test case description")
    test_type: TestTypeEnum = Field(..., description="Test type")
    priority: PriorityEnum = Field(PriorityEnum.MEDIUM, description="Test priority")
    complexity: ComplexityEnum = Field(ComplexityEnum.MEDIUM, description="Test complexity")
    estimated_duration: int = Field(60, ge=1, description="Estimated duration in seconds")
    prerequisites: Optional[str] = Field(None, description="Test prerequisites")
    test_steps: Optional[List[Dict[str, Any]]] = Field(None, description="Test execution steps")
    expected_results: Optional[str] = Field(None, description="Expected test results")
    is_data_dependent: bool = Field(False, description="Whether test depends on specific data")
    data_requirements: Optional[Dict[str, Any]] = Field(None, description="Data requirements for test")
    is_active: bool = Field(True, description="Whether test case is active")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the test case")


class TestRunBase(BaseModel):
    """Base model for test runs."""
    model_config = ConfigDict(from_attributes=True)
    
    test_suite_id: str = Field(..., description="Test suite ID")
    run_name: str = Field(..., min_length=1, max_length=200, description="Test run identifier")
    run_type: RunTypeEnum = Field(..., description="Test run type")
    trigger_source: Optional[str] = Field(None, max_length=100, description="Trigger source")
    environment: str = Field(..., max_length=100, description="Environment")
    branch_name: Optional[str] = Field(None, max_length=100, description="Git branch name")
    commit_hash: Optional[str] = Field(None, max_length=100, description="Git commit hash")
    start_time: datetime = Field(..., description="When test run started")
    end_time: Optional[datetime] = Field(None, description="When test run completed")
    status: TestStatusEnum = Field(TestStatusEnum.RUNNING, description="Test run status")
    total_tests: int = Field(0, ge=0, description="Total number of tests")
    passed_tests: int = Field(0, ge=0, description="Number of passed tests")
    failed_tests: int = Field(0, ge=0, description="Number of failed tests")
    skipped_tests: int = Field(0, ge=0, description="Number of skipped tests")
    execution_time: Optional[int] = Field(None, ge=0, description="Total execution time in seconds")
    parallel_workers: int = Field(1, ge=1, description="Number of parallel workers")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who initiated the test run")


class TestResultBase(BaseModel):
    """Base model for test results."""
    model_config = ConfigDict(from_attributes=True)
    
    test_run_id: str = Field(..., description="Test run ID")
    test_case_id: str = Field(..., description="Test case ID")
    test_name: str = Field(..., min_length=1, max_length=200, description="Test name for quick reference")
    status: TestResultStatusEnum = Field(..., description="Test result status")
    execution_time: Optional[float] = Field(None, ge=0.0, description="Test execution time in seconds")
    start_time: datetime = Field(..., description="When test started")
    end_time: Optional[datetime] = Field(None, description="When test completed")
    error_message: Optional[str] = Field(None, description="Error message if test failed")
    stack_trace: Optional[str] = Field(None, description="Stack trace if test failed")
    screenshot_path: Optional[str] = Field(None, max_length=500, description="Path to screenshot if applicable")
    log_output: Optional[str] = Field(None, description="Test log output")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional test metadata")
    retry_count: int = Field(0, ge=0, description="Number of retries attempted")


class QualityMetricBase(BaseModel):
    """Base model for quality metrics."""
    model_config = ConfigDict(from_attributes=True)
    
    metric_name: str = Field(..., min_length=1, max_length=200, description="Metric identifier")
    metric_description: Optional[str] = Field(None, description="Metric description")
    metric_type: MetricTypeEnum = Field(..., description="Metric type")
    metric_category: MetricCategoryEnum = Field(..., description="Metric category")
    target_value: Optional[float] = Field(None, description="Target value for the metric")
    current_value: float = Field(..., description="Current metric value")
    unit: Optional[str] = Field(None, max_length=50, description="Unit of measurement")
    calculation_method: str = Field(..., min_length=1, max_length=200, description="How metric is calculated")
    data_source: str = Field(..., min_length=1, max_length=200, description="Source of metric data")
    collection_frequency: str = Field(..., min_length=1, max_length=50, description="How often metric is collected")
    last_updated: datetime = Field(..., description="When metric was last updated")
    trend_direction: Optional[str] = Field(None, max_length=50, description="Trend direction")
    is_critical: bool = Field(False, description="Whether metric is critical")


class TestCoverageBase(BaseModel):
    """Base model for test coverage."""
    model_config = ConfigDict(from_attributes=True)
    
    test_run_id: str = Field(..., description="Test run ID")
    coverage_type: CoverageTypeEnum = Field(..., description="Coverage type")
    total_lines: int = Field(..., ge=0, description="Total lines of code")
    covered_lines: int = Field(..., ge=0, description="Lines covered by tests")
    coverage_percentage: float = Field(..., ge=0.0, le=100.0, description="Coverage percentage")
    uncovered_lines: Optional[List[int]] = Field(None, description="List of uncovered lines")
    coverage_report_path: Optional[str] = Field(None, max_length=500, description="Path to coverage report")
    coverage_timestamp: datetime = Field(..., description="When coverage was measured")


class TestEnvironmentBase(BaseModel):
    """Base model for test environments."""
    model_config = ConfigDict(from_attributes=True)
    
    environment_name: str = Field(..., min_length=1, max_length=200, description="Environment identifier")
    environment_type: EnvironmentTypeEnum = Field(..., description="Environment type")
    base_url: str = Field(..., min_length=1, max_length=500, description="Base URL for the environment")
    database_url: Optional[str] = Field(None, max_length=500, description="Database connection string")
    api_key: Optional[str] = Field(None, max_length=200, description="API key for the environment")
    environment_variables: Optional[Dict[str, Any]] = Field(None, description="Environment-specific variables")
    is_active: bool = Field(True, description="Whether environment is active")
    supports_parallel: bool = Field(False, description="Whether environment supports parallel testing")
    max_parallel_tests: int = Field(1, ge=1, description="Maximum parallel tests")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the environment")


class TestScheduleBase(BaseModel):
    """Base model for test schedules."""
    model_config = ConfigDict(from_attributes=True)
    
    schedule_name: str = Field(..., min_length=1, max_length=200, description="Schedule identifier")
    test_suite_id: str = Field(..., description="Test suite ID")
    environment_id: str = Field(..., description="Environment ID")
    cron_expression: str = Field(..., min_length=1, max_length=100, description="Cron expression for scheduling")
    timezone: str = Field("UTC", max_length=100, description="Timezone for scheduling")
    is_active: bool = Field(True, description="Whether schedule is active")
    last_run: Optional[datetime] = Field(None, description="When schedule last ran")
    next_run: Optional[datetime] = Field(None, description="When schedule will next run")
    max_retries: int = Field(3, ge=0, description="Maximum retries on failure")
    notification_channels: Optional[List[str]] = Field(None, description="Notification channels for results")
    created_by: str = Field(..., min_length=1, max_length=100, description="Who created the schedule")


class TestReportBase(BaseModel):
    """Base model for test reports."""
    model_config = ConfigDict(from_attributes=True)
    
    report_name: str = Field(..., min_length=1, max_length=200, description="Report identifier")
    report_type: ReportTypeEnum = Field(..., description="Type of report")
    report_period_start: datetime = Field(..., description="Report period start")
    report_period_end: datetime = Field(..., description="Report period end")
    test_suite_id: Optional[str] = Field(None, description="Specific test suite")
    environment_id: Optional[str] = Field(None, description="Specific environment")
    total_test_runs: int = Field(0, ge=0, description="Total test runs in period")
    total_tests_executed: int = Field(0, ge=0, description="Total tests executed")
    total_tests_passed: int = Field(0, ge=0, description="Total tests passed")
    total_tests_failed: int = Field(0, ge=0, description="Total tests failed")
    total_tests_skipped: int = Field(0, ge=0, description="Total tests skipped")
    overall_success_rate: float = Field(0.0, ge=0.0, le=100.0, description="Overall success rate percentage")
    average_execution_time: float = Field(0.0, ge=0.0, description="Average execution time")
    coverage_summary: Optional[Dict[str, Any]] = Field(None, description="Coverage summary data")
    quality_metrics: Optional[Dict[str, Any]] = Field(None, description="Quality metrics summary")
    recommendations: Optional[List[str]] = Field(None, description="Improvement recommendations")
    generated_by: str = Field(..., min_length=1, max_length=100, description="Who generated the report")
    is_automated: bool = Field(True, description="Whether report was auto-generated")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class TestSuiteCreateRequest(TestSuiteBase):
    """Request model for creating test suites."""
    pass


class TestSuiteUpdateRequest(BaseModel):
    """Request model for updating test suites."""
    suite_description: Optional[str] = None
    suite_category: Optional[SuiteCategoryEnum] = None
    test_framework: Optional[TestFrameworkEnum] = None
    is_active: Optional[bool] = None
    is_automated: Optional[bool] = None
    execution_frequency: Optional[ExecutionFrequencyEnum] = None
    timeout_seconds: Optional[int] = Field(None, ge=1)
    parallel_execution: Optional[bool] = None
    retry_count: Optional[int] = Field(None, ge=0)


class TestCaseCreateRequest(TestCaseBase):
    """Request model for creating test cases."""
    pass


class TestCaseUpdateRequest(BaseModel):
    """Request model for updating test cases."""
    test_description: Optional[str] = None
    test_type: Optional[TestTypeEnum] = None
    priority: Optional[PriorityEnum] = None
    complexity: Optional[ComplexityEnum] = None
    estimated_duration: Optional[int] = Field(None, ge=1)
    prerequisites: Optional[str] = None
    test_steps: Optional[List[Dict[str, Any]]] = None
    expected_results: Optional[str] = None
    is_data_dependent: Optional[bool] = None
    data_requirements: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class TestRunCreateRequest(TestRunBase):
    """Request model for creating test runs."""
    pass


class TestRunUpdateRequest(BaseModel):
    """Request model for updating test runs."""
    end_time: Optional[datetime] = None
    status: Optional[TestStatusEnum] = None
    total_tests: Optional[int] = Field(None, ge=0)
    passed_tests: Optional[int] = Field(None, ge=0)
    failed_tests: Optional[int] = Field(None, ge=0)
    skipped_tests: Optional[int] = Field(None, ge=0)
    execution_time: Optional[int] = Field(None, ge=0)


class TestResultCreateRequest(TestResultBase):
    """Request model for creating test results."""
    pass


class TestResultUpdateRequest(BaseModel):
    """Request model for updating test results."""
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = Field(None, ge=0.0)
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    screenshot_path: Optional[str] = Field(None, max_length=500)
    log_output: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class QualityMetricCreateRequest(QualityMetricBase):
    """Request model for creating quality metrics."""
    pass


class QualityMetricUpdateRequest(BaseModel):
    """Request model for updating quality metrics."""
    metric_description: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = Field(None, max_length=50)
    calculation_method: Optional[str] = Field(None, min_length=1, max_length=200)
    data_source: Optional[str] = Field(None, min_length=1, max_length=200)
    collection_frequency: Optional[str] = Field(None, min_length=1, max_length=50)
    trend_direction: Optional[str] = Field(None, max_length=50)
    is_critical: Optional[bool] = None


class TestEnvironmentCreateRequest(TestEnvironmentBase):
    """Request model for creating test environments."""
    pass


class TestEnvironmentUpdateRequest(BaseModel):
    """Request model for updating test environments."""
    environment_type: Optional[EnvironmentTypeEnum] = None
    base_url: Optional[str] = Field(None, min_length=1, max_length=500)
    database_url: Optional[str] = Field(None, max_length=500)
    api_key: Optional[str] = Field(None, max_length=200)
    environment_variables: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    supports_parallel: Optional[bool] = None
    max_parallel_tests: Optional[int] = Field(None, ge=1)


class TestScheduleCreateRequest(TestScheduleBase):
    """Request model for creating test schedules."""
    pass


class TestScheduleUpdateRequest(BaseModel):
    """Request model for updating test schedules."""
    cron_expression: Optional[str] = Field(None, min_length=1, max_length=100)
    timezone: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    max_retries: Optional[int] = Field(None, ge=0)
    notification_channels: Optional[List[str]] = None


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class TestSuiteResponse(TestSuiteBase):
    """Response model for test suites."""
    id: str
    created_at: datetime
    updated_at: datetime


class TestCaseResponse(TestCaseBase):
    """Response model for test cases."""
    id: str
    created_at: datetime
    updated_at: datetime


class TestRunResponse(TestRunBase):
    """Response model for test runs."""
    id: str
    created_at: datetime


class TestResultResponse(TestResultBase):
    """Response model for test results."""
    id: str
    created_at: datetime


class QualityMetricResponse(QualityMetricBase):
    """Response model for quality metrics."""
    id: str
    created_at: datetime
    updated_at: datetime


class TestCoverageResponse(TestCoverageBase):
    """Response model for test coverage."""
    id: str
    created_at: datetime


class TestEnvironmentResponse(TestEnvironmentBase):
    """Response model for test environments."""
    id: str
    created_at: datetime
    updated_at: datetime


class TestScheduleResponse(TestScheduleBase):
    """Response model for test schedules."""
    id: str
    created_at: datetime
    updated_at: datetime


class TestReportResponse(TestReportBase):
    """Response model for test reports."""
    id: str
    created_at: datetime


# ============================================================================
# LIST RESPONSE MODELS
# ============================================================================

class TestSuiteListResponse(BaseModel):
    """List response model for test suites."""
    test_suites: List[TestSuiteResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TestCaseListResponse(BaseModel):
    """List response model for test cases."""
    test_cases: List[TestCaseResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TestRunListResponse(BaseModel):
    """List response model for test runs."""
    test_runs: List[TestRunResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TestResultListResponse(BaseModel):
    """List response model for test results."""
    test_results: List[TestResultResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class QualityMetricListResponse(BaseModel):
    """List response model for quality metrics."""
    quality_metrics: List[QualityMetricResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TestCoverageListResponse(BaseModel):
    """List response model for test coverage."""
    test_coverage: List[TestCoverageResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TestEnvironmentListResponse(BaseModel):
    """List response model for test environments."""
    test_environments: List[TestEnvironmentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TestScheduleListResponse(BaseModel):
    """List response model for test schedules."""
    test_schedules: List[TestScheduleResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class TestReportListResponse(BaseModel):
    """List response model for test reports."""
    test_reports: List[TestReportResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ============================================================================
# SPECIALIZED MODELS
# ============================================================================

class TestExecutionRequest(BaseModel):
    """Request model for executing tests."""
    test_suite_id: str = Field(..., description="Test suite ID to execute")
    environment_id: str = Field(..., description="Environment ID to run tests in")
    run_type: RunTypeEnum = Field(RunTypeEnum.MANUAL, description="Type of test run")
    trigger_source: Optional[str] = Field(None, max_length=100, description="Trigger source")
    branch_name: Optional[str] = Field(None, max_length=100, description="Git branch name")
    commit_hash: Optional[str] = Field(None, max_length=100, description="Git commit hash")
    parallel_workers: int = Field(1, ge=1, description="Number of parallel workers")
    timeout_seconds: Optional[int] = Field(None, ge=1, description="Custom timeout for this run")


class TestExecutionResponse(BaseModel):
    """Response model for test execution."""
    test_run_id: str = Field(..., description="Test run ID")
    run_name: str = Field(..., description="Test run name")
    status: TestStatusEnum = Field(..., description="Test run status")
    estimated_duration: int = Field(..., description="Estimated duration in seconds")
    start_time: datetime = Field(..., description="When test run started")
    message: str = Field(..., description="Execution message")


class TestCoverageRequest(BaseModel):
    """Request model for test coverage analysis."""
    test_run_id: str = Field(..., description="Test run ID")
    coverage_type: CoverageTypeEnum = Field(..., description="Type of coverage to analyze")
    include_uncovered: bool = Field(False, description="Whether to include uncovered lines")
    coverage_threshold: Optional[float] = Field(None, ge=0.0, le=100.0, description="Coverage threshold")


class QualityReportRequest(BaseModel):
    """Request model for quality reports."""
    report_type: ReportTypeEnum = Field(..., description="Type of report")
    start_date: datetime = Field(..., description="Report start date")
    end_date: datetime = Field(..., description="Report end date")
    test_suite_id: Optional[str] = Field(None, description="Specific test suite")
    environment_id: Optional[str] = Field(None, description="Specific environment")
    include_recommendations: bool = Field(True, description="Whether to include recommendations")
    include_trends: bool = Field(True, description="Whether to include trend analysis")


class SystemQualityOverview(BaseModel):
    """Model for system quality overview."""
    total_test_suites: int = Field(..., description="Total test suites")
    active_test_suites: int = Field(..., description="Active test suites")
    total_test_cases: int = Field(..., description="Total test cases")
    active_test_cases: int = Field(..., description="Active test cases")
    overall_test_coverage: float = Field(..., ge=0.0, le=100.0, description="Overall test coverage percentage")
    recent_success_rate: float = Field(..., ge=0.0, le=100.0, description="Recent test success rate")
    average_execution_time: float = Field(..., description="Average test execution time")
    critical_quality_metrics: List[Dict[str, Any]] = Field(..., description="Critical quality metrics")
    quality_score: float = Field(..., ge=0.0, le=100.0, description="Overall quality score")
    last_updated: datetime = Field(..., description="When overview was last updated")


class TestTrend(BaseModel):
    """Model for test execution trends."""
    period: str = Field(..., description="Trend period")
    total_test_runs: int = Field(..., description="Total test runs in period")
    success_rate: float = Field(..., ge=0.0, le=100.0, description="Success rate percentage")
    average_execution_time: float = Field(..., description="Average execution time")
    coverage_trend: str = Field(..., description="Coverage trend direction")
    quality_trend: str = Field(..., description="Quality trend direction")
    data_points: List[Dict[str, Union[datetime, float]]] = Field(..., description="Trend data points")
    generated_at: datetime = Field(..., description="When trend was generated")


class QualityRecommendation(BaseModel):
    """Model for quality improvement recommendations."""
    recommendation_id: str = Field(..., description="Recommendation identifier")
    category: str = Field(..., description="Recommendation category")
    priority: PriorityEnum = Field(..., description="Recommendation priority")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Recommendation description")
    rationale: str = Field(..., description="Why this recommendation is made")
    expected_impact: str = Field(..., description="Expected impact of implementation")
    implementation_steps: List[str] = Field(..., description="Steps to implement recommendation")
    estimated_effort: str = Field(..., description="Estimated effort required")
    created_at: datetime = Field(..., description="When recommendation was created")
