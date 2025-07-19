import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "NPPES_PL_CSV",
    "NPPES_PL_DIR"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmd = [
    "csviper", "full-compile",
    f"--overwrite_previous",
    f"--from_csv={os.getenv('NPPES_PL_CSV')}",
    f"--output_dir={os.getenv('NPPES_PL_DIR')}"
]

print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)
