-- Merged SQL statements for schema: public
-- Generated on: 2025-07-14 12:28:32
-- Total statements for this schema: 3
--
-- Source files:
--   ./sql/create_table_sql/create_intake_npi_changes.sql


-- Source: ./sql/create_table_sql/create_intake_npi_changes.sql
CREATE INDEX IF NOT EXISTS idx_npi_processing_run_date ON intake.npi_processing_run(run_date);
CREATE INDEX IF NOT EXISTS idx_npi_change_log_npi ON intake.npi_change_log(npi);

-- Source: ./sql/create_table_sql/create_intake_npi_changes.sql
CREATE INDEX IF NOT EXISTS idx_npi_change_log_run ON intake.npi_change_log(processing_run_id);
CREATE INDEX IF NOT EXISTS idx_npi_change_log_type ON intake.npi_change_log(change_type);

-- Source: ./sql/create_table_sql/create_intake_npi_changes.sql
CREATE INDEX IF NOT EXISTS idx_individual_change_log_npi ON intake.individual_change_log(npi);
CREATE INDEX IF NOT EXISTS idx_parent_relationship_change_log_child ON intake.parent_relationship_change_log(child_npi);
