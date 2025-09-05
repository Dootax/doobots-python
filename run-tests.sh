#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

echo ">> Instalando dependências..."
pip install -r requirements.txt

echo ">> Instalando pacote em modo editável..."
pip install -e .

echo ">> Rodando testes..."
pytest -v
