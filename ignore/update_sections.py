import json
from pathlib import Path

NOTEBOOK = Path("notebook_coleta.ipynb")

with open(NOTEBOOK, "r", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# --- Update Cell 22: add 8.3 Padronização DIEESE ---
c22 = cells[22]
src22 = "".join(c22["source"]) if isinstance(c22["source"], list) else c22["source"]

old_83 = "# --- 8.3 Padronização ---\n# Preencher posteriormente."
new_83 = """# --- 8.3 Padronização ---
#
# Padronização dos dados DIEESE (após extração em coletaDados.ipynb):
#   - Colunas: capital, valor, var_mensal, pct_sal, tempo, var_ano, var_12, aammes
#   - Formato tempo: normalizado para XhYm (ex: '111h 57min' -> '111h57m')
#   - Tipos: todas as colunas numéricas como float
#   - Valores ausentes: None (ex: variação anual quando não disponível)
#   - Consistente com a base extraída automaticamente (mesma estrutura de colunas)"""

if old_83 in src22:
    src22 = src22.replace(old_83, new_83)
    cells[22]["source"] = [src22] if isinstance(c22["source"], list) else src22
    print("Cell 22: Added 8.3 Padronização DIEESE")

# --- Update Cell 28: Section 11 Proveniência ---
c28 = cells[28]
src28 = "".join(c28["source"]) if isinstance(c28["source"], list) else c28["source"]

old_11 = "## 11. Proveniência e observações\n\n*Preencher posteriormente.*"
new_11 = """## 11. Proveniência e observações

### 11.1 Registros de proveniência

Cada fonte mantém seu próprio log de proveniência:

| Fonte | Arquivo de proveniência | Descrição |
|---|---|---|
| Fonte 1 — IBGE/SIDRA | `projeto/dados_brutos/proveniencia/sidra_t{N}_alimentacao_{stamp}.json` + `proveniencia_sidra_{stamp}.csv` | URL, status HTTP, data/hora, tamanho |
| Fonte 2 — DIEESE | `projeto/dados_brutos/dieese/provenance_log.csv` | boletim, URL, status HTTP, formato, data/hora |
| Fonte 3 — TSE | `projeto/dados_brutos/proveniencia/proveniencia_tse.csv` | dataset, recurso, URL, status HTTP, tamanho |

### 11.2 Observações

- **DIEESE**: Coleta respeita Crawl-delay de 10s (robots.txt). Arquivos já existentes não são re-baixados. Boletim 201001 corrigido (URL mapeada incorretamente). Julho/2005 transcrito manualmente.
- **TSE**: CKAN API protegida por Akamai (intermitente HTTP 403, contornado via cookies). Arquivos ZIP reportados como CSV pela API. CDN downloads diretos confirmados.
- **IBGE/SIDRA**: API pública, sem proteção anti-bot. Múltiplas tabelas concatenadas para cobertura contínua (1994-2026+).
"""

if old_11 in src28:
    src28 = src28.replace(old_11, new_11)
    cells[28]["source"] = [src28] if isinstance(c28["source"], list) else src28
    print("Cell 28: Added Section 11 content")

with open(NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done!")
