import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "NPPES_PL_DIR",
    "NPPES_ENDPOINT_DIR",
    "NPPES_OTHERNAME_DIR",
    "NPPES_MAIN_DIR",
    "NPPES_DATA_DIR",
    "NPPES_DB_TYPE",
    "NPPES_RAW_SCHEMA",
    "NPPES_PL_TABLE",
    "NPPES_ENDPOINT_TABLE",
    "NPPES_OTHERNAME_TABLE",
    "NPPES_MAIN_TABLE"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmds = [
    [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={os.getenv('NPPES_PL_DIR')}",
        f"--import_data_from_dir={os.getenv('NPPES_DATA_DIR')}",
        f"--database_type={os.getenv('NPPES_DB_TYPE')}",
        f"--db_schema_name={os.getenv('NPPES_RAW_SCHEMA')}",
        f"--table_name={os.getenv('NPPES_PL_TABLE')}"
    ],
    [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={os.getenv('NPPES_ENDPOINT_DIR')}",
        f"--import_data_from_dir={os.getenv('NPPES_DATA_DIR')}",
        f"--database_type={os.getenv('NPPES_DB_TYPE')}",
        f"--db_schema_name={os.getenv('NPPES_RAW_SCHEMA')}",
        f"--table_name={os.getenv('NPPES_ENDPOINT_TABLE')}"
    ],
    [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={os.getenv('NPPES_OTHERNAME_DIR')}",
        f"--import_data_from_dir={os.getenv('NPPES_DATA_DIR')}",
        f"--database_type={os.getenv('NPPES_DB_TYPE')}",
        f"--db_schema_name={os.getenv('NPPES_RAW_SCHEMA')}",
        f"--table_name={os.getenv('NPPES_OTHERNAME_TABLE')}"
    ],
    [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={os.getenv('NPPES_MAIN_DIR')}",
        f"--import_data_from_dir={os.getenv('NPPES_DATA_DIR')}",
        f"--database_type={os.getenv('NPPES_DB_TYPE')}",
        f"--db_schema_name={os.getenv('NPPES_RAW_SCHEMA')}",
        f"--table_name={os.getenv('NPPES_MAIN_TABLE')}"
    ]
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    #subprocess.run(cmd, check=True)
