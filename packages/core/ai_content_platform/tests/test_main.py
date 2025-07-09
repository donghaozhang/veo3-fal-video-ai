"""Main test runner and test discovery."""

import os
import sys
from pathlib import Path

import pytest


def run_tests(
    test_type: str = "all", 
    verbose: bool = False,
    coverage: bool = True,
    parallel: bool = False
):
    """Run the test suite with various options.
    
    Args:
        test_type: Type of tests to run ('unit', 'integration', 'all')
        verbose: Enable verbose output
        coverage: Enable coverage reporting
        parallel: Enable parallel test execution
    """
    # Build pytest arguments
    args = []
    
    # Test selection
    if test_type == "unit":
        args.extend(["-m", "unit"])
    elif test_type == "integration":
        args.extend(["-m", "integration"])
    elif test_type == "fast":
        args.extend(["-m", "not slow"])
    # 'all' runs everything by default
    
    # Verbose output
    if verbose:
        args.append("-v")
    
    # Coverage
    if coverage:
        args.extend([
            "--cov=ai_content_platform",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=70"
        ])
    
    # Parallel execution
    if parallel:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        args.extend(["-n", str(max(2, cpu_count // 2))])
    
    # Add test directory
    test_dir = Path(__file__).parent
    args.append(str(test_dir))
    
    # Run tests
    exit_code = pytest.main(args)
    return exit_code


def main():
    """Main entry point for test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Content Platform Test Runner")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "fast", "all"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage reporting"
    )
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Quick test run (unit tests only, no coverage)"
    )
    
    args = parser.parse_args()
    
    # Quick mode overrides
    if args.quick:
        test_type = "fast"
        coverage = False
        verbose = False
    else:
        test_type = args.type
        coverage = not args.no_coverage
        verbose = args.verbose
    
    print(f"Running {test_type} tests...")
    if coverage:
        print("Coverage reporting enabled")
    if args.parallel:
        print("Parallel execution enabled")
    
    exit_code = run_tests(
        test_type=test_type,
        verbose=verbose,
        coverage=coverage,
        parallel=args.parallel
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()