import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "NPPES_ENDPOINT_CSV",
    "NPPES_ENDPOINT_DIR",
    "NPPES_ENDPOINT_METADATA"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmds = [
    [
        "csviper", "extract-metadata",
        f"--from_csv={os.getenv('NPPES_ENDPOINT_CSV')}",
        f"--output_dir={os.getenv('NPPES_ENDPOINT_DIR')}"
    ],
    [
        "csviper", "build-sql",
        f"--from_metadata_json={os.getenv('NPPES_ENDPOINT_METADATA')}",
        f"--output_dir={os.getenv('NPPES_ENDPOINT_DIR')}",
        "--overwrite_previous"
    ],
    [
        "csviper", "build-import-script",
        f"--from_resource_dir={os.getenv('NPPES_ENDPOINT_DIR')}",
        f"--output_dir={os.getenv('NPPES_ENDPOINT_DIR')}",
        "--overwrite_previous"
    ]
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
