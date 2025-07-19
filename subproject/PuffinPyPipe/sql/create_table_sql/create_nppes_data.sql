
-- normalized version of data from NPPES (National Plan and Provider Enumeration System) 
-- from https://download.cms.gov/nppes/NPI_Files.html



-- NPI Core Entity Table
CREATE TABLE nppes_normal.npidetail (
    id BIGINT PRIMARY KEY,
    npi BIGINT,
    entity_type_code SMALLINT NOT NULL, -- 1 = individual, 2 = organization
    replacement_npi VARCHAR(11),
    enumeration_date DATE,
    last_update_date DATE,
    deactivation_reason_code VARCHAR(3),
    deactivation_date DATE,
    reactivation_date DATE,
    certification_date DATE
);

-- Individuals
CREATE TABLE nppes_normal.npi_individual (
    npidetail_id BIGINT,  
    npi BIGINT,
    last_name VARCHAR(36),
    first_name VARCHAR(36),
    middle_name VARCHAR(21),
    name_prefix VARCHAR(6),
    name_suffix VARCHAR(6),
    credential_text VARCHAR(21),
    is_sole_proprietor BOOLEAN,
    sex_code CHAR(1)
);

-- Organizations
CREATE TABLE nppes_normal.npi_organization (
    npidetail_id BIGINT,    
    npi BIGINT,
    organization_name VARCHAR(101),
    authorized_official_last_name VARCHAR(36),
    authorized_official_first_name VARCHAR(21),
    authorized_official_middle_name VARCHAR(21),
    authorized_official_prefix VARCHAR(6),
    authorized_official_suffix VARCHAR(6),
    authorized_official_title VARCHAR(36),
    authorized_official_credential_text VARCHAR(21),
    authorized_official_phone VARCHAR(21),
    parent_org_lbn VARCHAR(71),
    parent_org_tin VARCHAR(10),
    is_org_subpart BOOLEAN
);

-- identifier type lookup table
CREATE TABLE nppes_normal.identifier_type_lut (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT UNIQUE NOT NULL
);


-- Identifiers
CREATE TABLE nppes_normal.npi_identifier (    
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,    
    npi BIGINT,
    identifier VARCHAR(21),
    identifier_type_code INTEGER REFERENCES nppes_normal.identifier_type_lut(id),
    state VARCHAR(3),
    issuer VARCHAR(81)
);


-- Lookup: Address Type
CREATE TABLE nppes_normal.address_type_lut (
    id SERIAL PRIMARY KEY,
    address_type_description TEXT UNIQUE NOT NULL
);

INSERT INTO nppes_normal.address_type_lut (address_type_description) VALUES
    ('mailing_address_main'),
    ('practice_location_main'),
    ('secondary_practice_location'),
    ('endpoint_address');

-- Lookup: Phone Type
CREATE TABLE nppes_normal.phone_type_lut (
    id SERIAL PRIMARY KEY,
    phone_type_description TEXT UNIQUE NOT NULL
);

INSERT INTO nppes_normal.phone_type_lut (phone_type_description) VALUES
    ('main_mailing_phone'),
    ('main_practice_phone'),
    ('secondary_practice_phone'),
    ('main_mailing_fax'),
    ('main_practice_fax'),
    ('secondary_practice_fax');


-- Lookup: State Codes
CREATE TABLE nppes_normal.state_code_lut (
    id SERIAL PRIMARY KEY,
    state_code VARCHAR(100) UNIQUE NOT NULL,
    state_name VARCHAR(100) NOT NULL
);

-- Lookup: Organization Name Types
CREATE TABLE nppes_normal.orgname_type_lut (
    id SERIAL PRIMARY KEY,
    orgname_description TEXT UNIQUE NOT NULL,
    source_file TEXT NOT NULL,
    source_field TEXT NOT NULL
);

INSERT INTO nppes_normal.orgname_type_lut (orgname_description, source_file, source_field) VALUES
    -- From Other Name Reference File
    ('Doing Business As (DBA) Name', 'Other Name Reference File', 'Other Organization Name Type Code'),
    ('Former Legal Business Name', 'Other Name Reference File', 'Other Organization Name Type Code'),
    ('Other Name', 'Other Name Reference File', 'Other Organization Name Type Code'),
    ('Other', 'Other Name Reference File', 'Other Organization Name Type Code'),

    -- From Endpoint Reference File
    ('Endpoint Affiliated Legal Business Name', 'Endpoint Reference File', 'Affiliated Legal Business Name'),
    ('Endpoint Organization Affiliation', 'Endpoint Reference File', 'Affiliation'),
    ('Endpoint Contact Name', 'Endpoint Reference File', 'Contact Name'),

    -- From Base NPPES File
    ('Primary Legal Business Name', 'NPPES Core File', 'Provider Organization Name (Legal Business Name)'),

    -- From Deactivation/Subpart fields
    ('Parent Organization', 'NPPES Core File', 'Parent Organization LBN'),
    ('Subpart Organization', 'NPPES Core File', 'Is Subpart');

-- Organization Alternate Names
CREATE TABLE nppes_normal.orgname (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    organization_name VARCHAR(70),
    orgname_type_code INTEGER REFERENCES nppes_normal.orgname_type_lut(id),
    code_description VARCHAR(100)
);

-- Addresses
CREATE TABLE nppes_normal.npi_address (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    address_type_id INTEGER ,
    line_1 VARCHAR(55),
    line_2 VARCHAR(55),
    city VARCHAR(40),
    state_id INTEGER REFERENCES nppes_normal.state_code_lut(id),
    postal_code VARCHAR(20),
    country_code VARCHAR(2)
);

-- Phone Numbers
CREATE TABLE nppes_normal.npi_phone (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    phone_type_id INTEGER ,
    phone_number VARCHAR(20),
    is_fax BOOLEAN
);

-- Taxonomy Entries
CREATE TABLE nppes_normal.npi_taxonomy (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    taxonomy_code VARCHAR(10),
    license_number VARCHAR(20),
    license_state_id INTEGER ,
    is_primary BOOLEAN,
    taxonomy_group VARCHAR(10)
);

-- Identifiers
CREATE TABLE nppes_normal.npi_identifiers (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    identifier VARCHAR(20),
    type_code VARCHAR(2),
    state_id INTEGER ,
    issuer VARCHAR(80)
);

CREATE TABLE nppes_normal.npi_endpoints (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    endpoint_type TEXT,                             -- E.g., Direct Messaging, FHIR, etc.
    endpoint_type_description TEXT,
    endpoint TEXT,                                  -- The actual URL or address
    affiliation TEXT,                               -- Relationship to the NPI
    affiliation_legal_business_name TEXT,
    use TEXT,                                       -- E.g., 'Work', 'Home'
    use_description TEXT,
    content_type TEXT,                              -- E.g., application/fhir+json
    content_type_description TEXT,
    content_other TEXT,                             -- When 'Other' is specified
    address_line_1 TEXT,
    address_line_2 TEXT,
    city TEXT,
    state_id INTEGER REFERENCES nppes_normal.state_code_lut(id),
    postal_code TEXT,
    country_code TEXT,
    endpoint_description TEXT,
    endpoint_comments TEXT,
    last_updated DATE
);
