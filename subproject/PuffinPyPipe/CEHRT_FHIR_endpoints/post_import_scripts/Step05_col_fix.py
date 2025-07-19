#!/usr/bin/env python3
"""
Fixes the npi as varchar import for othername table
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle, InLaw # type: ignore
import pandas as pd
import sqlalchemy
from pathlib import Path
import os

def main():

    is_just_print = False
    
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location) # grab the parents parents .env


    ehr_fhir_table = 'ehr_fhir_url' # for production

    ehr_fhir_DBTable = DBTable(schema='lantern_ehr_fhir_raw', table=ehr_fhir_table)

    sql = FrostDict()

# Convert the NPI field from VARCHAR to BIGINT. 

    sql['drop the new_npi column if exists from previous run'] = f"""
ALTER TABLE {ehr_fhir_DBTable}
DROP COLUMN IF EXISTS new_npi;
"""

    sql['create new_npi column'] = f"""
ALTER TABLE {ehr_fhir_DBTable}
ADD COLUMN new_npi BIGINT;        
    """

    sql['populate the bigint version from the varchar version'] = f"""
UPDATE {ehr_fhir_DBTable}
SET new_npi = npi::BIGINT;
""" 
 
    sql['drop the varchar column'] = f"""
ALTER TABLE {ehr_fhir_DBTable}
DROP COLUMN npi;
"""

    sql['rename new column'] = f"""
ALTER TABLE {ehr_fhir_DBTable}
RENAME COLUMN new_npi TO npi;
"""

    # Add index on npi column to improve performance
    sql['add index on npi column'] = f"""
CREATE INDEX idx_npi_ehr_fhir ON {ehr_fhir_DBTable} (npi);
"""

    print("About to run SQL")
    SQLoopcicle.run_sql_loop(   sql_dict=sql,
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
