import shutil
from pathlib import Path
import pandas as pd

BRUTOS = Path("projeto/dados_brutos")
TRATADOS = Path("projeto/dados_tratados")

print("=" * 60)
print("ORGANIZANDO dados_brutos/")
print("=" * 60)

# 1. IBGE/SIDRA: mover JSONs para ibge_sidra/
print("\n1. IBGE/SIDRA -> ibge_sidra/")
ibge_dir = BRUTOS / "ibge_sidra"
ibge_dir.mkdir(parents=True, exist_ok=True)

sidra_jsons = list(BRUTOS.glob("sidra_t*_alimentacao_*.json"))
for f in sidra_jsons:
    dest = ibge_dir / f.name
    f.rename(dest)
    print("  Moved: {}".format(f.name))

# Also move the raw IPCA JSON if exists
ipca_raw = BRUTOS / "sidra_t61_ipca_alimentacao_bruto.json"
if ipca_raw.exists():
    dest = ibge_dir / ipca_raw.name
    ipca_raw.rename(dest)
    print("  Moved: {}".format(ipca_raw.name))

# 2. Proveniencia: mover para proveniencia/
print("\n2. Proveniencia -> proveniencia/")
prov_dir = BRUTOS / "proveniencia"
prov_dir.mkdir(parents=True, exist_ok=True)

prov_files = list(BRUTOS.glob("proveniencia_*.csv"))
for f in prov_files:
    dest = prov_dir / f.name
    f.rename(dest)
    print("  Moved: {}".format(f.name))

# Also update references in proveniencia_tse.csv
prov_tse = prov_dir / "proveniencia_tse.csv"
if prov_tse.exists():
    df = pd.read_csv(prov_tse)
    df["arquivo_bruto"] = df["arquivo_bruto"].apply(
        lambda x: x.replace("dados_brutos/proveniencia_", "dados_brutos/proveniencia/")
        if "proveniencia_" in str(x) and "proveniencia_tse" not in str(x)
        else x
    )
    df.to_csv(prov_tse, index=False, encoding="utf-8")
    print("  Updated proveniencia_tse.csv paths")

# 3. IPCA tratado -> dados_tratados/
print("\n3. IPCA tratado -> dados_tratados/")
TRATADOS.mkdir(parents=True, exist_ok=True)

ipca_csv = BRUTOS / "ipca_alimentacao_1994_2026.csv"
ipca_parquet = BRUTOS / "ipca_alimentacao_1994_2026.parquet"

for f in [ipca_csv, ipca_parquet]:
    if f.exists():
        dest = TRATADOS / f.name
        f.rename(dest)
        print("  Moved: {} -> dados_tratados/".format(f.name))

# 4. Verificar estrutura final
print("\n4. Estrutura final de projeto/dados_brutos/:")
for item in sorted(BRUTOS.iterdir()):
    if item.is_dir():
        count = len(list(item.iterdir()))
        total = sum(f.stat().st_size for f in item.iterdir())
        print("  [DIR] {}/ ({} itens, {:.2f} MB)".format(item.name, count, total/1e6))
    elif item.is_file():
        print("  [FILE] {} ({} bytes)".format(item.name, item.stat().st_size))

# Update proveniencia CSV if it references moved files
# The proveniencia_tse.csv has paths like "dados_brutos/tse/..." which are still correct
# The proveniencia_sidra_*.csv might reference root-level files
for prov_file in prov_dir.glob("proveniencia_sidra_*.csv"):
    print("\n  Checking {}".format(prov_file.name))
    df = pd.read_csv(prov_file)
    print("  Columns: {}".format(list(df.columns)))
    print("  Rows: {}".format(len(df)))

print("\n" + "=" * 60)
print("ORGANIZACAO CONCLUIDA")
print("=" * 60)
