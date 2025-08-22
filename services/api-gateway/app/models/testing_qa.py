"""
Testing and Quality Assurance Models for OpenPolicy V2

Comprehensive models for testing and quality assurance system.
Implements P2 priority feature for enhanced system quality and reliability.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class TestSuite(Base):
    """Model for test suite configurations."""
    
    __tablename__ = "test_suites"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suite_name = Column(String(200), nullable=False, unique=True)  # Test suite identifier
    suite_description = Column(Text, nullable=True)  # Test suite description
    suite_category = Column(String(100), nullable=False)  # unit, integration, e2e, performance, security
    test_framework = Column(String(100), nullable=False)  # pytest, jest, cypress, selenium, etc.
    is_active = Column(Boolean, default=True, nullable=False)  # Whether suite is active
    is_automated = Column(Boolean, default=True, nullable=False)  # Whether suite is automated
    execution_frequency = Column(String(50), nullable=False)  # on_commit, daily, weekly, manual
    timeout_seconds = Column(Integer, default=300, nullable=False)  # Test suite timeout
    parallel_execution = Column(Boolean, default=False, nullable=False)  # Whether tests run in parallel
    retry_count = Column(Integer, default=0, nullable=False)  # Number of retries on failure
    created_by = Column(String(100), nullable=False)  # Who created the test suite
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    test_cases = relationship("TestCase", back_populates="test_suite", cascade="all, delete-orphan")
    test_runs = relationship("TestRun", back_populates="test_suite", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_test_suites_suite_name', 'suite_name'),
        Index('ix_test_suites_suite_category', 'suite_category'),
        Index('ix_test_suites_test_framework', 'test_framework'),
        Index('ix_test_suites_is_active', 'is_active'),
        Index('ix_test_suites_execution_frequency', 'execution_frequency'),
    )


class TestCase(Base):
    """Model for individual test cases."""
    
    __tablename__ = "test_cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_suite_id = Column(UUID(as_uuid=True), ForeignKey("test_suites.id"), nullable=False)
    test_name = Column(String(200), nullable=False)  # Test case name
    test_description = Column(Text, nullable=True)  # Test case description
    test_type = Column(String(100), nullable=False)  # functional, performance, security, accessibility
    priority = Column(String(50), default="medium", nullable=False)  # low, medium, high, critical
    complexity = Column(String(50), default="medium", nullable=False)  # simple, medium, complex
    estimated_duration = Column(Integer, default=60, nullable=False)  # Estimated duration in seconds
    prerequisites = Column(Text, nullable=True)  # Test prerequisites
    test_steps = Column(JSONB, nullable=True)  # Test execution steps
    expected_results = Column(Text, nullable=True)  # Expected test results
    is_data_dependent = Column(Boolean, default=False, nullable=False)  # Whether test depends on specific data
    data_requirements = Column(JSONB, nullable=True)  # Data requirements for test
    is_active = Column(Boolean, default=True, nullable=False)  # Whether test case is active
    created_by = Column(String(100), nullable=False)  # Who created the test case
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    test_suite = relationship("TestSuite", back_populates="test_cases")
    test_results = relationship("TestResult", back_populates="test_case", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_test_cases_test_suite_id', 'test_suite_id'),
        Index('ix_test_cases_test_name', 'test_name'),
        Index('ix_test_cases_test_type', 'test_type'),
        Index('ix_test_cases_priority', 'priority'),
        Index('ix_test_cases_is_active', 'is_active'),
    )


class TestRun(Base):
    """Model for test run executions."""
    
    __tablename__ = "test_runs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_suite_id = Column(UUID(as_uuid=True), ForeignKey("test_suites.id"), nullable=False)
    run_name = Column(String(200), nullable=False)  # Test run identifier
    run_type = Column(String(50), nullable=False)  # scheduled, manual, triggered, ci_cd
    trigger_source = Column(String(100), nullable=True)  # git_commit, manual, schedule, webhook
    environment = Column(String(100), nullable=False)  # development, staging, production, ci
    branch_name = Column(String(100), nullable=True)  # Git branch name
    commit_hash = Column(String(100), nullable=True)  # Git commit hash
    start_time = Column(DateTime, nullable=False)  # When test run started
    end_time = Column(DateTime, nullable=True)  # When test run completed
    status = Column(String(50), default="running", nullable=False)  # running, completed, failed, cancelled
    total_tests = Column(Integer, default=0, nullable=False)  # Total number of tests
    passed_tests = Column(Integer, default=0, nullable=False)  # Number of passed tests
    failed_tests = Column(Integer, default=0, nullable=False)  # Number of failed tests
    skipped_tests = Column(Integer, default=0, nullable=False)  # Number of skipped tests
    execution_time = Column(Integer, nullable=True)  # Total execution time in seconds
    parallel_workers = Column(Integer, default=1, nullable=False)  # Number of parallel workers
    created_by = Column(String(100), nullable=False)  # Who initiated the test run
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    test_suite = relationship("TestSuite", back_populates="test_runs")
    test_results = relationship("TestResult", back_populates="test_run", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_test_runs_test_suite_id', 'test_suite_id'),
        Index('ix_test_runs_run_name', 'run_name'),
        Index('ix_test_runs_run_type', 'run_type'),
        Index('ix_test_runs_environment', 'environment'),
        Index('ix_test_runs_status', 'status'),
        Index('ix_test_runs_start_time', 'start_time'),
        Index('ix_test_runs_commit_hash', 'commit_hash'),
    )


class TestResult(Base):
    """Model for individual test results."""
    
    __tablename__ = "test_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_run_id = Column(UUID(as_uuid=True), ForeignKey("test_runs.id"), nullable=False)
    test_case_id = Column(UUID(as_uuid=True), ForeignKey("test_cases.id"), nullable=False)
    test_name = Column(String(200), nullable=False)  # Test name for quick reference
    status = Column(String(50), nullable=False)  # passed, failed, skipped, error, timeout
    execution_time = Column(Float, nullable=True)  # Test execution time in seconds
    start_time = Column(DateTime, nullable=False)  # When test started
    end_time = Column(DateTime, nullable=True)  # When test completed
    error_message = Column(Text, nullable=True)  # Error message if test failed
    stack_trace = Column(Text, nullable=True)  # Stack trace if test failed
    screenshot_path = Column(String(500), nullable=True)  # Path to screenshot if applicable
    log_output = Column(Text, nullable=True)  # Test log output
    metadata = Column(JSONB, nullable=True)  # Additional test metadata
    retry_count = Column(Integer, default=0, nullable=False)  # Number of retries attempted
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    test_run = relationship("TestRun", back_populates="test_results")
    test_case = relationship("TestCase", back_populates="test_results")
    
    # Indexes
    __table_args__ = (
        Index('ix_test_results_test_run_id', 'test_run_id'),
        Index('ix_test_results_test_case_id', 'test_case_id'),
        Index('ix_test_results_test_name', 'test_name'),
        Index('ix_test_results_status', 'status'),
        Index('ix_test_results_start_time', 'start_time'),
    )


class QualityMetric(Base):
    """Model for quality metrics and KPIs."""
    
    __tablename__ = "quality_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(200), nullable=False, unique=True)  # Metric identifier
    metric_description = Column(Text, nullable=True)  # Metric description
    metric_type = Column(String(100), nullable=False)  # coverage, reliability, performance, security
    metric_category = Column(String(100), nullable=False)  # test, code, deployment, user
    target_value = Column(Float, nullable=True)  # Target value for the metric
    current_value = Column(Float, nullable=False)  # Current metric value
    unit = Column(String(50), nullable=True)  # Unit of measurement
    calculation_method = Column(String(200), nullable=False)  # How metric is calculated
    data_source = Column(String(200), nullable=False)  # Source of metric data
    collection_frequency = Column(String(50), nullable=False)  # How often metric is collected
    last_updated = Column(DateTime, nullable=False)  # When metric was last updated
    trend_direction = Column(String(50), nullable=True)  # improving, declining, stable
    is_critical = Column(Boolean, default=False, nullable=False)  # Whether metric is critical
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_quality_metrics_metric_name', 'metric_name'),
        Index('ix_quality_metrics_metric_type', 'metric_type'),
        Index('ix_quality_metrics_metric_category', 'metric_category'),
        Index('ix_quality_metrics_is_critical', 'is_critical'),
        Index('ix_quality_metrics_last_updated', 'last_updated'),
    )


class TestCoverage(Base):
    """Model for test coverage tracking."""
    
    __tablename__ = "test_coverage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_run_id = Column(UUID(as_uuid=True), ForeignKey("test_runs.id"), nullable=False)
    coverage_type = Column(String(100), nullable=False)  # line, branch, function, statement
    total_lines = Column(Integer, nullable=False)  # Total lines of code
    covered_lines = Column(Integer, nullable=False)  # Lines covered by tests
    coverage_percentage = Column(Float, nullable=False)  # Coverage percentage
    uncovered_lines = Column(JSONB, nullable=True)  # List of uncovered lines
    coverage_report_path = Column(String(500), nullable=True)  # Path to coverage report
    coverage_timestamp = Column(DateTime, nullable=False)  # When coverage was measured
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    test_run = relationship("TestRun", foreign_keys=[test_run_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_test_coverage_test_run_id', 'test_run_id'),
        Index('ix_test_coverage_coverage_type', 'coverage_type'),
        Index('ix_test_coverage_coverage_percentage', 'coverage_percentage'),
        Index('ix_test_coverage_coverage_timestamp', 'coverage_timestamp'),
    )


class TestEnvironment(Base):
    """Model for test environment configurations."""
    
    __tablename__ = "test_environments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    environment_name = Column(String(200), nullable=False, unique=True)  # Environment identifier
    environment_type = Column(String(100), nullable=False)  # development, staging, production, ci
    base_url = Column(String(500), nullable=False)  # Base URL for the environment
    database_url = Column(String(500), nullable=True)  # Database connection string
    api_key = Column(String(200), nullable=True)  # API key for the environment
    environment_variables = Column(JSONB, nullable=True)  # Environment-specific variables
    is_active = Column(Boolean, default=True, nullable=False)  # Whether environment is active
    supports_parallel = Column(Boolean, default=False, nullable=False)  # Whether environment supports parallel testing
    max_parallel_tests = Column(Integer, default=1, nullable=False)  # Maximum parallel tests
    created_by = Column(String(100), nullable=False)  # Who created the environment
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_test_environments_environment_name', 'environment_name'),
        Index('ix_test_environments_environment_type', 'environment_type'),
        Index('ix_test_environments_is_active', 'is_active'),
    )


class TestSchedule(Base):
    """Model for automated test scheduling."""
    
    __tablename__ = "test_schedules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_name = Column(String(200), nullable=False, unique=True)  # Schedule identifier
    test_suite_id = Column(UUID(as_uuid=True), ForeignKey("test_suites.id"), nullable=False)
    environment_id = Column(UUID(as_uuid=True), ForeignKey("test_environments.id"), nullable=False)
    cron_expression = Column(String(100), nullable=False)  # Cron expression for scheduling
    timezone = Column(String(100), default="UTC", nullable=False)  # Timezone for scheduling
    is_active = Column(Boolean, default=True, nullable=False)  # Whether schedule is active
    last_run = Column(DateTime, nullable=True)  # When schedule last ran
    next_run = Column(DateTime, nullable=True)  # When schedule will next run
    max_retries = Column(Integer, default=3, nullable=False)  # Maximum retries on failure
    notification_channels = Column(JSONB, nullable=True)  # Notification channels for results
    created_by = Column(String(100), nullable=False)  # Who created the schedule
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    test_suite = relationship("TestSuite", foreign_keys=[test_suite_id])
    environment = relationship("TestEnvironment", foreign_keys=[environment_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_test_schedules_schedule_name', 'schedule_name'),
        Index('ix_test_schedules_test_suite_id', 'test_suite_id'),
        Index('ix_test_schedules_environment_id', 'environment_id'),
        Index('ix_test_schedules_is_active', 'is_active'),
        Index('ix_test_schedules_next_run', 'next_run'),
    )


class TestReport(Base):
    """Model for test reports and analytics."""
    
    __tablename__ = "test_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_name = Column(String(200), nullable=False)  # Report identifier
    report_type = Column(String(100), nullable=False)  # daily, weekly, monthly, custom
    report_period_start = Column(DateTime, nullable=False)  # Report period start
    report_period_end = Column(DateTime, nullable=False)  # Report period end
    test_suite_id = Column(UUID(as_uuid=True), ForeignKey("test_suites.id"), nullable=True)  # Specific test suite
    environment_id = Column(UUID(as_uuid=True), ForeignKey("test_environments.id"), nullable=True)  # Specific environment
    total_test_runs = Column(Integer, default=0, nullable=False)  # Total test runs in period
    total_tests_executed = Column(Integer, default=0, nullable=False)  # Total tests executed
    total_tests_passed = Column(Integer, default=0, nullable=False)  # Total tests passed
    total_tests_failed = Column(Integer, default=0, nullable=False)  # Total tests failed
    total_tests_skipped = Column(Integer, default=0, nullable=False)  # Total tests skipped
    overall_success_rate = Column(Float, default=0.0, nullable=False)  # Overall success rate percentage
    average_execution_time = Column(Float, default=0.0, nullable=False)  # Average execution time
    coverage_summary = Column(JSONB, nullable=True)  # Coverage summary data
    quality_metrics = Column(JSONB, nullable=True)  # Quality metrics summary
    recommendations = Column(JSONB, nullable=True)  # Improvement recommendations
    generated_by = Column(String(100), nullable=False)  # Who generated the report
    is_automated = Column(Boolean, default=True, nullable=False)  # Whether report was auto-generated
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    test_suite = relationship("TestSuite", foreign_keys=[test_suite_id])
    environment = relationship("TestEnvironment", foreign_keys=[environment_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_test_reports_report_name', 'report_name'),
        Index('ix_test_reports_report_type', 'report_type'),
        Index('ix_test_reports_report_period_start', 'report_period_start'),
        Index('ix_test_reports_report_period_end', 'report_period_end'),
        Index('ix_test_reports_test_suite_id', 'test_suite_id'),
        Index('ix_test_reports_environment_id', 'environment_id'),
    )
