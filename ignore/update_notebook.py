import json
from pathlib import Path

NOTEBOOK = Path("notebook_coleta.ipynb")

with open(NOTEBOOK, "r", encoding="utf-8", errors="ignore") as f:
    nb = json.load(f)

cells = nb["cells"]

# --- New content for Section 6 (Fonte 2 — DIEESE) ---

section6_markdown = """## 6. Fonte 2 — DIEESE (Web Scraping)

### 6.1 Descrição da fonte

O DIEESE (Departamento Intersindical de Estatística e Estudos Socioeconômicos) publica mensalmente a **Pesquisa Nacional da Cesta Básica**, que registra o valor da cesta básica de alimentos em diversas capitais brasileiras, além do tempo de trabalho necessário para comprá-la e as variações mensais, anuais e em 12 meses.

A coleta dos boletins mensais é realizada a partir da página de índice de boletins anteriores do DIEESE, onde cada boletim está disponível como PDF (ou, em alguns casos, como página HTML intermediária que redireciona para o PDF). Todo o processo — coleta, limpeza de arquivos HTML "casca", extração de tabelas dos PDFs e correção manual de meses problemáticos — é documentado de forma reprodutível no notebook **`coletaDados.ipynb`**.

**Fonte dos dados:** [DIEESE — Análise da Cesta Básica](https://www.dieese.org.br/analisecestabasica/analiseCestaBasicaAnteriores.html)

> ⚠️ Este notebook faz requisições HTTP reais ao site do DIEESE e respeita um intervalo de 10 segundos entre downloads (conforme o `Crawl-delay` do `robots.txt` do site). Rodar o notebook do zero, portanto, pode levar bastante tempo dependendo de quantos boletins ainda não estiverem salvos localmente em `dados_brutos/dieese/`.

### 6.2 URL

- Página de índice de boletins: `https://www.dieese.org.br/analisecestabasica/analiseCestaBasicaAnteriores.html`

### 6.3 Estrutura HTML

A página de índice contém uma lista de links para boletins mensais, identificados pelo padrão `cestabasica` seguido ou precedido por 6 dígitos (formato `AAMMES`, ex: `202001`). Os boletins podem ser:

- **Arquivos PDF diretos**: baixados e salvos como `{aammes}.pdf`
- **Páginas HTML "casca"**: páginas intermediárias que apenas exibem um link para o PDF real. São identificadas pelo texto `"Resultados Mensais de"` e possuem o link do PDF real embutido em um tag `<a href="...cestabasica.pdf">`. Após baixar o PDF, o `.html` casca é removido.

### 6.4 Scraping

O processo de coleta segue os passos abaixo (implementação completa em `coletaDados.ipynb`):

1. Acessar a página de índice e extrair todos os links de boletins mensais via expressão regular `(cestabasica\\d{6}|\\d{6}cestabasica)`
2. Para cada boletim:
   - Se o arquivo (`.html` ou `.pdf`) já existir localmente, registrar no log de proveniência com a data de modificação do arquivo existente (**sem** re-baixar)
   - Caso contrário, baixar o arquivo via HTTP e salvar em `dados_brutos/dieese/{aammes}.{extensao}`
   - Registrar a proveniência (URL, status HTTP, formato, data/hora) em `dados_brutos/dieese/provenance_log.csv`
   - Respeitar o intervalo de **10 segundos** entre requisições (Crawl-delay do `robots.txt`)

```python
BASE = "https://www.dieese.org.br"
INDEX_URL = f"{BASE}/analisecestabasica/analiseCestaBasicaAnteriores.html"
HEADERS = {"User-Agent": "Projeto-UFAM/1.0"}

Path("dados_brutos/dieese").mkdir(parents=True, exist_ok=True)
caminho_log = "dados_brutos/dieese/provenance_log.csv"
campos = ["aammes", "titulo", "url", "status_http", "formato", "coletado_em"]

arquivo_novo = not Path(caminho_log).exists()
arquivo_log = open(caminho_log, "a", newline="", encoding="utf-8")
escritor = csv.DictWriter(arquivo_log, fieldnames=campos)
if arquivo_novo:
    escritor.writeheader()

# Baixar página de índice e extrair links de boletins
resposta = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
sopa = BeautifulSoup(resposta.text, "html.parser")
padrao = re.compile(r"(cestabasica\\d{6}|\\d{6}cestabasica)", re.IGNORECASE)
boletins = [(a.get_text(strip=True), a["href"]) for a in sopa.find_all("a", href=True) if padrao.search(a["href"])]

for titulo, href in boletins:
    url = href if href.startswith("http") else BASE + href
    extensao = url.split(".")[-1]
    aammes = re.search(r"(\\d{6})", url).group(1)
    # Lógica de download e registro de proveniência...
```

### 6.5 Salvamento dos dados brutos

- **Arquivos baixados**: `dados_brutos/dieese/{aammes}.pdf` e/ou `{aammes}.html`
- **Log de proveniência**: `dados_brutos/dieese/provenance_log.csv` (campos: aammes, titulo, url, status_http, formato, coletado_em)
- **Formato**: PDF (principal) e HTML (intermediário/casca)
- **Observação**: arquivos já existentes não são re-baixados; apenas registrados no log com data de modificação do arquivo em disco

"""

section6_scraping_code = """# 6.4 Scraping — coleta dos boletins mensais
# Acessa a página de índice, identifica links de boletins e baixa cada um,
# respeitando o intervalo de 10s entre requisições.

BASE = "https://www.dieese.org.br"
INDEX_URL = f"{BASE}/analisecestabasica/analiseCestaBasicaAnteriores.html"
HEADERS = {"User-Agent": "Projeto-UFAM/1.0"}
pasta = Path("dados_brutos/dieese")
pasta.mkdir(parents=True, exist_ok=True)

caminho_log = pasta / "provenance_log.csv"
campos = ["aammes", "titulo", "url", "status_http", "formato", "coletado_em"]

arquivo_novo = not caminho_log.exists()
arquivo_log = open(caminho_log, "a", newline="", encoding="utf-8")
escritor = csv.DictWriter(arquivo_log, fieldnames=campos)
if arquivo_novo:
    escritor.writeheader()

# Baixa a página de índice e extrai links de boletins mensais
resposta = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
sopa = BeautifulSoup(resposta.text, "html.parser")
padrao = re.compile(r"(cestabasica\\d{6}|\\d{6}cestabasica)", re.IGNORECASE)
boletins = [(a.get_text(strip=True), a["href"]) for a in sopa.find_all("a", href=True) if padrao.search(a["href"])]
print("Total de boletins encontrados:", len(boletins))

for titulo, href in boletins:
    url = href if href.startswith("http") else BASE + href
    extensao = url.split(".")[-1]
    aammes = re.search(r"(\\d{6})", url).group(1)
    caminho_html = pasta / f"{aammes}.html"
    caminho_pdf = pasta / f"{aammes}.pdf"

    if caminho_html.exists() or caminho_pdf.exists():
        existente = caminho_html if caminho_html.exists() else caminho_pdf
        hora = datetime.fromtimestamp(existente.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        escritor.writerow({"aammes": aammes, "titulo": titulo, "url": url, "status_http": 200,
                           "formato": existente.suffix[1:], "coletado_em": hora + " (recuperado, já existia)"})
        arquivo_log.flush()
        print(aammes, "-> já existia, registrado no log")
        continue

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            with open(pasta / f"{aammes}.{extensao}", "wb") as f:
                f.write(r.content)
            print(aammes, "-> salvo como", extensao)
        else:
            print(aammes, "-> falhou, status", r.status_code)
        escritor.writerow({"aammes": aammes, "titulo": titulo, "url": url,
                           "status_http": r.status_code, "formato": extensao,
                           "coletado_em": time.strftime("%Y-%m-%d %H:%M:%S")})
    except requests.exceptions.RequestException as erro:
        print(aammes, "-> erro, pulando:", erro)
        escritor.writerow({"aammes": aammes, "titulo": titulo, "url": url,
                           "status_http": "erro", "formato": extensao,
                           "coletado_em": time.strftime("%Y-%m-%d %H:%M:%S")})

    arquivo_log.flush()
    time.sleep(10)

arquivo_log.close()
print("Coleta finalizada.")
"""

section6_saving_code = """# 6.5 Salvamento dos dados brutos
# Arquivos brutos e proveniência já foram salvos durante o scraping (6.4).
# Verificação dos arquivos salvos:

print("Arquivos em dados_brutos/dieese/:")
for f in sorted(pasta.iterdir()):
    print(f"  {f.name} ({f.stat().st_size:,} bytes)")

print(f"\\nLog de proveniência: {caminho_log}")
if caminho_log.exists():
    with open(caminho_log, "r", encoding="utf-8") as lf:
        print(lf.read())
"""

section82_update = """### 8.2 Tratamento DIEESE

O tratamento dos dados do DIEESE segue três etapas principais, documentadas no notebook **`coletaDados.ipynb`**:

#### 8.2.1 Limpeza dos arquivos HTML ("cascas")

Alguns boletins baixados são páginas HTML intermediárias ("cascas") que apenas redirecionam para o PDF real. Esta etapa:

1. Varre todos os `.html` em `dados_brutos/dieese/`
2. Identifica cascas pelo texto `"Resultados Mensais de"`
3. Extrai o link do PDF real e baixa o PDF
4. Substitui o `.html` pelo `.pdf` correspondente (remove a casca)
5. HTMLs de conteúdo verdadeiro são mantidos

```python
def achar_pdf_real(caminho_html):
    texto = caminho_html.read_text(encoding="iso-8859-1", errors="ignore")
    if "Resultados Mensais de" not in texto:
        return None
    m = re.search(r'href="([^"]*cestabasica\\.pdf)"', texto)
    if m:
        href = m.group(1)
        return href if href.startswith("http") else BASE + href
    return None

arquivos_html = sorted(pasta.glob("*.html"))
convertidos, mantidos, falharam = [], [], []
for arquivo_html in arquivos_html:
    link_pdf = achar_pdf_real(arquivo_html)
    if link_pdf is None:
        mantidos.append(arquivo_html.name)
        continue
    r = requests.get(link_pdf, headers=HEADERS, timeout=30)
    if r.status_code == 200:
        novo_caminho = arquivo_html.with_suffix(".pdf")
        novo_caminho.write_bytes(r.content)
        arquivo_html.unlink()
        convertidos.append(arquivo_html.name)
    else:
        falharam.append((arquivo_html.name, r.status_code))
    time.sleep(10)
```

#### 8.2.2 Extração das tabelas dos PDFs

Cada boletim PDF contém uma tabela com uma linha por capital, com campos: valor da cesta básica, tempo de trabalho necessário, variações mensal/anual/12 meses e percentual em relação ao salário mínimo. A extração usa **pdfplumber** com parsing por posição relativa dos campos (não por ordem fixa de colunas), identificando:

- `tempo`: formato `XhYm`
- `valor`: único número > 100
- `pct_sal` e `var_mensal`: campos vizinhos

O parser é robusto a variações de layout entre meses. Exceção: **julho/2005** (`200507`) teve formatação divergente e foi transcrito manualmente.

```python
import pdfplumber

def extrair_tabela_pdf(caminho_arquivo):
    with pdfplumber.open(caminho_arquivo) as pdf:
        for i, pagina in enumerate(pdf.pages):
            candidatos = [c for c in (parse_linha_generico(l) for l in linhas_da_pagina(pagina)) if c]
            if len(candidatos) >= 9:
                if i + 1 < len(pdf.pages):
                    ja_achadas = {c["capital"] for c in candidatos}
                    novos = [c for c in (parse_linha_generico(l) for l in linhas_da_pagina(pdf.pages[i+1]))
                             if c["capital"] not in ja_achadas][:15]
                    candidatos += novos
                df = pd.DataFrame(candidatos)
                df["aammes"] = Path(caminho_arquivo).stem
                return df
    return None

arquivos_pdf = sorted(pasta.glob("*.pdf"))
tabelas = []
for caminho in arquivos_pdf:
    df = extrair_tabela_pdf(str(caminho))
    if df is not None:
        tabelas.append(df)
base_pdf = pd.concat(tabelas, ignore_index=True)
```

#### 8.2.3 Correção manual e exportação

O boletim de **julho/2005** (`200507`) não pôde ser extraído automaticamente (formatação divergente no PDF). Os 16 capitais foram transcritos manualmente a partir do PDF oficial e inseridos na base. A base final é exportada para `base_tratada_dieese_completa.csv`:

```python
linha_200507 = [
    {"capital": "Natal", "var_mensal": 0.36, "valor": 140.25, ...},
    # ... 16 capitais, transcritos manualmente
]
df_200507 = pd.DataFrame(linha_200507)
df_200507["aammes"] = "200507"
base_pdf = pd.concat([base_pdf, df_200507], ignore_index=True)
base_pdf.to_csv("base_tratada_dieese_completa.csv", index=False, encoding="utf-8-sig")
```

**Arquivo de saída**: `base_tratada_dieese_completa.csv` (~4.759 linhas, 16 capitais × N meses)

"""

section8_code = """# 8. Tratamento e padronização dos dados
#
# --- 8.1 Tratamento IBGE (Fonte 1) ---
# Implementado em notebook_ipca_alimentacao_1994_2026.py
#
# --- 8.2 Tratamento DIEESE (Fonte 2) ---
# Implementado em coletaDados.ipynb (seções 3 e 4):
#   - Limpeza de HTMLs "cascas" → PDFs
#   - Extração de tabelas dos PDFs (pdfplumber)
#   - Correção manual julho/2005
#   - Exportação: base_tratada_dieese_completa.csv
#
# --- 8.3 Padronização ---
# Preencher posteriormente.
"""

# --- Apply replacements ---
# Cell 14: Section 6 markdown header + stubs → full description
# Cell 15: # 6.4 Scraping stub → actual scraping code
# Cell 16: # 6.5 Salvamento stub → actual saving code
# Cell 21: Section 8 markdown (with stubs including 8.2) → updated with DIEESE details
# Cell 22: # 8. Treatment code stub → updated code

# Verify cell indices before replacing
for i in [14, 15, 16, 21, 22]:
    c = cells[i]
    src = c.get("source", "")
    if isinstance(src, list):
        src = "".join(src)[:60]
    print(f"Cell {i} ({c['cell_type']}): {src}")

print()

cells[14]["source"] = section6_markdown
cells[15]["source"] = section6_scraping_code
cells[16]["source"] = section6_saving_code
cells[21]["source"] = section82_update
cells[22]["source"] = section8_code

# Write back
with open(NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("notebook_coleta.ipynb updated successfully!")
print(f"Total cells: {len(cells)}")
