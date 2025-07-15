"""
Regenerate the OpenAPI spec for the current FastAPI app including all seeded demo endpoints and data.

Usage: Run this script after changing routes or models to refresh /docs (interfaces/openapi.json).
"""

import json
import os

from src.api.main import app

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
