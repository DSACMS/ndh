#!/usr/bin/env python3
"""
Restore the main nppes table from backup.. useful for testing the ETL
"""

import plainerflow
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle, InLaw
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
    

    npi_table = 'main_file' # for production

    npi_DBTable = DBTable(schema='nppes_raw', table=npi_table)
    npi_small_DBTable = npi_DBTable.create_child('_small')
    npi_backup_DBTable = npi_DBTable.create_child('_backup')

    sql = FrostDict()


    sql['drop the prod database'] = f"""
DROP TABLE IF EXISTS {npi_DBTable}
"""


    big_sql= f"""
CREATE TABLE {npi_DBTable} AS 
SELECT * FROM {npi_backup_DBTable}
"""  
    # So that we can comment this out.
    sql['restore the main database from backup'] = big_sql

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
        
