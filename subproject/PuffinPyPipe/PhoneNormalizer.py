#!/usr/bin/env python3
"""
Phone Number Normalization Utilities
Provides phone number parsing, validation, and normalization using the phonenumbers library.
"""

import pandas as pd
import phonenumbers
from phonenumbers import NumberParseException
import re
from typing import Optional, Tuple


class PhoneNormalizer:
    """Phone number normalization and processing utilities"""
    
    @staticmethod
    def _extract_extension_from_text(phone_text: str) -> Tuple[str, Optional[str]]:
        """
        Extract phone extension from mixed text field
        Returns: (clean_phone, extension)
        """
        if not phone_text or pd.isna(phone_text):
            return "", None
            
        phone_text = str(phone_text).strip()
        if not phone_text:
            return "", None
            
        # Common extension patterns
        extension_patterns = [
            r'\s+ext\.?\s*(\d+)',
            r'\s+extension\s+(\d+)',
            r'\s+x\s*(\d+)',
            r'\s+#\s*(\d+)',
            r'\s+ext\s+(\d+)',
        ]
        
        for pattern in extension_patterns:
            match = re.search(pattern, phone_text, re.IGNORECASE)
            if match:
                extension = match.group(1)
                clean_phone = re.sub(pattern, '', phone_text, flags=re.IGNORECASE).strip()
                return clean_phone, extension
                
        return phone_text, None
    
    @staticmethod
    def _normalize_phone_number(raw_phone: str, default_country: str = 'US') -> Tuple[Optional[str], Optional[str], bool, Optional[str]]:
        """
        Normalize phone number using phonenumbers library
        Returns: (e164_format, country_code, success, error_message)
        """
        if not raw_phone or pd.isna(raw_phone):
            return None, None, False, "Empty phone number"
            
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(raw_phone, default_country)
            
            # Validate the number
            if not phonenumbers.is_valid_number(parsed_number):
                return None, None, False, "Invalid phone number format"
                
            # Get E164 format and country code
            e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            country_code = str(parsed_number.country_code)
            
            return e164_format, country_code, True, None
            
        except NumberParseException as e:
            return None, None, False, f"Parse error: {str(e)}"
        except Exception as e:
            return None, None, False, f"Unexpected error: {str(e)}"
    
    @staticmethod
    def normalize_phone_with_extension(raw_phone: str, raw_extension: Optional[str] = None, default_country: str = 'US') -> dict:
        """
        Complete phone normalization workflow including extension extraction
        Returns: dict with normalized phone data
        """
        result = {
            'original_phone': raw_phone,
            'original_extension': raw_extension,
            'clean_phone': None,
            'extracted_extension': None,
            'final_extension': None,
            'e164_format': None,
            'country_code': None,
            'is_success': False,
            'error_message': None
        }
        
        # Extract extension from main phone text if not already provided
        if pd.isna(raw_extension) or not raw_extension:
            clean_phone, extracted_extension = PhoneNormalizer._extract_extension_from_text(raw_phone)
            result['clean_phone'] = clean_phone
            result['extracted_extension'] = extracted_extension
            result['final_extension'] = extracted_extension
            phone_to_normalize = clean_phone
        else:
            result['clean_phone'] = raw_phone
            result['final_extension'] = raw_extension
            phone_to_normalize = raw_phone
        
        # Normalize the phone number
        e164_format, country_code, success, error_msg = PhoneNormalizer._normalize_phone_number(phone_to_normalize, default_country)
        
        result['e164_format'] = e164_format
        result['country_code'] = country_code
        result['is_success'] = success
        result['error_message'] = error_msg
        
        return result
