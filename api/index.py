from pathlib import Path
import sys

# En Vercel, el root del proyecto no incluye automaticamente backend/ en PYTHONPATH.
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
	sys.path.insert(0, str(backend_path))

from app.main import app

# Vercel serverless entrypoint.
