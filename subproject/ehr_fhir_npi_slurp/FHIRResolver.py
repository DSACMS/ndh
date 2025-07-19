import json
import os
import re
import time
from typing import List, Dict, Any, Optional, Union
from urllib.parse import urlparse, urljoin
import urllib3.exceptions

import requests
from pydantic import ValidationError
from FHIR_URL_Results import FHIR_URL_Results

# Dynamic FHIR version imports
FHIR_VERSIONS = ['fhir.resources', 'fhir.resources.R4B', 'fhir.resources.STU3']
FHIR_MODULES = {}

def load_fhir_modules():
    """Load FHIR modules dynamically, trying different versions."""
    global FHIR_MODULES
    
    for version in FHIR_VERSIONS:
        try:
            # Import the base module
            base_module = __import__(version, fromlist=[''])
            
            # Try to import Bundle and common resource types from this version
            try:
                bundle_module = __import__(f"{version}.bundle", fromlist=['Bundle'])
                resource_module = __import__(f"{version}.resource", fromlist=['Resource'])
                
                # Load specific resource classes
                endpoint_module = __import__(f"{version}.endpoint", fromlist=['Endpoint'])
                organization_module = __import__(f"{version}.organization", fromlist=['Organization'])
                
                FHIR_MODULES[version] = {
                    'base': base_module,
                    'Bundle': bundle_module.Bundle,
                    'Resource': resource_module.Resource,
                    'Endpoint': endpoint_module.Endpoint,
                    'Organization': organization_module.Organization
                }
                print(f"Successfully loaded FHIR version: {version}")
                
            except ImportError as e:
                print(f"Could not load Bundle/Resource from {version}: {e}")
                continue
                
        except ImportError as e:
            print(f"Could not load FHIR version {version}: {e}")
            continue
    
    if not FHIR_MODULES:
        raise ImportError("No FHIR modules could be loaded")

# Load FHIR modules on import
load_fhir_modules()




class FHIRResolver:
    """
    Enhanced FHIR Resource Resolver with comprehensive URL validation and endpoint discovery.
    All methods are static to maintain stateless operation.
    """
    
    # Standard FHIR headers for JSON requests
    FHIR_HEADERS = {
        'Accept': 'application/fhir+json,application/json',
        'Content-Type': 'application/fhir+json'
    }
    
    # HTML detection patterns
    HTML_PATTERNS = [
        r'<!DOCTYPE\s+html',
        r'<html\b',
        r'<head\b',
        r'<body\b',
        r'<title\b'
    ]
    
    @staticmethod
    def get_json_from_url(url: str) -> FHIR_URL_Results:
        """
        Gets JSON text from a URL and returns a FHIR_URL_Results object 
        populated with any issues with the URL, plus the JSON object.
        
        Args:
            url: The URL to fetch JSON from
            
        Returns:
            FHIR_URL_Results object with validation results and response data
        """
        results = FHIR_URL_Results()
        results['resource_url'] = url
        
        try:
            # Make the request with appropriate headers
            response = requests.get(url, headers=FHIRResolver.FHIR_HEADERS, timeout=30, allow_redirects=True)
            
            # Store response information
            results['http_status'] = response.status_code
            results['response_headers'] = dict(response.headers)
            results['response_text'] = response.text
            
            # Check if URL works (2xx status codes)
            if 200 <= response.status_code < 300:
                results['url_works'] = True
            else:
                results['errors'].append(f"HTTP {response.status_code}")
                return results
            
            # Check content type and format
            content_type = response.headers.get('content-type', '').lower()
            response_text = response.text.strip()
            
            # Check if response is HTML
            for pattern in FHIRResolver.HTML_PATTERNS:
                if re.search(pattern, response_text, re.IGNORECASE):
                    results['is_html_response'] = True
                    break
            
            # Check if response is XML
            if response_text.startswith('<?xml') or response_text.startswith('<'):
                results['is_valid_xml'] = True
            
            # Check if response is valid JSON
            try:
                json_data = json.loads(response_text)
                results['is_valid_json'] = True
                
                # Check if it's valid FHIR
                if isinstance(json_data, dict) and 'resourceType' in json_data:
                    results['is_valid_fhir'] = True
                    resource_type = json_data.get('resourceType')
                    
                    if resource_type == 'Bundle':
                        results['is_bundle_or_resource'] = 'Bundle'
                    else:
                        results['is_bundle_or_resource'] = 'Resource'
                        
            except json.JSONDecodeError:
                results['errors'].append("Response is not valid JSON")
                
        except requests.exceptions.Timeout:
            results['timeout_occurred'] = True
            results['errors'].append("Request timed out")
        except urllib3.exceptions.HeaderParsingError:
            results['url_works'] = True
            results['http_status'] = 200
            results['errors'].append("Custom headers detected but endpoint responsive")
        except Exception as e:
            results['errors'].append(f"Request failed: {e}")
        
        return results
    
    @staticmethod
    def get_json_from_file(file_path: str) -> Dict[str, Any]:
        """
        Gets a plain JSON object from a file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Plain JSON object (dict)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def get_json_from_text(json_text: str) -> Dict[str, Any]:
        """
        Accepts JSON text and turns it into a plain JSON object.
        
        Args:
            json_text: Raw JSON text string
            
        Returns:
            Plain JSON object (dict)
        """
        return json.loads(json_text)
    
    @staticmethod
    def validate_and_parse_json_to_fhir_resources(json_data: Dict[str, Any], is_debug: bool = False) -> List[Any]:
        """
        Central validation function that accepts a plain JSON object 
        and converts it into FHIR resources. This is the ONLY function 
        that handles fhir.resources validation logic.
        
        Args:
            json_data: Plain JSON object (dict) to validate and parse
            
        Returns:
            List of FHIR resource objects (or mock resources if validation fails)
        """
        resources = []


        try:
            if json_data.get("resourceType") == "Bundle":
                if(is_debug):
                    print(f"🔄 Attempting to parse Bundle using {len(FHIR_MODULES)} FHIR versions...")
                # Try different FHIR versions for Bundle parsing
                bundle_parsed = False
                bundle_success_version = None
                
                for version_name, modules in FHIR_MODULES.items():
                    if(is_debug):
                        print(f"  📦 Trying Bundle parsing with {version_name}...")
                    try:
                        Bundle = modules['Bundle']
                        bundle = Bundle(**json_data)
                        print(f"  ✅ SUCCESS: Bundle parsed successfully with {version_name}")
                        if bundle.entry:
                            for entry in bundle.entry:
                                if entry.resource:
                                    resources.append(entry.resource)
                        bundle_parsed = True
                        bundle_success_version = version_name
                        break
                    except ValidationError as e:
                        print(f"  ❌ FAILED: Bundle parsing failed with {version_name}")
                        print(f"      Full error: {str(e)}")
                        continue
                
                if not bundle_parsed:
                    if(is_debug):
                        print(f"  ⚠️  Bundle validation failed with all {len(FHIR_MODULES)} FHIR versions, extracting resources manually from entry array")
                    # If Bundle parsing fails, extract resources manually from entry array
                    if "entry" in json_data and isinstance(json_data["entry"], list):
                        if(is_debug):
                            print(f"  📂 Found {len(json_data['entry'])} entries in Bundle, attempting individual resource parsing...")
                        
                        for i, entry in enumerate(json_data["entry"]):
                            if isinstance(entry, dict) and "resource" in entry:
                                resource_data = entry["resource"]
                                full_url = entry.get("fullUrl")
                                resource_type = resource_data.get('resourceType', 'Unknown')
                                resource_id = resource_data.get('id', 'No-ID')
                                
                                if(is_debug):
                                    print(f"    🔍 Entry {i+1}: Attempting to parse {resource_type} resource (ID: {resource_id})...")
                                
                                # Try to parse individual resource with different FHIR versions
                                resource_parsed = False
                                individual_success_version = None
                                
                                for version_name, modules in FHIR_MODULES.items():
                                    if(is_debug):
                                        print(f"      📋 Trying {resource_type} parsing with {version_name}...")
                                    try:
                                        # Try to get the specific resource class first
                                        if resource_type in modules:
                                            ResourceClass = modules[resource_type]
                                            if(is_debug):
                                                print(f"          Using specific {resource_type} class")
                                        else:
                                            # Fall back to generic Resource class
                                            ResourceClass = modules['Resource']
                                            if(is_debug):
                                                print(f"          Using generic Resource class for {resource_type}")
                                        
                                        resource = ResourceClass(**resource_data)
                                        # Store fullUrl for later use
                                        if full_url:
                                            resource._full_url = full_url
                                        resources.append(resource)
                                        resource_parsed = True
                                        individual_success_version = version_name
                                        print(f"      ✅ SUCCESS: {resource_type} parsed successfully with {version_name}")
                                        break
                                    except ValidationError as e:
                                        print(f"      ❌ FAILED: {resource_type} parsing failed with {version_name}")
                                        print(f"          Full error: {str(e)}")
                                        continue
                                
                                if not resource_parsed:
                                    # If individual resource parsing fails, create a generic resource
                                    print(f"      ⚠️  All FHIR versions failed for {resource_type}, creating mock resource with raw data")
                                    # Create a mock resource with the raw data
                                    class MockResource:
                                        def __init__(self, resource_data, full_url):
                                            self.resource_type = resource_data.get('resourceType', 'ResourceTypeUnknown')
                                            self.id = resource_data.get('id')
                                            self._full_url = full_url
                                            self._resource_data = resource_data
                                        
                                        def json(self):
                                            return json.dumps(self._resource_data)
                                    
                                    mock_resource = MockResource(resource_data, full_url)
                                    resources.append(mock_resource)
                                else:
                                    
                                    if(is_debug):
                                        print(f"      🎯 {resource_type} successfully processed with {individual_success_version}")
                else:
                    print(f"  🎯 Final result: Bundle successfully parsed with {bundle_success_version}, extracted {len(resources)} resources")
                    
            else:
                # Try different FHIR versions for Resource parsing
                resource_type = json_data.get('resourceType', 'ResourceTypeUnknown')
                resource_id = json_data.get('id', 'No-ID')
                
                print(f"🔄 Attempting to parse single {resource_type} resource (ID: {resource_id}) using {len(FHIR_MODULES)} FHIR versions...")
                
                resource_parsed = False
                single_success_version = None
                
                for version_name, modules in FHIR_MODULES.items():
                    print(f"  📋 Trying {resource_type} parsing with {version_name}...")
                    try:
                        # Try to get the specific resource class first
                        if resource_type in modules:
                            ResourceClass = modules[resource_type]
                            print(f"      Using specific {resource_type} class")
                        else:
                            # Fall back to generic Resource class
                            ResourceClass = modules['Resource']
                            print(f"      Using generic Resource class for {resource_type}")
                        
                        resource = ResourceClass(**json_data)
                        resources.append(resource)
                        resource_parsed = True
                        single_success_version = version_name
                        print(f"  ✅ SUCCESS: {resource_type} parsed successfully with {version_name}")
                        break
                    except ValidationError as e:
                        print(f"  ❌ FAILED: {resource_type} parsing failed with {version_name}")
                        print(f"      Full error: {str(e)}")
                        continue
                
                if not resource_parsed:
                    print(f"  ⚠️  All {len(FHIR_MODULES)} FHIR versions failed for {resource_type}, cannot process resource")
                else:

                    print(f"  🎯 Final result: {resource_type} successfully parsed with {single_success_version}")
                    
        except Exception as e:
            print(f"Error parsing JSON data: {e}")
        
        return resources
    
    @staticmethod
    def get_resource_array_from(
        *,
        resource_url: Optional[str] = None,
        resource_json_file: Optional[str] = None,
        resource_json_text: Optional[str] = None,
        resource_Object: Optional[Any] = None,
        filter_by_ResourceTypes: Optional[List[str]] = None
    ) -> List[Any]:
        """
        Main resource extraction method that handles multiple input types.
        Uses the DRY architecture functions.
        
        Args:
            resource_url: FHIR HTTPS URL to download and process
            resource_json_file: Path to JSON file containing FHIR data
            resource_json_text: Raw JSON text containing FHIR data
            resource_Object: fhir.resources Resource object
            filter_by_ResourceTypes: List of resource types to filter by (empty = all)
            
        Returns:
            List of fhir.resources.resource.Resource instances
        """
        if filter_by_ResourceTypes is None:
            filter_by_ResourceTypes = []
        
        resources = []
        
        try:
            # Handle different input types using DRY functions
            if resource_url:
                # Get JSON from URL and validate
                url_result = FHIRResolver.get_json_from_url(resource_url)
                if url_result['url_works'] and url_result['is_valid_json']:
                    json_data = json.loads(url_result['response_text'])
                    resources = FHIRResolver.validate_and_parse_json_to_fhir_resources(json_data)
                else:
                    print(f"Error: Could not fetch or parse FHIR data from URL: {resource_url}")
            
            elif resource_json_file:
                # Get JSON from file and validate
                json_data = FHIRResolver.get_json_from_file(resource_json_file)
                resources = FHIRResolver.validate_and_parse_json_to_fhir_resources(json_data)
            
            elif resource_json_text:
                # Get JSON from text and validate
                json_data = FHIRResolver.get_json_from_text(resource_json_text)
                resources = FHIRResolver.validate_and_parse_json_to_fhir_resources(json_data)
            
            elif resource_Object:
                # Direct resource object
                resources = [resource_Object]
            
            else:
                raise ValueError("One of resource_url, resource_json_file, resource_json_text, or resource_Object must be provided")
            
            # Apply resource type filtering if specified
            if filter_by_ResourceTypes:
                resources = [r for r in resources if hasattr(r, 'resource_type') and r.resource_type in filter_by_ResourceTypes]
            
            return resources
            
        except Exception as e:
            print(f"Error processing FHIR resource: {e}")
            return []
    
    @staticmethod
    def get_endpoints_from(
        *,
        resource_url: Optional[str] = None,
        resource_json_file: Optional[str] = None,
        resource_json_text: Optional[str] = None,
        resource_Object: Optional[Any] = None,
        filter_by_ResourceTypes: Optional[List[str]] = None
    ) -> List[FHIR_URL_Results]:
        """
        Extract endpoints from multiple resources using DRY architecture.
        
        Args:
            resource_url: FHIR HTTPS URL to download and process
            resource_json_file: Path to JSON file containing FHIR data
            resource_json_text: Raw JSON text containing FHIR data
            resource_Object: fhir.resources Resource object
            filter_by_ResourceTypes: List of resource types to filter by (empty = all)
            
        Returns:
            List of FHIR_URL_Results objects
        """
        results = []
        
        try:
            # Get resources using the existing method
            resources = FHIRResolver.get_resource_array_from(
                resource_url=resource_url,
                resource_json_file=resource_json_file,
                resource_json_text=resource_json_text,
                resource_Object=resource_Object,
                filter_by_ResourceTypes=filter_by_ResourceTypes
            )
            
            # Process each resource to get URL results
            for resource in resources:
                try:
                    # Try to determine base URL from the original source
                    base_url = None
                    
                    # If we have a URL input, use it as base
                    if resource_url:
                        parsed = urlparse(resource_url)
                        base_url = f"{parsed.scheme}://{parsed.netloc}"
                    
                    # Get URL results for this resource
                    url_result = FHIRResolver._get_resource_url_results(
                        resource=resource,
                        base_url=base_url
                    )
                    
                    results.append(url_result)
                    
                except Exception as e:
                    # Create error result for this resource
                    error_result = FHIR_URL_Results()
                    error_result['errors'].append(f"Error processing resource: {e}")
                    if hasattr(resource, 'resource_type'):
                        error_result['original_resource_type'] = resource.resource_type
                    if hasattr(resource, 'id'):
                        error_result['original_resource_id'] = resource.id
                    results.append(error_result)
            
            return results
            
        except Exception as e:
            print(f"Error in get_endpoints_from: {e}")
            return []
    
    @staticmethod
    def _get_resource_url_results(resource: Any, base_url: Optional[str] = None) -> FHIR_URL_Results:
        """
        Extract and validate the global FHIR URL for a single resource.
        
        Args:
            resource: fhir.resources Resource object
            base_url: Base URL for constructing resource URLs
            
        Returns:
            FHIR_URL_Results object with validation results
        """
        results = FHIR_URL_Results()
        
        try:
            # Store original resource information
            if hasattr(resource, 'json'):
                results['original_resource_json'] = resource.json()
            results['original_resource_id'] = getattr(resource, 'id', None)
            results['original_resource_type'] = getattr(resource, 'resource_type', None)
            
            # Determine the resource URL
            resource_url = None
            
            # First priority: check if resource has a stored fullUrl from Bundle entry
            if hasattr(resource, '_full_url') and resource._full_url and (resource._full_url.startswith('http://') or resource._full_url.startswith('https://')):
                resource_url = resource._full_url
            # Second priority: construct from base_url if available
            elif base_url and results['original_resource_type'] and results['original_resource_id']:
                resource_url = f"{base_url.rstrip('/')}/{results['original_resource_type']}/{results['original_resource_id']}"
            # Third priority: try to extract from resource itself
            elif hasattr(resource, 'meta') and hasattr(resource.meta, 'source'):
                resource_url = resource.meta.source
            
            if not resource_url:
                results['errors'].append("Could not determine resource URL")
                return results
            
            results['resource_url'] = resource_url
            
            # Validate the URL using existing function
            url_validation = FHIRResolver.get_json_from_url(resource_url)
            
            # Copy validation results
            results['url_works'] = url_validation['url_works']
            results['http_status'] = url_validation['http_status']
            results['is_valid_json'] = url_validation['is_valid_json']
            results['is_valid_fhir'] = url_validation['is_valid_fhir']
            results['is_bundle_or_resource'] = url_validation['is_bundle_or_resource']
            results['errors'].extend(url_validation['errors'])
            results['timeout_occurred'] = url_validation['timeout_occurred']
            results['response_text'] = url_validation['response_text']
            results['response_headers'] = url_validation['response_headers']
            
            # Discover endpoints if URL is valid
            if results['url_works']:
                FHIRResolver._discover_endpoints(resource_url, results)
            
        except Exception as e:
            results['errors'].append(f"Error processing resource: {e}")
        
        return results
    
    @staticmethod
    def _discover_endpoints(url: str, results: FHIR_URL_Results) -> None:
        """Discover FHIR endpoints at various levels from a given URL."""
        try:
            # Extract base URL from the resource URL
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Define endpoints to test
            endpoints = {
                'capability_url': '/metadata',
                'smart_config_url': '/.well-known/smart-configuration',
                'openapi_docs_url': '/api-docs',
                'openapi_json_url': '/openapi.json',
                'swagger_url': '/swagger',
                'swagger_json_url': '/swagger.json'
            }
            
            # Test each endpoint
            for endpoint_key, endpoint_path in endpoints.items():
                status_key = f"{endpoint_key}_status"
                test_url = f"{base_url}{endpoint_path}"
                
                try:
                    response = requests.get(test_url, timeout=10, allow_redirects=True)
                    
                    if 200 <= response.status_code < 300:
                        results[endpoint_key] = test_url
                        
                        # Validate content based on endpoint type
                        if endpoint_key == 'capability_url':
                            try:
                                json_data = response.json()
                                if json_data.get('resourceType') == 'CapabilityStatement':
                                    results[status_key] = 'success'
                                else:
                                    results[status_key] = 'error: got JSON but not CapabilityStatement'
                            except:
                                results[status_key] = 'error: got response but not valid JSON'
                        elif endpoint_key == 'smart_config_url':
                            try:
                                json_data = response.json()
                                if 'capabilities' in json_data:
                                    results[status_key] = 'success'
                                else:
                                    results[status_key] = 'error: got JSON but no capabilities key'
                            except:
                                results[status_key] = 'error: got response but not valid JSON'
                        elif endpoint_key in ['openapi_docs_url', 'openapi_json_url']:
                            try:
                                json_data = response.json()
                                if 'openapi' in json_data:
                                    results[status_key] = 'success'
                                else:
                                    results[status_key] = 'error: got JSON but no openapi key'
                            except:
                                # Could be YAML, check content
                                if 'openapi:' in response.text:
                                    results[status_key] = 'success'
                                else:
                                    results[status_key] = 'error: got response but not valid OpenAPI'
                        elif endpoint_key == 'swagger_url':
                            # Swagger often returns HTML
                            if 'html' in response.headers.get('content-type', '').lower():
                                results[status_key] = 'success'
                            else:
                                results[status_key] = 'error: got response but not HTML page'
                        elif endpoint_key == 'swagger_json_url':
                            try:
                                json_data = response.json()
                                if 'swagger' in json_data or 'openapi' in json_data:
                                    results[status_key] = 'success'
                                else:
                                    results[status_key] = 'error: got JSON but no swagger/openapi key'
                            except:
                                results[status_key] = 'error: got response but not valid JSON'
                        else:
                            results[status_key] = 'success'
                    else:
                        results[status_key] = f'error: got {response.status_code}'
                        
                except Exception as e:
                    results[status_key] = f'error: {e}'
                    
                # Small delay between requests
                time.sleep(0.1)
                
        except Exception as e:
            # Add general error to results
            for endpoint_key in ['capability_url', 'smart_config_url', 'openapi_docs_url', 
                               'openapi_json_url', 'swagger_url', 'swagger_json_url']:
                status_key = f"{endpoint_key}_status"
                if results.get(status_key) is None:
                    results[status_key] = f'error: endpoint discovery failed - {e}'
