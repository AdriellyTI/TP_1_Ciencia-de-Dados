import requests, re, time
from pathlib import Path

BASE = "https://www.dieese.org.br"
HEADERS = {"User-Agent": "Projeto-UFAM/1.0"}
pasta = Path("dados_brutos/dieese")

def achar_pdf_real(caminho_html):
    """Se o .html for uma página-casca, devolve o link do PDF real escondido nela."""
    texto = caminho_html.read_text(encoding="iso-8859-1", errors="ignore")
    if "Resultados Mensais de" not in texto:
        return None
    m = re.search(r'href="([^"]*cestabasica\.pdf)"', texto)
    if m:
        href = m.group(1)
        return href if href.startswith("http") else BASE + href
    return None

arquivos_html = sorted(pasta.glob("*.html"))
print("Total de .html encontrados:", len(arquivos_html))



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
        arquivo_html.unlink()  # apaga a casca, já que o PDF real tomou o lugar dela
        convertidos.append(arquivo_html.name)
        print(arquivo_html.name, "-> convertido para", novo_caminho.name)
    else:
        falharam.append((arquivo_html.name, r.status_code))
        print(arquivo_html.name, "-> falhou ao baixar PDF, status", r.status_code)

    time.sleep(10)  # respeita o Crawl-delay do robots.txt

print("\nConvertidos para PDF:", len(convertidos))
print("Mantidos como HTML de verdade:", len(mantidos), mantidos)
print("Falharam:", falharam if falharam else "nenhum")