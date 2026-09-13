# Dataset Card — Trabalho 1: Aquisição de Dados

## A.1 Identificação

**Nome da base:**  
`[Preencher com um nome curto e descritivo]`

**Grupo / integrantes:**

- Nome 1
- Nome 2
- Nome 3
- Nome 4

**Tema:**  
Análise da relação entre a variação dos preços da cesta básica, a inflação dos alimentos e os diferentes períodos de governos presidenciais e estaduais no Brasil desde 1994.

**Pergunta motivadora:**  
`[Preencher posteriormente]`

**Data ou período da coleta:**  
`[Preencher posteriormente com a data, hora e período da coleta]`

---

## A.2 Fontes e proveniência

### Fonte 1 — IBGE/SIDRA (API)

**Nome e URL:**  
`[Preencher posteriormente com a URL exata]`

**Método de aquisição:**  
API web.

**Endpoint e parâmetros:**  
`[Preencher posteriormente]`

**Dados coletados:**  
`[Preencher posteriormente]`

**Licença ou termos de uso:**  
`[Preencher posteriormente]`

**O uso pretendido é permitido?**  
`[Preencher posteriormente e justificar]`

**Arquivo bruto correspondente:**  
`[Preencher posteriormente com o caminho do arquivo em dados_brutos/]`

### Fonte 2 — DIEESE (web scraping)

**Nome e URL:**  
`[Preencher posteriormente com a URL exata]`

**Método de aquisição:**  
Web scraping de HTML.

**Página, tabela ou seletores utilizados:**  
`[Preencher posteriormente]`

**Dados coletados:**  
`[Preencher posteriormente]`

**Licença ou termos de uso:**  
`[Preencher posteriormente]`

**O uso pretendido é permitido?**  
`[Preencher posteriormente e justificar]`

**Arquivo bruto correspondente:**  
`[Preencher posteriormente com o caminho do arquivo em dados_brutos/]`

### Chave de integração

**Chave ou conjunto de chaves:**  
`[Preencher posteriormente]`

**Campo correspondente na fonte IBGE/SIDRA:**  
`[Preencher posteriormente]`

**Campo correspondente na fonte DIEESE:**  
`[Preencher posteriormente]`

**Normalizações realizadas:**  
`[Preencher posteriormente: acentos, maiúsculas, espaços, grafias, datas, códigos ou unidades]`

**Tipo de junção utilizado:**  
`[Preencher posteriormente: inner, left, right ou outro]`

**Tratamento dos registros sem correspondência:**  
`[Preencher posteriormente]`

---

## A.3 Dicionário de variáveis

Preencher uma linha para cada variável da base tratada.

| Variável | Tipo | Descrição | Unidade |
|---|---|---|---|
| `[nome_da_coluna]` | `[categórica, numérica contínua, numérica discreta, data/hora, texto ou booleana]` | `[Preencher posteriormente]` | `[Preencher posteriormente ou “não se aplica”]` |
| `[nome_da_coluna]` | `[Preencher posteriormente]` | `[Preencher posteriormente]` | `[Preencher posteriormente]` |
| `[nome_da_coluna]` | `[Preencher posteriormente]` | `[Preencher posteriormente]` | `[Preencher posteriormente]` |

---

## A.4 Volume e granularidade

**Número final de linhas:**  
`[Preencher posteriormente]`

**Número final de colunas:**  
`[Preencher posteriormente]`

**O que representa uma linha:**  
`[Preencher posteriormente: unidade de observação da base]`

**Cobertura temporal:**  
`[Preencher posteriormente]`

**Cobertura geográfica:**  
`[Preencher posteriormente]`

**Universo abrangido:**  
`[Preencher posteriormente]`

---

## A.5 Limitações e decisões

### Dados descartados

`[Descrever os registros, colunas ou períodos removidos e justificar cada descarte. Caso nenhum dado tenha sido descartado, informar “Nenhum dado descartado”.]`

### Lacunas conhecidas

`[Descrever valores faltantes, períodos ausentes, municípios ou estados não cobertos, vieses de cobertura e campos incompletos.]`

### Decisões de limpeza relevantes

`[Descrever conversões de tipos, padronizações, remoção de duplicatas, tratamento de valores ausentes, conversões de unidades e variáveis derivadas.]`

### Limitações das fontes

`[Descrever limitações da API, do site raspado, da periodicidade, da cobertura e da disponibilidade dos dados.]`

### Verificações de qualidade

`[Descrever as verificações realizadas antes e depois da integração.]`

---

## A.6 Considerações éticas

### Contém dados pessoais?

`[Responder sim ou não. Se sim, explicar quais dados foram encontrados, como foram minimizados ou anonimizados e quais cuidados foram adotados sob a LGPD.]`

### Restrições de uso e redistribuição

`[Descrever o que as licenças ou termos de uso permitem e proíbem, incluindo atribuição, redistribuição e uso acadêmico.]`

### `robots.txt` verificado?

`[Responder sim ou não.]`

**URL do `robots.txt`:**  
`[Preencher posteriormente]`

**Data da verificação:**  
`[Preencher posteriormente]`

**Resultado da verificação:**  
`[Descrever as regras encontradas e se os caminhos coletados estavam autorizados.]`

### Cuidados com os servidores

`[Descrever pausas entre requisições, limites respeitados, quantidade de páginas acessadas e medidas para evitar sobrecarga.]`

---

## A.7 Arquivos da entrega

| Artefato | Caminho | Status |
|---|---|---|
| Notebook de coleta | `../notebook_coleta.ipynb` | `[A preencher]` |
| Dados brutos da API | `../dados_brutos/[arquivo]` | `[A preencher]` |
| Dados brutos do scraping | `../dados_brutos/[arquivo]` | `[A preencher]` |
| Base tratada | `../dados_tratados/[arquivo]` | `[A preencher]` |
| Registro de proveniência | `proveniencia.csv` | `[A preencher]` |
| Dataset card | `dataset_card.md` | `[A preencher]` |
