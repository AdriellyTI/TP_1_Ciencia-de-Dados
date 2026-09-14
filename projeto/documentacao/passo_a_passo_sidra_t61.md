# Passo a passo — Coleta do IPCA de alimentação (cesta básica) pela API do SIDRA

**Fonte:** IBGE/SIDRA — Tabela 61
**Tabela:** IPCA - Peso mensal, para o índice geral, grupos, subgrupos, itens e subitens de produtos e serviços (janeiro/1991 a julho/1999)
**Dado de interesse:** peso mensal (%) de cada grupo/subgrupo/item/subitem na composição do IPCA — aqui, restrito ao grupo de alimentação ("cesta básica").
**Data da coleta:** 14/09/2026
**Arquivo bruto gerado:** `dados_brutos/sidra_t61_ipca_alimentacao_bruto.json`

---

## 1. Problema da URL original

```text
https://apisidra.ibge.gov.br/values/t/61/n1/all/v/all/p/all/c315/all=
```

Essa URL retorna **HTTP 400 (Bad Request)** por dois motivos:

1. **`=` e espaço no final** — quebram a URL.
2. **`c315` não existe na Tabela 61.** Essa classificação é de outras tabelas
   (ex.: Tabela 7060, IPCA atual). Na Tabela 61, a única classificação é a
   **`c72`** — *Geral, grupos, subgrupos, itens e subitens*.

---

## 2. URL corrigida (só alimentação / "cesta básica")

```text
https://apisidra.ibge.gov.br/values/t/61/n1/all/v/all/p/all/c72/1313
```

| Parâmetro | Valor | Significado |
|---|---|---|
| `t/61` | 61 | Tabela do SIDRA |
| `n1/all` | all | Todas as unidades do nível Brasil |
| `v/all` | all | Todas as variáveis (na prática, só existe a **V66** — IPCA - Peso mensal) |
| `p/all` | all | Todos os períodos disponíveis (jan/1991 a jul/1999, 102 meses) |
| `c72/1313` | 1313 | Apenas a categoria **"1.Alimentação e bebidas"** |

> **Atenção:** ao passar `c72/1313`, o SIDRA retorna **só o grupo fechado**
> "Alimentação e bebidas" (uma linha por mês). Para os **itens individuais**
> (arroz, feijão, carne, leite, pão...), é preciso listar os códigos de cada
> subitem — ver seção 5.

---

## 3. GET na API

### 3.1 Com `requests` (Python — como no notebook)

```python
import requests

url = "https://apisidra.ibge.gov.br/values/t/61/n1/all/v/all/p/all/c72/1313"

resposta = requests.get(url)
print(resposta.status_code)              # 200

if resposta.status_code == 200:
    json_bruto = resposta.json()         # lista: [0]=cabeçalho, [1:]=dados
    print(len(json_bruto) - 1, "registros")
else:
    print("Erro na requisição:", resposta.status_code)
```

### 3.2 Com PowerShell

```powershell
$url = "https://apisidra.ibge.gov.br/values/t/61/n1/all/v/all/p/all/c72/1313"
$r = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing
$r.StatusCode   # 200
$r.Content
```

---

## 4. Salvamento do bruto (antes de qualquer limpeza)

```python
import json
from datetime import datetime, timezone
from pathlib import Path

BRUTOS_DIR = Path("projeto/dados_brutos")
BRUTOS_DIR.mkdir(parents=True, exist_ok=True)

# Registra o momento da coleta
data_hora = datetime.now(timezone.utc).isoformat()

arquivo = BRUTOS_DIR / "sidra_t61_ipca_alimentacao_bruto.json"
with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(json_bruto, f, ensure_ascii=False, indent=2)

print("Salvo em:", arquivo)
print("Coletado em (UTC):", data_hora)
```

---

## 5. (Opcional) Pegar os itens individuais da cesta básica

Na classificação `c72`, a hierarquia de "Alimentação e bebidas" é:

| Nível | Categoria |
|---|---|
| Grupo | 1313 — 1.Alimentação e bebidas |
| Subgrupo | 1101 — Cereais, leguminosas e oleaginosas; 1107 — Carnes frescas e vísceras; 1111 — Leite e derivados; etc. |
| Item / subitem | 1457 — Arroz; 1463 — Feijão; 1509 — Batata-inglesa; 1789 — Frango; 1795 — Leite pasteurizado; 1827 — Pão francês; 1853 — Café moído; etc. |

Principais subitens de "cesta básica" (códigos `c72`):

| Código | Item |
|---|---|
| 1457 | Arroz |
| 1463 / 1465 / 1471 | Feijão (mulatinho / preto / jalo) |
| 1509 | Batata-inglesa |
| 1545 / 1547 | Açúcar (refinado / cristal) |
| 1635 | Carne de porco |
| 1649 / 1651 | Carne bovina (chã de dentro / alcatra) |
| 1789 | Frango |
| 1791 | Ovo de galinha |
| 1795 | Leite pasteurizado |
| 1827 | Pão francês |
| 1843 | Óleo de soja |
| 1853 | Café moído |

Exemplo de URL com múltiplos subitens:

```text
https://apisidra.ibge.gov.br/values/t/61/n1/all/v/all/p/all/c72/1457,1463,1509,1545,1635,1789,1791,1795,1827,1843,1853
```

---

## 6. Provisão e reprodutibilidade

| Campo | Valor |
|---|---|
| `fonte_id` | IBGE-SIDRA-61 |
| `nome` | IPCA - Peso mensal (grupo Alimentação e bebidas) |
| `url` | `https://apisidra.ibge.gov.br/values/t/61/n1/all/v/all/p/all/c72/1313` |
| `metodo` | API (GET) |
| `status_http` | 200 |
| `quantidade_registros` | 102 (meses jan/1991–jul/1999) |
| `arquivo_bruto` | `projeto/dados_brutos/sidra_t61_ipca_alimentacao_bruto.json` |
| `variavel` | V66 — IPCA - Peso mensal (%) |
| `classificacao` | c72, categoria 1313 |