# Instalar skills globalmente (todos os projetos)

## Opção A — Cursor Desktop (recomendado)

1. Copie a pasta `skills/` para `~/.cursor/skills/` no seu Mac/PC:

```bash
# na raiz deste repo
cp -R .cursor/skills/. ~/.cursor/skills/
# ou a partir deste bundle:
cp -R cursor-user-skills-bundle/skills/. ~/.cursor/skills/
```

2. Em **Cursor Settings → Agents → Context and Tools**, ligue **Sync Skills for Cloud Agents**.
3. (Opcional) Copie `mcp.json` para `~/.cursor/mcp.json` e autentique em Customize → MCP.
4. (Opcional) Em **Cursor Settings → Rules**, cole a regra PT-BR de `pt-br.mdc` como User Rule always-on.

## Opção B — Importar do GitHub

1. Abra **Customize → Skills** (ou Plugins).
2. Escolha instalar **From GitHub Repository**.
3. Use: `https://github.com/victor-fagundes/freecodecamp`
4. Confirme as skills e instale.

Skills de projeto (neste repo) já funcionam sem isso. User skills + Sync cobrem qualquer Cloud Agent seu.
