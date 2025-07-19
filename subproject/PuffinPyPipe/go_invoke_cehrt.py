import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "CHERT_FHIR_ENDPOINTS_DIR",
    "CHERT_FHIR_IMPORT_DATA_DIR",
    "CHERT_FHIR_DB_TYPE",
    "CHERT_FHIR_SCHEMA",
    "CHERT_FHIR_TABLE"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmd = [
    "python", "-m", "csviper", "invoke-compiled-script",
    f"--run_import_from={os.getenv('CHERT_FHIR_ENDPOINTS_DIR')}",
    f"--import_data_from_dir={os.getenv('CHERT_FHIR_IMPORT_DATA_DIR')}",
    f"--database_type={os.getenv('CHERT_FHIR_DB_TYPE')}",
    f"--db_schema_name={os.getenv('CHERT_FHIR_SCHEMA')}",
    f"--table_name={os.getenv('CHERT_FHIR_TABLE')}"
]

print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)
