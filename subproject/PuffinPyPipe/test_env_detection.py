#!/usr/bin/env python3
"""
Test script to verify that the ImportExecutor can find .env and .gitignore files
when scripts are invoked from the parent directory.
"""

import os
import sys

# Add the csviper package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'csviper', 'src'))

from csviper.import_executor import ImportExecutor

def test_env_file_detection():
    """Test that .env file can be found when invoked from parent directory."""
    print("Testing .env file detection...")
    
    env_file = ImportExecutor.find_env_file()
    if env_file:
        print(f"✓ Found .env file at: {env_file}")
        return True
    else:
        print("✗ No .env file found")
        return False

def test_gitignore_check():
    """Test that .gitignore check works when invoked from parent directory."""
    print("\nTesting .gitignore check...")
    
    try:
        ImportExecutor.check_gitignore_for_env()
        print("✓ .gitignore check completed without errors")
        return True
    except Exception as e:
        print(f"✗ .gitignore check failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing ImportExecutor file detection from parent directory...")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {__file__}")
    print("-" * 60)
    
    env_test = test_env_file_detection()
    gitignore_test = test_gitignore_check()
    
    print("-" * 60)
    if env_test and gitignore_test:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
