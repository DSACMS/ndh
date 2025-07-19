# CSViper Invoker Command Design

## Overview

The `invoke_compiled_script` command is designed to handle dynamic file selection and execution of compiled CSViper import scripts. This command addresses the common scenario where data files change names over time (e.g., with date stamps) and users need to automatically find and process the latest version.

## Command Structure

```bash
python -m csviper invoke_compiled_script \
    --run_import_from=<importer_directory> \
    --import_data_from_dir=<data_search_directory> \
    --database_type=<mysql|postgresql>
```

### Parameters

- `--run_import_from`: Directory containing the compiled CSViper scripts and metadata
- `--import_data_from_dir`: Directory to search for data files (searches recursively)
- `--database_type`: Database type (mysql or postgresql) to determine which script to execute

## Directory Structure Assumptions

Each importer directory should contain:

```
nppes_main/
├── npidata_pfile_20050523-20250608.metadata.json  # Single metadata file
├── go.mysql.py                                    # MySQL import script
├── go.postgresql.py                               # PostgreSQL import script
├── *.create_table_mysql.sql                       # Generated SQL files
├── *.create_table_postgres.sql
└── *.import_data_*.sql
```

**Key Requirement**: Each importer directory must contain exactly one `*.metadata.json` file.

## Enhanced Metadata Structure

The metadata.json file will be extended to include file discovery information:

```json
{
  "filename": "npidata_pfile_20050523-20250608.csv",
  "filename_without_extension": "npidata_pfile_20050523-20250608",
  "file_glob_pattern": "npidata_pfile_*.csv",
  "recursive_search": true,
  "full_path": "/original/path/to/npidata_pfile_20050523-20250608.csv",
  "file_size_bytes": 2147483648,
  "delimiter": ",",
  "quote_character": "\"",
  "encoding": "utf-8",
  "original_column_names": [...],
  "normalized_column_names": [...],
  "column_name_mapping": {...},
  "max_column_lengths": {...},
  "total_columns": 330,
  "column_headers_hash": "abc123def456..."
}
```

### New Metadata Fields

- `file_glob_pattern`: Glob pattern to match similar files (auto-generated from original filename)
- `recursive_search`: Whether to search subdirectories recursively (default: true)

## Implementation Architecture

### 1. New Module: `src/csviper/script_invoker.py`

```python
class CompiledScriptInvoker:
    @staticmethod
    def invoke_from_directory(run_import_from: str, import_data_from_dir: str, 
                            database_type: str) -> None:
        """Main entry point for directory-based import invocation."""
        
    @staticmethod
    def _load_directory_metadata(directory: str) -> Dict[str, Any]:
        """Find and load the single metadata.json file in directory."""
        
    @staticmethod
    def _find_latest_data_file(search_dir: str, pattern: str, recursive: bool) -> str:
        """Find the most recently modified file matching the pattern."""
        
    @staticmethod
    def _confirm_file_selection(file_path: str) -> bool:
        """Present file to user for confirmation."""
        
    @staticmethod
    def _execute_import_script(script_dir: str, csv_file: str, db_type: str) -> None:
        """Execute go.mysql.py or go.postgresql.py with the CSV file."""
```

### 2. CLI Integration in `__main__.py`

Add new command to the existing CLI structure:

```python
@cli.command()
@click.option('--run_import_from', required=True, type=click.Path(exists=True),
              help='Directory containing compiled CSViper scripts and metadata')
@click.option('--import_data_from_dir', required=True, type=click.Path(exists=True),
              help='Directory to search for data files')
@click.option('--database_type', required=True, type=click.Choice(['mysql', 'postgresql']),
              help='Database type for import script selection')
def invoke_compiled_script(run_import_from, import_data_from_dir, database_type):
    """
    Execute compiled import scripts with automatic file discovery.
    
    Finds the latest data file matching the pattern stored in metadata
    and executes the appropriate database import script.
    """
```

### 3. Metadata Enhancement in `metadata_extractor.py`

Extend `CSVMetadataExtractor.fromFileToMetadata()` to include:

```python
@staticmethod
def _generate_file_glob_pattern(filename: str) -> str:
    """
    Generate a glob pattern from a filename by replacing date-like patterns with wildcards.
    
    Examples:
    - npidata_pfile_20050523-20250608.csv → npidata_pfile_*.csv
    - PPEF_Enrollment_Extract_2025.04.01.csv → PPEF_Enrollment_Extract_*.csv
    - sales_data_2024_Q4.csv → sales_data_*.csv
    """
```

## Workflow Logic

### 1. Metadata Discovery
- Scan `--run_import_from` directory for `*.metadata.json` files
- Ensure exactly one metadata file exists
- Load metadata to extract `file_glob_pattern`

### 2. File Discovery
- Search `--import_data_from_dir` using the glob pattern
- Search recursively through subdirectories if `recursive_search` is true
- Sort matching files by modification time (newest first)

### 3. User Confirmation
- Display the latest matching file with metadata:
  - Full path
  - File size
  - Modification date
- Prompt: "Use this file for import? [Y/n]"
- Allow user to abort or continue

### 4. Script Execution
- Select appropriate script based on `--database_type`:
  - `go.mysql.py` for MySQL
  - `go.postgresql.py` for PostgreSQL
- Execute script with `--csv_file=<selected_file>` parameter
- Pass through any additional environment variables or parameters

## Example Usage Scenarios

### NPPES Main Data Import
```bash
python -m csviper invoke_compiled_script \
    --run_import_from=./nppes_main \
    --import_data_from_dir=/data/cms/nppes \
    --database_type=postgresql
```

### PECOS Enrollment Import
```bash
python -m csviper invoke_compiled_script \
    --run_import_from=./pecos_enrollment \
    --import_data_from_dir=/data/cms/pecos \
    --database_type=mysql
```

## Expected User Experience

```bash
$ python -m csviper invoke_compiled_script --run_import_from=./nppes_main --import_data_from_dir=/data/downloads --database_type=postgresql

Loading metadata from: ./nppes_main/npidata_pfile_20050523-20250608.metadata.json
Searching for files matching 'npidata_pfile_*.csv' in /data/downloads...

Found 3 matching files:
  1. npidata_pfile_20050523-20250608.csv (2.1 GB, modified: 2025-01-04 15:30:22)
  2. npidata_pfile_20050523-20241201.csv (2.0 GB, modified: 2024-12-01 10:15:33)
  3. npidata_pfile_20050523-20241101.csv (1.9 GB, modified: 2024-11-01 09:22:11)

Latest file: /data/downloads/npidata_pfile_20050523-20250608.csv
Use this file for import? [Y/n]: y

Executing: python ./nppes_main/go.postgresql.py --csv_file=/data/downloads/npidata_pfile_20050523-20250608.csv
```

## Error Handling

The invoker must handle these scenarios:

### Metadata Issues
- **No metadata file found** in run_import_from directory
- **Multiple metadata files** found (should be exactly one)
- **Corrupted or invalid metadata** file

### File Discovery Issues
- **No matching data files** found in import_data_from_dir
- **Pattern matching failures** (invalid glob patterns)
- **Permission issues** accessing search directories

### Script Execution Issues
- **Missing import script** (go.mysql.py or go.postgresql.py)
- **Invalid database_type** parameter
- **Script execution failures**

### User Interaction Issues
- **User cancellation** during confirmation
- **Invalid user input** during confirmation prompts

## Pattern Generation Rules

The automatic glob pattern generation should follow these rules:

1. **Date patterns**: Replace date-like sequences with wildcards
   - `YYYY-MM-DD` → `*`
   - `YYYYMMDD` → `*`
   - `YYYY.MM.DD` → `*`

2. **Version patterns**: Replace version-like sequences
   - `v1.2.3` → `v*`
   - `2024_Q4` → `*`

3. **Preserve structure**: Keep the core filename structure intact
   - `npidata_pfile_20050523-20250608.csv` → `npidata_pfile_*.csv`
   - `PPEF_Enrollment_Extract_2025.04.01.csv` → `PPEF_Enrollment_Extract_*.csv`

## Future Enhancements

### Advanced Pattern Matching
- Support for multiple glob patterns per metadata file
- Exclusion patterns to ignore backup or temporary files
- Age-based filtering (ignore files older than N days)

### Enhanced User Experience
- `--auto_confirm` flag to skip user confirmation
- `--dry_run` flag to show what would be executed without running
- Progress indicators for large file searches

### Integration Features
- Integration with existing PuffinPyPipe shell scripts
- Support for environment variable configuration
- Logging and audit trail capabilities

## Backward Compatibility

For existing metadata files that don't include the new fields:
1. Auto-generate `file_glob_pattern` from the original filename
2. Set `recursive_search` to `true` by default
3. Optionally update the metadata file with generated values

This ensures existing compiled scripts continue to work without modification.
