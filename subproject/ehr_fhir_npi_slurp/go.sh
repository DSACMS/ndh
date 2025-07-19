#!/bin/bash

# EHR FHIR NPI Slurp Pipeline
# Complete data processing pipeline for FHIR endpoint analysis

set -e  # Exit on any error

echo "Starting EHR FHIR NPI Slurp Pipeline..."
echo "========================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Warning: Virtual environment not detected. Consider running:"
    echo "source source_me_to_get_venv.sh"
    echo ""
fi

# Step 1: Extract list sources from Lantern CSV
echo "Step 1: Extracting list sources from Lantern CSV..."
python Step10_extract_list_source_from_lantern_csv.py \
    --input_file prod_data/fhir_endpoints.csv \
    --output_file prod_data/list_sources_summary.csv

echo "✓ Step 1 completed"
echo ""

# Step 2: Download service JSON files
echo "Step 2: Downloading service JSON files..."
python Step20_download_list_source_json.py \
    --input_file ./prod_data/list_sources_summary.csv \
    --output_dir ./data/service_json/ \
    --delay 1.0

echo "✓ Step 2 completed"
echo ""

# Step 3: Parse FHIR bundles
echo "Step 3: Parsing FHIR bundles..."
python Step30_parse_source_bundle.py --input_dir ./data/service_json/

echo "✓ Step 3 completed"
echo ""

# Step 4: Extract and normalize CSV data
echo "Step 4: Extracting and normalizing CSV data..."
python Step40_extract_csv_data.py

echo "✓ Step 4 completed"
echo ""

# Step 5: Clean and validate org_to_npi data
echo "Step 5: Cleaning and validating org_to_npi data..."
echo "  - Filtering for valid HTTPS URLs and 10-digit NPI numbers"
echo "  - Checking domain responsiveness"
echo "  - Outputting clean data for further processing"
python Step50_simple_clean_output.py \
    --input_file data/output_data/normalized_csv_files/org_to_npi.csv \
    --output_file data/output_data/clean_npi_to_org_fhir_url.csv

echo "✓ Step 5 completed"
echo ""

# Step 6: Discover FHIR endpoints at multiple directory levels
echo "Step 6: Discovering FHIR endpoints..."
echo "  - Testing multiple directory levels for each domain"
echo "  - Looking for: Capability Statement, SMART Config, OpenAPI, Swagger"
echo "  - Enriching data with endpoint discovery results"
python Step60_CalculateOpenEndpoints.py \
    --input_csv_file data/output_data/clean_npi_to_org_fhir_url.csv \
    --output_csv_file data/output_data/enriched_endpoints.csv

echo "✓ Step 6 completed"
echo ""

# Step 89: Generate CEHRT Dashboard CSV
echo "Step 89: Generating CEHRT compliance dashboard CSV..."
echo "  - Aggregating compliance results per vendor"
echo "  - Reading vendor mapping from list_sources_summary.csv"
echo "  - Combining endpoint discovery with partial compliance data"
echo "  - Creating dashboard input CSV"
python Step89_GenerateCEHRTDashboardCSV.py

echo "✓ Step 89 completed"
echo ""

# Step 90: Create CEHRT Dashboard Markdown Report
echo "Step 90: Creating CEHRT dashboard markdown report..."
echo "  - Converting CSV compliance data to visual dashboard"
echo "  - Using icons for pass/fail status visualization"
echo "  - Generating CEHRT_FHIR_Report.md"
python Step90_MakeCEHRTDashboard.py

echo "✓ Step 90 completed"
echo ""

echo "========================================"
echo "Pipeline completed successfully!"
echo ""
echo "Output files are available in:"
echo "  - ./data/output_data/normalized_csv_files/ (raw extracted data)"
echo "  - ./data/output_data/clean_npi_to_org_fhir_url.csv (cleaned org/NPI data)"
echo "  - ./data/output_data/enriched_endpoints.csv (with FHIR endpoint discovery)"
echo "  - ./CEHRT_FHIR_Report.csv (compliance summary by vendor)"
echo "  - ./CEHRT_FHIR_Report.md (visual compliance dashboard)"
echo ""
echo "Key deliverables:"
echo "  - CEHRT_FHIR_Report.md: Visual dashboard showing vendor compliance"
echo "  - enriched_endpoints.csv: Complete dataset with endpoint discovery"
echo ""
echo "Additional options:"
echo "  - Run tests: python test_pipeline.py"
echo "  - Test mode (faster): python Step40_extract_csv_data.py --test"
echo "  - View dashboard: open CEHRT_FHIR_Report.md"
