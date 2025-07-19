CREATE DATABASE IF NOT EXISTS REPLACE_ME_DB_NAME;

DROP TABLE IF EXISTS REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME;

CREATE TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME (
    `npi` VARCHAR(11),
    `provider_secondary_practice_address_address_line_1` VARCHAR(56),
    `provider_secondary_practice_address_address_line_2` VARCHAR(56),
    `provider_secondary_practice_address_city_name` VARCHAR(41),
    `provider_secondary_practice_address_state_name` VARCHAR(40),
    `provider_secondary_practice_address_postal_code` VARCHAR(17),
    `provider_secondary_practice_address_country_code` VARCHAR(3),
    `provider_secondary_practice_address_telephone_number` VARCHAR(20),
    `provider_secondary_practice_address_telephone_extension` VARCHAR(6),
    `provider_practice_address_fax_number` VARCHAR(16)
);