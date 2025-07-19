#!/bin/bash
# Run each ETL step in order, explicitly listed

set -e  # Exit immediately if a command exits with a non-zero status

cd "$(dirname "$0")"

echo "Running Step05_fix_column_types.py"
python3 Step05_fix_column_types.py

echo "Running Step07_generate_row_hashes.py"
python3 Step07_generate_row_hashes.py

echo "Running Step10_NormalizePhones.py"
python3 Step10_NormalizePhones.py

echo "Running Step15_populate_core_npi_tables.py"
python3 Step15_populate_core_npi_tables.py

echo "Running Step16_verify_core_npi_tables.py"
python3 Step16_verify_core_npi_tables.py

echo "Running Step20_create_npi_indexes.py"
python3 Step20_create_npi_indexes.py

echo "Running Step30_pecos_knows_clinical_orgs.py"
python3 Step30_pecos_knows_clinical_orgs.py

echo "Running Step35_pecos_knows_reassignment.py"
python3 Step35_pecos_knows_reassignment.py

