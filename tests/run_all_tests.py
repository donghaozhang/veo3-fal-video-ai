#!/usr/bin/env python3
"""
Run all AI Content Pipeline tests
"""
import subprocess
import sys
from pathlib import Path

def run_test(test_file):
    """Run a single test file and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Print output
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {test_file} - PASSED")
            return True
        else:
            print(f"❌ {test_file} - FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ {test_file} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {test_file} - ERROR: {e}")
        return False

def main():
    """Run all tests in the tests directory"""
    print("🚀 AI Content Pipeline - Test Suite Runner")
    print("="*60)
    
    # Get all test files
    tests_dir = Path(__file__).parent
    test_files = sorted([
        f for f in tests_dir.glob("test_*.py") 
        if f.name != "run_all_tests.py"
    ])
    
    print(f"📋 Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"   • {test_file.name}")
    
    # Run all tests
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if run_test(str(test_file)):
            passed += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📋 Total: {len(test_files)}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())