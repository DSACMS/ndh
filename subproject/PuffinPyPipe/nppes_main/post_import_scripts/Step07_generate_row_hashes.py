#!/usr/bin/env python3
"""
Step07: Generate Row Hashes for Change Detection

This script creates MD5 hashes of all column values for each row in the NPPES data.
The hashes are used to detect changes in any field, even when Last_Update_Date hasn't changed.
This provides more comprehensive change detection for incremental processing.
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle # type: ignore
import pandas as pd
import sqlalchemy
from pathlib import Path
import os
import json

def main():

    is_just_print = False  # Start in dry-run mode for safety
    
    print("🔗 Connecting to database...")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    # Load metadata to get column names dynamically
    metadata_path = os.path.abspath(os.path.join(base_path, "..", "npidata_pfile_20050523-20250608.metadata.json"))
    print(f"📋 Loading metadata from: {metadata_path}")
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    normalized_columns = metadata['normalized_column_names']
    print(f"✅ Found {len(normalized_columns)} columns in metadata")

    # Table selection
    #npi_table = 'main_file_small'  # For testing
    npi_table = 'main_file'  # For production

    npi_DBTable = DBTable(schema='nppes_raw', table=npi_table)
    print(f"🎯 Target table: {npi_DBTable}")

    sql = FrostDict()

    # Step 1: Drop existing row_hash column if it exists
    sql['01_drop_existing_row_hash_column'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN IF EXISTS row_hash;
"""

    # Step 2: Add new row_hash column
    sql['02_add_row_hash_column'] = f"""
ALTER TABLE {npi_DBTable}
ADD COLUMN row_hash VARCHAR(32);
"""

    # Step 3: Create the concatenation string dynamically
    # Build the concatenation expression by joining all columns with '|' separator
    concat_parts = []
    for column in normalized_columns:
        # Use COALESCE to handle NULL values and convert everything to TEXT
        concat_parts.append(f'COALESCE("{column}"::TEXT, \'\')')
    
    # Join all parts with ' || \'|\' || ' to create the full concatenation
    concat_expression = ' || \'|\' || '.join(concat_parts)
    
    print(f"📝 Generated concatenation expression for {len(concat_parts)} columns")
    
    # Step 4: Update the row_hash column with MD5 of concatenated values
    sql['03_populate_row_hash_with_md5'] = f"""
UPDATE {npi_DBTable}
SET row_hash = MD5({concat_expression});
"""

    # Step 5: Create index on row_hash for performance
    sql['04_create_index_on_row_hash'] = f"""
CREATE INDEX IF NOT EXISTS idx_{npi_table}_row_hash 
ON {npi_DBTable} (row_hash);
"""

    # Step 6: Analyze the table for query optimization
    sql['05_analyze_table_for_optimization'] = f"""
ANALYZE {npi_DBTable};
"""

    # Step 7: Generate summary statistics
    sql['06_generate_hash_statistics'] = f"""
SELECT 
    'Row Hash Generation Summary' as summary_type,
    COUNT(*) as total_rows,
    COUNT(DISTINCT row_hash) as unique_hashes,
    COUNT(*) - COUNT(DISTINCT row_hash) as duplicate_hash_count,
    ROUND(
        (COUNT(DISTINCT row_hash)::DECIMAL / COUNT(*)) * 100, 2
    ) as uniqueness_percentage
FROM {npi_DBTable}
WHERE row_hash IS NOT NULL;
"""

    print("\n🚀 About to execute row hash generation...")
    print(f"📊 Processing table: {npi_DBTable}")
    print(f"🔢 Columns to hash: {len(normalized_columns)}")
    print(f"🧪 Dry-run mode: {is_just_print}")
    
    if is_just_print:
        print("\n⚠️  DRY-RUN MODE: No changes will be made to the database")
        print("💡 To execute for real, edit this script and set is_just_print = False")
    
    SQLoopcicle.run_sql_loop(
        sql_dict=sql,
        is_just_print=is_just_print,
        engine=alchemy_engine
    )
    
    if not is_just_print:
        print("\n✅ Row hash generation completed successfully!")
        print("📈 Hash statistics have been generated")
        print("🔍 Use the row_hash column for efficient change detection")
    else:
        print("\n🔍 Dry-run completed - review the SQL above")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Row hash generation failed with error: {e}")
        print("\nMake sure you have:")
        print("- Installed required dependencies: pip install plainerflow pandas")
        print("- Completed Step05 (column type fixes)")
        print("- Valid database connection")
        raise
