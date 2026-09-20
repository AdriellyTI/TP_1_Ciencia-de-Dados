import json
import re as re_module
from pathlib import Path

NOTEBOOK = Path("notebook_coleta.ipynb")

with open(NOTEBOOK, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Fix cell 8: add import re on its own line
c8 = nb["cells"][8]
src = "".join(c8["source"]) if isinstance(c8["source"], list) else c8["source"]
has_import_re = bool(re_module.search(r"^import re$", src, re_module.MULTILINE))
print("Cell 8 - Has import re (proper):", has_import_re)

if not has_import_re:
    src = src.replace("import csv\n", "import csv\nimport re\n", 1)
    c8["source"] = [src]
    print("Cell 8 - Added import re")

# Fix cell 16: broken print statement
c16 = nb["cells"][16]
src16 = "".join(c16["source"]) if isinstance(c16["source"], list) else c16["source"]
old_line = 'print("Arquivos em BRUTOS_DIR / "dieese" /:")'
new_line = 'print(f"Arquivos em {pasta}:")'
print("Cell 16 - Has broken line:", old_line in src16)
if old_line in src16:
    src16 = src16.replace(old_line, new_line)
    c16["source"] = [src16]
    print("Cell 16 - Fixed print statement")

# Also check cell 15 for any remaining issues
c15 = nb["cells"][15]
src15 = "".join(c15["source"]) if isinstance(c15["source"], list) else c15["source"]
# Verify no remaining bare "dados_brutos/dieese" paths
if "dados_brutos/dieese" in src15 and "BRUTOS_DIR" not in src15:
    print("Cell 15 - Warning: still has raw paths")
else:
    print("Cell 15 - OK")

with open(NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done!")
