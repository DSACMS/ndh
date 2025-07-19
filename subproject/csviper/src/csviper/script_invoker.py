"""
Script Invoker for CSViper - Handles dynamic file discovery and script execution
"""

import os
import glob
import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
from .exceptions import CSViperError, FileSystemError, MetadataError


class CompiledScriptInvoker:
    """
    Handles discovery of data files and execution of compiled CSViper import scripts.
    """
    
    @staticmethod
    def invoke_from_directory(run_import_from: str, import_data_from_dir: str, 
                            database_type: str, db_schema_name: Optional[str] = None,
                            table_name: Optional[str] = None) -> None:
        """
        Main entry point for directory-based import invocation.
        
        Args:
            run_import_from (str): Directory containing compiled CSViper scripts and metadata
            import_data_from_dir (str): Directory to search for data files
            database_type (str): Database type ('mysql' or 'postgresql')
            db_schema_name (Optional[str]): Database schema name to pass to the import script
            table_name (Optional[str]): Table name to pass to the import script
            
        Raises:
            CSViperError: If any step of the process fails
        """
        try:
            print(f"CSViper Script Invoker")
            print(f"=" * 50)
            print(f"Import scripts directory: {run_import_from}")
            print(f"Data search directory: {import_data_from_dir}")
            print(f"Database type: {database_type}")
            print()
            
            # 1. Find and load the single metadata file
            metadata = CompiledScriptInvoker._load_directory_metadata(run_import_from)
            
            # 2. Find latest matching data file
            latest_file = CompiledScriptInvoker._find_latest_data_file(
                import_data_from_dir, 
                metadata['file_glob_pattern'],
                metadata.get('recursive_search', True)
            )
            
            # 3. Confirm with user
            if not CompiledScriptInvoker._confirm_file_selection(latest_file, metadata):
                print("Operation cancelled by user.")
                return
            
            # 4. Execute the import script
            CompiledScriptInvoker._execute_import_script(
                run_import_from, latest_file, database_type, db_schema_name, table_name
            )
            
        except Exception as e:
            raise CSViperError(f"Script invocation failed: {e}")
    
    @staticmethod
    def _load_directory_metadata(directory: str) -> Dict[str, Any]:
        """
        Find and load the single metadata.json file in directory.
        
        Args:
            directory (str): Directory to search for metadata file
            
        Returns:
            Dict[str, Any]: Loaded metadata dictionary
            
        Raises:
            MetadataError: If metadata file issues are encountered
        """
        # Find all metadata files in the directory
        metadata_pattern = os.path.join(directory, "*.metadata.json")
        metadata_files = glob.glob(metadata_pattern)
        
        if len(metadata_files) == 0:
            raise MetadataError(
                f"No metadata.json file found in directory: {directory}\n"
                f"Expected exactly one *.metadata.json file."
            )
        
        if len(metadata_files) > 1:
            raise MetadataError(
                f"Multiple metadata.json files found in directory: {directory}\n"
                f"Found: {[os.path.basename(f) for f in metadata_files]}\n"
                f"Expected exactly one *.metadata.json file."
            )
        
        metadata_file = metadata_files[0]
        print(f"Loading metadata from: {os.path.basename(metadata_file)}")
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Validate required fields for invoker functionality
            required_fields = ['file_glob_pattern']
            missing_fields = [field for field in required_fields if field not in metadata]
            
            if missing_fields:
                print(f"Warning: Metadata file missing invoker fields: {missing_fields}")
                print(f"Using fallback values...")
                
                # Provide fallback values for backward compatibility
                if 'file_glob_pattern' not in metadata:
                    if 'filename' in metadata:
                        metadata['file_glob_pattern'] = metadata['filename']
                    else:
                        raise MetadataError("Metadata file missing both 'file_glob_pattern' and 'filename' fields")
                
                if 'recursive_search' not in metadata:
                    metadata['recursive_search'] = True
            
            return metadata
            
        except json.JSONDecodeError as e:
            raise MetadataError(f"Invalid JSON in metadata file {metadata_file}: {e}")
        except Exception as e:
            raise MetadataError(f"Error reading metadata file {metadata_file}: {e}")
    
    @staticmethod
    def _find_latest_data_file(search_dir: str, pattern: str, recursive: bool) -> str:
        """
        Find the most recently modified file matching the pattern.
        
        Args:
            search_dir (str): Directory to search in
            pattern (str): Glob pattern to match files
            recursive (bool): Whether to search recursively
            
        Returns:
            str: Path to the most recently modified matching file
            
        Raises:
            FileSystemError: If no matching files are found or search fails
        """
        print(f"Searching for files matching '{pattern}' in {search_dir}...")
        
        try:
            if recursive:
                # Search recursively through subdirectories
                search_pattern = os.path.join(search_dir, "**", pattern)
                matching_files = glob.glob(search_pattern, recursive=True)
            else:
                # Search only in the top-level directory
                search_pattern = os.path.join(search_dir, pattern)
                matching_files = glob.glob(search_pattern)
            
            if not matching_files:
                raise FileSystemError(
                    f"No files found matching pattern '{pattern}' in {search_dir}\n"
                    f"Recursive search: {recursive}"
                )
            
            # Sort by modification time (newest first)
            matching_files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
            
            print(f"Found {len(matching_files)} matching file(s):")
            for i, file_path in enumerate(matching_files[:5]):  # Show up to 5 files
                mtime = os.path.getmtime(file_path)
                size = os.path.getsize(file_path)
                print(f"  {i+1}. {os.path.basename(file_path)} "
                      f"({CompiledScriptInvoker._format_file_size(size)}, "
                      f"modified: {CompiledScriptInvoker._format_timestamp(mtime)})")
            
            if len(matching_files) > 5:
                print(f"  ... and {len(matching_files) - 5} more files")
            
            return matching_files[0]  # Return the most recent file
            
        except Exception as e:
            raise FileSystemError(f"Error searching for files: {e}")
    
    @staticmethod
    def _confirm_file_selection(file_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Present file to user for confirmation.
        
        Args:
            file_path (str): Path to the selected file
            metadata (Dict[str, Any]): Metadata dictionary for context
            
        Returns:
            bool: True if user confirms, False if user cancels
        """
        print(f"\nLatest file selected:")
        print(f"  Path: {file_path}")
        print(f"  Size: {CompiledScriptInvoker._format_file_size(os.path.getsize(file_path))}")
        print(f"  Modified: {CompiledScriptInvoker._format_timestamp(os.path.getmtime(file_path))}")
        
        # Show some context from metadata
        if 'total_columns' in metadata:
            print(f"  Expected columns: {metadata['total_columns']}")
        if 'delimiter' in metadata:
            print(f"  Expected delimiter: '{metadata['delimiter']}'")
        
        print()
        
        while True:
            response = input("Use this file for import? [Y/n]: ").strip().lower()
            if response in ['', 'y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    @staticmethod
    def _execute_import_script(script_dir: str, csv_file: str, db_type: str, 
                             db_schema_name: Optional[str] = None, 
                             table_name: Optional[str] = None) -> None:
        """
        Execute go.mysql.py or go.postgresql.py with the CSV file.
        
        Args:
            script_dir (str): Directory containing the import scripts
            csv_file (str): Path to the CSV file to import
            db_type (str): Database type ('mysql' or 'postgresql')
            db_schema_name (Optional[str]): Database schema name to pass to the import script
            table_name (Optional[str]): Table name to pass to the import script
            
        Raises:
            FileSystemError: If import script is not found
            CSViperError: If script execution fails
        """
        # Determine script filename based on database type
        if db_type.lower() == 'mysql':
            script_name = 'go.mysql.py'
        elif db_type.lower() == 'postgresql':
            script_name = 'go.postgresql.py'
        else:
            raise CSViperError(f"Unsupported database type: {db_type}")
        
        script_path = os.path.join(script_dir, script_name)
        
        if not os.path.exists(script_path):
            raise FileSystemError(
                f"Import script not found: {script_path}\n"
                f"Expected to find {script_name} in {script_dir}"
            )
        
        # Build command to execute
        cmd = [sys.executable, script_path, f"--csv_file={csv_file}"]
        
        # Add optional arguments if provided
        if db_schema_name:
            cmd.append(f"--db_schema_name={db_schema_name}")
        
        if table_name:
            cmd.append(f"--table_name={table_name}")
        
        print(f"\nExecuting import script:")
        print(f"  Command: {' '.join(cmd)}")
        print(f"  Working directory: {script_dir}")
        print()
        
        try:
            # Execute the script
            result = subprocess.run(
                cmd,
                cwd=script_dir,
                capture_output=False,  # Let output go to console
                text=True
            )
            
            if result.returncode != 0:
                raise CSViperError(f"Import script failed with exit code {result.returncode}")
            
            print(f"\n✓ Import script completed successfully")
            
        except subprocess.SubprocessError as e:
            raise CSViperError(f"Error executing import script: {e}")
        except Exception as e:
            raise CSViperError(f"Unexpected error during script execution: {e}")
    
    @staticmethod
    def _format_file_size(size_bytes: float) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes (int): File size in bytes
            
        Returns:
            str: Formatted file size
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    @staticmethod
    def _format_timestamp(timestamp: float) -> str:
        """
        Format timestamp in human-readable format.
        
        Args:
            timestamp (float): Unix timestamp
            
        Returns:
            str: Formatted timestamp
        """
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
