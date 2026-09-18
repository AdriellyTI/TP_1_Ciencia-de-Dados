import pdfplumber
import pandas as pd
import re
from pathlib import Path

def normalizar_tempo(texto):
    """Troca '111h 57min' por '111h57m' (formato único, compacto)."""
    return re.sub(r'(\d+)h\s*(\d+)\s*(?:min|m)\b', r'\1h\2m', texto)

def numero(t):
    """Converte texto tipo '1.234,56' em float. '(---)' vira None (dado inexistente)."""
    if t in ("NA", "(---)"):
        return None
    t = t.rstrip('%')
    try:
        return float(t.replace(',', '.'))
    except ValueError:
        return None

def parse_linha_generico(linha):
    """Reconhece cada campo pela posição relativa aos outros, não pela ordem fixa.
    Regra: 'tempo' tem o formato Xh Ym; 'valor' é o único número > 100; 'pct_sal'
    fica sempre colado no 'tempo'; 'var_mensal' fica sempre colado no 'valor'."""
    linha = normalizar_tempo(linha.strip())
    m_capital = re.match(r'^([^\d(\-]+)\s*(?:\(\d+\)\s*)?(.*)$', linha)
    if not m_capital:
        return None
    capital, resto = m_capital.groups()
    capital = capital.strip()
    tokens = resto.split()
    if len(tokens) < 4:
        return None

    idx_tempo = next((i for i, t in enumerate(tokens) if re.match(r'^\d+h\d+m$', t)), None)
    if idx_tempo is None:
        return None
    idx_valor = next((i for i, t in enumerate(tokens) if i != idx_tempo and (numero(t) or 0) > 100), None)
    if idx_valor is None:
        return None

    vizinhos_tempo = [i for i in (idx_tempo - 1, idx_tempo + 1) if 0 <= i < len(tokens) and i != idx_valor]
    idx_pct = vizinhos_tempo[0] if vizinhos_tempo else None
    vizinhos_valor = [i for i in (idx_valor - 1, idx_valor + 1) if 0 <= i < len(tokens) and i not in (idx_tempo, idx_pct)]
    idx_var_mensal = vizinhos_valor[0] if vizinhos_valor else None
    if idx_pct is None or idx_var_mensal is None:
        return None

    usados = {idx_tempo, idx_valor, idx_pct, idx_var_mensal}
    sobra = [i for i in range(len(tokens)) if i not in usados]
    var_ano, var_12 = None, None
    if len(sobra) == 1:
        if sobra[0] < idx_valor:
            var_ano = numero(tokens[sobra[0]])
        else:
            var_12 = numero(tokens[sobra[0]])
    elif len(sobra) >= 2:
        var_ano = numero(tokens[sobra[0]])
        var_12 = numero(tokens[sobra[1]])

    return {"capital": capital, "valor": numero(tokens[idx_valor]), "var_mensal": numero(tokens[idx_var_mensal]),
            "pct_sal": numero(tokens[idx_pct]), "tempo": tokens[idx_tempo], "var_ano": var_ano, "var_12": var_12}

def linhas_da_pagina(pagina, tolerancia=3):
    """Junta palavras na mesma linha visual, mesmo com pequenas variações de posição (sub-pixel)."""
    palavras = sorted(pagina.extract_words(x_tolerance=2, y_tolerance=3), key=lambda w: w["top"])
    linhas, atual, ultimo_top = [], [], None
    for p in palavras:
        if ultimo_top is not None and p["top"] - ultimo_top > tolerancia:
            linhas.append(atual)
            atual = []
        atual.append(p)
        ultimo_top = p["top"]
    if atual:
        linhas.append(atual)
    return [" ".join(w["text"] for w in sorted(g, key=lambda w: w["x0"])) for g in linhas]

def linhas_validas_da_pagina(pagina):
    return [c for c in (parse_linha_generico(l) for l in linhas_da_pagina(pagina)) if c]

def extrair_tabela_pdf(caminho_arquivo):
    with pdfplumber.open(caminho_arquivo) as pdf:
        paginas = pdf.pages
        for i, pagina in enumerate(paginas):
            candidatos = linhas_validas_da_pagina(pagina)
            if len(candidatos) >= 9:
                if i + 1 < len(paginas):
                    ja_achadas = {c["capital"] for c in candidatos}
                    continuacao = linhas_validas_da_pagina(paginas[i + 1])
                    novos = [c for c in continuacao if c["capital"] not in ja_achadas]
                    if 0 < len(novos) <= 15:
                        candidatos += novos
                df = pd.DataFrame(candidatos)
                df["aammes"] = Path(caminho_arquivo).stem
                return df
    return None

# --- roda em TODOS os PDFs ---
pasta = Path("dados_brutos/dieese")
arquivos_pdf = sorted(pasta.glob("*.pdf"))
print("Total de PDFs encontrados:", len(arquivos_pdf))

tabelas, falharam = [], []
for caminho in arquivos_pdf:
    df = extrair_tabela_pdf(str(caminho))
    (tabelas if df is not None else falharam).append(df if df is not None else caminho.name)

base_pdf = pd.concat(tabelas, ignore_index=True)
print("\nTotal de linhas extraídas:", len(base_pdf))
print("Meses que falharam:", falharam if falharam else "nenhum!")
print("\nFaixa de preço da cesta:")
print(base_pdf['valor'].describe()[['min', 'max']])
print("\nContagem de capitais por mês:")
print(base_pdf.groupby('aammes').size().value_counts().sort_index())

base_pdf.to_csv("base_tratada_dieese_completa.csv", index=False, encoding="utf-8-sig")
print("\nSalvo em base_tratada_dieese_completa.csv")

linha_200507 = [
    {"capital": "Natal", "var_mensal": 0.36, "valor": 140.25, "pct_sal": 50.62, "tempo": "102h51m", "var_ano": 6.41, "var_12": -0.15},
    {"capital": "João Pessoa", "var_mensal": -0.09, "valor": 143.91, "pct_sal": 51.94, "tempo": "105h32m", "var_ano": 14.10, "var_12": 2.25},
    {"capital": "Florianópolis", "var_mensal": -1.23, "valor": 163.81, "pct_sal": 59.13, "tempo": "120h08m", "var_ano": 4.06, "var_12": 0.79},
    {"capital": "Vitória", "var_mensal": -1.47, "valor": 160.50, "pct_sal": 57.93, "tempo": "117h42m", "var_ano": 5.33, "var_12": 4.63},
    {"capital": "Belo Horizonte", "var_mensal": -1.90, "valor": 164.87, "pct_sal": 59.51, "tempo": "120h54m", "var_ano": 8.27, "var_12": -2.78},
    {"capital": "Salvador", "var_mensal": -1.99, "valor": 134.23, "pct_sal": 48.45, "tempo": "98h26m", "var_ano": 6.67, "var_12": -1.29},
    {"capital": "Rio de Janeiro", "var_mensal": -2.12, "valor": 168.60, "pct_sal": 60.86, "tempo": "123h38m", "var_ano": 1.95, "var_12": 0.04},
    {"capital": "São Paulo", "var_mensal": -2.69, "valor": 178.22, "pct_sal": 64.33, "tempo": "130h42m", "var_ano": 3.50, "var_12": 2.45},
    {"capital": "Belém", "var_mensal": -2.86, "valor": 149.46, "pct_sal": 53.95, "tempo": "109h36m", "var_ano": -0.16, "var_12": -2.65},
    {"capital": "Goiânia", "var_mensal": -3.02, "valor": 152.68, "pct_sal": 55.11, "tempo": "111h58m", "var_ano": 2.55, "var_12": 3.78},
    {"capital": "Curitiba", "var_mensal": -3.08, "valor": 163.21, "pct_sal": 58.91, "tempo": "119h41m", "var_ano": 4.68, "var_12": -1.37},
    {"capital": "Fortaleza", "var_mensal": -3.38, "valor": 140.29, "pct_sal": 50.64, "tempo": "102h53m", "var_ano": 12.47, "var_12": -2.70},
    {"capital": "Recife", "var_mensal": -3.40, "valor": 143.40, "pct_sal": 51.76, "tempo": "105h10m", "var_ano": 16.59, "var_12": 1.29},
    {"capital": "Porto Alegre", "var_mensal": -4.01, "valor": 174.75, "pct_sal": 63.08, "tempo": "128h09m", "var_ano": 0.00, "var_12": -3.89},
    {"capital": "Brasília", "var_mensal": -4.55, "valor": 165.14, "pct_sal": 59.61, "tempo": "121h06m", "var_ano": -2.13, "var_12": 0.07},
    {"capital": "Aracaju", "var_mensal": -5.07, "valor": 139.92, "pct_sal": 50.50, "tempo": "102h36m", "var_ano": 6.56, "var_12": 1.13},
]
df_200507 = pd.DataFrame(linha_200507)
df_200507["aammes"] = "200507"

# junta com a base que já tem tudo
base_pdf = pd.concat([base_pdf, df_200507], ignore_index=True)
base_pdf.to_csv("base_tratada_dieese_completa.csv", index=False, encoding="utf-8-sig")
print("Total final:", len(base_pdf), "linhas,", base_pdf['aammes'].nunique(), "meses")