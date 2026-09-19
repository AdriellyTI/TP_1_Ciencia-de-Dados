# Dataset Card — Trabalho 1: Aquisição de Dados

## A.1 Identificação

**Nome da base:**  
`Cesta_Basica_DIEESE_x_IPCA_SIDRA_BR` — Base integrada da cesta básica (DIEESE) com o IPCA do grupo "Alimentação e bebidas" (IBGE/SIDRA), 2005–2026.

**Grupo / integrantes:**

- Nome 1
- Nome 2
- Nome 3
- Nome 4

**Tema:**  
Análise da relação entre a variação dos preços da cesta básica, a inflação dos alimentos e os diferentes períodos de governos presidenciais e estaduais no Brasil desde 1994.

**Pergunta motivadora:**  
"De que maneira a variação nos preços da cesta básica e a inflação dos alimentos se comportaram ao longo das diferentes gestões presidenciais e estaduais no Brasil desde 1994, e como os ciclos eleitorais e espectros partidários se correlacionam com esses momentos de instabilidade?" (texto do enunciado `Info_Trabalho_CD (1).pdf`)

**Data ou período da coleta:**  
- IBGE/SIDRA (IPCA): **14/09/2026, ~19:00–19:01 (UTC)** — registrado em `proveniencia_sidra_ipca_20260914_190056.csv` (e `.csv` 190130, execução duplicada).
- DIEESE (cesta básica): **18/09/2026, 05:11–05:23 (America/Sao_Paulo)** — última execução registrada em `dados_brutos/dieese/provenance_log.csv` (o log cobre também execuções anteriores do mesmo fluxo).
- TSE/Dados Abertos: a registrar pelo grupo (fonte testada, ainda sem arquivos no pacote).

---

## A.2 Fontes e proveniência

### Fonte 1 — IBGE/SIDRA (API)

**Nome e URL:**  
IBGE/SIDRA — IPCA, grupo "Alimentação e bebidas". API `apisidra.ibge.gov.br`; páginas das tabelas em `https://sidra.ibge.gov.br/tabela/{58, 655, 2938, 1419, 7060}`.

**Método de aquisição:**  
API web (GET).

**Endpoint e parâmetros:**  
`https://apisidra.ibge.gov.br/values/t/{tabela}/n1/all/v/all/p/all/c72/1313` (tabela 58) ou `.../c315/7170` (tabelas 655, 2938, 1419 e 7060). Parâmetros: `n1=all` (Brasil), `v=all`, `p=all` (todos os períodos), classificações `c72/1313` ou `c315/7170` (grupo "Alimentação e bebidas").

**Dados coletados:**  
Variação mensal (%) do IPCA do grupo "Alimentação e bebidas", Brasil, de jan/1991 a ago/2026, obtida por meio de cinco tabelas históricas sobrepostas: t58 (103 registros, jan/1991–jul/1999), t655 (83, ago/1999–jun/2006), t2938 (66, jul/2006–dez/2011), t1419 (96, jan/2012–dez/2019) e t7060 (80, jan/2020–ago/2026) — **428 registros** no total.

**Licença ou termos de uso:**  
Dados públicos do IBGE. A API SIDRA (`apisidra.ibge.gov.br`) é acessível sem autenticação. Não foi localizada uma licença formalmente marcada nos metadados da consulta; registra-se essa ausência (não se inventa licença onde não há).

**O uso pretendido é permitido?**  
Sim. Os dados são públicos e a API não exige autenticação; o uso acadêmico é o público-alvo do serviço. Atribuição ao IBGE será feita no trabalho.

**Arquivo bruto correspondente:**  
`projeto/dados_brutos/sidra_t{58,655,2938,1419,7060}_alimentacao_20260914_190056.json` (e `_190130.json`, conteúdo idêntico). Arquivo complementar de exploração: `projeto/dados_brutos/sidra_t61_ipca_alimentacao_bruto.json` (tabela 61, peso mensal do grupo).

### Fonte 2 — DIEESE (web scraping)

**Nome e URL:**  
DIEESE — Pesquisa Nacional da Cesta Básica. Página de índice dos boletins: `https://www.dieese.org.br/analisecestabasica/analiseCestaBasicaAnteriores.html` (boletins individuais em `https://www.dieese.org.br/analisecestabasica/{ano}/{aammes}cestabasica.pdf`).

**Método de aquisição:**  
Web scraping de HTML (com download dos PDFs de boletins).

**Página, tabela ou seletores utilizados:**  
Links da página de índice cujo `href` casa o padrão `(cestabasica\d{6}|\d{6}cestabasica)`; em cada boletim, a tabela "Resultados Mensais" com uma linha por capital (parse implementado em `Dados do DIEESE/limpezaPDF.py` e `coletaDados.ipynb`).

**Dados coletados:**  
Por capital e mês: valor da cesta (R$), variação mensal (%) , variação no ano (%) , variação em 12 meses (%) , relação cesta/salário mínimo (%) e tempo de trabalho necessário (formato `XhYm`). **259 meses** (jan/2005–jul/2026), 16–27 capitais conforme o período, **4758 linhas** consolidadas (brutas, sem tratamento) em `Dados do DIEESE/dados_Coletados.csv`. 260 PDFs brutos em `dados_brutos/dieese/`.

**Licença ou termos de uso:**  
Não foi localizada licença explícita nas páginas públicas dos boletins do DIEESE. Registra-se essa ausência; o conteúdo é de divulgação pública, mas não há autorização formal de redistribuição registrada.

**O uso pretendido é permitido?**  
Sim, para fins acadêmicos, com atribuição ao DIEESE; o acesso às páginas é público e o `robots.txt` não bloqueia os caminhos usados (ver A.6). Não é feita redistribuição dos boletins além do uso no trabalho.

**Arquivo bruto correspondente:**  
`dados_brutos/dieese/*.pdf` (260 boletins), `dados_brutos/dieese/provenance_log.csv`, e a consolidação do parse `Dados do DIEESE/dados_Coletados.csv`. Os scripts de coleta estão em `Dados do DIEESE/`.

### Fonte 3 — TSE/Dados Abertos (API)

**Nome e URL:**  
Portal de Dados Abertos do TSE — `https://dadosabertos.tse.jus.br/`  
DivulgaCandContas REST — `https://divulgacandcontas.tse.jus.br/divulga/rest/v1`

**Método de aquisição:**  
API web (CKAN + REST).

**Endpoint e parâmetros:**  
- CKAN: `https://dadosabertos.tse.jus.br/api/3/action`  
  - `package_search?q=candidatos` — busca datasets de candidatos  
  - `package_show?id=candidatos-{ano}` — metadados e recursos (URLs de download)  
  - `resource_show?id=<resource_id>` — detalhes de um recurso  
- DivulgaCandContas REST: `https://divulgacandcontas.tse.jus.br/divulga/rest/v1`  
  - `/eleicao/ordinarias` — lista eleições ordinárias  
  - `/candidatura/listar/{ano}/{municipio_cod}/{eleicao_id}/{cargo_cod}/candidatos` — lista candidatos

**Dados coletados:**  
Dados de candidatos (nome, partido, cargo, UF) e resultados eleitorais para as eleições presidenciais e gubernatoriais de 1994 a 2022 (1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022). Datasets `candidatos-{ano}` e `resultados-{ano}` no formato ZIP contendo arquivos CSV.

**Licença ou termos de uso:**  
Creative Commons Atribuição (CC-BY).

**O uso pretendido é permitido?**  
Sim. A licença CC-BY permite uso acadêmico desde que se atribua a fonte ao TSE. A API CKAN não exige autenticação.

**Arquivo bruto correspondente:**  
`dados_brutos/tse/` (arquivos ZIP baixados da CDN do TSE) e `dados_brutos/tse_ckan_api_resposta_YYYYMMDD_HHMMSS.json` (resposta bruta da API CKAN). *Estes arquivos ainda não estão presentes neste pacote.*

### Chave de integração

**Chave ou conjunto de chaves:**  
`mes` (AAAAMM).

**Campo correspondente na fonte IBGE/SIDRA:**  
`D3C`/`D3N` do JSON de resposta (ano e mês da variação), normalizado para AAAAMM (ex.: "janeiro 1991" → `199101`).

**Campo correspondente na fonte DIEESE:**  
`aammes` (6 dígitos) do boletim, convertido para `mes` (ex.: `200501`).

**Campo correspondente na fonte TSE/Dados Abertos:**  
`ano` (ano eleitoral) e `sigla_partido` (partido do candidato/governador/presidente eleito). **A fonte TSE não entra nesta base integrada** — a integração por `ano`/`sigla_partido` será feita na etapa de análise.

**Normalizações realizadas:**  
- Grafias dos nomes das capitais: 61 grafias distintas (variações de maiúsculas, acentos, "São Luís"/"Sao Luis", sufixos "(1)") mapeadas para 27 nomes canônicos e suas siglas de UF.
- Remoção de marcadores de rodapé "(1)" e espaços duplos.
- Datas: `aammes` (AAAAMM) e mês/ano do SIDRA → coluna `mes` padrão; coluna `data_referencia` ISO (AAAA-MM).
- Números: padrão decimal brasileiro ("1.234,56" → `1234.56`); variações em % convertidas para `float`.
- Tempo: "111h 57min" → `tempo` compacto `XhYm` (mantendo a grafia original) + `tempo_em_horas` numérico derivado.
- Nada foi alterado nos **valores numéricos** coletados; as irregularidades ficaram sinalizadas por flags (ver A.5).

**Tipo de junção utilizado:**  
`LEFT JOIN` da base DIEESE com a série IPCA pela chave `mes` (com validação `many_to_one` — cada mês é único na série IPCA).

**Tratamento dos registros sem correspondência:**  
Nenhum registro da base DIEESE ficou sem IPCA (todos os meses de jan/2005 a jul/2026 existem na série IPCA tratada). A base é construída sobre os meses cobertos pelo DIEESE.

---

## A.3 Dicionário de variáveis

Variáveis da base tratada (24 colunas de `base_integrada`):

| Variável | Tipo | Descrição | Unidade |
|---|---|---|---|
| `mes` | numérica discreta | Ano e mês da observação, AAAAMM (chave de integração) | não se aplica (AAAAMM) |
| `data_referencia` | data/hora | Data de referência do mês (AAAA-MM) | AAAA-MM |
| `ano` | numérica discreta | Ano da observação | ano |
| `mes_num` | numérica discreta | Mês da observação (1–12) | mês |
| `capital` | categórica | Nome canônico da capital | não se aplica |
| `sigla_uf` | categórica | Unidade federativa (2 letras) | não se aplica |
| `capital_bruto` | texto | Grafia exata como apareceu no boletim original | não se aplica |
| `valor` | numérica contínua | Custo da cesta básica no mês | R$ |
| `var_mensal` | numérica contínua | Variação mensal da cesta básica | % |
| `pct_sal` | numérica contínua | Custo da cesta como proporção do salário mínimo | % |
| `tempo` | texto | Tempo de trabalho necessário para comprar a cesta (formato original XhYm) | horas e minutos |
| `tempo_em_horas` | numérica contínua | Tempo de trabalho em horas (derivada de `tempo`) | horas |
| `var_ano` | numérica contínua | Variação acumulada no ano / variação de dezembro a dezembro (quando publicada) | % |
| `var_12` | numérica contínua | Variação em 12 meses (quando publicada) | % |
| `flag_capital_variante` | booleana | `True` quando a grafia da capital no boletim difere da canônica | não se aplica |
| `flag_conflito_capital_mes` | booleana | `True` quando a mesma capital aparece mais de uma vez no mesmo mês (duplicata); **0 casos** na base | não se aplica |
| `flag_diverge_var_mensal` | booleana | `True` quando `var_mensal` é suspeita por anomalia de layout/parse (ver A.5); **84 casos** | não se aplica |
| `n_capitais_no_mes` | numérica discreta | Quantidade de capitais capturadas no mês | capitais |
| `periodo_cobertura` | categórica | Fase de metodologia/cobertura do extrato (rótulos na tabela abaixo) | não se aplica |
| `tipo_cesta` | categórica | Tipo de cesta calculada (`Cesta Básica de Alimentos - DIEESE`) | não se aplica |
| `ipca_grupo` | categórica | Grupo do IPCA correspondente (`1.Alimentação e bebidas`) | não se aplica |
| `ipca_variavel` | categórica | Variável do IPCA (`IPCA - Variação mensal`) | não se aplica |
| `ipca_var_mensal_pct` | numérica contínua | Variação mensal (%) do IPCA do grupo Alimentação e bebidas | % |
| `ipca_tabela_sidra` | numérica discreta | Tabela SIDRA de origem do valor de IPCA (55/655/2938/1419/7060) | nº da tabela |

Valores de `periodo_cobertura`:

| `periodo_cobertura` | `n_capitais` | Linhas |
|---|---|---|
| `2005-01 a 2015-12 \| 16/18 capitais, ponderação anterior` | 16 → 18 | 2232 |
| `2016-01 a 2025-04 \| 27 capitais, ponderação atualizada` | 27 | 2146 |
| `2025-05 a 2025-06 \| 17 capitais publicadas` | 14 capturadas | 28 |
| `2025-07 em diante \| 27 capitais, cesta atualizada` | 27 | 351 |

---

## A.4 Volume e granularidade

**Número final de linhas:**  
4757 (`base_integrada`; série IPCA tratada isolada: 392 meses).

**Número final de colunas:**  
24 (`base_integrada`); 6 (`ipca_alimentacao_tratada`); 20 (`cesta_basica_dieese_tratada`).

**O que representa uma linha:**  
Uma capital em um mês (observação capital × mês da pesquisa DIEESE), enriquecida com o IPCA nacional do grupo Alimentação e bebidas correspondente ao mesmo mês.

**Cobertura temporal:**  
jan/2005 a jul/2026 (base integrada). A série IPCA tratada cobre jan/1994 a ago/2026.

**Cobertura geográfica:**  
27 capitais brasileiras, com cobertura crescente ao longo do tempo: 16 capitais no início da série (2005–2008), ~17–18 até 2015, 27 a partir de 2016-01, e — após duas edições reduzidas (mai–jun/2025 com 17 capitais publicadas) — 27 capitais de jul/2025 em diante. Ver `n_capitais_no_mes`/`periodo_cobertura` para a cobertura exata por mês.

**Universo abrangido:**  
Boletins mensais da Pesquisa Nacional da Cesta Básica (DIEESE) e série mensal de IPCA do grupo "Alimentação e bebidas" (IBGE/SIDRA), para o Brasil (IPCA) e suas capitais (DIEESE).

---

## A.5 Limitações e decisões

### Dados descartados

- **1 linha duplicata exata** (SÃO PAULO, 201905) removida da base DIEESE; registro em `log_duplicatas_removidas.csv`.
- **Meses de IPCA de 1991 a 1993** (tabela 58) fora da série tratada: a base começa em **1994**, coerente com o tema do trabalho ("desde 1994").
- Nenhum outro dado foi descartado. **Nenhum valor numérico foi alterado** — as irregularidades foram registradas em flags, não corrigidas.

### Lacunas conhecidas

- `var_ano` ausente em **829** linhas, `var_12` em **451**, `var_mensal` em **41** (os boletins nem sempre publicam todos os indicadores).
- **2025-05 e 2025-06**: o DIEESE publicou apenas 17 capitais; a captura resultou em 14 (faltam Rio de Janeiro, Belo Horizonte e Campo Grande, presentes nos PDFs desses meses — o parser posicional não os reconheceu). **28 linhas** nesses meses.
- **Capitais do Norte/Nordeste** só entram a partir de 2016-01 (ponderação atualizada do DIEESE).
- A **fonte TSE** não está integrada nesta base (fica para a etapa de análise, via `ano`/`sigla_partido`).

### Decisões de limpeza relevantes

Tratamento **estrutural apenas** (sem alteração de valores):
- Normalização de grafias (61 → 27 capitais canônicas), acentos, maiúsculas, espaços, remoção de "(1)" e padronização de datas e números (ver A.2).
- Derivação de `tempo_em_horas` a partir de `tempo`.
- Separação entre arquivo bruto (`dados_Coletados.csv` / PDFs) e tratado (`dados_tratados/`).
- Anomalias de parse do DIEESE sinalizadas em `flag_diverge_var_mensal` (**84 linhas**), SEM correção dos números:
  1. **2016-01** (18 linhas): a coluna "Valor da cesta dez/2015" do PDF foi capturada como `var_mensal`; a variação mensal verdadeira está na coluna publicada como `var_ano`.
  2. **dez/2005, 2006 e 2007** (e parte do período 200509–201309, 56 linhas): a tabela de dezembro coloca a variação anual antes do valor; `var_mensal` guardou a anual e `var_ano` guardou a mensal.
  3. **mai/2013 e set/2013**: linhas com sinal travessão "‐" tiveram o sinal de `var_mensal` invertido.
  4. **2025-07** (10 linhas): boletins da nova cesta (27 capitais) — variações de capitais do Norte incompatíveis com a série anterior (quebra de metodologia, ver `periodo_cobertura`).

### Limitações das fontes

- O parser DIEESE reconhece os campos por **posição relativa** (não por cabeçalho de coluna), então layouts atípicos (tabela extra em 2016-01, ordem invertida em dezembro, novidades da cesta 2025) geram as incoerências sinalizadas acima.
- A metodologia/extrato da cesta mudou ao longo da série (16–18 capitais, 27 capitais, e **cesta atualizada** em jul/2025); as fases não são estritamente comparáveis entre si.
- A API SIDRA exigiu **cinco tabelas** (58/655/2938/1419/7060) para cobrir o período completo, com sobreposição entre elas.
- Não foi localizada licença formal no site do DIEESE (ver A.6).

### Verificações de qualidade

- Checagem de duplicatas exatas e por chave `aammes`+`capital` (0 conflitos após remoção de 1 duplicata).
- Contagem de valores ausentes por variável.
- Medição de cobertura (`n_capitais_no_mes`) e rotulagem por fase de metodologia (`periodo_cobertura`).
- Cruzamento de uma amostra dos valores capturados (`var_mensal`, `valor`, `tempo`) com os PDFs originais do DIEESE (meses 200512, 200712, 201309, 201601, 202505–07), confirmando as anomalias descritas em A.5.
- Validação do join: 0 linhas sem IPCA na base integrada; valores de IPCA coincidentes nas sobreposições das cinco tabelas SIDRA.

---

## A.6 Considerações éticas

### Contém dados pessoais?

**Não.** As três fontes contêm apenas dados agregados (preços, índices, variações) ou dados de candidatos a cargos eletivos (nomes de candidatos/políticos são dados públicos eleitorais de interesse público, não tratarados como dados pessoais sensíveis neste trabalho).

### Restrições de uso e redistribuição

- **IBGE/SIDRA**: dados públicos, API sem autenticação; uso acadêmico permitido mediante atribuição ao IBGE.
- **DIEESE**: não foi localizada licença explícita; o conteúdo é público e acessível, mas não há autorização formal de redistribuição registrada — por isso os boletins são usados apenas como insumo do trabalho, com atribuição, e não é feita redistribuição dos arquivos.
- **TSE**: licença CC-BY, uso acadêmico permitido com atribuição.

### `robots.txt` verificado?

**Sim** (DIEESE, o único site raspado).

**URL do `robots.txt`:**  
`https://www.dieese.org.br/robots.txt`

**Data da verificação:**  
18/09/2026.

**Resultado da verificação:**  
`User-agent: *` com `Crawl-delay: 10` e `Disallow` apenas para `/cedoc/`, `/cedocadm/`, `/http/cgi-bin/`, `/cgi-bin/`, `/bol/`, `/phprojekt/`, `/bugzilla/` e `/canal/`. O caminho usado na coleta (`/analisecestabasica/`) **não está bloqueado** → coleta autorizada. A coleta aplica pausa de 10 s entre requisições, conforme o `Crawl-delay`.

### Cuidados com os servidores

- DIEESE: 1 requisição à página de índice + 1 por boletim, com **pausa de 10 s** (Crawl-delay), `User-Agent` identificando o projeto e reuso local dos arquivos já baixados (não re-baixa o que já existe).
- SIDRA: 5 requisições GET (uma por tabela), sem paginação, sem volume excessivo.
- TSE: pausa de 1,5 s entre requisições (fluxo testado, não executado de novo nesta entrega).

---

## A.7 Arquivos da entrega

Caminhos relativos à pasta `projeto/documentacao/`.

| Artefato | Caminho | Status |
|---|---|---|
| Notebook/scripts de coleta IBGE (API) | `../../notebook_ipca_alimentacao_1994_2026.py` | OK |
| Notebook/scripts de coleta DIEESE (scraping) | `../../Dados do DIEESE/coletaDados.ipynb` (+ `coletaDeDados.py`, `limpezaHTML.py`, `limpezaPDF.py`, `especifico201001html.py`) | OK |
| Notebook de coleta consolidado | `../../notebook_coleta.ipynb` | A consolidar (rascunho) |
| Dados brutos da API (IBGE/SIDRA) | `../dados_brutos/sidra_t{58,655,2938,1419,7060}_alimentacao_20260914_190056.json` | OK |
| Dados brutos do scraping (DIEESE) | `../../dados_brutos/dieese/*.pdf` (260), `../../dados_brutos/dieese/provenance_log.csv`, `../../Dados do DIEESE/dados_Coletados.csv` | OK |
| Dados brutos da API (TSE/Dados Abertos) | `../dados_brutos/tse/*.zip` | Pendente (não presente) |
| Base tratada | `../dados_tratados/base_integrada.{parquet,csv}` (+ `cesta_basica_dieese_tratada.*`, `ipca_alimentacao_tratada.*`, `log_duplicatas_removidas.csv`) | OK |
| Tratamento/integração (código) | `../../notebook_tratamento_base_integrada.py` | OK |
| Registro de proveniência | `proveniencia.csv` | OK |
| Dataset card | `dataset_card.md` | OK |