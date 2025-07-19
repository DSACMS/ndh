#!/usr/bin/env python3
"""
Test script to verify local csviper and plainerflow libraries are working
"""

def test_csviper():
    """Test csviper import and basic functionality"""
    try:
        import csviper
        print("✓ csviper imported successfully")
        
        # Test specific module import
        from csviper.import_executor import ImportExecutor
        print("✓ csviper.import_executor.ImportExecutor imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ csviper import failed: {e}")
        return False

def test_plainerflow():
    """Test plainerflow import and basic functionality"""
    try:
        import plainerflow
        print("✓ plainerflow imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ plainerflow import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing local library installations...")
    print("=" * 50)
    
    csviper_ok = test_csviper()
    print()
    plainerflow_ok = test_plainerflow()
    
    print()
    print("=" * 50)
    if csviper_ok and plainerflow_ok:
        print("✓ All tests passed! Local libraries are working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Check the output above.")
        return 1

if __name__ == '__main__':
    exit(main())
