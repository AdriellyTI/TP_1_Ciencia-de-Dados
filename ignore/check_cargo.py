import zipfile
import pandas as pd
import json
from pathlib import Path

tse_dir = Path("projeto/dados_brutos/tse")

# Check CD_CARGO values from one file
zip_file = tse_dir / "Candidatos_1994.zip"
with zipfile.ZipFile(zip_file, "r") as zf:
    csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
    with zf.open(csv_files[0]) as f:
        header = f.readline().decode("utf-8", errors="ignore").strip()
        fields = [h.strip('"') for h in header.split(";")]
        idx = {name: i for i, name in enumerate(fields)}
        print("CD_CARGO index:", idx.get("CD_CARGO"))
        print("DS_CARGO index:", idx.get("DS_CARGO"))
        print("CD_SIT_TOT_TURNO index:", idx.get("CD_SIT_TOT_TURNO"))
        print("DS_SIT_TOT_TURNO index:", idx.get("DS_SIT_TOT_TURNO"))
        print("SG_PARTIDO index:", idx.get("SG_PARTIDO"))
        print("NM_PARTIDO index:", idx.get("NM_PARTIDO"))
        print("NR_PARTIDO index:", idx.get("NR_PARTIDO"))
        print("ANO_ELEICAO index:", idx.get("ANO_ELEICAO"))
        print("SG_UF index:", idx.get("SG_UF"))
        print("SQ_COLIGACAO index:", idx.get("SQ_COLIGACAO"))
        print("NM_COLIGACAO index:", idx.get("NM_COLIGACAO"))

        # Read first few data rows
        for i, line in enumerate(f):
            if i >= 5:
                break
            values = line.decode("utf-8", errors="ignore").strip().split(";")
            cargo = values[idx["CD_CARGO"]] if idx["CD_CARGO"] < len(values) else "?"
            desc = values[idx["DS_CARGO"]] if idx["DS_CARGO"] < len(values) else "?"
            sit = values[idx["CD_SIT_TOT_TURNO"]] if idx["CD_SIT_TOT_TURNO"] < len(values) else "?"
            print(f"  Row {i}: CD_CARGO={cargo}, DS_CARGO={desc}, CD_SIT={sit}")

# Also check Coligacoes
zip_file = tse_dir / "Coligações_2018.zip"
with zipfile.ZipFile(zip_file, "r") as zf:
    csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
    with zf.open(csv_files[0]) as f:
        header = f.readline().decode("utf-8", errors="ignore").strip()
        fields = [h.strip('"') for h in header.split(";")]
        idx = {name: i for i, name in enumerate(fields)}
        print("\nColigacoes fields:")
        for name in ["ANO_ELEICAO", "CD_CARGO", "DS_CARGO", "SG_PARTIDO", "NM_PARTIDO", "SQ_COLIGACAO", "NM_COLIGACAO", "SG_UF"]:
            print(f"  {name}: index {idx.get(name)}")
