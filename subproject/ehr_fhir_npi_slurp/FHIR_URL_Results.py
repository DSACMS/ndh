
class FHIR_URL_Results:
    """
    Dictionary-like class for storing FHIR URL validation results.
    Acts as a comprehensive container for URL testing and validation data.
    """
    
    def __init__(self):
        self.data = {
            # Core URL validation
            'url_works': False,
            'http_status': None,
            'is_valid_json': False,
            'is_valid_fhir': False,
            'is_valid_xml': False,
            'is_html_response': False,
            'is_bundle_or_resource': None,
            'next_page_url': False,
            
            # Resource information
            'original_resource_json': None,
            'original_resource_id': None,
            'original_resource_type': None,
            'resource_url': None,
            'referenced_urls': [],
            
            # Endpoint discovery
            'capability_url': None,
            'capability_url_status': None,
            'smart_config_url': None,
            'smart_config_url_status': None,
            'openapi_docs_url': None,
            'openapi_docs_url_status': None,
            'openapi_json_url': None,
            'openapi_json_url_status': None,
            'swagger_url': None,
            'swagger_url_status': None,
            'swagger_json_url': None,
            'swagger_json_url_status': None,
            
            # Error tracking
            'errors': [],
            'timeout_occurred': False,
            'response_text': None,
            'response_headers': None
        }
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __contains__(self, key):
        return key in self.data
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
    
    def items(self):
        return self.data.items()
    
    def to_dict(self):
        """Return the internal dictionary representation."""
        return self.data.copy()
    
    def __str__(self):
        """Format the results for human-readable output."""
        lines = []
        
        # Basic resource information
        lines.append(f"  Resource Type: {self.get('original_resource_type', 'Unknown')}")
        lines.append(f"  Resource ID: {self.get('original_resource_id', 'None')}")
        lines.append(f"  Resource URL: {self.get('resource_url', 'None')}")
        
        # URL validation results
        lines.append(f"  URL Works: {self.get('url_works', False)}")
        lines.append(f"  HTTP Status: {self.get('http_status', 'None')}")
        lines.append(f"  Valid JSON: {self.get('is_valid_json', False)}")
        lines.append(f"  Valid FHIR: {self.get('is_valid_fhir', False)}")
        
        # Resource type information
        bundle_or_resource = self.get('is_bundle_or_resource', 'None')
        lines.append(f"  Bundle or Resource: {bundle_or_resource}")
        
        # Endpoint discovery results
        endpoint_info = [
            ('Capability URL', 'capability_url', 'capability_url_status'),
            ('SMART Config URL', 'smart_config_url', 'smart_config_url_status'),
            ('OpenAPI Docs URL', 'openapi_docs_url', 'openapi_docs_url_status'),
            ('OpenAPI JSON URL', 'openapi_json_url', 'openapi_json_url_status'),
            ('Swagger URL', 'swagger_url', 'swagger_url_status'),
            ('Swagger JSON URL', 'swagger_json_url', 'swagger_json_url_status')
        ]
        
        for label, url_key, status_key in endpoint_info:
            url = self.get(url_key)
            status = self.get(status_key)
            
            if url:
                lines.append(f"  {label}: {url}")
                if status:
                    # Format status - handle both string and list formats
                    if isinstance(status, list):
                        status_str = ', '.join(str(s) for s in status)
                    else:
                        status_str = str(status)
                    lines.append(f"  {label.split()[0]} Status: {status_str}")
        
        # Error information
        errors = self.get('errors', [])
        if errors:
            error_str = ', '.join(str(error) for error in errors)
            lines.append(f"  Errors: {error_str}")
        
        # Timeout information
        if self.get('timeout_occurred', False):
            lines.append("  Timeout: Yes")
        
        # Next page URL for bundles
        next_page = self.get('next_page_url')
        if next_page:
            lines.append(f"  Next Page URL: {next_page}")
        
        # Referenced URLs for bundles
        referenced_urls = self.get('referenced_urls', [])
        if referenced_urls:
            lines.append(f"  Referenced URLs: {len(referenced_urls)} found")
            for i, url in enumerate(referenced_urls[:3]):  # Show first 3
                lines.append(f"    {i+1}. {url}")
            if len(referenced_urls) > 3:
                lines.append(f"    ... and {len(referenced_urls) - 3} more")
        
        return '\n'.join(lines)
