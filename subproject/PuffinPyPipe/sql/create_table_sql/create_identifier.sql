-- TODO: Would like feedback from Sarah and others about this. This is a reflection of what is currently in NPPES
-- we will need to replicate this if we want to replicate a back-wards compatible NPPES
-- but in reality, the use-case of mapping previous insurance idenfifiers is really over..
-- and this is no used for state level licensing, and other uses cases that should be data mined
-- i.e. some states still have Medicaid identifiers I think


CREATE TABLE ndh.identifier_type (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT   NOT NULL,
    CONSTRAINT uc_IdentifierTypeLUT_identifier_type_description UNIQUE (
        identifier_type_description
    )
);

CREATE TABLE ndh.npi_identifier (
    id SERIAL PRIMARY KEY,
    npi_id BIGINT   NOT NULL,
    identifier VARCHAR(21)   NOT NULL,
    identifier_type_id INTEGER   NOT NULL,
    state_id INT   NOT NULL,
    identifier_issuer_name VARCHAR(81)   NOT NULL
);
