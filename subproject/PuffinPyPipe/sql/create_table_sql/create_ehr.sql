--Sourced from CHPL data and Lantern data



-- I would love it if this could be EHR to ONPI, but there are sole pracitioners and other informal partnership arrangements that mean that there are individuals who have no ONPI
-- who are using an EHR that has a distinct endpoint. 

CREATE TABLE ndh.ehr_instance_to_npi (
    id SERIAL PRIMARY KEY,
    npi_id BIGINT   NOT NULL,
    ehr_id INT   NOT NULL
);

CREATE TABLE ndh.ehr_instance (
    id SERIAL PRIMARY KEY,
    -- Sourced from CHPL data here https://chpl.healthit.gov/
    chpl_id VARCHAR(200)   NOT NULL,
    bulk_endpoint_json_url VARCHAR(500) NULL
);
