#!/usr/bin/env python3
"""
Run all AI Content Pipeline tests
"""
import subprocess
import sys
import os
from pathlib import Path

def run_test(test_name, test_file):
    """Run a single test file and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running: {test_name}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=120  # Increased timeout for integration tests
        )
        
        # Print output
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"\n✅ {test_name} - PASSED")
            return True
        else:
            print(f"\n❌ {test_name} - FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n⏱️ {test_name} - TIMEOUT")
        return False
    except Exception as e:
        print(f"\n❌ {test_name} - ERROR: {e}")
        return False

def main():
    """Run all tests in the tests directory"""
    print("🚀 AI Content Pipeline - Test Suite Runner")
    print("="*60)
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Check command line arguments
    quick_mode = len(sys.argv) > 1 and sys.argv[1] == '--quick'
    
    # Define test order and descriptions
    if quick_mode:
        print("⚡ Running in quick mode (core tests only)")
        tests = [
            ("Core Tests", "tests/test_core.py"),
        ]
    else:
        tests = [
            ("Core Tests", "tests/test_core.py"),
            ("Integration Tests", "tests/test_integration.py"),
        ]
    
    print(f"📋 Running {len(tests)} test suite(s):")
    for test_name, test_file in tests:
        status = "✓" if Path(test_file).exists() else "✗"
        print(f"   {status} {test_name}")
    
    # Run all tests
    passed = 0
    failed = 0
    
    for test_name, test_file in tests:
        if run_test(test_name, test_file):
            passed += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📋 Total: {len(tests)}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        
        if not quick_mode:
            print("\n🏆 The AI Content Pipeline package is fully functional!")
            print("\n🔧 Available Commands:")
            print("   • ai-content-pipeline --help")
            print("   • ai-content-pipeline list-models")
            print("   • ai-content-pipeline run-chain --config config.yaml")
            print("   • aicp (shortened alias)")
        
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed!")
        print("\n💡 To run individual tests:")
        print("   python tests/test_core.py")
        print("   python tests/test_integration.py")
        print("   python tests/demo.py --interactive")
        print("\n🔧 Test runner options:")
        print("   python tests/run_all_tests.py --quick  # Core tests only")
        return 1

if __name__ == "__main__":
    sys.exit(main())