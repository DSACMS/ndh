Validate NPI assignment and endpoint data
==================

Introduction
--------------
I would like you to write a script that validates that CSV files are being imported correctly into the database and that JOINS against the database produce the desired results. 

* 1043699168 - Woodridge Primary Clinic
* 1023008976 - Dr Hussain



Please move on to the fourth step. The others are provided here just for context. 

First Step - use system calls to grep to examine the source CSV files
---------------

Note: the first step is complete.

For the first part of the script, I would like you to make system calls using GREP on files in precise locations on the file system. Using this, we will look inside the origin CSV files to make sure that the data that we think is in those files is in those files in the format that we want to see. So the NPIs are:


The files to check are:

* The pecos enrollment file at: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Enrollment_Extract_2025.04.01.csv
* The pecos reassignment file at: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Reassignment_Extract_2025.04.01.csv
* The FHIR endpoint data at: /Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/clean_npi_to_org_fhir_url.csv

The file structure of the enrollment file is:
NPI,PECOS_ASCT_CNTL_ID,ENRLMT_ID,PROVIDER_TYPE_CD,PROVIDER_TYPE_DESC,STATE_CD,FIRST_NAME,MDL_NAME,LAST_NAME,ORG_NAME

Use the NPI of each provider to get the ENRLMT_ID of the provider.
Then when you search the pecos reassignment file, use the ENRLMT_ID instead of the NPI.

Finally when you search the FHIR endpint file you will again use the NPI.

What we expect:

* There should be two different rows for the two NPIs in the enrollment file
* There should be one identical row of data in the assignment file that shows the Dr. Hussien assigns payment to Woodridge, but via enrollment ids instead of NPIs
* There should be one row of data in the EHR file that matches the NPI of Woodridge

Second Step - query the database using a series of InLaw tests to ensure that the data is being properly imported and ETLed. 
---------------

The second step is complete. 

Please write the following tests:

* Confirm that there is a record in pecos_raw.pecos_enrollment for Dr. Hussain and Woodridge clinic. There should be two rows returned in that table, when a WHERE IN clause with those NPIs as content is used against the 'npi' column.
* Confirm that the enrollment ids return one row of data when querying the pecos_raw.pecos_reassignment table. The columns there are reasgn_bnft_enrlmt_id and rcv_bnft_enrlmt_id respectively

This will confirm that the pecos assignment and enrollment files are properly imported into the database.

* Confirm that Woodridge Clinics NPI appears in the postgres.lantern_ehr_fhir_raw.ehr_fhir_url table when searching for the 'npi' column

This will confirm that the EHR endpoint data is being imported sucessfully.

Third Step
-------------------

Please read the following code: 

* nppes_main/post_import_scripts/Step30_pecos_knows_clinical_orgs.py
* nppes_main/post_import_scripts/Step35_pecos_knows_reassignment.py
* CHERT_FHIR_endpoints/post_import_scripts/Step10_OrgToEndpoint.py
* sql/create_table_sql/create_clinical_organization.sql
* sql/create_table_sql/create_interop_endpoint.sql

Using this source code, tell me the order of joins I need to do in order to determine a list of fhir endpoints for Dr. Hussien.

Please list out the table join structure to be able to determine how to join from:

* And individual who is assigning their medicare payments (like dr Hussain is to Woodridge) in the pecos reassignment table
* across a clinical organization (which aggregates many organizational pac_id from the pecos enrollment file, of which woodridge is one) which uses the pac_id from the assignment file to map many organizational npis from the enrollment file to a single clinical_organization which is using the same VTIN generated from the pac_id
* To the fhir endpoint table, which is suppose to be linked to clinical organizations 

Based on the previous analysis, make a new set of InLaw tests using the following three queries: 

```sql
--- Query for dr. Hussain
SELECT * FROM ndh.assigning_npi WHERE npi_id = '1023008976';
-- should return one row.

SELECT co.*
FROM ndh.assigning_npi an
JOIN ndh.clinical_organization co
  ON an.clinical_organization_id = co.id
WHERE an.npi_id = '1023008976';
-- should return one row

SELECT ie.fhir_endpoint_url
FROM ndh.assigning_npi an
JOIN ndh.clinical_organization_interop_endpoint coie
  ON an.clinical_organization_id = coie.clinical_organization_id
JOIN ndh.interop_endpoint ie
  ON coie.interop_endpoint_id = ie.id
WHERE an.npi_id = '1023008976';
-- should return at least one row
```

Add these inlaw scripts to the validation class and then run it.

Fourth Step
-----------

Please the new tests in  nppes_main/post_import_scripts/Step45_ExamineJoins.py

The last query in the third step above fails. 

Please write out all of the intermediate joins, using Woodridge Primary Clinic and  Dr Hussais NPIs in both directions until we determine what precise intermediate table is not working. 

For this, do not bother to follow the typical InLaw pattern. Instead, just run needed SELECT the queries against the database one at a time to figure out which part of broken.

Use the new file at nppes_main/post_import_scripts/Step45_ExamineJoins.py to record this process. 