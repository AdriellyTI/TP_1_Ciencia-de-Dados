import json
from pathlib import Path

NOTEBOOK = Path("notebook_coleta.ipynb")

with open(NOTEBOOK, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Verify JSON validity
json.dumps(nb, ensure_ascii=False)
print("JSON valid: True")
print(f"Cells: {len(nb['cells'])}")

# Fix cell 22: update section reference from "seções 3 e 4" to more accurate description
c22 = nb["cells"][22]
src22 = "".join(c22["source"]) if isinstance(c22["source"], list) else c22["source"]
old_ref = "# Implementado em coletaDados.ipynb (seções 3 e 4):"
new_ref = "# Implementado em coletaDados.ipynb (seções 2-5):"
if old_ref in src22:
    src22 = src22.replace(old_ref, new_ref)
    c22["source"] = [src22] if isinstance(c22["source"], list) else src22
    print("Cell 22: Updated section reference")

# Verify cell 8 imports
c8 = nb["cells"][8]
src8 = "".join(c8["source"]) if isinstance(c8["source"], list) else c8["source"]
imports = ["import requests", "import csv", "import re", "import pandas", "import pdfplumber"]
for imp in imports:
    present = imp in src8
    print(f"Cell 8 - {imp}: {'OK' if present else 'MISSING'}")

# Verify cell 16 print statement
c16 = nb["cells"][16]
src16 = "".join(c16["source"]) if isinstance(c16["source"], list) else c16["source"]
if "Arquivos em {pasta}" in src16:
    print("Cell 16 - Print statement: FIXED")
else:
    print("Cell 16 - Print statement: STILL BROKEN")

# Verify Section 6 has no "Preencher posteriormente"
c14 = nb["cells"][14]
src14 = "".join(c14["source"]) if isinstance(c14["source"], list) else c14["source"]
if "Preencher posteriormente" in src14:
    print("Cell 14 - WARNING: still has TODOs")
else:
    print("Cell 14 - No TODOs: OK")

# Verify no "Preencher posteriormente" in cells 15, 16, 21, 22
for idx in [15, 16, 21, 22]:
    c = nb["cells"][idx]
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "Preencher posteriormente" in src:
        print(f"Cell {idx} - WARNING: still has TODOs")
    else:
        print(f"Cell {idx} - No TODOs: OK")

with open(NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("\nNotebook saved!")
