import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "NUCC_MERGED_DIR",
    "NUCC_SOURCES_DIR",
    "NUCC_ANCESTOR_DIR",
    "NUCC_IMPORT_DATA_DIR",
    "NUCC_DB_TYPE",
    "NUCC_SCHEMA",
    "NUCC_MERGED_TABLE",
    "NUCC_SOURCES_TABLE",
    "NUCC_ANCESTOR_TABLE"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmds = [
    [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={os.getenv('NUCC_MERGED_DIR')}",
        f"--import_data_from_dir={os.getenv('NUCC_IMPORT_DATA_DIR')}",
        f"--database_type={os.getenv('NUCC_DB_TYPE')}",
        f"--db_schema_name={os.getenv('NUCC_SCHEMA')}",
        f"--table_name={os.getenv('NUCC_MERGED_TABLE')}"
    ],
    [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={os.getenv('NUCC_SOURCES_DIR')}",
        f"--import_data_from_dir={os.getenv('NUCC_IMPORT_DATA_DIR')}",
        f"--database_type={os.getenv('NUCC_DB_TYPE')}",
        f"--db_schema_name={os.getenv('NUCC_SCHEMA')}",
        f"--table_name={os.getenv('NUCC_SOURCES_TABLE')}"
    ],
    [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={os.getenv('NUCC_ANCESTOR_DIR')}",
        f"--import_data_from_dir={os.getenv('NUCC_IMPORT_DATA_DIR')}",
        f"--database_type={os.getenv('NUCC_DB_TYPE')}",
        f"--db_schema_name={os.getenv('NUCC_SCHEMA')}",
        f"--table_name={os.getenv('NUCC_ANCESTOR_TABLE')}"
    ]
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
