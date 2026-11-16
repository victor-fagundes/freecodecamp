#!/usr/bin/env bash
# Instala as knowledge-work skills no nível do usuário (~/.cursor/skills)
# para todos os projetos no Cursor Desktop. Depois ligue:
# Settings → Agents → Sync Skills for Cloud Agents
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/.cursor/skills"
DEST="${HOME}/.cursor/skills"
MCP_SRC="$ROOT/.cursor/mcp.json"
MCP_DEST="${HOME}/.cursor/mcp.json"

if [[ ! -d "$SRC" ]]; then
  echo "Não achei $SRC — rode este script na raiz do repo com .cursor/skills." >&2
  exit 1
fi

mkdir -p "$DEST"
# Copia sem apagar skills pessoais que não existem neste pacote
cp -R "$SRC"/. "$DEST"/
echo "Skills instaladas em $DEST ($(ls "$DEST" | wc -l | tr -d ' ') pastas)"

if [[ -f "$MCP_SRC" ]]; then
  if [[ -f "$MCP_DEST" ]]; then
    echo "Já existe $MCP_DEST — não sobrescrevi. Compare com $MCP_SRC se quiser."
  else
    cp "$MCP_SRC" "$MCP_DEST"
    echo "MCP copiado para $MCP_DEST"
  fi
fi

echo
echo "Próximo passo no Cursor Desktop:"
echo "  Settings → Agents → Context and Tools → ligue Sync Skills for Cloud Agents"
echo "Opcional: User Rule PT-BR em Settings → Rules (veja .cursor/rules/pt-br.mdc)"
