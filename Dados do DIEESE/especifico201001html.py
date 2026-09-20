import requests
from pathlib import Path

url = "https://www.dieese.org.br/analisecestabasica/2009/201001cestabasica.pdf"
r = requests.get(url, headers={"User-Agent": "Projeto-UFAM/1.0"}, timeout=30)

if r.status_code == 200:
    Path("dados_brutos/dieese/201001.pdf").write_bytes(r.content)
    Path("dados_brutos/dieese/201001.html").unlink(missing_ok=True)  # apaga a casca antiga
    print("Salvo com sucesso!")
else:
    print("Ainda deu erro, status:", r.status_code)