import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "SQL_CREATE_TABLE_DIR",
    "SQL_MERGED_CREATE_TABLE_DIR"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmd = [
    "python", "merge_create_sql_files.py",
    "--input_dir", os.getenv("SQL_CREATE_TABLE_DIR"),
    "--output_dir", os.getenv("SQL_MERGED_CREATE_TABLE_DIR")
]

print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)
