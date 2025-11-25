"""
Vercel Serverless Function Entry Point

This file serves as the entry point for Vercel's Serverless Functions.
It imports and exports the FastAPI app from the main module.

Note: For Vercel deployment, the UPLOAD_DIR in main.py uses the default
'uploads' directory which works because files are processed in memory
and cleaned up immediately after use.
"""

import sys
from pathlib import Path

# Add the parent directory to sys.path to enable importing from main.py
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app from main module
from main import app

# Export the app for Vercel
# Vercel looks for an 'app' or 'handler' variable
