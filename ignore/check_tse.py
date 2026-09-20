import json
import zipfile
from pathlib import Path
from collections import Counter

tse_dir = Path("projeto/dados_brutos/tse")

# Check CKAN candidates JSON for 1994
print("=" * 60)
print("CKAN candidatos-1994")
print("=" * 60)
ckan_files = sorted(tse_dir.glob("ckan_candidatos-*_raw_*.json"))
for ckan_file in ckan_files:
    with open(ckan_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    result = data.get("result", {})
    resources = result.get("resources", [])
    print(f"\n{ckan_file.name}:")
    print(f"  Title: {result.get('title', 'N/A')}")
    print(f"  License: {result.get('license_id', 'N/A')}")
    print(f"  Resources: {len(resources)}")
    for r in resources:
        fmt = r.get("format", "?")
        size = r.get("size", "?")
        name = r.get("name", "?")
        print(f"    - {name}: {fmt} ({size} bytes)")

# Check TSE ZIP file categories
print("\n" + "=" * 60)
print("TSE ZIP file categories")
print("=" * 60)

zips = list(tse_dir.glob("*.zip"))
print(f"Total ZIPs: {len(zips)}")

# Categorize by type
categories = Counter()
uf_counts = Counter()
year_counts = Counter()

for f in zips:
    name = f.name.replace(".zip", "")
    parts = name.split("_")
    
    # Identify category
    if "Detalhe" in name:
        categories["Detalhe_da_apuracao"] += 1
    elif "Votacao_em_partido" in name:
        categories["Votacao_em_partido"] += 1
    elif "Votacao_nominal" in name:
        categories["Votacao_nominal"] += 1
    elif "Candidatos" in name:
        categories["Candidatos"] += 1
    elif "Coligacoes" in name:
        categories["Coligacoes"] += 1
    elif "Vagasp" in name or "Vagas" in name:
        categories["Vagas"] += 1
    elif "Bens" in name:
        categories["Bens_candidatos"] += 1
    elif "Notas" in name:
        categories["Notas_fiscais"] += 1
    elif "Presidente" in name or "Governador" in name:
        categories["Presidente_Governador"] += 1
    else:
        categories["Outro"] += 1
    
    # Extract UF
    for uf in ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP"]:
        if f"{uf}_-" in name or f"{uf}_" in name:
            uf_counts[uf] += 1
            break
    
    # Extract year
    for year in ["1994", "1998", "2002", "2006", "2010", "2014", "2018", "2022"]:
        if year in name:
            year_counts[year] += 1
            break

print("\nBy category:")
for cat, count in categories.most_common():
    print(f"  {cat}: {count}")

print("\nBy UF:")
for uf, count in uf_counts.most_common():
    print(f"  {uf}: {count}")

print("\nBy year:")
for year, count in sorted(year_counts.items()):
    print(f"  {year}: {count}")

# Check total size
total_size = sum(f.stat().st_size for f in zips)
print(f"\nTotal size: {total_size / 1e6:.2f} MB ({total_size / 1e9:.2f} GB)")

# Show non-UF specific files
print("\nNon-UF specific files:")
for f in sorted(zips):
    name = f.name
    # Check if it's NOT a state-specific file
    is_state_file = any(f"{uf}_-" in name or f"{uf}_" in name for uf in
        ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP"])
    if not is_state_file:
        print(f"  {name} ({f.stat().st_size / 1e6:.2f} MB)")
