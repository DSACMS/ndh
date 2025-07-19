-- Intake tables for tracking NPI changes during monthly updates
-- These tables support incremental processing of NPPES data

-- Track processing runs and their metadata
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

-- Track individual NPI changes detected during processing
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

-- Track Individual record changes
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

-- Track parent relationship changes for organizations
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

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_npi_processing_run_date ON intake.npi_processing_run(run_date);
CREATE INDEX IF NOT EXISTS idx_npi_change_log_npi ON intake.npi_change_log(npi);
CREATE INDEX IF NOT EXISTS idx_npi_change_log_run ON intake.npi_change_log(processing_run_id);
CREATE INDEX IF NOT EXISTS idx_npi_change_log_type ON intake.npi_change_log(change_type);
CREATE INDEX IF NOT EXISTS idx_individual_change_log_npi ON intake.individual_change_log(npi);
CREATE INDEX IF NOT EXISTS idx_parent_relationship_change_log_child ON intake.parent_relationship_change_log(child_npi);
