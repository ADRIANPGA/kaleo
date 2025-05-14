#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import subprocess
import sys
import re
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Literal

# Add parent directory to path to allow importing from apis
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class Language(Enum):
    PYTHON = "python"
    TYPESCRIPT = "typescript"

class Mode(Enum):
    SERVER = "server"
    CLIENT = "client"

class GeneratorType(Enum):
    OPENAPI = "openapi"
    ORVAL = "orval"

# Type definitions for better type checking
ApiName = str
ProjectName = str
LanguageType = Literal["python", "typescript"]
ModeType = Literal["server", "client"]

# Configuration mapping
LANGUAGE_CONFIGS: Dict[Language, Dict] = {
    Language.PYTHON: {
        "generator": GeneratorType.OPENAPI,
        "generator_name": "python-fastapi",
        "output_dir": "code",
        "package_prefix": "kaleo",
        "import_replacements": {
            "openapi_server": "{package_name}"
        },
        "async_config": {
            "additional_properties": [
                "sourceFolder=/",
                "asyncServer=true",
                "packageName={package_name}",
                "projectName={project_name}",
                "packageVersion=1.0.0"
            ]
        }
    },
    Language.TYPESCRIPT: {
        "generator": GeneratorType.ORVAL,
        "output_dir": "code",
        "config_file": "orval.config.js"
    }
}

def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate API code for specified project and type")
    parser.add_argument("--api", type=str, required=True, help="Name of the API to generate")
    parser.add_argument("--project", type=str, required=True, help="Project name to generate API for")
    parser.add_argument("--language", type=str, choices=[lang.value for lang in Language], required=True, help="Target language")
    parser.add_argument("--mode", type=str, choices=[mode.value for mode in Mode], required=True, help="Generation mode (server/client)")
    parser.add_argument("--dist-dir", type=str, default="./../dist", help="Directory containing API specifications")
    parser.add_argument("--async", action="store_true", help="Generate async API code")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

def find_api_spec(api_name: str, dist_dir: str) -> Optional[str]:
    """Find the OpenAPI specification file for the given API."""
    logger.info(f"Searching for API specification for '{api_name}' in '{dist_dir}'")
    
    # First try direct match in dist directory
    direct_paths = [
        os.path.join(dist_dir, f"{api_name}.yml"),
        os.path.join(dist_dir, f"{api_name}.yaml"),
        os.path.join(dist_dir, f"{api_name}.json")
    ]
    
    for path in direct_paths:
        if os.path.exists(path):
            logger.info(f"Found API specification at: {path}")
            return path

    # Then try subdirectory match
    subdir_paths = [
        os.path.join(dist_dir, api_name, "open_api.yml"),
        os.path.join(dist_dir, api_name, "openapi.yml"),
        os.path.join(dist_dir, api_name, "swagger.yml"),
        os.path.join(dist_dir, api_name, "swagger.yaml")
    ]
    
    for path in subdir_paths:
        if os.path.exists(path):
            logger.info(f"Found API specification at: {path}")
            return path

    # Try with hyphenated name
    hyphenated_name = api_name.replace("_", "-")
    hyphenated_paths = [
        os.path.join(dist_dir, f"{hyphenated_name}.yml"),
        os.path.join(dist_dir, f"{hyphenated_name}.yaml"),
        os.path.join(dist_dir, f"{hyphenated_name}.json")
    ]
    
    for path in hyphenated_paths:
        if os.path.exists(path):
            logger.info(f"Found API specification at: {path}")
            return path

    logger.error(f"No API specification found for '{api_name}' in '{dist_dir}'")
    return None

def generate_with_openapi(
    api_name: str,
    input_file: str,
    output_folder: str,
    final_folder: str,
    package_name: str,
    import_replacements: Dict[str, str],
    is_async: bool = False,
    project_name: str = None
) -> bool:
    """Generate API using OpenAPI Generator."""
    logger.info(f"Generating Python API using OpenAPI Generator")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output folder: {output_folder}")
    logger.info(f"Final folder: {final_folder}")
    logger.info(f"Package name: {package_name}")
    logger.info(f"Async mode: {is_async}")

    # Ensure directories exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(final_folder, exist_ok=True)

    # Prepare additional properties
    additional_props = ["sourceFolder=/"]
    if is_async:
        additional_props.extend([
            "asyncServer=true",
            f"packageName={package_name}",
            f"projectName={project_name or api_name}",
            "packageVersion=1.0.0"
        ])
    logger.debug(f"Additional properties: {additional_props}")

    # Generate API files using openapi-generator-cli
    cmd = [
        "openapi-generator-cli",
        "generate",
        "-g", "python-fastapi",
        "-i", input_file,
        "-o", output_folder,
        "--package-name", package_name,
        "--additional-properties", ",".join(additional_props)
    ]
    logger.info(f"Running command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Failed to generate API files: {result.stderr}")
        return False

    logger.info("API files generated successfully")

    # Clean up existing content
    if os.path.exists(final_folder):
        logger.info(f"Cleaning up existing content in {final_folder}")
        shutil.rmtree(final_folder)
    os.makedirs(final_folder)

    # Copy generated files
    generated_api_folder = os.path.join(output_folder, package_name)
    if os.path.exists(generated_api_folder):
        logger.info(f"Copying generated files from {generated_api_folder} to {final_folder}")
        for item in os.listdir(generated_api_folder):
            s = os.path.join(generated_api_folder, item)
            d = os.path.join(final_folder, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
            else:
                shutil.copytree(s, d)

    # Clean up imports in Python files
    logger.info("Cleaning up imports in Python files")
    for root, _, files in os.walk(final_folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                for old, new in import_replacements.items():
                    # Format the replacement with the actual package name
                    formatted_new = new.format(package_name=package_name)
                    content = content.replace(old, formatted_new)

                # Replace 'from <package>.models.object import object' with 'from pydantic import BaseModel'
                # and update class inheritance to BaseModel for generated models.
                content = re.sub(r"from\s+[\w.]+\.models\.object\s+import\s+object",
                                 "from pydantic import BaseModel",
                                 content)

                content = re.sub(r"class\s+(\w+)\(object\):",
                                 "class \\1(BaseModel):",
                                 content)

                with open(file_path, 'w') as f:
                    f.write(content)

    # Create __init__.py
    init_file = os.path.join(final_folder, "__init__.py")
    Path(init_file).touch()
    logger.info(f"Created {init_file}")

    # Clean up temporary folder
    logger.info(f"Cleaning up temporary folder {output_folder}")
    shutil.rmtree(output_folder)

    # Delete openapitools.json from the script's directory
    openapitools_json_path = Path(__file__).parent / "openapitools.json"
    if openapitools_json_path.exists():
        try:
            os.remove(openapitools_json_path)
            logger.info(f"Successfully deleted {openapitools_json_path}")
        except OSError as e:
            logger.error(f"Error deleting {openapitools_json_path}: {e}")
            
    return True

def generate_with_orval(
    api_name: str,
    input_file: str,
    output_folder: str,
    config_file: str,
    is_async: bool = False
) -> bool:
    """Generate API using Orval."""
    logger.info(f"Generating TypeScript API using Orval")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output folder: {output_folder}")
    logger.info(f"Config file: {config_file}")
    logger.info(f"Async mode: {is_async}")

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Generate API using Orval
    cmd = [
        "orval",
        "--input", input_file,
        "--output", output_folder,
        "--config", config_file
    ]

    if is_async:
        cmd.extend(["--async"])

    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Failed to generate web API files: {result.stderr}")
        return False

    logger.info("API files generated successfully")
    return True

def generate_api(
    api_name: str,
    project: str,
    language: Language,
    mode: Mode,
    dist_dir: str,
    is_async: bool = False
) -> None:
    """Main API generation function."""
    logger.info(f"Starting API generation for:")
    logger.info(f"  API: {api_name}")
    logger.info(f"  Project: {project}")
    logger.info(f"  Language: {language.value}")
    logger.info(f"  Mode: {mode.value}")
    logger.info(f"  Async: {is_async}")

    # Find API specification
    input_file = find_api_spec(api_name, dist_dir)
    if not input_file:
        logger.error(f"Could not find API specification for {api_name} in {dist_dir}")
        return

    # Get language configuration
    config = LANGUAGE_CONFIGS[language]
    logger.info(f"Using generator: {config['generator'].value}")
    
    # Setup paths
    project_path = Path(__file__).parent.parent.parent / "services" / project
    output_folder = project_path / config["output_dir"]
    logger.info(f"Output will be placed in: {output_folder}")
    
    if config["generator"] == GeneratorType.OPENAPI:
        # Format API name: replace hyphens with underscores and add _api_{mode}
        formatted_api_name = f"{api_name.replace('-', '_')}_api_{mode.value}"
        temp_folder = Path(__file__).parent / "tmp" / "generated"
        package_name = formatted_api_name  # Remove the package_prefix to avoid duplication
        success = generate_with_openapi(
            api_name,
            input_file,
            str(temp_folder),
            str(output_folder / formatted_api_name),
            package_name,
            config.get("import_replacements", {}),
            is_async,
            project
        )
    else:  # ORVAL
        success = generate_with_orval(
            api_name,
            input_file,
            str(output_folder / api_name),
            config["config_file"],
            is_async
        )

    if success:
        logger.info(f"API files successfully generated in {output_folder}")
    else:
        logger.error("API generation failed")

def main():
    args = setup_argparse()
    
    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        language = Language(args.language)
        mode = Mode(args.mode)
    except ValueError as e:
        logger.error(f"Invalid language or mode: {e}")
        return

    generate_api(
        args.api,
        args.project,
        language,
        mode,
        args.dist_dir,
        getattr(args, 'async', False)
    )

if __name__ == "__main__":
    main() 