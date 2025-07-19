ETL Specification: Translating NPPES into NDH
=====================

Context

The goal is to translate the raw NPI database known as NPPES into a more sophisticated and integrated database called NDH (National Directory of Healthcare). NDH consolidates multiple data sources, but NPPES is the core, and it is essential that NPPES be imported correctly.

NPI Types

There are three types of NPIs in the raw NPPES file:

 1. Organizational
 2. Individual
 3. Retired

Core Data Validation Expectations - Each of these should be a seperate InLaw class.

 1. Exclude Retired
 • After accounting for retired NPIs using a WHERE on the raw NPPES data, every remaining NPI should be one-to-one in the NDH npi table.
 2. Split Across Types
 • The number of records in organizational_npi and individual_npi should add up to the total number of records in ndh.npi.
 3. Record Set Consistency
 • Every NPI listed in ndh.organizational_npi should exist in the raw nppes data, and there should be the same number of tem
 • A left join of raw organizational NPIs to ndh.organizational_npi, followed by a WHERE IS NULL, should return zero rows, when joining in both directions
 • The same applies to individual_npi: Every individual NPI must be matched in the NDH target.
 4. Attribute-Level Sanity Checks
 • For the most part other attributes in NPPES normalize, and are not 1:1. But for those few things that are, they should be validated to be identical to the source data.

ETL Model: In-Law Classes

These expectations will be implemented as InLaw classes, where each class represents a single expectation.
