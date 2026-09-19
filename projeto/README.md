# Trabalho 1 — Aquisição de Dados: Cesta Básica × Inflação dos Alimentos × Governos

## Descrição do projeto

Este repositório contém a coleta, integração e limpeza dos dados do **Trabalho 1 da disciplina Ciência de Dados**. O tema investiga a relação entre a variação dos preços da **cesta básica**, a **inflação dos alimentos** e as diferentes **gestões presidenciais e estaduais** no Brasil desde 1994, considerando ciclos eleitorais e espectros partidários.

**Pergunta motivadora** (enunciado): de que maneira a variação nos preços da cesta básica e a inflação dos alimentos se comportaram ao longo das diferentes gestões presidenciais e estaduais no Brasil desde 1994, e como os ciclos eleitorais e espectros partidários se correlacionam com esses momentos de instabilidade?

**Fontes de dados (3 fontes):**

| Fonte | O que fornece | Método |
|---|---|---|
| IBGE/SIDRA | IPCA do grupo "Alimentação e bebidas" (variação mensal %, 1994–2026) | API (`apisidra.ibge.gov.br`) |
| DIEESE | Pesquisa Nacional da Cesta Básica (valor, variações, % do salário mínimo, tempo de trabalho por capital, 2005–2026) | Web scraping de HTML + PDFs |
| TSE/Dados Abertos | Candidatos e resultados de eleições presidenciais/gubernatoriais 1994–2022 | API (CKAN + REST) |

## Integrantes

- Nome 1
- Nome 2
- Nome 3
- Nome 4

## Estrutura das pastas

```text
.
├── Dados do DIEESE/                 # coleta e parse do DIEESE (notebook + scripts)
│   ├── coletaDados.ipynb            # notebook reprodutível da coleta/limpeza do DIEESE
│   ├── coletaDeDados.py             # scraping da página de índice (boletins)
│   ├── limpezaHTML.py               # converte páginas "casca" HTML em PDFs reais
│   ├── limpezaPDF.py                # parser das tabelas dos PDFs
│   ├── especifico201001html.py      # correção do boletim de 201001
│   └── dados_Coletados.csv          # consolidação bruta do parse (4758 linhas)
├── dados_brutos/                    # dados brutos (exatamente como coletados)
│   └── dieese/                      # 260 PDFs de boletins + provenance_log.csv
├── notebook_coleta.ipynb            # rascunho/consolidação (a completar)
├── notebook_ipca_alimentacao_1994_2026.py   # coleta do IPCA via API SIDRA + limpeza
├── notebook_tratamento_base_integrada.py    # tratamento estrutural + integração DIEESE×IPCA
├── projeto/
│   ├── README.md                    # este arquivo
│   ├── dados_brutos/                # JSONs brutos da API SIDRA + proveniência IPCA
│   ├── dados_tratados/              # base tratada e integrada (CSV + Parquet)
│   └── documentacao/
│       ├── dataset_card.md          # ficha descritiva da base
│       ├── proveniencia.csv         # registro de proveniência (3 fontes)
│       └── passo_a_passo_sidra_t61.md
├── GUIA_TRABALHO_1_AQUISICAO_DE_DADOS.md  # guia do trabalho (instruções/rubrica)
├── Info_Trabalho_CD (1).pdf        # enunciado do trabalho
└── Trabalho1_Aquisicao_de_Dados (1).pdf   # roteiro de aquisição de dados
```

## Dependências

Python 3.10+ com as bibliotecas:

- `requests`
- `beautifulsoup4`
- `pdfplumber`
- `pandas`
- `pyarrow` (para os arquivos Parquet)

Instalação sugerida (ambiente Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 pdfplumber pandas pyarrow
```

## Instruções de execução

O fluxo completo tem três etapas. **A coleta exige acesso à internet** e, no caso do DIEESE, respeita o `Crawl-delay` da página (10 s entre requisições — rodar do zero leva tempo).

1. **Fonte 1 — IPCA (IBGE/SIDRA):**
   ```bash
   python notebook_ipca_alimentacao_1994_2026.py
   ```
   Baixa as cinco tabelas SIDRA (58/655/2938/1419/7060) pela API, concatena e escreve a série tratada em `projeto/dados_tratados/ipca_alimentacao_tratada.{csv,parquet}`. Os JSONs brutos ficam em `projeto/dados_brutos/`.

2. **Fonte 2 — Cesta básica (DIEESE):**
   execute `Dados do DIEESE/coletaDados.ipynb` (Jupyter) ou diretamente os scripts `coletaDeDados.py` → `limpezaHTML.py` → `limpezaPDF.py`. Os boletins vão para `dados_brutos/dieese/` e o parse consolidado para `Dados do DIEESE/dados_Coletados.csv`.

3. **Tratamento + integração:**
   ```bash
   python notebook_tratamento_base_integrada.py
   ```
   Lê `Dados do DIEESE/dados_Coletados.csv` e `projeto/dados_brutos/ipca_alimentacao_1994_2026.csv`, normaliza (estruturalmente, sem alterar valores), remove duplicatas, aplica flags de anomalia e gera em `projeto/dados_tratados/`:
   - `cesta_basica_dieese_tratada.{csv,parquet}`
   - `ipca_alimentacao_tratada.{csv,parquet}` (espelho da série IPCA)
   - `base_integrada.{csv,parquet}` (join DIEESE × IPCA pela chave `mes`)
   - `log_duplicatas_removidas.csv`

A fonte 3 (TSE) está testada e documentada, mas **ainda não produz arquivos neste pacote**; sua integração com a base (por `ano` e `partido` do governo) pertence à etapa de análise.

## Localização dos dados

| Tipo | Caminho |
|---|---|
| Brutos DIEESE | `dados_brutos/dieese/` (+ `Dados do DIEESE/dados_Coletados.csv` consolidado) |
| Brutos IBGE/SIDRA (API) | `projeto/dados_brutos/` |
| Brutos TSE (pendente) | `dados_brutos/tse/` |
| **Base tratada e integrada** | `projeto/dados_tratados/base_integrada.{parquet,csv}` |
| Proveniência | `projeto/documentacao/proveniencia.csv` |
| Dataset card | `projeto/documentacao/dataset_card.md` |

## Observações

- **Nenhum valor foi alterado** na etapa de tratamento; irregularidades conhecidas de parse do DIEESE ficam sinalizadas na coluna `flag_diverge_var_mensal` e detalhadas no dataset card (A.5). Não use `var_mensal` dessas linhas sem considerar o flag.
- Não há senhas, tokens ou chaves privadas no pacote.
- Entrega conforme o guia: prazo indicado **10/09/2026**, formato **ColabWeb**.

## Veja também

- `GUIA_TRABALHO_1_AQUISICAO_DE_DADOS.md` — roteiro completo, estrutura e rubrica de avaliação.
- `projeto/documentacao/dataset_card.md` — ficha descritiva, limitações e decisões.
- `projeto/documentacao/proveniencia.csv` — registro de onde, quando e como cada fonte foi coletada.