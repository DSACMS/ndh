#!/usr/bin/env python3
"""
Step60_CalculateOpenEndpoints.py

This script enriches the org_fhir_url,npi CSV data by discovering well-known FHIR endpoints
at various directory levels for each unique domain.

TODO: Need to implement the specific content expectations after getting a 200 message for the following urls. 
Getting a 200 but failing to provide the expected content, should be listed as as fail. But with a different error. 

For each domain, it tests directory levels to find:
- Capability Statement (/metadata) Request JSON in the headers and Expect JSON with a "resourceType" that should be called "CapabilityStatement"
- Smart Config (/.well-known/smart-configuration) Request JSON in the headers and Expect JSON with a key called 'capabilities'
- OpenAPI docs (/api-docs)
- OpenAPI JSON (/openapi.json) Request JSON in the headers and Expect JSON with
- Swagger (/swagger) - this will often forward to /swagger/index.html which is fine. 
- Swagger JSON (/swagger.json) Request JSON in the headers and Expect JSON with

Usage:
    python Step60_CalculateOpenEndpoints.py --input_csv_file input.csv --output_csv_file output.csv
"""

import argparse
import csv
import requests
from urllib.parse import urlparse
from typing import List, Tuple, Dict, Set
import time
import logging
import urllib3.exceptions

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EndpointCalculator:
    """Class for discovering FHIR endpoints at various directory levels"""
    
    # Define the endpoints we're looking for
    ENDPOINTS = {
        'capability_url': '/metadata',
        'smart_url': '/.well-known/smart-configuration',
        'openapi_docs_url': '/api-docs',
        'openapi_json_url': '/openapi.json',
        'swagger_url': '/swagger',
        'swagger_json_url': '/swagger.json'
    }
    
    @staticmethod
    def parse_arguments():
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description='Calculate open FHIR endpoints for org URLs')
        parser.add_argument('--input_csv_file', required=True, help='Path to input CSV file')
        parser.add_argument('--output_csv_file', required=True, help='Path to output CSV file')
        return parser.parse_args()
    
    @staticmethod
    def load_csv_data(*, input_file_path: str) -> List[Tuple[str, str]]:
        """Load CSV data from input file"""
        data = []
        
        try:
            with open(input_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    org_fhir_url = row.get('org_fhir_url', '').strip()
                    npi = row.get('npi', '').strip()
                    
                    if org_fhir_url and npi:
                        data.append((org_fhir_url, npi))
                        
        except FileNotFoundError:
            logger.error(f"Input file not found: {input_file_path}")
            return []
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            return []
        
        logger.info(f"Loaded {len(data)} records from input file")
        return data
    
    @staticmethod
    def extract_unique_domains(*, csv_data: List[Tuple[str, str]]) -> Dict[str, str]:
        """Extract unique domains and map them to a sample full URL"""
        domain_to_sample_url = {}
        
        for org_fhir_url, _ in csv_data:
            try:
                parsed = urlparse(org_fhir_url)
                domain = f"{parsed.scheme}://{parsed.netloc}/"
                
                # Store the first full URL we see for this domain as sample
                if domain not in domain_to_sample_url:
                    domain_to_sample_url[domain] = org_fhir_url
                    
            except Exception as e:
                logger.warning(f"Failed to parse URL {org_fhir_url}: {e}")
                continue
        
        logger.info(f"Found {len(domain_to_sample_url)} unique domains")
        return domain_to_sample_url
    
    @staticmethod
    def get_directory_levels(*, url: str) -> List[str]:
        """Get all directory levels from a URL for testing"""
        try:
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Start with just the domain
            levels = [base_url + "/"]
            
            # Add each directory level
            if parsed.path and parsed.path != '/':
                path_parts = [p for p in parsed.path.split('/') if p]
                current_path = ""
                
                for part in path_parts:
                    current_path += "/" + part
                    levels.append(base_url + current_path + "/")
            
            return levels
            
        except Exception as e:
            logger.warning(f"Failed to get directory levels for {url}: {e}")
            return []
    
    @staticmethod
    def test_endpoint_at_level(*, base_url: str, endpoint_path: str, timeout: int = 10) -> bool:
        """Test if an endpoint exists at a given base URL level"""
        try:
            test_url = base_url.rstrip('/') + endpoint_path
            response = requests.get(test_url, timeout=timeout, allow_redirects=True)
            
            # Accept 200-299 status codes as successful
            return 200 <= response.status_code < 300
            
        except urllib3.exceptions.HeaderParsingError as e:
            # Custom headers are fine - consider endpoint responsive
            logger.debug(f"Endpoint {base_url}{endpoint_path} has custom headers but is responsive: {e}")
            return True
        except Exception as e:
            # Handle any other HeaderParsingError variants
            if "HeaderParsingError" in str(e) or "MissingHeaderBodySeparatorDefect" in str(e):
                logger.debug(f"Endpoint {base_url}{endpoint_path} has custom headers but is responsive: {e}")
                return True
            
            logger.debug(f"Endpoint {base_url}{endpoint_path} not responsive: {e}")
            return False
    
    @staticmethod
    def discover_endpoints_for_domain(*, domain: str, sample_url: str) -> Dict[str, str]:
        """Discover all endpoints for a given domain"""
        logger.info(f"Discovering endpoints for domain: {domain}")
        
        # Get all directory levels to test
        levels = EndpointCalculator.get_directory_levels(url=sample_url)
        
        # Initialize results with error messages
        results = {}
        for endpoint_name in EndpointCalculator.ENDPOINTS.keys():
            results[endpoint_name] = f"Error - failed to find {endpoint_name.replace('_', ' ')}"
        
        # Test each level for each endpoint
        for level in levels:
            logger.debug(f"Testing level: {level}")
            
            for endpoint_name, endpoint_path in EndpointCalculator.ENDPOINTS.items():
                # Skip if we already found this endpoint
                if not results[endpoint_name].startswith("Error"):
                    continue
                
                if EndpointCalculator.test_endpoint_at_level(base_url=level, endpoint_path=endpoint_path):
                    found_url = level.rstrip('/') + endpoint_path
                    results[endpoint_name] = found_url
                    logger.info(f"Found {endpoint_name}: {found_url}")
                
                # Add small delay between requests
                time.sleep(0.1)
            
            # Add delay between levels
            time.sleep(0.5)
        
        # Check if no URLs were found at all and warn
        found_any_url = any(not result.startswith("Error") for result in results.values())
        if not found_any_url:
            logger.warning(f"No FHIR endpoints found for domain: {domain}")
        
        return results
    
    @staticmethod
    def choose_https_org_url(*, org_fhir_url: str, endpoints: Dict[str, str]) -> str:
        """Choose the best HTTPS organizational URL from available options"""
        
        # First preference: use the original org_fhir_url if it's HTTPS
        if org_fhir_url.startswith('https://'):
            return org_fhir_url
        
        # Second preference: look for working HTTPS endpoints in priority order
        endpoint_priority = ['capability_url', 'smart_url', 'openapi_docs_url', 'swagger_url', 'openapi_json_url', 'swagger_json_url']
        
        for endpoint_name in endpoint_priority:
            endpoint_url = endpoints.get(endpoint_name, '')
            if endpoint_url.startswith('https://'):
                return endpoint_url
        
        # Third preference: use the original org_fhir_url even if it's HTTP
        if org_fhir_url.startswith('http://'):
            return org_fhir_url
        
        # Fourth preference: look for any working HTTP endpoints
        for endpoint_name in endpoint_priority:
            endpoint_url = endpoints.get(endpoint_name, '')
            if endpoint_url.startswith('http://'):
                return endpoint_url
        
        # Last resort: return the original URL
        return org_fhir_url
    
    @staticmethod
    def generate_enriched_output(*, csv_data: List[Tuple[str, str]], domain_endpoints: Dict[str, Dict[str, str]]) -> List[Dict[str, str]]:
        """Generate enriched output data"""
        enriched_data = []
        
        for org_fhir_url, npi in csv_data:
            try:
                parsed = urlparse(org_fhir_url)
                domain = f"{parsed.scheme}://{parsed.netloc}/"
                
                # Get endpoints for this domain
                endpoints = domain_endpoints.get(domain, {})
                
                # Choose the best HTTPS organizational URL
                https_org_url = EndpointCalculator.choose_https_org_url(
                    org_fhir_url=org_fhir_url,
                    endpoints=endpoints
                )
                
                # Create enriched row
                row = {
                    'org_fhir_url': org_fhir_url,
                    'npi': npi,
                    'https_org_url': https_org_url,
                    'capability_url': endpoints.get('capability_url', 'Error - failed to find capability url'),
                    'smart_url': endpoints.get('smart_url', 'Error - failed to find smart url'),
                    'openapi_docs_url': endpoints.get('openapi_docs_url', 'Error - failed to find openapi docs url'),
                    'openapi_json_url': endpoints.get('openapi_json_url', 'Error - failed to find openapi json url'),
                    'swagger_url': endpoints.get('swagger_url', 'Error - failed to find swagger url'),
                    'swagger_json_url': endpoints.get('swagger_json_url', 'Error - failed to find swagger json url')
                }
                
                enriched_data.append(row)
                
            except Exception as e:
                logger.warning(f"Failed to process URL {org_fhir_url}: {e}")
                # Add row with all errors
                row = {
                    'org_fhir_url': org_fhir_url,
                    'npi': npi,
                    'https_org_url': org_fhir_url,  # Use original URL as fallback
                    'capability_url': 'Error - failed to find capability url',
                    'smart_url': 'Error - failed to find smart url',
                    'openapi_docs_url': 'Error - failed to find openapi docs url',
                    'openapi_json_url': 'Error - failed to find openapi json url',
                    'swagger_url': 'Error - failed to find swagger url',
                    'swagger_json_url': 'Error - failed to find swagger json url'
                }
                enriched_data.append(row)
        
        return enriched_data
    
    @staticmethod
    def write_output_csv(*, output_file_path: str, enriched_data: List[Dict[str, str]]):
        """Write enriched data to output CSV file"""
        try:
            fieldnames = [
                'org_fhir_url', 'npi', 'https_org_url', 'capability_url', 'smart_url', 
                'openapi_docs_url', 'openapi_json_url', 'swagger_url', 'swagger_json_url'
            ]
            
            with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(enriched_data)
            
            logger.info(f"Successfully wrote {len(enriched_data)} records to {output_file_path}")
            
        except Exception as e:
            logger.error(f"Error writing output file: {e}")
            raise
    
    @staticmethod
    def process_data(*, input_file_path: str, output_file_path: str):
        """Main processing method"""
        logger.info("Starting endpoint discovery process")
        
        # Load CSV data
        csv_data = EndpointCalculator.load_csv_data(input_file_path=input_file_path)
        if not csv_data:
            logger.error("No valid CSV data found")
            return
        
        # Extract unique domains
        domain_to_sample_url = EndpointCalculator.extract_unique_domains(csv_data=csv_data)
        if not domain_to_sample_url:
            logger.error("No valid domains found")
            return
        
        # Discover endpoints for each domain
        domain_endpoints = {}
        for domain, sample_url in domain_to_sample_url.items():
            try:
                endpoints = EndpointCalculator.discover_endpoints_for_domain(
                    domain=domain, 
                    sample_url=sample_url
                )
                domain_endpoints[domain] = endpoints
                
            except Exception as e:
                logger.error(f"Failed to discover endpoints for domain {domain}: {e}")
                # Add error entries for this domain
                domain_endpoints[domain] = {}
                for endpoint_name in EndpointCalculator.ENDPOINTS.keys():
                    domain_endpoints[domain][endpoint_name] = f"Error - failed to find {endpoint_name.replace('_', ' ')}"
        
        # Generate enriched output
        enriched_data = EndpointCalculator.generate_enriched_output(
            csv_data=csv_data,
            domain_endpoints=domain_endpoints
        )
        
        # Write output
        EndpointCalculator.write_output_csv(
            output_file_path=output_file_path,
            enriched_data=enriched_data
        )
        
        logger.info("Endpoint discovery process completed successfully")


def main():
    """Main function"""
    args = EndpointCalculator.parse_arguments()
    
    EndpointCalculator.process_data(
        input_file_path=args.input_csv_file,
        output_file_path=args.output_csv_file
    )


if __name__ == '__main__':
    main()
