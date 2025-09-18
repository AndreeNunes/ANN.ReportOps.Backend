#!/bin/bash

# Ativar o ambiente virtual
source .venv/bin/activate

# Carregar variáveis de ambiente do arquivo .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Executar a aplicação
python3 app.py
