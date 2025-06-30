#!/usr/bin/env python3
"""Main test runner that delegates to tests directory."""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the test suite from the tests directory."""
    tests_dir = Path(__file__).parent / "tests"
    test_runner = tests_dir / "run_quick_tests.py"
    
    if not test_runner.exists():
        print("❌ Test runner not found at:", test_runner)
        return False
    
    print("🚀 Running Enhanced Architecture Test Suite")
    print(f"📁 Test directory: {tests_dir}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["python3", str(test_runner)],
            cwd=tests_dir,
            check=False
        )
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)