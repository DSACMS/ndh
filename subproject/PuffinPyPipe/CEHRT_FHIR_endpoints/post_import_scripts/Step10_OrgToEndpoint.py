#!/usr/bin/env python3
"""
ETL Pipeline Step: Map org_fhir_url endpoints to interopendpoint and link to ClinicalOrganization

This script:
1. Inserts all unique org_fhir_url values from lantern_ehr_fhir_raw.ehr_fhir_url into ndh.interopendpoint,
   with endpoint_name and endpoint_desc as 'EHR endpoint', using ON CONFLICT DO NOTHING.
2. Populates ndh.clinicalorg_to_interopendpoint by joining lantern_ehr_fhir_raw.ehr_fhir_url,
   ndh.organizational_npi, and ndh.interopendpoint, inserting all possible (clinicalorganization_id, interopendpoint_id) pairs,
   using ON CONFLICT DO NOTHING.

This script is idempotent and can be run multiple times safely.
"""

import os
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle # type: ignore

def main():
    is_just_print = False  # Set to True for dry-run

    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    # Table references
    ehr_fhir_url_DBTable = DBTable(schema='lantern_ehr_fhir_raw', table='ehr_fhir_url')
    interop_endpoint_DBTable = DBTable(schema='ndh', table='interop_endpoint')
    organizational_npi_DBTable = DBTable(schema='ndh', table='organizational_npi')
    clinical_organization_interopendpoint_DBTable = DBTable(schema='ndh', table='clinical_organization_interop_endpoint')

    sql = FrostDict()

    # Step 1: Insert unique org_fhir_url into ndh.interopendpoint
    sql['insert_interopendpoints'] = f"""
    INSERT INTO {interop_endpoint_DBTable} (fhir_endpoint_url, endpoint_name, endpoint_desc)
    SELECT DISTINCT org_fhir_url, 'EHR endpoint', 'EHR endpoint'
    FROM {ehr_fhir_url_DBTable}
    WHERE org_fhir_url IS NOT NULL
    ON CONFLICT (fhir_endpoint_url) DO NOTHING;
    """

    # Step 2: Insert links into ndh.clinicalorg_to_interopendpoint
    sql['insert_clinicalorg_to_interopendpoint'] = f"""
    INSERT INTO {clinical_organization_interopendpoint_DBTable} (clinical_organization_id, interop_endpoint_id)
    SELECT DISTINCT
        npi.clinical_organization_id,
        interop_endpoint.id AS interop_endpoint_id
    FROM {ehr_fhir_url_DBTable} AS ehr_fhir
    JOIN {organizational_npi_DBTable} AS npi
        ON ehr_fhir.npi = npi.NPI_id
    JOIN {interop_endpoint_DBTable} AS interop_endpoint
        ON ehr_fhir.org_fhir_url = interop_endpoint.fhir_endpoint_url
    WHERE ehr_fhir.org_fhir_url IS NOT NULL
      AND npi.clinical_organization_id IS NOT NULL
    ON CONFLICT DO NOTHING;
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
