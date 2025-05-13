#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from pathlib import Path

def ensure_dist_dir():
    """Ensure the dist directory exists"""
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    return dist_dir

def bundle_api(api_name):
    """Bundle a single API specification"""
    input_file = Path(f"{api_name}/{api_name}.yml")
    output_file = Path("dist") / f"{api_name}.yml"
    
    if not input_file.exists():
        print(f"Error: API specification not found at {input_file}")
        return False
    
    try:
        cmd = [
            "swagger-cli", "bundle",
            str(input_file),
            "--outfile", str(output_file),
            "--type", "yaml"
        ]
        subprocess.run(cmd, check=True)
        print(f"Successfully bundled {api_name} to {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error bundling {api_name}: {e}")
        return False

def get_available_apis():
    """Get list of available APIs by looking for .yml files"""
    apis = []
    for item in Path(".").iterdir():
        if item.is_dir() and (item / f"{item.name}.yml").exists():
            apis.append(item.name)
    return apis

def main():
    parser = argparse.ArgumentParser(description="Bundle OpenAPI specifications")
    parser.add_argument("api_name", nargs="?", help="Name of the API to bundle")
    parser.add_argument("--all", action="store_true", help="Bundle all available APIs")
    args = parser.parse_args()

    if not args.api_name and not args.all:
        parser.print_help()
        sys.exit(1)

    ensure_dist_dir()

    if args.all:
        apis = get_available_apis()
        if not apis:
            print("No APIs found to bundle")
            sys.exit(1)
        
        success = True
        for api in apis:
            if not bundle_api(api):
                success = False
        sys.exit(0 if success else 1)
    else:
        if not bundle_api(args.api_name):
            sys.exit(1)

if __name__ == "__main__":
    main() 