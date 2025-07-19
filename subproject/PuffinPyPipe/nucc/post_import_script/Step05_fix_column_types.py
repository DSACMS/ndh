#!/usr/bin/env python3
"""
Fixes the npi as varchar import
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
    

    nucc_db = 'nucc_raw'

    nucc_table = 'nucc_merged_file' # for production
    nucc_ancestor_table = 'nucc_ancestor'
    nucc_sources_table = 'nucc_sources'

    nucc_DBTable = DBTable(schema=nucc_db, table=nucc_table)
    nucc_ancestor_DBTable = DBTable(schema=nucc_db, table=nucc_ancestor_table)
    nucc_sources_DBTable = DBTable(schema=nucc_db, table=nucc_sources_table)

    sql = FrostDict()

# Convert all of the code_id fields in the core nucc codes table from VARCHAR to INT. 

    sql['drop the id column if exists from previous run'] = f"""
ALTER TABLE {nucc_DBTable}
DROP COLUMN IF EXISTS id;
"""

    sql['create id column'] = f"""
ALTER TABLE {nucc_DBTable}
ADD COLUMN id INT;        
    """

    sql['populate the int version from the varchar version'] = f"""
UPDATE {nucc_DBTable}
SET id = scraped_code_id::INT;
""" 
 
# repeat the process for the sources table 

    sql['drop the id column if exists from previous run in sources'] = f"""
ALTER TABLE {nucc_sources_DBTable}
DROP COLUMN IF EXISTS nucc_id;
"""

    sql['create id column sources'] = f"""
ALTER TABLE {nucc_sources_DBTable}
ADD COLUMN nucc_id INT;        
    """

    sql['populate the int version from the varchar version in sources'] = f"""
UPDATE {nucc_sources_DBTable}
SET nucc_id = nucc_code_id::INT;
""" 
 

# repeat the process twice for the ancestor table. 

    sql['drop the id column if exists from previous run for ancestor'] = f"""
ALTER TABLE {nucc_ancestor_DBTable}
DROP COLUMN IF EXISTS ancestor_nucc_id;
"""
    sql['drop the id column if exists from previous run for child'] = f"""
ALTER TABLE {nucc_ancestor_DBTable}
DROP COLUMN IF EXISTS child_nucc_id;
"""

    sql['create id column ancestor'] = f"""
ALTER TABLE {nucc_ancestor_DBTable}
ADD COLUMN ancestor_nucc_id INT;        
    """

    sql['create id column child'] = f"""
ALTER TABLE {nucc_ancestor_DBTable}
ADD COLUMN child_nucc_id INT;        
    """

    sql['populate the int version from the varchar version ancestor'] = f"""
UPDATE {nucc_ancestor_DBTable}
SET ancestor_nucc_id = ancestor_nucc_code_id::INT;
""" 
 
    sql['populate the int version from the varchar version child'] = f"""
UPDATE {nucc_ancestor_DBTable}
SET child_nucc_id = child_nucc_code_id::INT;
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
