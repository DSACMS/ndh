-- OverwriteThisOnNextCompile=True

CREATE DATABASE IF NOT EXISTS REPLACE_ME_DB_NAME;

DROP TABLE IF EXISTS REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME;

CREATE TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME (
    `combined_code` VARCHAR(11),
    `download_grouping` VARCHAR(77),
    `download_classification` VARCHAR(95),
    `download_specialization` VARCHAR(72),
    `download_definition` VARCHAR(2007),
    `download_notes` VARCHAR(1408),
    `download_display_name` VARCHAR(94),
    `download_section` VARCHAR(15),
    `scraped_code_id` VARCHAR(5),
    `scraped_code_long_name` VARCHAR(94),
    `scraped_code_short_name` VARCHAR(95),
    `scraped_code_definition` VARCHAR(1999),
    `scraped_code_notes` VARCHAR(1375),
    `scraped_code_effective_date` VARCHAR(10),
    `scraped_last_modified_date` VARCHAR(10),
    `scraped_deactivation_date` VARCHAR(10),
    `scraped_immediate_parent_code_id` VARCHAR(5),
    `code` VARCHAR(11),
    `code_text` VARCHAR(11)
);