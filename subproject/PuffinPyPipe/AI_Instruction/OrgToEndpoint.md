Org To Endpoint
===================

Please implement this in CHERT_FHIR_endpoints/post_import_scripts/Step10_OrgToEndpoint.py using the plainerflow tools as described in AI_Instruction/PlainerflowTools.md
This is a PostgreSQL only implementation. 

Ignore validation for this ETL for now. We will do a seperate validation project later.

In the table lantern_ehr_fhir_raw.ehr_fhir_url we have a npi column and a org_fhir_url column.

These org_fhir_urls actually map to the higher level organizational concept in our ndh database.

First, we need to ensure that every distinct endppint in the org_fhir_url column exists as a distinct entity in the interopendpoints table, which looks like this:

CREATE TABLE ndh.interopendpoint (
    id SERIAL PRIMARY KEY,
    fhir_endpoint_url VARCHAR(500)   NOT NULL,
    endpoint_name VARCHAR(100)   NOT NULL,
    endpoint_desc VARCHAR(100)   NOT NULL,
    endpoint_address_id INT  DEFAULT NULL,
    interopendpointtype_id INT DEFAULT 1  NOT NULL

    -- Prevent duplicate FHIR endpoint URLs
    CONSTRAINT uq_interopendpoint_url UNIQUE (fhir_endpoint_url)    
);

For now populate the endpoint_name and endpoint description as the string 'EHR endpoint'
A uninque fhir_endpoint_url should always create a new record in ndh.interopendpoint

We need ClinicalOrganization_id to ndh.clinicalorg_to_interopendpoint table (which looks like this)

CREATE TABLE ndh.clinicalorg_to_interopendpoint (
    id SERIAL PRIMARY KEY,
    clinicalorganization_id int   NOT NULL,
    interopendpoint_id int   NOT NULL
);

We need to make a CTAS statement, where an underlying SELECT has bridged between ClinicalOrganization and Org NPI.

Thus, we create a SELECT that joins lantern_ehr_fhir_raw.ehr_fhir_url and ndh.organizational_npi which has the org npi to clinicalorganization mappings

CREATE TABLE ndh.organizational_npi (
    id BIGINT  PRIMARY KEY,
    NPI_id BIGINT   NOT NULL UNIQUE,
    ClinicalOrganization_id INT  DEFAULT NULL,
    PrimaryAuthorizedOfficial_Individual_id INT NOT NULL,
    Parent_NPI_id BIGINT DEFAULT NULL-- TODO shold this be its own intermediate table? With an is_primary boolean in it?
);

The second join will be against the fhir url itself which now resides in the ndh.interopendpoint table. 
This will be a join on the urls: fhir_endpoint_url = org_fhir_url


Having a select, with that join allows us to do a CTAS to populate clinicalorg_to_interopendpoint
clinicalorg_to_interopendpoint has a unique index and so when this data has already been intered, the CTAS statement should do nothing on those conflicts.
Rely on the rely on ON CONFLICT DO NOTHING to ensure that only new connections are added. 

The script should be run again and again so it should be idempotent. 


