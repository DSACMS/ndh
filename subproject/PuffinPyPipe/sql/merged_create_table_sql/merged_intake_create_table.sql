-- Merged SQL statements for schema: intake
-- Generated on: 2025-07-14 12:28:32
-- Total statements for this schema: 6
--
-- Source files:
--   ./sql/create_table_sql/create_intake_npi_changes.sql
--   ./sql/create_table_sql/create_intake_phone.sql
--   ./sql/create_table_sql/create_intake_wrongnpi.sql


-- Source: ./sql/create_table_sql/create_intake_npi_changes.sql
CREATE TABLE IF NOT EXISTS intake.npi_processing_run (
    id SERIAL PRIMARY KEY,
    run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_table VARCHAR(100) NOT NULL,
    total_npis_processed INTEGER,
    new_npis INTEGER,
    updated_npis INTEGER,
    deactivated_npis INTEGER,
    processing_status VARCHAR(50) DEFAULT 'IN_PROGRESS',
    notes TEXT
);

-- Source: ./sql/create_table_sql/create_intake_npi_changes.sql
CREATE TABLE IF NOT EXISTS intake.npi_change_log (
    id SERIAL PRIMARY KEY,
    processing_run_id INTEGER REFERENCES intake.npi_processing_run(id),
    npi BIGINT NOT NULL,
    change_type VARCHAR(50) NOT NULL, -- 'NEW', 'UPDATED', 'DEACTIVATED', 'REACTIVATED'
    change_detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_last_update_date DATE,
    new_last_update_date DATE,
    change_details JSONB,
    processed BOOLEAN DEFAULT FALSE
);

-- Source: ./sql/create_table_sql/create_intake_npi_changes.sql
CREATE TABLE IF NOT EXISTS intake.individual_change_log (
    id SERIAL PRIMARY KEY,
    processing_run_id INTEGER REFERENCES intake.npi_processing_run(id),
    individual_id INTEGER,
    npi BIGINT,
    change_type VARCHAR(50) NOT NULL, -- 'NEW', 'UPDATED', 'NAME_CHANGE'
    change_detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB,
    processed BOOLEAN DEFAULT FALSE
);

-- Source: ./sql/create_table_sql/create_intake_npi_changes.sql
CREATE TABLE IF NOT EXISTS intake.parent_relationship_change_log (
    id SERIAL PRIMARY KEY,
    processing_run_id INTEGER REFERENCES intake.npi_processing_run(id),
    child_npi BIGINT NOT NULL,
    old_parent_npi BIGINT,
    new_parent_npi BIGINT,
    change_type VARCHAR(50) NOT NULL, -- 'NEW_PARENT', 'PARENT_CHANGED', 'PARENT_REMOVED'
    change_detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Source: ./sql/create_table_sql/create_intake_phone.sql
CREATE TABLE intake.staging_phone (
    id SERIAL PRIMARY KEY,

    -- 1) Raw input exactly as received
    raw_phone          TEXT,                         -- e.g. "(415)555-2671 ext.123"
    is_normalized_success BOOLEAN DEFAULT FALSE,

    -- 2) Parsed components (after Python `phonenumbers`)
    phone_e164         VARCHAR(20),                  -- canonical: "+14155552671"
    country_code       VARCHAR(4),                   -- e.g. "1"
    ndh_PhoneNumber_id  INT DEFAULT NULL, -- link to the unique NDH records for this phone_e164 and country code.   

    raw_phone_extension    VARCHAR(10),                  -- optional: "123"
    ndh_PhoneExtension_id INT, -- link to phone type

    -- 3) Metadata for lineage / debugging
    source_file        TEXT,                         -- feed filename or identifier
    is_fax_in_source   BOOLEAN,
    source_row         INTEGER,                      -- original row number in feed
    ingestion_ts       TIMESTAMPTZ DEFAULT NOW(),    -- when ingested
    error_notes        TEXT,                         -- parser errors or validations
    
    -- Unique constraint to prevent duplicate processing of same raw phone from same source
    CONSTRAINT uc_staging_phone_raw_source UNIQUE (raw_phone, source_file, is_fax_in_source)
);

-- Source: ./sql/create_table_sql/create_intake_wrongnpi.sql
CREATE TABLE intake.wrongnpi (
    npi BIGINT,
    error_type_string VARCHAR(50),
    reason_npi_is_wrong TEXT
);
