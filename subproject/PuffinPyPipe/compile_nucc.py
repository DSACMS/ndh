import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    # Nucc nodes
    "NUCC_MERGED_CSV", "NUCC_MERGED_DIR", "NUCC_MERGED_METADATA",
    # Nucc ancestors
    "NUCC_ANCESTOR_CSV", "NUCC_ANCESTOR_DIR", "NUCC_ANCESTOR_METADATA",
    # Nucc sources
    "NUCC_SOURCES_CSV", "NUCC_SOURCES_DIR", "NUCC_SOURCES_METADATA"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmds = [
    # Nucc nodes
    [
        "csviper", "extract-metadata",
        f"--from_csv={os.getenv('NUCC_MERGED_CSV')}",
        f"--output_dir={os.getenv('NUCC_MERGED_DIR')}"
    ],
    [
        "csviper", "build-sql",
        f"--from_metadata_json={os.getenv('NUCC_MERGED_METADATA')}",
        f"--output_dir={os.getenv('NUCC_MERGED_DIR')}"
    ],
    [
        "csviper", "build-import-script",
        f"--from_resource_dir={os.getenv('NUCC_MERGED_DIR')}",
        f"--output_dir={os.getenv('NUCC_MERGED_DIR')}",
        "--overwrite_previous"
    ],
    # Nucc ancestors
    [
        "csviper", "extract-metadata",
        f"--from_csv={os.getenv('NUCC_ANCESTOR_CSV')}",
        f"--output_dir={os.getenv('NUCC_ANCESTOR_DIR')}"
    ],
    [
        "csviper", "build-sql",
        f"--from_metadata_json={os.getenv('NUCC_ANCESTOR_METADATA')}",
        f"--output_dir={os.getenv('NUCC_ANCESTOR_DIR')}"
    ],
    [
        "csviper", "build-import-script",
        f"--from_resource_dir={os.getenv('NUCC_ANCESTOR_DIR')}",
        f"--output_dir={os.getenv('NUCC_ANCESTOR_DIR')}",
        "--overwrite_previous"
    ],
    # Nucc sources
    [
        "csviper", "extract-metadata",
        f"--from_csv={os.getenv('NUCC_SOURCES_CSV')}",
        f"--output_dir={os.getenv('NUCC_SOURCES_DIR')}"
    ],
    [
        "csviper", "build-sql",
        f"--from_metadata_json={os.getenv('NUCC_SOURCES_METADATA')}",
        f"--output_dir={os.getenv('NUCC_SOURCES_DIR')}"
    ],
    [
        "csviper", "build-import-script",
        f"--from_resource_dir={os.getenv('NUCC_SOURCES_DIR')}",
        f"--output_dir={os.getenv('NUCC_SOURCES_DIR')}",
        "--overwrite_previous"
    ]
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
