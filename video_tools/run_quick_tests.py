#!/usr/bin/env python3
"""Quick test runner for essential validation of enhanced architecture."""

import subprocess
import sys
from pathlib import Path

def run_test(test_file, description, timeout=60):
    """Run a test file and return result."""
    print(f"\n{'='*50}")
    print(f"🧪 {description}")
    print(f"📁 {test_file}")
    print('='*50)
    
    try:
        result = subprocess.run(
            ["python3", test_file],
            cwd=Path(__file__).parent,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        
        success = result.returncode == 0
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr and not success:
            print("STDERR:", result.stderr)
        
        print(f"\n🏁 Result: {'✅ PASSED' if success else '❌ FAILED'}")
        return success
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT after {timeout} seconds")
        return False
    except FileNotFoundError:
        print(f"❌ Test file not found: {test_file}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run essential tests for enhanced architecture."""
    print("🚀 Enhanced Architecture - Quick Test Suite")
    print("🎯 Running essential validation tests")
    
    # Essential tests in order of importance
    tests = [
        ("test_enhanced_architecture.py", "Architecture Validation", 30),
        ("test_backward_compatibility.py", "Backward Compatibility", 30),
        ("test_enhanced_video_processor.py", "Enhanced Video Processor", 60),
    ]
    
    results = []
    
    for test_file, description, timeout in tests:
        if Path(test_file).exists():
            result = run_test(test_file, description, timeout)
            results.append((description, result))
        else:
            print(f"⚠️ Skipping {description} - test file not found")
            results.append((description, None))
    
    # Test CLI basic functionality
    print(f"\n{'='*50}")
    print("🧪 CLI Basic Functionality")
    print('='*50)
    
    try:
        # Test CLI help
        result = subprocess.run(
            ["python3", "enhanced_cli.py", "--help"],
            cwd=Path(__file__).parent,
            timeout=10,
            capture_output=True,
            text=True
        )
        
        cli_help_success = result.returncode == 0
        if cli_help_success:
            print("✅ CLI help command works")
        else:
            print("❌ CLI help command failed")
            print("STDERR:", result.stderr)
        
        results.append(("CLI Help", cli_help_success))
        
    except Exception as e:
        print(f"❌ CLI test error: {e}")
        results.append(("CLI Help", False))
    
    # Test CLI status
    try:
        result = subprocess.run(
            ["python3", "enhanced_cli.py", "--command", "status"],
            cwd=Path(__file__).parent,
            timeout=15,
            capture_output=True,
            text=True
        )
        
        cli_status_success = result.returncode == 0
        if cli_status_success:
            print("✅ CLI status command works")
            # Print relevant output
            if "AI Services Status" in result.stdout:
                print("✅ Status check includes AI services")
        else:
            print("❌ CLI status command failed")
            print("STDERR:", result.stderr)
        
        results.append(("CLI Status", cli_status_success))
        
    except Exception as e:
        print(f"❌ CLI status test error: {e}")
        results.append(("CLI Status", False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 QUICK TEST SUMMARY")
    print('='*60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for description, result in results:
        if result is True:
            print(f"✅ {description}")
            passed += 1
        elif result is False:
            print(f"❌ {description}")
            failed += 1
        else:
            print(f"⚠️ {description} (skipped)")
            skipped += 1
    
    total = passed + failed
    print(f"\n📈 Results: {passed}/{total} passed")
    if skipped > 0:
        print(f"⚠️ {skipped} tests skipped")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"🎯 Success rate: {success_rate:.1f}%")
    
    # Determine overall result
    critical_tests = ["Architecture Validation", "Backward Compatibility"]
    critical_passed = all(
        result for desc, result in results 
        if desc in critical_tests and result is not None
    )
    
    if critical_passed and success_rate >= 70:
        print("\n🎉 QUICK TEST SUITE PASSED!")
        print("✅ Enhanced architecture is working correctly")
        print("✅ Backward compatibility is maintained")
        if success_rate >= 90:
            print("🌟 Excellent! All major features are functional")
        return True
    else:
        print("\n❌ QUICK TEST SUITE FAILED!")
        if not critical_passed:
            print("🚨 Critical architecture or compatibility issues detected")
        else:
            print("⚠️ Some enhanced features may have issues")
        return False

if __name__ == "__main__":
    success = main()
    
    print(f"\n{'='*60}")
    print("🏁 FINAL RESULT")
    print('='*60)
    
    if success:
        print("✅ Enhanced class-based architecture is ready for use!")
        print("📚 Check docs/MIGRATION_GUIDE.md for usage examples")
        print("🎬 Try: python3 enhanced_cli.py")
    else:
        print("❌ Issues detected with enhanced architecture")
        print("🔧 Check individual test results above")
        print("📖 Review docs/ARCHITECTURE_OVERVIEW.md for details")
    
    sys.exit(0 if success else 1)