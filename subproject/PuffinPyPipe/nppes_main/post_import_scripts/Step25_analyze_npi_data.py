#!/usr/bin/env python3
"""
Step 25: Analyze Core NPI Data and Perform Data Quality Checks

This script performs comprehensive analysis and data quality checks on the core NDH NPI tables
after data transformation and index creation. It should be run after Step15 (data transformation)
and Step20 (index creation).

Key Features:
- Comprehensive summary statistics
- Data quality validation
- Change analysis and trends
- Error pattern analysis
- Performance metrics
- Data integrity checks

Analysis Areas:
1. Processing run summary
2. NPI distribution analysis
3. Individual record analysis
4. Organizational hierarchy analysis
5. Change pattern analysis
6. Error analysis and data quality
7. Performance and completeness metrics
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
    
    # Intake tracking tables
    processing_run_DBTable = DBTable(schema='intake', table='npi_processing_run')
    npi_change_log_DBTable = DBTable(schema='intake', table='npi_change_log')
    individual_change_log_DBTable = DBTable(schema='intake', table='individual_change_log')
    parent_change_log_DBTable = DBTable(schema='intake', table='parent_relationship_change_log')
    
    # Source table for comparison
    source_DBTable = DBTable(schema='nppes_raw', table='main_file_small')  # For testing
    #source_DBTable = DBTable(schema='nppes_raw', table='main_file')  # For production
    
    # Create SQL execution plan
    sql = FrostDict()
    
    # ========================================
    # PHASE 1: Processing run summary
    # ========================================
    
    sql['01_latest_processing_run_summary'] = f"""
    SELECT 
        'Latest Processing Run Summary' as analysis_type,
        pr.id as run_id,
        pr.run_date,
        pr.source_table,
        pr.processing_status,
        pr.total_npis_processed,
        pr.new_npis,
        pr.updated_npis,
        pr.deactivated_npis,
        pr.notes,
        EXTRACT(EPOCH FROM (pr.completion_date - pr.run_date))/60 as processing_time_minutes
    FROM {processing_run_DBTable} pr
    ORDER BY pr.run_date DESC
    LIMIT 5;
    """
    
    sql['02_processing_run_trends'] = f"""
    SELECT 
        'Processing Run Trends (Last 10 Runs)' as analysis_type,
        DATE(pr.run_date) as run_date,
        pr.total_npis_processed,
        pr.new_npis,
        pr.updated_npis,
        pr.deactivated_npis,
        ROUND(pr.new_npis::DECIMAL / NULLIF(pr.total_npis_processed, 0) * 100, 2) as new_percentage,
        ROUND(pr.updated_npis::DECIMAL / NULLIF(pr.total_npis_processed, 0) * 100, 2) as updated_percentage
    FROM {processing_run_DBTable} pr
    WHERE pr.processing_status = 'COMPLETED'
    ORDER BY pr.run_date DESC
    LIMIT 10;
    """
    
    # ========================================
    # PHASE 2: NPI distribution analysis
    # ========================================
    
    sql['03_npi_distribution_summary'] = f"""
    SELECT 
        'NPI Distribution Summary' as analysis_type,
        COUNT(*) as total_npi_records,
        COUNT(*) FILTER (WHERE entity_type_code = 1) as individual_npis,
        COUNT(*) FILTER (WHERE entity_type_code = 2) as organizational_npis,
        COUNT(*) FILTER (WHERE deactivation_date IS NOT NULL) as deactivated_npis,
        COUNT(*) FILTER (WHERE reactivation_date IS NOT NULL) as reactivated_npis,
        COUNT(*) FILTER (WHERE replacement_npi IS NOT NULL) as npis_with_replacements,
        ROUND(COUNT(*) FILTER (WHERE entity_type_code = 1)::DECIMAL / COUNT(*) * 100, 2) as individual_percentage,
        ROUND(COUNT(*) FILTER (WHERE entity_type_code = 2)::DECIMAL / COUNT(*) * 100, 2) as organizational_percentage,
        ROUND(COUNT(*) FILTER (WHERE deactivation_date IS NOT NULL)::DECIMAL / COUNT(*) * 100, 2) as deactivation_percentage
    FROM {npi_DBTable};
    """
    
    sql['04_npi_enumeration_trends'] = f"""
    SELECT 
        'NPI Enumeration Trends by Year' as analysis_type,
        EXTRACT(YEAR FROM enumeration_date) as enumeration_year,
        COUNT(*) as npis_enumerated,
        COUNT(*) FILTER (WHERE entity_type_code = 1) as individual_npis,
        COUNT(*) FILTER (WHERE entity_type_code = 2) as organizational_npis
    FROM {npi_DBTable}
    WHERE enumeration_date IS NOT NULL
    AND EXTRACT(YEAR FROM enumeration_date) >= 2005
    GROUP BY EXTRACT(YEAR FROM enumeration_date)
    ORDER BY enumeration_year DESC
    LIMIT 20;
    """
    
    sql['05_npi_last_update_analysis'] = f"""
    SELECT 
        'NPI Last Update Analysis' as analysis_type,
        DATE_TRUNC('month', last_update_date) as update_month,
        COUNT(*) as npis_updated,
        COUNT(*) FILTER (WHERE entity_type_code = 1) as individual_updates,
        COUNT(*) FILTER (WHERE entity_type_code = 2) as organizational_updates
    FROM {npi_DBTable}
    WHERE last_update_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY DATE_TRUNC('month', last_update_date)
    ORDER BY update_month DESC;
    """
    
    # ========================================
    # PHASE 3: Individual record analysis
    # ========================================
    
    sql['06_individual_records_summary'] = f"""
    SELECT 
        'Individual Records Summary' as analysis_type,
        COUNT(*) as total_individual_records,
        COUNT(*) FILTER (WHERE last_name != '') as records_with_last_name,
        COUNT(*) FILTER (WHERE first_name != '') as records_with_first_name,
        COUNT(*) FILTER (WHERE middle_name != '') as records_with_middle_name,
        COUNT(*) FILTER (WHERE name_prefix != '') as records_with_prefix,
        COUNT(*) FILTER (WHERE name_suffix != '') as records_with_suffix,
        COUNT(*) FILTER (WHERE email_address IS NOT NULL) as records_with_email,
        COUNT(*) FILTER (WHERE SSN IS NOT NULL) as records_with_ssn,
        ROUND(COUNT(*) FILTER (WHERE middle_name != '')::DECIMAL / COUNT(*) * 100, 2) as middle_name_percentage
    FROM {individual_DBTable};
    """
    
    sql['07_individual_npi_relationships'] = f"""
    SELECT 
        'Individual-NPI Relationship Analysis' as analysis_type,
        COUNT(*) as total_relationships,
        COUNT(*) FILTER (WHERE is_sole_proprietor = TRUE) as sole_proprietor_count,
        COUNT(DISTINCT individual_id) as unique_individuals_with_npis,
        COUNT(DISTINCT npi_id) as unique_npis_with_individuals,
        ROUND(COUNT(*) FILTER (WHERE is_sole_proprietor = TRUE)::DECIMAL / COUNT(*) * 100, 2) as sole_proprietor_percentage
    FROM {npi_to_individual_DBTable};
    """
    
    
    # ========================================
    # PHASE 4: Organizational hierarchy analysis
    # ========================================
    
    sql['09_organizational_hierarchy_summary'] = f"""
    SELECT 
        'Organizational Hierarchy Summary' as analysis_type,
        COUNT(*) as total_organizational_npis,
        COUNT(*) FILTER (WHERE parent_npi_id IS NOT NULL) as npis_with_parents,
        COUNT(*) FILTER (WHERE parent_npi_id IS NULL) as npis_without_parents,
        COUNT(DISTINCT parent_npi_id) as unique_parent_organizations,
        COUNT(DISTINCT primary_authorized_official_individual_id) as unique_authorized_officials,
        ROUND(COUNT(*) FILTER (WHERE parent_npi_id IS NOT NULL)::DECIMAL / COUNT(*) * 100, 2) as subpart_percentage
    FROM {npi_to_clinical_org_DBTable};
    """
    
    sql['10_parent_organization_analysis'] = f"""
    SELECT 
        'Parent Organization Analysis' as analysis_type,
        parent_npi,
        COUNT(*) as child_count,
        RANK() OVER (ORDER BY COUNT(*) DESC) as parent_rank
    FROM (
        SELECT parent_npi_id as parent_npi
        FROM {npi_to_clinical_org_DBTable}
        WHERE parent_npi_id IS NOT NULL
    ) subparts
    GROUP BY parent_npi
    ORDER BY child_count DESC
    LIMIT 20;
    """
    
    sql['11_authorized_official_analysis'] = f"""
    SELECT 
        'Authorized Official Analysis' as analysis_type,
        individual_id,
        organization_count,
        RANK() OVER (ORDER BY organization_count DESC) as official_rank
    FROM (
        SELECT 
            primary_authorized_official_individual_id as individual_id,
            COUNT(*) as organization_count
        FROM {npi_to_clinical_org_DBTable}
        WHERE primary_authorized_official_individual_id IS NOT NULL
        GROUP BY primary_authorized_official_individual_id
    ) officials
    ORDER BY organization_count DESC
    LIMIT 20;
    """
    
    # ========================================
    # PHASE 5: Change pattern analysis
    # ========================================
    
    sql['12_change_type_distribution'] = f"""
    SELECT 
        'Change Type Distribution (Latest Run)' as analysis_type,
        change_type,
        COUNT(*) as change_count,
        ROUND(COUNT(*)::DECIMAL / SUM(COUNT(*)) OVER () * 100, 2) as percentage
    FROM {npi_change_log_DBTable} ncl
    JOIN (
        SELECT id FROM {processing_run_DBTable} 
        WHERE processing_status = 'COMPLETED' 
        ORDER BY run_date DESC LIMIT 1
    ) latest_run ON ncl.processing_run_id = latest_run.id
    GROUP BY change_type
    ORDER BY change_count DESC;
    """
    
    sql['13_individual_change_analysis'] = f"""
    SELECT 
        'Individual Change Analysis (Latest Run)' as analysis_type,
        change_type,
        COUNT(*) as change_count,
        COUNT(DISTINCT individual_id) as unique_individuals_changed,
        COUNT(DISTINCT npi) as unique_npis_affected
    FROM {individual_change_log_DBTable} icl
    JOIN (
        SELECT id FROM {processing_run_DBTable} 
        WHERE processing_status = 'COMPLETED' 
        ORDER BY run_date DESC LIMIT 1
    ) latest_run ON icl.processing_run_id = latest_run.id
    GROUP BY change_type
    ORDER BY change_count DESC;
    """
    
    sql['14_parent_relationship_changes'] = f"""
    SELECT 
        'Parent Relationship Changes (Latest Run)' as analysis_type,
        change_type,
        COUNT(*) as change_count,
        COUNT(DISTINCT child_npi) as unique_children_affected,
        COUNT(DISTINCT old_parent_npi) as unique_old_parents,
        COUNT(DISTINCT new_parent_npi) as unique_new_parents
    FROM {parent_change_log_DBTable} pcl
    JOIN (
        SELECT id FROM {processing_run_DBTable} 
        WHERE processing_status = 'COMPLETED' 
        ORDER BY run_date DESC LIMIT 1
    ) latest_run ON pcl.processing_run_id = latest_run.id
    GROUP BY change_type
    ORDER BY change_count DESC;
    """
    
    # ========================================
    # PHASE 6: Error analysis and data quality
    # ========================================
    
    sql['15_error_summary'] = f"""
    SELECT 
        'Error Summary' as analysis_type,
        error_type_string,
        COUNT(*) as error_count,
        ROUND(COUNT(*)::DECIMAL / SUM(COUNT(*)) OVER () * 100, 2) as error_percentage
    FROM {wrongnpi_DBTable}
    GROUP BY error_type_string
    ORDER BY error_count DESC;
    """
    
    sql['16_data_completeness_check'] = f"""
    SELECT 
        'Data Completeness Check' as analysis_type,
        'NPI Records' as table_name,
        COUNT(*) as total_records,
        COUNT(*) FILTER (WHERE npi IS NOT NULL) as npi_not_null,
        COUNT(*) FILTER (WHERE entity_type_code IS NOT NULL) as entity_type_not_null,
        COUNT(*) FILTER (WHERE enumeration_date IS NOT NULL) as enumeration_date_not_null,
        COUNT(*) FILTER (WHERE last_update_date IS NOT NULL) as last_update_not_null,
        ROUND(COUNT(*) FILTER (WHERE npi IS NOT NULL)::DECIMAL / COUNT(*) * 100, 2) as npi_completeness_pct
    FROM {npi_DBTable}
    
    UNION ALL
    
    SELECT 
        'Data Completeness Check' as analysis_type,
        'Individual Records' as table_name,
        COUNT(*) as total_records,
        COUNT(*) FILTER (WHERE last_name != '') as last_name_not_empty,
        COUNT(*) FILTER (WHERE first_name != '') as first_name_not_empty,
        NULL as enumeration_date_not_null,
        NULL as last_update_not_null,
        ROUND(COUNT(*) FILTER (WHERE last_name != '' AND first_name != '')::DECIMAL / COUNT(*) * 100, 2) as name_completeness_pct
    FROM {individual_DBTable};
    """
    
    sql['17_data_integrity_checks'] = f"""
    SELECT 
        'Data Integrity Checks' as analysis_type,
        'Orphaned NPI-Individual Links' as check_type,
        COUNT(*) as issue_count
    FROM {npi_to_individual_DBTable} nti
    LEFT JOIN {npi_DBTable} n ON nti.npi_id = n.id
    LEFT JOIN {individual_DBTable} i ON nti.individual_id = i.id
    WHERE n.id IS NULL OR i.id IS NULL
    
    UNION ALL
    
    SELECT 
        'Data Integrity Checks' as analysis_type,
        'Orphaned NPI-ClinicalOrg Links' as check_type,
        COUNT(*) as issue_count
    FROM {npi_to_clinical_org_DBTable} nco
    LEFT JOIN {npi_DBTable} n ON nco.npi_id = n.npi
    WHERE n.id IS NULL
    
    UNION ALL
    
    SELECT 
        'Data Integrity Checks' as analysis_type,
        'Invalid Parent References' as check_type,
        COUNT(*) as issue_count
    FROM {npi_to_clinical_org_DBTable} nco
    LEFT JOIN {npi_DBTable} parent ON nco.parent_npi_id = parent.npi
    WHERE nco.parent_npi_id IS NOT NULL AND parent.id IS NULL;
    """
    
    # ========================================
    # PHASE 7: Performance and completeness metrics
    # ========================================
    
    sql['18_source_vs_processed_comparison'] = f"""
    SELECT 
        'Source vs Processed Comparison' as analysis_type,
        source_stats.total_source_npis,
        processed_stats.total_processed_npis,
        source_stats.source_individuals,
        processed_stats.processed_individuals,
        source_stats.source_organizations,
        processed_stats.processed_organizations,
        ROUND(processed_stats.total_processed_npis::DECIMAL / source_stats.total_source_npis * 100, 2) as processing_completeness_pct
    FROM (
        SELECT 
            COUNT(*) as total_source_npis,
            COUNT(*) FILTER (WHERE "Entity_Type_Code" = '1') as source_individuals,
            COUNT(*) FILTER (WHERE "Entity_Type_Code" = '2') as source_organizations
        FROM {source_DBTable}
        WHERE "NPI" IS NOT NULL
    ) source_stats
    CROSS JOIN (
        SELECT 
            COUNT(*) as total_processed_npis,
            COUNT(*) FILTER (WHERE entity_type_code = 1) as processed_individuals,
            COUNT(*) FILTER (WHERE entity_type_code = 2) as processed_organizations
        FROM {npi_DBTable}
    ) processed_stats;
    """
    
    sql['19_relationship_coverage_analysis'] = f"""
    SELECT 
        'Relationship Coverage Analysis' as analysis_type,
        npi_stats.total_npis,
        npi_stats.individual_npis,
        npi_stats.organizational_npis,
        individual_links.individual_links_count,
        org_links.org_links_count,
        ROUND(individual_links.individual_links_count::DECIMAL / npi_stats.individual_npis * 100, 2) as individual_link_coverage_pct,
        ROUND(org_links.org_links_count::DECIMAL / npi_stats.organizational_npis * 100, 2) as org_link_coverage_pct
    FROM (
        SELECT 
            COUNT(*) as total_npis,
            COUNT(*) FILTER (WHERE entity_type_code = 1) as individual_npis,
            COUNT(*) FILTER (WHERE entity_type_code = 2) as organizational_npis
        FROM {npi_DBTable}
    ) npi_stats
    CROSS JOIN (
        SELECT COUNT(*) as individual_links_count FROM {npi_to_individual_DBTable}
    ) individual_links
    CROSS JOIN (
        SELECT COUNT(*) as org_links_count FROM {npi_to_clinical_org_DBTable}
    ) org_links;
    """
    
    sql['20_processing_efficiency_metrics'] = f"""
    SELECT 
        'Processing Efficiency Metrics' as analysis_type,
        pr.run_date,
        pr.total_npis_processed,
        EXTRACT(EPOCH FROM (pr.completion_date - pr.run_date)) as processing_time_seconds,
        ROUND(pr.total_npis_processed::DECIMAL / EXTRACT(EPOCH FROM (pr.completion_date - pr.run_date)) * 60, 2) as npis_per_minute,
        error_stats.total_errors,
        ROUND(error_stats.total_errors::DECIMAL / pr.total_npis_processed * 100, 4) as error_rate_pct
    FROM {processing_run_DBTable} pr
    CROSS JOIN (
        SELECT COUNT(*) as total_errors FROM {wrongnpi_DBTable}
    ) error_stats
    WHERE pr.processing_status = 'COMPLETED'
    ORDER BY pr.run_date DESC
    LIMIT 5;
    """
    
    # Execute SQL pipeline
    print("About to run Core NPI Data Analysis and Quality Checks")
    print("=" * 60)
    print("This comprehensive analysis will cover:")
    print("1. Processing run summary and trends")
    print("2. NPI distribution and enumeration analysis")
    print("3. Individual record analysis and demographics")
    print("4. Organizational hierarchy and relationships")
    print("5. Change pattern analysis and trends")
    print("6. Error analysis and data quality checks")
    print("7. Performance metrics and completeness analysis")
    print("=" * 60)
    print("Key Features:")
    print("- Comprehensive data quality validation")
    print("- Change trend analysis")
    print("- Performance and efficiency metrics")
    print("- Data integrity checks")
    print("- Source vs processed comparison")
    print("=" * 60)
    
    SQLoopcicle.run_sql_loop(
        sql_dict=sql,
        is_just_print=is_just_print,
        engine=alchemy_engine
    )
    
    print("\n" + "=" * 60)
    print("✅ Core NPI Data Analysis completed!")
    print("Review the results above for:")
    print("- Data quality issues that need attention")
    print("- Processing efficiency opportunities")
    print("- Change patterns and trends")
    print("- Completeness and integrity metrics")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Core NPI Data Analysis failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        print("\nAlso ensure Step15 and Step20 have been run successfully first.")
        raise
