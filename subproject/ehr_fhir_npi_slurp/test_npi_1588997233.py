#!/usr/bin/env python3
"""
Test to verify that NPI 1588997233 is correctly returned as valid from cache without API call.
"""

import os
import sys
from unittest.mock import patch, MagicMock
from NPIValidator import NPIValidator


def test_npi_1588997233_from_cache():
    """
    Test that NPI 1588997233 is returned as valid from the local cache
    without making an API call.
    """
    print("Testing NPI 1588997233 validation from cache...")
    
    # Initialize validator (this will load the cache)
    validator = NPIValidator()
    
    # Check that the cache was loaded
    print(f"Cache loaded with {len(validator.npi_cache)} NPIs")
    
    # Check if our test NPI is in the cache
    test_npi = "1588997233"
    print(f"Checking if NPI {test_npi} is in cache...")
    
    if test_npi in validator.npi_cache:
        cached_result = validator.npi_cache[test_npi]
        print(f"✓ NPI {test_npi} found in cache with result: {cached_result}")
    else:
        print(f"✗ NPI {test_npi} NOT found in cache")
        return False
    
    # Now test the validation method with API call monitoring
    print(f"Testing validation method for NPI {test_npi}...")
    
    # Mock the API call to ensure it's not called
    with patch.object(NPIValidator, '_validate_npi_via_api') as mock_api_call:
        # Call the validation method
        result = validator.is_this_npi_valid(npi_value=test_npi)
        
        # Verify the result is True (valid)
        if result:
            print(f"✓ NPI {test_npi} returned as VALID")
        else:
            print(f"✗ NPI {test_npi} returned as INVALID")
            return False
        
        # Verify the API was not called
        if mock_api_call.called:
            print(f"✗ API was called {mock_api_call.call_count} times - should not have been called!")
            return False
        else:
            print("✓ API was NOT called - validation used cache as expected")
    
    print(f"✓ All tests passed for NPI {test_npi}")
    return True


def test_cache_loading():
    """
    Test that the cache file is properly loaded and contains expected data.
    """
    print("\nTesting cache loading...")
    
    # Check if cache file exists
    cache_file = "prod_data/valid_npi_list.csv"
    if not os.path.exists(cache_file):
        print(f"✗ Cache file {cache_file} does not exist")
        return False
    
    print(f"✓ Cache file {cache_file} exists")
    
    # Initialize validator
    validator = NPIValidator()
    
    # Check cache size
    if len(validator.npi_cache) == 0:
        print("✗ Cache is empty - no NPIs loaded")
        return False
    
    print(f"✓ Cache loaded with {len(validator.npi_cache)} NPIs")
    
    # Check for some valid and invalid NPIs from the file
    test_cases = [
        ("1588997233", True),   # Should be valid
        ("1000239023", False),  # Should be invalid
        ("1003004284", True),   # Should be valid
        ("1111111111", False),  # Should be invalid
    ]
    
    for npi, expected_valid in test_cases:
        if npi in validator.npi_cache:
            actual_valid = validator.npi_cache[npi]
            if actual_valid == expected_valid:
                print(f"✓ NPI {npi} correctly cached as {'valid' if expected_valid else 'invalid'}")
            else:
                print(f"✗ NPI {npi} cached as {'valid' if actual_valid else 'invalid'}, expected {'valid' if expected_valid else 'invalid'}")
                return False
        else:
            print(f"✗ NPI {npi} not found in cache")
            return False
    
    print("✓ All cache loading tests passed")
    return True


def main():
    """
    Run all tests for NPI 1588997233 validation.
    """
    print("=" * 60)
    print("Testing NPI 1588997233 validation from cache")
    print("=" * 60)
    
    # Test cache loading
    if not test_cache_loading():
        print("\n✗ Cache loading tests FAILED")
        return False
    
    # Test specific NPI validation
    if not test_npi_1588997233_from_cache():
        print("\n✗ NPI 1588997233 validation tests FAILED")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("NPI 1588997233 is correctly validated as VALID from cache without API calls")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
