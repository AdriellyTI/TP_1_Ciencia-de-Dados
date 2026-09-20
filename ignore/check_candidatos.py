import zipfile
from pathlib import Path
from collections import Counter

tse_dir = Path("projeto/dados_brutos/tse")

# Check Candidatos ZIP structure for a few years
for year in [1994, 2006, 2022]:
    zip_file = tse_dir / f"Candidatos_{year}.zip"
    if not zip_file.exists():
        continue
    print(f"\n=== Candidatos_{year}.zip ({zip_file.stat().st_size/1e6:.2f} MB) ===")
    with zipfile.ZipFile(zip_file, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.lower().endswith(".csv")]
        print(f"CSV files: {len(csv_files)}")
        for cf in csv_files[:2]:
            print(f"\n  {cf}:")
            with zf.open(cf) as f:
                header = f.readline().decode("utf-8", errors="ignore").strip()
                fields = header.split(";")
                print(f"  Fields ({len(fields)}): {fields[:20]}")
                if len(fields) > 20:
                    print(f"  ... and {len(fields) - 20} more: {fields[20:]}")

# Also check Coligacoes
for year in [1998, 2018]:
    zip_file = tse_dir / f"Coligações_{year}.zip"
    if not zip_file.exists():
        continue
    print(f"\n=== Coligações_{year}.zip ({zip_file.stat().st_size/1e6:.2f} MB) ===")
    with zipfile.ZipFile(zip_file, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.lower().endswith(".csv")]
        print(f"CSV files: {len(csv_files)}")
        for cf in csv_files[:2]:
            print(f"\n  {cf}:")
            with zf.open(cf) as f:
                header = f.readline().decode("utf-8", errors="ignore").strip()
                fields = header.split(";")
                print(f"  Fields ({len(fields)}): {fields[:20]}")

# Check Vagas
zip_file = tse_dir / "Vagas_2022.zip"
if zip_file.exists():
    print(f"\n=== Vagas_2022.zip ({zip_file.stat().st_size/1e6:.2f} MB) ===")
    with zipfile.ZipFile(zip_file, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.lower().endswith(".csv")]
        print(f"CSV files: {len(csv_files)}")
        for cf in csv_files[:2]:
            print(f"\n  {cf}:")
            with zf.open(cf) as f:
                header = f.readline().decode("utf-8", errors="ignore").strip()
                fields = header.split(";")
                print(f"  Fields ({len(fields)}): {fields[:20]}")
