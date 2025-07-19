-- There are regulatory requirements for using both NUCC codes and Medicare Provider Types, in the claims flow and elsewhere. 
-- Now it has been mandated by FHIR and is all around the provider data. 
-- Neither of these systems is good, but I see no way around using both of them and introducing a third "better"
-- system would just confuse everyone more. 



CREATE TABLE ndh.nucc_taxonomy_code (
    id SERIAL PRIMARY KEY,
    parent_nucc_taxonomy_code_id INT   NOT NULL,
    taxonomy_code VARCHAR(10)   NOT NULL,
    tax_grouping TEXT   NOT NULL,
    tax_classification TEXT   NOT NULL,
    tax_specialization TEXT   NOT NULL,
    tax_definition TEXT   NOT NULL,
    tax_notes TEXT   NOT NULL,
    tax_display_name TEXT   NOT NULL,
    tax_certifying_board_name TEXT   NOT NULL,
    tax_certifying_board_url TEXT   NOT NULL,
    CONSTRAINT uc_nucctaxonomycode_taxonomy_code UNIQUE (
        taxonomy_code
    )
);

-- TODO would it be easier if this included a parent, grandparent, greatgrandparent indicator of some kind?
CREATE TABLE ndh.nucc_taxonomy_code_ancestor_path (
    id SERIAL PRIMARY KEY,
    decendant_nucc_taxonomy_code_id INT   NOT NULL,
    ancestor_nucc_taxonomy_code_id INT   NOT NULL
);

-- 
CREATE TABLE ndh.npi_nucc_taxonomy_code (
    id SERIAL PRIMARY KEY,
    npi_id BIGINT   NOT NULL,
    nucc_taxonomy_code_id INT   NOT NULL,
    license_number VARCHAR(20)   NOT NULL,
    state_code_id INTEGER   NOT NULL,
    is_primary BOOLEAN   NOT NULL,
    taxonomy_group VARCHAR(10)   NOT NULL
);

CREATE TABLE ndh.medicare_provider_type_code (
    id SERIAL PRIMARY KEY,
    medicare_provider_type_name VARCHAR   NOT NULL
);

-- Crosswalk from: https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-provider-and-supplier-taxonomy-crosswalk

CREATE TABLE ndh.nucc_medicare_provider_type_code (
    id SERIAL PRIMARY KEY,
    medicare_provider_type_code_id INT   NOT NULL,
    nucc_taxonomy_code_id INT   NOT NULL
);
