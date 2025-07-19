-- Merged SQL statements for schema: nppes_normal
-- Generated on: 2025-07-14 12:28:32
-- Total statements for this schema: 15
--
-- Source files:
--   ./sql/create_table_sql/create_nppes_data.sql


-- Source: ./sql/create_table_sql/create_nppes_data.sql
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

-- Source: ./sql/create_table_sql/create_nppes_data.sql
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

-- Source: ./sql/create_table_sql/create_nppes_data.sql
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

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.identifier_type_lut (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT UNIQUE NOT NULL
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.npi_identifier (    
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,    
    npi BIGINT,
    identifier VARCHAR(21),
    identifier_type_code INTEGER REFERENCES nppes_normal.identifier_type_lut(id),
    state VARCHAR(3),
    issuer VARCHAR(81)
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.address_type_lut (
    id SERIAL PRIMARY KEY,
    address_type_description TEXT UNIQUE NOT NULL
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.phone_type_lut (
    id SERIAL PRIMARY KEY,
    phone_type_description TEXT UNIQUE NOT NULL
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.state_code_lut (
    id SERIAL PRIMARY KEY,
    state_code VARCHAR(100) UNIQUE NOT NULL,
    state_name VARCHAR(100) NOT NULL
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.orgname_type_lut (
    id SERIAL PRIMARY KEY,
    orgname_description TEXT UNIQUE NOT NULL,
    source_file TEXT NOT NULL,
    source_field TEXT NOT NULL
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.orgname (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    organization_name VARCHAR(70),
    orgname_type_code INTEGER REFERENCES nppes_normal.orgname_type_lut(id),
    code_description VARCHAR(100)
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
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

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.npi_phone (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    phone_type_id INTEGER ,
    phone_number VARCHAR(20),
    is_fax BOOLEAN
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
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

-- Source: ./sql/create_table_sql/create_nppes_data.sql
CREATE TABLE nppes_normal.npi_identifiers (
    id SERIAL PRIMARY KEY,
    npidetail_id BIGINT,     
    npi BIGINT,
    identifier VARCHAR(20),
    type_code VARCHAR(2),
    state_id INTEGER ,
    issuer VARCHAR(80)
);

-- Source: ./sql/create_table_sql/create_nppes_data.sql
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
