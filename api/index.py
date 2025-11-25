"""
Vercel Serverless Function Entry Point

This file serves as the entry point for Vercel's Serverless Functions.
It imports and exports the FastAPI app from the main module.

Note: For Vercel deployment, the UPLOAD_DIR environment variable should
be set to '/tmp/uploads' since Vercel's filesystem is read-only except
for the /tmp directory. Files are written to disk temporarily and then
deleted after processing.
"""

import os
import sys
from pathlib import Path

# Set UPLOAD_DIR to /tmp for Vercel's writable directory before importing main
# This must be done before main.py is imported
if os.environ.get('VERCEL'):
    os.environ.setdefault('UPLOAD_DIR', '/tmp/uploads')

# Add the parent directory to sys.path to enable importing from main.py
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app from main module
from main import app

# Explicitly assign app for Vercel detection
# Vercel looks for 'app' or 'handler' variable in the module namespace
app = app
