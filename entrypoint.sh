#!/bin/sh
set -e

DB_DIR="/app/data"
DB_PATH="$DB_DIR/db.sqlite3"
SEED_PATH="/app/db.sqlite3.seed"

# Garante que a pasta do volume existe
mkdir -p "$DB_DIR"

# Se o volume ainda não tem banco (primeiro deploy), semeia com o banco atual do repositório
if [ ! -f "$DB_PATH" ]; then
    if [ -f "$SEED_PATH" ]; then
        echo "Nenhum banco encontrado no volume. Semeando com db.sqlite3.seed..."
        cp "$SEED_PATH" "$DB_PATH"
    else
        echo "Nenhum banco encontrado no volume e nenhum seed disponível. O Django vai criar um banco novo."
    fi
else
    echo "Banco já existe no volume, mantendo dados atuais."
fi

exec "$@"
