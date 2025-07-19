





-- these will most obviously include "Payer", "EHR", but could eventually run the gamut "PHR", "Public Health", "HIE", "Patient Registry", etc etc.

DROP TABLE IF EXISTS ndh.interop_endpoint_type

CREATE TABLE ndh.interop_endpoint_type (
    id SERIAL PRIMARY KEY,
    interop_endpoint_type_description TEXT   NOT NULL,
    CONSTRAINT uc_endpoint_type_interop_endpoint_type_description UNIQUE (
        interop_endpoint_type_description
    )
);

-- TODO This is our practical and current need, but I suspect there is a existing FHIR standard that we may need to implement with or instead of this. 
INSERT INTO ndh.interop_endpoint_type (id, interop_endpoint_type_description)
VALUES (1, 'EHR FHIR Endpoint'),
        (2,'Payer Plan Network Endpoint'),
        (3, 'Payer Patient Data Endpoint')

DROP TABLE IF EXISTS ndh.interop_endpoint;

CREATE TABLE ndh.interop_endpoint (
    id SERIAL PRIMARY KEY,
    -- for now only FHIR and Direct
    fhir_endpoint_url VARCHAR(500)   NOT NULL,
    -- endpoint NPPES file as endpoint_description
    endpoint_name VARCHAR(100)   NOT NULL,
    -- endpoint NPPES file as endpoint_comments
    endpoint_desc VARCHAR(100)   NOT NULL,
    endpoint_address_id INT   DEFAULT NULL, -- this I am unsure about. It is specified in the FHIR standard, but perhaps it is ephemerial? What does it mean for a mutli-ONPI EHR endpoint to have 'an' address?
    interop_endpoint_type_id INT DEFAULT 1  NOT NULL,
    -- Prevent duplicate FHIR endpoint URLs
    CONSTRAINT uq_interop_endpoint_url UNIQUE (fhir_endpoint_url)    
);

DROP TABLE IF EXISTS ndh.clinical_organization_interop_endpoint;

CREATE TABLE ndh.clinical_organization_interop_endpoint (
    id SERIAL PRIMARY KEY,
    clinical_organization_id INT   NOT NULL,
    interop_endpoint_id INT   NOT NULL
);

DROP INDEX IF EXISTS ndh.idx_clinorg_interop_unique;

CREATE UNIQUE INDEX idx_clinorg_interop_unique
ON ndh.clinical_organization_interop_endpoint (clinical_organization_id, interop_endpoint_id);