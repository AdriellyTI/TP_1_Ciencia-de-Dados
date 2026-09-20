import json
import shutil
from pathlib import Path
import pandas as pd

# Remove empty dados_brutos at root
root_brutos = Path("dados_brutos")
if root_brutos.exists() and not any(root_brutos.iterdir()):
    root_brutos.rmdir()
    print("Removed empty dados_brutos/ at root")

# Final verification
print("\n" + "=" * 60)
print("FINAL PROJECT STRUCTURE")
print("=" * 60)

print("\nRoot:")
for p in sorted(Path(".").iterdir()):
    if p.is_file() and not p.name.startswith("."):
        print(f"  {p.name}")
    elif p.is_dir() and not p.name.startswith("."):
        items = list(p.iterdir())
        print(f"  {p.name}/ ({len(items)} items)")

print("\nprojeto/:")
proj = Path("projeto")
for p in sorted(proj.iterdir()):
    if p.is_file():
        print(f"  {p.name}")
    elif p.is_dir():
        items = list(p.iterdir())
        print(f"  {p.name}/ ({len(items)} items)")

print("\nKEY FILES CHECK:")
checks = [
    ("projeto/README.md", "README"),
    ("projeto/dados_tratados/tse_derivada_presidentes_governadores.csv", "TSE derived CSV"),
    ("projeto/dados_tratados/tse_derivada_presidentes_governadores.parquet", "TSE derived Parquet"),
    ("projeto/documentacao/dataset_card.md", "Dataset card"),
    ("projeto/documentacao/proveniencia.csv", "Proveniencia"),
    ("notebook_coleta.ipynb", "Main notebook"),
    ("coletaDados.ipynb", "DIEESE notebook"),
]
for path, name in checks:
    p = Path(path)
    if p.exists():
        if p.suffix == ".ipynb":
            try:
                with open(p, "r", encoding="utf-8") as f:
                    nb = json.load(f)
                ncells = len(nb.get("cells", []))
                print(f"  {name}: OK (valid JSON, {ncells} cells)")
            except Exception as e:
                print(f"  {name}: EXISTS but invalid ({e})")
        else:
            size = p.stat().st_size
            print(f"  {name}: OK ({size:,} bytes)")
    else:
        print(f"  {name}: MISSING")

# Verify TSE derived table content
df = pd.read_csv("projeto/dados_tratados/tse_derivada_presidentes_governadores.csv")
print(f"\nTSE derived table: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Years: {sorted(df['ANO_ELEICAO'].unique().tolist())}")
print(f"Office breakdown: President={len(df[df['CD_CARGO']==1])}, Governor={len(df[df['CD_CARGO']==3])}")
print(f"Election status breakdown: {df['CD_SIT_TOT_TURNO'].value_counts(dropna=False).to_dict()}")
personal_cols = [c for c in df.columns if any(k in c.upper() for k in ["CPF", "NASC", "TITULO"])]
print(f"Personal data columns: {personal_cols if personal_cols else 'NONE (correct!)'}")

# Check ignore folder
print(f"\nprojeto/ignore/ contents:")
for p in sorted(Path("projeto/ignore").iterdir()):
    print(f"  {p.name}")
