LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @nucc_code_id, @full_source_text, @source_date, @source_date_note, @extracted_urls
)
SET
    `nucc_code_id` = NULLIF(@nucc_code_id, ''),
    `full_source_text` = NULLIF(@full_source_text, ''),
    `source_date` = NULLIF(@source_date, ''),
    `source_date_note` = NULLIF(@source_date_note, ''),
    `extracted_urls` = NULLIF(@extracted_urls, '')
;