-- FUNCTION: ndh.insert_practitioner(bigint, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character, character varying)

-- DROP FUNCTION IF EXISTS ndh.insert_practitioner(bigint, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character, character varying);

/* SAMPLE USAGE:

SELECT ndh.insert_practitioner(
	<p_npi bigint>,
	<p_ssn character varying>,
	<p_gender_code character varying>,
	<p_birth_date date>,
	<p_first_name character varying>,
	<p_middle_name character varying>,
	<p_last_name character varying>,
	<p_name_prefix character varying>,
	<p_name_suffix character varying>,
	<p_language_spoken_id character varying>,
	<p_email_address character varying>,
	<p_nucc_taxonomy_code_id character varying>,
	<p_state_id character>,
	<p_phone_number character varying>
)
*/

CREATE OR REPLACE FUNCTION ndh.insert_practitioner(
	p_npi bigint,
	p_ssn character varying,
	p_gender_code character varying,
	p_birth_date date,
	p_first_name character varying,
	p_middle_name character varying,
	p_last_name character varying,
	p_name_prefix character varying,
	p_name_suffix character varying,
	p_language_spoken_id character varying,
	p_email_address character varying,
	p_nucc_taxonomy_code_id character varying,
	p_state_id character,
	p_phone_number character varying)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE p_individual_id int; p_phone_number_id int;
BEGIN

	INSERT INTO npi(npi, entity_type_code, enumeration_date, last_update_date)
	VALUES (p_npi, 1, CURRENT_DATE, CURRENT_DATE);

    INSERT INTO individual (ssn, gender_code, birth_date)
    VALUES (p_ssn, p_gender_code, p_birth_date)
	RETURNING id into p_individual_id;

	INSERT INTO provider (individual_id, npi)
	VALUES (p_individual_id, p_npi);

	INSERT INTO individual_to_name (individual_id, first_name, middle_name, last_name, prefix, suffix, fhir_name_type_id,effective_date)
	VALUES (p_individual_id, p_first_name,p_middle_name, p_last_name,p_name_prefix, p_name_suffix,2,p_birth_date);

	INSERT INTO phone_number (value)
	VALUES (p_phone_number)
	RETURNING id into p_phone_number_id;

	INSERT INTO individual_to_phone_number (individual_id, phone_number_id, phone_type_id)
	VALUES (p_individual_id, p_phone_number_id, 1);

	INSERT INTO individual_to_email_address (individual_id, email_address)
	VALUES (p_individual_id, p_email_address);

	INSERT INTO individual_to_language_spoken (individual_id, language_spoken_id)
	VALUES (p_individual_id, p_language_spoken_id);

	INSERT INTO individual_to_nucc_taxonomy_code (individual_id, nucc_taxonomy_code_id, state_id)
	values (p_individual_id, p_nucc_taxonomy_code_id, p_state_id);
	
END;
$BODY$;

ALTER FUNCTION ndh.insert_practitioner(bigint, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character, character varying)
    OWNER TO ndh;
