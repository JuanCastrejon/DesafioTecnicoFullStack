from pathlib import Path
import os
import sys

# Hace reproducibles los imports del paquete app sin depender de PYTHONPATH externo.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# Para pruebas unitarias locales, el fallback se habilita de forma explicita.
os.environ.setdefault("ENABLE_IN_MEMORY_FALLBACK", "true")
