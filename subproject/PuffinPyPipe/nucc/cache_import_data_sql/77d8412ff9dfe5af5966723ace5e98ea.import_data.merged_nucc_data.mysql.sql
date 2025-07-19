LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @combined_code, @download_grouping, @download_classification, @download_specialization, @download_definition, @download_notes, @download_display_name, @download_section, @scraped_code_id, @scraped_code_long_name, @scraped_code_short_name, @scraped_code_definition, @scraped_code_notes, @scraped_code_effective_date, @scraped_last_modified_date, @scraped_deactivation_date, @code, @code_text
)
SET
    `combined_code` = NULLIF(@combined_code, ''),
    `download_grouping` = NULLIF(@download_grouping, ''),
    `download_classification` = NULLIF(@download_classification, ''),
    `download_specialization` = NULLIF(@download_specialization, ''),
    `download_definition` = NULLIF(@download_definition, ''),
    `download_notes` = NULLIF(@download_notes, ''),
    `download_display_name` = NULLIF(@download_display_name, ''),
    `download_section` = NULLIF(@download_section, ''),
    `scraped_code_id` = NULLIF(@scraped_code_id, ''),
    `scraped_code_long_name` = NULLIF(@scraped_code_long_name, ''),
    `scraped_code_short_name` = NULLIF(@scraped_code_short_name, ''),
    `scraped_code_definition` = NULLIF(@scraped_code_definition, ''),
    `scraped_code_notes` = NULLIF(@scraped_code_notes, ''),
    `scraped_code_effective_date` = NULLIF(@scraped_code_effective_date, ''),
    `scraped_last_modified_date` = NULLIF(@scraped_last_modified_date, ''),
    `scraped_deactivation_date` = NULLIF(@scraped_deactivation_date, ''),
    `code` = NULLIF(@code, ''),
    `code_text` = NULLIF(@code_text, '')
;