Create Markdown Report on Vendor compliance. 
=======

DO NOT TRY AND READ CSV FILES DIRECTLY this causes Cline to crash.
Instead do a head -100 on the file and read that result.

Please read all of the Step* files to see the progression from the public use data associated with Lantern (prod_data/fhir_endpoints.csv )
to a list of NPI encoded FHIR endpoints, along with their compliance status in (data/output_data/enriched_endpoints.csv)

Most usefully there is a stage at prod_data/list_sources_summary.csv that explictly lists the EHR vendors who are selling Certified EHR Technolocy (CEHRT).

Then we mine the URLS into JSON endpoint data, which we convert into a CSV file in data/output_data/normalized_csv_files/org_to_endpoint.csv

We drop all endpoints that do not give us both NPI records and full url endpoints for their organizations. 

Then we loop over the remaining results to see which ones are fully compliant with the open parts of the API requirments (i.e. swagger urls etc)

I would like to have a markdown generated dashboard that lists  the CEHRT vendors in order of their compliance with a scrappable FHIR ecosystem.
Please put an implementation of this in Step90_MakeCEHRTDashboard.py
Please include the following checks, as columns: 

* Reachable: Is the FHIR API listed for the CEHRT in prod_data/list_sources_summary.csv reachable?
* Has ONPI: Does the resulting JSON have organizational NPIs?
* HTTPS ORG URL: Does the resulting JSON have full https urls for organizational endpoints? (i.e https rather than uuid)
* Findable Capabilities: Do the CEHRT endpoints have Capability Statement (/metadata)
* Finalble SMART: Do the CEHRT endpoints have Smart Config (/.well-known/smart-configuration)
* Findable OpenAPI Docs: Do the CEHRT endpoints have OpenAPI docs (/api-docs)
* Findable OpenAPI JSON: Do the CEHRT endpoints have OpenAPI JSON (/openapi.json)
* Findable Swagger: Do the CEHRT endpoints have Swagger (/swagger)
* Findable Swagger JSON: Do the CEHRT endpoints have Swagger JSON (/swagger.json)

All of these things are implicitly tested for in the Step## slurping pipeline in this project.
Read the files to get clarity on precicely how to tell if a given test has been met. 

Sorting by hte number of passing tests, descending (i.e. the best vendors at the top), create a table in a new markdown file called CEHRT_FHIR_Report.md in the main directory. 
Use shield.io badges to list the status of the issue in each cell, For instance the first cell results should be: 

Reachable: https://img.shields.io/badge/Reachablee-green?style=for-the-badge
Un-Reachable: https://img.shields.io/badge/'Not Reachablee'-red?style=for-the-badge

And so on. 
