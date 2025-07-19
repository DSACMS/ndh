Populating NDH NPI data
=========================

I would like to populate the three basic NPI tables in the ndh database found here sql/create_table_sql/create_npi.sql

The NPI record here: nppes_main/npidata_pfile_20050523-20250608.create_table_postgres.sql
is the datasource and it will be found under nppes_raw.main_file in the database.

See AI_Instruction/PlainerflowTools.md for the basics of building out a simple ETL pipeline by putting plainerflow scripts in the post_import_scripts directory of nppes_main.

An NPI comes in two flavors, dependant on the contents of the Entity_Type_Code variable. A 1 for an entity type code means that the provider is an individual. A doctor, nurse or some other kind of individual practicioner.
Every individual gets one and only one NPI.

An organization can have as many type 2 NPI records as they like. Organizational NPI records can also have sub-parts, which means they link back to themselves.
In the NDH model, we identify an organization has having one tax identifier, which we model as a VTIN, which is usually a hash of an EIN.

Later, we will try and associate the VTINS with specific Organizational EINs. Which means that when we create a record in the ndh.NPI_to_ClinicalOrganization table for each organizational NPI, we will simply use the link to ClinicalOrganization_id as NULL.
A later ETL will address that association.

Please read docs/nppes/NPPES_ReadMe_And_CodeValues.md to understand the overall structure of the NPPES files.
Confirm that the fields that I have exposed in the sql/create_table_sql/create_npi.sql core NDH tables are in fact the only ones connected one-to-one with the NPI, or with a personal NPI or with an organizational NPI.

Unlike the Organizations, please go ahead and populate the links to Individuals (look in sql/create_table_sql/create_individual.sql) for more.
For now, ignore the Individuals credentials. Do not import them at all. A later ETL will address this. Do not import the Provider_Credential_Text at all.

We do not have the email or SSN for the individuals in the NPI database for now. Please leave these fields NULL.

FYI, despite documentation to the contrary the "NPI" column in nppes_raw.main_file is a BIGINT. Similarly all of the dates have been converted to postgresql DATE fields.
Please inspect nppes_main/post_import_scripts/Step05_fix_column_types.py to see how this was accomplished. 

In order to calculate if an organizational NPI has a parent organizational NPI, you must search all of the organizational NPI records to see if therre is one and only one organizational NPI that has the value
in its Provider_Organization_Name_Legal_Business_Name as an organization that lists itself as a subpart in the "Is_Organization_Subpart" field as yes..
in its "Parent_Organization_LBN". Please remove special characters and spaces, and only consider letters and numbers after converting all letters to lowercase for this comparision. 

There is a database table called intake.wrongnpi (look in sql/create_table_sql/create_intake_wrongnpi.sql) that can be used to mark failures in the processing.

When a organizational subpart NPI does not have a parent with the same legal business name, or there are more than one non-subpart organizational NPIs with the same legal business name...
This should be logged in wrongnpi.

You should create Records in the Individual table for Authorized Officials. For now, every distinct individual record should get a new record in the database. 
This is wrong, but we will not be correcting it for some time. Do not try and deduplicate authorized officials, or try to link in Individuals that are aquired from the individual NPI records. 

Please add a field mapping to this document before you begin coding a solution.

The NPPES file is released every month. Subsequent runs of the script should update the information, rather than create completely new information. If nessecary, create new tables in the intake schema in order to support this use-case. 

## Data Field Mapping

### Source Data Structure
The source data comes from `nppes_raw.main_file` table, which contains the NPPES data after processing by `Step05_fix_column_types.py`. Key transformations applied:
- `NPI` column: Converted from VARCHAR(11) to BIGINT
- `Replacement_NPI` column: Converted from VARCHAR(11) to BIGINT (nullable)
- Date columns: Converted from VARCHAR to DATE format using MM/DD/YYYY pattern:
  - `Provider_Enumeration_Date`
  - `Last_Update_Date`
  - `NPI_Deactivation_Date`
  - `NPI_Reactivation_Date`
  - `Certification_Date`

### Target NDH Tables

#### 1. ndh.NPI Table Mapping
| NDH Field | Source Field | Data Type | Notes |
|-----------|--------------|-----------|-------|
| id | AUTO-GENERATED | BIGINT | Primary key, auto-increment |
| npi | NPI | BIGINT | Direct mapping, converted from VARCHAR |
| entity_type_code | Entity_Type_Code | SMALLINT | 1=Individual, 2=Organization |
| replacement_npi | Replacement_NPI | VARCHAR(11) | Nullable, converted from BIGINT back to VARCHAR for consistency |
| enumeration_date | Provider_Enumeration_Date | DATE | Converted from MM/DD/YYYY string |
| last_update_date | Last_Update_Date | DATE | Converted from MM/DD/YYYY string |
| deactivation_reason_code | NPI_Deactivation_Reason_Code | VARCHAR(3) | Direct mapping |
| deactivation_date | NPI_Deactivation_Date | DATE | Nullable, converted from MM/DD/YYYY string |
| reactivation_date | NPI_Reactivation_Date | DATE | Nullable, converted from MM/DD/YYYY string |
| certification_date | Certification_Date | DATE | Nullable, converted from MM/DD/YYYY string |

#### 2. ndh.NPI_to_Individual Table Mapping (Entity_Type_Code = 1)
| NDH Field | Source Field | Data Type | Notes |
|-----------|--------------|-----------|-------|
| id | AUTO-GENERATED | BIGINT | Primary key, auto-increment |
| NPI_id | NPI | INT | Foreign key to ndh.NPI.id |
| Individual_id | DERIVED | INT | Foreign key to ndh.Individual.id (created from provider name fields) |
| is_sole_proprietor | Is_Sole_Proprietor | BOOLEAN | Convert 'Y'/'N' to boolean |
| sex_code | Provider_Sex_Code | CHAR(1) | Direct mapping |

#### 3. ndh.NPI_to_ClinicalOrganization Table Mapping (Entity_Type_Code = 2)
| NDH Field | Source Field | Data Type | Notes |
|-----------|--------------|-----------|-------|
| id | AUTO-GENERATED | BIGINT | Primary key, auto-increment |
| NPI_id | NPI | BIGINT | Foreign key to ndh.NPI.id |
| ClinicalOrganization_id | NULL | INT | Set to NULL initially, populated by later ETL |
| PrimaryAuthorizedOfficial_Individual_id | DERIVED | INT | Foreign key to ndh.Individual.id (created from Authorized Official fields) |
| Parent_NPI_id | DERIVED | BIGINT | Calculated by matching Parent_Organization_LBN with Provider_Organization_Name_Legal_Business_Name |

#### 4. ndh.Individual Table Mapping

##### For Individual Providers (Entity_Type_Code = 1):
| NDH Field | Source Field | Data Type | Notes |
|-----------|--------------|-----------|-------|
| id | AUTO-GENERATED | SERIAL | Primary key, auto-increment |
| last_name | Provider_Last_Name_Legal_Name | VARCHAR(100) | Direct mapping |
| first_name | Provider_First_Name | VARCHAR(100) | Direct mapping |
| middle_name | Provider_Middle_Name | VARCHAR(21) | Direct mapping |
| name_prefix | Provider_Name_Prefix_Text | VARCHAR(6) | Direct mapping |
| name_suffix | Provider_Name_Suffix_Text | VARCHAR(6) | Direct mapping |
| email_address | NULL | VARCHAR(200) | Set to NULL (not available in NPPES) |
| SSN | NULL | VARCHAR(10) | Set to NULL (not available in NPPES) |

##### For Authorized Officials (Entity_Type_Code = 2):
| NDH Field | Source Field | Data Type | Notes |
|-----------|--------------|-----------|-------|
| id | AUTO-GENERATED | SERIAL | Primary key, auto-increment |
| last_name | Authorized_Official_Last_Name | VARCHAR(100) | Direct mapping |
| first_name | Authorized_Official_First_Name | VARCHAR(100) | Direct mapping |
| middle_name | Authorized_Official_Middle_Name | VARCHAR(21) | Direct mapping |
| name_prefix | Authorized_Official_Name_Prefix_Text | VARCHAR(6) | Direct mapping |
| name_suffix | Authorized_Official_Name_Suffix_Text | VARCHAR(6) | Direct mapping |
| email_address | NULL | VARCHAR(200) | Set to NULL (not available in NPPES) |
| SSN | NULL | VARCHAR(10) | Set to NULL (not available in NPPES) |

### Business Logic for Parent Organization Matching

For organizational NPIs (Entity_Type_Code = 2) where `Is_Organization_Subpart = 'Y'`:

1. **Normalize Legal Business Names**: Remove special characters and spaces, convert to lowercase for comparison
2. **Find Parent Match**: Search for organizational NPIs where:
   - `Is_Organization_Subpart = 'N'` (not a subpart)
   - Normalized `Provider_Organization_Name_Legal_Business_Name` matches normalized `Parent_Organization_LBN`
3. **Validation Rules**:
   - If exactly one match found: Set `Parent_NPI_id` to the matching NPI
   - If no matches or multiple matches found: Log error in `intake.wrongnpi` table
   - Error types: 'NO_PARENT' or 'MULTI_PARENT'

### Error Logging in intake.wrongnpi

| Field | Data Type | Usage |
|-------|-----------|-------|
| npi | BIGINT | The problematic NPI |
| error_type_string | VARCHAR(10) | 'NO_PARENT', 'MULTI_PARENT', or other error codes |
| reason_npi_is_wrong | TEXT | Detailed explanation of the issue |

### Fields NOT Imported (Per Instructions)

- `Provider_Credential_Text` - Explicitly excluded, will be handled by later ETL
- All taxonomy codes and license information - Not part of core NPI tables
- All "Other Provider Identifier" fields - Not part of core NPI tables  
- All address and phone fields - Not part of core NPI tables
- All "Provider_Other_*" name fields - Not part of core NPI tables

### Processing Order

1. **Phase 1**: Create all ndh.NPI records (both individual and organizational)
2. **Phase 2**: Create ndh.Individual records for individual providers
3. **Phase 3**: Create ndh.Individual records for authorized officials
4. **Phase 4**: Create ndh.NPI_to_Individual records for individual NPIs
5. **Phase 5**: Calculate parent relationships and create ndh.NPI_to_ClinicalOrganization records
6. **Phase 6**: Log any errors to intake.wrongnpi table
