#!/usr/bin/env python3
"""
Check if Woodridge NPI (1043699168) is mapped to clinical_organization_id 929617 in ndh.organizational_npi.
"""

import os
import pandas as pd
from plainerflow import CredentialFinder

def main():
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    npi = '1043699168'
    clinical_organization_id = 929617

    query = f"""
    SELECT * FROM ndh.organizational_npi
    WHERE npi_id = '{npi}' AND clinical_organization_id = {clinical_organization_id};
    """
    print("Querying ndh.organizational_npi for Woodridge mapping...")
    df = pd.read_sql_query(query, engine)
    print(df if not df.empty else "No mapping found.")

if __name__ == "__main__":
    main()
