#!/usr/bin/env python3
"""
Step90_MakeCEHRTDashboard.py

Generates a markdown dashboard (CEHRT_FHIR_Report.md) listing CEHRT vendors in order of their compliance
with a scrappable FHIR ecosystem, using shield.io badges for each compliance check.

- Reads prod_data/list_sources_summary.csv for vendor info.
- Reads data/output_data/enriched_endpoints.csv for endpoint compliance.
- Aggregates compliance per vendor.
- Outputs CEHRT_FHIR_Report.md in the project root.

See AI_Instructions/CreateEHrVendorMarkdownReport.md for details.
"""

import csv
import os
from urllib.parse import urlparse

# TODO lets replace the word-based table with perfectly square icons use the icon_img_height and width variables to display all of the images in the same size. 
# Replace all failing displays with a the ./icons/red_x.png
# Replace the successful icons using the icons listed below in the comments to the CHECKS variable. 

icon_img_height = 200
icon_img_width = 200

# Compliance checks and their markdown column names
# Use short column names for headings and icon mapping
CHECKS = [
    ("Up", "reachable"), # ./icons/green_check.png
    ("ONPI", "has_onpi"), # ./icons/green_check.png
    ("HTTPS", "https_org_url"), # ./icons/green_fire_org_endpoint.200.png
    ("Metadata", "capability_url"),  # ./icons/green_fire_metadata.200.png
    ("SMART", "smart_url"), # ./icons/green_fire_smart.200.png
    ("OpenAPI Docs", "openapi_docs_url"), # ./icons/green_fire_openapi.200.png
    ("OpenAPI JSON", "openapi_json_url"), # ./icons/green_fire_openapi.200.png
    ("Swagger", "swagger_url"), # ./icons/green_fire_swagger.200.png
    ("Swagger JSON", "swagger_json_url"), # ./icons/green_fire_swagger.200.png
]

# Icon mapping for passing checks (short keys)
PASS_ICONS = {
    "Up": "./icons/green_check.png",
    "ONPI": "./icons/green_check.png",
    "HTTPS": "./icons/green_fire_org_endpoint.200.png",
    "Metadata": "./icons/green_fire_metadata.200.png",
    "SMART": "./icons/green_fire_smart.200.png",
    "OpenAPI Docs": "./icons/green_fire_openapi.200.png",
    "OpenAPI JSON": "./icons/green_fire_openapi.200.png",
    "Swagger": "./icons/green_fire_swagger.200.png",
    "Swagger JSON": "./icons/green_fire_swagger.200.png",
}
FAIL_ICON = "./icons/red_x.png"

def get_base_domain(url):
    """Extract scheme://netloc from a URL."""
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return url

def load_vendor_mapping(list_sources_path):
    """
    Returns a dict mapping base domain (scheme://netloc) to certified_api_developer_name.
    If multiple list_sources share a domain, the last one wins.
    """
    mapping = {}
    with open(list_sources_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            list_source = row.get("list_source", "").strip()
            vendor = row.get("certified_api_developer_name", "").strip()
            if list_source.startswith("http"):
                base = get_base_domain(list_source)
                mapping[base] = vendor if vendor else "Unknown, missing from list_sources_summary.csv"
    return mapping

def is_https_url(url):
    return url.startswith("https://")

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

def check_reachable(row):
    # If any of the endpoint checks is a valid URL, consider it reachable
    for col in [
        "capability_url", "smart_url", "openapi_docs_url",
        "openapi_json_url", "swagger_url", "swagger_json_url"
    ]:
        if is_valid_url(row.get(col, "")):
            return True
    return False

def check_has_onpi(row):
    # If NPI is a non-empty string of digits, consider it present
    npi = row.get("npi", "").strip()
    return npi.isdigit() and len(npi) > 0

def check_https_org_url(row):
    # If org_fhir_url is https, consider it compliant
    return is_https_url(row.get("org_fhir_url", ""))

def check_endpoint_found(row, col):
    # If the value is a valid URL, consider it found
    return is_valid_url(row.get(col, ""))

# Updated to accept org_to_npi_path as a parameter and implement correct logic
def aggregate_vendor_compliance(enriched_path, org_to_npi_path, vendor_map):
    """
    Returns a dict: vendor_name -> {check_name: bool, ...}
    Implements logic:
    - For orgs in org_to_npi.csv but not in enriched_endpoints.csv, use Step50 logic for first three columns.
    - For orgs in enriched_endpoints.csv, use normal logic.
    - If vendor has no org_id in either: all fail.
    """
    import re
    import requests

    def is_valid_npi(npi_value):
        return bool(re.match(r'^\d{10}$', npi_value.strip()))

    def is_valid_https_url(url):
        return url.strip().startswith('https://')

    def is_domain_responsive(base_domain):
        try:
            response = requests.get(base_domain, timeout=10, allow_redirects=True)
            return 200 <= response.status_code < 500
        except Exception:
            return False

    # 1. Parse org_to_npi.csv and collect per-vendor org info
    org_to_npi = {}
    org_to_npi_rows = []
    with open(org_to_npi_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            org_id = row.get("org_id", "").strip()
            npi_value = row.get("npi_value", "").strip()
            base = get_base_domain(org_id)
            vendor = vendor_map.get(base, "Unknown, missing from list_sources_summary.csv")
            org_to_npi_rows.append((vendor, org_id, npi_value))
            if vendor not in org_to_npi:
                org_to_npi[vendor] = []
            org_to_npi[vendor].append((org_id, npi_value))

    # 2. Parse enriched_endpoints.csv
    org_in_enriched = {}
    with open(enriched_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            org_url = row.get("org_fhir_url", "").strip()
            base = get_base_domain(org_url)
            vendor = vendor_map.get(base, "Unknown, missing from list_sources_summary.csv")
            if vendor not in org_in_enriched:
                org_in_enriched[vendor] = set()
            org_in_enriched[vendor].add(org_url)

    # 3. Aggregate compliance
    vendor_results = {}

    # First, handle vendors with orgs in enriched_endpoints.csv (normal logic)
    with open(enriched_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            org_url = row.get("org_fhir_url", "").strip()
            base = get_base_domain(org_url)
            vendor = vendor_map.get(base, "Unknown, missing from list_sources_summary.csv")
            if vendor not in vendor_results:
                vendor_results[vendor] = {c[0]: False for c in CHECKS}
                vendor_results[vendor]["_count"] = 0  # For sorting

            # Evaluate all checks for this row
            checks = {
                "Reachable": check_reachable(row),
                "Has ONPI": check_has_onpi(row),
                "HTTPS ORG URL": check_https_org_url(row),
                "Findable Metadata": check_endpoint_found(row, "capability_url"),
                "Findable SMART": check_endpoint_found(row, "smart_url"),
                "Findable OpenAPI Docs": check_endpoint_found(row, "openapi_docs_url"),
                "Findable OpenAPI JSON": check_endpoint_found(row, "openapi_json_url"),
                "Findable Swagger": check_endpoint_found(row, "swagger_url"),
                "Findable Swagger JSON": check_endpoint_found(row, "swagger_json_url"),
            }
            # If any endpoint for this vendor passes a check, mark as True
            for k, v in checks.items():
                if v:
                    vendor_results[vendor][k] = True

    # Next, handle vendors with orgs in org_to_npi.csv but not in enriched_endpoints.csv
    for vendor in org_to_npi:
        if vendor not in vendor_results:
            # For each org_id, check the three criteria
            reachable = False
            has_onpi = False
            https_org_url = False
            for org_id, npi_value in org_to_npi[vendor]:
                # Reachable: base domain is responsive
                base_domain = get_base_domain(org_id)
                if is_domain_responsive(base_domain):
                    reachable = True
                # Has ONPI: valid 10-digit NPI
                if is_valid_npi(npi_value):
                    has_onpi = True
                # HTTPS ORG URL: starts with https://
                if is_valid_https_url(org_id):
                    https_org_url = True
            vendor_results[vendor] = {c[0]: False for c in CHECKS}
            vendor_results[vendor]["Reachable"] = reachable
            vendor_results[vendor]["Has ONPI"] = has_onpi
            vendor_results[vendor]["HTTPS ORG URL"] = https_org_url
            vendor_results[vendor]["_count"] = sum([reachable, has_onpi, https_org_url])

    # Count number of passing checks for sorting (for those with real data)
    for vendor in vendor_results:
        vendor_results[vendor]["_count"] = sum(
            vendor_results[vendor][c[0]] for c in CHECKS
        )
    return vendor_results

# (write_markdown_report function removed; all HTML table logic is now in main())

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(base_dir, "CEHRT_FHIR_Report.csv")
    output_path = os.path.join(base_dir, "CEHRT_FHIR_Report.md")

    # Read CSV
    vendor_results = []
    with open(input_csv, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vendor_results.append(row)

    one_space = '&nbsp;'
    how_many_spaces = 15
    the_spaces = one_space * how_many_spaces

    # HTML table header
    html = []
    html.append("<table>")
    html.append("  <thead>")
    html.append("    <tr>")
    for col in vendor_results[0].keys():
        html.append(f"      <th>{the_spaces}<br>{col}</th>")
    html.append("    </tr>")
    html.append("  </thead>")
    html.append("  <tbody>")

    # Map CSV column names to PASS_ICONS keys
    CSV_TO_ICON_KEY = {
        "Reachable": "Up",
        "Has ONPI": "ONPI",
        "HTTPS ORG URL": "HTTPS",
        "Findable Metadata": "Metadata",
        "Findable SMART": "SMART",
        "Findable OpenAPI Docs": "OpenAPI Docs",
        "Findable OpenAPI JSON": "OpenAPI JSON",
        "Findable Swagger": "Swagger",
        "Findable Swagger JSON": "Swagger JSON",
    }

    for row in vendor_results:
        html.append("    <tr>")
        for col, val in row.items():
            if col == "Vendor":
                html.append(f"      <td>{val}</td>")
            else:
                # Check if value is a URL (starts with http) or boolean string
                is_url = val.startswith("http://") or val.startswith("https://")
                is_passed = val == "True" or is_url
                
                icon_key = CSV_TO_ICON_KEY.get(col, "Up")
                icon_path = PASS_ICONS.get(icon_key, PASS_ICONS["Up"]) if is_passed else FAIL_ICON
                alt_text = f"{col}: {'Pass' if is_passed else 'Fail'}"
                
                if is_url:
                    # Make icon clickable link to the actual endpoint
                    html.append(f'      <td style="text-align:center; vertical-align:middle;">'
                                f'<a href="{val}" target="_blank" rel="noopener noreferrer">'
                                f'<img src="{icon_path}" alt="{alt_text}" title="Click to visit: {val}" ></a></td>')
                else:
                    # Regular icon without link
                    html.append(f'      <td style="text-align:center; vertical-align:middle;">'
                                f'<img src="{icon_path}" alt="{alt_text}" title="{alt_text}" ></td>')
        html.append("    </tr>")
    html.append("  </tbody>")
    html.append("</table>")

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# CEHRT FHIR Vendor Compliance Dashboard\n\n")
        f.write("This dashboard lists CEHRT vendors in order of their compliance with a scrappable FHIR ecosystem. Each column represents a compliance check, and each cell shows a shield.io badge indicating pass (green) or fail (red).\n\n")
        for line in html:
            f.write(line + "\n")

    print(f"Dashboard written to {output_path}")

if __name__ == "__main__":
    main()
