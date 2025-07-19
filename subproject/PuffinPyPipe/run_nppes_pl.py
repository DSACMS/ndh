import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "NPPES_PL_CSV",
    "NPPES_RAW_SCHEMA",
    "NPPES_PL_TABLE"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmd = [
    "python", "./nppes_pl/go.postgresql.py",
    f"--csv_file={os.getenv('NPPES_PL_CSV')}",
    f"--db_schema_name={os.getenv('NPPES_RAW_SCHEMA')}",
    f"--table_name={os.getenv('NPPES_PL_TABLE')}"
]

print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)
