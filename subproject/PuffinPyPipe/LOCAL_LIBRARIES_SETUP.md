# Local Libraries Setup Guide

This document explains how the PuffinPyPipe project is configured to use local development versions of the csviper and plainerflow libraries.

## Overview

The PuffinPyPipe project now uses local, editable installations of:

- **csviper** - Located at `../csviper`
- **plainerflow** - Located at `../plainerflow`

This means any changes you make to the source code of these libraries will be immediately available in the PuffinPyPipe project without needing to reinstall.

## Setup Instructions

### 1. Activate the Virtual Environment

```bash
source ./venv/bin/activate
# or use the provided script:
source ./source_me_to_get_venv.sh
```

### 2. Install Dependencies (if not already done)

```bash
pip install -r requirements.txt
```

This will install both local libraries in editable mode along with all their dependencies.

### 3. Verify Installation

Run the test script to verify everything is working:

```bash
python test_local_libraries.py
```

You should see:

```text
✓ csviper imported successfully
✓ csviper.import_executor.ImportExecutor imported successfully
✓ plainerflow imported successfully
✓ All tests passed! Local libraries are working correctly.
```

## What's Installed

The following packages are installed in editable mode:

- `csviper` (from `../csviper`)
- `plainerflow` (from `../plainerflow`)

Plus their dependencies:

- click, python-dotenv, chardet (for csviper)
- sqlalchemy (for plainerflow)
- pandas, great-expectations (for plainerflow's InLaw functionality)

## Usage

The existing scripts in the project (like `nppes_endpoint/go.mysql.py`) will automatically use the local versions of these libraries. For example:

```python
from csviper.import_executor import ImportExecutor
```

This import will use your local development version of csviper.

## Development Workflow

1. Make changes to the csviper or plainerflow source code in their respective directories
2. Changes are immediately available in PuffinPyPipe - no reinstallation needed
3. Test your changes using the existing scripts or the test script
4. Commit changes to the respective library repositories when ready

## Troubleshooting

If you encounter import errors:

1. Make sure the virtual environment is activated
2. Verify the local library directories exist at `../csviper` and `../plainerflow`
3. Run `pip list` to confirm the editable installations are present
4. Run the test script to diagnose specific issues

## File Structure

```text
/Users/ftrotter/gitgov/ftrotter/
├── csviper/                    # Local csviper library
├── plainerflow/               # Local plainerflow library
└── PuffinPyPipe/             # This project
    ├── requirements.txt       # Includes editable installs
    ├── test_local_libraries.py # Test script
    └── venv/                  # Virtual environment
```
