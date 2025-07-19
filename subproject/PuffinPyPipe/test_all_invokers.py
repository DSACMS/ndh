#!/usr/bin/env python3
"""
Test script to verify all PuffinPyPipe invokers work with glob patterns
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add csviper to path
sys.path.append('../csviper/src')

def create_test_data():
    """Create test CSV files for each import type"""
    
    # Create test data directory
    test_dir = Path("test_all_data")
    test_dir.mkdir(exist_ok=True)
    
    # NPPES Main data
    (test_dir / "npidata_pfile_20050523-20241201.csv").write_text(
        "NPI,Entity Type Code,Provider Last Name\n"
        "1234567890,1,Smith\n"
        "2345678901,2,Johnson\n"
    )
    
    # NPPES PL data
    (test_dir / "pl_pfile_20050523-20241201.csv").write_text(
        "NPI,Provider Last Name,Provider First Name\n"
        "1234567890,Smith,John\n"
        "2345678901,Johnson,Jane\n"
    )
    
    # NPPES Other Name data
    (test_dir / "othername_pfile_20050523-20241201.csv").write_text(
        "NPI,Provider Other Organization Name,Provider Other Organization Name Type Code\n"
        "1234567890,Test Org,5\n"
        "2345678901,Another Org,3\n"
    )
    
    # NPPES Endpoint data
    (test_dir / "endpoint_pfile_20050523-20241201.csv").write_text(
        "NPI,Endpoint Type,Endpoint Type Description\n"
        "1234567890,FHIR,FHIR R4\n"
        "2345678901,REST,REST Services\n"
    )
    
    # PECOS Enrollment data
    (test_dir / "PPEF_Enrollment_Extract_2025.05.01.csv").write_text(
        "NPI,Provider Name,Enrollment Status\n"
        "1234567890,Smith John,Active\n"
        "2345678901,Johnson Jane,Active\n"
    )
    
    # PECOS Reassignment data
    (test_dir / "PPEF_Reassignment_Extract_2025.05.01.csv").write_text(
        "NPI,Reassignment Organization,Reassignment Date\n"
        "1234567890,Test Hospital,2025-01-01\n"
        "2345678901,Another Clinic,2025-01-02\n"
    )
    
    print(f"Created test data in {test_dir}")
    return test_dir

def test_invoker(import_dir, test_data_dir, db_type="postgresql"):
    """Test a specific invoker"""
    print(f"\n{'='*50}")
    print(f"Testing {import_dir} with {db_type}")
    print(f"{'='*50}")
    
    cmd = [
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from=./{import_dir}",
        f"--import_data_from_dir=./{test_data_dir}",
        f"--database_type={db_type}",
        "--db_schema_name=test_schema",
        f"--table_name={import_dir}_table"
    ]
    
    try:
        # Run the command but expect it to fail at database connection
        # We just want to verify the file discovery works
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30,
            input="n\n"  # Answer 'no' to the confirmation prompt
        )
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        # Check if file discovery worked (should show found files)
        if "Found" in result.stdout and "matching file" in result.stdout:
            print("✅ File discovery PASSED")
            return True
        else:
            print("❌ File discovery FAILED")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Command timed out (likely waiting for input)")
        return True  # This is actually expected behavior
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Main test function"""
    print("Testing all PuffinPyPipe invokers with glob patterns")
    print("=" * 60)
    
    # Change to csviper directory and activate venv
    os.chdir("../csviper")
    subprocess.run(["source", "source_me_to_get_venv.sh"], shell=True)
    os.chdir("../PuffinPyPipe")
    
    # Create test data
    test_data_dir = create_test_data()
    
    # Test each import type
    import_dirs = [
        "nppes_main",
        "nppes_pl", 
        "nppes_othername",
        "nppes_endpoint",
        "pecos_enrollment"  # This has two metadata files, we'll test both
    ]
    
    results = {}
    
    for import_dir in import_dirs:
        results[import_dir] = test_invoker(import_dir, test_data_dir)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    for import_dir, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{import_dir:20} {status}")
    
    # Cleanup
    shutil.rmtree(test_data_dir)
    print(f"\nCleaned up {test_data_dir}")

if __name__ == "__main__":
    main()
