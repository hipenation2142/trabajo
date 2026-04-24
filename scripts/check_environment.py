"""Comprobación básica del entorno de desarrollo del TFG.

Este script permite verificar que las librerías principales se importan correctamente
y, también que la estructura mínima del repositorio ya está creada (y, por tanto, disponible).

Se debe ejecutar desde la raíz del proyecto mediante:

    python scripts/check_environment.py
"""

from __future__ import annotations

import importlib
import importlib.metadata as metadata
import platform
import sys
from pathlib import Path

PACKAGES = {
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "scipy": "scipy",
    "statsmodels": "statsmodels",
    "scikit-learn": "sklearn",
    "lightgbm": "lightgbm",
    "catboost": "catboost",
    "mapie": "mapie",
    "skforecast": "skforecast",
    "pyarrow": "pyarrow",
    "python-dotenv": "dotenv",
    "tqdm": "tqdm",
    "joblib": "joblib",
}

# La estructura que se espera exista en el repositorio.
# Mediante esta comprobación se puede determinar si falta alguna carpeta necesaria para reproducir el pipeline.
REQUIRED_PATHS = [
    "data/raw",
    "data/processed",
    "notebooks",
    "reports/figures/generated",
    "reports/figures/final",
    "scripts",
    "src/data",
    "src/features",
    "src/models",
    "src/uncertainty",
    "src/evaluation",
    "src/explainability",
]

def check_packages() -> None:
    """Comprueba que las librerías principales del proyecto pueden importarse."""
    print("\nComprobación de las librerías")
    print("-" * 50)

    for distribution_name, import_name in PACKAGES.items():
        # Se importa el paquete para verificar que funcione.
        importlib.import_module(import_name)

        # Se lee la versión del paquete.
        version = metadata.version(distribution_name)

        print(f"{distribution_name:15s} {version}")

def check_project_structure(project_root: Path) -> None:
    """Comprueba que existen las carpetas esperadas del proyecto."""
    print("\nComprobación de la estructura del proyecto")
    print("-" * 50)

    missing_paths: list[str] = []

    for relative_path in REQUIRED_PATHS:
        path = project_root / relative_path

        if path.exists():
            print(f"OK {relative_path}")
        else:
            print(f"FALTA {relative_path}")
            missing_paths.append(relative_path)

    if missing_paths:
        missing = ", ".join(missing_paths)
        raise FileNotFoundError(f"Al proyecto le faltan las siguientes rutas: {missing}")

def main() -> None:
    """Ejecuta todas las comprobaciones del entorno del TFG."""
    # Como el script está dentro de scripts/, parents[1] apunta a la raíz del repositorio.
    project_root = Path(__file__).resolve().parents[1]

    print("Comprobación del entorno del TFG")
    print("=" * 50)
    print(f"Python: {sys.version.split()[0]}")
    print(f"Ejecutable: {sys.executable}")
    print(f"Plataforma: {platform.platform()}")
    print(f"Raíz proyecto: {project_root}")

    check_packages()
    check_project_structure(project_root)

    print("\nEl entorno está configurado correctamente.")

if __name__ == "__main__":
    main()