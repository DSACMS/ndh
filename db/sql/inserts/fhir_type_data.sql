--
-- Data for Name: fhir_address_use; Type: TABLE DATA; Schema: ndh; Owner: -
--

INSERT INTO ndh.fhir_address_use VALUES (1, 'home');
INSERT INTO ndh.fhir_address_use VALUES (2, 'work');
INSERT INTO ndh.fhir_address_use VALUES (3, 'temp');
INSERT INTO ndh.fhir_address_use VALUES (4, 'old');
INSERT INTO ndh.fhir_address_use VALUES (5, 'billing');


--
-- Data for Name: fhir_name_use; Type: TABLE DATA; Schema: ndh; Owner: -
--

INSERT INTO ndh.fhir_name_use VALUES (1, 'usual');
INSERT INTO ndh.fhir_name_use VALUES (2, 'official');
INSERT INTO ndh.fhir_name_use VALUES (3, 'temp');
INSERT INTO ndh.fhir_name_use VALUES (4, 'nickname');
INSERT INTO ndh.fhir_name_use VALUES (5, 'anonymous');
INSERT INTO ndh.fhir_name_use VALUES (6, 'old');
INSERT INTO ndh.fhir_name_use VALUES (7, 'maiden');


--
-- Data for Name: fhir_phone_system; Type: TABLE DATA; Schema: ndh; Owner: -
--

INSERT INTO ndh.fhir_phone_system VALUES (1, 'phone');
INSERT INTO ndh.fhir_phone_system VALUES (2, 'fax');
INSERT INTO ndh.fhir_phone_system VALUES (3, 'pager');
INSERT INTO ndh.fhir_phone_system VALUES (4, 'sms');
INSERT INTO ndh.fhir_phone_system VALUES (5, 'other');


--
-- Data for Name: fhir_phone_use; Type: TABLE DATA; Schema: ndh; Owner: -
--

INSERT INTO ndh.fhir_phone_use VALUES (1, 'home');
INSERT INTO ndh.fhir_phone_use VALUES (2, 'work');
INSERT INTO ndh.fhir_phone_use VALUES (3, 'temp');
INSERT INTO ndh.fhir_phone_use VALUES (4, 'old');
INSERT INTO ndh.fhir_phone_use VALUES (5, 'mobile');

--
-- Data for Name: other_identifier_type; Type: TABLE DATA; Schema: ndh; Owner: -
--

INSERT INTO ndh.other_identifier_type VALUES (1, 'OTHER');
INSERT INTO ndh.other_identifier_type VALUES (2, 'MEDICARE UPIN');
INSERT INTO ndh.other_identifier_type VALUES (4, 'MEDICARE ID-TYPE UNSPECIFIED');
INSERT INTO ndh.other_identifier_type VALUES (5, 'MEDICAID');
INSERT INTO ndh.other_identifier_type VALUES (6, 'MEDICARE OSCAR/CERTIFICATION');
INSERT INTO ndh.other_identifier_type VALUES (7, 'MEDICARE NSC');
INSERT INTO ndh.other_identifier_type VALUES (8, 'MEDICARE PIN');