#!/usr/bin/env python3
"""
Test runner script for API Gateway.

This script provides various options for running tests with different
configurations, coverage reporting, and test selection.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(command: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError as e:
        print(f"\n❌ Command not found: {e}")
        return False


def run_unit_tests(verbose: bool = False, coverage: bool = False) -> bool:
    """Run unit tests."""
    command = ["python", "-m", "pytest", "tests/", "-m", "unit"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend(["--cov=app", "--cov-report=term-missing", "--cov-report=html"])
    
    return run_command(command, "Unit Tests")


def run_integration_tests(verbose: bool = False, coverage: bool = False) -> bool:
    """Run integration tests."""
    command = ["python", "-m", "pytest", "tests/", "-m", "integration"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend(["--cov=app", "--cov-report=term-missing", "--cov-report=html"])
    
    return run_command(command, "Integration Tests")


def run_all_tests(verbose: bool = False, coverage: bool = False, fast: bool = False) -> bool:
    """Run all tests."""
    command = ["python", "-m", "pytest", "tests/"]
    
    if verbose:
        command.append("-v")
    
    if fast:
        command.extend(["-m", "not slow"])
    
    if coverage:
        command.extend(["--cov=app", "--cov-report=term-missing", "--cov-report=html"])
    
    return run_command(command, "All Tests")


def run_specific_test(test_path: str, verbose: bool = False) -> bool:
    """Run a specific test file or test function."""
    command = ["python", "-m", "pytest", test_path]
    
    if verbose:
        command.append("-v")
    
    return run_command(command, f"Specific Test: {test_path}")


def run_tests_with_markers(markers: list[str], verbose: bool = False, coverage: bool = False) -> bool:
    """Run tests with specific markers."""
    marker_expr = " and ".join(markers)
    command = ["python", "-m", "pytest", "tests/", "-m", marker_expr]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend(["--cov=app", "--cov-report=term-missing", "--cov-report=html"])
    
    return run_command(command, f"Tests with markers: {marker_expr}")


def run_coverage_report() -> bool:
    """Generate coverage report."""
    command = ["python", "-m", "coverage", "report", "--show-missing"]
    return run_command(command, "Coverage Report")


def run_coverage_html() -> bool:
    """Generate HTML coverage report."""
    command = ["python", "-m", "coverage", "html"]
    return run_command(command, "HTML Coverage Report")


def run_linting() -> bool:
    """Run code linting."""
    command = ["python", "-m", "flake8", "app/", "tests/", "--max-line-length=88", "--extend-ignore=E203,W503"]
    return run_command(command, "Code Linting")


def run_type_checking() -> bool:
    """Run type checking."""
    command = ["python", "-m", "mypy", "app/", "--ignore-missing-imports"]
    return run_command(command, "Type Checking")


def run_security_checks() -> bool:
    """Run security checks."""
    command = ["python", "-m", "bandit", "-r", "app/", "-f", "json", "-o", "bandit-report.json"]
    return run_command(command, "Security Checks")


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Test runner for API Gateway",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --all                    # Run all tests
  python run_tests.py --unit --coverage        # Run unit tests with coverage
  python run_tests.py --integration --verbose  # Run integration tests verbosely
  python run_tests.py --markers api websocket  # Run tests with specific markers
  python run_tests.py --file tests/test_bills.py  # Run specific test file
  python run_tests.py --lint --type-check      # Run code quality checks
        """
    )
    
    # Test selection options
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--fast", action="store_true", help="Run only fast tests (exclude slow)")
    parser.add_argument("--file", type=str, help="Run specific test file or test function")
    parser.add_argument("--markers", nargs="+", help="Run tests with specific markers")
    
    # Test execution options
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--coverage-only", action="store_true", help="Generate coverage report only")
    
    # Code quality options
    parser.add_argument("--lint", action="store_true", help="Run code linting")
    parser.add_argument("--type-check", action="store_true", help="Run type checking")
    parser.add_argument("--security", action="store_true", help="Run security checks")
    parser.add_argument("--quality", action="store_true", help="Run all code quality checks")
    
    # Output options
    parser.add_argument("--html-report", action="store_true", help="Generate HTML coverage report")
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    success = True
    
    try:
        # Code quality checks
        if args.quality or args.lint:
            success &= run_linting()
        
        if args.quality or args.type_check:
            success &= run_type_checking()
        
        if args.quality or args.security:
            success &= run_security_checks()
        
        # Coverage reports only
        if args.coverage_only:
            if args.html_report:
                success &= run_coverage_html()
            else:
                success &= run_coverage_report()
            return
        
        # Test execution
        if args.file:
            success &= run_specific_test(args.file, args.verbose)
        elif args.markers:
            success &= run_tests_with_markers(args.markers, args.verbose, args.coverage)
        elif args.unit:
            success &= run_unit_tests(args.verbose, args.coverage)
        elif args.integration:
            success &= run_integration_tests(args.verbose, args.coverage)
        elif args.all or not any([args.unit, args.integration, args.file, args.markers]):
            success &= run_all_tests(args.verbose, args.coverage, args.fast)
        
        # Additional coverage reports
        if args.coverage and args.html_report:
            success &= run_coverage_html()
        
        # Final status
        if success:
            print(f"\n{'='*60}")
            print("🎉 All operations completed successfully!")
            print(f"{'='*60}")
            sys.exit(0)
        else:
            print(f"\n{'='*60}")
            print("💥 Some operations failed. Check the output above.")
            print(f"{'='*60}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
