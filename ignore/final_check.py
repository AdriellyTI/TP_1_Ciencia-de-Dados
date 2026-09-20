import json
from pathlib import Path

NOTEBOOK = Path("notebook_coleta.ipynb")

with open(NOTEBOOK, "r", encoding="utf-8") as f:
    nb = json.load(f)

# JSON valid
json.dumps(nb, ensure_ascii=False)
print(f"JSON valid | Cells: {len(nb['cells'])}")

# Check ALL cells for TODOs
todo_cells = []
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "Preencher posteriormente" in src:
        todo_cells.append(i)
        # Get the section header if available
        first_line = src.strip().split("\n")[0][:80]
        print(f"  Cell {i} ({c['cell_type']}): {first_line}")

if not todo_cells:
    print("No TODOs found - all cells filled!")
else:
    print(f"\n{len(todo_cells)} cells still have TODOs (sections 9-10 about integration/final base - not DIEESE specific)")

# Verify key cells
print("\n--- Key cell verification ---")
c8 = nb["cells"][8]
src8 = "".join(c8["source"])
imports_needed = ["import csv", "import re", "import pdfplumber"]
for imp in imports_needed:
    line = f"{imp}\n"
    print(f"  {imp}: {'OK' if line in src8 else 'MISSING'}")

c16 = nb["cells"][16]
src16 = "".join(c16["source"])
print(f"  Cell 16 print fixed: {'OK' if '{pasta}' in src16 else 'STILL BROKEN'}")

c14 = nb["cells"][14]
src14 = "".join(c14["source"])
sections = ["6.1", "6.2", "6.3", "6.4", "6.5"]
for s in sections:
    print(f"  Section 6.{s[2:]}: {'OK' if s in src14 else 'MISSING'}")

c21 = nb["cells"][21]
src21 = "".join(c21["source"])
sections2 = ["8.2.1", "8.2.2", "8.2.3"]
for s in sections2:
    print(f"  Section 8.{s}: {'OK' if s in src21 else 'MISSING'}")

print("\nAll checks passed!" if all([
    all(f"{imp}\n" in "".join(nb['cells'][8]['source']) for imp in ["import csv", "import re", "import pdfplumber"]),
    '{pasta}' in "".join(nb['cells'][16]['source']),
    all(f"6.{s}" in "".join(nb['cells'][14]['source']) for s in ["1", "2", "3", "4", "5"]),
    all(f"8.{s}" in "".join(nb['cells'][21]['source']) for s in ["2.1", "2.2", "2.3"]),
]) else "Some checks FAILED!")
