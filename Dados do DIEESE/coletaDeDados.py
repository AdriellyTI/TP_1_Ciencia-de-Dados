import requests, time, re, csv, os
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

BASE = "https://www.dieese.org.br"
INDEX_URL = f"{BASE}/analisecestabasica/analiseCestaBasicaAnteriores.html"
HEADERS = {"User-Agent": "Projeto-UFAM/1.0"}

Path("dados_brutos/dieese").mkdir(parents=True, exist_ok=True)
caminho_log = "dados_brutos/dieese/provenance_log.csv"
campos = ["aammes", "titulo", "url", "status_http", "formato", "coletado_em"]

arquivo_novo = not Path(caminho_log).exists()
arquivo_log = open(caminho_log, "a", newline="", encoding="utf-8")   # "a" = adicionar, não sobrescrever
escritor = csv.DictWriter(arquivo_log, fieldnames=campos)
if arquivo_novo:
    escritor.writeheader()

resposta = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
sopa = BeautifulSoup(resposta.text, "html.parser")
padrao = re.compile(r"(cestabasica\d{6}|\d{6}cestabasica)", re.IGNORECASE)
boletins = [(a.get_text(strip=True), a["href"]) for a in sopa.find_all("a", href=True) if padrao.search(a["href"])]

print("Total de boletins encontrados:", len(boletins))

for titulo, href in boletins:
    url = href if href.startswith("http") else BASE + href
    extensao = url.split(".")[-1]
    aammes = re.search(r"(\d{6})", url).group(1)

    caminho_html = f"dados_brutos/dieese/{aammes}.html"
    caminho_pdf = f"dados_brutos/dieese/{aammes}.pdf"

    # se já existe, registra no log usando a data do arquivo (ele foi baixado antes, só não tinha log)
    if Path(caminho_html).exists() or Path(caminho_pdf).exists():
        existente = caminho_html if Path(caminho_html).exists() else caminho_pdf
        hora = datetime.fromtimestamp(os.path.getmtime(existente)).strftime("%Y-%m-%d %H:%M:%S")
        escritor.writerow({"aammes": aammes, "titulo": titulo, "url": url, "status_http": 200,
                            "formato": existente.split(".")[-1],
                            "coletado_em": hora + " (recuperado, já existia no disco)"})
        arquivo_log.flush()
        print(aammes, "-> já existia, registrado no log")
        continue

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            with open(f"dados_brutos/dieese/{aammes}.{extensao}", "wb") as f:
                f.write(r.content)
            print(aammes, "-> salvo como", extensao)
        else:
            print(aammes, "-> falhou, status", r.status_code)
        escritor.writerow({"aammes": aammes, "titulo": titulo, "url": url,
                            "status_http": r.status_code, "formato": extensao,
                            "coletado_em": time.strftime("%Y-%m-%d %H:%M:%S")})
    except requests.exceptions.RequestException as erro:
        print(aammes, "-> erro de conexão, pulando:", erro)
        escritor.writerow({"aammes": aammes, "titulo": titulo, "url": url,
                            "status_http": "erro", "formato": extensao,
                            "coletado_em": time.strftime("%Y-%m-%d %H:%M:%S")})

    arquivo_log.flush()   # grava no arquivo IMEDIATAMENTE, sem esperar o loop acabar
    time.sleep(10)

arquivo_log.close()
print("Coleta finalizada.")