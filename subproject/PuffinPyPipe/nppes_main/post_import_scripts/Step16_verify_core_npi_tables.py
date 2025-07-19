#!/usr/bin/env python3
"""
--- Step16_verify_core_npi_tables.py ---------
This step handles all of the InLaw validation tests for Step15 using Great Expectations.
See AI_Instruction/PlainerflowTools.md for how to work with the InLaw framework.

The validations this performs:
* Verify that ndh.individual_npi only contains NPIs with entity_type_code = '1' (individuals)
* Verify that ndh.organizational_npi only contains NPIs with entity_type_code = '2' (organizations)
* Verify that no NPI appears in both relationship tables (mutually exclusive)
* Verify that entity_type_code in ndh.npi matches the original source data
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, InLaw  # type: ignore
import os

class VerifyIndividualNPIsOnly(InLaw):
    """
    Verify that ndh.individual_npi only contains NPIs with entity_type_code = '1' (individuals)
    """
    title = "individual_npi table should only contain Individual NPIs (entity_type_code = '1')"
    
    @staticmethod
    def run(engine):
        # Define source table - matches Step15 configuration
        npi_table = 'main_file_small'  # For testing
        #npi_table = 'main_file'  # For production
        source_DBTable = DBTable(schema='nppes_raw', table=npi_table)
        
        # Target tables
        npi_DBTable = DBTable(schema='ndh', table='npi')
        npi_to_individual_DBTable = DBTable(schema='ndh', table='individual_npi')
        
        # Count violations: NPIs in individual_npi that are NOT entity_type_code = 1
        sql = f"""
        SELECT COUNT(*) as violation_count
        FROM {npi_to_individual_DBTable} AS npi_to_individual
        JOIN {npi_DBTable} AS npi_table ON npi_to_individual.npi_id = npi_table.id
        WHERE npi_table.entity_type_code != 1
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect exactly 0 violations (using min=0, max=0 to check for equality)
        result = gx_df.expect_column_values_to_be_between(
            column="violation_count", 
            min_value=0,
            max_value=0
        )
        
        if result.success:
            return True
        return f"Found NPIs in NPI_to_Individual table with incorrect entity_type_code (should be 1 for individuals)"


class VerifyOrganizationNPIsOnly(InLaw):
    """
    Verify that ndh.organizational_npi only contains NPIs with entity_type_code = '2' (organizations)
    """
    title = "organizational_npi table should only contain Organization NPIs (entity_type_code = '2')"
    
    @staticmethod
    def run(engine):
        # Define source table - matches Step15 configuration
        npi_table = 'main_file_small'  # For testing
        #npi_table = 'main_file'  # For production
        source_DBTable = DBTable(schema='nppes_raw', table=npi_table)
        
        # Target tables
        npi_DBTable = DBTable(schema='ndh', table='npi')
        npi_to_clinical_org_DBTable = DBTable(schema='ndh', table='organizational_npi')
        
        # Count violations: NPIs in organizational_npi that are NOT entity_type_code = 2
        sql = f"""
        SELECT COUNT(*) as violation_count
        FROM {npi_to_clinical_org_DBTable} AS npi_to_clinical_org
        JOIN {npi_DBTable} AS npi_table ON npi_to_clinical_org.npi_id = npi_table.id
        WHERE npi_table.entity_type_code != 2
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect exactly 0 violations (using min=0, max=0 to check for equality)
        result = gx_df.expect_column_values_to_be_between(
            column="violation_count", 
            min_value=0,
            max_value=0
        )
        
        if result.success:
            return True
        return f"Found NPIs in NPI_to_ClinicalOrganization table with incorrect entity_type_code (should be 2 for organizations)"


class VerifyNoNPIInBothTables(InLaw):
    """
    Verify that no NPI appears in both relationship tables
    An NPI should be either Individual (type 1) or Organization (type 2), not both
    """
    title = "No NPI should appear in both individual_npi and organizational_npi tables"
    
    @staticmethod
    def run(engine):
        # Target tables
        npi_to_individual_DBTable = DBTable(schema='ndh', table='individual_npi')
        npi_to_clinical_org_DBTable = DBTable(schema='ndh', table='organizational_npi')
        
        # Count NPIs that appear in both tables
        sql = f"""
        SELECT COUNT(*) as duplicate_count
        FROM {npi_to_individual_DBTable} AS npi_to_individual
        JOIN {npi_to_clinical_org_DBTable} AS npi_to_clinical_org 
            ON npi_to_individual.npi_id = npi_to_clinical_org.npi_id
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect exactly 0 duplicates (using min=0, max=0 to check for equality)
        result = gx_df.expect_column_values_to_be_between(
            column="duplicate_count", 
            min_value=0,
            max_value=0
        )
        
        if result.success:
            return True
        return f"Found NPIs that appear in both relationship tables (should be mutually exclusive)"


class VerifyEntityTypeConsistency(InLaw):
    """
    Verify that entity_type_code in ndh.npi matches the original source data
    """
    title = "Entity type codes in ndh.npi should match source data from nppes_raw"
    
    @staticmethod
    def run(engine):
        # Define source table - matches Step15 configuration
        npi_table = 'main_file_small'  # For testing
        #npi_table = 'main_file'  # For production
        source_DBTable = DBTable(schema='nppes_raw', table=npi_table)
        
        # Target tables
        npi_DBTable = DBTable(schema='ndh', table='npi')
        
        # Count mismatches between NDH and source entity types
        sql = f"""
        SELECT COUNT(*) as mismatch_count
        FROM {npi_DBTable} AS npi_table
        JOIN {source_DBTable} AS source_table ON npi_table.npi = source_table."NPI"
        WHERE npi_table.entity_type_code::TEXT != source_table."Entity_Type_Code"
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect exactly 0 mismatches (using min=0, max=0 to check for equality)
        result = gx_df.expect_column_values_to_be_between(
            column="mismatch_count", 
            min_value=0,
            max_value=0
        )
        
        if result.success:
            return True
        return f"Found NPIs with inconsistent entity_type_code between NDH and source data"


class VerifyNPITableHasData(InLaw):
    """
    Verify that the NPI table has a reasonable number of records
    """
    title = "NPI table should contain a reasonable number of records"
    
    @staticmethod
    def run(engine):
        # Target table
        npi_DBTable = DBTable(schema='ndh', table='npi')
        
        # Count total records
        sql = f"""
        SELECT COUNT(*) as total_records
        FROM {npi_DBTable}
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect at least 1 record, but not more than 10 million (reasonable upper bound)
        result = gx_df.expect_column_values_to_be_between(
            column="total_records", 
            min_value=1, 
            max_value=10000000
        )
        
        if result.success:
            return True
        return f"NPI table record count is outside expected range (1 to 10,000,000)"


class VerifyRelationshipTablesHaveData(InLaw):
    """
    Verify that both relationship tables have records
    """
    title = "Both NPI relationship tables should contain records"
    
    @staticmethod
    def run(engine):
        # Target tables
        npi_to_individual_DBTable = DBTable(schema='ndh', table='individual_npi')
        npi_to_clinical_org_DBTable = DBTable(schema='ndh', table='organizational_npi')
        
        # Count records in both tables
        sql = f"""
        SELECT 
            (SELECT COUNT(*) FROM {npi_to_individual_DBTable}) as individual_count,
            (SELECT COUNT(*) FROM {npi_to_clinical_org_DBTable}) as organization_count
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        # Expect at least 1 record in each table
        individual_result = gx_df.expect_column_values_to_be_between(
            column="individual_count", 
            min_value=1,
            max_value=10000000
        )
        
        organization_result = gx_df.expect_column_values_to_be_between(
            column="organization_count", 
            min_value=1,
            max_value=10000000
        )
        
        if individual_result.success and organization_result.success:
            return True
        return f"One or both relationship tables have no records (Individual: {individual_result.success}, Organization: {organization_result.success})"


def main():
    print("Running Step16: Core NPI Table Verification")
    print("=" * 60)
    
    # Get database connection
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    print("Running InLaw verification tests...")
    print("=" * 60)
    
    # Run all validation tests
    test_results = InLaw.run_all(engine=alchemy_engine)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Step16 verification failed with error: {e}")
        print("\nMake sure you have:")
        print("1. Run Step15 successfully first")
        print("2. Installed required dependencies: pip install plainerflow pandas great-expectations")
        print("3. Proper database connection configured in .env")
        raise
