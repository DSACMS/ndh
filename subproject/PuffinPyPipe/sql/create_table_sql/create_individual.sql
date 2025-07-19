
-- TODO How does FHIR want us to express validated vs unvalidated credentials?
-- Is there an existing codeset they have specified for this?
-- Do we need to make an extension to have our own "credential codeset"
-- should this be 
CREATE TABLE ndh.clinical_credential (
    id SERIAL PRIMARY KEY,
    -- i.e. M.D.
    credential_acronym VARCHAR(20)   NOT NULL,
    -- i.e. Medical Doctor
    credential_name VARCHAR(100)   NOT NULL,
    -- for when there is only one source for the credential (unlike medical schools etc)
    credential_source_url VARCHAR(250)   NOT NULL,
    graduation_date DATE,
    clinical_school_id INT 
);

-- TODO We probably need a "type" for this, but we should wait until we have a better understanding of what it takes to validate this
CREATE TABLE ndh.clinical_school (
    id SERIAL PRIMARY KEY,
    -- i.e. M.D.
    clinical_school_name VARCHAR(20)   NOT NULL,
    clinical_school_url VARCHAR(500)
)

CREATE TABLE ndh.individual_to_credential (
    id SERIAL PRIMARY KEY,
    individual_id int   NOT NULL,
    clinical_credential_id int   NOT NULL
);

-- TODO: Presently I am assuming that we should keep the "user" system Django, OAuth and RBAC focused, linking to this table in the case where 
-- the user haa their own NPI or appears as an "authorized official" for an organization. An artifact from NPPES that will be difficult 
-- to release... though there probably be many "authorized official" one of which has primary contact status for a given org?

CREATE TABLE ndh.individual (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100)   NOT NULL,
    first_name VARCHAR(100)   NOT NULL,
    middle_name VARCHAR(21)   DEFAULT NULL,
    name_prefix VARCHAR(6)   DEFAULT NULL,
    name_suffix VARCHAR(6)   DEFAULT NULL,
    email_address VARCHAR(200)   DEFAULT NULL,
    ssn VARCHAR(10)   DEFAULT NULL,
    sex_code CHAR(1)  DEFAULT NULL,
    birth_date DATE
);
