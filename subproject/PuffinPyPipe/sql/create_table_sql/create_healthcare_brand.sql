-- It is obvious that we need a mechanism to support "brand-level" searching in the NDH. This is likely not sophisticated enough but it is an OK MVP, given that we 
-- do not know for certain what should be here. 

-- TODO does this reconcile with the brand/logo work that the new FHIR IG is doing, or do we need a different layer to manage this problem.
-- Test cases to sort: 
-- Searches for "walgreens"
-- Searches for "Mayo Clinic" and other system names
-- Should we be using the AHA or other system modelings for this?
-- How does this connect to the contract-owning-EIN vs delivering-care EIN problem?
-- Assuming that "control of trademark" is the approach for determining access control..
-- But "control of domain name" or web-ssl cert verification might be easier to implement and work with

CREATE TABLE ndh.healthcare_brand (
    id SERIAL PRIMARY KEY,
    healthcare_brand_name VARCHAR(200)   NOT NULL,
    trademark_serial_number VARCHAR(20)   NOT NULL,
    CONSTRAINT uc_healthcare_brand_name UNIQUE (
        healthcare_brand_name
    )
);

CREATE TABLE ndh.organization_healthcare_brand (
    id SERIAL PRIMARY KEY,
    healthcare_brand_id INT   NOT NULL,
    clinical_organization_id INT   NOT NULL
);
