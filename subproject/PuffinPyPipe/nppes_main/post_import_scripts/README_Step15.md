# Step 15: Incremental Core NPI Pipeline Implementation

## Overview

This script implements the Core NPI Pipeline with **incremental update support** for monthly NPPES releases. It populates the core NDH (National Directory of Healthcare Providers & Services) tables from NPPES raw data while preserving existing data and only processing changes.

## Key Features

- **Incremental Updates**: Only processes NEW, UPDATED, DEACTIVATED, or REACTIVATED NPIs
- **Change Tracking**: Comprehensive logging of all changes to intake tables
- **Data Preservation**: Maintains existing data, only updates what changed
- **Monthly Processing**: Designed for monthly NPPES file releases
- **Safe Execution**: Starts in dry-run mode by default
- **Performance Optimized**: Uses UPSERT operations and appropriate indexes

## What it does

The pipeline processes NPPES data through 11 main phases, broken into 27 small, clear SQL steps with no CTEs:

### Phase 1: Initialize Processing Run and Detect Changes

- Creates a processing run record in `intake.npi_processing_run`
- Detects changes by comparing `Last_Update_Date` with existing records
- Logs all detected changes to `intake.npi_change_log`
- Change types: NEW, UPDATED, DEACTIVATED, REACTIVATED

### Phase 2: Process NPI Record Changes (UPSERT)

- Uses PostgreSQL UPSERT (INSERT ... ON CONFLICT DO UPDATE)
- Only processes NPIs that have changes detected in Phase 1
- Updates `ndh.NPI` table with changed records only
- Preserves existing records that haven't changed

### Phase 3: Process Individual Record Changes

- Detects changes in Individual provider and authorized official names
- Logs changes to `intake.individual_change_log`
- Creates new Individual records only when needed
- Avoids duplicate Individual records

### Phase 4: Update NPI-to-Individual Relationships

- Uses UPSERT to update `ndh.NPI_to_Individual` table
- Only processes relationships for changed NPIs
- Updates sole proprietor status and sex code

### Phase 5: Update NPI-to-ClinicalOrganization Relationships

- Detects parent relationship changes for organizational subparts
- Logs parent changes to `intake.parent_relationship_change_log`
- Uses UPSERT to update `ndh.NPI_to_ClinicalOrganization` table
- Tracks NEW_PARENT, PARENT_CHANGED, PARENT_REMOVED events

### Phase 6: Error Logging and Change Processing

- Logs parent relationship errors to `intake.wrongnpi` table
- Marks all processed changes as completed
- Tracks organizations with no parent or multiple potential parents

### Phase 7: Finalize Processing Run

- Updates processing run with completion statistics
- Records total changes processed
- Marks run as completed

## Usage

### Dry-run mode (recommended first)

```bash
cd nppes_main/post_import_scripts
python Step15_populate_core_npi_tables.py
```

### Production mode

Edit the script and change `is_just_print = False` on line 32, then run:

```bash
python Step15_populate_core_npi_tables.py
```

## Data Sources

- **Input**: `nppes_raw.main_file` (or `main_file_small` for testing)
- **Output Tables**:
  - `ndh.NPI` (UPSERT operations)
  - `ndh.Individual` (INSERT new records only)
  - `ndh.NPI_to_Individual` (UPSERT operations)
  - `ndh.NPI_to_ClinicalOrganization` (UPSERT operations)
  - `intake.wrongnpi` (error logging)

- **Change Tracking Tables**:
  - `intake.npi_processing_run` (processing metadata)
  - `intake.npi_change_log` (NPI-level changes)
  - `intake.individual_change_log` (Individual record changes)
  - `intake.parent_relationship_change_log` (parent relationship changes)

## Prerequisites

- NPPES data must be imported into `nppes_raw.main_file`
- NDH and intake schemas must exist
- Required tables must be created (see `sql/create_table_sql/`)
- **NEW**: Intake change tracking tables must exist (see `sql/create_table_sql/create_intake_npi_changes.sql`)

## Monthly Processing Workflow

1. **First Run**: Processes all NPIs as NEW records
2. **Subsequent Runs**: Only processes changed NPIs based on `Last_Update_Date`
3. **Change Detection**: Compares current NPPES data with existing NDH data
4. **Incremental Updates**: Uses UPSERT operations to update only changed records
5. **Audit Trail**: Complete change history maintained in intake tables

## Error Types Logged

- **NO_PARENT**: Organizational subpart has no matching parent organization
- **MULTI_PARENT**: Organizational subpart has multiple potential parent matches

## Change Types Tracked

- **NEW**: NPI appears for first time
- **UPDATED**: NPI has newer `Last_Update_Date`
- **DEACTIVATED**: NPI has new deactivation date
- **REACTIVATED**: NPI has new reactivation date
- **NEW_PARENT**: Organization gains a parent relationship
- **PARENT_CHANGED**: Organization's parent changes
- **PARENT_REMOVED**: Organization loses parent relationship

## Performance Benefits

- **Faster Processing**: Only processes changed records
- **Reduced Database Load**: Uses efficient UPSERT operations
- **Preserved History**: Maintains complete audit trail
- **Scalable**: Handles large monthly updates efficiently

## Testing

The script includes a toggle to use `main_file_small` for testing with smaller datasets.

## Dependencies

- plainerflow
- pandas
- great-expectations
- PostgreSQL database connection

## Modular Pipeline Workflow

This script is part of a 3-step modular pipeline:

### Step 15: Data Transformation (This Script)
- Processes NPPES data into NDH tables
- Handles incremental updates and change detection
- Logs all changes for audit trail
- **Focus**: Pure data transformation logic

### Step 20: Index Creation
- Creates performance indexes after data transformation
- Optimizes query performance for analysis
- **Run**: `python Step20_create_npi_indexes.py`
- **Focus**: Database performance optimization

### Step 25: Analysis and Quality Checks
- Comprehensive data analysis and quality validation
- Performance metrics and trend analysis
- **Run**: `python Step25_analyze_npi_data.py`
- **Focus**: Data quality and business intelligence

## Complete Workflow

```bash
# 1. Transform data (this script)
python Step15_populate_core_npi_tables.py

# 2. Create indexes for performance
python Step20_create_npi_indexes.py

# 3. Analyze results and check quality
python Step25_analyze_npi_data.py
```

## Monitoring

Check processing results in:
- `intake.npi_processing_run` - Overall run statistics
- `intake.npi_change_log` - Individual NPI changes
- `intake.individual_change_log` - Name changes
- `intake.parent_relationship_change_log` - Organizational changes
