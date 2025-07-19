
-- Organizations have lots of DBAs and brand names that require a many-to-one notation.. 
-- and we can define the whole concept of a higher level brand as a many-to-many name relationship..
-- If NUCC codes were reasonable, we could possibly do away with Organization Type as a seperate table.
-- But NUCC is so broken that I suspect in the future we are going to want to track data "just about SNFs"
-- JUst about Hospitals and just about FQHCs etc etc. Given that, having a org type that we control seems like an invaluable first step. 
-- Also want to clarify when I am talking about organizations that provide clinical care directly, as opposed to holding companies
-- which own clinical organizations but are not themselves clinical. Which strangely enough can also include payers.. 
-- TODO: discuss the clinical org, payer, and holding company question with Sarah and team. 
-- TODO: do we want to use vtin or vein? What exactly is our commitment level to using puns.

CREATE TABLE ndh.clinical_organization (
    id SERIAL PRIMARY KEY,
    clinical_organization_legal_name VARCHAR(200)   NOT NULL,
    authorized_official_individual_id INT   NOT NULL,
    organization_tin VARCHAR(10)   DEFAULT NULL,
    organization_vtin VARCHAR(50) DEFAULT NULL,
    organization_glief VARCHAR(300)  DEFAULT NULL,
    CONSTRAINT uc_organization_organization_vtin UNIQUE (
        organization_vtin
    )
);


CREATE TABLE ndh.clinical_orgname_type (
    id SERIAL PRIMARY KEY,
    orgname_type_description TEXT   NOT NULL,
    source_file TEXT   NOT NULL,
    source_field TEXT   NOT NULL,
    CONSTRAINT uc_orgname_type_orgname_description UNIQUE (
        orgname_type_description, source_file, source_field
    )
);

INSERT INTO ndh.clinical_orgname_type (orgname_type_description, source_file, source_field)
VALUES ('NPPES', 'main file', 'name_field');

INSERT INTO ndh.clinical_orgname_type (orgname_type_description, source_file, source_field)
VALUES ('NPPES', 'endpoint file', 'name_field');

INSERT INTO ndh.clinical_orgname_type (orgname_type_description, source_file, source_field)
VALUES ('NPPES', 'othername file', 'name_field');



CREATE TABLE ndh.orgname (
    id SERIAL PRIMARY KEY,
    clinical_organization_id INT   NOT NULL,
    clinical_organization_name VARCHAR(70)   NOT NULL,
    clinical_orgname_type_id INTEGER   NOT NULL
);

-- TODO should we label this as from PECOS?
CREATE TABLE ndh.assigning_npi (
    clinical_organization_id INT   NOT NULL,
    npi_id INT NOT NULL
);