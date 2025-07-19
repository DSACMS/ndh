FHIRResolver
================

FHIR has a concept of a "resource" which is a container abstraction for all-the-things.
It also has a concept of a "Bundle" which is a Resource wth other resources under the "entry" sub-tag.
And "fullUrl" which often sits alongside the resource key, which can provide some insights into further information for a given FHIR endpoint.

This project is designed to make it easier to scrape publicly available FHIR resources, in a clean way that abstracts out the concept of Bundle and lets us think
in terms of arrays of resources.. which usually just have one item in the array (i.e. not a bundle)

But we are also concerned with centralizing the logic for scraping these FHIR URLS correctly. And for rating their relative friendliness and standards-conformance.
As a result, we will also be defining server interaction features, including the ability to reverse engineer the FHIR server structure from starting FHIR urls, etc.

The class should leverage fhir.resources and pydantic (from <https://github.com/nazrulworld/fhir.resources>) whenever possible.
And the implementation should be an improvement of the current implementation in ../ehr_fhir_npi_slurp/FHIRResolver.py and be stored in that file.

This should be a class holding only static methods. The two main functions are:

get_resource_array_from
----------------------

* accepts resource_? either:
  * resource_url a FHIR https global url, that should be downloaded and converted internally into the "starting resource/bundle". This is the one that the is currently implemented in the current class with from_url()
  * resource_json_file a json file path, that should be read in and converted into the "starting resource/bundle"
  * resource_json_text json text containing a resource or a bundle
  * resource_Object a fhir.resources Resource Object

* accepts filter_by_ResourceTypes which is an array of strings that represents a specific resource types. Only resource types of those type should be returned in the array. The default should be an empty array which means every resource type should be accepted.

Returns an array of fhir.resources

* accepts a single fhir.resources resource object

* Returns the global url for that single resource

### get_resource_url_from_resource


Looks inside  single resourcee seeking a global https FHIR url for that resource.

Sometimes a full https url will be returned in under the 'fullUrl' key. When this is an https link, it should be trusted as the FHIR url endpoint for a given resource object.
However, often the endpoint takes the form: "fullUrl": "urn:uuid:2cc42815-dc15-4343-ba03-2e8067ae1e41" which is a hint that it a local reference. Generally to dereference the https global FHIR url when it is not explicitly listed in the resource in fullUrl,
we must use the components of the resource itself to infer the url by taking:

```python
calculated_full_url = f"{thisResource.address}/{thisResource.resourceType}/{thisResource.id} 
```

In either case, the class should use curl to make sure that the URL is real and returns some kind of valid FHIR JSON, even if this JSON requires authentication.

This should return a single instance of the FHIR_URL_Results class, which should also be defined in the ../ehr_fhir_npi_slurp/FHIRResolver.py file.
For now, this should be a "class waiting for methods acting like a dictionary", and that dictionary should contain.

* Did the url work or did it time out.
* What was the HTTP response for the url 200 ? 404? etc
* Was the response valid JSON.
* Was the response valid FHIR.
* Was the response valid XML
* If the response was valid XML, when the url was requested again with specific json/fhir headers request was it JSON?
* Was the response HTML? (based on seeing "doctype html", "<html", "<head", "<body" or similar tags in the text.
* If the response was valid XML, when the url was requested again with specific json/fhir headers request was it JSON?
* Was the response a FHIR Bundle or a Resource? or something else?
* If the resource was a bundle, what was
* An array of the calculated https FHIR urls for objects that were referenced inside the Resources
* a single string url for the calculated FHIR https url for the resource itself.
* if the resource is a bundle of entries (i.e. search results), then what is the url for the next bach of entries. See line 110 in Step70_SlurpPayerProviderNetworks.py for how to calculate this. False if there is no next url in the bundle download.
* original Resource_json
* original resource_id
* original resource type
* Capability Statement url (/metadata) Request JSON in the headers and Expect JSON with a "resourceType" that should be called "CapabilityStatement"
* Smart Config url (/.well-known/smart-configuration) Request JSON in the headers and Expect JSON with a key called 'capabilities'
* OpenAPI docs url (/api-docs) - should return JSON or YAML both with an openapi
* OpenAPI JSON url (/openapi.json) Request JSON in the headers and Expect JSON with 
* Swagger url (/swagger) - this will often forward to /swagger/index.html which is fine. expect an html page
* Swagger JSON url (/swagger.json) Request JSON in the headers and Expect JSON with an openapi key with a version number.

Note the definition of these last variables are documented in the ../ehr_fhir_npi_slurp/Step60_CalculateOpenEndpoints.py 
For each of the various url variables there should also be a something_something_url_status which should either have 'success' as a value or an array of error messages about what particular expectation for the url happened. Frequently, swagger and openapi urls are not both used.. and so when one is absent there should 
just be a single entry with "error: got 404" or "error: got HTML page" or "error: got json that was did not have openapi as a variable" or whatever. 

Create simple dictionary key names for each of these variables as you design the FHIR_URL_Results class.

### get_endpoints_from


This accepts the same arguments as get_resource_array_from and begins by leveraging that function internally to get the initial starting resource objects,
which it feeds to the get_resource_url_from_resource one at a time to build an array of FHIR_URL_Results, which is what it returns. 

Unviversal Requirements
----------

* It is our goal to have a single URL validation and exploration layer that works for mining both EHR and Payer endpoints and will work for other types of slurping data in the future.
* Please read the current Payer FHIR slurping process outlined in ../plan_scrape/Step70_SlurpPayerProviderNetworks.py and the EHR FHIR slurping process outlined in ../ehr_fhir_npi_slurp/Step30_parse_source_bundle.py and ../ehr_fhir_npi_slurp/Step60_CalculateOpenEndpoints.py

## Implementation Plan

### Architecture Design

#### 1. Core Classes to Implement

**FHIRResourceResolver** (static methods only):
- `get_resource_array_from()` - Main resource extraction method
- `get_resource_url_from_resource()` - URL resolution for individual resources  
- `get_endpoints_from()` - Endpoint discovery and validation

**FHIR_URL_Results** (dictionary-like class):
- Comprehensive URL validation results
- HTTP response analysis
- FHIR compliance checking
- Endpoint capability testing

#### 2. Key Technical Components

**Input Handling** (4 input types):
- `resource_url` - HTTP(S) FHIR URLs (extends existing `from_url`)
- `resource_json_file` - Local JSON file paths
- `resource_json_text` - Raw JSON string content
- `resource_Object` - fhir.resources objects

**Resource Processing**:
- Bundle vs single resource detection
- Resource type filtering support
- Pagination handling (next links)
- Reference resolution between resources

**URL Validation & Testing**:
- HTTP response validation (200, 404, timeout, etc.)
- JSON vs XML content detection
- HTML content detection
- FHIR compliance validation
- Bundle vs Resource classification

**Endpoint Discovery**:
- Capability Statement (`/metadata`)
- SMART Configuration (`/.well-known/smart-configuration`)
- OpenAPI docs (`/api-docs`, `/openapi.json`)
- Swagger (`/swagger`, `/swagger.json`)

#### 3. Integration Points

**Leverage Existing Code**:
- Use `Step60_CalculateOpenEndpoints.py` patterns for endpoint testing
- Use `Step70_SlurpPayerProviderNetworks.py` patterns for pagination
- Use `Step30_parse_source_bundle.py` patterns for bundle processing
- Build upon existing `FHIRResolver.from_url()` method

**Dependencies**:
- `fhir.resources` for FHIR object handling
- `pydantic` for validation
- `requests` for HTTP operations
- `urllib.parse` for URL manipulation

### Implementation Phases

#### Phase 1: Core Infrastructure
1. Create `FHIR_URL_Results` class with all required fields
2. Implement input parsing for all 4 input types
3. Set up basic resource extraction from bundles/single resources
4. Add resource type filtering capability

#### Phase 2: URL Resolution & Validation
1. Implement `get_resource_url_from_resource()` method:
   - Extract URLs from `fullUrl` field when present
   - Calculate URLs from `{base_url}/{resourceType}/{id}` when missing
   - Handle `urn:uuid:` local references appropriately
   - Validate URLs with HTTP requests

2. Build comprehensive URL validation in `FHIR_URL_Results`:
   - HTTP response codes (200, 404, etc.)
   - Content type detection (JSON, XML, HTML)
   - FHIR compliance validation
   - Bundle vs Resource classification
   - Timeout handling

#### Phase 3: Endpoint Discovery
1. Implement endpoint testing patterns from `Step60_CalculateOpenEndpoints.py`:
   - `/metadata` - Capability Statement validation
   - `/.well-known/smart-configuration` - SMART config validation
   - `/api-docs` and `/openapi.json` - OpenAPI documentation
   - `/swagger` and `/swagger.json` - Swagger documentation

2. Add status tracking for each endpoint:
   - Success/failure status
   - Detailed error messages
   - Content validation results

#### Phase 4: Resource Processing
1. Implement `get_resource_array_from()` method:
   - Handle all 4 input types (URL, file, text, object)
   - Process bundles and extract individual resources
   - Apply resource type filtering
   - Handle pagination (next links) from bundles

2. Implement `get_endpoints_from()` method:
   - Use `get_resource_array_from()` internally
   - Process each resource through `get_resource_url_from_resource()`
   - Return array of `FHIR_URL_Results` objects

### Key Technical Details

**FHIR_URL_Results Fields**:
- `url_works` - Boolean success/failure
- `http_status` - HTTP response code
- `is_valid_json` - JSON parsing success
- `is_valid_fhir` - FHIR compliance
- `is_valid_xml` - XML detection
- `is_html_response` - HTML content detection
- `is_bundle_or_resource` - Classification
- `next_page_url` - Pagination support
- `capability_url` & `capability_url_status` - Metadata endpoint
- `smart_config_url` & `smart_config_url_status` - SMART config
- `openapi_docs_url` & `openapi_docs_url_status` - API docs
- `swagger_url` & `swagger_url_status` - Swagger docs
- `original_resource_json` - Source data
- `original_resource_id` - Resource ID
- `original_resource_type` - Resource type

**Error Handling Strategy**:
- Comprehensive try/catch blocks
- Detailed error messages in status fields
- Graceful degradation when endpoints fail
- Timeout handling for slow responses
