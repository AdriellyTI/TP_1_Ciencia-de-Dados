# TSE — Aquisição de Dados Eleitorais

## Fonte

**Nome:** Portal de Dados Abertos do TSE / DivulgaCandContas  
**URL:**  
- CKAN API: `https://dadosabertos.tse.jus.br/api/3/action`  
- DivulgaCandContas REST: `https://divulgacandcontas.tse.jus.br/divulga/rest/v1`  

**Método:** API web (CKAN + REST)  

**Licença:** Creative Commons Atribuição (CC-BY)  

## Estratégia de Coleta

### 1. API CKAN (Descoberta de Metadados)

Utilizada para obter metadados dos datasets e URLs de download dos recursos:

- `package_search?q=candidatos` — busca datasets de candidatos
- `package_show?id=candidatos-{ano}` — metadados e recursos (URLs de download)
- `package_show?id=resultados-{ano}` — metadados e recursos de resultados

**Nota:** O endpoint CKAN (`dadosabertos.tse.jus.br`) é protegido por CDN Akamai com proteção anti-bot que eventualmente retorna HTTP 403. Foram utilizados:
- Sessão HTTP com cookies do site principal para contornar a proteção
- Retries automáticos com espera exponencial
- Acesso via `verify=False` quando necessário

### 2. API DivulgaCandContas (Dados de Eleições)

- `GET /eleicao/ordinarias` — lista todas as eleições ordinárias disponíveis
- Retorna 13 eleições (2026, 2024, 2022, 2020, 2018, 2016, 2014, 2012, 2010, 2008, 2006, 2004)

### 3. Download de Recursos (CDN)

Os recursos (arquivos ZIP/CSV) são hospedados em `cdn.tse.jus.br` e baixados diretamente via HTTP:
- Arquivos ZIP contendo CSVs (dados de candidatos por UF)
- Arquivos CSV individuais (resultados por seção eleitoral, etc.)
- Mantidos como bruto, sem transformação

## Anos Coletados

1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022 (eleições presidenciais e gubernamentais)

## Arquivos Brutos

### Localização

```
projeto/dados_brutos/tse/
├── ckan_candidatos-{ano}_raw_*.json    # Resposta bruta da API CKAN (16 arquivos)
├── ckan_resultados-{ano}_raw_*.json   # Resposta bruta da API CKAN
├── divulgacandcontas_eleicoes_ordinarias.json  # Lista de eleições
├── Candidatos_{ano}.csv               # Dados de candidatos (1 arquivo/ano)
├── Candidatos - Informações complementares_{ano}.csv
├── Coligações_{ano}.csv
├── Vagas_{ano}.csv
├── Bens_de_candidatos_{ano}.csv
├── Votação_nominal_por_município_e_zona_{ano}.csv
├── Votação_em_partido_por_município_e_zona_{ano}.csv
├── Votação_por_seção_eleitoral_{UF}_{ano}.csv
├── Detalhe_da_apuração_{...}_{ano}.csv
└── ... (287 arquivos no total, ~6.38 GB)
```

### Resumo por Ano

| Ano | Arquivos | Tamanho |
|---|---|---|
| 1994 | 14 | 55.3 MB |
| 1998 | 43 | 547.6 MB |
| 2002 | 43 | 609.1 MB |
| 2006 | 40 | 748.4 MB |
| 2010 | 42 | 528.5 MB |
| 2014 | 37 | 1,255.7 MB |
| 2018 | 62 | 1,775.6 MB |
| 2022 | 12 | 639.5 MB |
| **Total** | **296** | **6.38 GB** |

## Proveniência

- **Arquivo:** `projeto/dados_brutos/proveniencia_tse.csv`
- **Registros:** 241 (todos com status HTTP 200)
- **Campos:** fonte_id, dataset, endpoint, url, data_hora_coleta, status_http, arquivo_bruto, tamanho_bytes, recurso_nome, recurso_url, recurso_formato, observacoes

## Limitações

1. **CKAN API (dadosabertos.tse.jus.br):** Protegida por CDN Akamai com anti-bot. Acesso intermitente (HTTP 403). Contornada via sessão com cookies.
2. **Volume:** ~6.38 GB de dados brutos, principalmente devido aos arquivos de votação por seção eleitoral (estado por estado).
3. **Formato:** Arquivos CKAN reportam formato CSV mas são entregues como ZIP na CDN. Os arquivos baixados mantêm a extensão CSV conforme reportado pela API.
4. **Candidatos 2018 - Informações complementares:** Download inicial falhou (403), teve que ser retentado com headers diferentes.

## API Response Samples

Cada dataset possui sua resposta bruta da API CKAN salva em `ckan_{dataset}_raw_*.json`. Exemplo de conteúdo:

```json
{
  "help": "https://dadosabertos.tse.jus.br/api/3/action/help_show?name=package_show",
  "success": true,
  "result": {
    "name": "candidatos-1994",
    "title": "Candidatos - 1994",
    "license_id": "cc-by",
    "num_resources": 3,
    "resources": [...]
  }
}
```
