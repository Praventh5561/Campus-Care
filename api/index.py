"""
Vercel serverless entry point for CampusCare22 FastAPI app.
Vercel looks for an ASGI/WSGI app exported from api/index.py
"""
import sys
import os

# Add project root to Python path so backend imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.server import app  # noqa: F401 — Vercel uses 'app' as the handler
