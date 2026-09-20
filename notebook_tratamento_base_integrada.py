# %% [markdown]
# # Tratamento e integração da base de dados — Cesta Básica (DIEESE) × IPCA (IBGE/SIDRA)
#
# **Disciplina:** Ciência de Dados — UFAM
# **Fontes:** DIEESE (Pesquisa Nacional da Cesta Básica de Alimentos) e IBGE (IPCA/SIDRA).
#
# ## O que este notebook faz
#
# 1. **Limpeza/estruturação do DIEESE** (`dados_Coletados.csv`):
#    - normaliza o nome das capitais para 27 canônicos (acréscimo de `sigla_uf`);
#    - cria datas de referência (`data_referencia`, `ano`, `mes_num`) a partir de `aammes`;
#    - converte `tempo` ("XhYYm") em horas decimais (`tempo_em_horas`);
#    - remove **duplicatas exatas** com registro no log de tratamento;
#    - **não altera nenhum valor** — adiciona apenas *flags* de diagnóstico
#      (`flag_capital_variante`, `flag_diverge_var_mensal`, `n_capitais_no_mes`,
#      `flag_conflito_capital_mes`).
# 2. **Acomoda o IPCA tratado** (produzido por `notebook_ipca_alimentacao_1994_2026.py`)
#    em `projeto/dados_tratados/`.
# 3. **Integra as três fontes**: DIEESE × IPCA por `mes` e TSE por ano eleitoral/UF.
#
# > Todas as saídas vão para `projeto/dados_tratados/` (separados do bruto),
# > em CSV **e** Parquet.

# %%
# ---------------------------------------------------------------------------
# 1. Bibliotecas e caminhos
# ---------------------------------------------------------------------------
import re
import unicodedata
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BRUTOS_DIR = BASE_DIR / "projeto" / "dados_brutos"
TRATADOS_DIR = BASE_DIR / "projeto" / "dados_tratados"
FONTES_DIEESE = [
    BASE_DIR / "Dados do DIEESE" / "dados_Coletados.csv",
    TRATADOS_DIR / "dieese_dados_tratados.csv",
]
DIEESE_BRUTO = next((caminho for caminho in FONTES_DIEESE if caminho.exists()), FONTES_DIEESE[0])
TSE_DERIVADA = TRATADOS_DIR / "tse_derivada_presidentes_governadores.csv"
TRATADOS_DIR.mkdir(parents=True, exist_ok=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

print("Caminhos:")
print("  DIEESE:", DIEESE_BRUTO)
print("  saída :", TRATADOS_DIR)

# %% [markdown]
# ## 2. Capital canônica × sigla da UF
#
# As 61 variações de grafia colhidas (MAIÚSCULAS, "Vitória*", sufixo "‐" U+2010,
# "Rio de janeiro", etc.) reduzem-se a exatamente **27 capitais** distintas. Aqui
# fixamos o nome canônico e a sigla da UF de cada uma.

# %%
# ---------------------------------------------------------------------------
# 2. Mapa canônico: chave normalizada -> (nome canônico, sigla da UF)
# ---------------------------------------------------------------------------
CAP_TO_UF = {
    "SAOPAULO": ("São Paulo", "SP"),
    "RIODEJANEIRO": ("Rio de Janeiro", "RJ"),
    "BELOHORIZONTE": ("Belo Horizonte", "MG"),
    "PORTOALEGRE": ("Porto Alegre", "RS"),
    "CURITIBA": ("Curitiba", "PR"),
    "FLORIANOPOLIS": ("Florianópolis", "SC"),
    "BRASILIA": ("Brasília", "DF"),
    "GOIANIA": ("Goiânia", "GO"),
    "SALVADOR": ("Salvador", "BA"),
    "RECIFE": ("Recife", "PE"),
    "FORTALEZA": ("Fortaleza", "CE"),
    "BELEM": ("Belém", "PA"),
    "NATAL": ("Natal", "RN"),
    "JOAOPESSOA": ("João Pessoa", "PB"),
    "ARACAJU": ("Aracaju", "SE"),
    "VITORIA": ("Vitória", "ES"),
    "CAMPOGRANDE": ("Campo Grande", "MS"),
    "MANAUS": ("Manaus", "AM"),
    "CUIABA": ("Cuiabá", "MT"),
    "PALMAS": ("Palmas", "TO"),
    "MACEIO": ("Maceió", "AL"),
    "SAOLUIS": ("São Luís", "MA"),
    "TERESINA": ("Teresina", "PI"),
    "MACAPA": ("Macapá", "AP"),
    "RIOBRANCO": ("Rio Branco", "AC"),
    "PORTOVELHO": ("Porto Velho", "RO"),
    "BOAVISTA": ("Boa Vista", "RR"),
}


def chave_capital(nome) -> str:
    """Normaliza o nome bruto em uma chave estável (sem acentos/símbolos)."""
    s = unicodedata.normalize("NFKD", str(nome))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Za-z0-9]", "", s.upper())


print(f"Mapa criado para {len(CAP_TO_UF)} capitais.")

# %% [markdown]
# ## 3. Carga e limpeza estrutural do DIEESE
#
# Nenhum valor numérico é modificado: apenas *tipos*, *datas*, *nomes* e *flags*.

# %%
# ---------------------------------------------------------------------------
# 3. Carga do bruto do DIEESE
# ---------------------------------------------------------------------------
dieese = pd.read_csv(DIEESE_BRUTO, encoding="utf-8-sig")
print("Linhas lidas:", len(dieese))
dieese.columns = dieese.columns.str.strip()

# 3.1 Meses -> inteiro AAAAAM + data de referência (início do mês)
dieese["mes"] = dieese["aammes"].astype(str).str.zfill(6).astype(int)
dieese["data_referencia"] = pd.to_datetime(dieese["mes"].astype(str), format="%Y%m")
dieese["ano"] = dieese["data_referencia"].dt.year
dieese["mes_num"] = dieese["data_referencia"].dt.month

# 3.2 Capital canônica e UF
dieese["capital_bruto"] = dieese["capital"].astype(str).str.strip()
chaves = dieese["capital_bruto"].map(chave_capital)
desconhecidas = set(chaves) - set(CAP_TO_UF)
assert not desconhecidas, f"Chaves de capital não mapeadas: {desconhecidas}"
dieese["capital"] = chaves.map(lambda k: CAP_TO_UF[k][0])
dieese["sigla_uf"] = chaves.map(lambda k: CAP_TO_UF[k][1])
dieese["flag_capital_variante"] = dieese["capital_bruto"] != dieese["capital"]

# 3.3 Tempo de trabalho -> horas decimais (mantém o texto original)
TEMPO_RE = re.compile(r"^(\d+)h(\d{1,2})m$")


def parse_tempo(s) -> float | None:
    if pd.isna(s):
        return None
    m = TEMPO_RE.match(str(s).strip())
    if not m:
        return None
    return int(m.group(1)) + int(m.group(2)) / 60


dieese["tempo_em_horas"] = dieese["tempo"].map(parse_tempo)
n_tempo_nao_parseado = dieese["tempo_em_horas"].isna().sum()
print("Tempos não convertidos:", n_tempo_nao_parseado)

# 3.4 Numéricos
for col in ["valor", "var_mensal", "pct_sal", "var_ano", "var_12"]:
    dieese[col] = pd.to_numeric(dieese[col], errors="coerce")

# 3.5 Duplicatas exatas (todas as colunas idênticas) -> remove, mantendo 1 cópia
cols_conteudo = [
    c for c in dieese.columns
    if c not in {"capital_bruto"} and "flag" not in c
]
flag_dup = dieese.duplicated(subset=cols_conteudo, keep=False)
n_dup = int(flag_dup.sum())
if n_dup:
    remocao = dieese[flag_dup].copy()
    remocao["flag_duplicata_removida"] = True
    remocao["motivo_remocao"] = (
        "linha exatamente duplicada de outra do mesmo (capital, mes)"
    )
    remocao = remocao.drop_duplicates(subset=cols_conteudo, keep="first")
    dieese = dieese.drop_duplicates(subset=cols_conteudo, keep="first").copy()
    print(f"Duplicatas exatas: {remocao.shape[0]} linha(s) removida(s) e registrada(s).")
else:
    remocao = pd.DataFrame(
        columns=[*dieese.columns, "flag_duplicata_removida", "motivo_remocao"]
    )
    print("Duplicatas exatas: nenhuma.")

# 3.6 Conflitos restantes de (capital canônico, mes) com valores distintos
conflitos = dieese.groupby(["capital", "mes"], as_index=False).size()
conflitos = conflitos[conflitos["size"] > 1]
dieese["flag_conflito_capital_mes"] = dieese.duplicated(
    subset=["capital", "mes"], keep=False
)
print("Conflitos restantes de (capital, mes):", int(conflitos["size"].sum()))

# 3.7 Diagnóstico de consistência (não altera valores originais)
dieese = dieese.sort_values(["capital", "mes"]).reset_index(drop=True)
dieese["valor_mes_anterior"] = dieese.groupby("capital")["valor"].shift(1)
dieese["var_mensal_impl"] = (
    100 * (dieese["valor"] / dieese["valor_mes_anterior"] - 1)
).round(2)
alvo = dieese["var_mensal"].astype(float)
impl = dieese["var_mensal_impl"]
diff = (alvo - impl).abs()
dieese["flag_diverge_var_mensal"] = alvo.notna() & impl.notna() & (diff >= 5)

# 3.8 Cobertura mensal (nº de capitais publicadas no mês)
cap_por_mes = dieese.groupby("mes")["capital"].nunique().rename("n_capitais_no_mes")
dieese = dieese.merge(cap_por_mes, left_on="mes", right_index=True, how="left")

# 3.9 Períodos de cobertura/metodologia (documentação, não altera valores)
def periodo_label(row):
    a = row["mes"]
    if a <= 201512:
        return "2005-01 a 2015-12 | 16/18 capitais, ponderação anterior"
    if a <= 202504:
        return "2016-01 a 2025-04 | 27 capitais, ponderação atualizada"
    if a <= 202506:
        return "2025-05 a 2025-06 | 17 capitais publicadas"
    return "2025-07 em diante | 27 capitais, cesta atualizada"


dieese["periodo_cobertura"] = dieese.apply(periodo_label, axis=1)

print("\nVisão geral da base DIEESE tratada:")
print(dieese[["mes", "data_referencia", "capital", "sigla_uf", "capital_bruto", "valor",
              "var_mensal", "pct_sal", "tempo", "tempo_em_horas", "var_ano", "var_12",
              "n_capitais_no_mes"]].head().to_string(index=False))

# %% [markdown]
# ## 4. Controles de qualidade (resumo)

# %%
# ---------------------------------------------------------------------------
# 4. Qualidade
# ---------------------------------------------------------------------------
print("Dimensões:", dieese.shape)
print("\nValores ausentes por coluna:")
print(dieese[["valor", "var_mensal", "pct_sal", "tempo", "var_ano", "var_12"]].isna().sum().to_string())
print("\nMeses cobrindo cada período:")
print(dieese.groupby("periodo_cobertura")["mes"].agg(["count", "min", "max"]).to_string())
print("\nCapitais com menos publicações (possíveis lacunas reais da fonte):")
min_anos = dieese.groupby("capital")["ano"].agg(["min", "max", "count"])
print(min_anos.sort_values("count").head(10).to_string())

# 4.1 Registro de limpeza (duplicatas removidas) — guardado em dados_tratados
registro = remocao.copy()
if len(registro):
    registro = registro.drop_duplicates(subset=cols_conteudo, keep="last")
log_cols = ["mes", "data_referencia", "capital", "capital_bruto", "sigla_uf",
            "valor", "motivo_remocao"]
registro_out = registro[log_cols] if len(registro) else pd.DataFrame(columns=log_cols)
registro_out.to_csv(TRATADOS_DIR / "log_duplicatas_removidas.csv",
                    index=False, encoding="utf-8")
print("\nLog de duplicatas removidas salvo em dados_tratados/.")

# %% [markdown]
# ## 5. Exportação da base DIEESE tratada

# %%
# ---------------------------------------------------------------------------
# 5. Exporta cesta_basica_dieese_tratada (CSV + Parquet)
# ---------------------------------------------------------------------------
colunas_dieese = [
    "mes", "data_referencia", "ano", "mes_num",
    "capital", "sigla_uf", "capital_bruto",
    "valor", "var_mensal", "pct_sal", "tempo", "tempo_em_horas",
    "var_ano", "var_12",
    "flag_capital_variante", "flag_conflito_capital_mes",
    "flag_diverge_var_mensal", "n_capitais_no_mes", "periodo_cobertura",
]
base_dieese = dieese[colunas_dieese].copy()
base_dieese["tipo_cesta"] = "Cesta Básica de Alimentos - DIEESE"

arquivo_dieese_csv = TRATADOS_DIR / "cesta_basica_dieese_tratada.csv"
arquivo_dieese_parquet = TRATADOS_DIR / "cesta_basica_dieese_tratada.parquet"
base_dieese.to_csv(arquivo_dieese_csv, index=False, encoding="utf-8")
base_dieese.to_parquet(arquivo_dieese_parquet, index=False)
print("DIEESE tratado ->", arquivo_dieese_csv)
print("Linhas:", base_dieese.shape[0], "colunas:", base_dieese.shape[1])

# %% [markdown]
# ## 6. IPCA tratado (acomodação + exportação em `dados_tratados/`)
#
# A série do IPCA é gerada por `notebook_ipca_alimentacao_1994_2026.py` a partir
# dos JSONs brutos do SIDRA. Aqui apenas garantimos que a versão tratada esteja no
# lugar correto (`dados_tratados/`) e a usamos como insumo da integração.

# %%
# ---------------------------------------------------------------------------
# 6. Acomoda IPCA tratado
# ---------------------------------------------------------------------------
ipca_destino_csv = TRATADOS_DIR / "ipca_alimentacao_tratada.csv"
ipca_destino_parquet = TRATADOS_DIR / "ipca_alimentacao_tratada.parquet"

# fontes possíveis: dados_tratados (já pronto) ou dados_brutos (versão anterior)
candidatos = [
    TRATADOS_DIR / "ipca_alimentacao_1994_2026.csv",
    BRUTOS_DIR / "ipca_alimentacao_1994_2026.csv",
]
origem_ipca = next((p for p in candidatos if p.exists()), None)
assert origem_ipca is not None, "CSV tratado do IPCA não encontrado."

if ipca_destino_csv.exists() and origem_ipca != ipca_destino_csv:
    ipca = pd.read_csv(ipca_destino_csv)
    print("IPCA lido de dados_tratados/ (já existia).")
else:
    ipca = pd.read_csv(origem_ipca, encoding="utf-8-sig")
    if origem_ipca != ipca_destino_csv:
        ipca.to_csv(ipca_destino_csv, index=False, encoding="utf-8")
        print("IPCA copiado de", origem_ipca.name, "para dados_tratados/.")

ipca["mes"] = ipca["mes"].astype(int)
ipca["data"] = pd.to_datetime(ipca["data"])
print("IPCA tratado:", ipca.shape, "| meses",
      ipca["mes"].min(), "a", ipca["mes"].max())

# continuação: garante parquet
if not ipca_destino_parquet.exists():
    ipca.to_parquet(ipca_destino_parquet, index=False)
print("IPCA ->", ipca_destino_csv)

# %% [markdown]
# ## 7. Integração: DIEESE × IPCA (chave `mes`)
#
# O IPCA é uma série **nacional** (grupo "1.Alimentação e bebidas"); portanto cada
# linha capital-mês do DIEESE se liga à variação mensal do IPCA do mesmo mês.
# Usamos LEFT JOIN a partir do DIEESE (base principal cesta-básica por capital).

# %%
# ---------------------------------------------------------------------------
# 7. Integração
# ---------------------------------------------------------------------------
ipca_join = ipca[["mes", "grupo", "variavel", "valor", "tabela"]].rename(
    columns={
        "grupo": "ipca_grupo",
        "variavel": "ipca_variavel",
        "valor": "ipca_var_mensal_pct",
        "tabela": "ipca_tabela_sidra",
    }
)

base_integrada = base_dieese.merge(ipca_join, on="mes", how="left",
                                   validate="many_to_one")
n_sem_ipca = int(base_integrada["ipca_var_mensal_pct"].isna().sum())
print("Linhas da integrada:", base_integrada.shape)
print("Linhas sem correspondência de IPCA (meses além da série IPCA):", n_sem_ipca)

arquivo_integrada_csv = TRATADOS_DIR / "base_integrada.csv"
arquivo_integrada_parquet = TRATADOS_DIR / "base_integrada.parquet"
base_integrada.to_csv(arquivo_integrada_csv, index=False, encoding="utf-8")
base_integrada.to_parquet(arquivo_integrada_parquet, index=False)
print("Integrada ->", arquivo_integrada_csv)

# %% [markdown]
# ## 8. Integração do TSE por período de governo
#
# A tabela econômica é mensal, enquanto o TSE é eleitoral. Para manter uma
# linha por capital/mês, cada observação recebe o ano eleitoral mais recente
# até o ano da observação. Governadores são associados por UF e presidentes por
# ano eleitoral. Registros duplicados ou múltiplos do TSE são concatenados,
# preservando a informação sem multiplicar linhas da base econômica.

# %%
# ---------------------------------------------------------------------------
# 8. Integração TSE: governo de referência por ano e UF
# ---------------------------------------------------------------------------
assert TSE_DERIVADA.exists(), f"Tabela derivada do TSE não encontrada: {TSE_DERIVADA}"
tse = pd.read_csv(TSE_DERIVADA, encoding="utf-8-sig")
tse["ANO_ELEICAO"] = pd.to_numeric(tse["ANO_ELEICAO"], errors="coerce").astype("Int64")
tse["CD_CARGO"] = pd.to_numeric(tse["CD_CARGO"], errors="coerce").astype("Int64")
tse = tse[tse["CD_SIT_TOT_TURNO"].astype(str).eq("1")].copy()

anos_eleitorais = sorted(tse["ANO_ELEICAO"].dropna().astype(int).unique())
anos_presidenciais = sorted(tse.loc[tse["CD_CARGO"].eq(1), "ANO_ELEICAO"].dropna().astype(int).unique())
anos_governadores = sorted(tse.loc[tse["CD_CARGO"].eq(3), "ANO_ELEICAO"].dropna().astype(int).unique())


def ano_eleitoral_referencia(ano: int, anos_disponiveis: list[int]):
    return max((eleicao for eleicao in anos_disponiveis if eleicao <= ano), default=pd.NA)


base_integrada["ano_eleitoral_referencia"] = base_integrada["ano"].map(
    lambda ano: ano_eleitoral_referencia(ano, anos_eleitorais)
).astype("Int64")
base_integrada["ano_eleitoral_presidente_referencia"] = base_integrada["ano"].map(
    lambda ano: ano_eleitoral_referencia(ano, anos_presidenciais)
).astype("Int64")
base_integrada["ano_eleitoral_governador_referencia"] = base_integrada["ano"].map(
    lambda ano: ano_eleitoral_referencia(ano, anos_governadores)
).astype("Int64")


def valores_unicos(series: pd.Series) -> str:
    valores = sorted({str(valor).strip() for valor in series.dropna() if str(valor).strip()})
    return " | ".join(valores)


def resumo_tse(frame: pd.DataFrame, chaves: list[str], prefixo: str) -> pd.DataFrame:
    colunas = ["NM_CANDIDATO", "SG_PARTIDO", "NM_PARTIDO", "NM_COLIGACAO"]
    disponiveis = [coluna for coluna in colunas if coluna in frame.columns]
    resumo = frame.groupby(chaves, as_index=False, dropna=False)[disponiveis].agg(valores_unicos)
    return resumo.rename(columns={coluna: f"{prefixo}_{coluna.lower()}" for coluna in disponiveis})


tse_presidentes = tse[tse["CD_CARGO"].eq(1)].copy()
tse_governadores = tse[tse["CD_CARGO"].eq(3) & tse["SG_UF"].ne("BR")].copy()

presidentes = resumo_tse(tse_presidentes, ["ANO_ELEICAO"], "tse_presidente")
governadores = resumo_tse(tse_governadores, ["ANO_ELEICAO", "SG_UF"], "tse_governador")

base_integrada = base_integrada.merge(
    presidentes,
    left_on="ano_eleitoral_presidente_referencia",
    right_on="ANO_ELEICAO",
    how="left",
    validate="many_to_one",
).drop(columns=["ANO_ELEICAO"])
base_integrada = base_integrada.merge(
    governadores,
    left_on=["ano_eleitoral_governador_referencia", "sigla_uf"],
    right_on=["ANO_ELEICAO", "SG_UF"],
    how="left",
    validate="many_to_one",
).drop(columns=["ANO_ELEICAO", "SG_UF"])

print("TSE derivado:", tse.shape, "| presidentes:", presidentes.shape, "| governadores:", governadores.shape)
print("Linhas sem presidente de referência:", int(base_integrada["tse_presidente_nm_candidato"].isna().sum()))
print("Linhas sem governador de referência:", int(base_integrada["tse_governador_nm_candidato"].isna().sum()))

print("\nAmostra da base integrada:")
print(base_integrada[["mes", "capital", "sigla_uf", "valor", "var_mensal",
                      "tempo_em_horas", "ipca_var_mensal_pct", "ipca_tabela_sidra",
                      "ano_eleitoral_presidente_referencia",
                      "ano_eleitoral_governador_referencia", "tse_presidente_sg_partido",
                      "tse_governador_sg_partido"]]
      .tail(8).to_string(index=False))

arquivo_integrada_csv = TRATADOS_DIR / "base_integrada.csv"
arquivo_integrada_parquet = TRATADOS_DIR / "base_integrada.parquet"
base_integrada.to_csv(arquivo_integrada_csv, index=False, encoding="utf-8")
base_integrada.to_parquet(arquivo_integrada_parquet, index=False)
print("Integrada com TSE ->", arquivo_integrada_csv)

# %% [markdown]
# ## 9. Observações finais
#
# - **Unidade de observação:** capital × mês (DIEESE), com a variação mensal do IPCA
#   (grupo Alimentação e bebidas) agregada por mês.
# - **Valores originais preservados:** nenhum número foi alterado; anomalias conhecidas
#   de captura (ex.: 2016-01 em que `var_mensal` guarda o valor da cesta de
#   dezembro/2015 por configuração da tabela; dez/2005-2007 e 2013 com sinais/colunas
#   deslocados) ficam **sinalizadas** pela flag `flag_diverge_var_mensal` e registradas
#   no log de duplicatas/este notebook.
# - **Lacunas reais:** entre 2025-05 e 2025-06 o DIEESE publicou apenas 17 capitais
#   (a cesta foi readequada); as demais capitais só voltam em 2025-07. Isso aparece em
#   `n_capitais_no_mes`/`periodo_cobertura`.
# - **Reprodutibilidade:** reexecutar este notebook reproduz os mesmos arquivos a partir
#   do `dados_Coletados.csv` bruto e do CSV/IPCA tratado.