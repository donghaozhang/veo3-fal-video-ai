#!/usr/bin/env python3
"""
Test script for Image Understanding + Modification + Verification workflow.

This demonstrates the complete workflow combining:
1. Google Gemini AI - Image understanding
2. FAL AI - Image modification  
3. Verification - Before/after comparison

Author: AI Assistant
"""

from pathlib import Path
from image_modify_verify import ImageModifyVerifySystem

def test_system_availability():
    """Test if both systems are available."""
    print("🔧 Testing System Availability")
    print("=" * 50)
    
    system = ImageModifyVerifySystem()
    ready, message = system.check_requirements()
    
    print(f"Gemini Available: {system.gemini_available}")
    print(f"FAL Available: {system.fal_available}")
    print(f"System Ready: {ready}")
    print(f"Message: {message}")
    
    return ready

def test_image_understanding():
    """Test image understanding with sample image."""
    print("\n🔍 Testing Image Understanding")
    print("=" * 50)
    
    # Look for sample images
    test_images = [
        Path("samples/sample_image.jpg"),
        Path("samples/sample_image.png"),
        Path("../fal_image_to_image/assets/sample_images/original_ai_image.jpg"),
        Path("../fal_image_to_image/assets/sample_images/test_ai_image.jpg")
    ]
    
    test_image = None
    for img_path in test_images:
        if img_path.exists():
            test_image = img_path
            break
    
    if not test_image:
        print("❌ No test image found. Available paths checked:")
        for path in test_images:
            print(f"   - {path}")
        return False
    
    print(f"📸 Testing with: {test_image}")
    
    try:
        system = ImageModifyVerifySystem()
        understanding = system.understand_image(test_image, ['description', 'objects'])
        
        print("\n📋 Understanding Results:")
        for analysis_type, result in understanding['analysis'].items():
            print(f"\n{analysis_type.upper()}:")
            preview = result[:150] + "..." if len(result) > 150 else result
            print(f"   {preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ Understanding test failed: {e}")
        return False

def test_modification_suggestions():
    """Test intelligent modification suggestions."""
    print("\n🧠 Testing Modification Suggestions")
    print("=" * 50)
    
    # Mock understanding data for testing
    mock_understanding = {
        'analysis': {
            'description': 'A portrait photo showing a person in dim lighting with muted colors and a cluttered background',
            'objects': 'person, face, background objects, various items',
            'composition': 'centered subject with busy background'
        }
    }
    
    system = ImageModifyVerifySystem()
    suggestions = system.suggest_modifications(mock_understanding)
    
    print(f"Generated {len(suggestions)} suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['type'].replace('_', ' ').title()}")
        print(f"   Reason: {suggestion['reason']}")
        print(f"   Model: {suggestion['model']}")
        print(f"   Prompt: {suggestion['prompt']}")
        if 'strength' in suggestion:
            print(f"   Strength: {suggestion['strength']}")
    
    return True

def test_complete_workflow():
    """Test the complete workflow with understanding only."""
    print("\n🎯 Testing Complete Workflow (Understanding Only)")
    print("=" * 50)
    
    # Find test image
    test_images = [
        Path("../fal_image_to_image/assets/sample_images/original_ai_image.jpg"),
        Path("../fal_image_to_image/assets/sample_images/test_ai_image.jpg")
    ]
    
    test_image = None
    for img_path in test_images:
        if img_path.exists():
            test_image = img_path
            break
    
    if not test_image:
        print("❌ No test image found for workflow test")
        return False
    
    print(f"📸 Testing workflow with: {test_image}")
    
    try:
        system = ImageModifyVerifySystem()
        
        # Test understanding only (safer for testing)
        understanding = system.understand_image(test_image)
        suggestions = system.suggest_modifications(understanding)
        
        print("\n✅ Workflow Components Working:")
        print(f"   📸 Image Understanding: ✅")
        print(f"   🧠 Smart Suggestions: ✅ ({len(suggestions)} suggestions)")
        print(f"   🎨 Modification: ⏸️ (Skipped for testing)")
        print(f"   🔍 Verification: ⏸️ (Skipped for testing)")
        
        print(f"\n📊 Top Suggestion:")
        if suggestions:
            top = suggestions[0]
            print(f"   Type: {top['type']}")
            print(f"   Reason: {top['reason']}")
            print(f"   Prompt: {top['prompt'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎬 IMAGE MODIFY VERIFY SYSTEM TESTS")
    print("=" * 70)
    
    tests = [
        ("System Availability", test_system_availability),
        ("Image Understanding", test_image_understanding),
        ("Modification Suggestions", test_modification_suggestions),
        ("Complete Workflow", test_complete_workflow)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n💥 {test_name}: ERROR - {e}")
    
    print(f"\n📊 TEST RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! System is ready for use.")
        print("\n💡 Usage Examples:")
        print("   # Understand image only")
        print("   python image_modify_verify.py image.jpg --understand-only")
        print("")
        print("   # Complete workflow with auto suggestions")
        print("   python image_modify_verify.py image.jpg")
        print("")
        print("   # Custom modification")
        print("   python image_modify_verify.py image.jpg --prompt 'Make it brighter and more colorful'")
    else:
        print("⚠️  Some tests failed. Check configuration:")
        print("   1. Ensure GEMINI_API_KEY is set in .env")
        print("   2. Ensure FAL_KEY is set in fal_image_to_image/.env")
        print("   3. Install required packages")

if __name__ == "__main__":
    main()