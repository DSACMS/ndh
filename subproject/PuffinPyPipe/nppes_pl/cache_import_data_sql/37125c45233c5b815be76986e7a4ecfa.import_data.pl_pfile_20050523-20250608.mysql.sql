LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @npi, @provider_secondary_practice_address_address_line_1, @provider_secondary_practice_address_address_line_2, @provider_secondary_practice_address_city_name, @provider_secondary_practice_address_state_name, @provider_secondary_practice_address_postal_code, @provider_secondary_practice_address_country_code, @provider_secondary_practice_address_telephone_number, @provider_secondary_practice_address_telephone_extension, @provider_practice_address_fax_number
)
SET
    `npi` = NULLIF(@npi, ''),
    `provider_secondary_practice_address_address_line_1` = NULLIF(@provider_secondary_practice_address_address_line_1, ''),
    `provider_secondary_practice_address_address_line_2` = NULLIF(@provider_secondary_practice_address_address_line_2, ''),
    `provider_secondary_practice_address_city_name` = NULLIF(@provider_secondary_practice_address_city_name, ''),
    `provider_secondary_practice_address_state_name` = NULLIF(@provider_secondary_practice_address_state_name, ''),
    `provider_secondary_practice_address_postal_code` = NULLIF(@provider_secondary_practice_address_postal_code, ''),
    `provider_secondary_practice_address_country_code` = NULLIF(@provider_secondary_practice_address_country_code, ''),
    `provider_secondary_practice_address_telephone_number` = NULLIF(@provider_secondary_practice_address_telephone_number, ''),
    `provider_secondary_practice_address_telephone_extension` = NULLIF(@provider_secondary_practice_address_telephone_extension, ''),
    `provider_practice_address_fax_number` = NULLIF(@provider_practice_address_fax_number, '')
;