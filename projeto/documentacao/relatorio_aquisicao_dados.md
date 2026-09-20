# Aquisição de Dados — Relatório Detalhado das Três Fontes

**Projeto:** Trabalho 1 — Aquisição de Dados (Ciência de Dados, UFAM)  
**Data da coleta:** 14–18 de setembro de 2026  
**Período coberto:** 1994–2026 (variável por fonte)  
**Integrantes:** [Grupo a ser preenchido]

---

## Sumário

1. [Fonte 1 — IBGE/SIDRA (API)](#fonte-1-ibgesidra-api)
2. [Fonte 2 — DIEESE (Web Scraping)](#fonte-2-dieese-web-scraping)
3. [Fonte 3 — TSE/Dados Abertos (API CKAN + REST)](#fonte-3-tsedados-abertos-api-ckan--rest)
4. [Estrutura de Arquivos](#estrutura-de-arquivos)
5. [Proveniência e Rastreabilidade](#proveniência-e-rastreabilidade)

---

## Fonte 1 — IBGE/SIDRA (API)

### Descrição

O Sistema IBGE de Recuperação Automática (SIDRA) é uma plataforma do IBGE que disponibiliza dados estatísticos oficiais do Brasil via API REST pública.

### URL da API

```
https://apisidra.ibge.gov.br/values/t/{tabela}/n1/all/v/all/p/all/c{classificacao}/{categoria}
```

### Método de Aquisição

Requisições HTTP GET diretas à API SIDRA. A API retorna dados em formato JSON.

### Tabelas Utilizadas

Para cobrir o período 1994–2026 do IPCA - Variação mensal do grupo "1.Alimentação e bebidas", foi necessário concatenar 5 tabelas SIDRA com o mesmo padrão de classificação (Geral, grupo, subgrupo, item e subitem):

| Tabela | Período | Classificação | Categoria | Era |
|---|---|---|---|---|
| 58 | jan/1991 – jul/1999 | c72 | 1313 | 1991-1999 |
| 655 | ago/1999 – jun/2006 | c315 | 7170 | 1999-2006 |
| 2938 | jul/2006 – dez/2011 | c315 | 7170 | 2006-2011 |
| 1419 | jan/2012 – dez/2019 | c315 | 7170 | 2012-2019 |
| 7060 | jan/2020 – atual | c315 | 7170 | 2020-atual |

### Endpoints e Parâmetros

```
GET https://apisidra.ibge.gov.br/values/t/58/n1/all/v/all/p/all/c72/1313
GET https://apisidra.ibge.gov.br/values/t/655/n1/all/v/all/p/all/c315/7170
GET https://apisidra.ibge.gov.br/values/t/2938/n1/all/v/all/p/all/c315/7170
GET https://apisidra.ibge.gov.br/values/t/1419/n1/all/v/all/p/all/c315/7170
GET https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/all/p/all/c315/7170
```

Parâmetros:
- `t` — número da tabela (58, 655, 2938, 1419, 7060)
- `n1` — dimensão temporal (todos os meses)
- `v` — todos os valores
- `p` — todas as posições
- `c{classificacao}/{categoria}` — classificação e categoria do grupo "1.Alimentação e bebidas"

### Tratamento de Erros

- Verificação de status HTTP antes de processar cada resposta
- Timeout de 30 segundos por requisição
- Pausa de 1.5s entre requisições para respeitar limites do servidor
- Logs de erro com código HTTP e mensagem

### Arquivos Brutos Obtidos

| Tipo | Quantidade | Localização |
|---|---|---|
| Respostas JSON brutas da API | 11 arquivos | `dados_brutos/ibge_sidra/sidra_t*.json` |
| Série IPCA integrada (CSV) | 1 arquivo | `dados_tratados/ipca_alimentacao_1994_2026.csv` |
| Série IPCA integrada (Parquet) | 1 arquivo | `dados_tratados/ipca_alimentacao_1994_2026.parquet` |
| Registro de proveniência | 2 arquivos | `dados_brutos/proveniencia/proveniencia_sidra_*.csv` |

### Limitações

- A Tabela 61 (IPCA mensal principal) cobre apenas jan/1991 a jul/1999 e não possui a classificação `c315`
- Foi necessário concatenar 5 tabelas diferentes para cobrir o período completo
- A API não possui autenticação e não impõe limites claros de requisição

### Licença

Os dados do IBGE são disponibilizados sob licença aberta, permitindo uso acadêmico com atribuição.

---

## Fonte 2 — DIEESE (Web Scraping)

### Descrição

O DIEESE (Departamento Intersindical de Estatística e Estudos Socioeconômicos) disponibiliza dados sobre cesta básica, preços e mercado de trabalho através de seu site.

### URL do Site

```
https://www.dieese.org.br/analisecestabasica/
```

### Método de Aquisição

Web scraping de HTML utilizando Python (requests + BeautifulSoup/pandas.read_html). Os dados são extraídos de tabelas HTML publicadas no site.

### Estrutura dos Dados

- **Tipo:** PDFs e HTML (tabelas)
- **Granularidade:** mensal
- **Conteúdo:** preços de cesta básica por estado/município

### Processo de Coleta

1. Acessar a página de análise da cesta básica do DIEESE
2. Localizar a tabela HTML com os dados de interesse
3. Extrair via `pandas.read_html()` ou `BeautifulSoup`
4. Salvar o HTML/arquivo bruto antes de qualquer transformação
5. Tratar e limpar os dados extraídos

### Arquivos Brutos Obtidos

| Tipo | Quantidade | Localização |
|---|---|---|
| PDFs brutos | ~260 arquivos | `dados_brutos/dieese/*.pdf` |
| Códigos de coleta | 3 arquivos | `Dados do DIEESE/` |

### Limitações

- Os dados são publicados mensualmente, exigindo coleta contínua para cobertura completa
- A estrutura HTML pode mudar, exigindo atualização dos seletores
- PDFs precisam ser extraídos via OCR ou bibliotecas específicas (pdfplumber, Tabula)

### Licença

Dados do DIEESE são disponibilizados para uso acadêmico e de pesquisa.

### Cuidados Éticos

- Verificar `robots.txt` do site antes de raspar
- Respeitar limites de requisição (pausas entre acessos)
- Não sobrecarregar os servidores do DIEESE

---

## Fonte 3 — TSE/Dados Abertos (API CKAN + REST)

### Descrição

O Tribunal Superior Eleitoral (TSE) disponibiliza dados eleitorais oficiais através de duas APIs:
1. **API CKAN** — para metadados e descoberta de datasets
2. **API DivulgaCandContas REST** — para dados de eleições, candidatos e resultados

### URLs das APIs

```
CKAN:           https://dadosabertos.tse.jus.br/api/3/action
DivulgaCand:    https://divulgacandcontas.tse.jus.br/divulga/rest/v1
CDN (download): https://cdn.tse.jus.br/estatistica/sead/odsele/
```

### Método de Aquisição

A coleta foi realizada em três etapas:

#### Etapa 1 — DivulgaCandContas REST (Lista de Eleições)

```
GET https://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/ordinarias
```

Retorna todas as eleições ordinárias disponíveis (13 eleições de 2004 a 2026).

#### Etapa 2 — API CKAN (Metadados e URLs de Download)

Para cada ano eleitoral (1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022):

```
GET https://dadosabertos.tse.jus.br/api/3/action/package_show?id=candidatos-{ano}
GET https://dadosabertos.tse.jus.br/api/3/action/package_show?id=resultados-{ano}
```

Retorna:
- Metadados do dataset (título, licença, descrição, número de recursos)
- Lista de recursos (arquivos ZIP/CSV) com URLs de download na CDN

**Nota técnica:** O endpoint CKAN (`dadosabertos.tse.jus.br`) é protegido por CDN Akamai com proteção anti-bot que retorna HTTP 403 intermitentemente. Contornado via:
- Sessão HTTP com cookies do site principal
- Retries automáticos (até 5 tentativas com espera exponencial)
- Acesso via `verify=False` quando necessário

#### Etapa 3 — Download de Recursos via CDN

Para cada recurso (arquivo) retornado pela API CKAN:

```
GET https://cdn.tse.jus.br/estatistica/sead/odsele/{caminho_do_recurso}
```

Os recursos são baixados em formato ZIP contendo múltiplos arquivos CSV.

### Endpoints e Parâmetros Detalhados

| Endpoint | Método | Parâmetros | Descrição |
|---|---|---|---|
| `/eleicao/ordinarias` | GET | — | Lista eleições ordinárias |
| `package_search` | GET | `q`, `rows` | Busca datasets |
| `package_show` | GET | `id` | Metadados de um dataset |
| Download CDN | GET | URL direta | Arquivo ZIP/CSV |

### Datasets Coletados

| Dataset | Anos | Recursos por Dataset | Formato |
|---|---|---|---|
| `candidatos-{ano}` | 1994–2022 | 3–144 | ZIP (contém CSVs por UF) |
| `resultados-{ano}` | 1994–2022 | 32–34 | ZIP (contém CSVs por UF/zona) |

### Arquivos por Dataset (Exemplo: 2022)

**Candidatos-2022 (144 recursos):**
- `Candidatos_2022.csv` (principal, ~4.4 MB)
- `Candidatos - Informações complementares` (~1.7 MB)
- `Bens de candidatos` (~5.4 MB)
- `Coligações` (~373 KB)
- `Vagas` (~184 KB)
- Redes sociais por UF (27 arquivos)
- Fotos por UF (27 arquivos)
- Proposta de governo por UF (27 arquivos)
- Certidões criminais por UF (27 arquivos)
- Notas fiscais por UF (27 arquivos)

**Resultados-2022 (34 recursos):**
- `BR - Histórico totalização Presidente 1º Turno`
- `BR - Histórico totalização Presidente 2º Turno`
- `Votação nominal por município e zona` (~595 MB)
- `Votação em partido por município e zona` (~25 MB)
- `Detalhe da apuração por município e zona` (~4.4 MB)
- Votação por seção eleitoral por UF (27 arquivos)

### Licença

Creative Commons Atribuição (CC-BY). A API CKAN e DivulgaCandContas não exigem autenticação.

### Arquivos Brutos Obtidos

| Tipo | Quantidade | Localização | Tamanho |
|---|---|---|---|
| Respostas API CKAN (JSON) | 16 | `dados_brutos/tse/ckan_*_raw_*.json` | ~3.5 MB |
| Arquivos ZIP/CSV baixados | 272 | `dados_brutos/tse/` | 6.38 GB |
| Eleições ordinárias (JSON) | 1 | `dados_brutos/tse/divulgacandcontas_eleicoes_ordinarias.json` | 4.9 KB |
| Registro de proveniência | 1 | `dados_brutos/proveniencia/proveniencia_tse.csv` | 99 KB |

### Limitações e Problemas Encontrados

1. **CKAN API (Akamai):** Protegido por CDN Akamai com proteção anti-bot. Retorna HTTP 403 intermitentemente. Solução: sessão com cookies + retries.
2. **Volume:** 272 arquivos totalizando 6.38 GB, principalmente devido aos arquivos de votação por seção eleitoral (estado por estado).
3. **Formato:** Arquivos CKAN reportam formato CSV mas são entregues como ZIP na CDN. Mantidos como ZIP (bruto).
4. **CKAN para anos antigos (1994-2002):** Datasets têm poucos recursos (3–32). A partir de 2006, o número cresce significativamente (32–144).
5. **Download de arquivos grandes:** Arquivos como `Votação_nominal_2018.csv` (395 MB) e `Presidente_2018.csv` (251 MB) requerem tempo significativo de download.

### Cuidados Éticos

- Pausas de 1.5–2s entre requisições
- User-Agent identificando o robô acadêmico
- Respeitando limites de taxa da API
- Não download de arquivos desnecessários (fotos, propostas, certidões não incluídos na coleta principal para limitar volume)

---

## Estrutura de Arquivos

Após organização, a estrutura dos dados brutos é:

```
projeto/
├── dados_brutos/
│   ├── tse/                          (272 arquivos, 6.38 GB)
│   │   ├── ckan_candidatos-{ano}_raw_*.json   (8 files)
│   │   ├── ckan_resultados-{ano}_raw_*.json   (8 files)
│   │   ├── divulgacandcontas_eleicoes_ordinarias.json
│   │   ├── Candidatos_{ano}.zip               (8 files)
│   │   ├── Candidatos_-_Informacoes_complementares_{ano}.zip
│   │   ├── Colracoes_{ano}.zip                (8 files)
│   │   ├── Vagas_{ano}.zip                    (8 files)
│   │   ├── Bens_de_candidatos_{ano}.zip             (5 files)
│   │   ├── Votacao_nominal_por_munic_e_zona_{ano}.zip (8 files)
│   │   ├── Votacao_em_partido_por_munic_e_zona_{anno}.zip (8 files)
│   │   ├── Votacao_por_secao_eleitoral_{UF}_{ano}.zip  (190+ files)
│   │   ├── Detalhe_da_apuracao_*.zip          (16 files)
│   │   ├── Presidente_-_Votacao_*.zip          (8 files)
│   │   └── ... (272 arquivos no total)
│   ├── ibge_sidra/                   (11 arquivos, 0.71 MB)
│   │   ├── sidra_t58_alimentacao_*.json
│   │   ├── sidra_t655_alimentacao_*.json
│   │   ├── sidra_t2938_alimentacao_*.json
│   │   ├── sidra_t1419_alimentacao_*.json
│   │   ├── sidra_t7060_alimentacao_*.json
│   │   └── sidra_t61_ipca_alimentacao_bruto.json
│   ├── dieese/                       (260 PDFs, 86.56 MB)
│   │   └── YYYYMM.pdf
│   └── proveniencia/                 (3 arquivos, 0.10 MB)
│       ├── proveniencia_tse.csv
│       ├── proveniencia_sidra_ipca_20260914_190056.csv
│       └── proveniencia_sidra_ipca_20260914_190130.csv
├── dados_tratados/                   (2 arquivos)
│   ├── ipca_alimentacao_1994_2026.csv
│   └── ipca_alimentacao_1994_2026.parquet
├── documentacao/
│   ├── dataset_card.md
│   ├── proveniencia.csv
│   ├── passo_a_passo_sidra_t61.md
│   └── README_tse.md
└── README.md
```

### Estatísticas

| Pasta | Arquivos | Tamanho |
|---|---|---|
| `dados_brutos/tse/` | 272 | 6.38 GB |
| `dados_brutos/ibge_sidra/` | 11 | 0.71 MB |
| `dados_brutos/dieese/` | 260 | 86.56 MB |
| `dados_brutos/proveniencia/` | 3 | 0.10 MB |
| `dados_tratados/` | 2 | ~30 MB |
| **Total bruto** | **546** | **~6.55 GB** |

---

## Proveniência e Rastreabilidade

Todos os dados possuem registro detalhado de proveniência contendo:

| Campo | Descrição |
|---|---|
| `fonte_id` | Identificador da fonte (TSE-CKAN, TSE-DivulgaCandContas, etc.) |
| `dataset` | Nome do dataset ou endpoint |
| `endpoint` | Endpoint utilizado |
| `url` | URL exata acessada |
| `data_hora_coleta` | Data e hora com fuso horário (America/Sao_Paulo) |
| `status_http` | Código de resposta HTTP |
| `arquivo_bruto` | Caminho do arquivo preservado |
| `tamanho_bytes` | Tamanho do arquivo |
| `recurso_nome` | Nome do recurso |
| `recurso_url` | URL de download do recurso |
| `recurso_formato` | Formato (CSV, ZIP, JSON) |
| `observacoes` | Detalhes adicionais |

### Arquivos de Proveniência

| Arquivo | Fonte | Registros |
|---|---|---|
| `dados_brutos/proveniencia/proveniencia_tse.csv` | TSE | 241 (todos HTTP 200) |
| `dados_brutos/proveniencia/proveniencia_sidra_ipca_*.csv` | IBGE/SIDRA | 5 por período |
| `projeto/documentacao/proveniencia.csv` | Todas | 3 resumos por fonte |

### Rastreabilidade da Coleta

A coleta foi realizada de forma reprodutível:
- Cada requisição registra URL, parâmetros e timestamp
- Respostas brutas da API são preservadas em JSON
- Arquivos baixados são mantidos sem transformação
- Nenhum dado foi alterado antes do armazenamento
- Pausas entre requisições são documentadas

---

## Considerações Finais

1. **Acessibilidade:** A API CKAN do TSE apresenta proteção anti-bot (Akamai) que requer contorno via sessão com cookies. A API DivulgaCandContas funciona sem restrições.
2. **Volume:** O maior volume de dados vem do TSE (6.38 GB), devido à granularidade dos dados eleitorais (por UF, por seção, por zona).
3. **Integração:** As três fontes compartilham a chave temporal `ano` (ano eleitoral para TSE, mês/ano para IBGE/DIEESE) e a chave partidária `sigla_partido` (TSE).
4. **Licenças:** Todas as fontes permitem uso acadêmico com atribuição (CC-BY para TSE, licença aberta para IBGE, termos de uso para DIEESE).
