#!/usr/bin/env python3
"""
Assignment to Endpoint Validation Script

This script checks for the presence of two specific NPIs in three specific CSV files using system grep calls,
runs InLaw tests to validate that the data is properly imported and ETLed in the database,
and (step 3) validates the join path from an individual assigning NPI to clinical organization to FHIR endpoint.

NPIs to check:
- 1043699168 (Woodridge Primary Clinic)
- 1023008976 (Dr Hussain)

Files to check:
- PECOS Enrollment: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Enrollment_Extract_2025.04.01.csv
- PECOS Reassignment: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Reassignment_Extract_2025.04.01.csv
- FHIR Endpoint: /Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/clean_npi_to_org_fhir_url.csv

The file structure of the enrollment file is:
NPI,PECOS_ASCT_CNTL_ID,ENRLMT_ID,PROVIDER_TYPE_CD,PROVIDER_TYPE_DESC,STATE_CD,FIRST_NAME,MDL_NAME,LAST_NAME,ORG_NAME

Process:
1. Grep for the two NPIs in the enrollment file and extract their ENRLMT_IDs.
2. Use those ENRLMT_IDs to grep the reassignment file.
3. Grep for Woodridge's NPI in the FHIR endpoint file.
4. Report if the expected matches are found.

5. Run InLaw tests to confirm the data is imported and ETLed correctly in the database.

6. (Step 3) Run InLaw tests to validate the join path from an individual assigning NPI to clinical organization to FHIR endpoint.

Expected:
- Two rows for the two NPIs in the enrollment file
- One row in the reassignment file showing Dr. Hussain assigns payment to Woodridge, using ENRLMT_IDs
- One row in the EHR file matching the NPI of Woodridge

This script prints the matching lines and reports whether the expectations are met, then runs InLaw tests.
"""

import subprocess
import csv
import os

# --- PlainerFlow imports for InLaw tests ---
import plainerflow
from plainerflow import CredentialFinder, InLaw

NPIS = {
    "1043699168": "Woodridge Primary Clinic",
    "1023008976": "Dr Hussain"
}

FILES = {
    "PECOS Enrollment": "/Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Enrollment_Extract_2025.04.01.csv",
    "PECOS Reassignment": "/Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Reassignment_Extract_2025.04.01.csv",
    "FHIR Endpoint": "/Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/clean_npi_to_org_fhir_url.csv"
}

def grep_npi_in_file(npi, file_path):
    try:
        result = subprocess.run(
            ["grep", "-w", npi, file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().splitlines()
        else:
            return []
    except Exception as e:
        return [f"Error searching for {npi} in {file_path}: {e}"]

def grep_enrlmt_id_in_file(enrlmt_id, file_path):
    try:
        result = subprocess.run(
            ["grep", "-w", enrlmt_id, file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().splitlines()
        else:
            return []
    except Exception as e:
        return [f"Error searching for ENRLMT_ID {enrlmt_id} in {file_path}: {e}"]

def extract_enrlmt_id_from_enrollment_line(line):
    # Enrollment file columns:
    # NPI,PECOS_ASCT_CNTL_ID,ENRLMT_ID,PROVIDER_TYPE_CD,PROVIDER_TYPE_DESC,STATE_CD,FIRST_NAME,MDL_NAME,LAST_NAME,ORG_NAME
    try:
        reader = csv.reader([line])
        row = next(reader)
        if len(row) >= 3:
            return row[2]
        else:
            return None
    except Exception:
        return None

def run_grep_and_report():
    summary = {
        "enrollment": {"1043699168": 0, "1023008976": 0, "1043699168_enrlmt_id": None, "1023008976_enrlmt_id": None},
        "reassignment": {"woodridge_enrlmt_id": 0, "hussain_enrlmt_id": 0, "assignment_match": False},
        "fhir": {"1043699168": 0}
    }

    # Step 1: Grep for NPIs in enrollment file and extract ENRLMT_IDs
    print(f"\n=== Checking file: PECOS Enrollment ===")
    enrollment_path = FILES["PECOS Enrollment"]
    npi_to_enrlmt_id = {}
    for npi in NPIS:
        lines = grep_npi_in_file(npi, enrollment_path)
        summary["enrollment"][npi] = len(lines)
        print(f"\n-- Results for NPI {npi} ({NPIS[npi]}) --")
        if lines:
            for line in lines:
                print(line)
                enrlmt_id = extract_enrlmt_id_from_enrollment_line(line)
                if enrlmt_id:
                    npi_to_enrlmt_id[npi] = enrlmt_id
                    summary["enrollment"][f"{npi}_enrlmt_id"] = enrlmt_id
        else:
            print(f"No matches found for NPI {npi} in PECOS Enrollment.")

    # Step 2: Use ENRLMT_IDs to grep reassignment file
    print(f"\n=== Checking file: PECOS Reassignment ===")
    reassignment_path = FILES["PECOS Reassignment"]
    woodridge_enrlmt_id = npi_to_enrlmt_id.get("1043699168")
    hussain_enrlmt_id = npi_to_enrlmt_id.get("1023008976")
    reassignment_lines = {}
    if woodridge_enrlmt_id:
        lines = grep_enrlmt_id_in_file(woodridge_enrlmt_id, reassignment_path)
        summary["reassignment"]["woodridge_enrlmt_id"] = len(lines)
        reassignment_lines["woodridge"] = lines
        print(f"\n-- Results for Woodridge ENRLMT_ID {woodridge_enrlmt_id} --")
        if lines:
            for line in lines:
                print(line)
        else:
            print(f"No matches found for Woodridge ENRLMT_ID {woodridge_enrlmt_id} in PECOS Reassignment.")
    else:
        print("Could not determine Woodridge ENRLMT_ID from enrollment file.")

    if hussain_enrlmt_id:
        lines = grep_enrlmt_id_in_file(hussain_enrlmt_id, reassignment_path)
        summary["reassignment"]["hussain_enrlmt_id"] = len(lines)
        reassignment_lines["hussain"] = lines
        print(f"\n-- Results for Dr Hussain ENRLMT_ID {hussain_enrlmt_id} --")
        if lines:
            for line in lines:
                print(line)
        else:
            print(f"No matches found for Dr Hussain ENRLMT_ID {hussain_enrlmt_id} in PECOS Reassignment.")
    else:
        print("Could not determine Dr Hussain ENRLMT_ID from enrollment file.")

    # Check for assignment row: a line in reassignment file containing both ENRLMT_IDs
    found_assignment = False
    if woodridge_enrlmt_id and hussain_enrlmt_id:
        try:
            result = subprocess.run(
                ["grep", "-w", hussain_enrlmt_id, reassignment_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.strip().splitlines():
                    if woodridge_enrlmt_id in line:
                        found_assignment = True
                        print("\n-- Found assignment row (Dr Hussain assigns payment to Woodridge via ENRLMT_IDs):")
                        print(line)
            summary["reassignment"]["assignment_match"] = found_assignment
            if not found_assignment:
                print("\n-- No row found where Dr Hussain assigns payment to Woodridge in reassignment file (via ENRLMT_IDs).")
        except Exception as e:
            print(f"Error searching for assignment row: {e}")

    # Step 3: Grep for Woodridge NPI in FHIR Endpoint
    print(f"\n=== Checking file: FHIR Endpoint ===")
    fhir_path = FILES["FHIR Endpoint"]
    lines = grep_npi_in_file("1043699168", fhir_path)
    summary["fhir"]["1043699168"] = len(lines)
    print(f"\n-- Results for NPI 1043699168 (Woodridge Primary Clinic) --")
    if lines:
        for line in lines:
            print(line)
    else:
        print("No matches found for NPI 1043699168 in FHIR Endpoint.")

    # Print summary
    print("\n====================")
    print("Validation Summary:")
    print("====================")
    # Enrollment
    if summary["enrollment"]["1043699168"] >= 1 and summary["enrollment"]["1023008976"] >= 1:
        print("✔ Enrollment file: Found at least one row for each NPI (Woodridge and Dr Hussain).")
    else:
        print("✘ Enrollment file: Missing row(s) for one or both NPIs.")
    # Reassignment
    if summary["reassignment"]["assignment_match"]:
        print("✔ Reassignment file: Found row where Dr Hussain assigns payment to Woodridge (via ENRLMT_IDs).")
    else:
        print("✘ Reassignment file: Did NOT find row where Dr Hussain assigns payment to Woodridge (via ENRLMT_IDs).")
    # FHIR
    if summary["fhir"]["1043699168"] >= 1:
        print("✔ FHIR Endpoint file: Found at least one row for Woodridge NPI.")
    else:
        print("✘ FHIR Endpoint file: No row found for Woodridge NPI.")

    return npi_to_enrlmt_id

# --- InLaw Tests ---

class InLawEnrollmentNPIs(InLaw):
    title = "Enrollment table contains both NPIs"
    @staticmethod
    def run(engine):
        # Hardcoded NPIs for this test
        npi1 = "1043699168"
        npi2 = "1023008976"
        sql = f"""
        SELECT npi FROM pecos_raw.pecos_enrollment
        WHERE npi IN ('{npi1}', '{npi2}')
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_table_row_count_to_equal(2)
        if result.success:
            return True
        return f"pecos_raw.pecos_enrollment missing one or both NPIs: {npi1}, {npi2}"

class InLawReassignmentENRLMTIDs(InLaw):
    title = "Reassignment table contains assignment row for ENRLMT_IDs"
    @staticmethod
    def run(engine):
        # Hardcoded ENRLMT_IDs for Dr Hussain and Woodridge
        reasgn_bnft_enrlmt_id = "I20050609000361"  # Dr Hussain
        rcv_bnft_enrlmt_id = "O20160426001836"     # Woodridge
        sql = f"""
        SELECT reasgn_bnft_enrlmt_id, rcv_bnft_enrlmt_id FROM pecos_raw.pecos_reassignment
        WHERE reasgn_bnft_enrlmt_id = '{reasgn_bnft_enrlmt_id}'
          AND rcv_bnft_enrlmt_id = '{rcv_bnft_enrlmt_id}'
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_table_row_count_to_equal(1)
        if result.success:
            return True
        return f"pecos_raw.pecos_reassignment missing assignment row for ENRLMT_IDs: {reasgn_bnft_enrlmt_id}, {rcv_bnft_enrlmt_id}"

class InLawFhirNPI(InLaw):
    title = "Woodridge NPI appears in EHR FHIR URL table"
    @staticmethod
    def run(engine):
        npi = "1043699168"
        sql = f"""
        SELECT npi FROM postgres.lantern_ehr_fhir_raw.ehr_fhir_url
        WHERE npi = '{npi}'
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_table_row_count_to_be_between(min_value=1, max_value=1000)
        if result.success:
            return True
        return f"postgres.lantern_ehr_fhir_raw.ehr_fhir_url missing NPI: {npi}"

# --- Step 3: InLaw tests for join path from assigning NPI to endpoint ---

class InLawAssigningNpiRow(InLaw):
    title = "assigning_npi contains Dr. Hussain as assigning NPI"
    @staticmethod
    def run(engine):
        sql = """
        SELECT * FROM ndh.assigning_npi WHERE npi_id = '1023008976';
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_table_row_count_to_equal(1)
        if result.success:
            return True
        return "ndh.assigning_npi does not contain exactly one row for Dr. Hussain (NPI 1023008976)"

class InLawAssigningNpiToClinicalOrg(InLaw):
    title = "assigning_npi join to clinical_organization returns one row"
    @staticmethod
    def run(engine):
        sql = """
        SELECT co.*
        FROM ndh.assigning_npi an
        JOIN ndh.clinical_organization co
          ON an.clinical_organization_id = co.id
        WHERE an.npi_id = '1023008976';
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_table_row_count_to_equal(1)
        if result.success:
            return True
        return "assigning_npi join to clinical_organization does not return exactly one row for Dr. Hussain"


class InLawAssigningNpiToClinicalOrg(InLaw):
    title = "full test returns 1 row"
    @staticmethod
    def run(engine):
        sql = """
SELECT ie.fhir_endpoint_url
FROM ndh.assigning_npi an
JOIN ndh.clinical_organization_interop_endpoint coie
  ON an.clinical_organization_id = coie.clinical_organization_id
JOIN ndh.interop_endpoint ie
  ON coie.interop_endpoint_id = ie.id
WHERE an.npi_id = '1023008976';
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_table_row_count_to_equal(1)
        if result.success:
            return True
        return "joining all the way from Dr Hussain to the endpoints fails"



# (Removed InLawAssigningNpiToEndpoint)

def run_inlaw_tests(npi_to_enrlmt_id):
    print("\n====================")
    print("Running InLaw Database Validation Tests")
    print("====================")
    # Get DB engine from .env in parent to parent directory
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    # Run all InLaw tests in this script using the InLaw runner
    InLaw.run_all(engine=engine)


def main():
    npi_to_enrlmt_id = run_grep_and_report()
    run_inlaw_tests(npi_to_enrlmt_id)


if __name__ == "__main__":
    main()
