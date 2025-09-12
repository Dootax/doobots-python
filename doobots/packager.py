#!/usr/bin/env python3
import sys
from pathlib import Path
import toml
import zipfile

def main():
    try:
        app_path = Path("app")
        if not app_path.exists() or not (app_path / "main.py").exists():
            raise FileNotFoundError("Pasta 'app' ou 'app/main.py' não encontrada.")

        zip_name = "app.zip"
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            pyproject = toml.load(pyproject_path)
            name = pyproject.get("project", {}).get("name", "app")
            version = pyproject.get("project", {}).get("version", "0.0.1")
            zip_name = f"{name}-{version}.zip"

        with zipfile.ZipFile(zip_name, "w") as zf:
            for file in app_path.rglob("*"):
                zf.write(file, file.relative_to(app_path))

            requirements_path = Path("requirements.txt")
            if requirements_path.exists():
                zf.write(requirements_path, Path("requirements.txt"))

        print(f"Pacote criado com sucesso: {zip_name}")
        return 0
    except Exception as e:
        print(f"Erro ao criar pacote: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
