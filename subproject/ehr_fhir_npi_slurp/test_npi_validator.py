#!/usr/bin/env python3
"""
Simple test script for NPIValidator
"""

import re
from NPIValidator import NPIValidator

def test_npi_validator():
    """Test the NPIValidator class"""
    
    # Initialize validator
    validator = NPIValidator()
    
    # Test with some example NPIs
    test_npis = [
        "1234567890",  # Valid format, but likely not a real NPI
        "123456789",   # Invalid format (9 digits)
        "12345678901", # Invalid format (11 digits)
        "1234567890abcd", # Invalid format (contains letters)
        "1568495397",  # Real NPI that is invalid
        "1588997233",  # Real NPI that is valid
        ""             # Empty string
    ]
    
    print("Testing NPIValidator:")
    print("-" * 75)
    print(f"{'NPI':<15} {'Format OK':<10} {'Cached As':<12} {'Validator Says':<15} {'Source':<10}")
    print("-" * 75)
    
    for npi in test_npis:
        try:
            # Check format
            format_ok = validator._is_valid_npi_format(npi_value=npi)
            
            # Check what's in cache
            clean_npi = re.sub(r'\D', '', str(npi))
            if clean_npi in validator.npi_cache:
                cached_result = "Valid" if validator.npi_cache[clean_npi] else "Invalid"
                source = "Cache"
            else:
                cached_result = "Not cached"
                source = "API"
            
            # Get validator result
            validator_result = validator.is_this_npi_valid(npi_value=npi)
            validator_str = "Valid" if validator_result else "Invalid"
            
            print(f"{npi:<15} {str(format_ok):<10} {cached_result:<12} {validator_str:<15} {source:<10}")
            
        except Exception as e:
            print(f"{npi:<15} Error: {e}")
    
    print("\nTest completed!")
    print("\nExpected Results:")
    print("- 1568495397: Invalid (real NPI but invalid)")
    print("- 1588997233: Valid (real valid NPI)")
    print("- Format invalid NPIs: Invalid")
    print("- Made-up NPIs: Invalid")

if __name__ == "__main__":
    test_npi_validator()
