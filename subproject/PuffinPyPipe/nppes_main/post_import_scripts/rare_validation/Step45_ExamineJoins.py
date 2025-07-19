#!/usr/bin/env python3
"""
Step45_ExamineJoins.py

This script systematically examines the join chain from Dr. Hussain's NPI to FHIR endpoints,
printing the results of each intermediate step to help debug where the join chain is broken.

It does NOT use the InLaw pattern, but instead runs and prints SELECT queries one at a time.

NPIs:
- Dr. Hussain: 1023008976
- Woodridge Primary Clinic: 1043699168

Join chain:
1. ndh.assigning_npi (find Dr. Hussain's assignment)
2. ndh.clinical_organization (join via clinical_organization_id)
3. ndh.clinical_organization_interop_endpoint (join via clinical_organization_id)
4. ndh.interop_endpoint (join via interop_endpoint_id)

If any step returns no rows, that is likely where the join chain is broken.
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder
import pandas as pd
import sqlalchemy
import os

def print_query_and_result(engine, query, description):
    print("\n" + "="*80)
    print(f"{description}")
    print("-"*80)
    print(query.strip())
    try:
        df = pd.read_sql_query(query, engine)
        print(f"\nReturned {len(df)} rows.")
        if len(df) > 0:
            print(df.head(10).to_string(index=False))
            if len(df) > 10:
                print(f"... (showing first 10 rows of {len(df)})")
        else:
            print("No rows returned.")
    except Exception as e:
        print(f"Query failed: {e}")

def main():
    # Connect to DB using PlainerFlow
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    dr_hussain_npi = '1023008976'
    woodridge_npi = '1043699168'

    # 1. Check assigning_npi for Dr. Hussain
    q1 = f"""
    SELECT * FROM ndh.assigning_npi
    WHERE npi_id = '{dr_hussain_npi}';
    """
    print_query_and_result(engine, q1, "Step 1: ndh.assigning_npi for Dr. Hussain")

    # 2. Join to clinical_organization
    q2 = f"""
    SELECT co.*
    FROM ndh.assigning_npi an
    JOIN ndh.clinical_organization co
      ON an.clinical_organization_id = co.id
    WHERE an.npi_id = '{dr_hussain_npi}';
    """
    print_query_and_result(engine, q2, "Step 2: Join assigning_npi to clinical_organization")

    # 3. Join to clinical_organization_interop_endpoint
    q3 = f"""
    SELECT coie.*
    FROM ndh.assigning_npi an
    JOIN ndh.clinical_organization_interop_endpoint coie
      ON an.clinical_organization_id = coie.clinical_organization_id
    WHERE an.npi_id = '{dr_hussain_npi}';
    """
    print_query_and_result(engine, q3, "Step 3: Join assigning_npi to clinical_organization_interop_endpoint")

    # 4. Join to interop_endpoint
    q4 = f"""
    SELECT ie.*
    FROM ndh.assigning_npi an
    JOIN ndh.clinical_organization_interop_endpoint coie
      ON an.clinical_organization_id = coie.clinical_organization_id
    JOIN ndh.interop_endpoint ie
      ON coie.interop_endpoint_id = ie.id
    WHERE an.npi_id = '{dr_hussain_npi}';
    """
    print_query_and_result(engine, q4, "Step 4: Join to interop_endpoint (FHIR endpoint)")

    # 5. (Optional) Try the same for Woodridge NPI as a cross-check
    q5 = f"""
    SELECT * FROM ndh.assigning_npi
    WHERE npi_id = '{woodridge_npi}';
    """
    print_query_and_result(engine, q5, "Step 5: ndh.assigning_npi for Woodridge Primary Clinic")

    print("\n" + "="*80)
    print("Examination complete. Review the above outputs to determine where the join chain is broken.")
    print("="*80)

if __name__ == "__main__":
    main()
