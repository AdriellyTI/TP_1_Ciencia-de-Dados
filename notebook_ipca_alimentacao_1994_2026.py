# %% [markdown]
# # Coleta contínua do IPCA — Alimentação e bebidas (1994 a 2026+)
#
# **Disciplina:** Ciência de Dados — UFAM
# **Fonte:** IBGE/SIDRA (API) — `https://apisidra.ibge.gov.br/values/`
# **Tema:** variação dos preços da cesta básica / inflação dos alimentos
#
# ## Objetivo
#
# A Tabela 61 do SIDRA (IPCA - Peso mensal) cobre apenas **janeiro/1991 a julho/1999**.
# Nenhuma tabela única do SIDRA contém o grupo "Alimentação e bebidas" de janeiro/1994
# até o presente. A solução é **concatenar as tabelas IPCA de mesmo padrão**
# (classificação Geral, grupo, subgrupo, item e subitem) que se sucedem no tempo:
#
# | Tabela | Período | Classificação | Código do grupo "Alimentação e bebidas" |
# |---|---|---|---|
# | 58 | jan/1991 – jul/1999 | c72 (índice/variação) | 1313 |
# | 655 | ago/1999 – jun/2006 | c315 | 7170 |
# | 2938 | jul/2006 – dez/2011 | c315 | 7170 |
# | 1419 | jan/2012 – dez/2019 | c315 | 7170 |
# | 7060 | jan/2020 – ago/2026+ | c315 | 7170 |
#
# > **Nota:** a Tabela 61 só oferece o *peso mensal*; já a 58 tem a *variação mensal* do
# > mesmo período. O notebook usa a **variação mensal do grupo Alimentação e bebidas**
# > em todas as eras, gerando uma série única e contínua de 1994 até o mês mais recente
# > disponível, sem descontinuidade (as variações de preço sobrevivem à troca de estruturas).

# %%
# ---------------------------------------------------------------------------
# 1. Bibliotecas e configurações
# ---------------------------------------------------------------------------
import json
import time
from pathlib import Path
from datetime import datetime, timezone

import requests
import pandas as pd

# Caminhos (relativos à localização deste arquivo)
BASE_DIR = Path(__file__).resolve().parent
BRUTOS_DIR = BASE_DIR / "projeto" / "dados_brutos"
TRATADOS_DIR = BASE_DIR / "projeto" / "dados_tratados"
BRUTOS_DIR.mkdir(parents=True, exist_ok=True)
TRATADOS_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "TrabalhoAcademico-CienciaDeDados/1.0 (contato@exemplo.com)"}
TIMEOUT = 30
PAUSA = 1.0  # segundos entre requisições (cuidado com o servidor)
API = "https://apisidra.ibge.gov.br/values"

# A partir deste mês (inclusive) a série é usada
INICIO = "199401"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)

print("Configuração concluída.")

# %% [markdown]
# ## 2. Registro das tabelas pesquisadas
#
# Cada era do IPCA é uma tabela com o mesmo padrão de classificação
# ("Geral, grupo, subgrupo, item e subitem"). O grupo **"1.Alimentação e
# bebidas"** tem código fixo por era: `1313` na c72 e `7170` na c315.

# %%
# ---------------------------------------------------------------------------
# 2. Tabelas-fonte (mesmo padrão), na ordem cronológica
# ---------------------------------------------------------------------------
TABELAS = [
    {
        "id": 58,
        "era": "jan/1991 a jul/1999",
        "classificacao": 72,
        "categoria": 1313,
        "nome": "IPCA - Variação mensal (índice geral, grupos, subgrupos, itens e subitens)",
    },
    {
        "id": 655,
        "era": "ago/1999 a jun/2006",
        "classificacao": 315,
        "categoria": 7170,
        "nome": "IPCA - Variação mensal (índice geral, grupos, subgrupos, itens e subitens)",
    },
    {
        "id": 2938,
        "era": "jul/2006 a dez/2011",
        "classificacao": 315,
        "categoria": 7170,
        "nome": "IPCA - Variação mensal, acumulada no ano e peso mensal",
    },
    {
        "id": 1419,
        "era": "jan/2012 a dez/2019",
        "classificacao": 315,
        "categoria": 7170,
        "nome": "IPCA - Variação mensal, acumuladas e peso mensal",
    },
    {
        "id": 7060,
        "era": "jan/2020 ao mês mais recente",
        "classificacao": 315,
        "categoria": 7170,
        "nome": "IPCA - Variação mensal, acumuladas e peso mensal",
    },
]

print(f"Tabelas registradas: {len(TABELAS)}")
for t in TABELAS:
    print(f"  t/{t['id']}  [{t['era']}]  c{t['classificacao']}/{t['categoria']}")

# %% [markdown]
# ## 3. Coleta via API
#
# Para cada tabela é feito um GET no padrão
# `/t/{id}/n1/all/v/all/p/all/c{classif}/{categoria}` e a resposta bruta é
# preservada em `dados_brutos/` **antes de qualquer transformação**. Apenas o
# grupo "Alimentação e bebidas" (cesta básica) é selecionado.

# %%
# ---------------------------------------------------------------------------
# 3. Coleta das séries
# ---------------------------------------------------------------------------

data_hora_coleta = datetime.now(timezone.utc)
proveniencia = []


def coletar_grupo(tab: dict) -> pd.DataFrame:
    """GET do grupo 'Alimentação e bebidas' de uma tabela SIDRA.

    Salva a resposta bruta em dados_brutos/ e retorna apenas as linhas da
    variável 'IPCA - Variação mensal'.
    """
    url = f"{API}/t/{tab['id']}/n1/all/v/all/p/all/c{tab['classificacao']}/{tab['categoria']}"

    registro = {
        "fonte_id": f"SIDRA-t{tab['id']}",
        "nome": tab["nome"],
        "url": url,
        "era": tab["era"],
        "data_hora_coleta": data_hora_coleta.isoformat(),
        "metodo": "API GET",
        "status_http": None,
        "arquivo_bruto": None,
        "quantidade_registros": None,
        "observacoes": "",
    }

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        registro["status_http"] = r.status_code

        if r.status_code != 200:
            registro["observacoes"] = f"HTTP {r.status_code} — dados não obtidos"
            print(f"  t/{tab['id']}: HTTP {r.status_code} (ERRO)")
            return registro

        dados = r.json()
        # preserva o bruto exatamente como veio da API
        stamp = data_hora_coleta.strftime("%Y%m%d_%H%M%S")
        arquivo = BRUTOS_DIR / f"sidra_t{tab['id']}_alimentacao_{stamp}.json"
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        registro["arquivo_bruto"] = str(arquivo)

        # linha 0 é o cabeçalho; as demais são dados
        df = pd.DataFrame(dados[1:])
        df = df.rename(
            columns={
                "D3C": "mes",
                "D3N": "mes_nome",
                "D2C": "variavel_cod",
                "D2N": "variavel",
                "D4N": "grupo",
                "V": "valor",
            }
        )
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df["tabela"] = tab["id"]
        df = df[df["variavel"] == "IPCA - Variação mensal"].copy()
        df["mes"] = df["mes"].astype(str)

        registro["quantidade_registros"] = len(df)
        registro["observacoes"] = f"Só a variação mensal do grupo Alimentação e bebidas (c{tab['classificacao']}/{tab['categoria']})"
        print(f"  t/{tab['id']}: HTTP {r.status_code}, {len(df)} registros brutos salvos")
        return registro, df

    except Exception as e:  # noqa: BLE001 - erro de conexão é registrado, não interrompe
        registro["status_http"] = "erro_conexao"
        registro["observacoes"] = str(e)
        print(f"  t/{tab['id']}: erro de conexão — {e}")
        return registro


# %%
# ---------------------------------------------------------------------------
# 3.1 Executa a coleta de todas as tabelas
# ---------------------------------------------------------------------------
frames = []
for tab in TABELAS:
    resultado = coletar_grupo(tab)
    if isinstance(resultado, tuple):
        grupo_reg, df = resultado
        frames.append(df)
    else:
        grupo_reg = resultado
    proveniencia.append(grupo_reg)
    time.sleep(PAUSA)

print(f"\nFrames coletados: {len(frames)}")

# %%
# ---------------------------------------------------------------------------
# 3.2 Registro de proveniência consolidado
# ---------------------------------------------------------------------------
prov_df = pd.DataFrame(proveniencia)
prov_file = BRUTOS_DIR / f"proveniencia_sidra_ipca_{data_hora_coleta.strftime('%Y%m%d_%H%M%S')}.csv"
prov_df.to_csv(prov_file, index=False, encoding="utf-8")
print("Proveniência salva em:", prov_file)
prov_df[["fonte_id", "era", "status_http", "quantidade_registros"]]

# %% [markdown]
# ## 4. Integração da série contínua (1994 → mês mais recente)

# %%
# ---------------------------------------------------------------------------
# 4. Integração das séries em uma única base temporal
# ---------------------------------------------------------------------------
ipca = pd.concat(frames, ignore_index=True)
ipca["data"] = pd.to_datetime(ipca["mes"], format="%Y%m")
ipca = ipca.sort_values("data").reset_index(drop=True)

# série contínua a partir de janeiro/1994
ipca = ipca[ipca["mes"] >= INICIO].copy()
ipca = ipca.drop_duplicates(subset=["mes", "variavel", "grupo"]).reset_index(drop=True)

# verificação de continuidade (meses ausentes)
meses_esperados = pd.period_range(INICIO, ipca["data"].max().strftime("%Y-%m"), freq="M")
meses_obtidos = pd.DatetimeIndex(ipca["data"]).to_period("M")
faltantes = meses_esperados.difference(meses_obtidos)

print(f"Meses da série: {len(ipca)}")
print(f"Primeiro mês: {ipca['data'].min().strftime('%Y-%m')} | Último: {ipca['data'].max().strftime('%Y-%m')}")
print(f"Meses ausentes: {len(faltantes)}")
if len(faltantes):
    print("  Falta:", list(faltantes)[:20])

# %%
# ---------------------------------------------------------------------------
# 4.1 Exemplo das pontas da série
# ---------------------------------------------------------------------------
ipca[["data", "mes", "grupo", "variavel", "valor"]].head()
ipca[["data", "mes", "grupo", "variavel", "valor"]].tail()

# %%
# ---------------------------------------------------------------------------
# 5. Validações de qualidade
# ---------------------------------------------------------------------------
assert ipca["valor"].notna().all(), "Existem valores nulos na variável"
assert ipca["data"].is_monotonic_increasing, "Série fora de ordem cronológica"
assert ipca["data"].duplicated().sum() == 0, "Existem meses duplicados"
print(f"Valor mínimo: {ipca['valor'].min():.2f}% | máximo: {ipca['valor'].max():.2f}%")
print(f"Média: {ipca['valor'].mean():.2f}% | desvio: {ipca['valor'].std():.2f}%")
print("Validações OK.")

# %% [markdown]
# ## 6. Exportação da base tratada

# %%
# ---------------------------------------------------------------------------
# 6. Exportação (separada do bruto)
# ---------------------------------------------------------------------------
colunas = ["data", "mes", "grupo", "variavel", "valor", "tabela"]
base = ipca[colunas].copy()
base["data"] = base["data"].dt.strftime("%Y-%m-%d")

arquivo_csv = TRATADOS_DIR / "ipca_alimentacao_1994_2026.csv"
base.to_csv(arquivo_csv, index=False, encoding="utf-8")

arquivo_parquet = TRATADOS_DIR / "ipca_alimentacao_1994_2026.parquet"
try:
    base.to_parquet(arquivo_parquet, index=False)
    print("Base exportada em CSV e Parquet.")
except Exception as e:  # pyarrow pode não estar instalado
    print("CSV exportado; Parquet não gerado:", e)

print("CSV ->", arquivo_csv)
print(f"Dimensões da base tratada: {base.shape[0]} linhas x {base.shape[1]} colunas")
print("Unidade de observação: grupo 'Alimentação e bebidas' em um mês.")

# %% [markdown]
# ## 7. Observações finais
#
# - **Continuidade:** como a série usa **variações mensais** (e não pesos), a troca
#   de estrutura de ponderação entre eras não cria descontinuidade na base.
# - **Cobertura:** janeiro/1994 até o mês mais recente liberado pelo IBGE
#   (agosto/2026 na data da coleta).
# - **Brutos preservados:** um JSON por tabela em `projeto/dados_brutos/`, antes de
#   qualquer limpeza; proveniência consolidada em CSV.
# - **Limitação:** o grupo é agregado nacional (`n1/all`). Se o grupo for expandir para
#   capitais/regiões metropolitanas, usar `n2`/`n3` (ex.: `n3/all` retorna as RMs).