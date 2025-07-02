-- Merged CREATE TABLE statements
-- Generated on: 2025-07-02 03:39:10
-- Total CREATE TABLE statements: 63
--
-- Source files:
--   sql/create_table_sql/create_address.sql
--   sql/create_table_sql/create_clinical_organization.sql
--   sql/create_table_sql/create_EHR.sql
--   sql/create_table_sql/create_healthcarebrand.sql
--   sql/create_table_sql/create_identifier.sql
--   sql/create_table_sql/create_individual.sql
--   sql/create_table_sql/create_interop_endpoint.sql
--   sql/create_table_sql/create_npi.sql
--   sql/create_table_sql/create_nppes_data.sql
--   sql/create_table_sql/create_payer_data.sql
--   sql/create_table_sql/create_phone.sql
--   sql/create_table_sql/create_provider_taxonomy.sql
--   sql/create_table_sql/create_user_tables.sql


CREATE TABLE ndh.address (
    id SERIAL PRIMARY KEY,
    barcode_delivery_code VARCHAR(12),
    smarty_key VARCHAR(10),
    address_us_id INT NULL,
    address_international_id INT NULL,
    address_nonstandard_id INT NULL
);

CREATE TABLE ndh.address_us (
    id SERIAL PRIMARY KEY,
    address_id INT NOT NULL,
    input_id VARCHAR(36),
    input_index INT,
    candidate_index INT,
    addressee VARCHAR(64),
    delivery_line_1 VARCHAR(64),
    delivery_line_2 VARCHAR(64),
    last_line VARCHAR(64),
    delivery_point_barcode VARCHAR(12),
    
    -- Components
    urbanization VARCHAR(64),
    primary_number VARCHAR(30),
    street_name VARCHAR(64),
    street_predirection VARCHAR(16),
    street_postdirection VARCHAR(16),
    street_suffix VARCHAR(16),
    secondary_number VARCHAR(32),
    secondary_designator VARCHAR(16),
    extra_secondary_number VARCHAR(32),
    extra_secondary_designator VARCHAR(16),
    pmb_designator VARCHAR(16),
    pmb_number VARCHAR(16),
    city_name VARCHAR(64),
    default_city_name VARCHAR(64),
    state_abbreviation CHAR(2),
    zipcode CHAR(5),
    plus4_code VARCHAR(4),
    delivery_point CHAR(2),
    delivery_point_check_digit CHAR(1),
    
    -- Metadata
    record_type CHAR(1),
    zip_type VARCHAR(32),
    county_fips CHAR(5),
    county_name VARCHAR(64),
    ews_match CHAR(5),
    carrier_route CHAR(4),
    congressional_district CHAR(2),
    building_default_indicator CHAR(1),
    rdi VARCHAR(12),
    elot_sequence VARCHAR(4),
    elot_sort VARCHAR(4),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    coordinate_license INT,
    geo_precision VARCHAR(18),
    time_zone VARCHAR(48),
    utc_offset DECIMAL(4,2),
    dst CHAR(5),
    
    -- Analysis
    dpv_match_code VARCHAR(1),
    dpv_footnotes VARCHAR(32),
    dpv_cmra VARCHAR(1),
    dpv_vacant VARCHAR(1),
    dpv_no_stat VARCHAR(1),
    active VARCHAR(1),
    footnotes VARCHAR(24),
    lacslink_code VARCHAR(2),
    lacslink_indicator VARCHAR(1),
    suitelink_match VARCHAR(5),
    enhanced_match VARCHAR(64)
);

CREATE TABLE ndh.address_international (
    id SERIAL PRIMARY KEY,
    address_id INT NOT NULL,
    input_id VARCHAR(36),
    country VARCHAR(64),
    geocode VARCHAR(4),
    local_language VARCHAR(6),
    freeform VARCHAR(512),
    address1 VARCHAR(64),
    address2 VARCHAR(64),
    address3 VARCHAR(64),
    address4 VARCHAR(64),
    organization VARCHAR(64),
    locality VARCHAR(64),
    administrative_area VARCHAR(32),
    postal_code VARCHAR(16),
    
    -- Components
    administrative_area_iso2 VARCHAR(8),
    sub_administrative_area VARCHAR(64),
    country_iso_3 VARCHAR(3),
    premise VARCHAR(64),
    premise_number VARCHAR(64),
    thoroughfare VARCHAR(64),
    
    -- Metadata
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    geocode_precision VARCHAR(32),
    max_geocode_precision VARCHAR(32),
    address_format VARCHAR(128),
    
    -- Analysis
    verification_status VARCHAR(32),
    address_precision VARCHAR(32),
    max_address_precision VARCHAR(32)
);

CREATE TABLE ndh.address_nonstandard (
    id SERIAL PRIMARY KEY,
    address_id INT NOT NULL,
    input_id VARCHAR(36),
    input_index INT,
    candidate_index INT,
    addressee VARCHAR(64),
    delivery_line_1 VARCHAR(64),
    delivery_line_2 VARCHAR(64),
    last_line VARCHAR(64),
    
    -- Any additional fields specific to non-standard addresses
    address_type VARCHAR(32),
    address_format VARCHAR(128),
    raw_address TEXT,
    notes TEXT
);

CREATE TABLE ndh.AddressTypeLUT (
    id SERIAL PRIMARY KEY,
    address_type_description TEXT   NOT NULL,
    CONSTRAINT uc_AddressTypeLUT_address_type_description UNIQUE (
        address_type_description
    )
);

CREATE TABLE ndh.StateCodeLUT (
    id SERIAL PRIMARY KEY,
    state_code VARCHAR(100)   NOT NULL,
    state_name VARCHAR(100)   NOT NULL,
    CONSTRAINT uc_StateCodeLUT_state_code UNIQUE (
        state_code
    )
);

CREATE TABLE ndh.NPIAddress (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    AddressType_id INTEGER   NOT NULL,
    Address_id INT   NOT NULL
);

CREATE TABLE ndh.ClinicalOrganization (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_legal_name VARCHAR(200)   NOT NULL,
    AuthorizedOfficial_Individual_id INT   NOT NULL,
    ParentOrganization_id INT   NOT NULL,
    OrganizationTIN VARCHAR(10)   NOT NULL,
    primary_VTIN_id INT   NOT NULL,
    OrganizationGLIEF VARCHAR(300)   NOT NULL,
    CONSTRAINT uc_Organization_OrganizationTIN UNIQUE (
        OrganizationTIN
    )
);

CREATE TABLE ndh.VTIN (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_id INT NOT NULL,
    VTIN VARCHAR(37) NOT NULL,
    VTIN_extension_number INT NOT NULL -- defaults to 0
);

CREATE TABLE ndh.ClinicalOrgnameTypeLUT (
    id SERIAL PRIMARY KEY,
    orgname_type_description TEXT   NOT NULL,
    source_file TEXT   NOT NULL,
    source_field TEXT   NOT NULL,
    CONSTRAINT uc_OrgnameTypeLUT_orgname_description UNIQUE (
        orgname_type_description
    )
);

CREATE TABLE ndh.Orgname (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_id INT   NOT NULL,
    ClinicalOrganization_name VARCHAR(70)   NOT NULL,
    ClinicalOrgnameType_id INTEGER   NOT NULL
);

CREATE TABLE ndh.EHRToNPI (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    EHR_id int   NOT NULL
);

CREATE TABLE ndh.EHR (
    id SERIAL PRIMARY KEY,
    -- Sourced from CHPL data here https://chpl.healthit.gov/
    CHPL_ID VARCHAR(200)   NOT NULL,
    bulk_endpoint_json_url VARCHAR(500) NULL
);

CREATE TABLE ndh.HealthcareBrand (
    id SERIAL PRIMARY KEY,
    HealthcareBrand_name VARCHAR(200)   NOT NULL,
    TrademarkSerialNumber VARCHAR(20)   NOT NULL
);

CREATE TABLE ndh.OrganizationToHealthcareBrand (
    id SERIAL PRIMARY KEY,
    HealthcareBrand_id INT   NOT NULL,
    Organization_id INT   NOT NULL
);

CREATE TABLE ndh.IdentifierTypeLUT (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT   NOT NULL,
    CONSTRAINT uc_IdentifierTypeLUT_identifier_type_description UNIQUE (
        identifier_type_description
    )
);

CREATE TABLE ndh.NPIIdentifier (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    identifier VARCHAR(21)   NOT NULL,
    IdentifierType_id INTEGER   NOT NULL,
    state VARCHAR(3)   NOT NULL,
    issuer VARCHAR(81)   NOT NULL
);

CREATE TABLE ndh.CredentialLUT (
    id SERIAL PRIMARY KEY,
    -- i.e. M.D.
    Credential_acronym VARCHAR(20)   NOT NULL,
    -- i.e. Medical Doctor
    Credential_name VARCHAR(100)   NOT NULL,
    -- for when there is only one source for the credential (unlike medical schools etc)
    Credential_source_url VARCHAR(250)   NOT NULL
);

CREATE TABLE ndh.IndividualToCredential (
    id SERIAL PRIMARY KEY,
    Individual_id int   NOT NULL,
    Credential_id int   NOT NULL
);

CREATE TABLE ndh.Individual (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100)   NOT NULL,
    first_name VARCHAR(100)   NOT NULL,
    middle_name VARCHAR(21)   NOT NULL,
    name_prefix VARCHAR(6)   NOT NULL,
    name_suffix VARCHAR(6)   NOT NULL,
    email_address VARCHAR(200)   NOT NULL,
    maybe_SSN VARCHAR(10)   NOT NULL
);

CREATE TABLE ndh.NPIToEndpoint (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    Endpoint_id INT   NOT NULL
);

CREATE TABLE ndh.InteropEndpointTypeLUT (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT   NOT NULL,
    CONSTRAINT uc_EndpointTypeLUT_identifier_type_description UNIQUE (
        identifier_type_description
    )
);

CREATE TABLE ndh.InteropEndpoint (
    id SERIAL PRIMARY KEY,
    -- for now only FHIR and Direct
    fhir_endpoint_url VARCHAR(500)   NOT NULL,
    -- endpoint NPPES file as endpoint_description
    endpoint_name VARCHAR(100)   NOT NULL,
    -- endpoint NPPES file as endpoint_comments
    endpoint_desc VARCHAR(100)   NOT NULL,
    EndpointAddress_id int   NOT NULL, -- this I am unsure about. It is specified in the FHIR standard, but perhaps it is ephemerial? What does it mean for a mutli-ONPI EHR endpoint to have 'an' address?
    InteropEndpointType_id int   NOT NULL
);

CREATE TABLE ndh.OrgToInteropEndpoint (
    id SERIAL PRIMARY KEY,
    Organization_id int   NOT NULL,
    InteropEndpoint_id int   NOT NULL
);

CREATE TABLE ndh.NPI (
    id SERIAL PRIMARY KEY,
    npi BIGINT   NOT NULL,
    entity_type_code SMALLINT   NOT NULL,
    replacement_npi VARCHAR(11)   NOT NULL,
    enumeration_date DATE   NOT NULL,
    last_update_date DATE   NOT NULL,
    deactivation_reason_code VARCHAR(3)   NOT NULL,
    deactivation_date DATE   NOT NULL,
    reactivation_date DATE   NOT NULL,
    certification_date DATE   NOT NULL
);

CREATE TABLE ndh.NPI_to_Individual (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    Individual_id INT   NOT NULL,
    is_sole_proprietor BOOLEAN   NOT NULL,
    sex_code CHAR(1)   NOT NULL
);

CREATE TABLE ndh.NPI_to_ClinicalOrganization (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    ClinicalOrganization_id INT   NOT NULL,
    PrimaryAuthorizedOfficial_Individual_id INT NOT NULL -- TODO shold this be its own intermediate table? With an is_primary boolean in it?
);

CREATE TABLE nppes_normal.npidetail (
    id INT PRIMARY KEY,
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

CREATE TABLE nppes_normal.npi_individual (
    npidetail_id INT,  
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

CREATE TABLE nppes_normal.npi_organization (
    npidetail_id INT,    
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

CREATE TABLE nppes_normal.identifier_type_lut (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT UNIQUE NOT NULL
);

CREATE TABLE nppes_normal.npi_identifier (    
    id SERIAL PRIMARY KEY,
    npidetail_id INT,    
    npi BIGINT,
    identifier VARCHAR(21),
    identifier_type_code INTEGER REFERENCES nppes_normal.identifier_type_lut(id),
    state VARCHAR(3),
    issuer VARCHAR(81)
);

CREATE TABLE nppes_normal.address_type_lut (
    id SERIAL PRIMARY KEY,
    address_type_description TEXT UNIQUE NOT NULL
);

CREATE TABLE nppes_normal.phone_type_lut (
    id SERIAL PRIMARY KEY,
    phone_type_description TEXT UNIQUE NOT NULL
);

CREATE TABLE nppes_normal.state_code_lut (
    id SERIAL PRIMARY KEY,
    state_code VARCHAR(100) UNIQUE NOT NULL,
    state_name VARCHAR(100) NOT NULL
);

CREATE TABLE nppes_normal.orgname_type_lut (
    id SERIAL PRIMARY KEY,
    orgname_description TEXT UNIQUE NOT NULL,
    source_file TEXT NOT NULL,
    source_field TEXT NOT NULL
);

CREATE TABLE nppes_normal.orgname (
    id SERIAL PRIMARY KEY,
    npidetail_id INT,     
    npi BIGINT,
    organization_name VARCHAR(70),
    orgname_type_code INTEGER REFERENCES nppes_normal.orgname_type_lut(id),
    code_description VARCHAR(100)
);

CREATE TABLE nppes_normal.npi_address (
    id SERIAL PRIMARY KEY,
    npidetail_id INT,     
    npi BIGINT,
    address_type_id INTEGER ,
    line_1 VARCHAR(55),
    line_2 VARCHAR(55),
    city VARCHAR(40),
    state_id INTEGER REFERENCES nppes_normal.state_code_lut(id),
    postal_code VARCHAR(20),
    country_code VARCHAR(2)
);

CREATE TABLE nppes_normal.npi_phone (
    id SERIAL PRIMARY KEY,
    npidetail_id INT,     
    npi BIGINT,
    phone_type_id INTEGER ,
    phone_number VARCHAR(20),
    is_fax BOOLEAN
);

CREATE TABLE nppes_normal.npi_taxonomy (
    id SERIAL PRIMARY KEY,
    npidetail_id INT,     
    npi BIGINT,
    taxonomy_code VARCHAR(10),
    license_number VARCHAR(20),
    license_state_id INTEGER ,
    is_primary BOOLEAN,
    taxonomy_group VARCHAR(10)
);

CREATE TABLE nppes_normal.npi_identifiers (
    id SERIAL PRIMARY KEY,
    npidetail_id INT,     
    npi BIGINT,
    identifier VARCHAR(20),
    type_code VARCHAR(2),
    state_id INTEGER ,
    issuer VARCHAR(80)
);

CREATE TABLE nppes_normal.npi_endpoints (
    id SERIAL PRIMARY KEY,
    npidetail_id INT,     
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

CREATE TABLE ndh.PayerToInteropEndpoint (
    id SERIAL PRIMARY KEY,
    Payer_id int   NOT NULL,
    InteropEndpoint_id int   NOT NULL
);

CREATE TABLE ndh.Payer (
    -- marketplace/network-puf.IssuerID
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.IssuerMarketPlaceMarketingName
    PayerName varchar   NOT NULL
);

CREATE TABLE ndh.Plan (
    -- marketplace/plan-attributes-puf.PlanId
    id SERIAL PRIMARY KEY,
    Payer_id int   NOT NULL,
    MarketCoverage_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.ServiceAreaId
    ServiceArea_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.DentalOnlyPlan
    DentalOnlyPlan boolean   NOT NULL,
    -- marketplace/plan-attributes-puf.PlanMarketingName
    PlanMarketingName varchar   NOT NULL,
    -- marketplace/plan-attributes-puf.HIOSProductId
    HIOSProductID varchar   NOT NULL,
    PlanType_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.IsNewPlan
    IsNewPlan boolean   NOT NULL
);

CREATE TABLE ndh.PlanType (
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.PlanType
    PlanType varchar   NOT NULL
);

CREATE TABLE ndh.MarketCoverage (
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.MarketCoverage
    MarketCoverage varchar   NOT NULL
);

CREATE TABLE ndh.PlanNetworkToPlan (
    id SERIAL PRIMARY KEY,
    Plan_id int   NOT NULL,
    PlanNetwork_id int   NOT NULL
);

CREATE TABLE ndh.PlanNetwork (
    -- marketplace/network-puf.NetworkID
    id SERIAL PRIMARY KEY,
    -- marketplace/network-puf.NetworkName
    PlanNetworkName varchar   NOT NULL,
    -- marketplace/network-puf.NetworkURL
    PlanNetworkURL varchar   NOT NULL
);

CREATE TABLE ndh.ServiceArea (
    -- marketplace/plan-attributes-puf.ServiceAreaId
    id SERIAL PRIMARY KEY,
    -- marketplace/service-area-puf.ServiceAreaName
    ServiceAreaName varchar   NOT NULL,
    -- marketplace/service-area-puf.StateCode
    StateCode varchar   NOT NULL
    -- wishlist
    -- , service_area_shape GEOMETRY(MULTIPOLYGON, 4326)   NOT NULL -- enable with PostGIS turned on! 
);

CREATE TABLE ndh.PlanNetworkToOrg (
    id SERIAL PRIMARY KEY,
    PlanNetwork_id int   NOT NULL,
    Organization_id int   NOT NULL
);

CREATE TABLE ndh.PhoneTypeLUT (
    id SERIAL PRIMARY KEY,
    phone_type_description TEXT   NOT NULL,
    CONSTRAINT uc_PhoneTypeLUT_phone_type_description UNIQUE (
        phone_type_description
    )
);

CREATE TABLE ndh.NPIToPhone (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    PhoneType_id INTEGER   NOT NULL,
    PhoneNumber_id INTEGER   NOT NULL,
    PhoneExtension_id INTEGER  NULL,
    is_fax BOOLEAN   NOT NULL
);

Create TABLE ndh.PhoneNumber (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20)   NOT NULL
);

Create TABLE ndh.PhoneExtension (
    id SERIAL PRIMARY KEY,
    phone_extension VARCHAR(10)   NOT NULL
);

CREATE TABLE ndh.NUCCTaxonomyCode (
    id SERIAL PRIMARY KEY,
    ParentNUCCTaxonomyCode_id INT   NOT NULL,
    taxonomy_code VARCHAR(10)   NOT NULL,
    tax_grouping TEXT   NOT NULL,
    tax_classification TEXT   NOT NULL,
    tax_specialization TEXT   NOT NULL,
    tax_definition TEXT   NOT NULL,
    tax_notes TEXT   NOT NULL,
    tax_display_name TEXT   NOT NULL,
    tax_certifying_board_name TEXT   NOT NULL,
    tax_certifying_board_url TEXT   NOT NULL,
    CONSTRAINT uc_NUCCTaxonomyCode_taxonomy_code UNIQUE (
        taxonomy_code
    )
);

CREATE TABLE ndh.NUCCTaxonomyCodePath (
    id SERIAL PRIMARY KEY,
    NUCCTaxonomyCodeDecendant_id INT   NOT NULL,
    NUCCTaxonomyCodeAncestor_id INT   NOT NULL
);

CREATE TABLE ndh.NPITaxonomy (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    NUCCTaxonomyCode_id INT   NOT NULL,
    license_number VARCHAR(20)   NOT NULL,
    StateCode_id INTEGER   NOT NULL,
    is_primary BOOLEAN   NOT NULL,
    taxonomy_group VARCHAR(10)   NOT NULL
);

CREATE TABLE ndh.MedicareProviderType (
    id SERIAL PRIMARY KEY,
    MedicareProviderType_name VARCHAR   NOT NULL
);

CREATE TABLE ndh.NUCCMedicareProviderType (
    id SERIAL PRIMARY KEY,
    MedicareProviderType_id INT   NOT NULL,
    NUCCTaxonomyCode_id INT   NOT NULL
);

CREATE TABLE ndh.User (
    id SERIAL PRIMARY KEY,
    Email varchar   NOT NULL,
    FirstName varchar   NOT NULL,
    LastName varchar   NOT NULL,
    IdentityVerified boolean   NOT NULL
);

CREATE TABLE ndh.UserAccessRole (
    id SERIAL PRIMARY KEY,
    User_id INT   NOT NULL,
    Role_id INT   NOT NULL,
    NPI_id BIGINT   NOT NULL
);

CREATE TABLE ndh."Role" (
    id SERIAL PRIMARY KEY,
    "Role" varchar(100)   NOT NULL
);
