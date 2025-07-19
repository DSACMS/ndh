#!/usr/bin/env python3
"""
Step50_simple_clean_output.py

This script cleans the org_to_npi.csv file by:
1. Filtering for valid HTTPS URLs and 10-digit NPI numbers
2. Checking if the base domain of each URL is responsive
3. Outputting clean data to a new CSV file

Usage:
    python Step50_simple_clean_output.py --input_file data/output_data/normalized_csv_files/org_to_npi.csv --output_file data/output_data/clean_npi_to_org_fhir_url.csv
"""

import argparse
import csv
import re
import requests
from urllib.parse import urlparse
from typing import List, Tuple, Set
import time
import logging
import urllib3.exceptions

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataCleaner:
    """Class for cleaning org_to_npi CSV data"""
    
    @staticmethod
    def parse_arguments():
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description='Clean org_to_npi CSV data')
        parser.add_argument('--input_file', required=True, help='Path to input CSV file')
        parser.add_argument('--output_file', required=True, help='Path to output CSV file')
        return parser.parse_args()
    
    @staticmethod
    def is_valid_npi(*, npi_value: str) -> bool:
        """Check if NPI is a valid 10-digit number"""
        if not npi_value or npi_value.strip() == '':
            return False
        
        # Remove any whitespace
        npi_clean = npi_value.strip()
        
        # Check if it's exactly 10 digits
        return bool(re.match(r'^\d{10}$', npi_clean))
    
    @staticmethod
    def is_valid_https_url(*, url: str) -> bool:
        """Check if URL starts with https://"""
        if not url or url.strip() == '':
            return False
        
        return url.strip().startswith('https://')
    
    @staticmethod
    def extract_base_domain(*, url: str) -> str:
        """Extract base domain from URL (e.g., https://example.com/path -> https://example.com/)"""
        try:
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}/"
        except Exception as e:
            logger.warning(f"Failed to parse URL {url}: {e}")
            return ""
    
    @staticmethod
    def is_domain_responsive(*, base_domain: str, timeout: int = 10) -> bool:
        """Check if domain is responsive (returns 200, 300, or 400 status codes)"""
        try:
            response = requests.get(base_domain, timeout=timeout, allow_redirects=True)
            # Accept 200, 300, and 400 status codes as responsive
            return 200 <= response.status_code < 500
        except urllib3.exceptions.HeaderParsingError as e:
            # Custom headers are fine at this stage - consider domain responsive
            logger.info(f"Domain {base_domain} has custom headers but is responsive: {e}")
            return True
        except Exception as e:
            # Catch any other exceptions including HeaderParsingError that might bubble up
            if "HeaderParsingError" in str(e) or "MissingHeaderBodySeparatorDefect" in str(e):
                logger.info(f"Domain {base_domain} has custom headers but is responsive: {e}")
                return True
            logger.warning(f"Domain {base_domain} not responsive: {e}")
            return False
    
    @staticmethod
    def load_candidate_data(*, input_file_path: str) -> List[Tuple[str, str]]:
        """Load candidate data from CSV file that meets basic criteria"""
        candidates = []
        
        try:
            with open(input_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    org_id = row.get('org_id', '').strip()
                    npi_value = row.get('npi_value', '').strip()
                    
                    # Skip if either field is empty
                    if not org_id or not npi_value:
                        continue
                    
                    # Check if URL is valid HTTPS
                    if not DataCleaner.is_valid_https_url(url=org_id):
                        continue
                    
                    # Check if NPI is valid 10-digit number
                    if not DataCleaner.is_valid_npi(npi_value=npi_value):
                        continue
                    
                    candidates.append((org_id, npi_value))
                    
        except FileNotFoundError:
            logger.error(f"Input file not found: {input_file_path}")
            return []
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            return []
        
        logger.info(f"Found {len(candidates)} candidate records")
        return candidates
    
    @staticmethod
    def get_unique_domains(*, candidates: List[Tuple[str, str]]) -> Set[str]:
        """Extract unique base domains from candidate URLs"""
        domains = set()
        
        for org_url, _ in candidates:
            base_domain = DataCleaner.extract_base_domain(url=org_url)
            if base_domain:
                domains.add(base_domain)
        
        logger.info(f"Found {len(domains)} unique domains to check")
        return domains
    
    @staticmethod
    def check_responsive_domains(*, domains: Set[str]) -> Set[str]:
        """Check which domains are responsive and return the responsive ones"""
        responsive_domains = set()
        
        for domain in domains:
            logger.info(f"Checking domain: {domain}")
            if DataCleaner.is_domain_responsive(base_domain=domain):
                responsive_domains.add(domain)
                logger.info(f"Domain responsive: {domain}")
            else:
                logger.info(f"Domain not responsive: {domain}")
            
            # Add small delay to be respectful to servers
            time.sleep(0.5)
        
        logger.info(f"Found {len(responsive_domains)} responsive domains")
        return responsive_domains
    
    @staticmethod
    def filter_valid_records(*, candidates: List[Tuple[str, str]], responsive_domains: Set[str]) -> List[Tuple[str, str]]:
        """Filter candidates to only include those with responsive domains"""
        valid_records = []
        
        for org_url, npi_value in candidates:
            base_domain = DataCleaner.extract_base_domain(url=org_url)
            if base_domain in responsive_domains:
                valid_records.append((org_url, npi_value))
        
        logger.info(f"Found {len(valid_records)} valid records with responsive domains")
        return valid_records
    
    @staticmethod
    def write_output_csv(*, output_file_path: str, valid_records: List[Tuple[str, str]]):
        """Write valid records to output CSV file"""
        try:
            with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['org_fhir_url', 'npi']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for org_url, npi_value in valid_records:
                    writer.writerow({
                        'org_fhir_url': org_url,
                        'npi': npi_value
                    })
            
            logger.info(f"Successfully wrote {len(valid_records)} records to {output_file_path}")
            
        except Exception as e:
            logger.error(f"Error writing output file: {e}")
            raise
    
    @staticmethod
    def process_data(*, input_file_path: str, output_file_path: str):
        """Main processing method"""
        logger.info("Starting data cleaning process")
        
        # Load candidate data
        candidates = DataCleaner.load_candidate_data(input_file_path=input_file_path)
        if not candidates:
            logger.error("No valid candidate data found")
            return
        
        # Get unique domains
        domains = DataCleaner.get_unique_domains(candidates=candidates)
        if not domains:
            logger.error("No valid domains found")
            return
        
        # Check responsive domains
        responsive_domains = DataCleaner.check_responsive_domains(domains=domains)
        if not responsive_domains:
            logger.error("No responsive domains found")
            return
        
        # Filter valid records
        valid_records = DataCleaner.filter_valid_records(
            candidates=candidates,
            responsive_domains=responsive_domains
        )
        
        if not valid_records:
            logger.error("No valid records found")
            return
        
        # Write output
        DataCleaner.write_output_csv(
            output_file_path=output_file_path,
            valid_records=valid_records
        )
        
        logger.info("Data cleaning process completed successfully")


def main():
    """Main function"""
    args = DataCleaner.parse_arguments()
    
    DataCleaner.process_data(
        input_file_path=args.input_file,
        output_file_path=args.output_file
    )


if __name__ == '__main__':
    main()
