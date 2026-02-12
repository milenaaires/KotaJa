from pathlib import Path
import sys
import runpy

ROOT = Path(__file__).resolve().parent  # raiz do repo
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Executa o seu app existente como script
runpy.run_path(str(ROOT / "app" / "app.py"), run_name="__main__")
