-- I want to not support Faxes in the new NDH, but that may not be a realistic goal. 
-- beyond that, this is just a reasonable way to model phone numbers that is normalized in a way that makes 
-- detecting "same number... different extension" a useful excercise in provider data linking. 



CREATE TABLE ndh.phone_type (
    id SERIAL PRIMARY KEY,
    phone_type_description TEXT   NOT NULL,
    CONSTRAINT uc_phone_type_phone_type_description UNIQUE (
        phone_type_description
    )
);


CREATE TABLE ndh.npi_phone (
    id SERIAL PRIMARY KEY,
    npi_id BIGINT   NOT NULL,
    phonetype_id INTEGER   NOT NULL,
    phone_number_id INTEGER   NOT NULL,
    phone_extension VARCHAR(10)   NOT NULL,
    is_fax BOOLEAN   NOT NULL   -- TODO there is an edge case where one provider lists a phone as a fax and another lists it as a phone. Rare, but it could cause complexity
);



Create TABLE ndh.phone_number (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20)   NOT NULL,
    CONSTRAINT uc_phone_extension_phone UNIQUE (phone_number)
);
