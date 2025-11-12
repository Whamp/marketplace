#!/usr/bin/env python3
"""
PocketBase Data Import Script

Imports data from JSON export files back into PocketBase.
Useful for restores and migrations.

Usage:
    python import_data.py <pocketbase_url> <import_dir>

Example:
    python import_data.py http://127.0.0.1:8090 pocketbase_export
"""

import sys
import json
import requests
import os
from pathlib import Path

def import_collection(base_url, collection_name, import_file):
    """Import records to a collection from JSON file."""
    with open(import_file, 'r') as f:
        data = json.load(f)

    records = data.get('items', [])
    if not records:
        print(f"  No records found in {collection_name}")
        return True

    success_count = 0
    for record in records:
        # Remove system fields that shouldn't be imported
        record.pop('id', None)
        record.pop('created', None)
        record.pop('updated', None)

        url = f"{base_url}/api/collections/{collection_name}/records"
        response = requests.post(url, json=record)

        if response.status_code in [200, 201]:
            success_count += 1
        else:
            print(f"  ✗ Failed to import record: {response.status_code} - {response.text}")

    print(f"  ✓ Imported {success_count}/{len(records)} records to {collection_name}")
    return success_count == len(records)

def main():
    if len(sys.argv) < 3:
        print("Usage: python import_data.py <pocketbase_url> <import_dir>")
        print("Example: python import_data.py http://127.0.0.1:8090 pocketbase_export")
        sys.exit(1)

    base_url = sys.argv[1].rstrip('/')
    import_dir = sys.argv[2]

    if not Path(import_dir).exists():
        print(f"Error: Directory {import_dir} does not exist")
        sys.exit(1)

    json_files = list(Path(import_dir).glob("*.json"))

    if not json_files:
        print(f"Error: No JSON files found in {import_dir}")
        sys.exit(1)

    print(f"Importing to {base_url} from {import_dir}/")
    print("-" * 50)

    success_count = 0
    for json_file in sorted(json_files):
        collection_name = json_file.stem
        if import_collection(base_url, collection_name, json_file):
            success_count += 1

    print("-" * 50)
    print(f"Import complete: {success_count}/{len(json_files)} collections imported")

if __name__ == "__main__":
    main()
