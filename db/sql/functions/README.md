# Helper SQL Functions

## insert_practitioner
### Description
This function is a quick and dirty way to create a fake practitioner record. Note: This function does not populate address. It also only supports one value for each of the related fields. It can be made more comprehensive in a future version, if needed. 
### How to Run It
1. Ensure that you've executed the create function statement in insert_practitioner.sql
2. Ensure that the language_spoken and nucc_taxonomy_code that you'd like to use exist in their respective tables
3. Execute the following command, replacing the `<p_>` variables with values of your choosing: 
```
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
```
### Sample Execution
```
select insert_practitioner(9999999999, '999999999', 'F','1950-01-01','Testy','Test','Practitioner','','','en','test@test.com','207Q00000X','06','555-555-5555')
```
