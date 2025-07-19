Populating NDH with normalized phone data
========

I would like to populate the NDH phone data (look in sql/create_table_sql/create_phone.sql)
with normalized phone data from multiple incoming data streams. To facilitate the mapping of phone numbers from these multiple data streams, I have
created a staging database in intake.staging_phone

There are multiple different sources for phone number data, but lets start with just NPPES.

In the main NPPES file (see nppes_main/npidata_pfile_20050523-20250608.create_table_postgres.sql) there are the fields:

* Provider_Business_Mailing_Address_Telephone_Number
* Provider_Business_Mailing_Address_Fax_Number
* Provider_Business_Practice_Location_Address_Telephone_Number
* Provider_Business_Practice_Location_Address_Fax_Number
* Authorized_Official_Telephone_Number

Note: in the main file, phone extensions are often mixed into the mail text field and will need to be extracted.

In the additional practice location files (here: nppes_pl/pl_pfile_20050523-20250608.create_table_postgres.sql) there are:

* provider_secondary_practice_address_telephone_number
* provider_secondary_practice_address_telephone_extension

Use ndh.PhoneTypeLUT to record the type of phone number, which should include:

* 1 - Mailing Processing Telephone
* 2 - Mailing Processing Fax
* 3 - Practice Location Telephone
* 4 - Practice Location Fax
* 5 - Authorized Official Phone

If ndh.PhoneTypeLUT is not populated already, the script should add this data.

All phones from the nppes_pl datasource will be Practice Location Telephones

I would like to use a post_import_script, using the plainerflow tools as described in AI_Instruction/PlainerflowTools.md

Do not create InLaw validation steps at this time.

Please place the code here: nppes_main/post_import_scripts/Step10_NormalizePhones.py

ndh is the destination schema for the phone numbers. intake should be the location of any intermediate tables you need to build. and nppes_raw is the schema of source data

when processing the nppes main file, please used the main_file_small table as a mechanism to testing code before running it on the larger table.

One you have added distinct records to the intake.staging_phone you should use python phonenumbers to convert all phone numbers to their phone_e164 values to enter into the ndh datasets.
Do not copy phone numbers that cannot be converted to proper phone numbers. But keep them in the staging database.

For now, do not worry if a phone is a US phone or not, but ensure that all phone numbers that go into the NDH data are clean numbers that follow E164 formatting.

We will later describe how to link phone numbers to NPI records. For now, simply import the phone numbers in a clean manner.
