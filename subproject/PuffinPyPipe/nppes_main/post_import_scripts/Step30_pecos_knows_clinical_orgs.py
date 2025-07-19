#!/usr/bin/env python3
"""
Step30_pecos_knows_clinical_orgs.py

This script uses the raw PECOS data, in combination with the NPPES data processed in previous steps
to populate ClinicalOrganization and link them to organizational NPIs in npi_to_clinicalorganization.

The process:
1. Create staging table PAC_to_NPPES_org_names from PECOS + NPPES data
2. Populate ClinicalOrganization table with PECOS organizations
3. Add organization name type LUT entries
4. Populate Orgname table with all organization names
5. Create Individual records for authorized officials
6. Create NPI to ClinicalOrganization links
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle  # type: ignore
import pandas as pd
import sqlalchemy
from pathlib import Path
import os

def main():
    is_just_print = False  # Start with dry-run mode
    

    pecos_vtin_prefix = 'PECOS_'

    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    # Define table references using PlainerFlow DBTable pattern
    pecos_enrollment_DBTable = DBTable(schema='pecos_raw', table='pecos_enrollment')
    nppes_main_DBTable = DBTable(schema='nppes_raw', table='main_file')
    nppes_othername_DBTable = DBTable(schema='nppes_raw', table='othername_file')
    nppes_endpoint_DBTable = DBTable(schema='nppes_raw', table='endpoint_file')
    
    # Target tables in NDH schema
    clinical_org_DBTable = DBTable(schema='ndh', table='clinical_organization')
    orgname_type_DBTable = DBTable(schema='ndh', table='clinical_orgname_type')
    orgname_DBTable = DBTable(schema='ndh', table='orgname')
    individual_DBTable = DBTable(schema='ndh', table='individual')
    npi_to_clinical_org_DBTable = DBTable(schema='ndh', table='organizational_npi')
    
    # Staging table
    staging_table_DBTable = DBTable(schema='intake', table='PAC_to_NPPES_org_names')
    
    sql = FrostDict()
    
    # Phase 1: Create staging table with organization names from PECOS + NPPES
    sql['drop_staging_table_if_exists'] = f"""
    DROP TABLE IF EXISTS {staging_table_DBTable};
    """
    
    sql['create_staging_table_from_main_file'] = f"""
    CREATE TABLE {staging_table_DBTable} AS
    SELECT
        pecos_enrollment.pecos_asct_cntl_id,
        'nppes_main_file' AS data_source,
        MAX(pecos_enrollment.org_name) AS one_org_name,
        COUNT(DISTINCT(pecos_enrollment.npi)) AS pecos_npi_count,
        nppes_main."Provider_Organization_Name_Legal_Business_Name" AS organization_name
    FROM {pecos_enrollment_DBTable} AS pecos_enrollment
    LEFT JOIN {nppes_main_DBTable} AS nppes_main ON
        nppes_main."NPI" = pecos_enrollment.npi
    WHERE pecos_enrollment.org_name IS NOT NULL
    GROUP BY pecos_enrollment.pecos_asct_cntl_id, nppes_main."Provider_Organization_Name_Legal_Business_Name"
    ORDER BY pecos_npi_count DESC;
    """
    
    sql['insert_staging_from_othername_file'] = f"""
    INSERT INTO {staging_table_DBTable}
    SELECT
        pecos_enrollment.pecos_asct_cntl_id,
        'nppes_othername_file' AS data_source,
        MAX(pecos_enrollment.org_name) AS one_org_name,
        COUNT(DISTINCT(pecos_enrollment.npi)) AS pecos_npi_count,
        nppes_othername.provider_other_organization_name AS organization_name
    FROM {pecos_enrollment_DBTable} AS pecos_enrollment
    LEFT JOIN {nppes_othername_DBTable} AS nppes_othername ON
        nppes_othername.npi = pecos_enrollment.npi
    WHERE pecos_enrollment.org_name IS NOT NULL
    GROUP BY pecos_enrollment.pecos_asct_cntl_id, nppes_othername.provider_other_organization_name
    ORDER BY pecos_npi_count DESC;
    """
    
    sql['insert_staging_from_endpoint_file'] = f"""
    INSERT INTO {staging_table_DBTable}
    SELECT
        pecos_enrollment.pecos_asct_cntl_id,
        'nppes_endpoint_file' AS data_source,
        MAX(pecos_enrollment.org_name) AS one_org_name,
        COUNT(DISTINCT(pecos_enrollment.npi)) AS pecos_npi_count,
        nppes_endpoint.affiliation_legal_business_name AS organization_name
    FROM {pecos_enrollment_DBTable} AS pecos_enrollment
    LEFT JOIN {nppes_endpoint_DBTable} AS nppes_endpoint ON
        nppes_endpoint.npi = pecos_enrollment.npi
    WHERE pecos_enrollment.org_name IS NOT NULL
    AND nppes_endpoint.affiliation_legal_business_name != '' 
    AND nppes_endpoint.affiliation_legal_business_name IS NOT NULL
    GROUP BY pecos_enrollment.pecos_asct_cntl_id, nppes_endpoint.affiliation_legal_business_name
    ORDER BY pecos_npi_count DESC;
    """
    # the simplest case last.
    sql['insert_staging_from_pecos_enrollment'] = f"""
    INSERT INTO {staging_table_DBTable}
    SELECT
        pecos_enrollment.pecos_asct_cntl_id,
        'pecos_enrollment' AS data_source,
        MAX(pecos_enrollment.org_name) AS one_org_name,
        COUNT(DISTINCT(pecos_enrollment.npi)) AS pecos_npi_count,
        MAX(pecos_enrollment.org_name) AS organization_name
    FROM {pecos_enrollment_DBTable} AS pecos_enrollment
    WHERE pecos_enrollment.org_name IS NOT NULL
    GROUP BY pecos_asct_cntl_id
    ORDER BY pecos_npi_count DESC;
    """



    # Phase 2: Add required unique constraints for INSERT ON CONFLICT
    sql['add_individual_unique_constraint'] = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.table_constraints 
            WHERE constraint_name = 'uc_individual_name_components' 
            AND table_name = 'individual'
            AND table_schema = 'ndh'
        ) THEN
            ALTER TABLE {individual_DBTable}
            ADD CONSTRAINT uc_individual_name_components 
            UNIQUE (last_name, first_name, middle_name, name_prefix, name_suffix);
        END IF;
    END $$;
    """
    
    sql['add_orgname_unique_constraint'] = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.table_constraints 
            WHERE constraint_name = 'uc_orgname_combination' 
            AND table_name = 'orgname'
            AND table_schema = 'ndh'
        ) THEN
            ALTER TABLE {orgname_DBTable}
            ADD CONSTRAINT uc_orgname_combination 
            UNIQUE (ClinicalOrganization_id, ClinicalOrganization_name, ClinicalOrgnameType_id);
        END IF;
    END $$;
    """
    
    # Phase 3: Add organization name type LUT entries
    sql['insert_pecos_orgname_type'] = f"""
    INSERT INTO {orgname_type_DBTable} (orgname_type_description, source_file, source_field)
    VALUES ('PECOS', 'pecos_enrollment', 'org_name')
    ON CONFLICT (orgname_type_description) DO NOTHING;
    """
    
    sql['insert_nppes_main_orgname_type'] = f"""
    INSERT INTO {orgname_type_DBTable} (orgname_type_description, source_file, source_field)
    VALUES ('NPPES_main_file', 'main_file', 'Provider_Organization_Name_Legal_Business_Name')
    ON CONFLICT (orgname_type_description) DO NOTHING;
    """
    
    sql['insert_nppes_othername_orgname_type'] = f"""
    INSERT INTO {orgname_type_DBTable} (orgname_type_description, source_file, source_field)
    VALUES ('NPPES_othername_file', 'othername_file', 'provider_other_organization_name')
    ON CONFLICT (orgname_type_description) DO NOTHING;
    """
    
    sql['insert_nppes_endpoint_orgname_type'] = f"""
    INSERT INTO {orgname_type_DBTable} (orgname_type_description, source_file, source_field)
    VALUES ('NPPES_endpoint_file', 'endpoint_file', 'affiliation_legal_business_name')
    ON CONFLICT (orgname_type_description) DO NOTHING;
    """
    
    # Phase 4: Populate ClinicalOrganization table
    sql['populate_clinical_organizations'] = f"""
    INSERT INTO {clinical_org_DBTable} (
        clinical_organization_legal_name,
        authorized_official_individual_id,
        organization_tin,
        organization_vtin,
        organization_glief
    )
    SELECT DISTINCT
        staging.one_org_name,
        0 AS authorized_official_individual_id,
        NULL AS organization_tin,
        '{pecos_vtin_prefix}' || staging.pecos_asct_cntl_id AS organization_vtin,
        NULL AS organization_glief
    FROM {staging_table_DBTable} AS staging
    WHERE staging.one_org_name IS NOT NULL
    ON CONFLICT (organization_vtin) DO NOTHING;
    """
    
    # Phase 5: Populate Orgname table with PECOS names
    sql['populate_orgnames_pecos'] = f"""
    INSERT INTO {orgname_DBTable} (
        clinical_organization_id,
        clinical_organization_name,
        clinical_orgname_type_id
    )
    SELECT DISTINCT
        clinical_org.id,
        staging.one_org_name,
        orgname_type.id
    FROM {staging_table_DBTable} AS staging
    JOIN {clinical_org_DBTable} AS clinical_org ON
        clinical_org.organization_vtin = '{pecos_vtin_prefix}' || staging.pecos_asct_cntl_id
    JOIN {orgname_type_DBTable} AS orgname_type ON
        orgname_type.orgname_type_description = 'PECOS'
    WHERE staging.one_org_name IS NOT NULL
    ON CONFLICT (clinical_organization_id, clinical_organization_name, clinical_orgname_type_id) DO NOTHING;
    """
    
    # Phase 6: Populate Orgname table with NPPES names
    sql['populate_orgnames_nppes'] = f"""
    INSERT INTO {orgname_DBTable} (
        clinical_organization_id,
        clinical_organization_name,
        clinical_orgname_type_id
    )
    SELECT DISTINCT
        clinical_org.id,
        staging.organization_name,
        orgname_type.id
    FROM {staging_table_DBTable} AS staging
    JOIN {clinical_org_DBTable} AS clinical_org ON
        clinical_org.organization_vtin = '{pecos_vtin_prefix}' || staging.pecos_asct_cntl_id
    JOIN {orgname_type_DBTable} AS orgname_type ON
        orgname_type.orgname_type_description = staging.data_source
    WHERE staging.organization_name IS NOT NULL
    AND staging.organization_name != ''
    ON CONFLICT (clinical_organization_id, clinical_organization_name, clinical_orgname_type_id) DO NOTHING;
    """
    
    # Phase 7: Create Individual records for authorized officials
    sql['populate_authorized_officials'] = f"""
    INSERT INTO {individual_DBTable} (
        last_name,
        first_name,
        middle_name,
        name_prefix,
        name_suffix,
        email_address,
        ssn
    )
    SELECT DISTINCT
        COALESCE(nppes_main."Authorized_Official_Last_Name", '') AS last_name,
        COALESCE(nppes_main."Authorized_Official_First_Name", '') AS first_name,
        COALESCE(nppes_main."Authorized_Official_Middle_Name", '') AS middle_name,
        COALESCE(nppes_main."Authorized_Official_Name_Prefix_Text", '') AS name_prefix,
        COALESCE(nppes_main."Authorized_Official_Name_Suffix_Text", '') AS name_suffix,
        NULL AS email_address,
        NULL AS ssn
    FROM {pecos_enrollment_DBTable} AS pecos_enrollment
    JOIN {nppes_main_DBTable} AS nppes_main ON
        nppes_main."NPI" = pecos_enrollment.npi
    WHERE pecos_enrollment.org_name IS NOT NULL
    AND nppes_main."Entity_Type_Code" = '2'
    ON CONFLICT (last_name, first_name, middle_name, name_prefix, name_suffix) DO NOTHING;
    """
    
    # Phase 8: Create Organizational NPI to ClinicalOrganization links
    # Note the "WHERE nppes_main."Entity_Type_Code" = '2'" this si ensuring 
    sql['add_organizational_npi_unique_constraint'] = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.table_constraints
            WHERE constraint_name = 'uc_organizational_npi_pair'
            AND table_name = 'organizational_npi'
            AND table_schema = 'ndh'
        ) THEN
            ALTER TABLE {npi_to_clinical_org_DBTable}
            ADD CONSTRAINT uc_organizational_npi_pair
            UNIQUE (npi_id, clinical_organization_id);
        END IF;
    END $$;
    """

    sql['populate_npi_to_clinical_organization'] = f"""
    INSERT INTO {npi_to_clinical_org_DBTable} (
        npi_id,
        clinical_organization_id,
        primary_authorized_official_individual_id,
        parent_npi_id
    )
    SELECT DISTINCT
        nppes_main."NPI" AS npi_id,
        clinical_org.id AS clinical_organization_id,
        0 AS primary_authorized_official_individual_id,
        0 AS parent_npi_id
    FROM {pecos_enrollment_DBTable} AS pecos_enrollment
    JOIN {nppes_main_DBTable} AS nppes_main ON
        nppes_main."NPI" = pecos_enrollment.npi
    JOIN {clinical_org_DBTable} AS clinical_org ON
        clinical_org.organization_vtin = '{pecos_vtin_prefix}' || pecos_enrollment.pecos_asct_cntl_id
    WHERE pecos_enrollment.org_name IS NOT NULL
    AND nppes_main."Entity_Type_Code" = '2'
    ON CONFLICT (npi_id, clinical_organization_id) DO NOTHING;
    """
    
    # Phase 9: Create indexes for performance
    sql['create_staging_table_indexes'] = f"""
    CREATE INDEX IF NOT EXISTS idx_pac_to_nppes_org_names_pecos_id 
    ON {staging_table_DBTable}(pecos_asct_cntl_id);
    """
    
    sql['create_staging_table_data_source_index'] = f"""
    CREATE INDEX IF NOT EXISTS idx_pac_to_nppes_org_names_data_source 
    ON {staging_table_DBTable}(data_source);
    """
    
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
