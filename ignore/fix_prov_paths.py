import pandas as pd
from pathlib import Path

BRUTOS = Path("projeto/dados_brutos")
prov_dir = BRUTOS / "proveniencia"

print("Atualizando caminhos nas proveniencias SIDRA...")

for prov_file in prov_dir.glob("proveniencia_sidra_*.csv"):
    df = pd.read_csv(prov_file)

    # Update arquivo_bruto paths
    updated = 0
    for idx, row in df.iterrows():
        arch = row.get("arquivo_bruto", "")
        if arch and not str(arch).startswith("dados_brutos"):
            # It's a relative path like "sidra_t58_..." -> needs "ibge_sidra/" prefix
            if "sidra_t" in str(arch):
                df.at[idx, "arquivo_bruto"] = "dados_brutos/ibge_sidra/{}".format(arch)
                updated += 1

    df.to_csv(prov_file, index=False, encoding="utf-8")
    print("  {}: {} caminhos atualizados".format(prov_file.name, updated))

# Also check proveniencia_tse.csv for any root-level references
prov_tse = prov_dir / "proveniencia_tse.csv"
if prov_tse.exists():
    df = pd.read_csv(prov_tse)
    print("\nproveniencia_tse.csv:")
    print("  Total: {} entries".format(len(df)))
    print("  HTTP 200: {}".format((df["status_http"].astype(str) == "200").sum()))

print("\nDone!")
