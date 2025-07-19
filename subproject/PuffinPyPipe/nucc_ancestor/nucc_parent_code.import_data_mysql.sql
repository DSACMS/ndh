LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @ancestor_nucc_code_id, @child_nucc_code_id
)
SET
    `ancestor_nucc_code_id` = NULLIF(@ancestor_nucc_code_id, ''),
    `child_nucc_code_id` = NULLIF(@child_nucc_code_id, '')
;