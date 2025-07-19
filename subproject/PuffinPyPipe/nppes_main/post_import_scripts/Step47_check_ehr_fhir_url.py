#!/usr/bin/env python3
"""
Check if Woodridge NPI (1043699168) is present in lantern_ehr_fhir_raw.ehr_fhir_url.
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

    query = f"""
    SELECT * FROM lantern_ehr_fhir_raw.ehr_fhir_url
    WHERE npi = '{npi}';
    """
    print("Querying lantern_ehr_fhir_raw.ehr_fhir_url for Woodridge NPI...")
    df = pd.read_sql_query(query, engine)
    print(df if not df.empty else "No row found for Woodridge NPI.")

if __name__ == "__main__":
    main()
