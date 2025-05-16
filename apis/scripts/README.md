# API Scripts

This directory contains utility scripts for managing and generating API specifications.

## Bundle APIs Script (`bundle_apis.py`)

This script bundles OpenAPI specifications into single YAML files.

### Usage

```bash
# Bundle a specific API
python bundle_apis.py <api_name>

# Bundle all available APIs
python bundle_apis.py --all
```

### Requirements
- `swagger-cli` must be installed globally

## Generate API Script (`generate_api.py`)

This script generates API client/server code from OpenAPI specifications.

### Usage

```bash
python generate_api.py --api <api_name> --project <project_name> --language <language> --mode <mode> [options]
```

### Arguments
- `--api`: Name of the API to generate
- `--project`: Project name to generate API for
- `--language`: Target language (python/typescript)
- `--mode`: Generation mode (server/client)
- `--dist-dir`: Directory containing API specifications (default: ./dist)
- `--async`: Generate async API code
- `--verbose`, `-v`: Enable verbose logging

### Requirements
- For Python generation:
  - `openapi-generator-cli` must be installed globally
- For TypeScript generation:
  - `orval` must be installed globally

### Example
```bash
# Generate Python server code
python generate_api.py --api users --project auth --language python --mode server --async

# Generate TypeScript client code
python generate_api.py --api users --project web --language typescript --mode client
``` 