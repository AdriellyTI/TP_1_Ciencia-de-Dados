import zipfile
import pandas as pd
import json
from pathlib import Path

tse_dir = Path("projeto/dados_brutos/tse")
tratados_dir = Path("projeto/dados_tratados")
tratados_dir.mkdir(parents=True, exist_ok=True)

# Columns to keep (no personal data)
keep_cols = [
    "ANO_ELEICAO", "CD_ELEICAO", "DS_ELEICAO", "DT_ELEICAO",
    "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "NR_TURNO",
    "TP_ABRANGENCIA", "SG_UF", "SG_UE", "NM_UE",
    "CD_CARGO", "DS_CARGO",
    "SQ_CANDIDATO", "NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO",
    "CD_SITUACAO_CANDIDATURA", "DS_SITUACAO_CANDIDATURA",
    "TP_AGREMIACAO",
    "NR_PARTIDO", "SG_PARTIDO", "NM_PARTIDO",
    "NR_FEDERACAO", "NM_FEDERACAO", "SG_FEDERACAO",
    "SQ_COLIGACAO", "NM_COLIGACAO", "DS_COMPOSICAO_COLIGACAO",
    "CD_SIT_TOT_TURNO", "DS_SIT_TOT_TURNO",
]

all_dfs = []
year_stats = {}

for ano in [1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022]:
    zip_file = tse_dir / f"Candidatos_{ano}.zip"
    if not zip_file.exists():
        print(f"Skipping {ano}: {zip_file.name} not found")
        continue

    print(f"\nProcessing {zip_file.name}...")
    year_dfs = []

    with zipfile.ZipFile(zip_file, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        for cf in csv_files:
            try:
                df = pd.read_csv(zf.open(cf), sep=";", dtype=str, low_memory=False, encoding="latin-1")
            except Exception as e:
                print(f"  Error reading {cf}: {e}")
                continue

            # Filter for President (CD_CARGO=1) and Governor (CD_CARGO=3) who were elected (CD_SIT_TOT_TURNO=1)
            filtered = df[
                df["CD_CARGO"].isin(["1", "3"]) &
                (df["CD_SIT_TOT_TURNO"] == "1") &
                (df["ANO_ELEICAO"].astype(str) == str(ano))
            ]

            if len(filtered) > 0:
                # Keep only relevant columns that exist
                cols_to_keep = [c for c in keep_cols if c in filtered.columns]
                filtered = filtered[cols_to_keep].copy()
                year_dfs.append(filtered)
                print(f"    {cf}: {len(filtered)} elected presidents/governors")

    if year_dfs:
        year_df = pd.concat(year_dfs, ignore_index=True)
        all_dfs.append(year_df)
        year_stats[ano] = len(year_df)
        print(f"  Year {ano}: {len(year_df)} total records")

if all_dfs:
    tse_derivada = pd.concat(all_dfs, ignore_index=True)

    # Convert types
    tse_derivada["ANO_ELEICAO"] = pd.to_numeric(tse_derivada["ANO_ELEICAO"], errors="coerce").astype("Int64")
    tse_derivada["CD_CARGO"] = pd.to_numeric(tse_derivada["CD_CARGO"], errors="coerce").astype("Int64")
    tse_derivada["NR_PARTIDO"] = pd.to_numeric(tse_derivada["NR_PARTIDO"], errors="coerce").astype("Int64")
    tse_derivada["NR_FEDERACAO"] = pd.to_numeric(tse_derivada["NR_FEDERACAO"], errors="coerce").astype("Int64")
    tse_derivada["CD_ELEICAO"] = pd.to_numeric(tse_derivada["CD_ELEICAO"], errors="coerce").astype("Int64")
    tse_derivada["NR_TURNO"] = pd.to_numeric(tse_derivada["NR_TURNO"], errors="coerce").astype("Int64")

    # Save as parquet (recommended for processed data)
    parquet_file = tratados_dir / "tse_derivada_presidentes_governadores.parquet"
    tse_derivada.to_parquet(parquet_file, index=False, compression="snappy")
    print(f"\nSaved: {parquet_file}")

    # Also save as CSV for accessibility
    csv_file = tratados_dir / "tse_derivada_presidentes_governadores.csv"
    tse_derivada.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print(f"Saved: {csv_file}")

    print(f"\n=== Summary ===")
    print(f"Total records: {len(tse_derivada)}")
    print(f"Years: {sorted(tse_derivada['ANO_ELEICAO'].dropna().unique().tolist())}")
    print(f"By year: {dict(year_stats)}")
    print(f"By office:")
    cargo_map = {1: "PRESIDENTE", 3: "GOVERNADOR"}
    for cd in sorted(tse_derivada["CD_CARGO"].dropna().unique()):
        count = len(tse_derivada[tse_derivada["CD_CARGO"] == cd])
        print(f"  {cargo_map.get(int(cd), cd)}: {count}")
    print(f"By party:")
    party_counts = tse_derivada.groupby(["ANO_ELEICAO", "SG_PARTIDO"]).size().reset_index(name="count")
    for _, row in party_counts.sort_values(["ANO_ELEICAO", "count"], ascending=[True, False]).head(20).iterrows():
        print(f"  {int(row['ANO_ELEICAO'])}: {row['SG_PARTIDO']} ({row['count']})")
    print(f"Columns: {list(tse_derivada.columns)}")
else:
    print("No data extracted!")
