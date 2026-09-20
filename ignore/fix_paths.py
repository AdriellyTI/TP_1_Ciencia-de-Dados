import json
from pathlib import Path

NOTEBOOK = Path("notebook_coleta.ipynb")

with open(NOTEBOOK, "r", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# --- Fix Cell 8: add csv, re, pdfplumber imports needed by DIEESE sections ---
cell8_src = cells[8]["source"]
if isinstance(cell8_src, str):
    cell8_src = [cell8_src]
src_text = "".join(cell8_src)

# Add csv import if missing
if "import csv" not in src_text:
    src_text = src_text.replace("import requests\n", "import requests\nimport csv\n")

# Add re import if missing
if "import re" not in src_text:
    src_text = src_text.replace("import requests\nimport csv\n", "import requests\nimport csv\nimport re\n")

# Add pdfplumber import if missing
if "import pdfplumber" not in src_text:
    src_text = src_text.replace("import pyarrow as pa\n", "import pdfplumber\nimport pyarrow as pa\n")

cells[8]["source"] = src_text

# --- Fix Cells 14, 15, 16, 21, 22: update paths for consistency ---
# Replace "dados_brutos/dieese" with "BRUTOS_DIR / \"dieese\"" in code cells
# Replace "dados_brutos/dieese/" with "projeto/dados_brutos/dieese/" in markdown cells

for idx in [14, 15, 16, 21, 22]:
    cell = cells[idx]
    src = cell["source"]
    if isinstance(src, str):
        src = [src]

    new_src = []
    for line in src:
        # Code cells: use BRUTOS_DIR paths
        if cell["cell_type"] == "code":
            line = line.replace('Path("dados_brutos/dieese")', 'BRUTOS_DIR / "dieese"')
            line = line.replace('"dados_brutos/dieese/', 'str(BRUTOS_DIR / "dieese") + "/"')
            line = line.replace('"dados_brutos/dieese"', 'str(BRUTOS_DIR / "dieese")')
            line = line.replace("dados_brutos/dieese/", "BRUTOS_DIR / \"dieese\" /")
            line = line.replace("pasta = Path(\"dados_brutos/dieese\")", "pasta = BRUTOS_DIR / \"dieese\"")
            line = line.replace("pasta = Path('dados_brutos/dieese')", "pasta = BRUTOS_DIR / \"dieese\"")
        # Markdown cells: use project-relative paths
        else:
            line = line.replace("`dados_brutos/dieese/", "`projeto/dados_brutos/dieese/")
            line = line.replace("`dados_brutos/dieese`", "`projeto/dados_brutos/dieese`")
        new_src.append(line)

    cells[idx]["source"] = new_src

# Write back
with open(NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Paths and imports fixed!")

# Verify
for i in [8, 14, 15, 16, 21, 22]:
    c = cells[i]
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    print(f"\n--- Cell {i} ({c['cell_type']}) ---")
    print(src[:200])
