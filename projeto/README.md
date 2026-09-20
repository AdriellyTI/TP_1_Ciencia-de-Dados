# Trabalho 1 — Aquisição de Dados: Cesta Básica × Inflação dos Alimentos × Governos

## Descrição do projeto

Este repositório contém a coleta, integração e limpeza dos dados do trabalho 1 da disciplina de Ciência de Dados. O tema investiga a relação entre a variação dos preços da cesta básica, a inflação dos alimentos e as diferentes gestões presidenciais e estaduais no Brasil desde 1994, considerando ciclos eleitorais e espectros partidários.

Pergunta motivadora:

De que maneira a variação nos preços da cesta básica e a inflação dos alimentos se comportaram ao longo das diferentes gestões presidenciais e estaduais no Brasil desde 1994, e como os ciclos eleitorais e espectros partidários se correlacionam com esses momentos de instabilidade?

## Fontes de dados

- IBGE/SIDRA: IPCA do grupo Alimentação e bebidas, via API
- DIEESE: Pesquisa Nacional da Cesta Básica, via web scraping de HTML/PDF
- TSE/Dados Abertos: eleições presidenciais e governamentais, via API

## Integrantes

- Alonso Ramos de Brito Neto 
- Diego Gabriel Silva Azevedo 
- Luiz Henrique Barbosa Costa 
- Adrielly Silva de Souza

## Estrutura do projeto

```text
.
├── notebook_coleta.ipynb
├── dados_brutos/
│   ├── dieese/
│   ├── ibge_sidra/
│   ├── proveniencia/
│   └── tse/
├── dados_tratados/
│   ├── base_integrada.csv
│   └── base_integrada.parquet
├── documentacao/
│   ├── dataset_card.md
│   ├── proveniencia.csv
│   └── relatorio_aquisicao_dados.md
└── README.md
```

Os scripts auxiliares, o guia da disciplina e os arquivos de apoio ficam fora
da pasta de entrega, na raiz do workspace.

## Status atual

A base principal do projeto já está concluída e integrada:

- base DIEESE tratada em `projeto/dados_tratados/cesta_basica_dieese_tratada.csv`
- IPCA tratado em `projeto/dados_tratados/ipca_alimentacao_tratada.csv`
- base integrada com DIEESE, IPCA e contexto eleitoral em `projeto/dados_tratados/base_integrada.csv`

A parte do TSE foi concluída para o escopo analítico definido, com os dados brutos e a tabela derivada em:

- `projeto/dados_brutos/tse/`
- `projeto/dados_tratados/tse_derivada_presidentes_governadores.csv`
- `projeto/dados_tratados/tse_derivada_presidentes_governadores.parquet`

A coleta contém 255 arquivos ZIP, aproximadamente 6,38 GB e os anos eleitorais de 1994 a 2022. A tabela derivada contém 452 candidatos eleitos, sem colunas pessoais desnecessárias.

## Dependências

Python 3.10+ com as bibliotecas:

- requests
- beautifulsoup4
- pdfplumber
- pandas
- pyarrow

## Instruções de execução

### 1. Fonte 1 — IPCA (IBGE/SIDRA)

```bash
python notebook_ipca_alimentacao_1994_2026.py
```

### 2. Fonte 2 — Cesta básica (DIEESE)

Execute os scripts de coleta e limpeza do diretório `../Dados do DIEESE/`.

### 3. Tratamento e integração principal

```bash
python notebook_tratamento_base_integrada.py
```

### 4. TSE

A coleta, a derivação e a integração final do TSE já foram executadas. A metodologia e a proveniência estão registradas em `projeto/documentacao/relatorio_aquisicao_dados.md` e `projeto/dados_brutos/proveniencia/proveniencia_tse.csv`.

## Localização dos dados

| Tipo | Caminho |
|---|---|
| Brutos DIEESE | `dados_brutos/dieese/` |
| Brutos IBGE/SIDRA | `projeto/dados_brutos/` |
| Brutos TSE | `projeto/dados_brutos/tse/` |
| Base integrada principal | `projeto/dados_tratados/base_integrada.csv` |
| Base TSE derivada | `projeto/dados_tratados/tse_derivada_presidentes_governadores.csv` |
| Proveniência | `projeto/documentacao/proveniencia.csv` |
| Dataset card | `projeto/documentacao/dataset_card.md` |

## Observações

- Nenhum valor foi alterado de forma manual na base principal; flags foram usadas para sinalizar inconsistências.
- A base principal está pronta para uso.
- A base integrada tem 4.757 linhas e 35 colunas, preservando uma linha por capital/mês e adicionando o governo de referência por ano/UF.
- O TSE foi validado para o escopo analítico: 452 registros eleitos, oito anos eleitorais e nenhuma coluna pessoal identificada.
- O projeto deve garantir preservação dos dados brutos e registro de proveniência.

## Veja também

<<<<<<< HEAD
- `../ignore/GUIA_TRABALHO_1_AQUISICAO_DE_DADOS.md`
- `../ignore/README_tse.md`
- `projeto/documentacao/dataset_card.md`
- `projeto/documentacao/relatorio_aquisicao_dados.md`

## Minimização de dados TSE

A coleta original do TSE totalizou cerca de **6.38 GB** em 272 arquivos ZIP/CSV. Para o objetivo analítico do projeto — estudar a relação entre cesta básica, inflação e períodos de governo — apenas uma fração mínima desses dados é necessária.

**Dados mantidos para análise:**
- `projeto/dados_tratados/tse_derivada_presidentes_governadores.csv` — tabela derivada com 452 registros de presidentes e governadores eleitos (1994-2022), contendo partido, UF e coligação.

**Dados descartados da análise (mantidos apenas como referência bruta):**
- Votação por seção eleitoral (~1.9 GB)
- Votação nominal por município/zona (~1.7 GB)
- Votação por partido por município/zona (~111 MB)
- Bens de candidatos (~26 MB)
- Detalhes de apuração por município/zona (~28 MB)
- Notas fiscais de candidatos (~28 MB)
- Informações complementares e dados pessoais não necessários para a análise

**Justificativa:** a base derivada contém apenas variáveis necessárias para contextualizar períodos de governo e espectros partidários. Dados pessoais, como CPF, data de nascimento e título eleitoral, foram excluídos conforme princípios de minimização e uso acadêmico.
