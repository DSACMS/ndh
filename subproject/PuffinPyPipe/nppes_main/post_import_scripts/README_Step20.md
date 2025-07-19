# Step 20: Create Performance Indexes for Core NPI Tables

## Overview

This script creates performance indexes on the core NDH NPI tables after data transformation. It should be run after Step15 (data transformation) and before Step25 (analysis).

## Purpose

Creates optimized indexes to improve query performance for:
- Common lookup patterns
- Foreign key relationships
- Analytical queries
- Change tracking analysis

## What it does

The script creates 34 indexes across 6 phases:

### Phase 1: Core NPI Table Indexes (Steps 1-5)
- Primary NPI lookup index
- Entity type filtering index
- Last update date index for change detection
- Partial indexes for deactivated and replacement NPIs

### Phase 2: Individual Table Indexes (Steps 6-9)
- Name-based matching indexes
- Last name index for searches
- Full name composite index
- Complete name index including prefix/suffix

### Phase 3: NPI-to-Individual Relationship Indexes (Steps 10-13)
- Foreign key indexes for both directions
- Sole proprietor filtering index
- Sex code distribution index

### Phase 4: NPI-to-ClinicalOrganization Relationship Indexes (Steps 14-17)
- NPI foreign key index
- Parent hierarchy index (partial for non-null values)
- Authorized official index
- Clinical organization index (partial for non-null values)

### Phase 5: Error Tracking Indexes (Steps 18-20)
- NPI error lookup index
- Error type filtering index
- Combined NPI-error type index

### Phase 6: Change Tracking Indexes for Analysis (Steps 21-34)
- Processing run status and date indexes
- Change log indexes for all tracking tables
- Processed status indexes for incremental processing

## Usage

### Dry-run mode (recommended first):
```bash
cd nppes_main/post_import_scripts
python Step20_create_npi_indexes.py
```

### Production mode:
Edit the script and change `is_just_print = False` on line 25, then run:
```bash
python Step20_create_npi_indexes.py
```

## Key Features

- **Safe Execution**: Uses `IF NOT EXISTS` to avoid conflicts
- **Partial Indexes**: Creates partial indexes for sparse data (WHERE clauses)
- **Composite Indexes**: Optimizes common multi-column query patterns
- **OLTP and Analytics**: Supports both transactional and analytical workloads
- **Modular Design**: Separated from data transformation for clarity

## Index Types Created

### Primary Lookup Indexes
- Single column indexes for primary key lookups
- Entity type filtering for individual vs organizational NPIs

### Relationship Indexes
- Foreign key indexes for join performance
- Bidirectional relationship indexes

### Analytical Indexes
- Change tracking and audit trail indexes
- Date-based indexes for temporal analysis
- Status-based indexes for filtering

### Partial Indexes
- Only indexes non-null values where appropriate
- Reduces index size and maintenance overhead
- Optimizes for actual data patterns

## Performance Benefits

- **Faster Queries**: Dramatically improves lookup performance
- **Efficient Joins**: Optimizes foreign key relationships
- **Quick Filtering**: Enables fast filtering on common criteria
- **Analytical Speed**: Accelerates reporting and analysis queries

## Prerequisites

- Step15 (data transformation) must be completed successfully
- NDH and intake schemas must exist
- Required tables must be populated

## Dependencies

- plainerflow
- PostgreSQL database connection

## Monitoring

After running, check index usage with:
```sql
SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE schemaname IN ('ndh', 'intake')
ORDER BY idx_tup_read DESC;
```

## Next Steps

After completing Step20, run Step25 for comprehensive data analysis and quality checks.
