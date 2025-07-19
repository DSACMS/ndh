import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "PECOS_ENROLLMENT_CSV",
    "PECOS_ENROLLMENT_DIR",
    "PECOS_ENROLLMENT_TABLE",
    "PECOS_ASSIGNMENT_CSV",
    "PECOS_ASSIGNMENT_DIR",
    "PECOS_ASSIGNMENT_TABLE",
    "PECOS_SCHEMA",
    "PECOS_DB_TYPE"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmds = [
    [
        "csviper", "full-compile",
        f"--from_csv={os.getenv('PECOS_ENROLLMENT_CSV')}",
        f"--output_dir={os.getenv('PECOS_ENROLLMENT_DIR')}",
        "--overwrite_previous"
    ],
    [
        "python", f"{os.getenv('PECOS_ENROLLMENT_DIR')}/go.postgresql.py",
        f"--csv_file", os.getenv("PECOS_ENROLLMENT_CSV"),
        f"--db_schema_name", os.getenv("PECOS_SCHEMA"),
        "--table_name", os.getenv("PECOS_ENROLLMENT_TABLE")
    ],
    [
        "csviper", "full-compile",
        f"--from_csv={os.getenv('PECOS_ASSIGNMENT_CSV')}",
        f"--output_dir={os.getenv('PECOS_ASSIGNMENT_DIR')}",
        "--overwrite_previous"
    ],
    [
        "python", f"{os.getenv('PECOS_ASSIGNMENT_DIR')}/go.postgresql.py",
        f"--csv_file", os.getenv("PECOS_ASSIGNMENT_CSV"),
        f"--db_schema_name", os.getenv("PECOS_SCHEMA"),
        f"--table_name", os.getenv("PECOS_ASSIGNMENT_TABLE")
    ]
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
