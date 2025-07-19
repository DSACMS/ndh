#!/usr/bin/env python3
"""
Step 20: Create Performance Indexes for Core NPI Tables

This script creates performance indexes on the core NDH NPI tables after data transformation.
It should be run after Step15 (data transformation) and before Step25 (analysis).

Key Features:
- Creates indexes on frequently queried columns
- Uses IF NOT EXISTS to avoid conflicts
- Optimizes query performance for common operations
- Separate from data transformation for modularity

Indexes Created:
- ndh.npi: npi, entity_type_code
- ndh.individual: name components for matching
- ndh.individual_npi: foreign key relationships
- ndh.organizational_npi: foreign key relationships and parent hierarchy
- intake.wrongnpi: error analysis indexes
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle  # type: ignore
import os

def main():
    # Control dry-run mode - start with True to preview SQL
    is_just_print = True
    
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    # Define target tables
    npi_DBTable = DBTable(schema='ndh', table='npi')
    individual_DBTable = DBTable(schema='ndh', table='individual')
    npi_to_individual_DBTable = DBTable(schema='ndh', table='individual_npi')
    npi_to_clinical_org_DBTable = DBTable(schema='ndh', table='organizational_npi')
    wrongnpi_DBTable = DBTable(schema='intake', table='wrongnpi')
    
    # Intake tracking tables for analysis
    processing_run_DBTable = DBTable(schema='intake', table='npi_processing_run')
    npi_change_log_DBTable = DBTable(schema='intake', table='npi_change_log')
    individual_change_log_DBTable = DBTable(schema='intake', table='individual_change_log')
    parent_change_log_DBTable = DBTable(schema='intake', table='parent_relationship_change_log')
    
    # Create SQL execution plan
    sql = FrostDict()
    
    # ========================================
    # PHASE 1: Core NPI table indexes
    # ========================================
    
    sql['01_create_npi_primary_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_npi ON {npi_DBTable}(npi);
    """
    
    sql['02_create_npi_entity_type_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_entity_type ON {npi_DBTable}(entity_type_code);
    """
    
    sql['03_create_npi_last_update_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_last_update ON {npi_DBTable}(last_update_date);
    """
    
    sql['04_create_npi_deactivation_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_deactivation ON {npi_DBTable}(deactivation_date) WHERE deactivation_date IS NOT NULL;
    """
    
    sql['05_create_npi_replacement_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_replacement ON {npi_DBTable}(replacement_npi) WHERE replacement_npi IS NOT NULL;
    """
    
    # ========================================
    # PHASE 2: Individual table indexes
    # ========================================
    
    sql['06_create_individual_names_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_individual_names ON {individual_DBTable}(last_name, first_name);
    """
    
    sql['07_create_individual_last_name_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_individual_last_name ON {individual_DBTable}(last_name);
    """
    
    sql['08_create_individual_full_name_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_individual_full_name ON {individual_DBTable}(last_name, first_name, middle_name);
    """
    
    sql['09_create_individual_complete_name_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_individual_complete_name ON {individual_DBTable}(last_name, first_name, middle_name, name_prefix, name_suffix);
    """
    
    # ========================================
    # PHASE 3: NPI-to-Individual relationship indexes
    # ========================================
    
    sql['10_create_npi_to_individual_npi_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_to_individual_npi ON {npi_to_individual_DBTable}(npi_id);
    """
    
    sql['11_create_npi_to_individual_individual_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_to_individual_individual ON {npi_to_individual_DBTable}(individual_id);
    """
    
    sql['12_create_npi_to_individual_sole_proprietor_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_to_individual_sole_proprietor ON {npi_to_individual_DBTable}(is_sole_proprietor) WHERE is_sole_proprietor = TRUE;
    """
    
    # ========================================
    # PHASE 4: NPI-to-ClinicalOrganization relationship indexes
    # ========================================
    
    sql['14_create_npi_to_clinical_org_npi_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_to_clinical_org_npi ON {npi_to_clinical_org_DBTable}(npi_id);
    """
    
    sql['15_create_npi_to_clinical_org_parent_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_to_clinical_org_parent ON {npi_to_clinical_org_DBTable}(parent_npi_id) WHERE parent_npi_id IS NOT NULL;
    """
    
    sql['16_create_npi_to_clinical_org_individual_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_to_clinical_org_individual ON {npi_to_clinical_org_DBTable}(primary_authorized_official_individual_id);
    """
    
    sql['17_create_npi_to_clinical_org_clinical_org_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_to_clinical_org_clinical_org ON {npi_to_clinical_org_DBTable}(clinical_organization_id) WHERE clinical_organization_id IS NOT NULL;
    """
    
    # ========================================
    # PHASE 5: Error tracking indexes
    # ========================================
    
    sql['18_create_wrongnpi_npi_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_wrongnpi_npi ON {wrongnpi_DBTable}(npi);
    """
    
    sql['19_create_wrongnpi_error_type_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_wrongnpi_error_type ON {wrongnpi_DBTable}(error_type_string);
    """
    
    sql['20_create_wrongnpi_combined_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_wrongnpi_npi_error_type ON {wrongnpi_DBTable}(npi, error_type_string);
    """
    
    # ========================================
    # PHASE 6: Change tracking indexes for analysis
    # ========================================
    
    sql['21_create_processing_run_status_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_processing_run_status ON {processing_run_DBTable}(processing_status);
    """
    
    sql['22_create_processing_run_date_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_processing_run_date ON {processing_run_DBTable}(run_date);
    """
    
    sql['23_create_npi_change_log_run_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_change_log_run ON {npi_change_log_DBTable}(processing_run_id);
    """
    
    sql['24_create_npi_change_log_npi_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_change_log_npi ON {npi_change_log_DBTable}(npi);
    """
    
    sql['25_create_npi_change_log_type_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_change_log_type ON {npi_change_log_DBTable}(change_type);
    """
    
    sql['26_create_npi_change_log_processed_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_npi_change_log_processed ON {npi_change_log_DBTable}(processed);
    """
    
    sql['27_create_individual_change_log_run_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_individual_change_log_run ON {individual_change_log_DBTable}(processing_run_id);
    """
    
    sql['28_create_individual_change_log_individual_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_individual_change_log_individual ON {individual_change_log_DBTable}(individual_id) WHERE individual_id IS NOT NULL;
    """
    
    sql['29_create_individual_change_log_npi_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_individual_change_log_npi ON {individual_change_log_DBTable}(npi);
    """
    
    sql['30_create_parent_change_log_run_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_parent_change_log_run ON {parent_change_log_DBTable}(processing_run_id);
    """
    
    sql['31_create_parent_change_log_child_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_parent_change_log_child ON {parent_change_log_DBTable}(child_npi);
    """
    
    sql['32_create_parent_change_log_old_parent_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_parent_change_log_old_parent ON {parent_change_log_DBTable}(old_parent_npi) WHERE old_parent_npi IS NOT NULL;
    """
    
    sql['33_create_parent_change_log_new_parent_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_parent_change_log_new_parent ON {parent_change_log_DBTable}(new_parent_npi) WHERE new_parent_npi IS NOT NULL;
    """
    
    sql['34_create_parent_change_log_type_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_parent_change_log_type ON {parent_change_log_DBTable}(change_type);
    """
    
    # Execute SQL pipeline
    print("About to create Core NPI Performance Indexes")
    print("=" * 60)
    print("This script will create indexes for:")
    print("1. Core NPI table - primary lookups and filtering")
    print("2. Individual table - name matching and searches")
    print("3. NPI-to-Individual relationships - foreign key performance")
    print("4. NPI-to-ClinicalOrganization relationships - hierarchy queries")
    print("5. Error tracking - wrongnpi analysis")
    print("6. Change tracking - audit trail analysis")
    print("=" * 60)
    print("Key Features:")
    print("- Uses IF NOT EXISTS to avoid conflicts")
    print("- Partial indexes for sparse data (WHERE clauses)")
    print("- Composite indexes for common query patterns")
    print("- Optimized for both OLTP and analytical queries")
    print("=" * 60)
    
    SQLoopcicle.run_sql_loop(
        sql_dict=sql,
        is_just_print=is_just_print,
        engine=alchemy_engine
    )
    
    print("\n" + "=" * 60)
    print("✅ Index creation completed!")
    print("Next step: Run Step25 for analysis and data quality checks")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Core NPI Index Creation failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        print("\nAlso ensure Step15 has been run successfully first.")
        raise
