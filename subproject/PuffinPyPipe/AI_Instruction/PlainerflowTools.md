# PlainerFlow Tools: Simple ETL Pipeline Programming Guide

## Overview

PlainerFlow is a Python framework for creating simple, SQL-based ETL (Extract, Transform, Load) pipelines. It provides a clean interface for executing SQL statements in sequence with proper error handling, logging, and database connection management.

## Core Components

### 1. CredentialFinder - Database Connection Management

Automatically detects database configuration from various sources:

```python
from plainerflow import CredentialFinder

# Auto-detect from environment variables, .env files, or fallback to SQLite
engine = CredentialFinder.detect_config(verbose=True)

# Specify custom .env file location, which will always be in the parent to parent directory when making post_import_script directory scripts..
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
engine = CredentialFinder.detect_config(verbose=True, env_path=env_path)
```

### 2. DBTable - Database Table References

Create reusable table references that work across different schemas:

```python
from plainerflow import DBTable

# Define table with schema, always name the variables with something_DBTable at the end. 
npi_DBTable = DBTable(schema='nppes_raw', table='main_file')
customers_DBTable = DBTable(schema='public', table='customers')

#For similar table names, use the create_child syntax
npi_something_DBTable = npi_DBTable.create_child('_something')


# Use in SQL via f-strings
sql = f"SELECT * FROM {npi_table} WHERE status = 'active'"
```

### 3. FrostDict - Immutable SQL Configuration

Organize SQL statements in an ordered, partially-immutable dictionary:

```python
from plainerflow import FrostDict

sql = FrostDict()

# Add SQL statements in execution order
sql['create_table'] = f"CREATE TABLE {table_name} AS SELECT ..."
sql['add_index'] = f"CREATE INDEX idx_name ON {table_name}(column)"
sql['update_data'] = f"UPDATE {table_name} SET ..."

# Keys cannot be reassigned once set (prevents accidental overwrites)
```

### 4. SQLoopcicle - SQL Execution Engine

Execute SQL statements in sequence with built-in error handling:

```python
from plainerflow import SQLoopcicle

is_just_print = True # Always start with true for dry-run to allow the user to read generated SQL before it runs.. 


# Execute all SQL statements
SQLoopcicle.run_sql_loop(
    sql_dict=sql,
    engine=engine,
    is_just_print=is_just_print  
)
```

### 5. InLaw - Data Validation Framework

Initial creation of ETLs should not include InLaw statements. But once the user requests that they be added:
Create validation tests to ensure data quality using Great Expectations:

```python
from plainerflow import InLaw

class ValidateRowCount(InLaw):
    title = "Table should have expected number of rows"
    
    @staticmethod
    def run(engine):
        sql = "SELECT COUNT(*) as row_count FROM my_table"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Use Great Expectations to validate the data
        result = gx_df.expect_column_values_to_be_between(
            column="row_count", 
            min_value=1, 
            max_value=1000000
        )
        
        if result.success:
            return True
        return f"Row count validation failed: expected 1-1,000,000 rows"

class ValidateNoNullValues(InLaw):
    title = "Check for null values in required columns"
    
    @staticmethod
    def run(engine):
        sql = "SELECT COUNT(*) as null_count FROM my_table WHERE required_column IS NULL"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect exactly 0 null values (using min=0, max=0 to check for equality)
        result = gx_df.expect_column_values_to_be_between(
            column="null_count", 
            min_value=0,
            max_value=0
        )
        
        if result.success:
            return True
        return f"Found null values in required column"

# Run all validation tests
test_results = InLaw.run_all(engine=engine)
```

**Key InLaw Pattern:**
1. Write SQL that returns data to validate (not violations)
2. Use `InLaw.to_gx_dataframe(sql, engine)` to convert to GX DataFrame
3. Use Great Expectations methods like `expect_column_values_to_be_between()`, `expect_column_values_to_be_unique()`, etc.
4. Check `result.success` and return True/False with descriptive error messages

**Available GX Expectations (Commonly Used):**
- `expect_column_values_to_be_between(column, min_value, max_value)` - Range validation
- `expect_column_values_to_be_unique(column)` - Uniqueness validation
- `expect_column_values_to_not_be_null(column)` - Non-null validation
- `expect_column_values_to_be_null(column)` - Null validation
- `expect_table_row_count_to_equal(value)` - Exact row count
- `expect_table_row_count_to_be_between(min_value, max_value)` - Row count range
- `expect_column_sum_to_be_between(column, min_value, max_value)` - Sum validation
- `expect_column_values_to_match_regex(column, regex)` - Pattern matching

**Tips for equality testing:**
- Use `expect_column_values_to_be_between(column, min_value=0, max_value=0)` to test for exactly 0
- Use `expect_table_row_count_to_equal(value)` for exact row counts
- See ../plainerflow/docs/InLaw_README.md for complete list of available expectations

InLaw `run_all()` prints the results of the tests, so there is nothing to do with test_results unless you want to inspect some specific result for some reason.
Usually the run_all function is the last thing to do with the InLaw part of the process.

## Typical Usage Pattern for Post-Import ETL

### Directory Structure

Place your ETL scripts in the csviper-generated folder structure:

```diagram
your_import_folder/
├── post_import_scripts/
│   ├── Step01_fix_data_types.py
│   ├── Step02_some_big_step.py
│   └── Step03_data_cleanup.py
```

### Basic Script Template

Based on the real-world example in `Step05_fix_column_types.py`:

```python
#!/usr/bin/env python3
"""
ETL Pipeline Step: [Description of what this step does]
"""

import plainerflow
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle
import os

def main():
    # Control dry-run mode
    is_just_print = False  # Set to True to preview SQL without execution
    
    print("Connecting to DB")
    
    # Get database connection from parent directory's .env file
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    # Define target table
    # npi_table = 'main_file_small'  # For testing
    npi_table = 'main_file'  # For production
    npi_DBTable = DBTable(schema='nppes_raw', table=npi_table)
    
    # Create SQL execution plan
    sql = FrostDict()
    
    # Add SQL statements in execution order
    sql['step_1_description'] = f"""
    ALTER TABLE {npi_DBTable}
    ALTER COLUMN npi TYPE BIGINT USING npi::BIGINT;
    """
    
    sql['step_2_description'] = f"""
    CREATE INDEX IF NOT EXISTS idx_{npi_table}_npi 
    ON {npi_DBTable}(npi);
    """
    
    # Execute SQL pipeline
    print("About to run SQL")
    SQLoopcicle.run_sql_loop(
        sql_dict=sql,
        is_just_print=is_just_print,
        engine=alchemy_engine
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        raise
```

## Real-World Example: Data Type Conversion

Based on `nppes_main/post_import_scripts/Step05_fix_column_types.py`, here's how to handle complex data transformations:

## Best Practices

### 1. Safe Column Transformations

- Always create new columns first, then populate, then drop old columns
- Use the "new_column" → populate → drop → rename pattern
- This prevents data loss if transformation fails

### 2. SQL Organization

- Use descriptive keys in FrostDict for each SQL step
- Group related operations together
- Include step numbers or logical ordering in key names

### 3. Error Handling and Testing

- Use `is_just_print=True` for dry-run testing
- Test with small datasets first (`main_file_small` vs `main_file`)
- Include validation steps after major transformations

### 4. Environment Configuration

- Store database credentials in `.env` files
- Use relative paths to find `.env` files from script location
- Never hardcode credentials in scripts
- Do not overwrite existing .env files

### 5. Performance Considerations

- Create indexes as a final step  after data loading and transformation
- Use batch operations for large data sets
- Consider transaction boundaries for large operations

## Running ETL Scripts

```bash
# Run individual ETL step
python3 post_import_scripts/Step01_fix_data_types.py

# Run all steps in sequence
for script in post_import_scripts/Step*.py; do
    echo "Running $script"
    python3 "$script"
done
```

## Advanced Features

### 1. Conditional SQL Execution

```python
# Check if transformation is needed
sql['check_if_conversion_needed'] = f"""
SELECT COUNT(*) as needs_conversion
FROM information_schema.columns 
WHERE table_name='{table_name}' 
AND column_name='npi' 
AND data_type='character varying';
"""

# Only run conversion if needed (would require custom logic)
```

## Integration with CSViper

PlainerFlow is designed to work seamlessly with CSViper-generated import structures:

1. **CSViper** handles initial CSV-to-database import
2. **PlainerFlow** handles post-import transformations and cleanup
3. Both use the same environment configuration (`.env` files)
4. Scripts are organized in the `post_import_scripts/` directory
5. Table references use the same schema structure

This combination provides a complete ETL solution from raw CSV files to production-ready database tables with proper data types, indexes, and validation.
