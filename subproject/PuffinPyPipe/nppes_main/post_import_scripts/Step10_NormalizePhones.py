#!/usr/bin/env python3
"""
ETL Pipeline Step: Normalize NPPES Phone Numbers
Extracts phone numbers from NPPES data sources, normalizes them using phonenumbers library,
and populates staging and NDH tables for clean phone data management.
"""

import plainerflow
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle
import pandas as pd
import os
import sys

# Add the parent directory to the path to import PhoneNormalizer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from PhoneNormalizer import PhoneNormalizer


def main():
    """Main ETL pipeline execution"""
    
    # Control dry-run mode - start with True for testing
    is_just_print = False
    
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    # Define table references
    # Use small table for testing, main table for production
    # npi_table = 'main_file_small'  # Switch to 'main_file' for production
    npi_table = 'main_file'  # For production
    
    npi_main_DBTable = DBTable(schema='nppes_raw', table=npi_table)
    npi_pl_DBTable = DBTable(schema='nppes_raw', table='pl_file')
    staging_phone_DBTable = DBTable(schema='intake', table='staging_phone')
    phone_type_lut_DBTable = DBTable(schema='ndh', table='phone_type_lut')
    phone_number_DBTable = DBTable(schema='ndh', table='phone_number')
    phone_extension_DBTable = DBTable(schema='ndh', table='phone_extension')
    
    # Create SQL execution plan
    sql = FrostDict()
    
    # Phase 1: Setup PhoneTypeLUT
    sql['populate_phone_type_lut'] = f"""
    INSERT INTO {phone_type_lut_DBTable} (id, phone_type_description)
    VALUES 
        (1, 'Mailing Processing Telephone'),
        (2, 'Mailing Processing Fax'),
        (3, 'Practice Location Telephone'),
        (4, 'Practice Location Fax'),
        (5, 'Authorized Official Phone')
    ON CONFLICT (id) DO NOTHING;
    """
    
    # Phase 2: Extract phone data from NPPES main file - separate INSERT for each field
    
    # 2a: Business Mailing Address Telephone Numbers
    sql['extract_main_business_mailing_phone'] = f"""
    INSERT INTO {staging_phone_DBTable} 
    (raw_phone, source_file, is_fax_in_source, source_row, error_notes)
    SELECT 
        "Provider_Business_Mailing_Address_Telephone_Number" as raw_phone,
        'nppes_main' as source_file,
        FALSE as is_fax,
        ROW_NUMBER() OVER() as source_row,
        'Business Mailing Phone from main file' as error_notes
    FROM {npi_main_DBTable}
    WHERE "Provider_Business_Mailing_Address_Telephone_Number" IS NOT NULL 
    AND TRIM("Provider_Business_Mailing_Address_Telephone_Number") != ''
    ON CONFLICT (raw_phone, source_file, is_fax_in_source) DO NOTHING;
    """
    
    # 2b: Business Mailing Address Fax Numbers
    sql['extract_main_business_mailing_fax'] = f"""
    INSERT INTO {staging_phone_DBTable} 
    (raw_phone, source_file, is_fax_in_source, source_row, error_notes)
    SELECT 
        "Provider_Business_Mailing_Address_Fax_Number" as raw_phone,
        'nppes_main' as source_file,
        TRUE as is_fax,
        ROW_NUMBER() OVER() as source_row,
        'Business Mailing Fax from main file' as error_notes
    FROM {npi_main_DBTable}
    WHERE "Provider_Business_Mailing_Address_Fax_Number" IS NOT NULL 
    AND TRIM("Provider_Business_Mailing_Address_Fax_Number") != ''
    ON CONFLICT (raw_phone, source_file, is_fax_in_source) DO NOTHING;
    """
    
    # 2c: Business Practice Location Telephone Numbers
    sql['extract_main_practice_location_phone'] = f"""
    INSERT INTO {staging_phone_DBTable} 
    (raw_phone, source_file, is_fax_in_source, source_row, error_notes)
    SELECT 
        "Provider_Business_Practice_Location_Address_Telephone_Number" as raw_phone,
        'nppes_main' as source_file,
        FALSE as is_fax,
        ROW_NUMBER() OVER() as source_row,
        'Practice Location Phone from main file' as error_notes
    FROM {npi_main_DBTable}
    WHERE "Provider_Business_Practice_Location_Address_Telephone_Number" IS NOT NULL 
    AND TRIM("Provider_Business_Practice_Location_Address_Telephone_Number") != ''
    ON CONFLICT (raw_phone, source_file, is_fax_in_source) DO NOTHING;
    """
    
    # 2d: Business Practice Location Fax Numbers
    sql['extract_main_practice_location_fax'] = f"""
    INSERT INTO {staging_phone_DBTable} 
    (raw_phone, source_file, is_fax_in_source, source_row, error_notes)
    SELECT 
        "Provider_Business_Practice_Location_Address_Fax_Number" as raw_phone,
        'nppes_main' as source_file,
        TRUE as is_fax,
        ROW_NUMBER() OVER() as source_row,
        'Practice Location Fax from main file' as error_notes
    FROM {npi_main_DBTable}
    WHERE "Provider_Business_Practice_Location_Address_Fax_Number" IS NOT NULL 
    AND TRIM("Provider_Business_Practice_Location_Address_Fax_Number") != ''
    ON CONFLICT (raw_phone, source_file, is_fax_in_source) DO NOTHING;
    """
    
    # 2e: Authorized Official Telephone Numbers
    sql['extract_main_authorized_official_phone'] = f"""
    INSERT INTO {staging_phone_DBTable} 
    (raw_phone, source_file, is_fax_in_source, source_row, error_notes)
    SELECT 
        "Authorized_Official_Telephone_Number" as raw_phone,
        'nppes_main' as source_file,
        FALSE as is_fax,
        ROW_NUMBER() OVER() as source_row,
        'Authorized Official Phone from main file' as error_notes
    FROM {npi_main_DBTable}
    WHERE "Authorized_Official_Telephone_Number" IS NOT NULL 
    AND TRIM("Authorized_Official_Telephone_Number") != ''
    ON CONFLICT (raw_phone, source_file, is_fax_in_source) DO NOTHING;
    """
    
    # Phase 3: Extract phone data from NPPES practice location file - separate INSERT for each field
    
    # 3a: Secondary Practice Address Telephone Numbers (with extensions)
    sql['extract_pl_secondary_practice_phone'] = f"""
    INSERT INTO {staging_phone_DBTable} 
    (raw_phone, raw_phone_extension, source_file, is_fax_in_source, source_row, error_notes)
    SELECT 
        "provider_secondary_practice_address_telephone_number" as raw_phone,
        "provider_secondary_practice_address_telephone_extension" as raw_phone_extension,
        'nppes_pl_file' as source_file,
        FALSE as is_fax,
        ROW_NUMBER() OVER() as source_row,
        'Secondary Practice Phone from PL file' as error_notes
    FROM {npi_pl_DBTable}
    WHERE "provider_secondary_practice_address_telephone_number" IS NOT NULL 
    AND TRIM("provider_secondary_practice_address_telephone_number") != ''
    ON CONFLICT (raw_phone, source_file, is_fax_in_source) DO NOTHING;
    """
    
    # 3b: Practice Address Fax Numbers
    sql['extract_pl_practice_fax'] = f"""
    INSERT INTO {staging_phone_DBTable} 
    (raw_phone, source_file, is_fax_in_source, source_row, error_notes)
    SELECT 
        "provider_practice_address_fax_number" as raw_phone,
        'nppes_pl_file' as source_file,
        TRUE as is_fax,
        ROW_NUMBER() OVER() as source_row,
        'Practice Fax from PL file' as error_notes
    FROM {npi_pl_DBTable}
    WHERE "provider_practice_address_fax_number" IS NOT NULL 
    AND TRIM("provider_practice_address_fax_number") != ''
    ON CONFLICT (raw_phone, source_file, is_fax_in_source) DO NOTHING;
    """
    
    # Execute initial SQL setup and extraction
    print("About to run initial SQL setup and phone extraction")
    SQLoopcicle.run_sql_loop(
        sql_dict=sql,
        is_just_print=is_just_print,
        engine=alchemy_engine
    )
    
    if not is_just_print:
        # Phase 4: Process staging records with Python phonenumbers library
        print("Processing staging records with phonenumbers library...")
        
        # Read staging records for processing - only process records that haven't been normalized yet
        staging_query = f"""
        SELECT id, raw_phone, raw_phone_extension 
        FROM {staging_phone_DBTable} 
        WHERE phone_e164 IS NULL 
        AND is_normalized_success = FALSE
        """
        staging_df = pd.read_sql(staging_query, alchemy_engine)
        
        # Also get counts for reporting
        total_count_query = f"SELECT COUNT(*) as total FROM {staging_phone_DBTable}"
        processed_count_query = f"SELECT COUNT(*) as processed FROM {staging_phone_DBTable} WHERE phone_e164 IS NOT NULL"
        
        total_count = pd.read_sql(total_count_query, alchemy_engine).iloc[0]['total']
        processed_count = pd.read_sql(processed_count_query, alchemy_engine).iloc[0]['processed']
        
        print(f"Total records in staging: {total_count}")
        print(f"Previously processed: {processed_count}")
        print(f"Processing {len(staging_df)} new/unprocessed phone records...")
        
        # Process each record with progress indicator
        processed_count = 0
        for index, row in staging_df.iterrows():
            record_id = row['id']
            raw_phone = row['raw_phone']
            raw_extension = row['raw_phone_extension']
            
            # Extract extension from main phone text if not already provided
            if pd.isna(raw_extension) or not raw_extension:
                clean_phone, extracted_extension = PhoneNormalizer._extract_extension_from_text(raw_phone)
                if extracted_extension:
                    raw_extension = extracted_extension
                    raw_phone = clean_phone
            
            # Normalize the phone number
            e164_format, country_code, success, error_msg = PhoneNormalizer._normalize_phone_number(raw_phone)
            
            # Update staging record using SQLAlchemy text() for proper parameter binding
            from sqlalchemy import text
            update_sql = text(f"""
            UPDATE {staging_phone_DBTable} 
            SET 
                phone_e164 = :e164_format,
                country_code = :country_code,
                is_normalized_success = :success,
                raw_phone_extension = :raw_extension,
                error_notes = COALESCE(error_notes, '') || CASE WHEN :error_msg IS NOT NULL THEN '; ' || :error_msg ELSE '' END
            WHERE id = :record_id
            """)
            
            with alchemy_engine.connect() as conn:
                conn.execute(update_sql, {
                    'e164_format': e164_format,
                    'country_code': country_code,
                    'success': success,
                    'raw_extension': raw_extension,
                    'error_msg': error_msg,
                    'record_id': record_id
                })
                conn.commit()
            
            # Progress indicator: print '.' every 100 records, newline every 3000
            processed_count += 1
            if processed_count % 100 == 0:
                print('.', end='', flush=True)
            if processed_count % 3000 == 0:
                print(f' [{processed_count}/{len(staging_df)}]')
        
        # Print final newline if we didn't just print one
        if processed_count % 3000 != 0:
            print(f' [{processed_count}/{len(staging_df)}]')
        
        # Phase 6: Populate NDH tables with successfully normalized phones
        ndh_sql = FrostDict()
        
        # Insert distinct phone numbers
        ndh_sql['populate_ndh_phone_numbers'] = f"""
        INSERT INTO {phone_number_DBTable} (phone_number)
        SELECT DISTINCT phone_e164
        FROM {staging_phone_DBTable}
        WHERE is_normalized_success = TRUE 
        AND phone_e164 IS NOT NULL
        ON CONFLICT (phone_number) DO NOTHING;
        """
        
        # Insert distinct phone extensions
        ndh_sql['populate_ndh_phone_extensions'] = f"""
        INSERT INTO {phone_extension_DBTable} (phone_extension)
        SELECT DISTINCT raw_phone_extension
        FROM {staging_phone_DBTable}
        WHERE raw_phone_extension IS NOT NULL 
        AND TRIM(raw_phone_extension) != ''
        ON CONFLICT (phone_extension) DO NOTHING;
        """
        
        # Update staging records with NDH foreign keys
        ndh_sql['link_staging_to_ndh_phone_numbers'] = f"""
        UPDATE {staging_phone_DBTable} 
        SET ndh_PhoneNumber_id = pn.id
        FROM {phone_number_DBTable} pn
        WHERE {staging_phone_DBTable}.phone_e164 = pn.phone_number
        AND {staging_phone_DBTable}.is_normalized_success = TRUE;
        """
        
        ndh_sql['link_staging_to_ndh_phone_extensions'] = f"""
        UPDATE {staging_phone_DBTable} 
        SET ndh_PhoneExtension_id = pe.id
        FROM {phone_extension_DBTable} pe
        WHERE {staging_phone_DBTable}.raw_phone_extension = pe.phone_extension
        AND {staging_phone_DBTable}.raw_phone_extension IS NOT NULL;
        """
        
        print("Populating NDH tables with normalized phone data...")
        SQLoopcicle.run_sql_loop(
            sql_dict=ndh_sql,
            is_just_print=False,  # Execute NDH population
            engine=alchemy_engine
        )
        
        print("Phone normalization pipeline completed successfully!")
        
        # Print summary statistics
        summary_query = f"""
        SELECT 
            COUNT(*) as total_records,
            COUNT(CASE WHEN is_normalized_success = TRUE THEN 1 END) as successful_normalizations,
            COUNT(CASE WHEN is_normalized_success = FALSE THEN 1 END) as failed_normalizations,
            COUNT(CASE WHEN raw_phone_extension IS NOT NULL THEN 1 END) as records_with_extensions
        FROM {staging_phone_DBTable}
        """
        
        summary_df = pd.read_sql(summary_query, alchemy_engine)
        print("\nPipeline Summary:")
        print(f"Total records processed: {summary_df.iloc[0]['total_records']}")
        print(f"Successful normalizations: {summary_df.iloc[0]['successful_normalizations']}")
        print(f"Failed normalizations: {summary_df.iloc[0]['failed_normalizations']}")
        print(f"Records with extensions: {summary_df.iloc[0]['records_with_extensions']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas phonenumbers")
        raise
