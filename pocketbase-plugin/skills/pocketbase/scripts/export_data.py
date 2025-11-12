#!/usr/bin/env python3
"""
PocketBase Data Export Script

Exports all collections from a PocketBase instance to JSON files.
Useful for backups and migrations.

Usage:
    python export_data.py <pocketbase_url>

Example:
    python export_data.py http://127.0.0.1:8090
"""

import sys
import json
import requests
import os
from pathlib import Path

def export_collection(base_url, collection_name, output_dir):
    """Export a single collection to JSON file."""
    url = f"{base_url}/api/collections/{collection_name}/records"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        output_path = Path(output_dir) / f"{collection_name}.json"

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Exported {collection_name}: {len(data.get('items', []))} records")
        return True
    else:
        print(f"✗ Failed to export {collection_name}: {response.status_code}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python export_data.py <pocketbase_url> [output_dir]")
        print("Example: python export_data.py http://127.0.0.1:8090")
        sys.exit(1)

    base_url = sys.argv[1].rstrip('/')
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "pocketbase_export"

    # Common collections to export
    collections = [
        "users",
        "posts",
        "comments",
        "products",
        "orders"
    ]

    Path(output_dir).mkdir(exist_ok=True)

    print(f"Exporting from {base_url} to {output_dir}/")
    print("-" * 50)

    success_count = 0
    for collection in collections:
        if export_collection(base_url, collection, output_dir):
            success_count += 1

    print("-" * 50)
    print(f"Export complete: {success_count}/{len(collections)} collections exported")
    print(f"Output saved to: {output_dir}/")

if __name__ == "__main__":
    main()
