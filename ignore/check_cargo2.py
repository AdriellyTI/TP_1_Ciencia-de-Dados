import zipfile
import pandas as pd
from pathlib import Path
from collections import Counter

tse_dir = Path("projeto/dados_brutos/tse")

# Check all unique CD_CARGO values across files
cargo_counter = Counter()
cargo_names = {}

for zip_file in sorted(tse_dir.glob("Candidatos_*.zip")):
    with zipfile.ZipFile(zip_file, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        with zf.open(csv_files[0]) as f:
            header = f.readline().decode("utf-8", errors="ignore").strip()
            fields = [h.strip('"') for h in header.split(";")]
            idx = {name: i for i, name in enumerate(fields)}
            
            df = pd.read_csv(zipfile.ZipFile(zip_file, "r").open(csv_files[0]), sep=";", dtype=str,
                           usecols=[idx["CD_CARGO"], idx["DS_CARGO"], idx["CD_SIT_TOT_TURNO"], idx["ANO_ELEICAO"]],
                           nrows=500)
            
            for _, row in df.iterrows():
                cargo = row["CD_CARGO"]
                cargo_names[cargo] = row["DS_CARGO"]
                cargo_counter[cargo] += 1

print("Unique CD_CARGO values:")
for cargo, count in sorted(cargo_counter.items()):
    name = cargo_names.get(cargo, "?")
    print(f"  CD_CARGO={cargo}: {name} ({count} samples)")

print("\nCD_SIT_TOT_TURNO values:")
sit_counter = Counter()
for zip_file in sorted(tse_dir.glob("Candidatos_1994.zip")):
    with zipfile.ZipFile(zip_file, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        with zf.open(csv_files[0]) as f:
            header = f.readline().decode("utf-8", errors="ignore").strip()
            fields = [h.strip('"') for h in header.split(";")]
            idx = {name: i for i, name in enumerate(fields)}
            df = pd.read_csv(zipfile.ZipFile(zip_file, "r").open(csv_files[0]), sep=";", dtype=str,
                           usecols=[idx["CD_SIT_TOT_TURNO"], idx["DS_SIT_TOT_TURNO"]],
                           nrows=1000)
            for _, row in df.iterrows():
                sit_counter[(row["CD_SIT_TOT_TURNO"], row["DS_SIT_TOT_TURNO"])] += 1

for (cd, ds), count in sorted(sit_counter.items()):
    print(f"  {cd} = {ds}: {count}")
