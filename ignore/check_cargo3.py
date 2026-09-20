import zipfile
from pathlib import Path
from collections import Counter

tse_dir = Path("projeto/dados_brutos/tse")

cargo_counter = Counter()
cargo_names = {}

for zip_file in sorted(tse_dir.glob("Candidatos_*.zip")):
    with zipfile.ZipFile(zip_file, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        with zf.open(csv_files[0]) as f:
            header = f.readline().decode("utf-8", errors="ignore").strip()
            fields = [h.strip().strip('"') for h in header.split(";")]

            # Find indices
            try:
                idx_cargo = fields.index("CD_CARGO")
                idx_cargo_name = fields.index("DS_CARGO")
                idx_ano = fields.index("ANO_ELEICAO")
                idx_sit = fields.index("CD_SIT_TOT_TURNO")
            except ValueError as e:
                print(f"Missing field in {zip_file.name}: {e}")
                continue

            for line in f:
                values = line.decode("utf-8", errors="ignore").strip().split(";")
                if len(values) <= max(idx_cargo, idx_cargo_name, idx_ano, idx_sit):
                    continue
                cargo = values[idx_cargo]
                cargo_names[cargo] = values[idx_cargo_name]
                cargo_counter[cargo] += 1
                if sum(cargo_counter.values()) > 5000:
                    break

print("Unique CD_CARGO values (first files):")
for cargo, count in sorted(cargo_counter.items()):
    name = cargo_names.get(cargo, "?")
    print(f"  CD_CARGO={cargo}: {name} ({count} samples)")

# Now check SIT values from just one file
print("\nCD_SIT_TOT_TURNO from Candidatos_1994.zip:")
sit_counter = Counter()
sit_names = {}
with zipfile.ZipFile(tse_dir / "Candidatos_1994.zip", "r") as zf:
    csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
    with zf.open(csv_files[0]) as f:
        header = f.readline().decode("utf-8", errors="ignore").strip()
        fields = [h.strip().strip('"') for h in header.split(";")]
        idx_cargo = fields.index("CD_CARGO")
        idx_cargo_name = fields.index("DS_CARGO")
        idx_sit = fields.index("CD_SIT_TOT_TURNO")
        idx_sit_name = fields.index("DS_SIT_TOT_TURNO")

        for line in f:
            values = line.decode("utf-8", errors="ignore").strip().split(";")
            if len(values) <= max(idx_cargo, idx_sit):
                continue
            sit = values[idx_sit]
            sit_names[sit] = values[idx_sit_name]
            sit_counter[sit] += 1
            if sum(sit_counter.values()) > 2000:
                break

for sit, count in sorted(sit_counter.items()):
    name = sit_names.get(sit, "?")
    print(f"  {sit} = {name}: {count}")
