#!/usr/bin/env python3
"""
Merge SQL statements from multiple SQL files into schema-specific files.

This script recursively searches for .sql files in the specified input directory and subdirectories,
extracts SQL statements (CREATE TABLE, CREATE INDEX, etc.), groups them by schema,
and creates separate merged files for each schema in the output directory.
It ignores any existing merged files to avoid including previous runs.
"""

import os
import re
import glob
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class SQLMerger:
    OUTPUT_FILENAME_TEMPLATE = "merged_{schema}_create_table.sql"
    DEFAULT_SCHEMA = "public"
    
    @staticmethod
    def find_sql_files(input_directory):
        """
        Recursively find all .sql files, excluding any existing merged files.
        Returns files sorted alphabetically by filename (case-insensitive).
        """
        sql_files = []
        
        # Use glob to find all .sql files recursively
        pattern = os.path.join(input_directory, "**", "*.sql")
        all_sql_files = glob.glob(pattern, recursive=True)
        
        # Filter out merged files (both old and new format)
        for file_path in all_sql_files:
            filename = os.path.basename(file_path)
            if not (filename == "_merged_.sql" or filename.startswith("merged_") and filename.endswith("_create_table.sql")):
                sql_files.append(file_path)
        
        # Sort alphabetically by filename (case-insensitive)
        return sorted(sql_files, key=lambda x: os.path.basename(x).lower())
    
    @staticmethod
    def extract_schema_from_statement(statement):
        """
        Extract schema name from a SQL statement.
        Returns schema name or DEFAULT_SCHEMA if no schema is specified.
        """
        # Look for patterns like "CREATE TABLE schema.table_name" or "CREATE INDEX schema.index_name"
        schema_pattern = r'CREATE\s+(?:TABLE|INDEX|VIEW|SEQUENCE|FUNCTION|PROCEDURE)\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\.'
        match = re.search(schema_pattern, statement, re.IGNORECASE)
        
        if match:
            return match.group(1).lower()
        
        return SQLMerger.DEFAULT_SCHEMA
    
    @staticmethod
    def extract_sql_statements(file_path):
        """
        Extract SQL statements from a SQL file.
        Handles multi-line statements and various SQL formats.
        Returns list of statements with their schemas.
        """
        statements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
            except Exception as e:
                print(f"Warning: Could not read file {file_path}: {e}")
                return statements
        except Exception as e:
            print(f"Warning: Could not read file {file_path}: {e}")
            return statements
        
        # Split content into lines for processing
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('--'):
                i += 1
                continue
            
            # Look for SQL statements (CREATE TABLE, CREATE INDEX, etc.)
            if re.match(r'^\s*CREATE\s+(?:TABLE|INDEX|VIEW|SEQUENCE|FUNCTION|PROCEDURE|SCHEMA)\s+', line, re.IGNORECASE):
                # Found start of SQL statement
                statement_lines = [lines[i]]
                i += 1
                
                # For CREATE TABLE, count parentheses to find the end
                if re.match(r'^\s*CREATE\s+TABLE\s+', line, re.IGNORECASE):
                    paren_count = line.count('(') - line.count(')')
                    
                    # Continue reading lines until we have balanced parentheses
                    while i < len(lines) and paren_count > 0:
                        current_line = lines[i]
                        statement_lines.append(current_line)
                        # Only count parentheses that are not in comments
                        line_without_comments = current_line.split('--')[0]
                        paren_count += line_without_comments.count('(') - line_without_comments.count(')')
                        i += 1
                else:
                    # For other statements, read until semicolon at end of line (not in comment)
                    while i < len(lines):
                        current_line = lines[i]
                        statement_lines.append(current_line)
                        # Check if line ends with semicolon (not in comment)
                        line_without_comments = current_line.split('--')[0].strip()
                        if line_without_comments.endswith(';'):
                            i += 1
                            break
                        i += 1
                
                # Join the statement lines
                full_statement = '\n'.join(statement_lines)
                
                # Clean up the statement (remove extra whitespace, ensure it ends with semicolon)
                full_statement = full_statement.strip()
                if not full_statement.endswith(';'):
                    full_statement += ';'
                
                # Extract schema and add to statements
                schema = SQLMerger.extract_schema_from_statement(full_statement)
                statements.append({
                    'statement': full_statement,
                    'schema': schema
                })
            else:
                i += 1
        
        return statements
    
    @staticmethod
    def process_files(input_directory):
        """
        Process all SQL files and extract SQL statements grouped by schema.
        Returns tuple of (processed_files, statements_by_schema)
        """
        sql_files = SQLMerger.find_sql_files(input_directory)
        processed_files = []
        statements_by_schema = defaultdict(list)
        
        if not sql_files:
            print("No SQL files found.")
            return processed_files, statements_by_schema
        
        print(f"Found {len(sql_files)} SQL files to process:")
        
        for file_path in sql_files:
            print(f"  Processing: {file_path}")
            statements = SQLMerger.extract_sql_statements(file_path)
            
            if statements:
                processed_files.append(file_path)
                for stmt_info in statements:
                    statements_by_schema[stmt_info['schema']].append({
                        'file': file_path,
                        'statement': stmt_info['statement']
                    })
                print(f"    Found {len(statements)} SQL statement(s)")
                
                # Show schema breakdown
                schema_counts = defaultdict(int)
                for stmt_info in statements:
                    schema_counts[stmt_info['schema']] += 1
                for schema, count in schema_counts.items():
                    print(f"      {schema}: {count} statement(s)")
            else:
                print(f"    No SQL statements found")
        
        return processed_files, statements_by_schema
    
    @staticmethod
    def generate_schema_files(processed_files, statements_by_schema, output_directory):
        """
        Generate separate merged SQL files for each schema.
        """
        if not statements_by_schema:
            print("No SQL statements found to merge.")
            return
        
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        total_statements = sum(len(statements) for statements in statements_by_schema.values())
        print(f"\nGenerating schema-specific files:")
        print(f"Total schemas found: {len(statements_by_schema)}")
        print(f"Total statements: {total_statements}")
        
        for schema, statements in statements_by_schema.items():
            # Generate filename for this schema
            filename = SQLMerger.OUTPUT_FILENAME_TEMPLATE.format(schema=schema)
            output_path = os.path.join(output_directory, filename)
            
            # Generate header with list of source files
            header = [
                f"-- Merged SQL statements for schema: {schema}",
                f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"-- Total statements for this schema: {len(statements)}",
                "--",
                "-- Source files:",
            ]
            
            # Add each source file as a separate comment line
            source_files = sorted(set(stmt['file'] for stmt in statements))
            for file_path in source_files:
                header.append(f"--   {file_path}")
            
            header.extend(["", ""])  # Add blank lines after header
            
            # Build the content
            content_lines = header.copy()
            
            # Add all SQL statements for this schema
            for item in statements:
                content_lines.append(f"-- Source: {item['file']}")
                content_lines.append(item['statement'])
                content_lines.append("")  # Add blank line after each statement
            
            # Write to output file
            try:
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write('\n'.join(content_lines))
                
                print(f"  Created: {output_path} ({len(statements)} statements)")
                
            except Exception as e:
                print(f"  Error writing {output_path}: {e}")
    
    @staticmethod
    def run(input_directory, output_directory):
        """
        Main execution method.
        """
        print("SQL Schema-based Merger")
        print("=" * 50)
        print(f"Input directory: {os.path.abspath(input_directory)}")
        print(f"Output directory: {os.path.abspath(output_directory)}")
        
        processed_files, statements_by_schema = SQLMerger.process_files(input_directory)
        SQLMerger.generate_schema_files(processed_files, statements_by_schema, output_directory)


def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description="Merge SQL statements from multiple SQL files into schema-specific files."
    )
    parser.add_argument(
        "--input_dir",
        required=True,
        help="Directory to search for SQL files"
    )
    parser.add_argument(
        "--output_dir",
        required=True,
        help="Directory where schema-specific merged files will be created"
    )
    
    args = parser.parse_args()
    
    # Validate input directory exists
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        return 1
    
    SQLMerger.run(args.input_dir, args.output_dir)
    return 0


if __name__ == "__main__":
    exit(main())
