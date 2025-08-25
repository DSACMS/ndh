--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Homebrew)
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: ndh; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA ndh;


--
-- Name: insert_practitioner(bigint, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character, character varying); Type: FUNCTION; Schema: ndh; Owner: -
--

CREATE FUNCTION ndh.insert_practitioner(p_npi bigint, p_ssn character varying, p_gender_code character varying, p_birth_date date, p_first_name character varying, p_middle_name character varying, p_last_name character varying, p_name_prefix character varying, p_name_suffix character varying, p_language_spoken_id character varying, p_email_address character varying, p_nucc_taxonomy_code_id character varying, p_state_id character, p_phone_number character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: address; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.address (
    id integer NOT NULL,
    barcode_delivery_code character varying(12),
    smarty_key character varying(10),
    address_us_id integer,
    address_international_id integer,
    address_nonstandard_id integer
);


--
-- Name: address_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: address_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.address_id_seq OWNED BY ndh.address.id;


--
-- Name: address_international; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.address_international (
    id integer NOT NULL,
    address_id integer NOT NULL,
    input_id character varying(36),
    country character varying(64),
    geocode character varying(4),
    local_language character varying(6),
    freeform character varying(512),
    address1 character varying(64),
    address2 character varying(64),
    address3 character varying(64),
    address4 character varying(64),
    organization character varying(64),
    locality character varying(64),
    administrative_area character varying(32),
    postal_code character varying(16),
    administrative_area_iso2 character varying(8),
    sub_administrative_area character varying(64),
    country_iso_3 character varying(3),
    premise character varying(64),
    premise_number character varying(64),
    thoroughfare character varying(64),
    latitude numeric(9,6),
    longitude numeric(9,6),
    geocode_precision character varying(32),
    max_geocode_precision character varying(32),
    address_format character varying(128),
    verification_status character varying(32),
    address_precision character varying(32),
    max_address_precision character varying(32)
);


--
-- Name: address_international_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.address_international_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: address_international_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.address_international_id_seq OWNED BY ndh.address_international.id;


--
-- Name: address_nonstandard; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.address_nonstandard (
    id integer NOT NULL,
    address_id integer NOT NULL,
    input_id character varying(36),
    input_index integer,
    candidate_index integer,
    addressee character varying(64),
    delivery_line_1 character varying(64),
    delivery_line_2 character varying(64),
    last_line character varying(64),
    address_type character varying(32),
    address_format character varying(128),
    raw_address text,
    latitude numeric(9,6),
    longitude numeric(9,6),
    notes text
);


--
-- Name: address_nonstandard_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.address_nonstandard_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: address_nonstandard_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.address_nonstandard_id_seq OWNED BY ndh.address_nonstandard.id;


--
-- Name: address_us; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.address_us (
    id integer NOT NULL,
    address_id integer NOT NULL,
    input_id character varying(36),
    input_index integer,
    candidate_index integer,
    addressee character varying(64),
    delivery_line_1 character varying(64),
    delivery_line_2 character varying(64),
    last_line character varying(64),
    delivery_point_barcode character varying(12),
    urbanization character varying(64),
    primary_number character varying(30),
    street_name character varying(64),
    street_predirection character varying(16),
    street_postdirection character varying(16),
    street_suffix character varying(16),
    secondary_number character varying(32),
    secondary_designator character varying(16),
    extra_secondary_number character varying(32),
    extra_secondary_designator character varying(16),
    pmb_designator character varying(16),
    pmb_number character varying(16),
    city_name character varying(64),
    default_city_name character varying(64),
    state_code character(2),
    zipcode character(5),
    plus4_code character varying(4),
    delivery_point character(2),
    delivery_point_check_digit character(1),
    record_type character(1),
    zip_type character varying(32),
    county_code character(5),
    ews_match character(5),
    carrier_route character(4),
    congressional_district character(2),
    building_default_indicator character(1),
    rdi character varying(12),
    elot_sequence character varying(4),
    elot_sort character varying(4),
    latitude numeric(9,6),
    longitude numeric(9,6),
    coordinate_license integer,
    geo_precision character varying(18),
    time_zone character varying(48),
    utc_offset numeric(4,2),
    dst character(5),
    dpv_match_code character varying(1),
    dpv_footnotes character varying(32),
    dpv_cmra character varying(1),
    dpv_vacant character varying(1),
    dpv_no_stat character varying(1),
    active character varying(1),
    footnotes character varying(24),
    lacslink_code character varying(2),
    lacslink_indicator character varying(1),
    suitelink_match character varying(5),
    enhanced_match character varying(64)
);


--
-- Name: address_us_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.address_us_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: address_us_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.address_us_id_seq OWNED BY ndh.address_us.id;


--
-- Name: clinical_credential; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.clinical_credential (
    id integer NOT NULL,
    acronym character varying(20) NOT NULL,
    name character varying(100),
    source_url character varying(250)
);


--
-- Name: clinical_credential_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.clinical_credential_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: clinical_credential_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.clinical_credential_id_seq OWNED BY ndh.clinical_credential.id;


--
-- Name: clinical_school; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.clinical_school (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    url character varying(500)
);


--
-- Name: clinical_school_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.clinical_school_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: clinical_school_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.clinical_school_id_seq OWNED BY ndh.clinical_school.id;


--
-- Name: fhir_address_use; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.fhir_address_use (
    id integer NOT NULL,
    value text NOT NULL
);


--
-- Name: fhir_address_type_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.fhir_address_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fhir_address_type_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.fhir_address_type_id_seq OWNED BY ndh.fhir_address_use.id;


--
-- Name: fhir_name_use; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.fhir_name_use (
    id integer NOT NULL,
    value character varying(50) NOT NULL
);


--
-- Name: fhir_name_type_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.fhir_name_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fhir_name_type_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.fhir_name_type_id_seq OWNED BY ndh.fhir_name_use.id;


--
-- Name: fhir_phone_system; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.fhir_phone_system (
    id integer NOT NULL,
    value character varying(20)
);


--
-- Name: fhir_phone_system_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.fhir_phone_system_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fhir_phone_system_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.fhir_phone_system_id_seq OWNED BY ndh.fhir_phone_system.id;


--
-- Name: fhir_phone_use; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.fhir_phone_use (
    id integer NOT NULL,
    value text NOT NULL
);


--
-- Name: fips_county; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.fips_county (
    id character varying(5) NOT NULL,
    name character varying(200) NOT NULL,
    fips_state_id character varying(2) NOT NULL
);


--
-- Name: fips_state; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.fips_state (
    id character(2) NOT NULL,
    name character varying(100) NOT NULL,
    abbreviation character(2) NOT NULL
);


--
-- Name: individual; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.individual (
    ssn character varying(10) DEFAULT NULL::character varying,
    gender_code character(1) DEFAULT NULL::bpchar,
    birth_date date,
    id uuid NOT NULL
);


--
-- Name: individual_to_address; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.individual_to_address (
    address_use_id integer NOT NULL,
    address_id integer NOT NULL,
    individual_id uuid NOT NULL
);


--
-- Name: individual_to_email_address; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.individual_to_email_address (
    email_address character varying(300) NOT NULL,
    individual_id uuid
);


--
-- Name: individual_to_language_spoken; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.individual_to_language_spoken (
    language_spoken_id character(2) NOT NULL,
    individual_id uuid NOT NULL
);


--
-- Name: individual_to_name; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.individual_to_name (
    last_name character varying(100),
    first_name character varying(100),
    middle_name character varying(21),
    prefix character varying(6),
    suffix character varying(6),
    fhir_name_use_id integer NOT NULL,
    effective_date date NOT NULL,
    end_date date,
    individual_id uuid NOT NULL
);


--
-- Name: individual_to_phone_number; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.individual_to_phone_number (
    fhir_phone_use_id integer NOT NULL,
    phone_number_id integer NOT NULL,
    extension character varying(10),
    fhir_phone_system_id integer,
    individual_id uuid NOT NULL
);


--
-- Name: language_spoken; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.language_spoken (
    id character(2) NOT NULL,
    value character varying(200)
);


--
-- Name: medicare_provider_type; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.medicare_provider_type (
    id integer NOT NULL,
    value character varying NOT NULL
);


--
-- Name: medicare_provider_type_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.medicare_provider_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: medicare_provider_type_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.medicare_provider_type_id_seq OWNED BY ndh.medicare_provider_type.id;


--
-- Name: npi; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.npi (
    npi bigint NOT NULL,
    entity_type_code smallint NOT NULL,
    replacement_npi bigint,
    enumeration_date date NOT NULL,
    last_update_date date NOT NULL,
    deactivation_reason_code character varying(3),
    deactivation_date date,
    reactivation_date date,
    certification_date date,
    CONSTRAINT npi_npi_check CHECK (((npi > 999999999) AND (npi < '10000000000'::bigint)))
);


--
-- Name: nucc_classification; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.nucc_classification (
    id integer NOT NULL,
    nucc_taxonomy_code_id character varying(10),
    display_name character varying(100),
    nucc_grouping_id integer
);


--
-- Name: nucc_classification_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.nucc_classification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nucc_classification_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.nucc_classification_id_seq OWNED BY ndh.nucc_classification.id;


--
-- Name: nucc_grouping; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.nucc_grouping (
    id integer NOT NULL,
    display_name character varying(100)
);


--
-- Name: nucc_group_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.nucc_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nucc_group_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.nucc_group_id_seq OWNED BY ndh.nucc_grouping.id;


--
-- Name: nucc_specialization; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.nucc_specialization (
    id integer NOT NULL,
    nucc_taxonomy_code_id character varying(10),
    display_name character varying(100),
    nucc_classification_id integer
);


--
-- Name: nucc_hierarchy; Type: VIEW; Schema: ndh; Owner: -
--

CREATE VIEW ndh.nucc_hierarchy AS
 SELECT "Grouping",
    "Classification",
    "Specialization",
    "Taxonomy Code"
   FROM ( SELECT g.display_name AS "Grouping",
            c.display_name AS "Classification",
            s.display_name AS "Specialization",
            s.nucc_taxonomy_code_id AS "Taxonomy Code"
           FROM ((ndh.nucc_specialization s
             LEFT JOIN ndh.nucc_classification c ON ((c.id = s.nucc_classification_id)))
             LEFT JOIN ndh.nucc_grouping g ON ((g.id = c.nucc_grouping_id)))
        UNION
         SELECT g.display_name AS "Grouping",
            c.display_name AS "Classification",
            ''::character varying AS "Specialization",
                CASE
                    WHEN (c.nucc_taxonomy_code_id IS NULL) THEN ''::character varying
                    ELSE c.nucc_taxonomy_code_id
                END AS "Taxonomy Code"
           FROM (ndh.nucc_classification c
             LEFT JOIN ndh.nucc_grouping g ON ((g.id = c.nucc_grouping_id)))
        UNION
         SELECT g.display_name AS "Grouping",
            ''::character varying AS "Classification",
            ''::character varying AS "Specialization",
            ''::character varying AS "Taxonomy Code"
           FROM ndh.nucc_grouping g) unnamed_subquery
  ORDER BY ROW("Grouping", "Classification", "Specialization");


--
-- Name: nucc_specialization_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.nucc_specialization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nucc_specialization_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.nucc_specialization_id_seq OWNED BY ndh.nucc_specialization.id;


--
-- Name: nucc_taxonomy_code; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.nucc_taxonomy_code (
    id character varying(10) NOT NULL,
    display_name text NOT NULL,
    definition text,
    notes text,
    certifying_board_name text,
    certifying_board_url text
);


--
-- Name: nucc_taxonomy_code_to_medicare_provider_type; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.nucc_taxonomy_code_to_medicare_provider_type (
    id integer NOT NULL,
    medicare_provider_type_id integer NOT NULL,
    nucc_taxonomy_code_id integer NOT NULL
);


--
-- Name: nucc_taxonomy_code_to_medicare_provider_type_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.nucc_taxonomy_code_to_medicare_provider_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nucc_taxonomy_code_to_medicare_provider_type_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.nucc_taxonomy_code_to_medicare_provider_type_id_seq OWNED BY ndh.nucc_taxonomy_code_to_medicare_provider_type.id;


--
-- Name: other_identifier_type; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.other_identifier_type (
    id integer NOT NULL,
    value text NOT NULL
);


--
-- Name: other_identifier_type_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.other_identifier_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: other_identifier_type_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.other_identifier_type_id_seq OWNED BY ndh.other_identifier_type.id;


--
-- Name: phone_number; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.phone_number (
    id integer NOT NULL,
    value character varying(20) NOT NULL
);


--
-- Name: phone_number_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.phone_number_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: phone_number_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.phone_number_id_seq OWNED BY ndh.phone_number.id;


--
-- Name: phone_type_id_seq; Type: SEQUENCE; Schema: ndh; Owner: -
--

CREATE SEQUENCE ndh.phone_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: phone_type_id_seq; Type: SEQUENCE OWNED BY; Schema: ndh; Owner: -
--

ALTER SEQUENCE ndh.phone_type_id_seq OWNED BY ndh.fhir_phone_use.id;


--
-- Name: provider; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.provider (
    npi bigint NOT NULL,
    individual_id uuid
);


--
-- Name: provider_to_clinical_credential; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.provider_to_clinical_credential (
    clinical_credential_id integer NOT NULL,
    receipt_date date,
    clinical_school_id integer,
    individual_id uuid NOT NULL
);


--
-- Name: provider_to_nucc_taxonomy_code; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.provider_to_nucc_taxonomy_code (
    nucc_taxonomy_code_id character varying(10) NOT NULL,
    is_primary boolean NOT NULL,
    individual_id uuid NOT NULL
);


--
-- Name: provider_to_other_identifier; Type: TABLE; Schema: ndh; Owner: -
--

CREATE TABLE ndh.provider_to_other_identifier (
    value character varying(21) NOT NULL,
    other_identifier_type_id integer NOT NULL,
    state_id character(2) NOT NULL,
    issuer_name character varying(81) NOT NULL,
    issue_date date,
    expiry_date date,
    individual_id uuid NOT NULL
);


--
-- Name: address id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address ALTER COLUMN id SET DEFAULT nextval('ndh.address_id_seq'::regclass);


--
-- Name: address_international id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_international ALTER COLUMN id SET DEFAULT nextval('ndh.address_international_id_seq'::regclass);


--
-- Name: address_nonstandard id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_nonstandard ALTER COLUMN id SET DEFAULT nextval('ndh.address_nonstandard_id_seq'::regclass);


--
-- Name: address_us id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_us ALTER COLUMN id SET DEFAULT nextval('ndh.address_us_id_seq'::regclass);


--
-- Name: clinical_credential id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.clinical_credential ALTER COLUMN id SET DEFAULT nextval('ndh.clinical_credential_id_seq'::regclass);


--
-- Name: clinical_school id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.clinical_school ALTER COLUMN id SET DEFAULT nextval('ndh.clinical_school_id_seq'::regclass);


--
-- Name: fhir_address_use id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_address_use ALTER COLUMN id SET DEFAULT nextval('ndh.fhir_address_type_id_seq'::regclass);


--
-- Name: fhir_name_use id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_name_use ALTER COLUMN id SET DEFAULT nextval('ndh.fhir_name_type_id_seq'::regclass);


--
-- Name: fhir_phone_system id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_phone_system ALTER COLUMN id SET DEFAULT nextval('ndh.fhir_phone_system_id_seq'::regclass);


--
-- Name: fhir_phone_use id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_phone_use ALTER COLUMN id SET DEFAULT nextval('ndh.phone_type_id_seq'::regclass);


--
-- Name: medicare_provider_type id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.medicare_provider_type ALTER COLUMN id SET DEFAULT nextval('ndh.medicare_provider_type_id_seq'::regclass);


--
-- Name: nucc_classification id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_classification ALTER COLUMN id SET DEFAULT nextval('ndh.nucc_classification_id_seq'::regclass);


--
-- Name: nucc_grouping id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_grouping ALTER COLUMN id SET DEFAULT nextval('ndh.nucc_group_id_seq'::regclass);


--
-- Name: nucc_specialization id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_specialization ALTER COLUMN id SET DEFAULT nextval('ndh.nucc_specialization_id_seq'::regclass);


--
-- Name: nucc_taxonomy_code_to_medicare_provider_type id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_taxonomy_code_to_medicare_provider_type ALTER COLUMN id SET DEFAULT nextval('ndh.nucc_taxonomy_code_to_medicare_provider_type_id_seq'::regclass);


--
-- Name: other_identifier_type id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.other_identifier_type ALTER COLUMN id SET DEFAULT nextval('ndh.other_identifier_type_id_seq'::regclass);


--
-- Name: phone_number id; Type: DEFAULT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.phone_number ALTER COLUMN id SET DEFAULT nextval('ndh.phone_number_id_seq'::regclass);


--
-- Name: address_international address_international_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_international
    ADD CONSTRAINT address_international_pkey PRIMARY KEY (id);


--
-- Name: address_nonstandard address_nonstandard_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_nonstandard
    ADD CONSTRAINT address_nonstandard_pkey PRIMARY KEY (id);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);


--
-- Name: address_us address_us_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_us
    ADD CONSTRAINT address_us_pkey PRIMARY KEY (id);


--
-- Name: clinical_credential clinical_credential_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.clinical_credential
    ADD CONSTRAINT clinical_credential_pkey PRIMARY KEY (id);


--
-- Name: clinical_school clinical_school_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.clinical_school
    ADD CONSTRAINT clinical_school_pkey PRIMARY KEY (id);


--
-- Name: fhir_address_use fhir_address_use_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_address_use
    ADD CONSTRAINT fhir_address_use_pkey PRIMARY KEY (id);


--
-- Name: fhir_name_use fhir_name_use_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_name_use
    ADD CONSTRAINT fhir_name_use_pkey PRIMARY KEY (id);


--
-- Name: fhir_phone_system fhir_phone_system_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_phone_system
    ADD CONSTRAINT fhir_phone_system_pkey PRIMARY KEY (id);


--
-- Name: fhir_phone_use fhir_phone_use_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_phone_use
    ADD CONSTRAINT fhir_phone_use_pkey PRIMARY KEY (id);


--
-- Name: fips_county fips_county_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fips_county
    ADD CONSTRAINT fips_county_pkey PRIMARY KEY (id);


--
-- Name: fips_state fips_state_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fips_state
    ADD CONSTRAINT fips_state_pkey PRIMARY KEY (id);


--
-- Name: individual individual_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual
    ADD CONSTRAINT individual_pkey PRIMARY KEY (id);


--
-- Name: individual_to_address individual_to_address_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_address
    ADD CONSTRAINT individual_to_address_pkey PRIMARY KEY (individual_id, address_id);


--
-- Name: individual_to_email_address individual_to_email_address_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_email_address
    ADD CONSTRAINT individual_to_email_address_pkey PRIMARY KEY (email_address);


--
-- Name: individual_to_language_spoken individual_to_language_spoken_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_language_spoken
    ADD CONSTRAINT individual_to_language_spoken_pkey PRIMARY KEY (individual_id, language_spoken_id);


--
-- Name: individual_to_name individual_to_name_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_name
    ADD CONSTRAINT individual_to_name_pkey PRIMARY KEY (individual_id, fhir_name_use_id, effective_date);


--
-- Name: provider_to_other_identifier individual_to_other_identifier_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_other_identifier
    ADD CONSTRAINT individual_to_other_identifier_pkey PRIMARY KEY (individual_id, state_id, value, other_identifier_type_id, issuer_name);


--
-- Name: individual_to_phone_number individual_to_phone_number_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_phone_number
    ADD CONSTRAINT individual_to_phone_number_pkey PRIMARY KEY (individual_id, phone_number_id, fhir_phone_use_id);


--
-- Name: language_spoken language_spoken_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.language_spoken
    ADD CONSTRAINT language_spoken_pkey PRIMARY KEY (id);


--
-- Name: medicare_provider_type medicare_provider_type_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.medicare_provider_type
    ADD CONSTRAINT medicare_provider_type_pkey PRIMARY KEY (id);


--
-- Name: npi npi_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.npi
    ADD CONSTRAINT npi_pkey PRIMARY KEY (npi);


--
-- Name: nucc_classification nucc_classification_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_classification
    ADD CONSTRAINT nucc_classification_pkey PRIMARY KEY (id);


--
-- Name: nucc_grouping nucc_grouping_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_grouping
    ADD CONSTRAINT nucc_grouping_pkey PRIMARY KEY (id);


--
-- Name: nucc_specialization nucc_specialization_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_specialization
    ADD CONSTRAINT nucc_specialization_pkey PRIMARY KEY (id);


--
-- Name: nucc_taxonomy_code nucc_taxonomy_code_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_taxonomy_code
    ADD CONSTRAINT nucc_taxonomy_code_pkey PRIMARY KEY (id);


--
-- Name: nucc_taxonomy_code_to_medicare_provider_type nucc_taxonomy_code_to_medicare_provider_type_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_taxonomy_code_to_medicare_provider_type
    ADD CONSTRAINT nucc_taxonomy_code_to_medicare_provider_type_pkey PRIMARY KEY (id);


--
-- Name: other_identifier_type other_identifier_type_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.other_identifier_type
    ADD CONSTRAINT other_identifier_type_pkey PRIMARY KEY (id);


--
-- Name: phone_number phone_number_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.phone_number
    ADD CONSTRAINT phone_number_pkey PRIMARY KEY (id);


--
-- Name: provider provider_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider
    ADD CONSTRAINT provider_pkey PRIMARY KEY (npi);


--
-- Name: provider_to_clinical_credential provider_to_clinical_credential_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_clinical_credential
    ADD CONSTRAINT provider_to_clinical_credential_pkey PRIMARY KEY (individual_id, clinical_credential_id);


--
-- Name: provider_to_nucc_taxonomy_code provider_to_nucc_taxonomy_code_pkey; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_nucc_taxonomy_code
    ADD CONSTRAINT provider_to_nucc_taxonomy_code_pkey PRIMARY KEY (individual_id, nucc_taxonomy_code_id);


--
-- Name: fhir_address_use uc_fhir_address_use_value; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_address_use
    ADD CONSTRAINT uc_fhir_address_use_value UNIQUE (value);


--
-- Name: fhir_name_use uc_fhir_name_use_value; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_name_use
    ADD CONSTRAINT uc_fhir_name_use_value UNIQUE (value);


--
-- Name: fhir_phone_use uc_fhir_phone_use_value; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fhir_phone_use
    ADD CONSTRAINT uc_fhir_phone_use_value UNIQUE (value);


--
-- Name: fips_state uc_fips_state_abbreviation; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fips_state
    ADD CONSTRAINT uc_fips_state_abbreviation UNIQUE (abbreviation);


--
-- Name: fips_state uc_fips_state_name; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fips_state
    ADD CONSTRAINT uc_fips_state_name UNIQUE (name);


--
-- Name: medicare_provider_type uc_medicare_provider_type_value; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.medicare_provider_type
    ADD CONSTRAINT uc_medicare_provider_type_value UNIQUE (value);


--
-- Name: other_identifier_type uc_other_identifier_type_value; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.other_identifier_type
    ADD CONSTRAINT uc_other_identifier_type_value UNIQUE (value);


--
-- Name: phone_number uc_phone_number_value; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.phone_number
    ADD CONSTRAINT uc_phone_number_value UNIQUE (value);


--
-- Name: provider uc_provider_individual_id; Type: CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider
    ADD CONSTRAINT uc_provider_individual_id UNIQUE (individual_id);


--
-- Name: individual_to_name_last_name_first_name_middle_name_idx; Type: INDEX; Schema: ndh; Owner: -
--

CREATE INDEX individual_to_name_last_name_first_name_middle_name_idx ON ndh.individual_to_name USING btree (last_name, first_name, middle_name);


--
-- Name: nucc_taxonomy_code_display_name_idx; Type: INDEX; Schema: ndh; Owner: -
--

CREATE INDEX nucc_taxonomy_code_display_name_idx ON ndh.nucc_taxonomy_code USING btree (display_name);


--
-- Name: address address_address_international_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address
    ADD CONSTRAINT address_address_international_id_fkey FOREIGN KEY (address_international_id) REFERENCES ndh.address_international(id);


--
-- Name: address address_address_nonstandard_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address
    ADD CONSTRAINT address_address_nonstandard_id_fkey FOREIGN KEY (address_nonstandard_id) REFERENCES ndh.address_nonstandard(id);


--
-- Name: address address_address_us_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address
    ADD CONSTRAINT address_address_us_id_fkey FOREIGN KEY (address_us_id) REFERENCES ndh.address_us(id);


--
-- Name: address_us address_us_county_code_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_us
    ADD CONSTRAINT address_us_county_code_fkey FOREIGN KEY (county_code) REFERENCES ndh.fips_county(id);


--
-- Name: address_us address_us_state_code_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.address_us
    ADD CONSTRAINT address_us_state_code_fkey FOREIGN KEY (state_code) REFERENCES ndh.fips_state(id);


--
-- Name: fips_county fips_county_fips_state_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.fips_county
    ADD CONSTRAINT fips_county_fips_state_id_fkey FOREIGN KEY (fips_state_id) REFERENCES ndh.fips_state(id);


--
-- Name: individual_to_address individual_to_address_address_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_address
    ADD CONSTRAINT individual_to_address_address_id_fkey FOREIGN KEY (address_id) REFERENCES ndh.address(id);


--
-- Name: individual_to_address individual_to_address_address_type_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_address
    ADD CONSTRAINT individual_to_address_address_type_id_fkey FOREIGN KEY (address_use_id) REFERENCES ndh.fhir_address_use(id) ON DELETE CASCADE;


--
-- Name: individual_to_address individual_to_address_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_address
    ADD CONSTRAINT individual_to_address_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.individual(id) ON DELETE CASCADE;


--
-- Name: individual_to_email_address individual_to_email_address_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_email_address
    ADD CONSTRAINT individual_to_email_address_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.individual(id) ON DELETE CASCADE;


--
-- Name: individual_to_language_spoken individual_to_language_spoken_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_language_spoken
    ADD CONSTRAINT individual_to_language_spoken_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.individual(id) ON DELETE CASCADE;


--
-- Name: individual_to_language_spoken individual_to_language_spoken_language_spoken_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_language_spoken
    ADD CONSTRAINT individual_to_language_spoken_language_spoken_id_fkey FOREIGN KEY (language_spoken_id) REFERENCES ndh.language_spoken(id) ON UPDATE CASCADE;


--
-- Name: individual_to_name individual_to_name_fhir_name_use_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_name
    ADD CONSTRAINT individual_to_name_fhir_name_use_id_fkey FOREIGN KEY (fhir_name_use_id) REFERENCES ndh.fhir_name_use(id);


--
-- Name: individual_to_name individual_to_name_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_name
    ADD CONSTRAINT individual_to_name_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.individual(id) ON DELETE CASCADE;


--
-- Name: provider_to_other_identifier individual_to_other_identifier_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_other_identifier
    ADD CONSTRAINT individual_to_other_identifier_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.individual(id) ON DELETE CASCADE;


--
-- Name: provider_to_other_identifier individual_to_other_identifier_other_identifier_type_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_other_identifier
    ADD CONSTRAINT individual_to_other_identifier_other_identifier_type_id_fkey FOREIGN KEY (other_identifier_type_id) REFERENCES ndh.other_identifier_type(id);


--
-- Name: provider_to_other_identifier individual_to_other_identifier_state_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_other_identifier
    ADD CONSTRAINT individual_to_other_identifier_state_id_fkey FOREIGN KEY (state_id) REFERENCES ndh.fips_state(id);


--
-- Name: individual_to_phone_number individual_to_phone_number_fhir_phone_system_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_phone_number
    ADD CONSTRAINT individual_to_phone_number_fhir_phone_system_id_fkey FOREIGN KEY (fhir_phone_system_id) REFERENCES ndh.fhir_phone_system(id);


--
-- Name: individual_to_phone_number individual_to_phone_number_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_phone_number
    ADD CONSTRAINT individual_to_phone_number_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.individual(id) ON DELETE CASCADE;


--
-- Name: individual_to_phone_number individual_to_phone_number_phone_number_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_phone_number
    ADD CONSTRAINT individual_to_phone_number_phone_number_id_fkey FOREIGN KEY (phone_number_id) REFERENCES ndh.phone_number(id);


--
-- Name: individual_to_phone_number individual_to_phone_number_phone_type_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.individual_to_phone_number
    ADD CONSTRAINT individual_to_phone_number_phone_type_id_fkey FOREIGN KEY (fhir_phone_use_id) REFERENCES ndh.fhir_phone_use(id);


--
-- Name: nucc_classification nucc_classification_nucc_grouping_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_classification
    ADD CONSTRAINT nucc_classification_nucc_grouping_id_fkey FOREIGN KEY (nucc_grouping_id) REFERENCES ndh.nucc_grouping(id);


--
-- Name: nucc_classification nucc_classification_nucc_taxonomy_code_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_classification
    ADD CONSTRAINT nucc_classification_nucc_taxonomy_code_id_fkey FOREIGN KEY (nucc_taxonomy_code_id) REFERENCES ndh.nucc_taxonomy_code(id);


--
-- Name: nucc_specialization nucc_specialization_nucc_classification_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_specialization
    ADD CONSTRAINT nucc_specialization_nucc_classification_id_fkey FOREIGN KEY (nucc_classification_id) REFERENCES ndh.nucc_classification(id);


--
-- Name: nucc_specialization nucc_specialization_nucc_taxonomy_code_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.nucc_specialization
    ADD CONSTRAINT nucc_specialization_nucc_taxonomy_code_id_fkey FOREIGN KEY (nucc_taxonomy_code_id) REFERENCES ndh.nucc_taxonomy_code(id);


--
-- Name: provider provider_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider
    ADD CONSTRAINT provider_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.individual(id) ON DELETE CASCADE;


--
-- Name: provider provider_npi_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider
    ADD CONSTRAINT provider_npi_fkey FOREIGN KEY (npi) REFERENCES ndh.npi(npi) ON DELETE CASCADE;


--
-- Name: provider_to_clinical_credential provider_to_clinical_credential_clinical_credential_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_clinical_credential
    ADD CONSTRAINT provider_to_clinical_credential_clinical_credential_id_fkey FOREIGN KEY (clinical_credential_id) REFERENCES ndh.clinical_credential(id) ON UPDATE CASCADE;


--
-- Name: provider_to_clinical_credential provider_to_clinical_credential_npi_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_clinical_credential
    ADD CONSTRAINT provider_to_clinical_credential_npi_fkey FOREIGN KEY (individual_id) REFERENCES ndh.provider(individual_id) ON UPDATE CASCADE;


--
-- Name: provider_to_nucc_taxonomy_code provider_to_nucc_taxonomy_code_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_nucc_taxonomy_code
    ADD CONSTRAINT provider_to_nucc_taxonomy_code_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.provider(individual_id) ON DELETE CASCADE;


--
-- Name: provider_to_nucc_taxonomy_code provider_to_nucc_taxonomy_code_nucc_taxonomy_code_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_nucc_taxonomy_code
    ADD CONSTRAINT provider_to_nucc_taxonomy_code_nucc_taxonomy_code_id_fkey FOREIGN KEY (nucc_taxonomy_code_id) REFERENCES ndh.nucc_taxonomy_code(id);


--
-- Name: provider_to_other_identifier provider_to_other_identifier_individual_id_fkey; Type: FK CONSTRAINT; Schema: ndh; Owner: -
--

ALTER TABLE ONLY ndh.provider_to_other_identifier
    ADD CONSTRAINT provider_to_other_identifier_individual_id_fkey FOREIGN KEY (individual_id) REFERENCES ndh.provider(individual_id);


--
-- PostgreSQL database dump complete
--

