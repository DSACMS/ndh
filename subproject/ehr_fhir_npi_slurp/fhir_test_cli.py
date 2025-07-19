#!/usr/bin/env python3
"""
FHIR Test CLI Tool
Processes EHR and Payer test data using FHIRResolver functionality.
"""

import argparse
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from FHIRResolver import FHIRResolver


def print_separator(title: Optional[str] = None):
    """Print a separator line with optional title."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    else:
        print("-" * 60)


def print_fhir_url_results(results: List[Any]):
    """Print FHIR URL results using the built-in __str__ method."""
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(str(result))
        print()


def process_file(file_path: str):
    """Process a single file using FHIRResolver."""
    print_separator(f"Processing File: {os.path.basename(file_path)}")
    
    try:
        # Use FHIRResolver to get resource array
        resources = FHIRResolver.get_resource_array_from(
            resource_json_file=file_path
        )
        
        if not resources:
            print("❌ No resources found in file")
            return
        
        print(f"📋 Found {len(resources)} resources")
        
        # Get endpoints from the resources
        url_results = FHIRResolver.get_endpoints_from(
            resource_json_file=file_path
        )
        
        if not url_results:
            print("❌ No URL results generated")
            return
        
        print(f"🔗 Generated {len(url_results)} URL results")
        print_separator()
        
        # Print the results
        # Until we have the parsing working without errors, lets not print the results.
        # print_fhir_url_results(url_results)
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        import traceback
        traceback.print_exc()


def process_directory(directory_path: str, file_type: Optional[str] = None):
    """Process all JSON files in a directory."""
    print_separator(f"Processing {file_type or 'FHIR'} Data Directory")
    
    path = Path(directory_path)
    if not path.exists():
        print(f"❌ Directory not found: {directory_path}")
        return
    
    json_files = list(path.glob("*.json"))
    if not json_files:
        print(f"❌ No JSON files found in {directory_path}")
        return
    
    print(f"📁 Found {len(json_files)} JSON files")
    
    for json_file in json_files:
        process_file(str(json_file))


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="FHIR Test CLI Tool - Process EHR and Payer test data using FHIRResolver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fhir_test_cli.py --all                    # Process all test data
  python fhir_test_cli.py --ehr                    # Process EHR data only
  python fhir_test_cli.py --payer                  # Process payer data only
  python fhir_test_cli.py --file data/test.json    # Process specific file
  python fhir_test_cli.py --directory /path/to/dir # Process directory
        """
    )
    
    parser.add_argument('--all', action='store_true', help='Process all test data (EHR and Payer)')
    parser.add_argument('--ehr', action='store_true', help='Process EHR test data')
    parser.add_argument('--payer', action='store_true', help='Process payer test data')
    parser.add_argument('--file', type=str, help='Process specific JSON file')
    parser.add_argument('--directory', type=str, help='Process all JSON files in directory')
    
    args = parser.parse_args()
    
    # Default to all if no specific option is selected
    if not any([args.all, args.ehr, args.payer, args.file, args.directory]):
        args.all = True
    
    print("🔬 FHIR Test CLI Tool")
    print("Using FHIRResolver for endpoint discovery and validation")
    print("=" * 60)
    
    try:
        if args.file:
            # Process single file
            process_file(args.file)
        
        elif args.directory:
            # Process directory
            process_directory(args.directory, "Custom Directory")
        
        else:
            # Process test data directories
            base_path = Path(__file__).parent / "fhir_json_test_data"
            
            if args.all or args.ehr:
                ehr_path = base_path / "ehr"
                if ehr_path.exists():
                    process_directory(str(ehr_path), "EHR")
                else:
                    print(f"❌ EHR directory not found: {ehr_path}")
            
            if args.all or args.payer:
                payer_path = base_path / "payer"
                if payer_path.exists():
                    process_directory(str(payer_path), "Payer")
                else:
                    print(f"❌ Payer directory not found: {payer_path}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
