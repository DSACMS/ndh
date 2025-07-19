# National Plan and Provider Enumeration System (NPPES)

Data Dissemination – Readme

Prepared For

## Centers for Medicare and Medicaid Services

Updated: February 1, 2025

This page intentionally left blank.


### 1 Introduction

Per the NPPES Data Dissemination Notice, CMS- 6060- N, posted on the Federal Register on May 30, 2007, FOIA-disclosable NPPES health care provider data will be provided in a downloadable file format.

As of 12/24/2024, two versions of these data files will be available as we transition to allow additional characters in all first name and legal business name fields. Version 1 (original) will provide only the original field lengths while Version 2 (v.2) will include the extended field lengths for all relevant fields.

### 1.1 About the Data File

Each NPI record (i.e., the record of an enumerated health care provider) is stored in the file as comma separated values (CSV) in a single row. A new row is created for each NPI record.

Every data value (between the commas) is enclosed within double quotes. For example,

"data value 1","data value  $2^{\prime \prime}$  ,"data value  $3^{\prime \prime}$  ,...

If the data value itself contains double quotes, these double quotes will be replaced by single quote to avoid confusing them the enclosing double quotes.

For example, if the original data value 1 is sam"ple da"ta 1 it will be converted to sam'ple da'ta 1 and stored in the file as depicted below.

"sam'ple da'ta 1","data value  $2^{\prime \prime}$  ,"data value  $3^{\prime \prime}$  ,...

This CSV file can be viewed using a variety of third- party software. Due to large volume of the data and the nature of the file, it is recommended that this file be handled by personnel with technical expertise.

The data file contains the fields identified in the NPPES Data Dissemination Notice and certain sub- fields related to those fields will be disclosed in the downloadable file. The sub- fields are:

1. For Other Provider Identifiers, the downloadable file will include the Issuer (the name of the health plan that issued the Other Provider Identifier), and the State (if furnished, the State of the Medicaid plan when Medicaid is the issuer).
2. For Taxonomy Code, the downloadable file will denote the Primary Taxonomy with the Primary Taxonomy Flag.
3. For the Other Name, the downloadable file will include the Other Name Prefix Text, the Other Name Suffix Text, and the Other Name Credentials text if any of that information was furnished by the provider.

Some health care providers reported their SSNs, IRS ITINs or EINs in sections of the NPI application that contain information that is required to be disclosed under FOIA. For example,

1. Providers who are individuals may have reported SSNs or IRS ITINs in FOIA-disclosable fields (such as in the "Other Provider Identifiers" or "License Number" fields).

2. An incorporated individual, when applying for an NPI for the corporation, may have reported his/her SSN as the EIN of the corporation.

CMS has urged health care providers to review their NPPES FOIA- disclosable data to ensure that it is correct and to remove any inappropriate or sensitive information that they may have reported in any of those fields that are "optional" (i.e., not required to be furnished) and /or replace the inappropriate or sensitive information that they may have reported in required fields with the appropriate information. If health care providers did not remove SSNs, IRS ITINs or EINs from FOIA- disclosable fields, CMS took action to not disclose any SSNs or IRS ITINs that were entered in those fields. CMS also took action to temporarily suppress reported EINs, even though they are disclosable under FOIA, because providers reported SSNs in the EIN field. After April 21, 2008, CMS will mask SSNs, IRS ITINs, and EINs when these numbers are entered in the Other Provider Identifier Number and License Number fields as follows: SSNs to “$$$$$$$$$”, IRS ITINs to “********” and EINs to “_________”. This action also includes the continued suppression of the EINs and the suppression of the Subpart Parent Organization TINs of all Organizations in the downloadable file. CMS expects to lift the suppression of EINs and Parent Organization TINs in the future.

### 1.2 Monthly Data File

Each month, two file versions will be available for download. These files will contain all of the FOIA- disclosable active provider data in NPPES. These files will replace the file provided the previous month and will contain:

1. FOIA-disclosable NPPES health care provider information for health care providers.  
2. Updates and changes to the FOIA-disclosable NPPES health care provider information of enumerated health care providers.

Two new file versions will be available for download 30 days after the availability of the initial files, and each month thereafter.

### 1.3 Weekly Data File

Each week, 2 file versions will be available for download. These files will contain only the new FOIA- disclosable NPPES provider data since the last weekly or monthly files were generated.

### 1.4 Contents of the Download Bundle

This data file is provided in a ZIP archive to compress the size and facilitate easier downloading. The contents of this ZIP file are listed below:

1. Data File  - File contains the FOIA-disclosable NPPES provider data.  - File Name: npidata_pfile_yyyymmdd-yyyymmdd.csv

2. Data Header File

- File contains a comma separated list of the column headers for the Data file- File Name: npidata_pfile_yyyyymmdd-yyyymmdd_FileHeader.csv

3. Other Name Reference File

- File contains additional Other Names associated with Type 2 NPIs- File Name: otherwise_pfile_yyyyymmdd-yyyymmdd.csv

4. Other Name Header File

- File contains a comma separated list of the column headers for the Other Names Reference File- File Name: otherwise_pfile_yyyyymmdd-yyyymmdd_FileHeader.csv

5. Practice Location Reference File

- File contains all of the non-primary Practice Locations associated with Type 1 and Type 2 NPIs.- File Name: p1_pfile_yyyyymmdd-yyyymmdd.csv

6. Practice Location Header File

- File contains all of the non-primary Practice Locations associated with Type 1 and Type 2 NPIs.- File Name: p1_pfile_yyyyymmdd-yyyymmdd_FileHeader.csv

7. Endpoint Reference Header File

- File contains all Endpoints associated with Type 1 and Type 2 NPIs- File Name: endpoint_pfile_yyyyymmdd-yyyymmdd.csv

8. Endpoint Reference Header File

- File contains all Endpoints associated with Type 1 and Type 2 NPIs- File Name: endpoint_pfile_yyyyymmdd-yyyymmdd_FileHeader.csv

9. Data Dissemination File - Code Values File

- File contains the Data Dissemination File 
- Code Values document that provides the descriptions of the various reference codes used in the Data file.- File Name: NPPES_Data_Dissemination_CodeValues.pdf

10. Data Dissemination File - Readme File

- This document, which provides the file layouts of the Data file and all of the reference files.- File Name: NPPES_Data_Dissemination_Readme.pdf

## 2 File Layouts

### 2.1 Data File Layout

Each line in the data file represents an NPI record. The following is the list of the column headers in the order as present in the data file.

Exhibit 2-1 Data File Layout  


<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>NPI</td>
		<td>10</td>
		<td>NUMBER</td>
		<td>NPI</td>
	</tr>
	<tr>
		<td>Entity Type Code</td>
		<td>1</td>
		<td>NUMBER</td>
		<td>Entity Type Code</td>
	</tr>
	<tr>
		<td>Replacement NPI</td>
		<td>10</td>
		<td>NUMBER</td>
		<td>Replacement NPI</td>
	</tr>
	<tr>
		<td>Employer Identification Number (EIN)</td>
		<td>9</td>
		<td>VARCHAR</td>
		<td>Employer Identification Number (EIN)</td>
	</tr>
	<tr>
		<td>Provider Organization Name (Legal Business Name)</td>
		<td>100</td>
		<td>VARCHAR</td>
		<td>Provider Organization Name (Legal Business Name)</td>
	</tr>
	<tr>
		<td>Provider Last Name (Legal Name)</td>
		<td>35</td>
		<td>VARCHAR</td>
		<td>Provider Last Name (Legal Name)</td>
	</tr>
	<tr>
		<td>Provider First Name</td>
		<td>35</td>
		<td>VARCHAR</td>
		<td>Provider First Name</td>
	</tr>
	<tr>
		<td>Provider Middle Name</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Middle Name</td>
	</tr>
	<tr>
		<td>Provider Name Prefix Text</td>
		<td>5</td>
		<td>VARCHAR</td>
		<td>Provider Name Prefix Text</td>
	</tr>
	<tr>
		<td>Provider Name Suffix Text</td>
		<td>5</td>
		<td>VARCHAR</td>
		<td>Provider Name Suffix Text</td>
	</tr>
	<tr>
		<td>Provider Credential Text</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Credential Text</td>
	</tr>
	<tr>
		<td>Provider Other Organization Name</td>
		<td>100</td>
		<td>VARCHAR</td>
		<td>Provider Other Organization Name</td>
	</tr>
	<tr>
		<td>Provider Other Organization Name Type Code</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td>Provider Other Organization Name Type Code</td>
	</tr>
	<tr>
		<td>Provider Other Last Name</td>
		<td>35</td>
		<td>VARCHAR</td>
		<td>Provider Other Last Name</td>
	</tr>
	<tr>
		<td>Provider Other First Name</td>
		<td>35</td>
		<td>VARCHAR</td>
		<td>Provider Other First Name</td>
	</tr>
	<tr>
		<td>Provider Other Middle Name</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Other Middle Name</td>
	</tr>
	<tr>
		<td>Provider Other Name Prefix Text</td>
		<td>5</td>
		<td>VARCHAR</td>
		<td>Provider Other Name Prefix Text</td>
	</tr>
	<tr>
		<td>Provider Other Name Suffix Text</td>
		<td>5</td>
		<td>VARCHAR</td>
		<td>Provider Other Name Suffix Text</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Provider Other Credential Text</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Other Name Credential Text</td>
	</tr>
	<tr>
		<td>Provider Other Last Name Type Code</td>
		<td>1</td>
		<td>NUMBER</td>
		<td>Provider Other Last Name Type Code</td>
	</tr>
	<tr>
		<td>Provider First Line Business Mailing Address</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Provider First Line Business Mailing Address</td>
	</tr>
	<tr>
		<td>Provider Second Line Business Mailing Address</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Provider Second Line Business Mailing Address</td>
	</tr>
	<tr>
		<td>Provider Business Mailing Address City Name</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Provider Business Mailing Address City Name</td>
	</tr>
	<tr>
		<td>Provider Business Mailing Address State Name</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Provider Business Mailing Address State Name</td>
	</tr>
	<tr>
		<td>Provider Business Mailing Address Postal Code</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Mailing Address Postal Code</td>
	</tr>
	<tr>
		<td>Provider Business Mailing Address Country Code (If outside U.S.)</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider Business Mailing Address Country Code (If outside U.S.)</td>
	</tr>
	<tr>
		<td>Provider Business Mailing Address Telephone Number</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Mailing Address Telephone Number</td>
	</tr>
	<tr>
		<td>Provider Business Mailing Address Fax Number</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Mailing Address Fax Number</td>
	</tr>
	<tr>
		<td>Provider First Line Business Practice Location Address</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Provider First Line Business Location Address</td>
	</tr>
	<tr>
		<td>Provider Second Line Business Practice Location Address</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Provider Second Line Business Location Address</td>
	</tr>
	<tr>
		<td>Provider Business Practice Location Address City Name</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address City Name</td>
	</tr>
	<tr>
		<td>Provider Business Practice Location Address State Name</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address State Name</td>
	</tr>
	<tr>
		<td>Provider Business Practice Location Address Postal Code</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Postal Code</td>
	</tr>
	<tr>
		<td>Provider Business Practice Location Address Country Code (If outside U.S.)</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Country Code (If outside U.S.)</td>
	</tr>
	<tr>
		<td>Provider Business Practice Location Address Telephone Number</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Telephone Number</td>
	</tr>
	<tr>
		<td>Provider Business Practice Location Address Fax Number</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Fax Number</td>
	</tr>
	<tr>
		<td>Provider Enumeration Date</td>
		<td>10 (MM/DD/YYYY)</td>
		<td>DATE</td>
		<td>Provider Enumeration Date</td>
	</tr>
	<tr>
		<td>Last Update Date</td>
		<td>10 (MM/DD/YYYY)</td>
		<td>DATE</td>
		<td>Last Update Date</td>
	</tr>
	<tr>
		<td>NPI Deactivation Reason Code</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>NPI Deactivation Reason Code</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>NPI Deactivation Date</td>
		<td>10 (MM/DD/YYYY)</td>
		<td>DATE</td>
		<td>NPI Deactivation Date</td>
	</tr>
	<tr>
		<td>NPI Reactivation Date</td>
		<td>10 (MM/DD/YYYY)</td>
		<td>DATE</td>
		<td>NPI Reactivation Date</td>
	</tr>
	<tr>
		<td>Provider Sex Code</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td>Provider Sex Code</td>
	</tr>
	<tr>
		<td>Authorized Official Last Name</td>
		<td>35</td>
		<td>VARCHAR</td>
		<td>Authorized Official Last Name</td>
	</tr>
	<tr>
		<td>Authorized Official First Name</td>
		<td>35</td>
		<td>VARCHAR</td>
		<td>Authorized Official First Name</td>
	</tr>
	<tr>
		<td>Authorized Official Middle Name</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Authorized Official Middle Name</td>
	</tr>
	<tr>
		<td>Authorized Official Title or Position</td>
		<td>35</td>
		<td>VARCHAR</td>
		<td>Authorized Official Title or Position</td>
	</tr>
	<tr>
		<td>Authorized Official Telephone Number</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Authorized Official Telephone Number</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_1</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_1</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_1</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_1</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_2</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_2</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_2</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_2</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_3</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_3</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_3</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_3</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_4</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_4</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_4</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_4</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_5</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_5</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_5</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_5</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_6</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_6</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_6</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_6</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_7</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_7</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_7</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_7</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_8</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_8</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_8</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_8</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_9</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_9</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_9</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_9</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_10</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_10</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_10</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_10</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_11</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_11</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_11</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_11</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_12</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_12</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_12</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_12</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_13</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_13</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_13</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_13</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_14</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_14</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_14</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_14</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Code_15</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Code</td>
	</tr>
	<tr>
		<td>Provider License Number_15</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider License Number</td>
	</tr>
	<tr>
		<td>Provider License Number State Code_15</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider License Number State Code</td>
	</tr>
	<tr>
		<td>Healthcare Provider Primary Taxonomy Switch_15</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_1</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_1</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_1</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_1</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_2</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_2</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_2</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_2</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_3</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_3</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_3</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_3</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_4</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_4</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_4</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_4</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_5</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_5</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_5</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_5</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_6</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_6</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_6</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_6</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier_7</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_7</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_7</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_7</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_8</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_8</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_8</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_8</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_9</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_9</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_9</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_9</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_10</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_10</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_10</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_10</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_11</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_11</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_11</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_11</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_12</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_12</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_12</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_12</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_13</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_13</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_13</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_13</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_14</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_14</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_14</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_14</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_15</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_15</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_15</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_15</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_16</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_16</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_16</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_16</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_17</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_17</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_17</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_17</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_18</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_18</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_18</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_18</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_19</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_19</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_19</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_19</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_20</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_20</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_20</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_20</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_21</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_21</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_21</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_21</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_22</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_22</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_22</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_22</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_23</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_23</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_23</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_23</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_24</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_24</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_24</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_24</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_25</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_25</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_25</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_25</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_26</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_26</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_26</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_26</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_27</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_27</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_27</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_27</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_28</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_28</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_28</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_28</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_29</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_29</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_29</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_29</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier_30</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_30</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_30</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_30</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_31</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_31</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_31</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_31</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_32</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_32</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_32</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_32</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_33</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_33</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_33</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_33</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_34</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_34</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_34</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_34</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_35</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_35</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_35</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_35</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_36</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_36</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_36</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_36</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_37</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_37</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_37</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_37</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_38</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_38</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_38</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_38</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_39</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_39</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_39</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_39</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_40</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_40</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_40</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_40</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_41</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_41</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_41</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_41</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_42</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_42</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_42</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_42</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_43</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_43</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_43</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_43</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_44</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_44</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_44</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_44</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_45</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_45</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_45</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_45</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_46</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_46</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_46</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_46</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_47</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_47</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_47</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_47</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_48</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_48</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_48</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_48</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_49</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_49</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_49</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_49</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier_50</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier</td>
	</tr>
	<tr>
		<td>Other Provider Identifier Type Code_50</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Other Provider Identifier Type Code</td>
	</tr>
	<tr>
		<td>Other Provider Identifier State_50</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Other Provider Identifier Issue_50</td>
		<td>80</td>
		<td>VARCHAR</td>
		<td></td>
	</tr>
	<tr>
		<td>Is Sole Proprietor</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td>Provider Sole Proprietor Flag</td>
	</tr>
	<tr>
		<td>Is Organization Subpart</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td>Provider Organization Subpart Flag</td>
	</tr>
	<tr>
		<td>Parent Organization LBN</td>
		<td>100</td>
		<td>VARCHAR</td>
		<td>Provider Organization Subpart Legal Business Name</td>
	</tr>
	<tr>
		<td>Parent Organization TIN</td>
		<td>9</td>
		<td>VARCHAR</td>
		<td>Provider Organization Subpart TIN</td>
	</tr>
	<tr>
		<td>Authorized Official Name Prefix Text</td>
		<td>5</td>
		<td>VARCHAR</td>
		<td>Authorized Official Name Prefix Text</td>
	</tr>
	<tr>
		<td>Authorized Official Name Suffix Text</td>
		<td>5</td>
		<td>VARCHAR</td>
		<td>Authorized Official Name Suffix Text</td>
	</tr>
	<tr>
		<td>Authorized Official Credential Text</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Authorized Official Credential Text</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_1</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_2</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_3</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_4</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_5</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_6</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_7</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_8</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_9</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_10</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_11</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_12</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_13</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_14</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Healthcare Provider Taxonomy Group_15</td>
		<td>10</td>
		<td>VARCHAR</td>
		<td>Healthcare Provider Taxonomy Group</td>
	</tr>
	<tr>
		<td>Certification Date</td>
		<td>10 (MM/DD/YYYY)</td>
		<td>DATE</td>
		<td>Certification Date</td>
	</tr>
</table>

### 2.2 Other Name Reference File

NPPES now collects multiple Other Names associated with Type 2 NPIs.

Each line in the Other Name Reference File represents an Other Name associated with an NPI record. The following is the list of the column headers in the order as they are present in the Other Name Reference file.

Exhibit 2-2 Other Name Reference File Layout  

<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>NPI</td>
		<td>10</td>
		<td>NUMBER</td>
		<td>NPI</td>
	</tr>
	<tr>
		<td>Provider Other Organization Name</td>
		<td>100</td>
		<td>VARCHAR</td>
		<td>Provider Other Organization Name</td>
	</tr>
	<tr>
		<td>Provider Other Organization Name Type Code</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td>Provider Other Organization Name Type Code</td>
	</tr>
</table>

### 2.3 Practice Location Reference File

NPPES now collects multiple Practice Location associated with Type 1 and Type 2 NPIs. The Data File contains the first Primary Practice Location, and the Practice Location Reference File will contain all of the non- primary Practice Locations.

Each line in the Practice Location Reference File represents a Practice Location Address associated with an NPI record. The following is the list of the column headers in the order as they are present in the Practice Location Reference file.

Exhibit 2-3 Practice Location Reference File Layout  


<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>NPI</td>
		<td>10</td>
		<td>NUMBER</td>
		<td>NPI</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address- Address Line 1</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Provider First Line Business Location Address</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address- Address Line 2</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Provider Second Line Business Location Address</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address - City Name</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address City Name</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address - State Name</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address State Name</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address - Postal Code</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Postal Code</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address - Country Code (If outside U.S.)</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Country Code (If outside U.S.)</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address - Telephone Number</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Telephone Number</td>
	</tr>
	<tr>
		<td>Provider Secondary Practice Location Address - Telephone Extension</td>
		<td>5</td>
		<td>VARCHAR</td>
		<td>Added with DUA #18577</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Provider Practice Location Address - Fax Number</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Provider Business Location Address Fax Number</td>
	</tr>
</table>

### 2.4 Endpoint Reference File

NPPES now collects Endpoints associated with NPIs. The Endpoint Reference File contains allof the Endpoints associated with each NPI. Each line in the Endpoint Reference File represents a single Endpoint associated with an NPI record. The following is the list of the column headers in the order as they are present in the Endpoint Reference file.

Exhibit 2-4 Endpoint Reference File Layout  



<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>NPI</td>
		<td>10</td>
		<td>NUMBER</td>
		<td>NPI</td>
	</tr>
	<tr>
		<td>Endpoint Type</td>
		<td>50</td>
		<td>VARCHAR</td>
		<td>Endpoint Type</td>
	</tr>
	<tr>
		<td>Endpoint Type Description</td>
		<td>255</td>
		<td>VARCHAR</td>
		<td>Endpoint Type Full Description</td>
	</tr>
	<tr>
		<td>Endpoint</td>
		<td>1000</td>
		<td>VARCHAR</td>
		<td>Endpoint</td>
	</tr>
	<tr>
		<td>Affiliation</td>
		<td>1</td>
		<td>VARCHAR</td>
		<td>Endpoint Affiliated to another Organization Y or N</td>
	</tr>
	<tr>
		<td>Endpoint Description</td>
		<td>1000</td>
		<td>VARCHAR</td>
		<td>Endpoint Description</td>
	</tr>
	<tr>
		<td>Affiliation Legal Business Name</td>
		<td>100</td>
		<td>VARCHAR</td>
		<td>Legal Business Name (LBN) of the Affiliation the Endpoint is associated with.</td>
	</tr>
	<tr>
		<td>Use Code</td>
		<td>25</td>
		<td>VARCHAR</td>
		<td>Endpoint Use</td>
	</tr>
	<tr>
		<td>Use Description</td>
		<td>100</td>
		<td>VARCHAR</td>
		<td>Endpoint Use Description</td>
	</tr>
	<tr>
		<td>Other Use Description</td>
		<td>200</td>
		<td>VARCHAR</td>
		<td>Endpoint Use Description when Use of “Other”</td>
	</tr>
	<tr>
		<td>Content Type</td>
		<td>25</td>
		<td>VARCHAR</td>
		<td>Endpoint Content Type</td>
	</tr>
	<tr>
		<td>Content Description</td>
		<td>100</td>
		<td>VARCHAR</td>
		<td>Endpoint Content Type Description</td>
	</tr>
	<tr>
		<td>Other Content Description</td>
		<td>200</td>
		<td>VARCHAR</td>
		<td>Endpoint Content Description when Content Type of “Other”</td>
	</tr>
	<tr>
		<td>Affiliation Address Line One</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Endpoint Location Address – Address Line 1</td>
	</tr>
</table>
<table>
	<tr>
		<td>Column Name</td>
		<td>Max Length</td>
		<td>Data Type</td>
		<td>Corresponding Field in the Data Dissemination Notice</td>
	</tr>
	<tr>
		<td>Affiliation Address Line Two</td>
		<td>55</td>
		<td>VARCHAR</td>
		<td>Endpoint Location Address – Address Line 2</td>
	</tr>
	<tr>
		<td>Affiliation Address City</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Endpoint Location Address – City Name</td>
	</tr>
	<tr>
		<td>Affiliation Address State</td>
		<td>40</td>
		<td>VARCHAR</td>
		<td>Endpoint Location Address – State Name</td>
	</tr>
	<tr>
		<td>Affiliation Address Country</td>
		<td>2</td>
		<td>VARCHAR</td>
		<td>Endpoint Location Address - Country Code of the (if outside U.S.)</td>
	</tr>
	<tr>
		<td>Affiliation Address Line Postal Code</td>
		<td>20</td>
		<td>VARCHAR</td>
		<td>Endpoint Location Address – Postal Code</td>
	</tr>
</table>
