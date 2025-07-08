#!/usr/bin/env python3
"""
FAL AI Avatar Generation - Setup Test (FREE)

This script tests the FAL AI Avatar setup and environment without generating
any videos or incurring costs. It validates:
- Environment variables and configuration
- FAL AI API key and connection
- Required dependencies
- Voice options availability

⚠️ This script is completely FREE - it does not generate any videos or cost money.

Usage:
    python test_setup.py
"""

import os
import sys
from pathlib import Path

def test_environment():
    """Test environment setup and configuration"""
    print("🔧 Testing Environment Setup...")
    
    # Test Python version
    python_version = sys.version_info
    print(f"   Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("   ❌ Python 3.7+ required")
        return False
    else:
        print("   ✅ Python version OK")
    
    # Test required modules
    required_modules = [
        'os', 'sys', 'time', 'typing', 'pathlib'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module} available")
        except ImportError:
            print(f"   ❌ {module} missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"   ❌ Missing required modules: {missing_modules}")
        return False
    
    return True

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        ('fal_client', 'fal-client'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv')
    ]
    
    missing_packages = []
    
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"   ✅ {package_name} installed")
        except ImportError:
            print(f"   ❌ {package_name} missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n   📋 To install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_configuration():
    """Test configuration files and environment variables"""
    print("\n⚙️ Testing Configuration...")
    
    # Check for .env file
    env_file = Path('.env')
    if env_file.exists():
        print(f"   ✅ .env file found: {env_file.absolute()}")
    else:
        print(f"   ⚠️ .env file not found (optional)")
    
    # Check for FAL_KEY environment variable
    fal_key = os.getenv('FAL_KEY')
    if fal_key:
        # Don't print the actual key for security
        key_preview = f"{fal_key[:8]}...{fal_key[-4:]}" if len(fal_key) > 12 else "***"
        print(f"   ✅ FAL_KEY found: {key_preview}")
        
        # Basic key format validation
        if len(fal_key) < 10:
            print(f"   ⚠️ FAL_KEY seems too short")
            return False
        
        return True
    else:
        print(f"   ❌ FAL_KEY environment variable not found")
        print(f"   📋 Please set your FAL AI API key:")
        print(f"      export FAL_KEY='your-api-key-here'")
        print(f"   Or create a .env file with: FAL_KEY=your-api-key-here")
        return False

def test_fal_client():
    """Test FAL client import and basic functionality"""
    print("\n🔌 Testing FAL Client...")
    
    try:
        import fal_client
        print(f"   ✅ fal_client imported successfully")
        
        # Test basic client functionality (no API calls)
        print(f"   ✅ fal_client module loaded")
        
        # Check if we can access client methods (without calling them)
        if hasattr(fal_client, 'subscribe'):
            print(f"   ✅ fal_client.subscribe method available")
        else:
            print(f"   ❌ fal_client.subscribe method not found")
            return False
        
        if hasattr(fal_client, 'upload_file'):
            print(f"   ✅ fal_client.upload_file method available")
        else:
            print(f"   ❌ fal_client.upload_file method not found")
            return False
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Failed to import fal_client: {e}")
        print(f"   📋 Install with: pip install fal-client")
        return False
    except Exception as e:
        print(f"   ❌ Error testing fal_client: {e}")
        return False

def test_avatar_generator():
    """Test avatar generator class import and initialization"""
    print("\n🎭 Testing Avatar Generator...")
    
    try:
        # Add current directory to path for import
        current_dir = Path(__file__).parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        
        from fal_avatar_generator import FALAvatarGenerator, VOICE_OPTIONS
        print(f"   ✅ FALAvatarGenerator imported successfully")
        
        # Test voice options
        print(f"   ✅ Voice options loaded: {len(VOICE_OPTIONS)} voices")
        
        # Test some expected voices
        expected_voices = ["Sarah", "Roger", "Bill", "Alice"]
        for voice in expected_voices:
            if voice in VOICE_OPTIONS:
                print(f"   ✅ Voice '{voice}' available")
            else:
                print(f"   ⚠️ Expected voice '{voice}' not found")
        
        # Try to initialize generator (this will test API key)
        try:
            generator = FALAvatarGenerator()
            print(f"   ✅ FALAvatarGenerator initialized successfully")
            
            # Test methods availability
            if hasattr(generator, 'generate_avatar_video'):
                print(f"   ✅ generate_avatar_video method available")
            
            if hasattr(generator, 'get_available_voices'):
                voices = generator.get_available_voices()
                print(f"   ✅ get_available_voices method works ({len(voices)} voices)")
            
            return True
            
        except ValueError as e:
            if "FAL_KEY" in str(e):
                print(f"   ❌ API key issue: {e}")
                return False
            else:
                print(f"   ❌ Initialization error: {e}")
                return False
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            return False
            
    except ImportError as e:
        print(f"   ❌ Failed to import FALAvatarGenerator: {e}")
        print(f"   📋 Make sure fal_avatar_generator.py is in the current directory")
        return False
    except Exception as e:
        print(f"   ❌ Error testing avatar generator: {e}")
        return False

def test_output_directory():
    """Test output directory creation"""
    print("\n📁 Testing Output Directory...")
    
    output_dir = Path("output")
    
    try:
        output_dir.mkdir(exist_ok=True)
        print(f"   ✅ Output directory ready: {output_dir.absolute()}")
        
        # Test write permissions
        test_file = output_dir / "test_write.tmp"
        try:
            test_file.write_text("test")
            test_file.unlink()  # Delete test file
            print(f"   ✅ Write permissions OK")
            return True
        except Exception as e:
            print(f"   ❌ Write permission error: {e}")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to create output directory: {e}")
        return False

def run_all_tests():
    """Run all setup tests"""
    print("🧪 FAL AI Avatar Generation - Setup Tests")
    print("=" * 60)
    print("Testing environment and configuration (FREE - no API calls)")
    
    tests = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("FAL Client", test_fal_client),
        ("Avatar Generator", test_avatar_generator),
        ("Output Directory", test_output_directory)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"   ❌ Unexpected error in {test_name}: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your FAL Avatar setup is ready.")
        print("\n📋 Next steps:")
        print("   - Run 'python demo.py' for interactive avatar generation")
        print("   - Or use the FALAvatarGenerator class in your own code")
        print("   - Remember: Avatar generation costs money (~$0.02-0.05 per video)")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n📋 Common solutions:")
        print("   - Install missing packages: pip install fal-client requests python-dotenv")
        print("   - Set FAL_KEY environment variable with your API key")
        print("   - Make sure fal_avatar_generator.py is in the current directory")
        return False

def main():
    """Main function"""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 