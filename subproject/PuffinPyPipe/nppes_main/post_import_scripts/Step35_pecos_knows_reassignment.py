#!/usr/bin/env python3
"""
Step35_pecos_knows_reassignment.py

This script processes PECOS reassignment data to populate the ndh.assigning_npi table.
The reassignment data maps PECOS organizations that are assigning benefits to NPIs that are receiving them.

The process:
1. Drop and recreate the ndh.assigning_npi table
2. Map reassignment relationships from PECOS data to NDH structure
3. Use INNER JOINs to ensure underlying data exists in target tables

Data Flow:
- pecos_reassignment.reasgn_bnft_enrlmt_id -> ClinicalOrganization_id (via PECOS VTIN)
- pecos_reassignment.rcv_bnft_enrlmt_id -> npi_id (via pecos_enrollment.npi)
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle, InLaw  # type: ignore
import pandas as pd
import sqlalchemy
from pathlib import Path
import os

class Step35PecosKnowsReassignment:
    
    @staticmethod
    def main():
        is_just_print = False  # Start with dry-run mode
        
        print("Connecting to DB")
        base_path = os.path.dirname(os.path.abspath(__file__))
        env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
        alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
        
        # Define table references using PlainerFlow DBTable pattern
        pecos_reassignment_DBTable = DBTable(schema='pecos_raw', table='pecos_reassignment')
        pecos_enrollment_DBTable = DBTable(schema='pecos_raw', table='pecos_enrollment')
        clinical_org_DBTable = DBTable(schema='ndh', table='clinical_organization')
        assigning_npi_DBTable = DBTable(schema='ndh', table='assigning_npi')
        assign_expanded_DBTable = DBTable(schema='intake',table='pecos_assign_expanded')
        pac_list_DBTable = DBTable(schema='intake',table='pecos_pac_list')
        pac_count_DBTable = DBTable(schema='intake',table='pecos_pac_count')
        pac_to_onpi_DBTABLE = DBTable(schema='intake', table='pac_to_npi')

        sql = FrostDict()
        
        # Phase 1: Drop and recreate the assigning_npi table
        sql['drop_assigning_npi_table'] = f"""
        DROP TABLE IF EXISTS {assigning_npi_DBTable};
        """
        
        sql['create_assigning_npi_table'] = f"""
        CREATE TABLE {assigning_npi_DBTable} (
            clinical_organization_id INT NOT NULL,
            npi_id BIGINT NOT NULL
        );
        """
        
        pecos_vtin_prefix = 'PECOS_'

        # We do this one so that we can see how the assignment relationships actually look... 

        sql['drop the pecos expanded'] = f"DROP TABLE IF EXISTS {assign_expanded_DBTable}"

        sql['create the expanded pecos'] = f"""
        CREATE TABLE {assign_expanded_DBTable} AS 
        SELECT
            
            assigning_enrollment.npi AS assigning_npi,
            assigning_enrollment.provider_type_desc AS assigning_provider_type,
            COALESCE(assigning_enrollment.org_name, CONCAT(assigning_enrollment.last_name, ' ', assigning_enrollment.first_name)) AS assigning_provider_name,
            CASE WHEN assigning_enrollment.org_name IS NULL THEN 'individual' ELSE 'organization' END AS assigning_npi_type,
            reasgn_bnft_enrlmt_id,
            assigning_enrollment.pecos_asct_cntl_id  AS assigning_pac_id,
            receiving_enrollment.npi AS receiving_npi,
            receiving_enrollment.provider_type_desc AS receiving_provider_type,
            COALESCE(receiving_enrollment.org_name, CONCAT(receiving_enrollment.last_name, ' ', receiving_enrollment.first_name)) AS receiving_provider_name,
            receiving_enrollment.pecos_asct_cntl_id  AS receiving_pac_id,
            CASE WHEN receiving_enrollment.org_name IS NULL THEN 'individual' ELSE 'organization' END AS receiving_npi_type,
            rcv_bnft_enrlmt_id
        FROM {pecos_reassignment_DBTable} AS reassignment
        INNER JOIN {pecos_enrollment_DBTable} AS assigning_enrollment ON
            reassignment.reasgn_bnft_enrlmt_id = assigning_enrollment.enrlmt_id
        INNER JOIN {pecos_enrollment_DBTable} AS receiving_enrollment ON
            reassignment.rcv_bnft_enrlmt_id = receiving_enrollment.enrlmt_id

        """

        sql['indexing expanded pecos'] = f"""
        
            CREATE INDEX index_assign_npi ON {assign_expanded_DBTable} (assigning_npi);
            CREATE INDEX index_assigning_provider_name ON {assign_expanded_DBTable} (assigning_provider_name);
            CREATE INDEX index_assigning_bnft_enrlmt_id ON {assign_expanded_DBTable} (reasgn_bnft_enrlmt_id);
            CREATE INDEX index_assigning_pac_id ON {assign_expanded_DBTable} (assigning_pac_id);
            
            CREATE INDEX index_receiving_npi ON {assign_expanded_DBTable} (assigning_npi);
            CREATE INDEX index_receiving_provider_name ON {assign_expanded_DBTable} (receiving_provider_name);
            CREATE INDEX index_receiving_enrlmt_id ON {assign_expanded_DBTable} (rcv_bnft_enrlmt_id);
            CREATE INDEX index_receiving_pac_id ON {assign_expanded_DBTable} (receiving_pac_id);
        """

        sql['drop paclist'] = f"DROP TABLE IF EXISTS {pac_list_DBTable}"

        # Note that a given PAC ID can potentially have multiple PACIDs since apparently sharing a PACID is one form (at least) of "reassignment"
        # TODO the InLaw test on this one should be the verify that the enrollment_count is always equal or greater than the npi_count.

        sql['create paclist'] = f"""
            CREATE TABLE {pac_list_DBTable} AS 
            SELECT pecos_asct_cntl_id AS pac_id,
                COALESCE(org_name,CONCAT(last_name, ' ', first_name)) AS org_indv_group,
                COUNT(DISTINCT(enrlmt_id)) AS enrollment_count,
                COUNT(DISTINCT(npi)) AS npi_count
            FROM {pecos_enrollment_DBTable}
            GROUP BY pecos_asct_cntl_id, COALESCE(org_name,CONCAT(last_name, ' ', first_name))
            ORDER BY COUNT(DISTINCT(enrlmt_id)) DESC
        """

        sql['index pac id'] = f"""
            CREATE INDEX index_pac_list_pac_id ON {pac_list_DBTable} (pac_id);
        """

        sql['drop pac count'] = f"DROP TABLE IF EXISTS {pac_count_DBTable}"


        # TODO, this one should become a check. There should be no data in this table given this HAVING statement. 
        # We want to be able to see when it is more than a single org and a group of individuals.. so a org_indv_group of at least three values. 
        sql['create pac count'] = f"""
            CREATE TABLE {pac_count_DBTable} AS 
            SELECT 
                pac_id,
                COUNT(DISTINCT(org_indv_group)) AS cnt_org_indv_group
            FROM {pac_list_DBTable} AS pac_list
            GROUP BY pac_id
            HAVING COUNT(DISTINCT(org_indv_group)) > 1
        """

        sql['drop the pac to npi table'] = f"""
            DROP TABLE IF EXISTS {pac_to_onpi_DBTABLE}
        """

        sql['create the pac to npi table'] = f"""
            CREATE TABLE {pac_to_onpi_DBTABLE} AS 
            SELECT DISTINCT
                pecos_asct_cntl_id AS pac_id,
                COALESCE(org_name, CONCAT(last_name, ' ', first_name)) AS provider_name,
                npi
            FROM {pecos_enrollment_DBTable}
        """


        # Phase 2: Populate the assigning_npi table with reassignment data
        sql['populate_assigning_npi'] = f"""
        INSERT INTO {assigning_npi_DBTable} (
            clinical_organization_id,
            npi_id
        )
        SELECT DISTINCT
            clinical_org.id AS clinical_organization_id, 
            assigning_enrollment.npi AS npi_id
        FROM {pecos_reassignment_DBTable} AS reassignment
        INNER JOIN {pecos_enrollment_DBTable} AS assigning_enrollment ON
            reassignment.reasgn_bnft_enrlmt_id = assigning_enrollment.enrlmt_id
        INNER JOIN {pecos_enrollment_DBTable} AS receiving_enrollment ON
            reassignment.rcv_bnft_enrlmt_id = receiving_enrollment.enrlmt_id
        INNER JOIN {clinical_org_DBTable} AS clinical_org ON
            clinical_org.organization_vtin = CONCAT('{pecos_vtin_prefix}',receiving_enrollment.pecos_asct_cntl_id);
        """
        
        # Phase 3: Create indexes for performance
        sql['create_assigning_npi_org_index'] = f"""
        CREATE INDEX IF NOT EXISTS idx_assigning_npi_org_id 
        ON {assigning_npi_DBTable}(clinical_organization_id);
        """
        
        sql['create_assigning_npi_npi_index'] = f"""
        CREATE INDEX IF NOT EXISTS idx_assigning_npi_npi_id 
        ON {assigning_npi_DBTable}(npi_id);
        """
        
        # Phase 4: Create compound index for unique lookups
        sql['create_assigning_npi_compound_index'] = f"""
        CREATE INDEX IF NOT EXISTS idx_assigning_npi_compound 
        ON {assigning_npi_DBTable}(clinical_organization_id, npi_id);
        """
        
        print("About to run SQL")
        SQLoopcicle.run_sql_loop(
            sql_dict=sql,
            is_just_print=is_just_print,
            engine=alchemy_engine
        )
        
        # Run InLaw validation tests
        print("🔍 Running InLaw validation tests...")
        InLaw.run_all(engine=alchemy_engine)
        
        print("✅ Successfully processed PECOS reassignment data into ndh.assigning_npi table")


class ValidateRowCountRelationship(InLaw):
    title = "NDH assigning_npi should be approximately 6% of PECOS reassignment rows (distinct pairs)"
    
    @staticmethod
    def run(engine):
        # Calculate ratio of distinct pairs to total PECOS reassignment rows
        sql = """
        WITH table_counts AS (
            SELECT 
                (SELECT COUNT(*) FROM pecos_raw.pecos_reassignment) AS pecos_count,
                (SELECT COUNT(*) FROM ndh.assigning_npi) AS ndh_count
        )
        SELECT 
            pecos_count,
            ndh_count,
            CASE 
                WHEN pecos_count = 0 THEN 0.0
                ELSE (ndh_count * 100.0 / pecos_count)
            END AS ndh_to_pecos_ratio
        FROM table_counts;
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Validate ratio is approximately 6% (allow range 5% to 7%)
        result = gx_df.expect_column_values_to_be_between(
            column="ndh_to_pecos_ratio",
            min_value=5.0,
            max_value=7.0
        )
        
        if result.success:
            return True
        
        # Get actual values for error message
        row = gx_df.head(1)
        pecos_count = row.iloc[0]['pecos_count']
        ndh_count = row.iloc[0]['ndh_count']
        ratio = row.iloc[0]['ndh_to_pecos_ratio']
        
        return (f"NDH assigning_npi ratio ({ratio:.2f}%) is outside expected 5-7% range. "
                f"PECOS reassignment: {pecos_count:,}, NDH assigning_npi: {ndh_count:,}")


class ValidateAssigningNpiNotEmpty(InLaw):
    title = "NDH assigning_npi table should not be empty"
    
    @staticmethod
    def run(engine):
        sql = "SELECT COUNT(*) AS row_count FROM ndh.assigning_npi;"
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect at least 1 row
        result = gx_df.expect_column_values_to_be_between(
            column="row_count",
            min_value=1,
            max_value=None
        )
        
        if result.success:
            return True
        
        return "NDH assigning_npi table is empty - no reassignment data was processed"


class ValidateNoDuplicateAssignments(InLaw):
    title = "NDH assigning_npi should not have duplicate organization-npi pairs"
    
    @staticmethod
    def run(engine):
        sql = """
        SELECT COUNT(*) AS duplicate_count
        FROM (
            SELECT clinical_organization_id, npi_id, COUNT(*) AS cnt
            FROM ndh.assigning_npi
            GROUP BY clinical_organization_id, npi_id
            HAVING COUNT(*) > 1
        ) AS duplicates;
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect exactly 0 duplicates
        result = gx_df.expect_column_values_to_be_between(
            column="duplicate_count",
            min_value=0,
            max_value=0
        )
        
        if result.success:
            return True
        
        return "Found duplicate organization-npi pairs in NDH assigning_npi table"


class ValidateAssigningNpiRowCountExpected(InLaw):
    title = "NDH assigning_npi row count should be within 1% of expected 227000"
    
    @staticmethod
    def run(engine):
        sql = "SELECT COUNT(*) AS row_count FROM ndh.assigning_npi;"
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expected count: 227000 (distinct pairs)
        # 1% tolerance: 2270
        # Range: 224730 to 229270
        result = gx_df.expect_column_values_to_be_between(
            column="row_count",
            min_value=224730,
            max_value=229270
        )
        
        if result.success:
            return True
        
        # Get actual count for error message
        actual_count = gx_df.head(1).iloc[0]['row_count']
        expected_count = 227000
        percentage_diff = abs(actual_count - expected_count) / expected_count * 100
        
        return (f"Row count ({actual_count:,}) is outside 1% tolerance of expected {expected_count:,}. "
                f"Difference: {percentage_diff:.2f}%")

def main():
    try:
        Step35PecosKnowsReassignment.main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        raise

if __name__ == "__main__":
    main()
