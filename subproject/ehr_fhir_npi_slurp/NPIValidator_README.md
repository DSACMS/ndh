# NPIValidator Class

## Overview

The `NPIValidator` class provides a cached validation system for NPI (National Provider Identifier) numbers against the CMS NPI Registry API. It implements an efficient caching mechanism to avoid redundant API calls and persists validation results between sessions.

## Features

- **Caching**: Loads and saves validation results to/from CSV cache file
- **API Integration**: Validates NPIs against the official CMS NPI Registry API
- **Format Validation**: Checks NPI format (10 digits) before API calls
- **Error Handling**: Robust error handling with retry logic
- **Persistence**: Automatically saves new validation results to cache file

## Usage

### Basic Usage

```python
from NPIValidator import NPIValidator

# Initialize validator (uses default cache file)
validator = NPIValidator()

# Validate an NPI
is_valid = validator.is_this_npi_valid(npi_value="1234567890")
print(f"NPI is valid: {is_valid}")
```

### Custom Cache File

```python
# Use a custom cache file location
validator = NPIValidator(cache_file_path="./my_custom_cache.csv")

# Validate multiple NPIs
test_npis = ["1234567890", "1568495397", "1023456789"]
for npi in test_npis:
    is_valid = validator.is_this_npi_valid(npi_value=npi)
    print(f"NPI {npi}: {'Valid' if is_valid else 'Invalid'}")
```

## Cache File Format

The cache file is a CSV with the following columns:
- `npi`: The NPI number (10 digits)
- `is_invalid`: Either "Valid NPI" or "Invalid NPI"

Example cache file content:
```csv
npi,is_invalid
1234567890,Invalid NPI
1568495397,Invalid NPI
1003004284,Valid NPI
1003026204,Valid NPI
```

## API Integration

The validator uses the official CMS NPI Registry API:
- **Endpoint**: `https://npiregistry.cms.hhs.gov/api/?version=2.1&number={npi}`
- **Retry Logic**: Up to 3 attempts with exponential backoff
- **Rate Limiting**: Small delays between API calls to be respectful
- **Timeout**: 10 seconds per API call

## Methods

### `__init__(*, cache_file_path=None)`

Initialize the validator with optional custom cache file path.

**Parameters:**
- `cache_file_path` (str, optional): Path to CSV cache file. Defaults to `./prod_data/valid_npi_list.csv`

### `is_this_npi_valid(*, npi_value)`

Validate an NPI number, checking cache first, then API if needed.

**Parameters:**
- `npi_value` (str): The NPI number to validate

**Returns:**
- `bool`: True if NPI is valid, False otherwise

**Example:**
```python
validator = NPIValidator()
is_valid = validator.is_this_npi_valid(npi_value="1234567890")
```

## Implementation
